import logging
import sqlite3

import conf


logger = logging.getLogger('nnlb')


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
        self.conn = sqlite3.connect(conf.DB_NAME)
        self.conn.row_factory = sqlite3.Row
        self.conn.isolation_level = None  # enables manual transactions

    def close(self):
        if not self.is_connected():
            return
        self.conn.close()
        self.conn = None

    def _execute_select(self, query, **kwargs):
        self._assert_connection()
        c = self.conn.cursor()
        try:
            c.execute(query, kwargs)
            result = c.fetchall()
        except sqlite3.Error:
            logger.exception('Failed to execute select')
            result = None
        c.close()
        return result

    def add_user(self, **kwargs):
        self._assert_connection()
        c = self.conn.cursor()
        try:
            c.execute('INSERT INTO user(username, password, balance) VALUES (:username, :password, :balance);', kwargs)
            self.conn.commit()
            user_id = c.lastrowid
        except sqlite3.Error:
            user_id = None
        c.close()
        return user_id

    def authenticate_user(self, **kwargs):
        select_query = 'SELECT id FROM user WHERE username=:username AND password=:password;'
        result = self._execute_select(select_query, **kwargs)
        return result[0] if len(result) > 0 else None

    def fetch_user_by_id(self, id):
        select_query = 'SELECT * FROM user WHERE id=:id;'
        result = self._execute_select(select_query, id=id)
        return result[0] if len(result) > 0 else None

    def fetch_all_users(self):
        select_query = 'SELECT id, username FROM user ORDER BY username ASC;'
        return self._execute_select(select_query)

    def make_transaction(self, from_user, to_user, value):
        success = False
        c = self.conn.cursor()
        try:
            value = float(value)
            c.execute('BEGIN')
            c.execute('SELECT balance - ? FROM user WHERE id=?;', (value, from_user))
            if c.fetchone()[0] < 0:
                raise ValueError('User (id {}) does not have enough balance'.format(from_user))
            c.execute('UPDATE user SET balance = balance - ? WHERE id=?;', (value, from_user))
            logger.warning('User (id {}) balance change: {}'.format(from_user, -value))
            c.execute('UPDATE user SET balance = balance + ? WHERE id=?;', (value, to_user))
            logger.warning('User (id {}) balance change: {}'.format(to_user, value))
            c.execute('INSERT INTO bank_transaction(from_user, to_user, delta) VALUES (?, ?, ?);',
                      (from_user, to_user, value))
            c.execute('COMMIT')
            success = True
        except (sqlite3.Error, ValueError):
            logger.exception('Failed to make bank transaction')
            c.execute('ROLLBACK')
        c.close()
        return success

    def fetch_user_transactions(self, user_id):
        select_query = 'SELECT u1.username AS from_username, u2.username AS to_username, delta FROM bank_transaction ' \
                       'LEFT JOIN user u1 ON from_user = u1.id  LEFT JOIN user u2 ON to_user = u2.id ' \
                       'WHERE from_user = :user_id OR to_user = :user_id;'
        return self._execute_select(select_query, user_id=user_id)

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
