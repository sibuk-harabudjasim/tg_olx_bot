# -*- coding: utf-8 -*-
import asyncio

from core.task import pool as taskpool
from tasks.gumtree import GumtreeParser
from tasks.olx import OlxParser
from tasks.otomoto import OtomotoParser
from tasks.otodom import OtodomParser
from utils import log

if __name__ == '__main__':
    from bot.bot import parsebot as pbot

    log.init()
    pbot.init()
    taskpool.register_task_type(GumtreeParser)
    taskpool.register_task_type(OtomotoParser)
    taskpool.register_task_type(OlxParser)
    taskpool.register_task_type(OtodomParser)
    taskpool.init()
    pbot.run()

__author__ = 'manitou'
