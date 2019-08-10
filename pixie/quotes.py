import random
import os
from . import messages, data, utils, users


#
# ACCESS STRINGS
#

def get_strings(message, name, separator):
    strings = data.get_list(message, name, separator)
    return [s.strip() for s in strings]


def get_quotes(message):
    if not os.path.exists(data.get_path(message, "quotes")):
        return list()
    f = open(data.get_path(message, "quotes"), "r+")
    f_content = f.read()
    quotes = f_content.split('[quote]')
    return [x.strip() for x in quotes]


def random_quote(message):
    quotes = get_quotes(message)
    if len(quotes) == 0:
        messages.send_message(message, 'quotes-none')

    messages.send_custom_message(message, quotes[random.randrange(0,
        len(quotes),1)])


def add_quote(quote_list, message):
    if not utils.check_permissions(message):
        messages.send_message(message, 'no-permissions')

    if not os.path.isfile(data.get_path(message, "quotes")):
        f = open(data.get_path(message, "quotes"),'w+')
    else:
        f = open(data.get_path(message, "quotes" ),'a+')
    quote = ""
    for s in quote_list:
        quote += s + ' '
    f.write("[quote] " + quote.strip())
    messages.send_custom_message(message, messages.get_string('quotes-added') + quote)


def cmd_quotes(message, args):
    if len(args) == 0:
        return random_quote(message)
    if args[0] == "add":
        if len(args) < 2:
            return "Error: Not enough arguments."
        return add_quote(args[1:], message)
    if args[0] == "all":
        quotes = get_quotes(message)
        msg = ""
        for idx, q in enumerate(quotes):
            msg += str(idx + 1) + ': ' + q + '\n\n'
        messages.send_custom_message(message, msg.strip())
    if utils.represents_int(args[0]):
        quotes = get_quotes(message)
        qid = int(args[0])
        if qid > len(quotes) or qid == 0:
            return messages.send_message(message, 'quotes-out-of-range')
        return messages.send_custom_message(message, quotes[qid - 1])

    if args[0] == 'help':
        return messages.send_message(message, 'quotes-help')
