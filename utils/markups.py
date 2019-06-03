# -*- coding: utf-8 -*-
import json


def make_keyboard(cols, *args, to_json=True):
    res = []
    for i, item in enumerate(args):
        if not i % cols:
            res.append([])
        res[-1].append({'text': item})
    res = {'keyboard': res}
    if to_json:
        res = json.dumps(res)
    return res


def make_inline_keyboard(cols, *args, to_json=True):
    if not all([isinstance(item, (tuple, list)) for item in args]):
        raise Exception('all args must be tuples with (text, callback_data) in')
    res = []
    for i, item in enumerate(args):
        if not i % cols:
            res.append([])
        res[-1].append({'text': item[0], 'callback_data': item[1]})
    res = {'inline_keyboard': res}
    if to_json:
        res = json.dumps(res)
    return res


def parse_list(words):
    res = words.split(',')
    return [w.strip() for w in res]


__author__ = 'manitou'
