import re
from psycopg2 import sql
from exceptions import DatabaseConnectionException


def show_all(username, cursor):
    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException('You have no tasks.')
    else:
        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for task in match:
            task_values = [str(val) for val in task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))


def show_today(username, cursor):
    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos WHERE date_and_time::date = CURRENT_DATE;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException('You have no tasks today.')
    else:
        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for task in match:
            task_values = [str(val) for val in task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))


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
        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for task in match:
            task_values = [str(val) for val in task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))


def show_by_date(command, username, cursor):
    date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
    date = "".join(filter(date_regex.match, command))

    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos WHERE "
                           f"date_and_time::date = '{date}';"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f'No such task with date {date}.')
    else:
        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for task in match:
            task_values = [str(val) for val in task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))


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
        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for _task in match:
            task_values = [str(val) for val in _task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))


def show_by_task(command, username, cursor):
    task_name = ' '.join(command)

    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos WHERE "
                           f"task_name = '{task_name}';"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f"No such tasks with name '{task_name}'.")
    else:
        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for _task in match:
            task_values = [str(val) for val in _task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))


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
        print('Added.')
    except Exception as e:
        print(e)


def delete_all(username, cursor):
    cursor.execute(sql.SQL(f"DELETE FROM {username}_todos RETURNING *;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException('You have no tasks.')
    else:
        print('Deleted:')

        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for task in match:
            task_values = [str(val) for val in task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))


def delete_today(username, cursor):
    cursor.execute(sql.SQL(f"DELETE FROM {username}_todos WHERE date_and_time::date = CURRENT_DATE RETURNING *;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException('You have no tasks today.')
    else:
        print('Deleted:')

        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for task in match:
            task_values = [str(val) for val in task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))


def delete_by_index(command, username, cursor):
    try:
        index = int(command[0])
    except ValueError:
        print('Index must be int.')
        raise

    cursor.execute(sql.SQL(f"DELETE FROM {username}_todos WHERE id = {index} RETURNING *;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f'No such task with index {index}.')
    else:
        print('Deleted:')

        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]

        task = [str(val) for val in match[0]]
        pretty_print.append(task)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))


def delete_by_date(command, username, cursor):
    date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
    date = "".join(filter(date_regex.match, command))

    cursor.execute(sql.SQL(f"DELETE FROM {username}_todos WHERE "
                           f"date_and_time::date = '{date}' RETURNING *;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f'No such task with date {date}.')
    else:
        print('Deleted:')

        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for task in match:
            task_values = [str(val) for val in task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))


def delete_by_time(command, username, cursor):
    time_regex = re.compile(r'\d{2}:\d{2}:\d{2}|\d{2}:\d{2}')
    time = "".join(filter(time_regex.match, command))

    cursor.execute(sql.SQL(f"DELETE FROM {username}_todos WHERE "
                           f"(to_char(date_and_time::time, 'HH24:MI') = '{time}' OR "
                           f"date_and_time::time = '{time}') AND date_and_time::date = CURRENT_DATE RETURNING *;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f'No such task with time {time}.')
    else:
        print('Deleted:')

        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for _task in match:
            task_values = [str(val) for val in _task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))


def delete_by_task(command, username, cursor):
    task_name = ' '.join(command)

    cursor.execute(sql.SQL(f"DELETE FROM {username}_todos WHERE "
                           f"task_name = '{task_name}' RETURNING *;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f"No such tasks with name '{task_name}'.")
    else:
        print('Deleted:')

        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for _task in match:
            task_values = [str(val) for val in _task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))


def rewrite_all(username, cursor):
    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException('You have no tasks.')
    else:
        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for _task in match:
            task_values = [str(val) for val in _task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))

        task_indices_list = [int(row[0]) for row in match]

        for index in task_indices_list:
            match_index = 0
            upd_values = input(f'ID {index} [Task, Date, Time, Comment]: ').split()

            date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
            date = "".join(filter(date_regex.match, upd_values))

            if not date:
                date = str(match[match_index][2].date())

            time_regex = re.compile(r'\d{2}:\d{2}:\d{2}|\d{2}:\d{2}')
            time = "".join(filter(time_regex.match, upd_values))

            if not time:
                time = str(match[match_index][2].time())

            task_name = None
            try:
                task_finish_index = upd_values.index(date)
                task_name = ' '.join(upd_values[0:task_finish_index])
            except Exception:
                pass

            if task_name == time:
                raise DatabaseConnectionException('Cannot create task with time equivalent to task name.')

            timestamp = date + ' ' + time

            comment = None
            try:
                comment_start_index = upd_values.index(time) + 1
                comment = ' '.join(upd_values[comment_start_index::])
            except Exception:
                pass

            if not comment:
                comment = str(match[match_index][3])

            if not task_name:
                task_name = str(match[match_index][1])

            try:
                cursor.execute(sql.SQL(f"UPDATE {username}_todos SET "
                                       f"task_name = '{task_name}', "
                                       f"date_and_time = '{timestamp}', "
                                       f"comment = '{comment}'"
                                       f"WHERE id = {index};"))
            except Exception as e:
                print(e)

            match_index += 1

        print(f'Updated {len(match)} rows.')


def rewrite_today(username, cursor):
    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos WHERE date_and_time::date = CURRENT_DATE;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException('You have no tasks today.')
    else:
        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for _task in match:
            task_values = [str(val) for val in _task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))

        task_indices_list = [int(row[0]) for row in match]

        for index in task_indices_list:
            match_index = 0
            upd_values = input(f'ID {index} [Task, Date, Time, Comment]: ').split()

            date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
            date = "".join(filter(date_regex.match, upd_values))

            if not date:
                date = str(match[match_index][2].date())

            time_regex = re.compile(r'\d{2}:\d{2}:\d{2}|\d{2}:\d{2}')
            time = "".join(filter(time_regex.match, upd_values))

            if not time:
                time = str(match[match_index][2].time())

            task_name = None
            try:
                task_finish_index = upd_values.index(date)
                task_name = ' '.join(upd_values[0:task_finish_index])
            except Exception:
                pass

            if task_name == time:
                raise DatabaseConnectionException('Cannot create task with time equivalent to task name.')

            timestamp = date + ' ' + time

            comment = None
            try:
                comment_start_index = upd_values.index(time) + 1
                comment = ' '.join(upd_values[comment_start_index::])
            except Exception:
                pass

            if not comment:
                comment = str(match[match_index][3])

            if not task_name:
                task_name = str(match[match_index][1])

            try:
                cursor.execute(sql.SQL(f"UPDATE {username}_todos SET "
                                       f"task_name = '{task_name}', "
                                       f"date_and_time = '{timestamp}', "
                                       f"comment = '{comment}'"
                                       f"WHERE id = {index};"))
            except Exception as e:
                print(e)

            match_index += 1

        print(f'Updated {len(match)} rows.')


def rewrite_by_index(command, username, cursor):
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
        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]

        task = [str(val) for val in match[0]]
        pretty_print.append(task)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))

        upd_values = input(f'ID {index} [Task, Date, Time, Comment]: ').split()

        date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
        date = "".join(filter(date_regex.match, upd_values))

        if not date:
            date = str(match[0][2].date())

        time_regex = re.compile(r'\d{2}:\d{2}:\d{2}|\d{2}:\d{2}')
        time = "".join(filter(time_regex.match, upd_values))

        if not time:
            time = str(match[0][2].time())

        task_name = None
        try:
            task_finish_index = upd_values.index(date)
            task_name = ' '.join(upd_values[0:task_finish_index])
        except Exception:
            pass

        if task_name == time:
            raise DatabaseConnectionException('Cannot create task with time equivalent to task name.')

        timestamp = date + ' ' + time

        comment = None
        try:
            comment_start_index = upd_values.index(time) + 1
            comment = ' '.join(upd_values[comment_start_index::])
        except Exception:
            pass

        if not comment:
            comment = str(match[0][3])

        if not task_name:
            task_name = str(match[0][1])

        try:
            cursor.execute(sql.SQL(f"UPDATE {username}_todos SET "
                                   f"task_name = '{task_name}', "
                                   f"date_and_time = '{timestamp}', "
                                   f"comment = '{comment}'"
                                   f"WHERE id = {index};"))
        except Exception as e:
            print(e)

    print(f'Updated by index {index}.')


