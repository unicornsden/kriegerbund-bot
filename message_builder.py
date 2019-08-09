import storage
import asyncio
from user_settings import *
from discord import Message


def send_custom_message(message, msg, dm=False, user=None, format_content=True):
    """send_custom_message
    Sends a message with custom text.
    :param message: MessageWrapper object with data for formatting.
    :param string: Name of the string to read.
    :param dm: [Optional] Whether the message should be send as a dm.
    :param user: [Optional] Sends the message to a custom user. Requires
    dm=True
    :param format: [Optional] Whether .format(message) should be called on the
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
    :param channel: [Optional] Specify the channel to send to.
    :param format: [Optional] Whether .format(message) should be called on the
    content
    """
    msg = get_string(string, get_language(message))
    if not msg:
        return MessageCode.NO_STRING

    return send_custom_message(message, msg, dm=dm, user=user,
            format_content=format_content)


async def launch_message(channel, msg):
    """launch_message
    Launch message to discord. This should only contain the await.
    :param channel: The discord.Channel to send to.
    :param msg: The message str to send.
    """
    await channel.send(msg)


def get_string(name, lang):
    if lang == 'de':
        if name in storage.DATA.DE_STRINGS:
            return storage.DATA.DE_STRINGS[name]
    if name in storage.DATA.EN_STRINGS:
        return storage.DATA.EN_STRINGS[name]
    return None


def command_unknown_usage(message, command):
    name = storage.DATA.CMD_CHAR + command
    return storage.DATA.EN_STRINGS['command-unknown-usage'].format(command=name)


async def prepare_dm(user):
    if user.dm_channel is None:
        await user.create_dm()


class MessageCode:
    """MessageCode"""
    SENT = 0
    ERROR = 1
    NO_STRING = 2
    UNKNOWN_ARGS = 3


class MessageWrapper:
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

    message = None
    command = str()
    args = list()

    def __init__(self, message):
        self.message = message

    def __getattr__(self, name):
        """__getattr__
        If the attribute does not exist in the wrapper, try getting it from the
        message.
        :param name: attribute name
        """
        return getattr(self.message, name)


storage.init()
print(get_string('help', 'de'))
print(get_string('command-unknown-usage', 'de'))
