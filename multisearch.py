#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from lib.core.googlesearch import *
from lib.core.baidusearch import *
from lib.core.zoomeyesearch import *
from lib.core.sogousearch import *

#from lib.plugin.utils import url2base, url2domain


def logo():
    print "__________________________________________________________________"
    print "                                                                  "
    print "    /\  /\         | || |_ \    ___  ___  __ _ _ __  ___ | |__    "
    print "   /  \/  \ | | | || || __| |  / __|/ _ \/ _` | '__\/ __\| '_ \   "
    print "  / /\  /\ \| |_| || || |_| |  \__ |  __/ ( | | |  |  /__| | | |  "
    print " /_/  \/  \_\_____/|_| \__|_|  |___/\___|\__,_|_|   \___/|_| |_|  "
    print "                                                                  "
    print "                     MultiSearch Ver. 1.2                         "
    print "                         2014-12-05                               "
    print "                  rickchen.vip(at)gmail.com                       "
    print "------------------------------------------------------------------"


def parse_argv():
    parse = argparse.ArgumentParser(description='Mixed search to extract url,host,ip...')

    parse.add_argument('-v', '--verbose',
                       dest='verbose', action='store_true',
                       help='show more information or not')
    parse.add_argument('--version', action='version',
                       version='%(prog)s 1.2')

    group = parse.add_argument_group('necessary arguments')
    group.add_argument('-b',
                       dest='engine', type=str,
                       help='search engine (google, googlecse, baidu, zoomeye, sogou, all)')
    group.add_argument('-s',
                       dest='string', type=str,
                       help='search keyword')
    group.add_argument('-t',
                       dest='start', type=int, default=0,
                       help='start page to extract')
    group.add_argument('-l',
                       dest='limit', type=int, default=100,
                       help='limit the maximum number of search results')
    group.add_argument('-o',
                       dest='outfile', type=str,
                       help='put the search results output to file')

    return parse.parse_args()


def main():
    args = parse_argv()

    # verify the search engine provided
    engine_list = ['google', 'googlecse', 'baidu', 'zoomeye', 'sogou', 'all']
    if not args.engine or args.engine not in engine_list:
        cprint('Invalid engine, please specify a search engine.', 'red')
        sys.exit()
    engine = args.engine

    # verify the keyword is given or not
    if not args.string:
        cprint('None string found, please provide something to search.', 'red')
        sys.exit()
    word = args.string

    if engine == 'google':
        cprint('[-] Searching "%s" in Google:' % word, 'green')
        search = SearchGoogle(word, args.limit, args.start)
        search.process()
        urls = search.get_url()
        hosts = search.get_host()

    elif engine == 'googlecse':
        cprint('[-] Searching "%s" in Google CSE:' % word, 'green')
        search = SearchGoogle(word, args.limit, args.start)
        search.process_cse()
        urls = search.get_url_cse()
        hosts = search.get_host_cse()

    elif engine == 'baidu':
        cprint('[-] Searching "%s" in Baidu:' % word, 'green')
        search = SearchBaidu(word, args.limit, args.start)
        search.process()
        urls = search.get_url()
        hosts = search.get_host()

    elif engine == 'zoomeye':
        cprint('[-] Searching "%s" in ZoomEye:' % word, 'green')
        search = SearchZoomEye(word, args.limit, args.start)
        search.process()
        urls = search.get_url()
        hosts = search.get_host()

    elif engine == 'sogou':
        cprint('[-] Searching "%s" in Sogou:' % word, 'green')
        search = SearchSogou(word, args.limit, args.start)
        search.process()
        urls = search.get_url()
        hosts = search.get_host()

    elif engine == 'all':
        cprint('[-] Searching "%s" in All (except Baidu):' % word, 'green')
        search = SearchGoogle(word, args.limit, args.start)
        search.process()
        urls = search.get_url()
        hosts = search.get_host()

        search = SearchGoogle(word, args.limit, args.start)
        search.process_cse()
        urls.extend(search.get_url_cse())
        hosts.extend(search.get_host_cse())

        search = SearchZoomEye(word, args.limit, args.start)
        search.process()
        urls.extend(search.get_url())
        hosts.extend(search.get_host())

        search = SearchSogou(word, args.limit, args.start)
        search.process()
        urls.extend(search.get_url())
        hosts.extend(search.get_host())

    # duplicate handle
    urls = {}.fromkeys(urls).keys()
    hosts = {}.fromkeys(hosts).keys()

    # put the search results output to file

    if args.outfile:
        outfile = open(args.outfile, 'w')

        outfile.write('[+] Urls found:\n-----------------\n')
        for item in urls:
            outfile.write(item + '\n')
        outfile.write('\n[+] Total hosts:\n-----------------\n')
        for item in hosts:
            outfile.write(item + '\n')

        outfile.close()

    print '\n[+] Urls found:'
    print '-----------------'
    if urls:
        for url in urls:
            print url

    print '\n[+] Total hosts:'
    print '-----------------'
    if hosts:
        for host in hosts:
            print host

    cprint('\nTotal %d Urls, %d Hosts' % (urls.__len__(), hosts.__len__()), 'green')


if __name__ == '__main__':
    #logo()
    main()
