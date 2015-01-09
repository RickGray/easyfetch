#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import requests
import time
import lxml

from termcolor import cprint
from lxml import html


# default headers for each request with zoomeye search
default_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'www.zoomeye.org',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:31.0) Gecko/20100101 Firefox/31.0'
}


class SearchZoomEye(object):
    def __init__(self, word, limit, start=1):
        """
        :param word: search keyword
        :param limit: maximum to query
        :param start: results offset, default start 1 (zoomeye.org 1 is the first page)
        :return:
        """
        self.word = word
        self.number = '10'  # zoomeye.org limits the maximum number of results each page
        self.start = start
        self.limit = limit
        self.headers = default_headers

        self.results = ''
        self.totalresults = []

        self.totalurls = []

    def do_search(self):
        request_url = 'http://www.zoomeye.org/search' \
                      + '?t=web' \
                      + '&q=' + self.word \
                      + '&p=' + str(self.start)

        time.sleep(5)
        response = requests.get(request_url, headers=default_headers, allow_redirects=False)
        status_code = response.status_code
        headers = response.headers
        content = response.content

        self.results = content
        self.totalresults.append(self.results)

    def do_search_host(self):
        request_url = 'http://www.zoomeye.org/search' \
                      + '?t=host' \
                      + '&q=' + self.word \
                      + '&p=' + str(self.start)

        time.sleep(5)
        response = requests.get(request_url, headers=default_headers, allow_redirects=False)
        status_code = response.status_code
        headers = response.headers
        content = response.content

        self.results = content
        self.totalresults.append(self.results)

    def process(self):
        while (self.start * int(self.number)) <= self.limit:
            self.do_search()
            cprint('[-] Searching %s results from "ZoomEye"' % str(self.start * int(self.number)),
                   'green', file=sys.stdout)
            self.start += 1

    def get_url(self):
        urls = []
        if self.totalresults:
            for c in self.totalresults:
                try:
                    doc = html.document_fromstring(c)
                except Exception:
                    return
                pre_urls = doc.xpath(
                    '//div[@class="result-list"]/ul[@class="result web"]/li/h3/a/@href')

                if pre_urls:
                    for url in pre_urls:
                        urls.append(url)

        self.totalurls.extend(urls)

        return urls

    def get_ip(self):
        ips = []
        if self.totalresults:
            for c in self.totalresults:
                doc = html.document_fromstring(c)
                pre_ips = doc.xpath(
                    '//div[@class="result-list"]/ul[@class="result web"]/li/article/div[@class="ip"]/a/text()')

                if pre_ips:
                    for ip in pre_ips:
                        ips.append(ip)

        return ips

    def get_ip_host(self):
        ips = []
        if self.totalresults:
            for c in self.totalresults:
                doc = html.document_fromstring(c)
                pre_ips = doc.xpath(
                    '//div[@class="result-list"]/ul[@class="result device"]/li/h3/a[@class="ip"]/@href')

                if pre_ips:
                    for pre_ip in pre_ips:
                        m = re.compile(r'ip:(.*)').findall(pre_ip)
                        if m:
                            ip = m[0]
                        else:
                            continue

                        ips.append(ip)

        return ips

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
