#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib
import sys
import re
import time


class search_google:
    def __init__(self, word, limit, start):
        self.word = word
        self.results = ""
        self.totalresults = ""
        self.server = "www.google.com"
        self.hostname = "www.google.com"
        self.userAgent = "(Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0)"
        self.quantity = "100"
        self.limit = limit
        self.counter = start

    def do_search(self):
        h = httplib.HTTP(self.server)
        h.putrequest('GET', "/search?num=" + self.quantity + "&start=" + str(
            self.counter) + "&hl=en&meta=&q=%40\"" + self.word + "\"")
        h.putheader('Host', self.hostname)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        returncode, returnmsg, headers = h.getreply()
        self.results = h.getfile().read()
        self.totalresults += self.results

    def process(self):
        while self.counter <= self.limit and self.counter <= 1000:
            self.do_search()
            # more = self.check_next()
            time.sleep(1)
            print "\tSearching " + str(self.counter) + " results..."
            self.counter += 100
