#!/usr/bin/env python
# coding: utf-8

import re


def url2domain(urls):
    """
    :param urls:
    :return domains:

    将输入urls的域名（ip）提取并返回。
    e.g: http://www.baidu.com/search?asdf  ==> www.baidu.com
         https://base.163.com/home  ==> base.163.com
    """

    domains = []
    for url in urls:
        m = re.compile(r'^http[s]?://([^&/?]*)/??').findall(url)
        if m:
            domain = m[0]
            domains.append(domain)
        else:
            continue

    return domains


def url2base(urls):
    """
    :param urls:
    :return bases:

    将输入urls的基本uri提取并返回。
    e.g: http://www.baidu.com/search?asdf  ==> http://www.baidu.com
         https://base.163.com/home  ==> https://base.163.com
    """
    bases = []
    for url in urls:
        m = re.compile(r'^(http[s]?://[^&/?]*)/??').findall(url)
        if m:
            base = m[0]
            bases.append(base)
        else:
            continue

    return bases

