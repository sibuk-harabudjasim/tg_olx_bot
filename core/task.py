# -*- coding: utf-8 -*-
import asyncio
import logging
import traceback

from datetime import datetime, timedelta

from collections import defaultdict

from core.config import config
from core.signal import Signal, yield_data, start_task, stop_task
from typing import Iterable
from utils.db import Tasks, active_task_nt


loop = asyncio.get_event_loop()
log = logging.getLogger()


class Task(object):
    db_task: active_task_nt = None
    name: str = None
    type: str = None
    yield_signal: Signal = None

    def __init__(self, db_task: active_task_nt, yield_signal: Signal):
        self.db_task = db_task
        self.task_data = db_task.args
        self.name = db_task.name
        self.from_user = db_task.tg_id
        self.yield_signal = yield_signal

    def yield_data(self, *args, **kwargs):
        if self.yield_signal:
            self.yield_signal.emit(*args, **kwargs)
        else:
            raise Exception('No yield function in task {}'.format(self))

    async def run(self, **kwargs) -> dict:
        raise NotImplementedError


class TaskPool(object):
    types: dict[str, Task] = None
    signal: Signal = None
    default_interval: int = config.DEFAULT_TASK_INTERVAL * 60
    pool_run_interval: int = 60

    def __init__(self):
        self.types = {}
        self.signal = yield_data

    def init(self):
        asyncio.ensure_future(self._tasks_execution())

    def register_task_type(self, task_class: Task):
        self.types[task_class.type] = task_class

    async def _tasks_execution(self):
        while True:
            log.info("Task pool: executing tasks...")
            tasks = await self._get_pending_tasks()
            for task in tasks:
                try:
                    new_task_data = await task.run()
                    await self._update_task(task, new_task_data)
                except Exception as e:
                    log.error(f"Exception running task {task.__class__.__name__}: {str(e)}")
                    log.error(traceback.format_exc())
            await asyncio.sleep(self.pool_run_interval)

    async def _get_pending_tasks(self) -> Iterable[Task]:
        tasks_info = await Tasks.get_pending_tasks()
        return filter(None, [self._make_task(task_info) for task_info in tasks_info])

    def _make_task(self, db_task: active_task_nt) -> Task | None:
        if db_task.type in self.types:
            task_class = self.types[db_task.type]
            return task_class(db_task, self.signal)
        else:
            log.warning(f"Cannot handle task type '{db_task.type}'")

    async def _update_task(self, task: Task, new_task_data: dict):
        await Tasks.update_task(task.db_task.id, args=new_task_data, start_time=(datetime.now() + timedelta(seconds=self.default_interval)))
        log.info(f"Task '{task.name}' next run at: {datetime.now() + timedelta(seconds=self.default_interval)}")


pool = TaskPool()

__author__ = 'manitou'
