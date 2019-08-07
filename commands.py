import discord


def get_command(signs, message):
    args = message.content.split(' ')
    print(args)
    if isinstance(signs, list):
        for sign in signs:
            if message.content.startswith(sign):
                return (args[0])[len(sign):]
    elif isinstance(signs, str):
        if message.content.startswith(signs):
            return (args[0])[len(signs):]
    return None


def get_args(message):
    return message.content.split(' ')[1:]
