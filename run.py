# -*- coding: utf-8 -*-
from core.task import pool as taskpool
from tasks.gumtree import GumtreeTask

if __name__ == '__main__':
    from utils.db import db
    from bot.bot import parsebot as pbot

    db.init()
    pbot.init()
    taskpool.init(pbot.receive_data_signal)
    taskpool.register_default_task(GumtreeTask)
    pbot.run()

__author__ = 'manitou'
