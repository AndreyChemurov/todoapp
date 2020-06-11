import re
from psycopg2 import sql
from exceptions import DatabaseConnectionException


def show_all(username, cursor):
    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f'You have no tasks.')
    else:
        for task in match:
            print('ID: ', task[0])
            print('Task: ', task[1])
            print('Date and time: ', task[2])
            print('Comment: ', task[3])
            print('\n')


def show_today(username, cursor):
    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos WHERE date_and_time::date = CURRENT_DATE;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f'You have no tasks today.')
    else:
        for task in match:
            print('ID: ', task[0])
            print('Task: ', task[1])
            print('Date and time: ', task[2])
            print('Comment: ', task[3])
            print('\n')


def show_by_index(command, username, cursor):
    try:
        index = int(command[0])
    except ValueError:
        print('Index must be int.')
        raise

    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos WHERE id = {index};"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f'No such task with index {index}.')
    else:
        print('Task: ', match[0][1])
        print('Date and time: ', match[0][2])
        print('Comment: ', match[0][3])


def show_by_date(command, username, cursor):
    date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
    date = "".join(filter(date_regex.match, command))

    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos WHERE "
                           f"date_and_time::date = '{date}';"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f'No such task with date {date}.')
    else:
        for task in match:
            print('ID: ', task[0])
            print('Task: ', task[1])
            print('Date and time: ', task[2])
            print('Comment: ', task[3])
            print('\n')


def show_by_time(command, username, cursor):
    time_regex = re.compile(r'\d{2}:\d{2}:\d{2}|\d{2}:\d{2}')
    time = "".join(filter(time_regex.match, command))

    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos WHERE "
                           f"(to_char(date_and_time::time, 'HH24:MI') = '{time}' OR "
                           f"date_and_time::time = '{time}') AND date_and_time::date = CURRENT_DATE;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f'No such task with time {time}.')
    else:
        for task in match:
            print('ID: ', task[0])
            print('Task: ', task[1])
            print('Time: ', task[2])
            print('Comment: ', task[3])
            print('\n')


def show_by_task(command, username, cursor):
    task_name = ' '.join(command)

    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos WHERE "
                           f"task_name = '{task_name}';"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f"No such task with name '{task_name}'.")
    else:
        for task in match:
            print('ID: ', task[0])
            print('Task: ', task[1])
            print('Time: ', task[2])
            print('Comment: ', task[3])
            print('\n')


def add_task(command: list, username, cursor):
    date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
    date = "".join(filter(date_regex.match, command))

    if not date:
        raise DatabaseConnectionException('Cannot create task with no date.')

    time_regex = re.compile(r'\d{2}:\d{2}:\d{2}|\d{2}:\d{2}')
    time = "".join(filter(time_regex.match, command))

    if not time:
        raise DatabaseConnectionException('Cannot create task with no time.')

    task_finish_index = command.index(date)
    task_name = ' '.join(command[0:task_finish_index])

    if task_name == time:
        raise DatabaseConnectionException('Cannot create task with time equivalent to task name.')

    timestamp = date + ' ' + time

    comment_start_index = command.index(time) + 1
    comment = ' '.join(command[comment_start_index::])

    if not comment:
        comment = '-'

    if not task_name:
        raise DatabaseConnectionException('Cannot create task with no name.')

    try:
        cursor.execute(sql.SQL(f"INSERT INTO {username}_todos (id, task_name, date_and_time, comment) VALUES "
                               f"(DEFAULT, '{task_name}', '{timestamp}', '{comment}');"))
    except Exception as e:
        print(e)


def delete_all(username, cursor):
    pass


def delete_today(username, cursor):
    pass


def delete_by_index(command, username, cursor):
    pass


def delete_by_date(command, username, cursor):
    pass


def delete_by_time(command, username, cursor):
    pass


def delete_by_task(command, username, cursor):
    pass


def rewrite_all(username, cursor):
    pass


def rewrite_today(username, cursor):
    pass


def rewrite_by_index(command, username, cursor):
    pass


def rewrite_by_date(command, username, cursor):
    pass


def rewrite_by_time(command, username, cursor):
    pass


def rewrite_by_task(command, username, cursor):
    pass
