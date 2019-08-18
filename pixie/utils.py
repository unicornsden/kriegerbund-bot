import discord


def check_permissions(message, admin=False):
    """Checks the permissions of user calling function.
    If user has guild administrator permissions or permissions in the channel to kick users, return true

    :param message: The message to check for an author.
    :type message: :class:`messages.MessageWrapper`
    :param admin: Check for admin privileges instead if True
    :type admin: bool
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
    """Gets the server (guild) id and returns it as string

    :param message: The message to get the guild from.
    :type message: :class:`messages.MessageWrapper`
    :return: The server id as a string. TODO: FIX PRIVATE MESSAGES
    :return type: string
    """
    return str(message.guild.id)


def represents_int(s):
    """Checks if given value is a valid integer

    :param s: Number or string to be checked
    :type s: Any.
    :return: True if the input can be cast to int. False otherwise.
    :return type: boolean
    """
    try:
        int(s)
        return True
    except ValueError:
        return False
