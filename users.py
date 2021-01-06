import random
from database import Database


class User:

    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.protect = None
        self.age = None
        self.height = None
        self.weight = None
        self.gender = None

    def new_user(self, name):
        self.username = name
        print(f'User "{self.username}" created.\n')
        self.id = self.id_maker()
        print(f'Yor unique ID is "{self.id}".\n')
        self.secure(input('Please create your password.\nIt should has at least one uppercase,'
                          'one lowercase and at least 6 character long.\n'
                          'If you don\'t want password, just leave it blank at click ENTER:\n'))
        option = input('\nDo you want to add more information about you?\n'
                       '1. Yes\n'
                       '2. No\n')
        if option in ['1', '1.', 'Yes', 'yes']:
            self.more_info()

        elif option in ['2', '2.', 'No', 'no']:
            pass

    @staticmethod
    def id_maker():

        all_id = Database.id_db_check()
        new_id = ''.join([str(x) for x in random.sample(range(9), 5)])

        # The process will be repeated over over if id will same as any existing
        while new_id in all_id:
            new_id = ''.join([str(x) for x in random.sample(range(9), 5)])
        return new_id

    def more_info(self):
        while True:
            print(f'\n{self.username} INFO:'
                  '\nage', '-' if not self.age else self.age,
                  '\nheight', '-' if not self.height else self.height,
                  '\nweight', '-' if not self.weight else self.weight,
                  '\ngender:', 'Male' if self.gender else '-' if not self.gender else 'Woman')

            option = input('\nWhat do you want to add or change?:\n'
                           '1. Age\n'
                           '2. Height\n'
                           '3. Weight\n'
                           '4. Gender\n'
                           '0. All OK, go back\n')

            if option == '1':
                self.age = input('Age: ')
            elif option == '2':
                self.height = input('Height: ')
            elif option == '3':
                self.weight = input('Weight: ')
            elif option == '4':
                self.gender = True if input('Male or Female? ').lower() in ['male', 'man'] else False
            elif option == '0':
                break
            else:
                print('Invalid option')

    def add_to_db(self):
        pass

    def add_from_db(self):
        pass

    def secure(self, pin_pass):
        if not pin_pass:
            self.protect = False
        else:
            while not self.protect:

                if self.password_validator(pin_pass):
                    self.password = pin_pass
                    self.protect = True
                else:
                    pin_pass = input()

    @staticmethod
    def password_validator(pinpass):
        if len(pinpass) < 6:
            print('Password too short. It must be at least 6 character long')
            return False
        digit = False
        capital = False
        lowercase = False
        whitespace = False

        for i in pinpass:
            if i.islower():
                lowercase = True
            elif i.isupper():
                capital = True
            elif i.isdecimal():
                digit = True
            elif i.isspace():
                whitespace = True

        if digit and capital and lowercase and not whitespace:
            print('Password created')
            return True
        else:
            print('Password too weak. You must use at least one digit,'
                  ' one capital, one lowercase, and no whitespaces')
            return False
