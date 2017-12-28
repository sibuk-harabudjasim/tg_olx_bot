# -*- coding: utf-8 -*-
import importlib
import os

_required_params = ['DEBUG', 'TELEGRAM_TOKEN', 'DB_DSN', 'WEBHOOK_URL']


class ConfigContainer(object):
    def __init__(self):
        self._load_config(os.environ.get('BOT_CONFIG_PATH'))

    @staticmethod
    def _check_config(config):
        missed_params = [p for p in _required_params if getattr(config, p, None) is None]
        if missed_params:
            raise Exception('Param "{}" is required in config'.format(missed_params))
        return config

    def _load_config(self, path=None):
        config = importlib.import_module(path or 'config')
        self._check_config(config)
        self._apply_config(config)

    def _apply_config(self, config):
        _config = {k: v for k, v in config.__dict__.items() if not k.startswith('__')}
        self.__dict__.update(_config)


config = ConfigContainer()


__author__ = 'manitou'
