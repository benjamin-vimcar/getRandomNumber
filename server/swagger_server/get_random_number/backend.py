from swagger_server.get_random_number import db
import jwt
import logging

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
    def __init__(self, email, config):
        self.email = email
        self.config = config

    @staticmethod
    def get(email):
        """
        Get a user by e-mail

        Returns a `User`

        Raises `NoSuchUser` if no such user exists.
        """
        try:
            user_data = db.DB[email]
        except KeyError as e:
            raise NoSuchUser("No such user") from e
        else:
            return User(email, user_data)

    @staticmethod
    def create(email, password):
        """
        Create a new user. Add the user to the database, and then send
        out a confirmation e-mail.

        Raises `UserAlreadyExists` if the user has already been created.
        """
        if email not in db.DB:
            confirm_token = jwt.encode({'user': email},
                                       SUPER_SECRET_CONFIRMATION_KEY,
                                       algorithm='HS256')

            print("Please tell {} the following message: '{}'".format(
                email,
                confirm_token))

            db.DB[email] = {
                'password': password,
                'confirmed': False,
                'confirm_token': confirm_token,
            }
        else:
            raise UserAlreadyExists("User already exists")

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
        if password != self.config['password']:
            raise IncorrectPassword("Incorrect password")
        else:
            return jwt.encode({'user': self.email},
                              SUPER_SECRET_SECRET_KEY,
                              algorithm='HS256')

    @staticmethod
    def confirm(confirm_token):
        """
        Confirm this user's email address

        Raises `IncorrectConfirmationToken` if the user is already confirmed,
        or the token is invalid.
        """
        logger.info("confirm_token: {}".format(confirm_token))
        try:
            payload = jwt.decode(
                confirm_token,
                SUPER_SECRET_CONFIRMATION_KEY,
                algorithm='HS256')
        except jwt.exceptions.InvalidTokenError as e:
            raise IncorrectConfirmationToken("Token decoding failed") from e

        # Having validated the token, we can assume that it is in the expected
        # format.
        user_email = payload['user']

        try:
            user = User.get(user_email)
        except NoSuchUser as e:
            raise IncorrectConfirmationToken(
                "Confirmation token for non-existent user") from e

        if user.config['confirmed']:
            raise IncorrectConfirmationToken("Already confirmed")
        else:
            user.config['confirmed'] = True


def get_random_number():
    """
    Chosen by fair dice roll. Guaranteed to be random.
    """
    return 4
