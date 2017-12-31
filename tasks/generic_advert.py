# -*- coding: utf-8 -*-
import aiohttp
from datetime import datetime
from lxml import html

from core.config import config
from utils.common import detect_host


class GenericAdvertParser(object):
    async def parse(self, url):
        host = detect_host(url)
        handler = getattr(self, 'parse_' + host, None)
        if not handler:
            raise Exception('unsupported URL ({}): {}'.format(host, url))
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as page:
                document = html.fromstring(await page.read())
        return handler(document)

    @staticmethod
    def parse_gumtree(document):
        title = document.xpath('//h1[@class="item-title"]//text()')
        description = document.xpath('//div[@class="vip-details"]//div[@class="description"]//text()')
        return ' '.join(title + description).lower()

    @staticmethod
    def parse_otomoto(document):
        date_updated_text = document.xpath('//meta[@property="og:updated_time"]/@content')[0]
        date_updated = datetime.strptime(date_updated_text, "%Y-%m-%dT%H:%M:%S")
        if date_updated > datetime.now() or (datetime.now() - date_updated).total_seconds() > config.DEFAULT_TASK_INTERVAL * 10:
            return
        params = filter(None, document.xpath('//div[@id="parameters"]//div[@class="offer-params__value"]//text()'))
        features = filter(None, document.xpath('//li[@class="offer-features__item"]/text()'))
        description = filter(None, document.xpath('//div[@id="description"]//text()'))
        return ' '.join(list(params) + list(features) + list(description))

    @staticmethod
    def parse_allegro(document):
        title = document.xpath('//h1/text()')
        params = document.xpath('//div[@class="attributes-container"]//span[@class="attribute-value"]/text()')
        description = filter(None, document.xpath('//div[@class="description"]//text()'))
        return ' '.join(title + params + list(description))

    @staticmethod
    def parse_olx(document):
        title = document.xpath('//h1/text()')
        params = filter(None, document.xpath('//table[contains(@class, "details")]//strong//text()'))
        description = filter(None, document.xpath('//div[@id="textContent"]//text()'))
        return ' '.join(title + list(params) + list(description))


__author__ = 'manitou'
