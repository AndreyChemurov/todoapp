from user import *
from exceptions import LoginException
from database import *

import sys
import pickle


def database_info_collection():
    # Collect data (name: password) from DB (table) 'users'
    # no files (!) like 'users.pkl'
    pass


def login():
    while True:
        try:
            name = input('Enter name: ')

            if name == "NONE":
                sys.exit(0)

            if not name:
                continue

            with open('users.pkl', 'rb') as file:
                u = pickle.load(file)

                if name not in u:
                    confirm_new_user = input('No "{}" user found. Create? [Y/N]: '.format(name))
                    if confirm_new_user in ('y', 'Y'):
                        new_user_password = input('Enter password: ')
                        new_user_password_confirm = input('Confirm password: ')

                        if new_user_password == new_user_password_confirm:
                            new_user = User(name=name, password=new_user_password)
                            u.update({name: new_user})

                            Database(u[name].get_dbname(), u[name].get_name(), 'localhost',
                                     u[name].get_password()).connect()

                            with open('users.pkl', 'wb') as file:
                                pickle.dump(u, file, pickle.HIGHEST_PROTOCOL)
                        else:
                            raise LoginException('Password mismatch.')
                    else:
                        raise LoginException('Login failed.')
                else:
                    Database(u[name].get_dbname(), u[name].get_name(), 'localhost', u[name].get_password()).connect()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # with open('users.pkl', 'wb') as file:
    #     pickle.dump({'test': None}, file, pickle.HIGHEST_PROTOCOL)

    login()
