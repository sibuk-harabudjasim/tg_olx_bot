# -*- coding: utf-8 -*-


def make_keyboard(cols, *args):
    res = []
    for i, item in enumerate(args):
        if not i % cols:
            res.append([])
        res[-1].append({'text': item})
    return {'keyboard': res}


__author__ = 'manitou'
