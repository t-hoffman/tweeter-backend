from os import environ
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

class Config:
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JSON_SORT_KEYS = False
  SECRET_KEY = environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = environ.get('POSTGRES_URL')

config = {
  'development': DevelopmentConfig
}