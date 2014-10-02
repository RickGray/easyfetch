#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
from lib.googlesearch import *
from lib.baidusearch import *

def logo():
    print "\n*********************************************************************"
    print "*                                                                   *"
    print "*    /\  /\         | || |_ \    ___  ___  __ _ _ __  ___ | |__     *"
    print "*   /  \/  \ | | | || || __| |  / __|/ _ \/ _` | '__\/ __\| '_ \    *"
    print "*  / /\  /\ \| |_| || || |_| |  \__ |  __/ ( | | |  |  /__| | | |   *"
    print "* /_/  \/  \_\_____/|_| \__|_|  |___/\___|\__,_|_|   \___/|_| |_|   *"
    print "*                                                                   *"
    print "* MultiSearch Ver. 1.0                                              *"
    print "* Coded by RickGray                                                 *"
    print "* rickchen.vip@gmail.com                                            *"
    print "*********************************************************************\n"


if __name__ == '__main__':
    logo()

    parse = argparse.ArgumentParser(description='Multi Search Parse.')
    parse.add_argument('-b', dest='search_engine', type=str,
                       help='Search engine (google,bing,baidu,all)')

    parse.add_argument('-s', dest='search_string', type=str,
                       help='The keyword searched')

    parse.add_argument('-l', dest='limit_number', type=int, default=0,
                       help='Limit number of the results')

    parse.add_argument('--version', action='version',
                       version='%(prog)s 1.0')

    args = parse.parse_args()

    if args.search_engine not in ('google', 'bing', 'baidu', 'all'):
        print 'Invalid search engine, try with: google, bing, baidu or all'
        sys.exit()
    engine = args.search_engine

    if args.search_string is None:
        print 'Please give a string you wanna search for'
        sys.exit()
    word = args.search_string

    if engine == 'google':
        print '[-] Searching in Google:'
        search = search_google(word, args.limit_number, 0)
        search.process()

    elif engine == 'baidu':
        print '[-] Searching in Baidu:'
        search = search_baidu(word, args.limit_number, 0)
        search.process()
