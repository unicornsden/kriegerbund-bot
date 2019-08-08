import settings
from utils import *


def get_path(message, name):
    path = settings.DATA + '/' + get_server_id(message) + '_' + name + '.txt'
    return path


def get_list(message, name, seperator):
    f = open(get_path(message, name), 'r')
    return f.read().split(seperator)
