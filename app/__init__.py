from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime, timedelta

from .urls import *
from .config import config

def create_app():
  app = Flask(__name__)
  migrate = Migrate(compare_type=True)

  CORS(app)
  app.config.from_object(config['development'])
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
  # app.config['SQLALCHEMY_ECHO'] = True
  
  db.init_app(app)
  migrate.init_app(app, db)
  bcrypt.init_app(app)
  jwt.init_app(app)
  api.init_app(app)
  
  return app