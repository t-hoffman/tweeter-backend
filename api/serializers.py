from .models import *
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from flask_marshmallow import Marshmallow
import api

# ma = Marshmallow(app)

class UserSchema(SQLAlchemyAutoSchema):
  class Meta:
#     fields = ('id', 'name', 'email', 'username', 'image', 'banner', 'created_at')

# user_schema = UserSchema()
# users_schema = UserSchema(many=True)
    model = User
    load_instance = True

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(exclude=["password"],many=True)

class CommentSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Comment
    load_instance = True
  user = Nested(UserSchema(exclude=["password"]), attribute="user")

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

class TweetSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Tweet
    load_instance = True
  user = Nested(UserSchema(exclude=["password"]), attribute="user")
  comments = Nested(CommentSchema(many=True), attribute="comments")

tweet_schema = TweetSchema()
tweets_schema = TweetSchema(many=True)

class MessageSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Message
    load_instance = True
    include_fk = True
  
  # sender = Nested(UserSchema(), attribute="sender")

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

class SenderSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = User
    load_instance = True
  
  messages = Nested(MessageSchema(), attribute="messages", many=True)

sender_schema = SenderSchema(exclude=["password"])
senders_schema = SenderSchema(exclude=["password"],many=True)


class ConvoSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Message
    load_instance = True
  
  sender = Nested(UserSchema(exclude=["password"]), attribute="sender")
  # receiver = Nested(UserSchema(), attribute="receiver")

convo_schema = ConvoSchema()
convos_schema = ConvoSchema(many=True)

class ShowConvoSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = User
    load_instance = True
  
  messages = Nested(ConvoSchema(), attribute="messages", many=True)

show_convo_schema = ShowConvoSchema()
show_convos_schema = ShowConvoSchema(many=True)