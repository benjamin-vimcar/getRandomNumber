from flaskext.mysql import MySQL
# mysql = MySQL()
# mysql.init_app(app)

DB = {}

MYSQL_DB = None

def init_mysql(app):
    global MYSQL_DB
    MYSQL_DB = MySQL()
    app.app.config['MYSQL_DATABASE_USER'] = 'root'
    app.app.config['MYSQL_DATABASE_PASSWORD'] = 'super_secret_mysql_root_password'
    app.app.config['MYSQL_DATABASE_DB'] = 'random_number'
    app.app.config['MYSQL_DATABASE_HOST'] = 'database'
    MYSQL_DB.init_app(app.app)

    MYSQL_DB.connect().cursor()
