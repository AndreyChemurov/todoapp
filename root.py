from user import *
from exceptions import *
from database import *

import sys


def login():
    while True:
        try:
            name = input('Enter name: ')

            if name == "NONE":
                sys.exit(0)

            if not name:
                continue

            if name not in users:
                confirm_new_user = input('No "{}" user found. Create? [Y/N]: '.format(name))
                if confirm_new_user in ('y', 'Y'):
                    new_user_password = input('Enter password: ')
                    new_user_password_confirm = input('Confirm password: ')

                    if new_user_password == new_user_password_confirm:
                        new_user = User(name=name, password=new_user_password)
                        users.update({name: new_user})
                    else:
                        raise LoginException('Password mismatch.')
                else:
                    raise LoginException('Login failed.')
            else:
                u = users[name]
                Database(u.get_name(), u.get_name(), 'localhost', u.get_password()).connect()
        except Exception as e:
            print(e)


def main():
    login()


if __name__ == '__main__':
    main()
