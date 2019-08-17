import discord

def check_permissions(message, admin=False):
    """
    Checks the permissions of user calling function.
    If user has guild administrator permissions or permissions in the channel to kick users, return true
    :param message: discord.message object
    :param admin: boolean
    :return: boolean
    """
    if admin and isinstance(message.author, discord.Member):
        if message.author.guild_permissions.administrator:
            return True
        else:
            return False
    elif message.author.permissions_in(message.channel).kick_members:
        return True
    return False


def get_server_id(message):
    """
    Gets the server (guild) id and returns it as string
    :param message: discord.message object
    :return: string
    """
    return str(message.guild.id)


def ping(message):
    return "Pong!"


def represents_int(s):
    """
    Checks if given value is a valid integer
    :param s: Number or string to be checked
    :return: boolean
    """
    try:
        int(s)
        return True
    except ValueError:
        return False
