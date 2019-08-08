import storage


def get_string(name, lang):
    if lang == 'de':
        if name in storage.DATA.DE_STRINGS:
            return storage.DATA.DE_STRINGS[name]
    if name in storage.DATA.EN_STRINGS:
        return storage.DATA.EN_STRINGS[name]
    return ''


def command_unknown_usage(message, command):
    name = storage.DATA.CMD_CHAR + command
    return storage.DATA.EN_STRINGS['command-unknown-usage'].format(command=name)


storage.init()
print(get_string('help', 'de'))
print(get_string('command-unknown-usage', 'de'))
