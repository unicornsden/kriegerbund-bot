import os
import discord
import pickle
from . import messages
from . import utils
from . import data

USERPREFIX = '/user_'

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
    user = DiscordUser(id=message.author.id)
    user.data.lang = lang
    user.store_user_settings()
    messages.send_custom_message(message, messages.get_string('lang-changed') +
        lang)

def get_language(message):
    user = DiscordUser(id=message.author.id)
    user.read_user_settings()
    return user.data.lang


class UserData:
    dummy = ''
    lang = 'en'


class DiscordUser:

    def __init__(self, user=None, id=None):
        if (user is None and id is None) or (user is not None and id is not None):
            raise ValueError("Please supply either a value for user or a value for id")
        if user is not None and isinstance(user, discord.User):
            self.id = user.id
        elif id is not None and isinstance(id, int):
            self.id = id
        self.data = UserData()

    def get_path(self, file=False):
        if file:
            return self.get_path() + 'data.txt'
        return data.DATAPATH + USERPREFIX + str(self.id) + '/'

    def settings_exist(self, create_if_not_exists=False):
        settings_path = self.get_path(True)
        if os.path.isfile(settings_path):
            return True
        elif create_if_not_exists:
            self.store_user_settings()

    def read_user_settings(self):
        path = self.get_path()
        if not os.path.exists(path):
            os.makedirs(path)
            self.settings_exist(True)
            return
        if not self.settings_exist(True):
            return
        with open(self.get_path(True), 'rb') as input:
            self.data = pickle.load(input)

    def store_user_settings(self):
        path = self.get_path()
        if not os.path.exists(path):
            os.makedirs(path)
        with open(self.get_path(True), 'wb') as output:
            pickle.dump(self.data, output, pickle.HIGHEST_PROTOCOL)

