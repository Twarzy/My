#! python3
# Body tracker - is program that helps you track your body measurements.
# It uses SQL to database management.

import time
from users import User
from database import Database

program_database_filename = 'body_tracker_db.s3db'


def header():
    print('_' * 79)
    print('FIT_BETA - YOUR PERSONAL FIT DIARY by Bartosz Kowalik'.center(79, ' '))
    print('_' * 79)
    print(time.ctime().rjust(79, ' '))
    print('_' * 79)
    print()


def start_menu():
    header()

    user = User()
    print(f'DEBUG: created class instance {type(user)}')

    database = Database(program_database_filename)

    print(f'DEBUG: created class instance {type(database)}')

    while True:
        start = input('1. Login.\n2. Create new account.\n\n')

        if start in ['1', '1.', 'Login', 'login']:
            pass

        elif start in ['2', '2.', 'New', 'new']:
            user.new_user(input('Please enter your username:\n'))
            print(f' Created User {user.username}')
            database.db_insert(user.username, user.id, user.password, user.protect, user.age, user.height,
                               user.weight, user.gender)

            print(f' User {user.username} updated in database.')

            break
        else:
            print('Invalid option. Please try again.\n')






    print('\nTESTING AND DEBUGGING - TO DELETE BEFORE RELEASE\n'
          f'username - {user.username}\n'
          f'password - {user.password}\n'
          f'protection - {user.protect}\n'
          f'ID - {user.id}\n'
          f'age - {user.age}\n'
          f'height - {user.height}\n'
          f'gender - {user.gender}\n')

    database.debuger()

# PROGRAM INITIALIZATION


start_menu()
