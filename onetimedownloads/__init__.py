from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

#enable instance config
app = Flask(__name__, instance_relative_config=True)
#load config
app.config.from_object('config')
#have instance config overwrite/change settings
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
Bootstrap(app)

import onetimedownloads.views
import onetimedownloads.models
import onetimedownloads.forms
