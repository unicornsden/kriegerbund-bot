from git import *


def dev_help():
    return '''Usage:\n
    !dev help: This command\n\n
    !dev request name [--description description]\n
    e.g.: !dev request Cool Feature --description This feature would be really
    cool and awesome.\n\n
    !dev bugreport bug [--description description]\n
    e.g.: !dev bugreport Bug --description This bug is really awful :('''


def dev_issue(message, split, label):
    name = message.content.split(split, 1)[1].split('--description', 1)[0]
    if '--description' in message.content:
        description = message.content.split('--description')[1]
    else:
        description = None
    
    make_github_issue(name, description, label)

    return "Issue added!"


def cmd_dev(message, args):
    if len(args) == 0:
        return "Not enough arguments, run !dev help for more information"
    if args[0] == 'help':
        return dev_help()
    if len(args) < 2:
        return "Not enough arguments, run !dev help for more information"
    if args[0] == 'request':
        return dev_issue(message, args[0], 'enhancement')
    if args[0] == 'bugreport':
        return dev_issue(message, args[0], 'bug')
    return "Unknown command, run !dev help for more information" 
