#! python3
# Body-size Tracker - program that helps you track your body measurements and check progress. The main feature is
# storing provided body measurement in local SQLite database. All historical records will be available for user to
# analyze his progress. Password protected login for multiply user implemented.

import time
from users import User
from database import Database

# Database file will be created in current working directory.
program_database_filename = 'body_tracker_db.s3db'

# Class with program main loops.
class Menu:

    def __init__(self, db_filename):
        # Instance of User class storing information about user: like login, password
        self.user = User()
        # Instance of Database class with SQLite managing methods
        self.database = Database(program_database_filename)
        self.start_menu()
        self.header()

    # Main menu with two options: "login" or "create new user"
    def start_menu(self):
        print(f'DEBUG: created class instance {type(self.user)}') # DEV TESTING - DELETE THIS
        print(f'DEBUG: created class instance {type(self.database)}') # DEV TESTING - DELETE THIS

        while True:
            start = input('1. Login.\n2. Create new account.\n\n')

            if start in ['1', '1.', 'Login', 'login']:
                name = input('Enter Username: \n')
                password = input('Enter Password: \n')
                if self.database.db_login(name, password):
                    self.login_menu(name)


            elif start in ['2', '2.', 'New', 'new']:
                # Creating new user
                self.user.new_user(input('Please enter your username:\n'))
                print(f' Created User {self.user.username}')

                # Insert new user data in database
                self.database.db_insert(self.user.username, self.user.id, self.user.password, self.user.protect,
                                        self.user.age, self.user.height, self.user.weight, self.user.gender)

                print(f' User {self.user.username} updated in database.')
                self.start_menu()  # Return to main menu

            # DEV TESTING - DELETE THIS (Have to break main loop to get to testing and debugging data)
            elif start == '0':
                break

            # After inputting invalid options return to main menu (still in loop)
            else:
                print('Invalid option. Please try again.\n')

        self.debugger_user()  # DEV TESTING - DELETE THIS

        self.database.debuger()  # DEV TESTING - DELETE THIS

    # Main Loop with menu option for logged user
    def login_menu(self, name):
        # After successful login update User instance with data stored in database
        self.user.user_from_import(*self.database.import_user(name))

        print('User is here\n')
        self.debugger_user()



    # Simple header at after start of the program
    @staticmethod
    def header():
        print('_' * 79)
        print('FIT_BETA - YOUR PERSONAL FIT DIARY by Bartosz Kowalik'.center(79, ' '))
        print('_' * 79)
        print(time.ctime().rjust(79, ' '))
        print('_' * 79)
        print()

    # DEV TESTING - DELETE THIS
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

