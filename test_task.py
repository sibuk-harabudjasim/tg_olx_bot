# -*- coding: utf-8 -*-
import asyncio
import importlib
import json
import sys

from core.signal import yield_data
from utils import log
from utils.db import active_task_nt

"""
Test file for checking tasks working.
Mainly used for local check of existing tasks (taken from DB).
Example usage:
$ python test_task.py tasks.olx.OlxParser '{"url": "https://www.olx.pl/motoryzacja/samochody/q-civic/?search%5Bfilter_float_price%3Ato%5D=17000&search%5Bfilter_float_price%3Afrom%5D=8000&search%5Bfilter_float_year%3Afrom%5D=2006&search%5Bfilter_float_year%3Ato%5D=2011&search%5Bfilter_enum_petrol%5D%5B0%5D=petrol", "blacklist": ["1.4", "1400", "83km", "sedan", "coupe", "90km", "anglik", "2.2", "cdti", "diesel"], "whitelist": []}'
"""


def print_result(tg_id, text):
    print('\t\t ============ ADVERT ===============\n\t{}'.format(text))


if __name__ == '__main__':
    log.init()
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
    task_info = active_task_nt(1, 'testtask', Task.type, 1, args)
    task = Task(task_info, {}, yield_data)
    yield_data.add_observer('print', print_result)

    async def run_task():
        print('>>>>>>>>>>>> TASK START >>>>>>>>>>>>>>>>>>>')
        await task.run()
        print('>>>>>>>>>>>> TASK END >>>>>>>>>>>>>>>>>>>>>')
        await asyncio.sleep(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_task())


__author__ = 'manitou'
