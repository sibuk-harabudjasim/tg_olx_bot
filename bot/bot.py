# -*- coding: utf-8 -*-
from aiotg import Bot

from core.config import config
from core.signal import Signal


class ParseBot(object):
    bot = None

    def __init__(self):
        self.receive_data_signal = Signal('data_receive')

    def init(self):
        self.bot = Bot(api_token=config.TELEGRAM_TOKEN)
        from bot.conversation import init_dialogs
        init_dialogs(self.bot)

    def run(self, webhook=config.WEBHOOK_URL):
        if webhook:
            self.bot.run_webhook(webhook)
        else:
            self.bot.run(config.DEBUG)


parsebot = ParseBot()


__author__ = 'manitou'
