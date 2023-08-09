# -*- coding: utf-8 -*-
import re
import logging
import typing

import aiohttp
from lxml import html


from utils.common import detect_host


log = logging.getLogger()

class GenericAdvertParser(object):
    async def parse(self, url: str) -> str:
        host = detect_host(url)
        if not host:
            log.warning(f"Unsupported URL (no expected host detected): {url}")
            return
        page_parser: typing.Callable[[html.Element], str] = getattr(self, 'parse_' + host, None)
        if not page_parser:
            log.warning(f"Unsupported URL ({host}): {url}")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as page:
                document: html.Element = html.fromstring(await page.read())
        return self._prettify(page_parser(document))

    @staticmethod
    def _prettify(text: str) -> str:
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    @staticmethod
    def parse_gumtree(document: html.Element) -> str:
        title = document.xpath('//h1[@class="item-title"]//text()')
        description = document.xpath('//div[@class="vip-details"]//div[@class="description"]//text()')
        return ' '.join(title + description).lower()

    @staticmethod
    def parse_otomoto(document: html.Element) -> str:
        params = filter(None, document.xpath('//div[@id="parameters"]//div[@class="offer-params__value"]//text()'))
        features = filter(None, document.xpath('//li[@class="offer-features__item"]/text()'))
        description = filter(None, document.xpath('//div[@id="description"]//text()'))
        return ' '.join(list(params) + list(features) + list(description))

    @staticmethod
    def parse_allegro(document: html.Element) -> str:
        title = document.xpath('//h1/text()')
        params = document.xpath('//div[@class="attributes-container"]//span[@class="attribute-value"]/text()')
        description = filter(None, document.xpath('//div[@class="description"]//text()'))
        return ' '.join(title + params + list(description))

    @staticmethod
    def parse_olx(document: html.Element) -> str:
        title = document.xpath('//h1/text()')
        params = filter(None, document.xpath('//div[@data-testid="main"]//ul//li//p/text()'))
        description = filter(None, document.xpath('//div[@data-cy="ad_description"]/div//text()'))
        return ' '.join(title + list(params) + list(description))


__author__ = 'manitou'
