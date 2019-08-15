"""
Pixie Message Handling
======================
| ``pixie.messages``
| Handles message wrapping & data extraction from :class:`discord.message` objects
"""

import pixie.data as data
from pixie import users
import pixie.servers as servers
import asyncio
from .dev import cmd_dev
from .dice import cmd_dice
from .quotes import cmd_quotes
from .servers import cmd_server


class MessageCode:
    """MessageCode"""
    SENT = 0
    ERROR = 1
    NO_STRING = 2
    UNKNOWN_ARGS = 3
    UNKNOWN_STRING = '[[MessageCode=UNKNOWN_STRING]]'


class MessageWrapper:
    """
    A wrapper for the discord.Message class. Contains additional info.
    """
    # Shadow fields:
    # tts
    # type
    # author
    # content
    # nonce
    # embeds
    # channel
    # call
    # mention_everyone
    # mentions
    # channel_mentions
    # role_mentions
    # id
    # webhook_id
    # attachments
    # pinned
    # reactions
    # activity
    # application
    # guild
    # raw_mentions
    # raw_channel_mentions
    # raw_role_mentions
    # clean_content
    # created_at
    # edited_at
    # jump_url
    # system_content

    prefix = None
    message = None
    command = str()
    args = list()

    def __init__(self, message):
        """
        Constructor
        :param message: discord.Message to wrap
        """
        self.message = message
        self.server_id = message.guild.id
        self.user_id = message.author.id
        self.server_data = None

    def __getattr__(self, name):
        """__getattr__
        If the attribute does not exist in the wrapper, try getting it from the
        message.
        :param name: attribute name
        """
        return getattr(self.message, name)

    def get_server_data(self):
        self.server_data = servers.get_server_data(self.server_id)



def get_command(message, prefixes):
    """
    Gets a command (first word after the prefix) and stores it in the message
    :param message: MessageWrapper to extract from
    :param prefixes: list of valid prefixes or string of valid prefix
    :return: command name
    """
    args = message.content.split(' ')
    if isinstance(prefixes, list):
        for sign in prefixes:
            if message.content.startswith(sign):
                message.prefix = sign
                message.command = (args[0])[len(sign):]
                return message.command
    elif isinstance(prefixes, str):
        if message.content.startswith(prefixes):
            message.prefix = prefixes
            message.command = (args[0])[len(prefixes):]
            return message.command
    return None


def get_args(message):
    """
    Gets the arguments from a message's contents. Arguments are all strings separated by ' ' after the first.
    :param message: MessageWrapper to read from
    :return: list() of args
    """
    return message.content.split(' ')[1:]


def send_custom_message(message, msg, dm=False, user=None, format_content=True):
    """send_custom_message
    Sends a message with custom text.
    :param message: MessageWrapper object with data for formatting.
    :param msg: str() contents to send.
    :param dm: [Optional] Whether the message should be send as a dm.
    :param user: [Optional] Sends the message to a custom user. Requires
    dm=True
    :param format_content: [Optional] Whether .format(message) should be called on the
    content
    """

    channel = None

    # If send to dm ensure a dm channel is open
    if dm:
        if user is None:
            channel = message.author
        else:
            channel = user

    if not msg:
        return

    if format_content:
        msg = msg.format(message)

    # Default channel to the message channel
    if not channel:
        channel = message.channel

    asyncio.ensure_future(launch_message(channel, msg))
    return MessageCode.SENT


def send_message(message, string, dm=False, user=None, format_content=True):
    """send_message
    Sends a message with string supplied by [lang]_STRING.txt files.
    :param message: MessageWrapper object with data for formatting.
    :param string: Name of the string to read.
    :param dm: Whether the message should be sent to dm. Requires user to not be None
    :param user: User for dm usage.
    """
    msg = get_string(string, users.get_language(message))
    if not msg or msg == MessageCode.UNKNOWN_STRING:
        return MessageCode.NO_STRING

    return send_custom_message(message, msg, dm=dm, user=user, format_content=format_content)


async def launch_message(channel, msg):
    """launch_message
    Launch message to discord. This should only contain the await.
    :param channel: The discord.Channel to send to.
    :param msg: The message str to send.
    """
    await channel.send(msg)


def get_string(name, lang='en'):
    """
    Gets a string from data.STRINGS
    :param name: string name (key)
    :param lang: language to read string from
    :return: string content (value)
    """
    if lang in data.STRINGS:
        if name in data.STRINGS[lang]:
            return data.STRINGS[lang][name]
    if name in data.STRINGS['en']:
        return data.STRINGS['en'][name]
    return MessageCode.UNKNOWN_STRING


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
        code = send_message(message, 'help', dm=True)
    elif command == 'user':
        code = users.cmd_user(message, args)
    elif command == 'hallo':
        code = send_message(message, 'hallo')
    elif command == 'server':
        code = cmd_server(message, args)
    else:
        code = send_message(message, message.command)

    if code == MessageCode.UNKNOWN_ARGS:
        code = send_message(message, 'unknown-args')

    return code
