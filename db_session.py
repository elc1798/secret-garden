# -*- coding: utf-8 -*-

import db_utils as dbu
import AESCipher

class Session:
    def __init__(self, master):
        self.master = master
        self.enkryptor = AESCipher.AESCipher(self.master)

    def remove_from_table(self, key, username=""):
        if username == "":
            query = "DELETE FROM %s WHERE key=?;" % (dbu.PROJECT_TABLE_NAME)
            dbu.execute(query, (key,))
        else:
            query = "DELETE FROM %s WHERE key=? AND username=?;" % (dbu.PROJECT_TABLE_NAME)
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
        rows = dbu.execute(query,)
        return [ ( row[0], row[1], self.enkryptor.decrypt(row[2]) ) for row in rows ]

