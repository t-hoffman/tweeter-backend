from .models import *
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from flask_marshmallow import Marshmallow
import app

# ma = Marshmallow(app)

class UserSchema(SQLAlchemyAutoSchema):
  class Meta:
#     fields = ('id', 'name', 'email', 'username', 'image', 'banner', 'created_at')

# user_schema = UserSchema()
# users_schema = UserSchema(many=True)
    model = User
    loadInstance = True

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(exclude=["password"],many=True)

class CommentSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Comment
    loadInstance = True
  user = Nested(UserSchema(exclude=["password"]), attribute="user")

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

class TweetSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Tweet
    loadInstance = True
  user = Nested(UserSchema(exclude=["password"]), attribute="user")
  comments = Nested(CommentSchema(many=True), attribute="comments")

tweet_schema = TweetSchema()
tweets_schema = TweetSchema(many=True)

class MessageSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Message
    loadInstance = True
  sender = Nested(UserSchema(exclude=["password"]), attribute="sender")

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

class SenderSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = User
    loadInstance = True
  
  messages = Nested(MessageSchema(), attribute="messages", many=True)

sender_schema = SenderSchema(exclude=["password"])
senders_schema = SenderSchema(exclude=["password"],many=True)