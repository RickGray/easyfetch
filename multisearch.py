#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse


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

    parse = argparse.ArgumentParser()
    parse.add_argument('-b', '--search-engine', type=str,
                       help='Search engine (google,bing,baidu,all)')

    args = parse.parse_args()
