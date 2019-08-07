import discord
from string_set import *
from dev import *


def get_command(message, signs):
    args = message.content.split(' ')
    print(args)
    if isinstance(signs, list):
        for sign in signs:
            if message.content.startswith(sign):
                return (args[0])[len(sign):]
    elif isinstance(signs, str):
        if message.content.startswith(signs):
            return (args[0])[len(signs):]
    return None


def get_args(message):
    return message.content.split(' ')[1:]


def handle_commands(message, command, args):
    if command == 'ping':
        return ping()
    if command == 'zitat' or command == 'quote':
        return cmd_quotes(message, args)
    if command == 'dev':
        return cmd_dev(message, args)

