# -*- coding: utf-8 -*-
from aiotg import Bot

from bot.userstor import with_user_data
from core.config import config


class ParseBot(object):
    bot = None
    states = None

    def __init__(self):
        self.states = {}

    def init(self):
        self.bot = Bot(api_token=config.TELEGRAM_TOKEN)
        from bot.conversation import init_dialogs
        init_dialogs(self)
        self.bot.default(self.get_default_handler())
        # subscribe to signals

    def add_state_handler(self, state, hlr):
        self.states[state] = hlr

    def add_callback(self, regexp, fn):
        return self.bot.add_callback(regexp, fn)

    def add_command(self, regexp, fn):
        return self.bot.add_command(regexp, fn)

    def add_inline(self, regexp, fn):
        return self.bot.add_inline(regexp, fn)

    def get_default_handler(self):
        @with_user_data
        async def def_handler(chat, message, user_data):
            print('DEF HANDLER')
            print(chat, message, user_data, self.states)
            state = user_data.get('state')
            print('STATE:', state)
            if state:
                handler = self.states.get(state)
                if handler:
                    return await handler(chat, message, user_data)
            return await chat.send_text('Oops! Something went wrong, for now we can start again and see how it goes')
        return def_handler

    def run(self, webhook=config.WEBHOOK_URL):
        if webhook:
            self.bot.run_webhook(webhook)
        else:
            self.bot.run(config.DEBUG)


parsebot = ParseBot()


__author__ = 'manitou'
