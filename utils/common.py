# -*- coding: utf-8 -*-
import re


def detect_host(url):
    host_re = re.compile(r'^.+?//(www.)?(.+?)\.\w{2,}/')
    result = host_re.search(url)
    return result.group(2)


__author__ = 'manitou'
