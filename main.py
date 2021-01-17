#! python3
# Body-size Tracker - program that helps you track your body measurements and check progress. The main feature is
# storing provided body measurement in local SQLite database. All historical records will be available for user to
# analyze his progress. Password protected login for multiply user implemented.

import time
import sys
from users import User
from database import Database

# Database file will be created in current working directory.
database_filename = 'body_tracker_db.s3db'


# Class with program main loops.
class Menu:

    def __init__(self, db):
        # Instance of Database class with SQLite managing methods
        self.database = Database(db)
        self.header()
        self.start_menu()
        self.user = User()

    # Main menu with two options: "login" or "create new user"
    def start_menu(self):
        # Instance of User class storing information about user: like login, password
        self.user = User()

        while True:
            start = input('1. Login.\n2. Create new account.\n3. Quit\n4. About\n')

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

            elif start in ['3', '3.', 'exit', 'EXIT', 'Exit', 'quit', 'Quit', 'QUIT']:
                print('See you later!')
                sys.exit()

            elif start in ['4', '4.', 'about', 'About', 'ABOUT']:
                pass

            # DEV TESTING - DELETE THIS
            elif start == '0':
                self.debugger_user()  # DEV TESTING - DELETE THIS
                self.database.debuger()  # DEV TESTING - DELETE THIS

            # After inputting invalid options return to main menu (still in loop)
            else:
                print('Invalid option. Please try again.\n')

    # Main Loop with menu option for logged user
    def login_menu(self, name):
        # After successful login update User instance with data stored in database
        self.user.user_from_import(*self.database.import_user(name))
        self.debugger_user()  # DEV TESTING - DELETE THIS

        while True:
            self.login_menu_header()
            option = input(f'What You want to do {self.user.username}?:\n')

            if option in ['1', '1.']:  # new measurement
                self.add_measurement(self.user.id)
            elif option in ['2', '2.']:  # history
                self.database.user_measurments(self.user.id)

            elif option in ['3', '3.']:  # progress
                self.database.user_progress(self.user.id)

            elif option in ['4', '4.']:  # settings

                pass
            elif option in ['5', '5.']:  # logout

                print('Logout complete')
                self.start_menu()
            elif option in ['6', '6.']:  # del account
                if self.database.delete_user(self.user.id):
                    self.start_menu()

            # DEV TESTING - DELETE THIS
            elif option in ['0']:
                self.database.debugger_bodysize([self.user.id])


            else:
                print('Invalid option. Please try again.\n')

        # TODO historical data -> ilosc dni -> pick one
        # porównanie start-now
        # pick range of day

    def add_measurement(self, id_num):

        measurments = {'id': id_num,
                       'date': time.time(),
                       'Weight':  None,
                       'Chest':   None,
                       'Left Biceps':   None,
                       'Right Biceps':   None,
                       'Abdomen': None,
                       'Waist':   None,
                       'Hips':   None,
                       'Left Thigh': None,
                       'Right Thight': None,
                       }
        for body in list(measurments.keys())[2:]:
            measurments[body] = int(input(f'{body}: '))
        print()
        for body, x in measurments.items():
            print(body, '-', x)
        option = input('Save?\n1. Yes\n2. No.\n')
        if option in ['1', '1.', 'Yes', 'yes']:
            self.database.bodysize_insert(*list(measurments.values()))
        else:
            print('Canceled')

    def login_menu_header(self):
        print('-' * 79)
        print(f'Hello {self.user.username}\n')
        print('1. Add new measurement.\n'
              '2. Previous measurements.\n'
              '3. My Progress.\n'
              '4. Settings(TODO:My data, change password, delete account)\n'
              '5. Logout\n'
              '6. DELETE account\n')
        print('-' * 79)

    # Simple header at after start of the program
    @staticmethod
    def header():
        print('_' * 79)
        print('BODY-SIZE TRACKER - YOUR PERSONAL FIT DIARY by Bartosz Kowalik'.center(79, ' '))
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

Start = Menu(database_filename)
