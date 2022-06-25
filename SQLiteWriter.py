import sqlite3
from sqlite3 import Error


class SQLLiteWriter:

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def disconnect(self):
        if self.conn:
            self.conn.clpse()
