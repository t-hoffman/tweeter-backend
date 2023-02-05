from flask import request, jsonify
from sqlalchemy.orm import lazyload
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

from ..serializers import *


# User Authentication

class Register(Resource):
  def post(self):
    try:
      user = request.get_json()
      if User.query.filter_by(email=user['email']).first():
        return {'message': False, 'code': 1}, 200
      if User.query.filter_by(username=user['username']).first():
        return {'message': False, 'code': 2}, 200
      
      new_user = User(
        name = user['name'],
        username = user['username'],
        email = user['email'],
        password = user['password'],
        image = user['image'],
        banner = user['banner']
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

class VerifyUser(Resource):
  @jwt_required()
  def post(self):
    try:
      current_user = get_jwt_identity()
      user = User.query.get_or_404({'id': current_user})
      return user_schema.dump(user), 200
    except Exception as e:
      return {'error': str(e)}, 418

class GetUserInfo(Resource):
  def get(self, user_id):
    try:
      user = User.query.get_or_404({'id': user_id})
      return user_schema.dump(user), 200
    except Exception as e:
      return {'error': str(e)}, 418

class UpdateUser(Resource):
  @jwt_required()
  def put(self, user_id):
    try:
      update_user = request.get_json()
      
      if ('password' in update_user):
        update_user['password'] = bcrypt.generate_password_hash(update_user['password']).decode('UTF-8')

      User.query.filter_by(id=user_id).update(update_user)
      updated_user = User.query.get_or_404(user_id)

      return user_schema.dump(updated_user), 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 418
    finally:
        db.session.commit()