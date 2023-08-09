# -*- coding: utf-8 -*-
import re
from lxml import html
import logging

import aiohttp

from core.task import Task
from core.signal import Signal
from tasks.generic_advert import GenericAdvertParser

from utils.validation import escape_re
from utils.db import active_task_nt

log = logging.getLogger()

class BaseParserTask(Task):
    def __init__(self, db_task: active_task_nt, task_data: dict, yield_function: Signal):
        super().__init__(db_task, task_data, yield_function)
        self.blacklist_re = re.compile(r'({})'.format(escape_re('|'.join(self.db_task.args['blacklist']))), re.I)
        self.whitelist_re = re.compile(r'({})'.format(escape_re('|'.join(self.db_task.args['whitelist']))), re.I)

    @staticmethod
    async def _fetch_text(url: str) -> str:
        log.debug(f"Fetching AD from '{url}'...")
        return await GenericAdvertParser().parse(url)

    def _validate_text(self, text: str, url: str) -> bool:
        if not text:
            log.debug(f"Parser returned no data for url '{url}'")
            return
        if self.blacklist_re.search(text):
            log.debug(f"Blacklist match for ad '{url}': {self.blacklist_re.search(text)}")
            return
        if self.whitelist_re.search(text):
            return True
        log.debug(f"No whitelist match for ad '{url}': {self.db_task.args['whitelist']}")

    async def parse_ad(self, url):
        text = await self._fetch_text(url)
        if self._validate_text(text, url):
            self.yield_data(self.from_user, url)

    def parse_ads_list(self, document):
        '''
        Parses advert list and throws this.parse_ad(url) coroutines into loop
        :param document: lxml.Etree object with parsed page
        :return:
        '''
        raise NotImplementedError

    async def run(self):
        url = self.db_task.args['url']
        log.debug(f"Fetching list from '{url}'...")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as page:
                document = html.fromstring(await page.read())
                return self.parse_ads_list(document)


__author__ = 'manitou'
