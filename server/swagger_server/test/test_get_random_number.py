"""
Unit tests for the backend
"""
import unittest
from unittest.mock import patch
import jwt
from swagger_server.get_random_number.backend import (
    SUPER_SECRET_SECRET_KEY,
    SUPER_SECRET_CONFIRMATION_KEY,
    User,
    NoSuchUser,
    UserAlreadyExists,
    IncorrectConfirmationToken,
    IncorrectPassword)

from swagger_server.test import mock_db
from swagger_server.test.mock_db import (
    get_user, create_user, confirm_user, clear_db)


def generate_token(key, email):
    """
    Helper function to generate a JWT.
    """
    return jwt.encode({'user': email}, key, algorithm='HS256')


@patch('swagger_server.get_random_number.backend.db.create_user',
       side_effect=create_user)
class TestCreateUser(unittest.TestCase):

    @clear_db
    def test_success(self, *_):
        User.create("email@test.com", "test_password")

    @clear_db
    def test_duplicate_user(self, *_):
        User.create("duplicate@test.com", "test_password")
        with self.assertRaises(UserAlreadyExists):
            User.create("duplicate@test.com", "test_password")


@patch('swagger_server.get_random_number.backend.db.create_user',
       side_effect=create_user)
@patch('swagger_server.get_random_number.backend.db.get_user',
       side_effect=get_user)
@patch('swagger_server.get_random_number.backend.db.confirm_user',
       side_effect=confirm_user)
class TestConfirmUser(unittest.TestCase):

    @clear_db
    def test_success(self, *_):
        User.create("email@test.com", "test_password")
        User.get("email@test.com").confirm(generate_token(
            SUPER_SECRET_CONFIRMATION_KEY,
            "email@test.com"))
        self.assertEqual(mock_db.DB["email@test.com"]['confirmed'], True)

    @clear_db
    def test_no_user(self, *_):
        with self.assertRaises(NoSuchUser):
            User.get("none@test.com").confirm("bad_token")

    @clear_db
    def test_invalid_token(self, *_):
        User.create("email@test.com", "test_password")
        with self.assertRaises(IncorrectConfirmationToken):
            User.get("email@test.com").confirm("bad_token")


@patch('swagger_server.get_random_number.backend.db.create_user',
       side_effect=create_user)
@patch('swagger_server.get_random_number.backend.db.get_user',
       side_effect=get_user)
@patch('swagger_server.get_random_number.backend.db.confirm_user',
       side_effect=confirm_user)
class TestLogin(unittest.TestCase):

    @clear_db
    def test_success(self, *_):
        User.create("email@test.com", "test_password")
        User.get("email@test.com").confirm(generate_token(
            SUPER_SECRET_CONFIRMATION_KEY,
            "email@test.com"))
        self.assertEqual(
            User.get("email@test.com").login("test_password"),
            jwt.encode({"user": "email@test.com"},
                       SUPER_SECRET_SECRET_KEY,
                       algorithm='HS256').decode()
        )

    @clear_db
    def test_no_user(self, *_):
        with self.assertRaises(NoSuchUser):
            User.get("none@test.com").login("bad_password")

    @clear_db
    def test_wrong_password(self, *_):
        User.create("email@test.com", "test_password")
        User.get("email@test.com").confirm(generate_token(
            SUPER_SECRET_CONFIRMATION_KEY,
            "email@test.com"))
        with self.assertRaises(IncorrectPassword):
            User.get("email@test.com").login("bad_password")

    @clear_db
    def test_unconfirmed(self, *_):
        User.create("email@test.com", "test_password")
        with self.assertRaises(IncorrectPassword):
            User.get("email@test.com").login("bad_password")
