from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# import pymongo

from sample1 import app
from sample1.loader import model_load

import os

SQL_DB_NAME = os.environ['SQL_DB_NAME']
SQL_DB_USER = os.environ['SQL_DB_USER']
SQL_DB_PASSWORD = os.environ['SQL_DB_PASSWORD']
SQL_DB_ADDRESS = os.environ['SQL_DB_ADDRESS']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4'\
    .format(SQL_DB_USER, SQL_DB_PASSWORD, SQL_DB_ADDRESS, SQL_DB_NAME)

MYSQL = SQLAlchemy(app)
MYSQL_migrate = Migrate(app, MYSQL, compare_type=True)

# MONGODB_DB_NAME = os.environ['MONGODB_DB_NAME']
# MONGODB_DB_USER = os.environ['MONGODB_DB_USER']
# MONGODB_DB_PASSWORD = os.environ['MONGODB_DB_PASSWORD']
# MONGODB_DB_ADDRESS = os.environ['MONGODB_DB_ADDRESS']
#
# MONGODB = pymongo.MongoClient(MONGODB_DB_ADDRESS, 27017,
#                               username=MONGODB_DB_USER,
#                               password=MONGODB_DB_PASSWORD,
#                               authSource=MONGODB_DB_NAME,
#                               authMechanism='SCRAM-SHA-256')

model_load(
    'comment',
    'post',
    'tag',
    'user_tag',
    'revoked_token',
    'user'
)
