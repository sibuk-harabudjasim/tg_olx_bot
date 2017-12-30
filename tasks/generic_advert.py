# -*- coding: utf-8 -*-
import aiohttp
from lxml import html
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

    def parse_gumtree(self, document):
        title = document.xpath('//h1[@class="item-title"]//text()')
        description = document.xpath('//div[@class="vip-details"]//div[@class="description"]//text()')
        return ' '.join(title + description).lower()


__author__ = 'manitou'
