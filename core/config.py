# -*- coding: utf-8 -*-
import typing
import types
import os
from dotenv import load_dotenv


def is_optional(type_: typing.Type) -> bool:
    return typing.get_origin(type_) in [typing.Union, types.UnionType] and typing.get_args(type_)[1] is types.NoneType


class ConfigContainer(object):
    DEBUG: bool | None = False
    TELEGRAM_TOKEN: str = None
    DATABASE_URL: str = None
    WEBHOOK_URL: typing.Optional[str] = None
    DEFAULT_TASK_INTERVAL: int = 10 # Minutes

    def __init__(self):
        load_dotenv()
        self._load_config()

    def _load_config(self):
        print(typing.get_type_hints(self))
        for param, type_ in typing.get_type_hints(self).items():
            raw_value = os.getenv(param)
            if not raw_value:
                if not is_optional(type_):
                    raise Exception(f'Param "{param}" is required in environment variables')
                continue
            cast = typing.get_args(type_)[0] if is_optional(type_) else type_
            setattr(self, param, cast(raw_value))


config = ConfigContainer()


__author__ = 'manitou'
