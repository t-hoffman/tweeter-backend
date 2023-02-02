from .models import *
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

class UserSchema(SQLAlchemyAutoSchema):
  class Meta:
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