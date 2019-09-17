"""
Pixie Database Connection
===================
| Database module. Contains all functions for establishing a database connection.
"""
import json
import pathlib
import os.path
import github
from pathlib import Path
from configparser import ConfigParser

import psycopg2 as psycopg2

from pixie.utils import get_server_id
from pixie import utils
from pixie import data
from pixie import core


def read_database_config():
    """This function creates the file path for the database credentials, tries to open it. it returns a 1 if the file
    wasn't found, otherwise the file gets parsed into a string and gets returned
    :rtype: str
    """
    file = Path(os.path.dirname(data.__file__)).parent
    file = os.path.relpath(file)
    file = file + '/data/tokens/database.ini'
    section = 'postgresql'  # headline [postgresql] from the .ini file

    try:
        os.path.exists(file)
    except FileNotFoundError:
        print("database.ini file not found")
        return 1
    finally:
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(file)
        # get section
        credentials = {}
        if parser.has_section(section):

            params = parser.items(section)
            for param in params:
                credentials[param[0]] = param[1]
        else:
            print("section not found in the database.ini file")
        #buildastring thing
        stringcredentials = 'host="' + credentials['host'] + '", user="' + credentials['user'] + '", password="' + \
                            credentials['password'] + '", dbname="' + credentials['database'] + '"'
        return stringcredentials


def establish_database_connection():
    """Calls read_database_config and returns a 1 if no credentials were found
    otherwise, a database connection is created and a cursor returned
    """
    credentials = read_database_config()

    if credentials == 1:
        print("No credentials found")
        return 1

    conn = None
    try:
        # create connection
        conn = psycopg2.connect(credentials)
        # create cursor for doing things
        cur = conn.cursor()
        return cur
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 1


def print_version(cursor):
    print('PostgresSQL database version:')

    cursor.execute('SELECT version()')
