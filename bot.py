# discord bot - main application
import discord
import subprocess
import sys
from commands import *

CMDCHAR = '!'
TOKEN = sys.argv[1]
client = discord.Client()

storage.init()


@client.event
async def on_message(message):
    """
    Called whenever a message is read by the bot.
    :param message: The discord.Message
    :return: None
    """

    # Don't react to bot itself
    if message.author == client.user:
        return

    command = get_command(message, CMDCHAR)

    # Don't do anything if there was no valid command.
    if command is None:
        return

    # Get args (all strings after the command separated by ' ')
    args = get_args(message)

    # noinspection PyBroadException
    # catch exceptions
    try:
        msg = handle_commands(message, command, args)
    except:
        msg = '''\
Something went wrong.
This is so sad. Alexa, play Despacito!'''

    if not msg:
        return

    msg = msg.format(message)
    await message.channel.send(msg)


@client.event
async def on_ready():
    if os.path.exists(storage.DATAPATH):
        print('data already exists')
    else:
        if not os.path.isfile('create_env.sh'):
            return
        subprocess.run(['bash', 'create_env.sh'])
        print('data created')

client.run(TOKEN)
