# -*- coding: utf-8 -*-


def make_keyboard(cols, *args):
    res = []
    for i, item in enumerate(args):
        if not i % cols:
            res.append([])
        res[-1].append({'text': item})
    return {'keyboard': res}


def parse_list(words):
    res = words.split(',')
    return [w.strip() for w in res]


__author__ = 'manitou'
