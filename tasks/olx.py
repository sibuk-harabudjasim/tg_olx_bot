# -*- coding: utf-8 -*-

import asyncio
import logging


from core.signal import Signal
from tasks.base import BaseParserTask
from utils.common import Hosts, catch
from utils.db import active_task_nt


log = logging.getLogger()


class OlxParser(BaseParserTask):
    type = Hosts.OLX

    def __init__(self, db_task: active_task_nt, task_data: dict, yield_function: Signal):
        super().__init__(db_task, task_data, yield_function)
        self.seen_urls = set(self.task_data.get('seen_urls', list()))

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
        self.task_data['seen_urls'] = urls
        return self.task_data



__author__ = 'manitou'
