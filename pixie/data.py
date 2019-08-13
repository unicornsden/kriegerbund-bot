"""
Pixie Data Handling
===================
| ``pixie.data``
| Data storage module. Contains helper functions to read data and global variables used throughout the bot.
"""
import os
import builtins
from .utils import get_server_id

DATAPATH = './data/'


def init():
    """Initializes the global data vars. Most will be read from files or set to a default.
    / TODO: MORE GRANULARITY & BETTER DESCRIPTIONS
    """
    global STRINGS
    global LANG_ALTS
    global LANG_NAME
    global STORAGEPATH
    global CMDCHAR
    global REPO_OWNER
    global REPO_NAME

    CMDCHAR = '$'
    REPO_OWNER = 'unicornsden'
    REPO_NAME = 'pixie'

    string_path = DATAPATH + 'strings/'

    LANG_ALTS = dict()
    LANG_NAME = dict()
    STRINGS = dict()

    # Read inbuilt
    for f in os.listdir(string_path):
        if f.endswith('_STRINGS.txt'):
            s = str()
            lang = f.split('_STRINGS.txt')[0].lower()
            tup = read_key_value_pairs(string_path + f)
            STRINGS[lang] = tup[0]
            if s.strip() != '':
                LANG_NAME[lang] = get_lang_alts(tup[1], LANG_ALTS, lang)

    if os.path.isfile(DATAPATH + "datapath"):
        with open(DATAPATH + 'datapath', 'r') as f:
            STORAGEPATH = f.read().strip()
    else:
        STORAGEPATH = '/storage'


def get_lang_alts(string, output, lang):
    """ Gets the language alts from a string. / TODO: MORE GENERAL, MAYBE WRONG MODULE

    :param string: data to read
    :type string: str
    :param output: output dict
    :type output: dict[str,str]
    :param lang: base language
    :type lang: str
    :return: first alternative - should be the language name
    :return type: str
    """
    alts = string.split(',')
    for a in alts:
        output[a.strip()] = lang
    return alts[0]


def exists_lang(lang):
    """Checks whether a language abbr exists in data

    :param lang: language abbr
    :type lang: str
    :return: True if it exists, False otherwise
    :return type: bool
    """
    if lang.lower() in STRINGS:
        return True
    else:
        return False


def get_path(message, name):
    """Gets the STORAGEPATH + server id + name + .txt
    / TODO: SERIOUSLY WTF, THIS SHOULDN'T EXIST, JILLPLS THIS IS BAD CODE

    :param message: MessageWrapper for data
    :type message: :class:`messages.MessageWrapper`
    :param name: filename
    :type name: str
    :return: path to file
    :return type: str
    """
    path = STORAGEPATH + '/' + get_server_id(message) + '_' + name + '.txt'
    return path


def get_list(message, name, separator):
    """Gets the contents of a file as a list.

    :param message: MessageWrapper for data
    :type message: :class:`messages.MessageWrapper`
    :param name: filename
    :type name: str
    :param separator: character/string to split the file contents by
    :type separator: str
    :return: a list of all elements, can have length 0
    :return type: list(str)
    """
    f = open(get_path(message, name), 'r')
    return f.read().split(separator)


def read_key_value_pairs(filepath):
    """Reads key value pairs from a file.
    Format:
    [key]:value

    :param filepath: file to read from
    :type filepath: str
    :return: The key value pairs stored in a dictionary and the leftover string before the first pair.
    :return: tuple(dict[str,str],str)
    """
    pre_string = ''
    d = dict()
    with open(filepath, 'r+') as f:
        pairs = f.read().split('\n[')

        if len(pairs) != 0:
            if pairs[0][0] != '[':
                pre_string = pairs[0]
                pairs.pop(0)
            else:
                pairs[0] = pairs[0][1:]

        for p in pairs:
            if len(p.split(']:')) != 2:
                continue
            key = p.split(']:')[0].strip()
            value = p.split(']:')[1]
            d[key] = value
    return d, pre_string


class DataStorage:

    foo = ''

    def __init__(self, test=False):
        if test:
            self.foo = ['a000128128', 'b', 'c']
        else:
            self.foo = ['ab', 'cd', 'ef']

    def write_var(self, var):
        name = var[0]
        value = var[1]
        return '<<' + str(type(value)).split('\'')[1] + '>>' + name + ':' + str(value) + '\n'

    def build_data(self):
        out = ''
        for var, value in vars(self).items():
            out += self.write_var((var, value))
        return out

    def write_data(self, file_path, pre_string=None):
        with open(file_path, 'w+') as f:
            out = pre_string if pre_string is not None else ''
            if len(out) >= 2 and out[-2] != '\n':
                out += '\n'
            out += self.build_data()
            f.write(out)

    def read_data_string(self, input_string):
        var_rows = input_string.split('<<')
        if input_string[0:1] != '<<' and len(var_rows) > 0:
           var_rows = var_rows[1:]

        for row in var_rows:
            splits = row.split('>>')
            var_type = splits[0]
            splits = splits[1].split(':', 1)
            var_name = splits[0]
            var_value = splits[1]
            self.set_var(var_name, var_type, var_value)

    def read_data(self, file_path):
        with open(file_path, 'r') as f:
            input_string = f.read()
            self.read_data_string(input_string)

    def set_var(self, var_name, var_type, var_value):
        if var_type == 'list' or var_type == 'tuple':
            self.set_sequence(var_name, var_type, var_value)
            return
        elif var_type == 'dict':
            raise NotImplemented()

        try:
            setattr(self, var_name, getattr(builtins, var_type)(var_value))
        except Exception:
            pass

    def set_sequence(self, var_name, var_type, var_value):
        """TODO: CAN ONLY HANDLE STRING SEQUENCES

        :param var_name:
        :param var_type:
        :param var_value:
        :return:
        """
        var_value = var_value.strip()[1:-1]
        var_list = list()
        variables = var_value.split(',')
        for v in variables:
            var_list.append(v.strip()[1:-1])
        if var_type == 'tuple':
            setattr(self, var_name, tuple(var_list))
            return
        setattr(self, var_name, var_list)




