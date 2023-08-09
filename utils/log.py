# -*- coding: utf-8 -*-
import logging

from core.config import config


def init():
    logging.basicConfig(
        # filename=config.LOGFILE_PATH,
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=logging.DEBUG if config.DEBUG else logging.INFO
    )


__author__ = 'manitou'
