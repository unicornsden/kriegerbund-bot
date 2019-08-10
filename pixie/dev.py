from .git import *
from . import messages
from .messages import MessageCode


def dev_help(message):
    messages.send_message(message, 'dev-help')


def dev_issue(message, split, label):
    content = message.content.split(split, 1)[1].strip()
    if content[0] == '\"':
        splits = content[1:].split('\"', 1)
        name = splits[0]
        description = splits[1]
    else:
        splits = content.split(' ', 1)
        name = splits[0]
        description = splits[1]

    description = '[Issue created by {user}]\n'.format(user=message.author.name) + description
    make_github_issue(name, description, label)
    messages.send_message(message, 'dev-issue-created')


def cmd_dev(message, args):
    if len(args) == 0:
        return MessageCode.UNKNOWN_ARGS
    if args[0] == 'help':
        return dev_help(message)
    if len(args) < 2:
        return MessageCode.UNKNOWN_ARGS
    if args[0] == 'request':
        return dev_issue(message, args[0], 'type: enhancement')
    if args[0] == 'bugreport':
        return dev_issue(message, args[0], 'type: bug')
    return MessageCode.UNKNOWN_ARGS
