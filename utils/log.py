# -*- coding: utf-8 -*-
import json
import logging

from core.config import config

# TODO: add logging to Bot class


def init():
    logging.basicConfig(
        # filename=config.LOGFILE_PATH,
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=logging.DEBUG if config.DEBUG else logging.INFO
    )


def _make_message(fmt, *args, **kwargs):
    if not isinstance(fmt, (str, bytes)):
        return json.dumps(fmt)
    return fmt.format(*args, **kwargs)


def debug(fmt, *args, **kwargs):
    logging.debug(_make_message(fmt, *args, **kwargs))


def info(fmt, *args, **kwargs):
    logging.info(_make_message(fmt, *args, **kwargs))


def error(fmt, *args, **kwargs):
    logging.exception(_make_message(fmt, *args, **kwargs))


def warning(fmt, *args, **kwargs):
    logging.warning(_make_message(fmt, *args, **kwargs))


__author__ = 'manitou'
