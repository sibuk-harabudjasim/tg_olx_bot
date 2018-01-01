# -*- coding: utf-8 -*-
import importlib
import os

_required_params = {
    'DEBUG': bool,
    'TELEGRAM_TOKEN': str,
    'DB_DSN': str,
    'WEBHOOK_URL': str,
    'DEFAULT_TASK_INTERVAL': int
}


class ConfigContainer(object):
    _config_container = None

    def __init__(self):
        self._load_config(os.environ.get('BOT_CONFIG_PATH'))
        self._config_container = {}

    def _get_param(self, name):
        cast_type = _required_params.get(name, str)
        var = os.environ.get(name)
        if var is not None:
            return cast_type(var)
        return self._config_container.get(name, None)

    def _check_config(self, config):
        missed_params = [p for p in _required_params if self._get_param(p) is None]
        if missed_params:
            raise Exception('Param "{}" is required in config'.format(missed_params))
        return config

    def _load_config(self, path=None):
        config = importlib.import_module(path or 'config')
        self._apply_config(config)
        self._check_config(config)

    def _apply_config(self, config):
        _config = {k: v for k, v in config.__dict__.items() if not k.startswith('__')}
        self._config_container = _config

    __getattr__ = _get_param


config = ConfigContainer()


__author__ = 'manitou'
