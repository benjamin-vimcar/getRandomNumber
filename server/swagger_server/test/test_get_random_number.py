"""
test
"""
import unittest
from swagger_server.get_random_number.backend import (User,
                                                      NoSuchUser,
                                                      UserAlreadyExists,
                                                      IncorrectConfirmationToken,
                                                      IncorrectPassword)


class TestCreateUser(unittest.TestCase):

    def test_success(self):
        User.create("email@test.com", "test_password")

    def test_duplicate_user(self):
        with self.assertRaises(UserAlreadyExists):
            User.create("duplicate@test.com", "test_password")


class TestConfirmUser(unittest.TestCase):

    def test_success(self):
        User.get("email@test.com").confirm("secret_token")

    def test_no_user(self):
        with self.assertRaises(NoSuchUser):
            User.get("none@test.com").confirm("bad_token")

    def test_invalid_token(self):
        with self.assertRaises(IncorrectConfirmationToken):
            User.get("email@test.com").confirm("bad_token")


class TestLogin(unittest.TestCase):

    def test_success(self):
        User.get("email@test.com").login("test_password")

    def test_no_user(self):
        with self.assertRaises(NoSuchUser):
            User.get("none@test.com").login("bad_password")

    def test_wrong_password(self):
        with self.assertRaises(IncorrectPassword):
            User.get("email@test.com").login("bad_password")
