# -*- coding: utf-8 -*-
from bot.conversation.constants import Buttons, States
from bot.userstor import with_user_data
from .start import start
from .add_watch import add_watch, process_url, process_blacklist, process_whitelist, process_name


@with_user_data
def fallback(chat, match, user_data):
    user_data.pop('state', None)
    # TODO: add fallback inline button
    return chat.send_text('Sorry for that. So, what do you want to do now?')


def init_dialogs(bot):
    # START
    bot.add_command('/start', start)

    # ADD WATCH SEQ
    bot.add_command(Buttons.ADD_WATCH, add_watch)
    bot.add_state_handler(States.ADD_WATCH_URL, process_url)
    bot.add_state_handler(States.ADD_WATCH_BLACKLIST, process_blacklist)
    bot.add_state_handler(States.ADD_WATCH_WHITELIST, process_whitelist)
    bot.add_state_handler(States.ADD_WATCH_NAME, process_name)

    # FALLBACK
    bot.add_inline(Buttons.FALLBACK, fallback)


__author__ = 'manitou'
