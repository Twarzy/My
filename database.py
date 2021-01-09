import sqlite3

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
                        date    INT,
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

    def import_user(self,name):
        # Returning chosen user information from database needed for User class
        self.cur.execute("SELECT * FROM users WHERE login=?", [name])
        return self.cur.fetchall()[0]

    # TODO: DOUBLE CHECK IF IT CANT BE DONE BETTER not static method

    # Simple login method compere provided password with database one
    def db_login(self, username, password):
        self.cur.execute("SELECT login, password FROM users WHERE login=?", [username])
        login_data = self.cur.fetchall()
        if login_data:
            password_ = login_data[0][1]
            if password != password_:
                print('ERROR! Wrong password.\n')
                return False
            else:
                print('Login success\n')
                return True


        else:
            print('ERROR! Such user is not exist.\n')
            return False

    # Uses only to checking all ID's in database in User.id_maker() method
    @staticmethod
    def id_db_check():
        connect = sqlite3.connect('body_tracker_db.s3db')
        cursor = connect.cursor()
        cursor.execute('SELECT id FROM users')
        return [x[0] for x in cursor.fetchall()]

    # For later use
    def connect(self):
        connect = sqlite3.connect('body_tracker_db.s3db')
        cursor = connect.cursor()

    # DEV TESTING - DELETE THIS
    def debuger(self):

        print('DATABASE DEBUGER - TO DELETE')
        self.cur.execute('SELECT * from users')
        print(self.cur.fetchall())
