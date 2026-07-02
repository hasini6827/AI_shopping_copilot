import mysql.connector
from config import DB_CONFIG

class Database:

    def __init__(self):

        self.connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )

        self.cursor = self.connection.cursor(dictionary=True)

    def fetch_all(self, query, values=None):

        self.cursor.execute(query, values or ())

        return self.cursor.fetchall()

    def fetch_one(self, query, values=None):

        self.cursor.execute(query, values or ())

        return self.cursor.fetchone()

    def execute(self, query, values=None):

        self.cursor.execute(query, values or ())

        self.connection.commit()
    def last_insert_id(self):

        return self.cursor.lastrowid

    def executemany(self, query, values):

        self.cursor.executemany(query, values)

        self.connection.commit()

    def close(self):

        self.cursor.close()

        self.connection.close()


def get_connection():

    return Database()