# -*- coding: utf-8 -*-

import asyncio

from tasks.base import BaseParserTask
from utils import log
from utils.common import Hosts, catch


class OlxParser(BaseParserTask):
    type = Hosts.OLX

    def __init__(self, task, task_data, yield_function):
        super().__init__(task, task_data, yield_function)
        self.seen_urls = set(self.task_info.args.get('seen_urls', list()))

    def parse_ads_list(self, document):
        ads = document.xpath('//div[contains(@class, "listing-grid-container")]//div[@data-cy="l-card"]')
        urls = set([ad.xpath('.//a/@href')[0] for ad in ads])
        new_urls = urls - self.seen_urls
        if not new_urls:
            log.debug("No new ADs")
            return
        for url in new_urls:
            if not url.startswith("http"):
                url = "https://www.olx.pl" + url
            asyncio.ensure_future(catch(self.parse_ad(url)))
        self.task_info.args['seen_urls'] = urls


__author__ = 'manitou'
