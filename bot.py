# discord bot - main application
import discord
import subprocess
import sys
import traceback
from commands import *
from message_builder import MessageWrapper
from message_builder import MessageCode

CMDCHAR = '!'
if len(sys.argv) >= 2:
    TOKEN = sys.argv[1]
elif os.path.isfile('./bot-token'):
    with open('./bot-token', 'r') as f:
        TOKEN = f.read()
else:
    sys.exit("No TOKEN supplied")

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

    command = get_command(message, storage.CMDCHAR)

    # Don't do anything if there was no valid command.
    if command is None:
        return

    # Wrap message to allow additional attributes to be passed along
    message = MessageWrapper(message)
    message.prefix = storage.CMDCHAR
    message.command = command

    # Get args (all strings after the command separated by ' ')
    args = get_args(message)
    message.args = args

    # noinspection PyBroadException
    # catch exceptions
    try:
        msg = handle_commands(message)
    except Exception as e:
        print('Exception thrown: ' + str(e) + '\n')
        traceback.print_exc()
        msg = '''\
Something went wrong.
This is so sad. Alexa, play Despacito!'''

    if not msg or isinstance(msg, int):
        return

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

client.run(TOKEN.strip())
