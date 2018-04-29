from swagger_server.get_random_number import db


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
    A user.
    """
    def __init__(self, email, config):
        self.email = email
        self.config = config

    @staticmethod
    def get(email):
        """
        Get a user by e-mail
        """
        try:
            user_data = db.DB[email]
        except KeyError as e:
            raise NoSuchUser("No such user") from e
        else:
            return User(email, user_data)

    @staticmethod
    def create(email, password):
        if email not in db.DB:
            db.DB[email] = {
                'password': password,
                'confirmed': False,
                'confirm_token': "secret_token",
            }
        else:
            raise UserAlreadyExists("User already exists")

    def login(self, password):
        """
        Log this user in.
        """
        if password != self.config['password']:
            raise IncorrectPassword("Incorrect password")

    def confirm(self, token):
        """
        Confirm this user
        """
        if self.config['confirmed']:
            raise IncorrectConfirmationToken("Already confirmed")
        elif token != self.config['confirm_token']:
            raise IncorrectConfirmationToken("Wrong confirmation token")
        else:
            self.config['confirmed'] = True

def get_random_number():
    """
    Chosen by fair dice roll. Guaranteed to be random.
    """
    return 4
