# -*- coding: utf-8 -*-
import asyncio
from tasks.base import BaseParserTask


class GumtreeTask(BaseParserTask):
    def is_resent_created(self, created_text):
        if ' ' not in created_text:
            return False
        parts = created_text.split(' ')
        if parts[1] != 'min':
            return False
        if int(parts[0]) > self.call_interval / 60:
            return False
        return True

    def parse_ads_list(self, document):
        ads = document.xpath('//div[@class="view"]//li[@class="result pictures"]')
        for ad in ads:
            url = 'http://www.gumtree.pl' + ad.xpath('.//div[@class="title"]/a/@href')[0]
            created = ad.xpath('.//div[@class="creation-date"]/span[last()]/text()')[0].strip()
            if self.is_resent_created(created):
                print('GUMTREE: found new ad - ', url)
                asyncio.ensure_future(self.parse_ad(url))


__author__ = 'manitou'
