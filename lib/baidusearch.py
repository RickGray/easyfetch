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
        comfirm = raw_input('[!] Warning: processing will cost long time, continue? (yes/no): ')
        if comfirm.lower() != 'yes' and comfirm.lower() != 'y':
            sys.exit()

        while self.counter <= self.limit and self.counter <= 1000:
            self.do_search()
            # more = self.check_next()
            time.sleep(1)
            print "[-] Searching " + str(self.counter + 100) + " results..."
            self.counter += 100

        self.get_url()

    def get_url(self):
        urls = []
        if self.totalresults:
            for c in self.totalresults:
                doc = html.document_fromstring(c)
                pre_urls = doc.xpath('//div[@class="result c-container "]/h3/a/@href')

                if pre_urls:
                    for url in pre_urls:
                        try:
                            u = urllib2.urlopen(url, timeout=3).url
                        except socket.timeout:
                            continue
                        except urllib2.HTTPError:
                            continue
                        except urllib2.URLError:
                            continue

                        urls.append(u)

        return urls
