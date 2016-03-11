#!/usr/bin/env python

import os.path
import json

from .config_defaults import defaults

Settings = dict(defaults)


def read_configuration(config_file):
    """Merge user configuration.
    """
    configuration = Settings

    with open(os.path.expanduser(config_file)) as cnf:
        loaded_configuration = json.load(cnf)
        configuration.update(loaded_configuration)

    return configuration


def update_settings(configuration_file=None):
    global Settings
    if not configuration_file:
        configuration_file = '~/.misnamer.json'
    Settings.update(read_configuration(configuration_file))


def set_option(key, value):
    global Settings
    Settings[key] = value
