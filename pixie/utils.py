import discord

def check_permissions(message, admin=False):
    if admin and isinstance(message.author, discord.Member):
        if message.author.guild_permissions.administrator:
            return True
        else:
            return False
    elif message.author.permissions_in(message.channel).kick_members:
        return True
    return False


def get_server_id(message):
    return str(message.guild.id)


def ping(message):
    return "Pong!"


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
