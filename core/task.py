# -*- coding: utf-8 -*-
import asyncio

loop = asyncio.get_event_loop()


class Task(object):
    name = None
    handle = None
    yield_func = None

    def __init__(self, name, from_user, call_interval, *args):
        self.name = name
        self.from_user = from_user
        self.call_interval = call_interval
        self.args = args

    def yield_data(self, *args, **kwargs):
        if self.yield_func:
            self.yield_func(*args, **kwargs)
        else:
            raise Exception('No yield function in task {}'.format(self))

    async def run(self, *args):
        raise NotImplementedError

    async def _run(self, *args):
        await self.run(*args)
        self.handle = loop.call_later(self.call_interval, self._run, *args)

    async def start(self, immediate=False):
        if self.handle:
            return
        if immediate:
            await self._run(*self.args)
        else:
            self.handle = loop.call_later(self.call_interval, self._run, *self.args)

    def cancel(self):
        if self.handle:
            handle, self.handle = self.handle, None
            handle.cancel()


class TaskPool(object):
    tasks = None
    signal = None
    default_task = None

    def __init__(self):
        self.tasks = []

    def init(self, yield_signal):
        self.signal = yield_signal

    def load_tasks(self, tasks_info):
        pass

    def register_default_task(self, cls):
        self.default_task = cls

    def add_task(self, *args, name=None, from_user=None, interval=None, immediate=False):
        if isinstance(args[0], Task):
            self.add_task_by_instance(args[0], immediate)
        else:
            self.add_default_task(*args, name=name, from_user=from_user, interval=interval, immediate=immediate)

    def add_default_task(self, *args, name, from_user, interval, immediate=False):
        task = self.default_task(name, from_user, interval, *args)
        return self.add_task_by_instance(task, immediate)

    def add_task_by_instance(self, task, immediate=False):
        task.yield_func = self.signal
        self.tasks.append(task)
        task.start(immediate)


pool = TaskPool()

__author__ = 'manitou'