def rewrite_by_date(command, username, cursor):
    date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
    date = "".join(filter(date_regex.match, command))

    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos WHERE date_and_time::date = '{date}';"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException('You have no tasks today.')
    else:
        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for _task in match:
            task_values = [str(val) for val in _task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))

        task_indices_list = [int(row[0]) for row in match]

        for index in task_indices_list:
            match_index = 0
            upd_values = input(f'ID {index} [Task, Date, Time, Comment]: ').split()

            date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
            date = "".join(filter(date_regex.match, upd_values))

            if not date:
                date = str(match[match_index][2].date())

            time_regex = re.compile(r'\d{2}:\d{2}:\d{2}|\d{2}:\d{2}')
            time = "".join(filter(time_regex.match, upd_values))

            if not time:
                time = str(match[match_index][2].time())

            task_name = None
            try:
                task_finish_index = upd_values.index(date)
                task_name = ' '.join(upd_values[0:task_finish_index])
            except Exception:
                pass

            if task_name == time:
                raise DatabaseConnectionException('Cannot create task with time equivalent to task name.')

            timestamp = date + ' ' + time

            comment = None
            try:
                comment_start_index = upd_values.index(time) + 1
                comment = ' '.join(upd_values[comment_start_index::])
            except Exception:
                pass

            if not comment:
                comment = str(match[match_index][3])

            if not task_name:
                task_name = str(match[match_index][1])

            try:
                cursor.execute(sql.SQL(f"UPDATE {username}_todos SET "
                                       f"task_name = '{task_name}', "
                                       f"date_and_time = '{timestamp}', "
                                       f"comment = '{comment}'"
                                       f"WHERE id = {index};"))
            except Exception as e:
                print(e)

            match_index += 1

        print(f'Updated {len(match)} rows.')


