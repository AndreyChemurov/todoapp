import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from exceptions import DatabaseConnectionException

import pickle


class Database:
    def __init__(self, dbname: str, user: str, host: str, password: str):
        self.dbname = dbname
        self.user = user
        self.host = host
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        connection_str = \
            "dbname='{}' ".format(self.dbname) + \
            "user='{}' ".format(self.user) + \
            "host='{}' ".format(self.host) + \
            "password='{}'".format(self.password)

        with open('users.pkl', 'rb') as file:
            databases = pickle.load(file)

            if self.dbname not in databases:
                self.create_database()

                self.connection = psycopg2.connect(connection_str)
                self.cursor = self.connection.cursor()

                self.cursor.execute(sql.SQL("""
                    CREATE TABLE todos 
                    (
                        id serial PRIMARY KEY,
                        task_name TEXT,
                        date_and_time TIMESTAMP,
                        comment TEXT
                    );
                """))

                self.connection.commit()
                self.cursor.close()
                self.connection.close()
            else:
                password = input('Enter password: ')

                if password != self.password:
                    raise DatabaseConnectionException('Incorrect password for "{}".'.format(self.user))

                self.connection = psycopg2.connect(connection_str)
                self.cursor = self.connection.cursor()
                todos_action(self.connection, self.cursor, self.user)

    def create_database(self):
        self.connection = psycopg2.connect(dbname='begin', user='begin', host='localhost', password='123')
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        self.cursor = self.connection.cursor()

        self.cursor.execute(sql.SQL("CREATE DATABASE {};".format(self.dbname)))
        self.cursor.execute(sql.SQL("CREATE USER {} WITH ENCRYPTED PASSWORD '{}';".format(self.user, self.password)))
        self.cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {};".format(self.dbname, self.user)))
        self.cursor.execute(sql.SQL("ALTER USER {} CREATEDB;".format(self.user)))
        self.cursor.execute(sql.SQL("ALTER USER {} WITH SUPERUSER;".format(self.user)))
        self.cursor.execute(sql.SQL("ALTER USER {} WITH CREATEROLE;".format(self.user)))
        self.cursor.execute(sql.SQL("ALTER USER {} WITH REPLICATION;".format(self.user)))
        self.cursor.execute(sql.SQL("ALTER USER {} WITH BYPASSRLS;".format(self.user)))

        self.connection.commit()
        self.cursor.close()
        self.connection.close()


def todos_action(connection, cursor, user):
    while True:
        command = input(f'({user})> ')

        if command == 'exit':
            break
