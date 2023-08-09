# -*- coding: utf-8 -*-
import asyncio
import sys
import logging

from tasks.generic_advert import GenericAdvertParser
from utils.log import init as log_init

log = logging.getLogger()

if __name__ == '__main__':
    log_init()
    if len(sys.argv) < 2:
        print("Usage: python test_ad_parse.py <url>")
        exit(-1)
    url = sys.argv[1]

    async def run_parser():
        log.info(">>>>>>>>>>>> TASK START >>>>>>>>>>>>>>>>>>>")
        out = await GenericAdvertParser().parse(url)
        log.info(f"RESULT: {out}")
        log.info(">>>>>>>>>>>> TASK END >>>>>>>>>>>>>>>>>>>>>")
        await asyncio.sleep(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_parser())

__author__ = 'manitou'
