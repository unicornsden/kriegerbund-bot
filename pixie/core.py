"""
Pixie Core
==========
| ``pixie.core module``
| Contains calls to run and setup the bot
"""
import discord
import subprocess
import os
import sys
import traceback
from pixie import messages
import pixie.data as data
import pixie.debug as debug
import pixie.cache as cache
import pixie.servers as servers
from pixie.messages import MessageWrapper

client = discord.Client()
LOGGER = debug.Debugger()
LOGGER.run()


def run_bot(token=None):
    """Runs the bot

    :param token: Token supplied from non-default source, other wise data.DATAPATH/tokens/bot-token will be used
    :type token: str, optional
    """
    data.init()
    data.CACHE = cache.init()

    if token is not None:
        data.TOKEN = token.strip()
    if len(sys.argv) >= 2:
        data.TOKEN = sys.argv[1].strip()
    elif os.path.isfile(data.DATAPATH + 'tokens/bot-token'):
        with open(data.DATAPATH + 'tokens/bot-token', 'r') as f:
            data.TOKEN = f.read().strip()
    else:
        sys.exit("No TOKEN supplied")

    client.run(data.TOKEN)


@client.event
async def on_member_join(member):
    if member.guild.id in data.CACHE.cached_servers:
        channel_id = data.CACHE.cached_servers[member.guild.id].get('join-channel')
        if channel_id is None:
            return
        await member.guild.get_channel(channel_id).send(content='New member')
    return


@client.event
async def on_member_update(before, after):
    before_roles = before.roles
    after_roles = after.roles
    diff = list(set(after_roles) - set(before_roles))
    if len(diff) < 1:
        return
    s = servers.get_server_data(before.guild.id)
    if diff[0].id in s.get('welcome-roles'):
        channel_id = servers.get_server_data(before.guild.id).get('welcome-channel')
        if channel_id is None:
            return
        await before.guild.get_channel(channel_id).send(content=('Willkommen {0.name}'.format(before)))
    return


@client.event
async def on_message(message):
    """Called whenever a message is read by the bot.

    :param message: The message recieved
    :type message: :class:`discord.Message`
    """
    # Wrap message to allow additional attributes to be passed along
    message = MessageWrapper(message)

    # Don't react to bot itself
    if message.author == client.user:
        return

    command = messages.get_command(message, data.CMDCHARS)
    message.get_server_data()

    # Don't do anything if there was no valid command.
    if command is None:
        return

    # Get args (all strings after the command separated by ' ')
    args = messages.get_args(message)
    message.args = args

    # noinspection PyBroadException
    # catch exceptions
    try:
        msg = messages.handle_commands(message)
    except Exception as e:
        LOGGER.write(str(e), debug.Debugger.DebugCode.ERROR)
        LOGGER.write(traceback.format_exc(), debug.Debugger.DebugCode.ERROR)
        msg = '''\
Something went wrong.
This is so sad. Alexa, play Despacito!'''
        await message.channel.send(msg)


@client.event
async def on_ready():
    """Called when the bot is ready and running.
    """
    if os.path.exists(data.DATAPATH):
        print('data already exists')
    else:
        if not os.path.isfile('create_env.sh'):
            return
        subprocess.run(['bash', 'create_env.sh'])
        print('data created')

