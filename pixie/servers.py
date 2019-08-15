"""
Pixie Server Data
=================
``pixie.servers``
"""
import discord
from pixie import data, messages, utils


def set_settings(message, args):
    if not utils.check_permissions(message, admin=True):
        return messages.send_message(message, 'no-permissions')
    set_what = args[0][3:]
    if set_what == 'welcome' and len(message.channel_mentions) != 0:
        channel = message.channel_mentions[0]
        if not isinstance(channel, discord.TextChannel):
            return messages.MessageCode.UNKNOWN_ARGS
        message.server_data.set('welcome-channel', channel.id)
        message.server_data.store_settings()
        messages.send_custom_message(message, messages.get_string('channel-set').format(channel, 'welcome channel'),
                                     format_content=False)
        return messages.MessageCode.SENT
    elif set_what == 'welcomeroles' and len(args) > 1:
        roles = args[1:]
        roles_confirmed = list()
        for r in roles:
            for gr in message.guild.roles:
                if r.lower() == gr.name.lower():
                    roles_confirmed.append(gr)
        confirmed_ids = list()
        for r in roles_confirmed:
            confirmed_ids.append(r.id)
        message.server_data.set('welcome-roles', confirmed_ids)
        message.server_data.store_settings()
        if len(confirmed_ids) < 1:
            return messages.MessageCode.UNKNOWN_ARGS
    elif set_what == 'join' and len(message.channel_mentions) != 0:
        channel = message.channel_mentions[0]
        if not isinstance(channel, discord.TextChannel):
            return messages.MessageCode.UNKNOWN_ARGS
        message.server_data.set('join-channel', channel.id)
        message.server_data.store_settings()
        messages.send_custom_message(message, messages.get_string('channel-set').format(channel, 'join channel'),
                                     format_content=False)
        return messages.MessageCode.SENT
    else:
        return messages.MessageCode.UNKNOWN_ARGS


def cmd_server(message, args):
    if len(args) == 0:
        return messages.MessageCode.UNKNOWN_ARGS
    elif args[0] == 'help':
        return messages.send_message(message, 'server-help')
    elif args[0].startswith('set'):
        return set_settings(message, args)
    elif args[0] == 'welcomeroles':
        roles = list()
        for r in message.server_data.get('welcome-roles'):
            role = message.guild.get_role(int(r))
            roles.append(role.name)
        return messages.send_custom_message(message, str(roles))
    elif args[0] == 'welcomechannel':
        return messages.send_custom_message(message, '<#' + str(message.server_data.get('welcome-channel')) + '>')
    elif args[0] == 'joinchannel':
        return messages.send_custom_message(message, '<#' + str(message.server_data.get('join-channel')) + '>')



def get_server_data(guild):
    if isinstance(guild, int):
        id = guild
    else:
        id = guild.id

    if id in data.CACHE.cached_servers:
        return data.CACHE.cached_servers[id]
    server_data = DiscordServer(id)
    server_data.read_data()
    return server_data


class DiscordServer(data.DataStorage):
    PATHPREFIX = '/server_'

    def __init__(self, id=None, guild=None, no_files=False):
        if (guild is None and id is None) or (guild is not None and id is not None):
            raise ValueError('user or id arguments required')
        elif guild is not None and isinstance(guild, discord.User):
            self.set('id', guild.id)
        elif id is not None and isinstance(id, int):
            self.set('id', id)
        super(DiscordServer, self).__init__(no_files=no_files)

    def read_settings(self):
        try:
            self.read_data()
        except FileNotFoundError:
            return

    def store_settings(self):
        self.write_data()
