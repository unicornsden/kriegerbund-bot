import discord
import datetime
import pixie.data as data
from pixie.data import DataStorage

import pixie.messages as messages


def cmd_user(message, args):
    if len(args) == 0:
        return messages.MessageCode.UNKNOWN_ARGS
    if args[0] == 'help':
        return messages.send_message(message, 'user-help')
    if len(args) >= 2 and args[0] == 'setlang':
        if args[1].lower() in ['de', 'deutsch', 'german']:
            set_language(message, 'de')
            return
        elif args[1].lower() in ['en', 'english', 'englisch']:
            set_language(message, 'en')
            return
        else:
            set_language(message, args[1].lower())
            return
    return messages.MessageCode.UNKNOWN_ARGS


def set_language(message, lang):
    if not data.exists_lang(lang):
        messages.send_message(message, 'unknown-lang')
        return
    user = get_user(message)
    user.lang = lang
    user.store_settings()
    messages.send_custom_message(message, messages.get_string('lang-changed') +
        lang)


def get_language(message):
    return get_user(message).lang


def get_user(message):
    user = data.CACHE.get_user(message.user_id)
    if user is None:
        user = DiscordUser(id=message.author.id)
        user.read_settings()
        data.CACHE.add_user(user)
    return user


class DiscordUser(data.DataStorage):
    PATHPREFIX = 'user_'
    lang = 'en'

    def __init__(self, user=None, id=None, no_files=False):
        if (user is None and id is None) or (user is not None and id is not None):
            raise ValueError('user or id arguments required')
        elif user is not None and isinstance(user, discord.User):
            self.set('id', user.id)
        elif id is not None and isinstance(id, int):
            self.set('id', id)
        super(DiscordUser, self).__init__(no_files=no_files)

    def read_settings(self):
        try:
            self.read_data()
        except FileNotFoundError:
            return

    def store_settings(self):
        self.write_data()
