#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import html
import socket
import httplib, urllib2
import sys
import re
import time


class search_baidu:
    def __init__(self, word, limit, start):
        self.word = word
        self.results = ""
        self.totalresults = []
        self.server = "www.baidu.com"
        self.hostname = "www.baidu.com"
        self.userAgent = "(Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0)"
        self.quantity = "100"
        self.limit = limit
        self.counter = start

    def do_search(self):
        h = httplib.HTTPS(self.server)
        h.putrequest('GET', "/s?wd=" + self.word + "&pn=" + str(
            self.counter) * 100 + "&oq=" + self.word + "&rn=" + self.quantity + "&ie=utf-8")
        h.putheader('Host', self.hostname)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        returncode, returnmsg, headers = h.getreply()
        self.results = h.getfile().read()
        self.totalresults.append(self.results)

    def process(self):
        while self.counter <= self.limit and self.counter <= 1000:
            self.do_search()
            # more = self.check_next()
            time.sleep(1)
            print "\tSearching " + str(self.counter) + " results..."
            self.counter += 100

        self.get_url()

    def get_url(self):
        urls = []
        if self.totalresults:
            for c in self.totalresults:
                doc = html.document_fromstring(c)
                pre_urls = doc.xpath('//div[@class="result c-container "]/h3/a/@href')

                if pre_urls:
                    urls = []
                    for url in pre_urls:
                        try:
                            u = urllib2.urlopen(url, timeout=5).url
                        except socket.timeout:
                            continue
                        except urllib2.HTTPError:
                            continue

                        urls.append(u)

        return urls
