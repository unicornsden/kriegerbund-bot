import random
import os
from storage import *
from utils import *

#
# ACCESS STRINGS
#

def get_strings(message, name, separator):
    strings = get_list(message, name, separator)
    return [s.strip() for s in strings]


def get_quotes(message):
    if not os.path.exists(get_path(message, "quotes")):
        return list()
    f = open(get_path(message, "quotes"), "r+")
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
    if not os.path.isfile(get_path(message, "quotes")):
        f = open(get_path(message, "quotes"),'w+')
    else:
        f = open(get_path(message, "quotes" ),'a+')
    quote = ""
    for s in quote_list:
        quote += s + ' '
    f.write("[quote] " + quote.strip())
    return "Added quote:\n" + quote


def cmd_quotes(message, args):
    if len(args) == 0:
        return random_quote(message)
    if args[0] == "path":
        return get_path(message, 'quotes')
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
        print(quotes) 
        return quotes[qid - 1]
