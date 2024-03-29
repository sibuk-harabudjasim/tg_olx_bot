# -*- coding: utf-8 -*-
from aiotg import Bot
import logging
import traceback

from bot.userstor import with_user_data
from core.config import config
from core.signal import yield_data


log = logging.getLogger()

class ParseBot(object):
    bot = None
    states = None
    oops_handler = None

    def __init__(self):
        self.states = {}

    def init(self):
        self.bot = Bot(api_token=config.TELEGRAM_TOKEN)
        from bot.conversation import init_dialogs
        init_dialogs(self)
        self.bot.default(self.get_default_handler())
        yield_data.add_observer('pbot', self.data_receive_observer)

    async def data_receive_observer(self, tg_id, data):
        log.info(f"DATA RECEIVED: to {tg_id}, data: {data}")
        chat = self.bot.private(tg_id)
        return chat.send_text('Look what I found!\n{}'.format(data))

    def add_state_handler(self, state, hlr):
        self.states[state] = hlr

    def add_default_state_handler(self, hlr):
        self.oops_handler = hlr

    def add_callback(self, regexp, fn):
        return self.bot.add_callback(regexp, fn)

    def add_command(self, regexp, fn):
        return self.bot.add_command(regexp, fn)

    def add_inline(self, regexp, fn):
        return self.bot.add_inline(regexp, fn)

    def get_default_handler(self):
        @with_user_data
        async def def_handler(chat, message, user_data):
            state = user_data.get('state')
            if state:
                handler = self.states.get(state)
                if handler:
                    return await handler(chat, message, user_data)
            if self.oops_handler:
                return await self.oops_handler(chat, message, user_data)
            return await chat.send_text('Oops! Something went wrong, for now we can start again and see how it goes')
        return def_handler

    def run(self, webhook=config.WEBHOOK_URL):
        while True:
            try:
                if webhook:
                    self.bot.run_webhook(webhook)
                else:
                    self.bot.run(config.DEBUG)
            except Exception as e:
                log.error(traceback.format_exc())
                log.info("Restarting bot")
                continue
            else:
                log.info("bot.run() exited, probably keyboard interrupt, exiting")
                return

parsebot = ParseBot()


__author__ = 'manitou'
