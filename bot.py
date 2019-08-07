# discord bot - main application
import discord
import random
import subprocess
import os
import sys
from utils import *
from commands import *

CMDCHAR = '!'
DATA = '/data'

TOKEN = sys.argv[1]
client = discord.Client()


def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


def check_permissions(message):
    if message.author.permissions_in(message.channel).kick_members:
        return True
    return False


def get_path(name, message):
    path = DATA + '/' + get_server_id(message) + '_' + name + '.txt'
    return path


def get_quotes(message):
    if not os.path.exists(get_path("quotes", message)):
        return list()
    f = open(get_path("quotes", message), "r+")
    f_content = f.read()
    quotes = f_content.split('[quote]')
    return [x.strip() for x in quotes]


def random_quote(message):
    quotes = get_quotes(message)
    if len(quotes) == 0:
        return "There are no quotes saved yet :("
    return quotes[random.randrange(0, len(quotes),1)]


def add_quote(quote_list, message):
    if not check_permissions(message):
        return "You do not have permissions to add quotes."
    f = open(get_path("quotes", message),'a+')
    quote = ""
    for s in quote_list:
        quote += s + ' '
    f.write("[quote] " + quote.strip())
    return "Added quote:\n" + quote


def cmd_quotes(args, message):
    if len(args) == 0:
        return random_quote(message)
    if args[0] == "path":
        return get_path('quotes', message)
    if args[0] == "debug":
        return get_server_id(message)
    if args[0] == "add":
        if len(args) < 2:
            return "Error: Not enough arguments."
        return add_quote(args[1:], message)
    if args[0] == "all":
        quotes = get_quotes(message)
        msg = ""
        for idx, q in enumerate(quotes):
            msg += str(idx + 1) + ': ' + q + '\n\n'
        return msg.strip()
    if represents_int(args[0]):
        quotes = get_quotes(message)
        qid = int(args[0])
        if qid > len(quotes) or qid == 0:
            return "Error: Not a valid quote #id"
        return quotes[qid - 1]


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = get_command(CMDCHAR, message)

    if command is None:
        return

    args = get_args(message)

    if command == "ping":
        msg = 'Pong! {0.author.mention}'
    
    if command == "zitat" or command == "quote":
        msg = cmd_quotes(args, message)

    msg = msg.format(message)

    await message.channel.send(msg) 


@client.event
async def on_ready():
    if os.path.exists("/data"):
        print('data already exists')
    else:
        subprocess.run(['bash', 'create_env.sh'])
        print('data created')

client.run(TOKEN)
