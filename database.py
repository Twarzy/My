import sqlite3
import datetime


# Database class with SQLite managing methods
class Database:

    def __init__(self, db_filename):
        self.conn = sqlite3.connect(db_filename)
        self.cur = self.conn.cursor()

        self.create_tables()

    def create_tables(self):
        # Create our main database table collecting all body measurements.
        self.cur.execute("""CREATE TABLE IF NOT EXISTS bodysize (
                        id      VARCHAR(5),
                        date    FLOAT,
                        weight  INT,
                        chest   INT,
                        arm_l   INT,
                        arm_r   INT,
                        abdomen INT,
                        waist   INT,
                        hips    INT,
                        thigh_l INT,
                        thigh_r INT
                        )""")

        # Create separate table for users. User can choose if he want strong password or just simple
        # 4 digit PIN, there is also option to turn off account protection and login with 'blank' password.
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users ( 
                        login      VARCHAR(20),
                        id         VARCHAR(5), 
                        password   TEXT,
                        protection BOOLEAN,
                        age        INT,
                        height     INT,
                        weight     INT,
                        gender     BOOLEAN
                        )""")
        self.conn.commit()

    def db_insert(self, username, id_, password, protect, age, height, weight, gender):
        # Create new user information in SQL database
        self.cur.execute("""
              INSERT INTO users (login, id, password, protection, age, height, weight, gender)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?)
              """, (username, id_, password, protect, age, height, weight, gender))
        self.conn.commit()

    def import_user(self, name):
        # Returning chosen user information from database needed for User class
        self.cur.execute("SELECT * FROM users WHERE login=?", [name])
        return self.cur.fetchall()[0]

    # Simple login method compere provided password with database one
    def db_login(self, username, password):
        self.cur.execute("SELECT login, password FROM users WHERE login=?", [username])
        login_data = self.cur.fetchall()
        if login_data:
            password_ = login_data[0][1]
            if password == password_ or not password_:
                print('Login success\n')
                return True
            else:
                print('ERROR! Wrong password.\n')
                return False

        else:
            print('ERROR! Such user is not exist.\n')
            return False

    def bodysize_insert(self, id_num, date, weight, chest, arm_l, arm_r, abdomen, waist, hips, thigh, thigh_r):
        self.cur.execute("""
            INSERT INTO bodysize (id, date, weight, chest, arm_l, arm_r, abdomen, waist, hips, thigh_l, thigh_r)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (id_num, date, weight, chest, arm_l, arm_r, abdomen, waist, hips, thigh, thigh_r))
        self.conn.commit()
        print('Saved Successful')

    def delete_user(self, id_num):
        print(id_num)  # TO DELETE
        option = input('Are you sure?\n'
                       'Write your password to permanently delete you account and all data.\n')

        self.cur.execute("SELECT password FROM users WHERE id=?", [id_num])
        password = self.cur.fetchall()[0][0]

        if not password or option == password:

            self.cur.execute("DELETE FROM users WHERE id=?", [id_num])
            self.conn.commit()
            print('Account deleted.\n')
            return True
        else:
            print('Cancelled.\n')
            return False

    def user_measurments(self, id_num):
        # Output user measurement data. User can pick to see all data at once
        # TODO or select just specific date

        self.cur.execute("""SELECT date, weight, chest, arm_l, arm_r, abdomen, waist, hips, thigh_l, thigh_r
                          FROM bodysize WHERE id=?""", [id_num])
        user_data = self.cur.fetchall()

        header_row = ['Date', 'Weight', 'Chest', 'Left Arm', 'Right Arm', 'Abdomen', 'Waist',
                'Hips', 'Left Thigh', 'Right thigh']

        print(f'You have {len(user_data)} records in database')
        option = input('Pick one day or write "0" for all:\n')
        if option == '0':
            #  Creating text table of all user data
            new = []  # Variable needed to concatenete header_row and all measurement days
            new.append(header_row)
            for i in user_data:
                new.append(i)
            width = len(new) * 12  # Width for frame depending on table size, not working perfectly
            print('-' * width, end='')  # top frame
            for n in range(len(new[0])):
                if n != 1:
                    print()
                for s in range(len(new)):
                    if len(str(new[s][n])) > 15:  # Pick timestamp to convert it format
                        print('{:6s} |'.format(self.timedate_converter_table(new[s][n])), end=' ')
                    else:
                        if s != 0:  # data cell
                            if n == 1:  # second row is "weight"
                                print('{:9s}|'.format(str(new[s][n]) + ' kg'), end=' ')
                            else:  # in other cases we need to add "cm"
                                print('{:9s}|'.format(str(new[s][n]) + ' cm'), end=' ')
                        else:  # header row/column
                            print('| {:12s}|'.format(str(new[s][n])), end=' ')
                if n == 0:  # Create frame below date row
                    print()
                    print('*' * width)
            print('\n', '-' * width)  # bottom frame
            input('Press *ENTER* to continue.')

    def user_progress(self, id_num):
        self.cur.execute("""SELECT date, weight, chest, arm_l, arm_r, abdomen, waist, hips, thigh_l, thigh_r
                                  FROM bodysize WHERE id=?""", [id_num])
        user_data = self.cur.fetchall()
        self.cur.execute("SELECT weight FROM users WHERE id=?",  [id_num])
        start_weight = self.cur.fetchone()[0]

        header_row = ['Date', 'Weight', 'Chest', 'Left Arm', 'Right Arm', 'Abdomen', 'Waist',
                      'Hips', 'Left Thigh', 'Right thigh']

        #  Creating text table of all user data
        new = []  # Variable needed to concatenete header_row and all measurement days
        new.extend([header_row, list(user_data[0]), user_data[-1]])
        new[1][1] = start_weight  # Change weight from first measurement to weight from account creation

        progress_kg = []
        progress_perc = []
        for n in range(len(new[0])):
            progress_kg.append(new[2][n] - new[1][n])


        for n in range(len(new[0])):
            progress_perc.append(round(progress_kg[n] / new[1][n] * 100, 2))
        progress_perc[0] = '%'
        progress_kg[0] = 'KG'

        new.extend([progress_kg, progress_perc])

        width = len(new) * 12  # Width for frame depending on table size, not working perfectly
        print('-' * width, end='')  # top frame
        for n in range(len(new[0])):
            if n != 1:
                print()
            for s in range(len(new)):
                if n == 0:
                    if len(str(new[s][n])) > 15:  # Pick timestamp to convert it format
                        print('{:9s} |'.format(self.timedate_converter_table(new[s][n])), end=' ')
                    else: print('| {:9}|'.format(str(new[s][n])), end=' ')

                else:
                    if s != 0:  # data cell

                        if n == 1:  # second row is "weight"
                            print('{:9s}|'.format(str(new[s][n]) + ' kg'), end=' ')
                        else:  # in other cases we need to add "cm"
                            print('{:9s}|'.format(str(new[s][n]) + ' cm'), end=' ')
                    else:  # header row/column
                        print('| {:12s}|'.format(str(new[s][n])), end=' ')
            if n == 0:  # Create frame below date row
                print()
                print('*' * width)
        print('\n', '-' * width)  # bottom frame
        input('Press *ENTER* to continue.')



    def timedate_converter(self, timestamp):
        #  Convert timestamp to "DD.MM.YY (day of the week)" format
        return (datetime.datetime.fromtimestamp(timestamp).strftime('%d.%m.%y (%A)'))

    def timedate_converter_table(self, timestamp):
    #  Convert timestamp to "DD.MM.YY" format
        return (datetime.datetime.fromtimestamp(timestamp).strftime('%d.%m.%y'))

    # TODO: DOUBLE CHECK IF IT CANT BE DONE BETTER not static method

    # Uses only to checking all ID's in database in User.id_maker() method
    @staticmethod
    def id_db_check():
        conn = sqlite3.connect('body_tracker_db.s3db')
        cur = conn.cursor()
        cur.execute('SELECT id FROM users')
        return [x[0] for x in cur.fetchall()]

    # Prevent new user to pick same username as existing
    @staticmethod
    def user_exist(name):
        conn = sqlite3.connect('body_tracker_db.s3db')
        cur = conn.cursor()
        cur.execute("""SELECT login FROM users""")
        all_login = [x[0] for x in cur.fetchall()]
        return True if name not in all_login else False

    # For later use
    def connect(self):
        connect = sqlite3.connect('body_tracker_db.s3db')
        cursor = connect.cursor()

    # DEV TESTING - DELETE THIS
    def debuger(self):

        print('DATABASE DEBUGER - TO DELETE')
        self.cur.execute('SELECT * from users')
        for i in self.cur.fetchall():
            print(i)

    def debugger_bodysize(self, id_num):

        print('DATABASE DEBUGER - TO DELETE')
        self.cur.execute('SELECT * from bodysize')
        for i in self.cur.fetchall():
            print(i)


