#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import html
from multiprocessing.dummy import Pool as ThreadPool
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
        comfirm = raw_input('[!] Processing will cost long time, continue? (yes/no): ')
        if comfirm.lower() != 'yes' and comfirm.lower() != 'y':
            sys.exit()

        while (self.counter + 100) <= self.limit and self.counter <= 1000:
            self.do_search()
            # more = self.check_next()
            time.sleep(1)
            print "[-] Searching " + str(self.counter + 100) + " results from \"Baidu\"..."
            self.counter += 100

    def get_url(self):
        request_timeout = raw_input('[!] Please input timeout when resolve urls. (1-5): ').strip()
        if request_timeout not in ('1', '2', '3', '4', '5'):
            print '[!] Error input, processing will use default timeout: 2'
            request_timeout = 2
        else:
            request_timeout = int(request_timeout)
        thread_num = raw_input('[!] Please input thread number to start. (1-10): ').strip()
        if thread_num not in ('1','2','3','4','5','6','7','8','9','10'):
            print '[!] Error input, processing will use default thread number: 1'
            thread_num = 1
        else:
            thread_num = int(thread_num)

        urls = []
        if self.totalresults:
            for c in self.totalresults:
                doc = html.document_fromstring(c)
                pre_urls = doc.xpath('//div[@class="result c-container "]/h3/a/@href')

                def resolve(pre_url):
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
                    except httplib.BadStatusLine:
                        return

                    urls.append(url)

                pool = ThreadPool(thread_num)
                pool.map(resolve, pre_urls)

        return urls
