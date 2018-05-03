"""A mock database. Exposes the same API as the main db module"""
import pymysql

DB = {}


def clear_db(func):
    """
    A decorator to clear out the in-memory database prior to a test.
    """
    def test_wrapper(*args):
        global DB
        DB = {}
        return func(*args)
    return test_wrapper


def get_user(email):
    global DB
    if email in DB:
        return (email, DB[email]['password'], DB[email]['confirmed'])
    else:
        raise ValueError()


def create_user(email, password):
    global DB
    if email not in DB:
        DB[email] = {'password': password, 'confirmed': False}
    else:
        raise pymysql.err.IntegrityError()


def confirm_user(email):
    global DB
    DB[email]['confirmed'] = True
