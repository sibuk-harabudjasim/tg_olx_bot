# -*- coding: utf-8 -*-
import asyncio

from tasks.base import BaseParserTask
from utils.common import Hosts, catch


class OtodomParser(BaseParserTask):
    type = Hosts.OTODOM

    def __init__(self, task, yield_function):
        super().__init__(task, yield_function)
        self.seen_urls = set(self.task_data.get('seen_urls', list()))

    def parse_ads_list(self, document):
        ads = document.xpath('//li[@data-cy="listing-item"]')
        urls = set([ad.xpath('./a/@href')[0] for ad in ads])
        new_urls = urls - self.seen_urls
        for url in new_urls:
            if not url.startswith("http"):
                url = "https://www.otodom.pl" + url
            asyncio.ensure_future(catch(self.parse_ad(url)))
        self.task_data['seen_urls'] = urls
        return self.task_data
