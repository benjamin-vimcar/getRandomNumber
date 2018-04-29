import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util


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
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_random_number(secret_session_token):  # noqa: E501
    """get_random_number

    Get a single random digit from 1-6 # noqa: E501

    :param secret_session_token: @@@ placeholder for whatever mechanism we use for authentication later
    :type secret_session_token: str

    :rtype: int
    """
    return 'do some magic!'


def login_user(user):  # noqa: E501
    """login_user

    A user logs in. # noqa: E501

    :param user: User to log in as
    :type user: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
