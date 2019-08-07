import discord

def check_permissions(message):
    if message.author.permissions_in(message.channel).kick_members:
        return True
    return False


def get_server_id(message):
    return str(message.guild.id)


def ping():
    return "Pong!"


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
