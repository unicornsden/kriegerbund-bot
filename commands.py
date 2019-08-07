import discord
import asyncio
from string_set import *
from dev import *
import dice


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
    if command == 'roll':
        return dice.cmd_roll(message, args)
    if command == 'dev':
        return cmd_dev(message, args)
    if command == 'help': 
        asyncio.ensure_future(cmd_help(message))
        return ''


async def cmd_help(message):
    help_msg = '''\
```Kriegerbund Bot Help```
```Commands:

![command] help: Returns help for the specific command

!ping: Pong!

!quote and !zitat: Quote function, default: random quote

!dev: Development tools for reporting bugs and requesting
features```'''
    if message.author.dm_channel is None:
        await message.author.create_dm()
    await message.author.dm_channel.send(help_msg)
