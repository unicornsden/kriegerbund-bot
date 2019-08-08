from git import *


def dev_help():
    return '''\
```Usage:
  
  !dev help: This command
 
  !dev request name [description...] 
  or
  !dev request "really long name" [description...]
  
  !dev bugreport name [description...] 
  or
  !dev bugreport "really long name" [description...]
  ```'''


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

    # name = message.content.split(split, 1)[1].split('--description', 1)[0]
    # if '--description' in message.content:
    #     description = message.content.split('--description')[1]
    # else:
    #     description = None
    description = '[Issue created by {user}]\n'.format(user=message.author.name) + description

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
