from . import data
from . import users
import asyncio

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

    prefix = None
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


def get_command(message, signs):
    args = message.content.split(' ')
    if isinstance(signs, list):
        for sign in signs:
            if message.content.startswith(sign):
                message.prefix = sign
                message.command = (args[0])[len(sign):]
                return message.command
    elif isinstance(signs, str):
        if message.content.startswith(signs):
            message.prefix = signs;
            message.command = (args[0])[len(signs):]
            return message.command
    return None


def get_args(message):
    return message.content.split(' ')[1:]


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
    msg = get_string(string, users.get_language(message))
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


def get_string(name, lang='en'):
    if lang in data.STRINGS:
        if name in data.STRINGS[lang]:
            return data.STRINGS[lang][name]
    if name in data.STRINGS['en']:
        return data.STRINGS['en'][name]
    return None


def command_unknown_usage(message, command=None, lang='en'):
    command = message.command
    name = message.prefix + command
    return get_string('unknown-args', lang).format(command=name)
