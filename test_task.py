# -*- coding: utf-8 -*-
import asyncio
import importlib
import json
import sys

from core.signal import yield_data
from utils.db import active_task_nt


def print_result(tg_id, text):
    print('\t\t ============ ADVERT ===============\n\t{}'.format(text))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python test_task.py <task class module> <task args (JSON decoded)>")
        exit(-1)
    task_class_path = sys.argv[1]
    args = sys.argv[2]
    try:
        path, cls = task_class_path.rsplit('.', maxsplit=1)
        module = importlib.import_module(path)
        Task = getattr(module, cls)
        args = json.loads(args)
    except Exception as e:
        print('Error: {}'.format(str(e)))
        exit(-1)
    task_info = active_task_nt(1, 'testtask', 1, args)
    task = Task(task_info, None, None)
    task.yield_func = yield_data
    yield_data.add_observer('print', print_result)

    async def run_task():
        print('>>>>>>>>>>>> TASK START >>>>>>>>>>>>>>>>>>>')
        await task.run(**task.task_info.args)
        print('>>>>>>>>>>>> TASK END >>>>>>>>>>>>>>>>>>>>>')
        await asyncio.sleep(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_task())


__author__ = 'manitou'
