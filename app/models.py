from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

class Activity(db.Model):
  __tablename__ = 'activities'

  id = db.Column(db.Integer, primary_key=True)
  activity = db.Column(db.String)
  type = db.Column(db.String)
  participants = db.Column(db.Integer, default=1)
  price = db.Column(db.Integer, default=0)
  link = db.Column(db.String)
  key = db.Column(db.String)
  accessibility = db.Column(db.String)

  def __init__(self, activity, type, participants, price, link, key, accessibility):
    self.activity = activity
    self.type = type
    self.participants = participants
    self.price = price
    self.link = link
    self.key = key
    self.accessibility = accessibility

  def __repr__(self):
    return f'<Activity {self.activity}'

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  username = db.Column(db.String(16), nullable=False, unique=True)
  email = db.Column(db.Text, nullable=False)
  password = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now())

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
  
  @classmethod
  def authenticate(cls, username, password):
    found_user = cls.query.filter_by(username=username).first()
    if found_user:
      authenticated_user = bcrypt.check_password_hash(found_user.password, password)
      if authenticated_user:
        return found_user
    
    return False

class TokenBlocklist(db.Model):
  __tablename__ = 'token_blocklist'

  id = db.Column(db.Integer, primary_key=True)
  jti = db.Column(db.String(36), nullable=False, index=True)
  created_at = db.Column(db.DateTime, nullable=False)

  @jwt.token_in_blocklist_loader
  def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload['jti']
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None