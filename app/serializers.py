from .models import *
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class ActivitySchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Activity
    loadInstance = True

activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)

class UserSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = User
    loadInstance = True

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(exclude=["password"],many=True)