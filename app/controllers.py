from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity

from .serializers import *

class ActivityList(Resource):
  def get(self):
    try:
      activity_list = Activity.query.all()
      return activities_schema.dump(activity_list), 200
    except Exception as e:
      return {'message': str(e)}, 418

class ActivityCreate(Resource):
  def post(self):
    try: 
      activity_json = request.get_json()
      
      new_activity = Activity(
        activity = activity_json['activity'],
        type = activity_json['type'],
        participants = activity_json['participants'],
        price = activity_json['price'],
        link = activity_json['link'],
        key = activity_json['key'],
        accessibility = activity_json['accessibility'],
      )

      db.session.add(new_activity)
      # flush() allows us to show the new id when returning new_activity
      db.session.flush()
      return activity_schema.dump(new_activity), 201
    except Exception as e:
      db.session.rollback()
      return {'error': str(e)}, 418
    finally:
      db.session.commit()

class ActivityDetail(Resource):
  def get(self, id):
    try:
      activity = Activity.query.get_or_404(id)
      return activity_schema.dump(activity), 200
    except Exception as e:
      return {'message': str(e)}, 418

class ActivityUpdate(Resource):
  def put(self, id):
    try:
      update_activity = request.get_json()
      Activity.query.filter_by(id=id).update(update_activity)
      updated_activity = Activity.query.get_or_404(id)

      return activity_schema.dump(updated_activity), 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 418
    finally:
        db.session.commit()

class ActivityDelete(Resource):
  def delete(self, id):
    try:
      delete_activity = Activity.query.get_or_404(id)
      db.session.delete(delete_activity)
      db.session.commit()

      all_activities = Activity.query.all()
      return activities_schema.dump(all_activities), 200
    except Exception as e:
      return {'error': str(e)}, 418

class Register(Resource):
  def post(self):
    try:
      user = request.get_json()
      if User.query.filter_by(email=user['email']).first():
        return {'message': False, 'code': 1}, 200
      if User.query.filter_by(username=user['username']).first():
        return {'message': False, 'code': 2}, 200
      
      new_user = User(
        username=user['username'],
        email=user['email'],
        password=user['password']
      )
      db.session.add(new_user)
      db.session.commit()
      return {'message': True}
    except Exception as e:
      return {'error': str(e)}, 418

class Login(Resource):
  def post(self):
    try:
      user = request.get_json()
      if User.authenticate(user['username'], user['password']):
        user = User.query.filter_by(username=user['username']).first()
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
      else:
        return False
    except Exception as e:
      return {'error': str(e)}, 418

class Logout(Resource):
  @jwt_required()
  def delete(self):
    try:
      jti = get_jwt()['jti']
      now = datetime.now()
      db.session.add(TokenBlocklist(jti=jti, created_at=now))
      db.session.commit()
      return jsonify(message='User logged out')
    except Exception as e:
      return {'error': str(e)}, 418

class UsersList(Resource):
  def get(self):
    try:
      users = User.query.all()
      return users_schema.dump(users), 200
    except Exception as e:
      return {'error': str(e)}, 418

class UserInfo(Resource):
  @jwt_required()
  def post(self):
    try:
      current_user = get_jwt_identity()
      user = User.query.get_or_404({"id": current_user})
      return user_schema.dump(user), 200
    except Exception as e:
      return {'error': str(e)}, 418

class Test(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        return {"logged_in_as": current_user}, 200