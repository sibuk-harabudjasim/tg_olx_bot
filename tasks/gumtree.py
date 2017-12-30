# -*- coding: utf-8 -*-
import asyncio

import aiohttp
from lxml.html import parse

from core.task import Task


class GumtreeTask(Task):
    async def run(self, url, blacklist, whitelist, last_called_at=None):
        # page = await aiohttp.request('GET', url)
        # html = parse(page)
        # TODO: finish task
        print('>>>>>>>>>> {} >>>>>>>>>>>> task start, {}, {}, {}'.format(self.name, url, blacklist, whitelist))
        await asyncio.sleep(5)
        self.yield_data(111, 'this is advert')
        print('>>>>>>>>>> {} >>>>>>>>>>>> task ended'.format(self.name))


__author__ = 'manitou'
