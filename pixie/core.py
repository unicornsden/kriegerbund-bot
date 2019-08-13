# discord bot - main application
import discord
import subprocess
import os
import sys
import traceback
from . import commands
from . import messages
from . import data
from .messages import MessageWrapper

client = discord.Client()

def run_bot(token=None):

    data.init()

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
async def on_message(message):
    """
    Called whenever a message is read by the bot.
    :param message: The discord.Message
    :return: None
    """
    # Wrap message to allow additional attributes to be passed along
    message = MessageWrapper(message)

    # Don't react to bot itself
    if message.author == client.user:
        return

    command = messages.get_command(message, data.CMDCHAR)

    # Don't do anything if there was no valid command.
    if command is None:
        return

    # Get args (all strings after the command separated by ' ')
    args = messages.get_args(message)
    message.args = args

    # noinspection PyBroadException
    # catch exceptions
    try:
        msg = commands.handle_commands(message)
    except Exception as e:
        with open('debug_log', 'a+') as f:
            f.write(str(e))
            f.write(traceback.format_exc())
        msg = '''\
Something went wrong.
This is so sad. Alexa, play Despacito!'''
        await message.channel.send(msg)


@client.event
async def on_ready():
    if os.path.exists(data.DATAPATH):
        print('data already exists')
    else:
        if not os.path.isfile('create_env.sh'):
            return
        subprocess.run(['bash', 'create_env.sh'])
        print('data created')

