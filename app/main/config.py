import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hrkim0624@gmail.com'
    DEBUG = False
    JSON_AS_ASCII = False
    DELIMITER = '|'
    DEFAULT_LOCALE = 'ko'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'search_company.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'search_company_test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig
)

key = Config.SECRET_KEY
