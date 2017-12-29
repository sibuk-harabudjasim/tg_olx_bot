# -*- coding: utf-8 -*-


def validate_blacklist(words):
    res = []
    if len(words) > 10:
        res.append('Don`t write too much words, you can miss to many adverts, usually, 5 is enough.')
    if [w for w in words if len(w) > 10]:
        res.append('Aren`t your words too complicated? Maybe you`d better stick to simpler criterias?')
    return res


def validate_whitelist(words):
    res = []
    if [w for w in words if len(w) > 10]:
        res.append('Aren`t your words too complicated? Maybe you`d better stick to simpler criterias?')
    return res


def validate_url(url):
    # TODO: add validation
    return url


def validate_name(name):
    # TODO: check if already exist, regex cut
    return name

__author__ = 'manitou'
