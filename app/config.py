import os
import pwd

# Obtain the default postgres DB
def get_local_database_url():
    username = pwd.getpwuid( os.getuid() )[ 0 ]
    return 'postgresql://{0}@localhost'.format(username)

class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost'
    HOST="0.0.0.0"
    PORT = 5000

class ProductionConfig(Config):
    PORT = int(os.environ.get('PORT', 5000))
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_local_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True