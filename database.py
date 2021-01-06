import sqlite3


class Database:

    def __init__(self, db_filename):
        self.conn = sqlite3.connect(db_filename)
        self.cur = self.conn.cursor()

        self.create_tables()

    def initiate(self):
        self.create_tables()

    def create_tables(self):
        # Create our main database table collecting all body measurements.
        self.cur.execute("""CREATE TABLE IF NOT EXISTS bodysize (
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
                        id         VARCHAR(1), 
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

    # TODO: DOUBLE CHECK IF IT CANT BE DONE BETTER
    @staticmethod
    def id_db_check():
        connect = sqlite3.connect('body_tracker_db.s3db')
        cursor = connect.cursor()
        cursor.execute('SELECT id FROM users')
        return [x[0] for x in cursor.fetchall()]

    def debuger(self):

        print('DATABASE DEBUGER - TO DELETE')
        self.cur.execute('SELECT * from users')
        print(self.cur.fetchall())
