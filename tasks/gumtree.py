# -*- coding: utf-8 -*-
import aiohttp
from lxml.html import parse

from core.task import Task


class GumtreeTask(Task):
    async def run(self, url, blacklist, whitelist, last_called_at=None):
        page = await aiohttp.request('GET', url)
        html = parse(page)
        # TODO: finish task
        print('me is task')


__author__ = 'manitou'
