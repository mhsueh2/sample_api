import os

DB_USER = os.getenv('DB_USER', 'myuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mypass')
DB_SERVICE = os.getenv('DB_SERVICE', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'dev')
DB_TABLE = os.getenv('DB_TABLE', 'vehicle')
DB_SCHEMA = os.getenv('DB_SCHEMA', 'dev')

SQLALCHEMY_DATABASE_URI = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    DB_USER,
    DB_PASSWORD,
    DB_SERVICE,
    DB_PORT,
    DB_NAME
)