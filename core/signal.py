# -*- coding: utf-8 -*-
from collections import OrderedDict


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

    async def emit(self, *args, **kwargs):
        for callable, raise_exc in self.observers.values():
            try:
                await callable(*args, **kwargs)
            except:
                if raise_exc:
                    raise


__author__ = 'manitou'
