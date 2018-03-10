import os


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', '<\xabz\x8bu\xf8\xa6\x88\x8c\xc8 \x0e\xec\xa3\xfe];\x9f\x7f\xa3]\x8b\x89\x1f')
    DEBUG = False
    SQLALCHEMY_TRACK_NOTIFICATIONS = False
