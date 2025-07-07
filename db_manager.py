import sqlite3

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect("fitness.db")
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, age INTEGER, weight REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, date TEXT, time TEXT, type TEXT, duration REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, date TEXT, time TEXT, food TEXT, calories REAL
            )
        """)
        self.conn.commit()

    def execute(self, query, params=(), fetch=False, fetchone=False):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        result = None
        if fetch:
            result = cursor.fetchall()
        elif fetchone:
            result = cursor.fetchone()
        self.conn.commit()
        return result


