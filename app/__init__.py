import os
from flask import Flask 
from config import Config,basedir
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin


app = Flask(__name__,instance_relative_config=True)
app.config.from_object(Config)
db=SQLAlchemy(app)
login=LoginManager(app)
login.login_view='login'
admin=Admin(app)

try:
	os.makedirs(app.instance_path)
except OSError:
	pass

from app import routes,models