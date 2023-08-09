# -*- coding: utf-8 -*-
import asyncio
import re

from utils import log


class Hosts(object):
    GUMTREE = 'gumtree'
    OLX = 'olx'
    OTOMOTO = 'otomoto'
    ALLEGRO = 'allegro'


_allowed_hosts = [
    Hosts.GUMTREE,
    Hosts.OTOMOTO,
    Hosts.OLX
]


def detect_host(url):
    host_re = re.compile(r'^.+?//(www.)?(.+?)\.\w{2,}/')
    result = host_re.search(url)
    return result.group(2) if result else ""


def is_allowed_host(host):
    return host in _allowed_hosts


async def catch(coro):
    try:
        if asyncio.iscoroutine(coro):
            await coro
    except Exception as e:
        log.error('catch(): {}', str(e))


__author__ = 'manitou'
