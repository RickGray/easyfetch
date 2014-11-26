#!/usr/bin/env python
# coding: utf-8

import requests
import re
import json
import sys

from lxml import html
from termcolor import cprint


# default headers for each request with CSE
default_headers_cse = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'www.googleapis.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:31.0) Gecko/20100101 Firefox/31.0'
}

# default headers for each request with google search
default_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'www.google.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:31.0) Gecko/20100101 Firefox/31.0'
}


class SearchGoogle(object):
    def __init__(self, word, limit, start=0):
        """
        :param word: search keyword
        :param limit: maximum to query
        :param start: results offset, default start 0
        :return:
        """
        self.word = word
        self.number = '100'  # google.com limits the maximum number of each query
        self.number_cse = '20'  # CSE limits the maximum number of each query
        self.start = start
        self.limit = limit
        self.headers = default_headers
        self.result_name = 'Info'

        self.results = ''
        self.totalresults = []
        self.totalresults_cse = []

    def do_search(self):
        """
        Normal search with google.com.
        Sometimes there will be verification code requests.
        When google verification code needed, instead of using the CES.
        """
        request_url = 'https://www.google.com/search?' \
                      + 'num=' + self.number \
                      + '&hl=en' \
                      + '&safe=off' \
                      + '&start=' + str(self.start) \
                      + '&q=' + self.word \
                      + '&gws_rd=ssl'

        response = requests.get(request_url, headers=default_headers, allow_redirects=False)
        status_code = response.status_code
        headers = response.headers

        if status_code == 302:
            if 'location' in headers:
                redirect_url = headers['location']
                m = re.compile(r'http[s]?://([^/]*)/?').findall(redirect_url)
                if m:
                    google_domain = m[0]

                    request_url = 'https://' + google_domain + '/search?' \
                                  + 'num=' + self.number \
                                  + '&hl=en' \
                                  + '&safe=off' \
                                  + '&start=' + str(self.start) \
                                  + '&q=' + self.word \
                                  + '&gws_rd=ssl'

                    headers['Host'] = google_domain
                    response = requests.get(request_url, headers=default_headers, allow_redirects=False)

        content = response.content

        self.results = content
        self.totalresults.append(self.results)

    def do_search_cse(self):
        """
        Special search with CSE (Custom Search Engine)[https://www.google.com/cse]
        The request params 'key' and 'cx' are the apiKey of GoogleAccount.
        """
        request_url = 'https://www.googleapis.com/customsearch/v1element?' \
                      + 'key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY' \
                      + '&num=' + self.number_cse \
                      + '&hl=en' \
                      + '&prettyPrint=false' \
                      + '&start=' + str(self.start) \
                      + '&cx=010360375284501702268:or-ucup9noi' \
                      + '&q=' + self.word \
                      + '&callback=' + self.result_name

        response = requests.get(request_url, headers=default_headers_cse, allow_redirects=False)
        status_code = response.status_code
        headers = response.headers
        content = response.content

        self.results = content
        self.totalresults_cse.append(self.results)

    def process(self):
        self.start = 0
        while (int(self.start) + int(self.number)) <= int(self.limit):
            self.do_search()
            cprint('[+] Searching %s results from Google' % str(int(self.start) + int(self.number)),
                   'green', file=sys.stdout)
            self.start += int(self.number)

    def process_cse(self):
        self.start = 0
        while (int(self.start) + int(self.number_cse)) <= int(self.limit):
            self.do_search_cse()
            cprint('[+] Searching %s results from Google (CSE)' % str(int(self.start) + int(self.number_cse)),
                   'green', file=sys.stdout)
            self.start += int(self.number_cse)

    def get_url(self):
        urls = []
        if self.totalresults:
            for c in self.totalresults:
                print c
                doc = html.document_fromstring(c)
                pre_urls = doc.xpath(
                    '//div[@id="ires"]/ol/div[@class="srg"]/li[@class="g"]/div[@class="rc"]/h3/a/@href')

                if pre_urls:
                    for url in pre_urls:
                        urls.append(url)

        return urls

    def get_url_cse(self):
        urls = []
        if self.totalresults_cse:
            for content in self.totalresults_cse:
                m = re.compile(r'%s\((.*)\);' % self.result_name).findall(content)
                if m:
                    content_dic = json.loads(m[0])
                    if 'results' not in content_dic:
                        continue

                    results_dic = content_dic['results']
                    for result in results_dic:
                        url = result['url']
                        if url:
                            urls.append(url)
                else:
                    continue

        return urls

    def get_host(self):
        urls = self.get_url()
        hosts = []
        if urls:
            for url in urls:
                m = re.compile(r'http[s]?://([^/]*/)').findall(url)
                if m:
                    hosts.append(m[0])
                else:
                    continue

        return hosts

    def get_host_cse(self):
        hosts = []
        if self.totalresults_cse:
            for content in self.totalresults_cse:
                m = re.compile(r'%s\((.*)\);' % self.result_name).findall(content)
                if m:
                    content_dic = json.loads(m[0])
                    if 'results' not in content_dic:
                        continue

                    results_dic = content_dic['results']
                    for result in results_dic:
                        host = result['visibleUrl']
                        if host:
                            hosts.append(host)
                else:
                    continue

        return hosts

if __name__ == '__main__':
    if sys.argv.__len__() < 3:
        cprint('Usage: %s <keyword> <limit>' % sys.argv[0])
        sys.exit()

    keyword = sys.argv[1]
    limitnum = sys.argv[2]
