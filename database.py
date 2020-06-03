import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class MetaDatabase(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super(MetaDatabase, cls).__call__(*args, **kwargs)
            return cls.instances[cls]


class Database(metaclass=MetaDatabase):
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

        if self.connection is None:
            self.create_database()
            self.connection = psycopg2.connect(connection_str)
            self.cursor = self.connection.cursor()

            self.cursor.execute(sql.SQL("""CREATE TABLE todos (
                                                        id serial PRIMARY KEY,
                                                        task_name TEXT,
                                                        date_and_time TIMESTAMP,
                                                        comment TEXT);"""))
        else:
            # User planner menu
            pass

    def create_database(self):
        self.connection = psycopg2.connect(dbname='postgres')
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        self.cursor = self.connection.cursor()
        self.cursor.execute(sql.SQL("CREATE DATABASE {};".format(self.dbname)))
        self.cursor.execute(sql.SQL("CREATE USER {} WITH ENCRYPTED PASSWORD '{}';".format(self.user, self.password)))
        self.cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {};".format(self.dbname, self.user)))
        self.cursor.close()
        self.connection.close()
