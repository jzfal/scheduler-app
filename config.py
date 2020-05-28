import os
basedir = os.path.abspath(os.path.dirname(__file__))



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # config to track db migrations




class DevelopmentConfig(Config):
    Debug = True
    IMAGE_UPLOADS = "D:/User/Documents/ADMIN STUFF/intern-stuff/DTL/DTL-Interview/project-DTL/app/static"
    
