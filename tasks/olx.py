# -*- coding: utf-8 -*-

import asyncio

from tasks.base import BaseParserTask
from utils.common import Hosts, catch


class OlxParser(BaseParserTask):
    type = Hosts.OLX

    def __init__(self, task, task_data, yield_function):
        super().__init__(task, task_data, yield_function)
        self.seen_urls = self.task_data.get('seen_urls', set())

    def parse_ads_list(self, document):
        ads = document.xpath('//table[@id="offers_table"]//tr[@class="wrap"]')
        urls = set([ad.xpath('.//a[contains(@class, "link")][strong]/@href')[0] for ad in ads])
        new_urls = urls - self.seen_urls
        for url in new_urls:
            asyncio.ensure_future(catch(self.parse_ad(url)))
        self.task_data['seen_urls'] = urls


__author__ = 'manitou'
