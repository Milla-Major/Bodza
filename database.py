import sqlite3, random
from itertools import groupby

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_connection(self):

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  
        return conn

    def get_numberMagazines(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM magazine")
            return cursor.fetchall()  
    def magazine_exists(self, title):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM magazine WHERE title = ?", (title,))
            return cursor.fetchone() is not None

    def add_numberMagazines(self, title):
        with self.get_connection() as conn:
            type_code = random.randint(1, 4)
            publisher = "test"
            monthly_fee = random.randint(1, 49)
            conn.execute(
                "INSERT INTO magazine (title, type_code, publisher, monthly_fee) VALUES (?, ?, ?, ?)",
                (title, type_code, publisher, monthly_fee)
            )
    def get_user(self, username):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            return dict(row) if row else None