# -*- coding: utf-8 -*-
import asyncio

from core.task import pool as taskpool
from tasks.gumtree import GumtreeParser
from tasks.olx import OlxParser
from tasks.otomoto import OtomotoParser

if __name__ == '__main__':
    from bot.bot import parsebot as pbot

    pbot.init()
    taskpool.init()
    taskpool.register_task_type(GumtreeParser)
    taskpool.register_task_type(OtomotoParser)
    taskpool.register_task_type(OlxParser)
    asyncio.ensure_future(taskpool.load_tasks())
    pbot.run()

__author__ = 'manitou'
