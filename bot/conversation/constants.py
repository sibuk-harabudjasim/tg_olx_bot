# -*- coding: utf-8 -*-
from utils.markups import make_keyboard, make_inline_keyboard


class Constants(object):
    FALLBACK = 'fallback'
    TASK_INFO_TMPL = 'task_info_{}'
    TASK_INFO_REGEX = r'task_info_(.+)'
    TASK_DELETE_TMPL = 'task_delete_{}'
    TASK_DELETE_REGEX = r'task_delete_(.+)'
    TASK_RESTORE_TMPL = 'task_restore_{}'
    TASK_RESTORE_REGEX = r'task_restore_(.+)'
    ALLOWED_SITES = ['gumtree.pl', 'otomoto.pl', 'olx.pl']

    @classmethod
    def get_allowed_sites(cls):
        if len(cls.ALLOWED_SITES) == 1:
            return cls.ALLOWED_SITES[0]
        return ' and '.join([', '.join(cls.ALLOWED_SITES[:-1]), cls.ALLOWED_SITES[-1]])


class Buttons(object):
    ADD_WATCH = 'Add watch'
    MY_WATCHES = 'My watches'
    HOW_IT_WORKS = 'How it works'
    FALLBACK = 'Start again'
    TASK_DELETE = 'Delete task'
    TASK_RESTORE = 'Restore task'


class States(object):
    ADD_TASK_URL = 'url_add'
    ADD_TASK_BLACKLIST = 'blacklist_add'
    ADD_TASK_WHITELIST = 'whitelist_add'
    ADD_TASK_NAME = 'name_add'


mainmenu = make_keyboard(2, Buttons.ADD_WATCH, Buttons.MY_WATCHES, Buttons.HOW_IT_WORKS)
inline_fallback = make_inline_keyboard(1, (Buttons.FALLBACK, Constants.FALLBACK))


__author__ = 'manitou'
