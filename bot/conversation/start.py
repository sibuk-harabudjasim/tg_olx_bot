# -*- coding: utf-8 -*-
from bot.userstor import with_user_data
from bot.conversation.constants import mainmenu


@with_user_data
def start(chat, match, user_data):
    name = user_data['name']
    return chat.send_text('Greetings {}! Press any of my shiny buttons!'.format(name), reply_markup=mainmenu)


__author__ = 'manitou'
