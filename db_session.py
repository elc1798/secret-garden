import db_utils as dbu
import AESCipher

class Session:
    def __init__(self, master):
        self.master = master
        self.enkryptor = AESCipher.AESCipher(self.master)

    def remove_from_table(self, key):
        query = "DELETE FROM %s WHERE key=?;" % (dbu.PROJECT_TABLE_NAME)
        dbu.execute(query, (key,))

    def insert_into_table(self, key, password):
        query = "INSERT OR REPLACE INTO %s (key, hash) VALUES (? , ?);"
        query = query % (dbu.PROJECT_TABLE_NAME,)
        dbu.execute(query, (key, self.enkryptor.encrypt(password)))

    def get_password_by_key(self, key):
        query = "SELECT * FROM %s WHERE key=?;" % (dbu.PROJECT_TABLE_NAME,)
        rows = dbu.execute(query, (key,))
        assert(len(rows) <= 1)
        return rows[0] if len(rows) == 1 else None

