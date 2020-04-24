import sqlite3

_DB_NAME = 'banka.sql'


class Database:
    def __init__(self, ):
        self.conn = None

    def is_connected(self):
        return self.conn is not None

    def _assert_connection(self):
        assert self.is_connected(), 'no connection to database is established'

    def connect(self):
        if self.is_connected():
            return
        self.conn = sqlite3.connect(_DB_NAME)

    def close(self):
        if not self.is_connected():
            return
        self.conn.close()
        self.conn = None

    def _initialize_bank_db(self):
        self._assert_connection()
        c = self.conn.cursor()
        c.execute('CREATE TABLE user ('
                  'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                  'username TEXT UNIQUE NOT NULL,'
                  'password TEXT NOT NULL,'
                  'balance REAL DEFAULT 0);')
        c.execute('CREATE TABLE bank_transaction ('
                  'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                  'from_user INTEGER REFERENCES user(id),'
                  'to_user INTEGER REFERENCES user(id),'
                  'delta REAL DEFAULT 0);')
        self.conn.commit()
        c.close()

    def _destroy_bank_db(self):
        self._assert_connection()
        c = self.conn.cursor()
        c.execute('DROP TABLE IF EXISTS bank_transaction;')
        c.execute('DROP TABLE IF EXISTS user;')
        self.conn.commit()
        c.close()


if __name__ == '__main__':
    db = Database()
    db.connect()
    db._destroy_bank_db()
    db._initialize_bank_db()
    db.close()
