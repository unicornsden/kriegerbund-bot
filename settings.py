import os


def init():
    global DATA
    if os.path.isfile("datapath"):
        DATA = open("datapath", 'r').read().strip()
    else:
        DATA = '/data'
