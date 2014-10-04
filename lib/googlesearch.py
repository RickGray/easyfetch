#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import html
import httplib
import sys
import re
import time


class search_google:
    def __init__(self, word, limit, start):
        self.word = word
        self.results = ""
        self.totalresults = []
        self.server = "www.google.com"
        self.hostname = "www.google.com"
        self.userAgent = "(Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0)"
        self.quantity = "100"
        self.limit = limit
        self.counter = start

    def do_search(self):
        h = httplib.HTTPS(self.server)
        h.putrequest('GET', "/search?num=" + self.quantity + "&start=" + str(
            self.counter) + "&hl=en&meta=&q=" + self.word + "&gws_rd=ssl")
        h.putheader('Host', self.hostname)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        returncode, returnmsg, headers = h.getreply()
        self.results = h.getfile().read()
        self.totalresults.append(self.results)

    def process(self):
        while (self.counter + 100) <= self.limit and self.counter <= 1000:
            self.do_search()
            # more = self.check_next()
            time.sleep(1)
            print "[-] Searching " + str(self.counter + 100) + " results from \"Google\"..."
            self.counter += 100

    def get_url(self):
        urls = []
        if self.totalresults:
            for c in self.totalresults:
                doc = html.document_fromstring(c)
                pre_urls = doc.xpath('//div[@id="ires"]/ol/div[@class="srg"]/li[@class="g"]/div[@class="rc"]/h3/a/@href')

                if pre_urls:
                    for url in pre_urls:
                        urls.append(url)

        return urls
