import os
from .utils import get_server_id

DATAPATH = './data/'

def init():
    global STRINGS
    global STORAGEPATH
    global CMDCHAR
    global REPO_OWNER
    global REPO_NAME

    CMDCHAR = '$'
    REPO_OWNER = 'unicornsden'
    REPO_NAME = 'pixie'

    string_path = DATAPATH + 'strings/'

    STRINGS = dict()

    # Read inbuilt
    for f in os.listdir(string_path):
        if f.endswith('_STRINGS.txt'):
            STRINGS[f.split('_STRINGS.txt')[0].lower()] =\
                read_key_value_pairs(string_path + f)

    if os.path.isfile(DATAPATH + "datapath"):
        with open(DATAPATH + 'datapath', 'r') as f:
            STORAGEPATH = f.read().strip()
    else:
        STORAGEPATH = '/storage'


def get_path(message, name):
    path = DATAPATH + '/' + get_server_id(message) + '_' + name + '.txt'
    return path


def get_list(message, name, seperator):
    f = open(get_path(message, name), 'r')
    return f.read().split(seperator)


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


init()
