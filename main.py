#! python3
# Body tracker - is program that helps you track your body measurements.
# It uses SQL database requirements

import time
from users import User
from database import Database

program_database_filename = 'body_tracker_db.s3db'



class Menu:

    def __init__(self, db_filename):
        self.user = User()
        self.database = Database(program_database_filename)
        self.start_menu()
        self.header()

    def start_menu(self):
        print(f'DEBUG: created class instance {type(self.user)}')
        print(f'DEBUG: created class instance {type(self.database)}')

        while True:
            start = input('1. Login.\n2. Create new account.\n\n')

            if start in ['1', '1.', 'Login', 'login']:
                name = input('Enter Username: \n')
                password = input('Enter Password: \n')
                if self.database.db_login(name, password):
                    self.login_menu(name)


            elif start in ['2', '2.', 'New', 'new']:
                self.user.new_user(input('Please enter your username:\n'))
                print(f' Created User {self.user.username}')
                self.database.db_insert(self.user.username, self.user.id, self.user.password, self.user.protect,
                                        self.user.age, self.user.height, self.user.weight, self.user.gender)

                print(f' User {self.user.username} updated in database.')
                self.start_menu()

            #debugger to delete
            elif start == '0':
                break


            else:
                print('Invalid option. Please try again.\n')

        self.debugger_user()

        self.database.debuger()

    def login_menu(self, name):
        self.user.user_from_import(*self.database.import_user(name))

        print('User is here\n')
        self.debugger_user()




    @staticmethod
    def header():
        print('_' * 79)
        print('FIT_BETA - YOUR PERSONAL FIT DIARY by Bartosz Kowalik'.center(79, ' '))
        print('_' * 79)
        print(time.ctime().rjust(79, ' '))
        print('_' * 79)
        print()

    def debugger_user(self):
        print('\nTESTING AND DEBUGGING - TO DELETE BEFORE RELEASE\n'
              f'username - {self.user.username}\n'
              f'password - {self.user.password}\n'
              f'protection - {self.user.protect}\n'
              f'ID - {self.user.id}\n'
              f'age - {self.user.age}\n'
              f'height - {self.user.height}\n'
              f'gender - {self.user.gender}\n')


# PROGRAM INITIALIZATION


Start = Menu(program_database_filename)