def rewrite_by_time(command, username, cursor):
    time_regex = re.compile(r'\d{2}:\d{2}:\d{2}|\d{2}:\d{2}')
    time = "".join(filter(time_regex.match, command))

    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos WHERE "
                           f"(to_char(date_and_time::time, 'HH24:MI') = '{time}' OR "
                           f"date_and_time::time = '{time}') AND date_and_time::date = CURRENT_DATE;"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f'No such task with time {time}.')
    else:
        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for _task in match:
            task_values = [str(val) for val in _task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))

        task_indices_list = [int(row[0]) for row in match]

        for index in task_indices_list:
            match_index = 0
            upd_values = input(f'ID {index} [Task, Date, Time, Comment]: ').split()

            date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
            date = "".join(filter(date_regex.match, upd_values))

            if not date:
                date = str(match[match_index][2].date())

            time_regex = re.compile(r'\d{2}:\d{2}:\d{2}|\d{2}:\d{2}')
            time = "".join(filter(time_regex.match, upd_values))

            if not time:
                time = str(match[match_index][2].time())

            task_name = None
            try:
                task_finish_index = upd_values.index(date)
                task_name = ' '.join(upd_values[0:task_finish_index])
            except Exception:
                pass

            if task_name == time:
                raise DatabaseConnectionException('Cannot create task with time equivalent to task name.')

            timestamp = date + ' ' + time

            comment = None
            try:
                comment_start_index = upd_values.index(time) + 1
                comment = ' '.join(upd_values[comment_start_index::])
            except Exception:
                pass

            if not comment:
                comment = str(match[match_index][3])

            if not task_name:
                task_name = str(match[match_index][1])

            try:
                cursor.execute(sql.SQL(f"UPDATE {username}_todos SET "
                                       f"task_name = '{task_name}', "
                                       f"date_and_time = '{timestamp}', "
                                       f"comment = '{comment}'"
                                       f"WHERE id = {index};"))
            except Exception as e:
                print(e)

            match_index += 1

        print(f'Updated {len(match)} rows.')


def rewrite_by_task(command, username, cursor):
    task_name = ' '.join(command)

    cursor.execute(sql.SQL(f"SELECT * FROM {username}_todos WHERE "
                           f"task_name = '{task_name}';"))
    match = cursor.fetchall()

    if not match:
        raise DatabaseConnectionException(f"No such tasks with name '{task_name}'.")
    else:
        pretty_print = [
            ['ID', 'Task', 'Date and time', 'Comment'],
            ['----', '------------', '----------------------', '----------------']
        ]
        for _task in match:
            task_values = [str(val) for val in _task]
            pretty_print.append(task_values)

        lens = [max(map(len, col)) for col in zip(*pretty_print)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in pretty_print]
        print('\n'.join(table))

        task_indices_list = [int(row[0]) for row in match]

        for index in task_indices_list:
            match_index = 0
            upd_values = input(f'ID {index} [Task, Date, Time, Comment]: ').split()

            date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
            date = "".join(filter(date_regex.match, upd_values))

            if not date:
                date = str(match[match_index][2].date())

            time_regex = re.compile(r'\d{2}:\d{2}:\d{2}|\d{2}:\d{2}')
            time = "".join(filter(time_regex.match, upd_values))

            if not time:
                time = str(match[match_index][2].time())

            task_name = None
            try:
                task_finish_index = upd_values.index(date)
                task_name = ' '.join(upd_values[0:task_finish_index])
            except Exception:
                pass

            if task_name == time:
                raise DatabaseConnectionException('Cannot create task with time equivalent to task name.')

            timestamp = date + ' ' + time

            comment = None
            try:
                comment_start_index = upd_values.index(time) + 1
                comment = ' '.join(upd_values[comment_start_index::])
            except Exception:
                pass

            if not comment:
                comment = str(match[match_index][3])

            if not task_name:
                task_name = str(match[match_index][1])

            try:
                cursor.execute(sql.SQL(f"UPDATE {username}_todos SET "
                                       f"task_name = '{task_name}', "
                                       f"date_and_time = '{timestamp}', "
                                       f"comment = '{comment}'"
                                       f"WHERE id = {index};"))
            except Exception as e:
                print(e)

            match_index += 1

        print(f'Updated {len(match)} rows.')
