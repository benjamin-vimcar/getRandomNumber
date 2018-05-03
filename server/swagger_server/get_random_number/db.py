"""
Our server's database connection.

The rest of the application must use this module to interact with the database.
This ensures that we can easily mock out the database in UTs.
"""

from flaskext.mysql import MySQL

#
MYSQL_DB = None


def init_mysql(app):
    """
    Initialise the database handler.

    Must be called during application initialisation (i.e. before any API
    calls are handled).
    """
    global MYSQL_DB
    MYSQL_DB = MySQL()
    app.app.config['MYSQL_DATABASE_USER'] = 'root'
    app.app.config['MYSQL_DATABASE_PASSWORD'] = \
        'super_secret_mysql_root_password'
    app.app.config['MYSQL_DATABASE_DB'] = 'random_number'
    app.app.config['MYSQL_DATABASE_HOST'] = 'database'
    MYSQL_DB.init_app(app.app)


def get_user(email):
    """
    Get a user and their data

    Returns a `(email, password, confirmed)` tuple

    Raises a ValueError is the user doesn't exist
    """
    global MYSQL_DB
    connection = MYSQL_DB.connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT email, password, confirmed FROM users
            WHERE email = '{email}'
            """.format(email=email))
        [result] = cursor.fetchall()
        return result
    finally:
        connection.close()


def create_user(email, password):
    """
    Create a user.

    Raises a `pymysql.err.IntegrityError` if the user already exists.
    """
    global MYSQL_DB
    connection = MYSQL_DB.connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO users (email, password, confirmed)
            VALUES ('{email}', '{password}', FALSE)

            """.format(email=email, password=password))
        connection.commit()
    finally:
        connection.close()


def confirm_user(email):
    """
    Set a user as confirmed.

    Has no effect if the user is already confirmed, or doesn't exist.
    """
    global MYSQL_DB
    connection = MYSQL_DB.connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users "
            "SET confirmed = TRUE "
            "WHERE email = '{}'".format(email))
        connection.commit()
    finally:
        connection.close()
