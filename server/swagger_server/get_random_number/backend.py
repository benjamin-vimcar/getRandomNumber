"""
The core of the `get_random_number` application.

The single resource is simple, so this module contains
both the code for dealing with users and providing the resource.
"""

from swagger_server.get_random_number import db
import jwt
import logging
import pymysql

logger = logging.getLogger(__name__)

SUPER_SECRET_CONFIRMATION_KEY = "SUPER_SECRET_CONFIRMATION_KEY"
SUPER_SECRET_SECRET_KEY = "SUPER_SECRET_SECRET_KEY"


class NoSuchUser(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class IncorrectPassword(Exception):
    pass


class IncorrectConfirmationToken(Exception):
    pass


class AuthenticationFailure(Exception):
    pass


class User(object):
    """
    A user.
    """
    def __init__(self, email, password, confirmed):
        self.email = email
        self.password = password
        self.confirmed = confirmed

    @staticmethod
    def get(email):
        """
        Get a user by e-mail

        Returns a `User`

        Raises `NoSuchUser` if no such user exists.
        """
        try:
            user_data = db.get_user(email)
        except ValueError as e:
            raise NoSuchUser("No such user") from e
        else:
            return User(*user_data)

    @staticmethod
    def create(email, password):
        """
        Create a new user. Add the user to the database, and then send
        out a confirmation e-mail.

        Raises `UserAlreadyExists` if the user has already been created.
        """
        confirm_token = jwt.encode({'user': email},
                                   SUPER_SECRET_CONFIRMATION_KEY,
                                   algorithm='HS256').decode()

        logger.info("Please tell {} the following message: '{}'".format(
            email,
            confirm_token))

        try:
            db.create_user(email, password)
        except pymysql.err.IntegrityError as e:
            raise UserAlreadyExists("User already exists") from e

    @staticmethod
    def authenticate(authentication_header):
        """
        Validate the provided authentication header.

        Raises `AuthenticationFailure` exception on failure.
        """
        # Cope with the fact that OpenAPI v2 doesn't handle the 'Bearer'
        # section for us, so we must strip it manually here.
        auth_token = authentication_header.replace("Bearer ", "")

        try:
            jwt.decode(
                auth_token,
                SUPER_SECRET_SECRET_KEY,
                algorithm='HS256')
        except jwt.exceptions.InvalidTokenError as e:
            raise AuthenticationFailure("Invalid authentication token") from e

    def login(self, password):
        """
        Log this user in.

        Returns the JWT for this user.

        Raises `IncorrectPassword` if the password is incorrect.
        """
        if not self.confirmed:
            raise IncorrectPassword("Not yet confirmed")
        elif password != self.password:
            raise IncorrectPassword("Incorrect password")
        else:
            return jwt.encode({'user': self.email},
                              SUPER_SECRET_SECRET_KEY,
                              algorithm='HS256').decode()

    @staticmethod
    def confirm(confirm_token):
        """
        Confirm this user's email address

        Raises `IncorrectConfirmationToken` if the token is invalid.
        """
        logger.info("confirm_token: {}".format(confirm_token))
        try:
            payload = jwt.decode(
                confirm_token,
                SUPER_SECRET_CONFIRMATION_KEY,
                algorithm='HS256')
        except jwt.exceptions.InvalidTokenError as e:
            raise IncorrectConfirmationToken("Token decoding failed") from e

        db.confirm_user(payload['user'])


def get_random_number():
    """
    Chosen by fair dice roll. Guaranteed to be random.

    Returns an integer between 1 and 6
    """
    return 4
