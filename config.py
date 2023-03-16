import os 
basedir = os.path.abspath('./instance/')

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never guess'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'db.sqlite')
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	FLASK_ADMIN_SWATCH='cerulean'