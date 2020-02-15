# -*- coding: utf-8 -*-
import asyncio
import sys

from tasks.generic_advert import GenericAdvertParser
from utils import log

if __name__ == '__main__':
    log.init()
    if len(sys.argv) < 2:
        print("Usage: python test_ad_parse.py <url>")
        exit(-1)
    url = sys.argv[1]

    async def run_parser():
        print('>>>>>>>>>>>> TASK START >>>>>>>>>>>>>>>>>>>')
        out = await GenericAdvertParser().parse(url)
        print("RESULT: ", out)
        print('>>>>>>>>>>>> TASK END >>>>>>>>>>>>>>>>>>>>>')
        await asyncio.sleep(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_parser())

__author__ = 'manitou'
