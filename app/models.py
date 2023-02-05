from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

class Tweet(db.Model):
  __tablename__ = 'tweets'

  id = db.Column(db.Integer, nullable=False, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  content = db.Column(db.Text, nullable=False)
  likes = db.Column(db.Integer, nullable=True)
  retweet_id = db.Column(db.Integer, nullable=True)
  created_at = db.Column(db.DateTime, default=datetime.now)

class Comment(db.Model):
  __tablename__ = 'comments'

  id = db.Column(db.Integer, nullable=False, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'), nullable=False)
  comment = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now)

  comments = db.relationship('Tweet', backref='comments')

class Message(db.Model):
  __tablename__ = 'messages'

  id = db.Column(db.Integer, nullable=False, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  message = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now)
  # user = db.relationship('User', backref='user', foreign_keys="[Message.user_id]")
  
  sender = db.relationship('User', backref='sender', foreign_keys='[Message.user_id]')
  receiver = db.relationship('User', backref='receiver', foreign_keys='[Message.recipient_id]')
  
  def __init__(self, user_id, recipient_id, message):
    self.user_id = user_id
    self.recipient_id = recipient_id
    self.message = message
  
  def __repr__(self):
    return f'<Message: {self.message}'

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  username = db.Column(db.String(16), nullable=False, unique=True)
  email = db.Column(db.Text, nullable=False)
  password = db.Column(db.Text, nullable=False)
  name = db.Column(db.String(50), nullable=False)
  image = db.Column(db.Text, nullable=True)
  banner = db.Column(db.Text, nullable=True)
  created_at = db.Column(db.DateTime, default=datetime.now)

  tweets = db.relationship('Tweet', backref='user')
  comments = db.relationship('Comment', backref='user')
  messages = db.relationship('Message', backref='messages', foreign_keys="[Message.user_id]")
  # sender = db.relationship('Message', backref='sender', foreign_keys="[Message.user_id]")
  
  def __init__(self, username, email, password, name, image):
    self.username = username
    self.email = email
    self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
    self.name = name
    self.image = image
  
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