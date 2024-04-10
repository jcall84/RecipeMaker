import sqlite3

class DB:

    conn = None
    cursor = None

    def __init__(self, db_name):
        """Initialize the DB object with the name of the database."""
        self.db_name = db_name
        self.connect()

    def connect(self):
        """Connect to the database."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def execute_script(self, sql_string, params=()):
        """Execute a SQL script with params as input."""
        self.cursor.execute(sql_string, params)

    def reset_database(self):
        """Reset the database by dropping all tables. Must be run from the child class."""
        raise NotImplementedError("Must implement from the derived class")

    def close_db(self):
        """Close the database connection."""
        self.conn.close()

    @property
    def get_cursor(self):
        """Return the cursor object."""
        return self.cursor

    @property
    def get_connection(self):
        """Return the connection object."""
        return self.conn