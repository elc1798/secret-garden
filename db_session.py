# -*- coding: utf-8 -*-

import db_utils as dbu
import AESCipher

class Session:
    def __init__(self, master, run_as_flask=False):
        self.master = master
        self.enkryptor = AESCipher.AESCipher(self.master)
        if not run_as_flask:
            assert(self.verify_password())

    def remove_from_table(self, key, username=""):
        if username == "":
            query = "DELETE FROM %s WHERE key='?';" % (dbu.PROJECT_TABLE_NAME)
            dbu.execute(query, (key,))
        else:
            query = "DELETE FROM %s WHERE key='?' AND username='?';" % (dbu.PROJECT_TABLE_NAME)
            dbu.execute(query, (key, username))

    def insert_into_table(self, key, username, password):
        existing = self.get_password_by_key(key, username)
        if len(existing) > 0:
            return
        query = "INSERT INTO %s (key, username, hash) VALUES (? , ? , ?);"
        query = query % (dbu.PROJECT_TABLE_NAME,)
        dbu.execute(query, (key, username, self.enkryptor.encrypt(password)))

    def get_password_by_key(self, key, username=""):
        rows = []
        if username == "":
            query = "SELECT key, username, hash FROM %s WHERE key=?;" % (dbu.PROJECT_TABLE_NAME,)
            rows = dbu.execute(query, (key,))
        else:
            query = "SELECT key, username, hash FROM %s WHERE key=? AND username=?;" % (dbu.PROJECT_TABLE_NAME,)
            rows = dbu.execute(query, (key, username))
        return [ ( row[0], row[1], self.enkryptor.decrypt(row[2]) ) for row in rows ]

    def get_keys(self):
        query = "SELECT DISTINCT key FROM %s;" % (dbu.PROJECT_TABLE_NAME,)
        rows = dbu.execute(query)
        return rows

    def get_all(self):
        query = "SELECT key, username, hash FROM %s;" % (dbu.PROJECT_TABLE_NAME,)
        rows = dbu.execute(query)
        return [ ( row[0], row[1], self.enkryptor.decrypt(row[2]) ) for row in rows ]

    def get_config_value(self, value):
        query = "SELECT value FROM %s WHERE key='%s';"
        query = query % (dbu.CONFIG_TABLE_NAME, dbu.CONFIG_KEYS[value])
        # print "EXECUTING QUERY:", repr(query)
        rows = dbu.execute(query)
        # print rows
        return rows[0][0] if rows else None

    def verify_password(self):
        # print self.get_config_value("auth-key")
        if len(self.get_keys()) == 0 or not self.get_config_value("auth-key"):
            query = "INSERT INTO %s (key, value) VALUES (? , ?);"
            query = query % (dbu.CONFIG_TABLE_NAME,)
            dbu.execute(query, (dbu.CONFIG_KEYS["auth-key"], self.enkryptor.encrypt(self.master)))
            return True
        else:
            return self.enkryptor.decrypt(self.get_config_value("auth-key")) == self.master

    def __del__(self):
        del self.master
        del self.enkryptor

