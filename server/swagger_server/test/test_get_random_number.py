"""
Unit tests for the backend
"""
import unittest
import jwt
from swagger_server.get_random_number import db
from swagger_server.get_random_number.backend import (
    SUPER_SECRET_SECRET_KEY,
    SUPER_SECRET_CONFIRMATION_KEY,
    User,
    NoSuchUser,
    UserAlreadyExists,
    IncorrectConfirmationToken,
    IncorrectPassword)


def generate_token(key, email):
    """
    Helper function to generate a JWT.
    """
    return jwt.encode({'user': email}, key, algorithm='HS256')


def clear_db(func):
    """
    A decorator to clear out the in-memory database prior to a test.
    """
    def test_wrapper(*args, **kwargs):
        db.DB = {}
        return func(*args, **kwargs)
    return test_wrapper


class TestCreateUser(unittest.TestCase):

    @clear_db
    def test_success(self):
        User.create("email@test.com", "test_password")

    @clear_db
    def test_duplicate_user(self):
        User.create("duplicate@test.com", "test_password")
        with self.assertRaises(UserAlreadyExists):
            User.create("duplicate@test.com", "test_password")


class TestConfirmUser(unittest.TestCase):

    @clear_db
    def test_success(self):
        User.create("email@test.com", "test_password")
        User.get("email@test.com").confirm(generate_token(
            SUPER_SECRET_CONFIRMATION_KEY,
            "email@test.com"))
        self.assertEqual(db.DB["email@test.com"]['confirmed'], True)

    @clear_db
    def test_no_user(self):
        with self.assertRaises(NoSuchUser):
            User.get("none@test.com").confirm("bad_token")

    @clear_db
    def test_invalid_token(self):
        User.create("email@test.com", "test_password")
        with self.assertRaises(IncorrectConfirmationToken):
            User.get("email@test.com").confirm("bad_token")


class TestLogin(unittest.TestCase):

    @clear_db
    def test_success(self):
        User.create("email@test.com", "test_password")
        self.assertEqual(
            User.get("email@test.com").login("test_password"),
            jwt.encode({"user": "email@test.com"},
                       SUPER_SECRET_SECRET_KEY,
                       algorithm='HS256')
        )

    @clear_db
    def test_no_user(self):
        with self.assertRaises(NoSuchUser):
            User.get("none@test.com").login("bad_password")

    @clear_db
    def test_wrong_password(self):
        User.create("email@test.com", "test_password")
        with self.assertRaises(IncorrectPassword):
            User.get("email@test.com").login("bad_password")
