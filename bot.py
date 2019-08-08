# discord bot - main application
import discord
import random
import subprocess
import os
import sys
import settings
from utils import *
from commands import *
from dev import *

CMDCHAR = '!'
TOKEN = sys.argv[1]
client = discord.Client()

settings.init()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = get_command(message, CMDCHAR)

    if command is None:
        return

    args = get_args(message)

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
    if os.path.exists(settings.DATA):
        print('data already exists')
    else:
        subprocess.run(['bash', 'create_env.sh'])
        print('data created')

client.run(TOKEN)
