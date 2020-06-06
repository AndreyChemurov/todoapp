import psycopg2
from psycopg2 import sql

from exceptions import *
from config import POSTGRES_CONFIG, COMMANDS


def database_info_collection(name: str):
    connection, cursor = None, None

    try:
        connection = psycopg2.connect(dbname=POSTGRES_CONFIG['POSTGRES_DBNAME'],
                                      user=POSTGRES_CONFIG['POSTGRES_USER'],
                                      host=POSTGRES_CONFIG['POSTGRES_HOST'],
                                      password=POSTGRES_CONFIG['POSTGRES_PASSWORD'])
        cursor = connection.cursor()
        cursor.execute(sql.SQL("SELECT * FROM users;"))
        users = cursor.fetchall()
    finally:
        connection.commit()
        cursor.close()
        connection.close()

    match = [user for user in users if name == user[1]]

    if not match:
        return None
    else:
        return (match[0][1], match[0][2]) if match[0][1] == name else None


def create_new_user(name: str):
    while True:
        creation = input(f'No "{name}" user found. Create? [y/n]: ')

        if creation in ('n', 'N'):
            raise LoginException('Creation canceled.')

        if not creation:
            continue

        if creation in ('y', 'Y'):
            connection, cursor = None, None
            password = input(f'Enter password for "{name}": ')

            try:
                connection = psycopg2.connect(dbname=POSTGRES_CONFIG['POSTGRES_DBNAME'],
                                              user=POSTGRES_CONFIG['POSTGRES_USER'],
                                              host=POSTGRES_CONFIG['POSTGRES_HOST'],
                                              password=POSTGRES_CONFIG['POSTGRES_PASSWORD'])
                cursor = connection.cursor()

                cursor.execute(sql.SQL(f"INSERT INTO users (user_id, username, password) VALUES "
                                       f"(DEFAULT, '{name}', '{password}');"))

                cursor.execute(sql.SQL(f'CREATE TABLE {name}_todos ('
                                       f'id serial PRIMARY KEY, '
                                       f'task_name TEXT,'
                                       f'date_and_time TIMESTAMP,'
                                       f'comment TEXT);'))

            except Exception as e:
                print(e)
            finally:
                connection.commit()
                cursor.close()
                connection.close()
                break
        else:
            raise LoginException('Wrong parameter. Only "y(Y), n(N)" allowed.')


def serve_current_user(user: tuple):
    username, password = user[0], user[1]

    while True:
        confirm_password = input(f'Enter password for "{username}": ')

        if not confirm_password:
            continue

        if password != confirm_password:
            raise DatabaseConnectionException(f'Wrong password for "{username}".')
        else:
            break

    run = True
    while run:
        g_commands = COMMANDS
        commands = input(f'({username})> ').split()

        for command in commands:
            if command in g_commands:
                g_commands = g_commands[command]
            else:
                pass
