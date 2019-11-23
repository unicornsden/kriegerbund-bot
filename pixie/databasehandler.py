"""
Pixie Database Connection
===================
| Database module. Contains all functions for establishing a database connection.
"""
import json
import pathlib
import os.path
import github
import psycopg2.extras
from pathlib import Path
from configparser import ConfigParser

import psycopg2 as psycopg2
from psycopg2.extensions import cursor

from pixie.utils import get_server_id
from pixie import utils
from pixie import data
from pixie import core


class DatabaseHandler:
    cursor = cursor()

    def __init__(self):
        credentials = self.read_config()
        conn = None
        try:
            # create connection
            conn = psycopg2.connect(credentials)
            # create cursor for doing things
            self.cursor = conn.Cursor
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def read_config(self):
        """This function creates the file path for the database credentials, tries to open it. it returns a 1 if the file
        wasn't found, otherwise the file gets parsed into a string and returned
        :rtype: str
        """
        file = Path(os.path.dirname(data.__file__)).parent
        file = os.path.relpath(file)
        file = file + '/data/tokens/database.ini'
        section = 'postgresql'  # headline [postgresql] from the .ini file

        try:
            os.path.exists(file)
            # create a parser
            parser = ConfigParser()
            # read config file
            parser.read(file)
            # get section
            credentials = {}
            if parser.has_section(section):

                params = parser.items(section)
                # what the fuck do i do here?
                for param in params:
                    credentials[param[0]] = param[1]
            else:
                print("section not found in the database.ini file")
            # buildastring thing
            stringcredentials = 'host="' + credentials['host'] + '", user="' + credentials['user'] + '", password="' + \
                                credentials['password'] + '", dbname="' + credentials['database'] + '"'
            return stringcredentials
        except FileNotFoundError:
            print("database.ini file not found")
            print("Is the database.ini in " + file + "?")

    def establish_database_connection(self):
        """Calls read_database_config and returns a 1 if no credentials were found
        otherwise, a database connection is created and a cursor returned
        """
        credentials = self.read_config()
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


    def print_version(self):
        print('PostgresSQL database version:')
        try:
            self.cursor.execute('SELECT version()')
        except AttributeError:
            pass
        self.cursor.fetchall()
