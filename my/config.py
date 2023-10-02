import os
import json

global config

def load():
    global config
    try:
        f = open("/home/vyacheslav/.config/qtile/config.json")
        config = json.load(f)
        f.close()
    except:
        config = {}

def save():
    global config
    try:
        f = open("/home/vyacheslav/.config/qtile/config.json", "w")
        json.dump(config, f)
        f.close()
    except:
        config = {}


def put(system, key, value):
    global config
    if system not in config:
        config[system] = {}
    config[system][key] = value


def get(system, key, default=None):
    global config
    if system not in config:
        return default
    if key not in config[system]:
        return default
    return config[system][key]
