# -*- coding: utf-8 -*-
import asyncio

from tasks.base import BaseParserTask
from utils.common import Hosts


class OtomotoParser(BaseParserTask):
    type = Hosts.OTOMOTO

    def parse_ads_list(self, document):
        ads = document.xpath('//article[contains(@class, "offer-item")]')
        for ad in ads:
            url = ad.xpath('.//a[@class="offer-title__link"]/@href')[0]
            asyncio.ensure_future(self.parse_ad(url))


__author__ = 'manitou'
