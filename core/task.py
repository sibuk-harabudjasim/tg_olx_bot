# -*- coding: utf-8 -*-
import asyncio

from datetime import datetime, timedelta

from collections import defaultdict

from core.config import config
from core.signal import yield_data, start_task, stop_task
from utils.db import Tasks

loop = asyncio.get_event_loop()


class Task(object):
    name = None
    type = None
    handle = None
    yield_func = None

    def __init__(self, task, task_data, yield_function):
        self.task_info = task
        self.task_data = task_data
        self.name = task.name
        self.from_user = task.tg_id
        self.yield_func = yield_function

    def yield_data(self, *args, **kwargs):
        if self.yield_func:
            self.yield_func.emit(*args, **kwargs)
        else:
            raise Exception('No yield function in task {}'.format(self))

    async def run(self, **kwargs):
        raise NotImplementedError


class TaskPool(object):
    signal = None
    default_interval = config.DEFAULT_TASK_INTERVAL * 60
    pool_interval = 60

    def __init__(self):
        self.types = {}
        self.storage = defaultdict(dict)
        self.signal = yield_data

    def init(self):
        asyncio.ensure_future(self._tasks_execution())

    def register_task_type(self, cls):
        self.types[cls.type] = cls

    async def _tasks_execution(self):
        while True:
            print('Task pool: executing tasks...')
            tasks = await self._get_pending_tasks()
            for task in tasks:
                try:
                    await task.run()
                    await self._update_task_start_time(task)
                except Exception as e:
                    print("Exception running task {}: {}".format(task.__class__.__name__, str(e)))
            await asyncio.sleep(self.pool_interval)

    async def _get_pending_tasks(self):
        tasks_info = await Tasks.get_pending_tasks()
        return filter(None, [self._make_task(task_info) for task_info in tasks_info])

    def _get_task_data(self, task):
        return self.storage[task.task_info.id]

    def _make_task(self, task_info):
        if task_info.type in self.types:
            task_class = self.types[task_info.type]
            task_data = self.storage[task_info.id]
            return task_class(task_info, task_data, self.signal)
        else:
            print('ERROR: cannot handle task type "{}"'.format(task_info.type))

    def _update_task_start_time(self, task):
        return Tasks.update_task(task.task_info.id, start_time=(datetime.now() + timedelta(seconds=self.default_interval)))


pool = TaskPool()

__author__ = 'manitou'
