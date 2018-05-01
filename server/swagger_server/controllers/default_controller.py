import connexion
import logging
import jwt

from swagger_server.models.user import User as UserData# noqa: E501
from swagger_server.get_random_number.backend import *

logger = logging.getLogger(__name__)

def activate_user(token):  # noqa: E501
    """activate_user

    Confirm a registered user # noqa: E501

    :param token: @@@ Some sort of confirmation token. Ideally, should be fast to link this back to the user.
    :type token: str

    :rtype: None
    """
    return 'do some magic!'


def create_user(user):  # noqa: E501
    """create_user

    Register a new user # noqa: E501

    :param user: User to register
    :type user: dict | bytes

    :rtype: None
    """
    user = UserData.from_dict(connexion.request.get_json())  # noqa: E501

    try:
        User.create(user.email, user.password)
        logger.info("Successfully created user '{}'".format(user.email))
    except UserAlreadyExists:
        logger.info("User already exists: '{}'".format(user.email))


def get_random_number():  # noqa: E501
    """get_random_number

    Get a single random digit from 1-6 # noqa: E501

    :param secret_session_token: @@@ placeholder for whatever mechanism we use for authentication later
    :type secret_session_token: str

    :rtype: int
    """
    return 4


def login_user(user):  # noqa: E501
    """login_user

    A user logs in. # noqa: E501

    :param user: User to log in as
    :type user: dict | bytes

    :rtype: str
    """
    user = UserData.from_dict(connexion.request.get_json())  # noqa: E501

    try:
        User.get(user.email).login(user.password)
    except (NoSuchUser, IncorrectPassword) as e:
        logger.info("Unable to log '{}' in: {}".format(user.email, e))
        return "Invalid login information", 403
