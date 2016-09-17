from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

#enable instance config
app = Flask(__name__, instance_relative_config=True)
#load config
app.config.from_object('onetimedownloads.default_settings')
#have instance config overwrite/change settings
app.config.from_pyfile('config.py',silent=True)
if app.config['SECRET_KEY'] is None:
    raise Exception('no secret key in config')

db = SQLAlchemy(app)
Bootstrap(app)

import onetimedownloads.views
import onetimedownloads.models
import onetimedownloads.forms
