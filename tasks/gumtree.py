# -*- coding: utf-8 -*-
import asyncio
import re

import aiohttp
from lxml import html

from core.task import Task


class GumtreeTask(Task):
    def __init__(self, task, from_user, call_interval):
        super().__init__(task, from_user, call_interval)
        self.blacklist_re = re.compile(r'({})'.format('|'.join(self.task_info.args['blacklist'])))
        self.whitelist_re = re.compile(r'({})'.format('|'.join(self.task_info.args['whitelist'])))

    def is_resent_created(self, created_text):
        if ' ' not in created_text:
            return False
        parts = created_text.split(' ')
        if parts[1] != 'min':
            return False
        if int(parts[0]) > self.call_interval / 60:
            return False
        return True

    async def parse_ad(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as page:
                document = html.fromstring(await page.read())
        title = document.xpath('//h1[@class="item-title"]//text()')
        description = document.xpath('//div[@class="vip-details"]//div[@class="description"]//text()')
        text = ' '.join(title + description).lower()
        if self.blacklist_re.search(text):
            return
        if self.whitelist_re.search(text):
            self.yield_data(self.from_user, url)

    async def run(self, url, blacklist, whitelist, last_called_at=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as page:
                document = html.fromstring(await page.read())
        ads = document.xpath('//div[@class="view"]//li[@class="result pictures"]')
        for ad in ads:
            url = 'http://www.gumtree.pl' + ad.xpath('.//div[@class="title"]/a/@href')[0]
            created = ad.xpath('.//div[@class="creation-date"]/span[last()]/text()')[0].strip()
            if self.is_resent_created(created):
                print('GUMTREE: found new ad - ', url)
                asyncio.ensure_future(self.parse_ad(url))


__author__ = 'manitou'
