# -*- coding: utf-8 -*-
import asyncio
import re
import typing
import logging
import traceback


log = logging.getLogger()


class Hosts(object):
    GUMTREE = "gumtree"
    OLX = "olx"
    OTOMOTO = "otomoto"
    ALLEGRO = "allegro"
    OTODOM = "otodom"


_allowed_hosts = [
    Hosts.GUMTREE,
    Hosts.OTOMOTO,
    Hosts.OLX,
    Hosts.OTODOM,
]


def detect_host(url: str) -> str | None:
    host_re = re.compile(r'^.+?//(www.|m.)?(.+?)\.\w{2,}/')
    result = host_re.search(url)
    return result.group(2) if result else None


def is_allowed_host(host: str) -> bool:
    return host in _allowed_hosts


async def catch(coro: typing.Any) -> typing.Any:
    try:
        if asyncio.iscoroutine(coro):
            return await coro
        return coro
    except Exception as e:
        log.error(f"catch(): {str(e)}")
        log.error(traceback.format_exc())

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0",
}


__author__ = 'manitou'
