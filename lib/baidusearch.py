#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import requests
import socket

from termcolor import cprint
from lxml import html
from multiprocessing.dummy import Pool as ThreadPool


# default headers for each request with baidu search
default_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'www.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:31.0) Gecko/20100101 Firefox/31.0'
}


class SearchBaidu(object):
    def __init__(self, word, limit, start=0):
        """
        :param word: search keyword
        :param limit: maximum to query
        :param start: results offset, default start 0
        :return:
        """
        self.word = word
        self.number = '100'  # baidu.com limits the maximum number of each query
        self.start = start
        self.limit = limit
        self.headers = default_headers

        self.results = ''
        self.totalresults = []

        self.totalurls = []

    def do_search(self):
        request_url = 'http://www.baidu.com/s' \
                      + '?wd=' + self.word \
                      + '&pn=' + str(self.start) \
                      + '&rn=' + self.number \
                      + '&ie=utf-8'

        response = requests.get(request_url, headers=default_headers, allow_redirects=False)
        status_code = response.status_code
        headers = response.headers
        content = response.content

        self.results = content
        self.totalresults.append(self.results)

    def process(self):
        # comfirm = raw_input('[!] Processing will cost long time, continue? (yes/no): ')
        # if comfirm.lower() != 'yes' and comfirm.lower() != 'y':
        #   sys.exit()

        while (self.start + 100) <= self.limit:
            self.do_search()
            cprint('[-] Searching %s results from "Baidu"' % str(self.start + 100),
                   'green', file=sys.stdout)
            self.start += int(self.number)

    def get_url(self):
        # request_timeout = raw_input('[!] Please input timeout when resolve urls. (1-5): ').strip()
        # if request_timeout not in [str(i) for i in range(1, 6)]:
        #     print '[!] Error input, processing will use default timeout: 2'
        #     request_timeout = 2
        # else:
        #     request_timeout = int(request_timeout)
        # thread_num = raw_input('[!] Please input thread number to start. (1-10): ').strip()
        # if thread_num not in [str(i) for i in range(1, 11)]:
        #     print '[!] Error input, processing will use default thread number: 1'
        #     thread_num = 1
        # else:
        #     thread_num = int(thread_num)

        request_timeout = 2
        thread_num = 10

        urls = []
        if self.totalresults:
            cprint('[!] Parsing links, this will take some times.',
                   'yellow', file=sys.stdout)

            for c in self.totalresults:
                doc = html.document_fromstring(c)
                pre_urls = doc.xpath('//div[@class="result c-container "]/h3/a/@href')

                def resolve(pre_url):
                    """
                    try:
                        url = urllib2.urlopen(pre_url, timeout=request_timeout).url
                    except socket.timeout:
                        return
                    except socket.error:
                        return
                    except urllib2.HTTPError:
                        return
                    except urllib2.URLError:
                        return
                    """

                    try:
                        response = requests.get(pre_url, headers=default_headers, timeout=request_timeout)
                        url = response.url
                    except requests.exceptions.ConnectionError:
                        return
                    except requests.exceptions.TooManyRedirects:
                        return
                    except requests.exceptions.ReadTimeout:
                        return
                    except socket.error:
                        return

                    urls.append(url)

                pool = ThreadPool(thread_num)
                pool.map(resolve, pre_urls)

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
