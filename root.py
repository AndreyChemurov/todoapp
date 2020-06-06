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

            user = database_info_collection(name)

            if not user:
                create_new_user(name)
            else:
                serve_current_user(user)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    login()
