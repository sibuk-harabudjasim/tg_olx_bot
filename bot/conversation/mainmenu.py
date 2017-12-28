# -*- coding: utf-8 -*-
from bot.userstor import with_user_data
from bot.conversation.constants import Buttons
from utils.markups import make_keyboard


mainmenu = make_keyboard(2, Buttons.ADD_WATCH, Buttons.MY_WATCHES, Buttons.HOW_IT_WORKS)


@with_user_data
def add_watch(chat, *args, user_data):
    pass


__author__ = 'manitou'
