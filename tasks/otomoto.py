# -*- coding: utf-8 -*-
import asyncio

from tasks.base import BaseParserTask
from utils.common import Hosts


class OtomotoParser(BaseParserTask):
    type = Hosts.OTOMOTO

    def __init__(self, task, from_user, call_interval):
        super().__init__(task, from_user, call_interval)
        self.seen_urls = set()

    def parse_ads_list(self, document):
        ads = document.xpath('//article[contains(@class, "offer-item")]')
        urls = set([ad.xpath('.//a[@class="offer-title__link"]/@href')[0] for ad in ads])
        new_urls = urls - self.seen_urls
        for url in new_urls:
            asyncio.ensure_future(self.parse_ad(url))
        self.seen_urls = urls


__author__ = 'manitou'
