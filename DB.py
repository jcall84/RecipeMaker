import sqlite3

class DB:

    conn = None
    cursor = None

    def __init__(self, db_name):
        self.db_name = db_name
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def execute_script(self, sql_string):
        self.cursor.executescript(sql_string)

    def reset_database(self):
        raise NotImplementedError("Must implement from the derived class")

    def close_db(self):
        self.conn.close()

    @property
    def get_cursor(self):
        return self.cursor

    @property
    def get_connection(self):
        return self.conn