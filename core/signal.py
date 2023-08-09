# -*- coding: utf-8 -*-
import asyncio
import logging
from collections import OrderedDict


log = logging.getLogger()


class Signal(object):
    name = None
    observers = None

    def __init__(self, name):
        self.name = name
        self.observers = OrderedDict()

    def add_observer(self, name, callable, raise_exc=False):
        self.observers[name] = (callable, raise_exc)

    def remove_observer(self, name):
        self.observers.pop(name, None)

    def emit(self, *args, **kwargs):
        asyncio.ensure_future(self._emit(*args, **kwargs))

    async def _emit(self, *args, **kwargs):
        for callable, raise_exc in self.observers.values():
            try:
                if asyncio.iscoroutinefunction(callable):
                    await callable(*args, **kwargs)
                else:
                    callable(*args, **kwargs)
            except Exception as e:
                log.error(f"{self} exception: {str(e)}")
                if raise_exc:
                    raise

    def __repr__(self):
        return f"<Signal {self.name}>"


yield_data = Signal('yield_data')  # tg_id, text
start_task = Signal('start_task')  # tg_id, user_task_nt
stop_task = Signal('stop_task')  # task_id


__author__ = 'manitou'
