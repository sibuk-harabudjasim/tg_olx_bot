# -*- coding: utf-8 -*-
import asyncio

from core.task import pool as taskpool
from tasks.gumtree import GumtreeParser
from tasks.otomoto import OtomotoParser

if __name__ == '__main__':
    from utils.db import db
    from bot.bot import parsebot as pbot

    db.init()
    pbot.init()
    taskpool.init()
    taskpool.register_task_type(GumtreeParser)
    taskpool.register_task_type(OtomotoParser)
    asyncio.ensure_future(taskpool.load_tasks())
    pbot.run()

__author__ = 'manitou'
