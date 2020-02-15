# -*- coding: utf-8 -*-
import re
from lxml import html

import aiohttp

from core.task import Task
from tasks.generic_advert import GenericAdvertParser
from utils import log
from utils.validation import escape_re


class BaseParserTask(Task):
    def __init__(self, task, task_data, yield_function):
        super().__init__(task, task_data, yield_function)
        self.blacklist_re = re.compile(r'({})'.format(escape_re('|'.join(self.task_info.args['blacklist']))), re.I)
        self.whitelist_re = re.compile(r'({})'.format(escape_re('|'.join(self.task_info.args['whitelist']))), re.I)

    @staticmethod
    async def _fetch_text(url):
        log.debug("Fetching AD from '{}'...", url)
        return await GenericAdvertParser().parse(url)

    def _validate_text(self, text, url):
        if not text:
            log.debug("Parser returned no data for url '{}'", url)
            return
        if self.blacklist_re.search(text):
            log.debug("Blacklist match for ad '{}': {}", url, self.blacklist_re.search(text))
            return
        if self.whitelist_re.search(text):
            return True
        log.debug("No whitelist match for ad '{}': {}", url, self.task_info.args['whitelist'])

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
        url = self.task_info.args['url']
        log.debug("Fetching list from '{}'...", url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as page:
                document = html.fromstring(await page.read())
                return self.parse_ads_list(document)


__author__ = 'manitou'
