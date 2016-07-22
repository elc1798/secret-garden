import sqlite3
import os
import argparse

this_path = os.path.realpath(__file__)
this_dir = os.path.dirname(this_path)

PROJECT_DB_NAME = this_dir + "/passwords.db"
PROJECT_TABLE_NAME = "passwords"

class Connection:
    """
    Class to simplify executing SQL queries
    """

    def __init__(self, db_name):
        """
        Sets up the SQLite3 connection and cursor variable
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute(self, *args):
        """
        Executes an SQLite3 command and returns the return value, if any
        """
        self.cursor.execute(*args)
        self.conn.commit()
        return self.cursor.fetchall()

    def __del__(self):
        """
        Destroys the internal variables of this class
        """
        self.conn.close()
        del self.cursor
        del self.conn

def execute(*args):
    """
    Executes a single SQL command
    """
    retval = None
    try:
        retval = Connection(PROJECT_DB_NAME).execute(*args)
    except:
        retval = None
    return retval

def is_table_set_up():
    """
    Returns True if the table exists in the database, False otherwise
    """
    return len(execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
        (PROJECT_TABLE_NAME,)
    )) == 1

def create_project_table():
    """
    Returns True if table was successfully created, False otherwise
    """
    try:
        if not is_table_set_up():
            execute(
                "CREATE TABLE %s (key TEXT, username TEXT, hash TEXT);" % (PROJECT_TABLE_NAME,)
            )
        return True
    except:
        raise
        return False


def delete_project_table():
    """
    Returns True if table was successfully deleted, False otherwise
    """
    try:
        if is_table_set_up():
            execute(
                "DROP TABLE %s" % (PROJECT_TABLE_NAME,)
            )
        return True
    except:
        raise
        return False

def reset_project_table():
    delete_project_table()
    create_project_table()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--create",
        help="Creates the table",
        action="store_true"
    )

    parser.add_argument(
        "-d",
        "--delete",
        help="Deletes the table",
        action="store_true"
    )

    parser.add_argument(
        "-r",
        "--reset",
        help="Resets the table",
        action="store_true"
    )

    parser.add_argument(
        "-t",
        "--test",
        help="Prints True if the table is set up, False otherwise",
        action="store_true"
    )

    args = parser.parse_args()

    if args.create:
        if create_project_table():
            print "Table now exists"
        else:
            print "Failed to create table"
    elif args.delete:
        if delete_project_table():
            print "Table deleted"
        else:
            print "Failed to delete table"
    elif args.reset:
        reset_project_table()

    if args.test:
        print(is_table_set_up())

if __name__ == "__main__":
    main()

