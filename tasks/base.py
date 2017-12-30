# -*- coding: utf-8 -*-
import re
from lxml import html

import aiohttp

from core.task import Task
from tasks.generic_advert import GenericAdvertParser


class BaseParserTask(Task):
    def __init__(self, task, from_user, call_interval):
        super().__init__(task, from_user, call_interval)
        self.blacklist_re = re.compile(r'({})'.format('|'.join(self.task_info.args['blacklist'])))
        self.whitelist_re = re.compile(r'({})'.format('|'.join(self.task_info.args['whitelist'])))

    async def parse_ad(self, url):
        text = await GenericAdvertParser().parse(url)
        if not text:
            return
        if self.blacklist_re.search(text):
            return
        if self.whitelist_re.search(text):
            self.yield_data(self.from_user, url)

    def parse_ads_list(self, document):
        '''
        Parses advert list and throws this.parse_ad(url) coroutines into loop
        :param document: lxml.Etree object with parsed page
        :return:
        '''
        raise NotImplementedError

    async def run(self, url, blacklist, whitelist, last_called_at=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as page:
                document = html.fromstring(await page.read())
                return self.parse_ads_list(document)


__author__ = 'manitou'
