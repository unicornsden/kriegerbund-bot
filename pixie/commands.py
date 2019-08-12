"""
Pixie Commands
==============
| ``pixie.commands``
| Handles command switching.
| TODO: MAYBE COMBINE WITH `pixie.messages`
"""
import asyncio
import time
from . import utils
from . import messages
from .messages import MessageCode
from .dev import cmd_dev
from .users import cmd_user
from .dice import cmd_dice
from .quotes import cmd_quotes


def handle_commands(message):
    """Handles the command switch & calls relevant function.
    Add your custom command here. But ensure that it isn't in "EN_STRINGS.txt"

    :param message: The message to handle.
    :type message: :class:`messages.MessageWrapper`
    :return type: :class:`pixie.messages.MessageCode`
    """
    command = message.command
    print(command)
    args = message.args

    if command == 'zitat' or command == 'quote':
        code = cmd_quotes(message, args)
    elif command == 'roll' or command == 'dice':
        code = cmd_dice(message, args)
    elif command == 'dev':
        code = cmd_dev(message, args)
    elif command == 'help':
        code = messages.send_message(message, 'help', dm=True)
    elif command == 'user':
        code = cmd_user(message, args)
    elif command == 'hallo':
        if utils.check_permissions(message):
            code = messages.send_message(message, 'hallo-mod')
        else:
            code = messages.send_message(message, 'hallo')
    else:
        code = messages.send_message(message, message.command)

    if code == MessageCode.UNKNOWN_ARGS:
        code = messages.send_message(message, 'unknown-args')

    return code


async def cmd_load(message, count, max_count=20):
    """
    TODO: FIX AND STUFF - REALLY JUST A TECH DEMO x)
    """
    msg = '`Loading .'
    if count == 0:
        new_msg = (await message.channel.send(msg + '`'))
        asyncio.ensure_future(cmd_load(new_msg, 1))
        return
    if count >= max_count:
        time.sleep(2)
        await message.edit(content='lul, just kidding, nothing\'s gonna happen')
        return
    time.sleep(0.5)
    for _ in range(count):
        msg += '.'
    msg += '`'
    await message.edit(content=msg)
    asyncio.ensure_future(cmd_load(message, count+1))
