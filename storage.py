import settings
import os
from utils import *


def init():
    global DATA
    DATA = StorageContainer()
    DATA.EN_STRINGS = read_key_value_pairs('EN_STRINGS.txt')
    DATA.DE_STRINGS = read_key_value_pairs('DE_STRINGS.txt')


def get_path(message, name):
    path = settings.DATA + '/' + get_server_id(message) + '_' + name + '.txt'
    return path


def get_list(message, name, seperator):
    f = open(get_path(message, name), 'r')
    return f.read().split(seperator)


def read_strings():
    EN_STRINGS = dict()
    DE_STRINGS = dict()


def read_key_value_pairs(file):
    d = dict()
    with open(file, 'r+') as f:
        pairs = f.read().split('\n[')

        if len(pairs) != 0:
            if pairs[0][0] != '[':
                pairs.pop(0)
            else:
                pairs[0] = pairs[0][1:]

        for p in pairs:
            if len(p.split(']:')) != 2:
                continue
            key = p.split(']:')[0].strip()
            value = p.split(']:')[1].strip()
            d[key] = value
    return d


class StorageContainer:
    CMD_CHAR = '!'
    EN_STRINGS = dict()
    DE_STRINGS = dict()

init()
print(DATA.EN_STRINGS['unknown-args'].format(command=DATA.CMD_CHAR + 'test'))
