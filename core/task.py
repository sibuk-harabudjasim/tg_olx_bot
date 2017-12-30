# -*- coding: utf-8 -*-
import asyncio

from core.signal import yield_data, start_task, stop_task
from utils.db import Tasks

loop = asyncio.get_event_loop()


class Task(object):
    name = None
    handle = None
    yield_func = None

    def __init__(self, task, from_user, call_interval):
        self.task_info = task
        self.name = task.name
        self.from_user = from_user
        self.call_interval = call_interval
        self.running = False

    def yield_data(self, *args, **kwargs):
        if self.yield_func:
            self.yield_func(*args, **kwargs)
        else:
            raise Exception('No yield function in task {}'.format(self))

    async def run(self, **kwargs):
        raise NotImplementedError

    async def _run(self, kwargs):
        self.handle = None
        await self.run(**kwargs)
        if self.running:
            self.handle = loop.call_later(self.call_interval, self._rerun, kwargs)

    def _rerun(self, kwargs):
        asyncio.ensure_future(self._run(kwargs))

    def start(self, immediate=False):
        if self.running:
            return
        if immediate:
            asyncio.ensure_future(self._run(self.task_info.args))
        else:
            self.handle = loop.call_later(self.call_interval, self._rerun, self.task_info.args)
        self.running = True

    def cancel(self):
        if not self.running:
            return
        if self.handle:
            handle, self.handle = self.handle, None
            handle.cancel()


class TaskPool(object):
    tasks = None
    signal = None
    default_task = None

    def __init__(self):
        self.tasks = {}
        self.signal = yield_data

    def init(self):
        start_task.add_observer('task_pool', self.add_task_observer)
        stop_task.add_observer('task_pool', self.delete_task_observer)

    async def load_tasks(self):
        print('LOADING TASKS')
        tasks_info = await Tasks.get_active_tasks()
        # TODO: load tasks from DB
        for task in tasks_info:
            self.add_task(task, from_user=task.tg_id, interval=30, immediate=True)

    def register_default_task(self, cls):
        self.default_task = cls

    def add_task(self, task, from_user=None, interval=None, immediate=False):
        self.add_default_task(task, from_user=from_user, interval=interval, immediate=immediate)

    def add_default_task(self, task, from_user, interval, immediate=False):
        task = self.default_task(task, from_user, interval)
        return self.add_task_by_instance(task, immediate)

    def add_task_by_instance(self, task, immediate=False):
        task.yield_func = self.signal
        self.tasks[task.task_info.id] = task
        task.start(immediate)

    def delete_task(self, task_id):
        if task_id not in self.tasks:
            raise Exception('no such task')
        task = self.tasks[task_id]
        del self.tasks[task_id]
        task.cancel()

    def delete_task_observer(self, task_id):
        print("DELETING TASK")
        # TODO: remove task from schedule
        self.delete_task(task_id)

    def add_task_observer(self, tg_id, task):
        print('ADDING TASK')
        # TODO: add task
        self.add_task(task, from_user=tg_id, interval=30, immediate=True)


pool = TaskPool()

__author__ = 'manitou'
