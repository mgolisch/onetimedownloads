import os
from onetimedownloads import app 

DEBUG = False # Turns on debugging features in Flask
SECRET_KEY = os.environ.get('SECRET_KEY',None) # read secret key from environment if not present set to None (will cause execption on app start)
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','sqlite:///%s/onetimedownloads.db' % app.instance_path ) # read database url from environment if not present asume sqlite db in instance folder(local run)