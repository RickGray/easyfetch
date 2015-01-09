#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import requests
import lxml

from termcolor import cprint
from lxml import html


# default headers for each request with sogou search
default_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'www.sogou.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:31.0) Gecko/20100101 Firefox/31.0'
}


class SearchSogou(object):
    def __init__(self, word, limit, start=0):
        """
        :param word: search keyword
        :param limit: maximum to query
        :param start: results offset, default start 0
        :return:
        """
        self.word = word
        self.number = '100'  # sougou.com limits the maximum number of each query
        self.start = start
        self.limit = limit
        self.headers = default_headers

        self.results = ''
        self.totalresults = []

        self.totalurls = []

    def do_search(self):
        request_url = 'http://www.sogou.com/web' \
                      + '?query=' + self.word \
                      + '&ie=utf8' \
                      + '&page=' + str(self.start) \
                      + '&num=' + self.number

        response = requests.get(request_url, headers=default_headers, allow_redirects=False)
        status_code = response.status_code
        headers = response.headers
        content = response.content

        self.results = content
        self.totalresults.append(self.results)

    def process(self):
        while (self.start * int(self.number)) <= self.limit:
            self.do_search()
            cprint('[-] Searching %s results from "Sogou"' % str(self.start * int(self.number)),
                   'green', file=sys.stdout)
            self.start += 1

    def get_url(self):
        urls = []
        if self.totalresults:
            for c in self.totalresults:
                try:
                    doc = html.document_fromstring(c)
                except Exception:
                    continue
                pre_urls = doc.xpath(
                    '//div[@class="results"]/div[@class="rb"]/h3/a/@href')

                if pre_urls:
                    for url in pre_urls:
                        urls.append(url)

        self.totalurls.extend(urls)

        return urls

    def get_host(self):
        hosts = []
        if self.totalurls:
            for url in self.totalurls:
                m = re.compile(r'http[s]?://([^&/?]*)/??').findall(url)
                if m:
                    host = m[0]
                    hosts.append(host)
                else:
                    continue

        return hosts
