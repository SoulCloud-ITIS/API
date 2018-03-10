import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.BaseConfig'
)
app.config.from_object(app_settings)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fruyfjgqkbraaq' \
                                        ':b4c3da4697d68c1e9deb92ad4a2df110fc9fefc7e39dedefd86258049c833110@ec2-50-16' \
                                        '-217-122.compute-1.amazonaws.com:5432' \
                                        '/ddduintd5jnpep?sslmode=require'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

if __name__ == '__main__':
    app.debug = True
    app.run()

from app import models, user_routes
