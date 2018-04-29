class NoSuchUser(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class IncorrectPassword(Exception):
    pass


class IncorrectConfirmationToken(Exception):
    pass


class User(object):
    """
    A user with no special privileges.
    """
    @staticmethod
    def get(email):
        """
        Get a user by e-mail
        """
        if email == "none@test.com":
            raise NoSuchUser

        return User()

    @staticmethod
    def create(email, password):
        if email == "duplicate@test.com":
            raise UserAlreadyExists

    def login(self, password):
        """
        Log this user in.
        """
        if password != "test_password":
            raise IncorrectPassword

    def confirm(self, token):
        """
        Confirm this user
        """
        if token != "secret_token":
            raise IncorrectConfirmationToken


def get_random_number():
    """
    Chosen by fair dice roll. Guaranteed to be random.
    """
    return 4
