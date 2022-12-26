import os


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'you-will-never-guess'
    


class ProductionConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DATABASE_URL = os.environ.get('DATABASE_TEST_URL')
    TESTING = True


app_config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}