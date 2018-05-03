import connexion
import logging
import werkzeug

from swagger_server.models.user import User as UserData
from swagger_server.get_random_number import backend
from swagger_server.get_random_number.backend import (
    User,
    NoSuchUser,
    AuthenticationFailure,
    UserAlreadyExists,
    IncorrectPassword
)

logger = logging.getLogger(__name__)


class AuthException(connexion.ProblemException, werkzeug.exceptions.Forbidden):
    """
    Exception raised when an endpoint with `requires_authentication`
    fails due to a lack of authentication.
    """
    def __init__(self, title=None, status=403, **kwargs):
        super().__init__(title=title, status=status, **kwargs)


def requires_authentication(func):
    """
    Add this decorator to an API endpoint to ensure that it checks for
    authentication before allowing acccess.
    """
    def endpoint_wrapper(*args, **kwargs):
        try:
            header = connexion.request.headers['Authorization']
            User.authenticate(header)
        except KeyError:
            logger.info("Missing 'Authorization' header")
            raise AuthException("Missing 'Authorization' header")
        except AuthenticationFailure as e:
            logger.info("Unable to authenticate: {}".format(e))
            raise AuthException("Resource requires authentication")
        else:
            return func(*args, **kwargs)

    return endpoint_wrapper


def activate_user(token):  # noqa: E501
    """activate_user

    Confirm a registered user # noqa: E501

    :param token: @@@ Some sort of confirmation token. Ideally, should be fast to link this back to the user.
    :type token: str

    :rtype: None
    """
    User.confirm(token)


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


@requires_authentication
def get_random_number():  # noqa: E501
    """get_random_number

    Get a single random digit from 1-6 # noqa: E501

    :param secret_session_token: A secret JWT token
    :type secret_session_token: str

    :rtype: int
    """
    return backend.get_random_number()


def login_user(user):  # noqa: E501
    """login_user

    A user logs in. # noqa: E501

    :param user: User to log in as
    :type user: dict | bytes

    :rtype: str
    """
    user = UserData.from_dict(connexion.request.get_json())  # noqa: E501

    try:
        return str(User.get(user.email).login(user.password))
    except (NoSuchUser, IncorrectPassword) as e:
        logger.info("Unable to log '{}' in: {}".format(user.email, e))
        return "Invalid login information", 403
