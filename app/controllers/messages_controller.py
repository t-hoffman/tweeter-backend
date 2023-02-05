from flask import request
from sqlalchemy.orm import lazyload, joinedload
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from sqlalchemy import and_

from ..serializers import *

# Messages

class SendMessage(Resource):
  @jwt_required()
  def post(self):
    try: 
      message_json = request.get_json()

      new_message = Message(
        user_id = get_jwt_identity(),
        recipient_id = message_json['recipient_id'],
        message = message_json['message'],
      )

      db.session.add(new_message)
      # flush() allows us to show the new id when returning new_activity
      db.session.flush()
      return message_schema.dump(new_message), 201
    except Exception as e:
      db.session.rollback()
      return {'error': str(e)}, 418
    finally:
      db.session.commit()

class ShowUserMessages(Resource):
  def get(self, user_id):
    try:
      # message_list = User.query.join(Message, Message.user_id == User.id).filter((Message.recipient_id == user_id) | (Message.user_id == user_id)).all()
      message_list = User.query.join(Message, Message.user_id == User.id).filter(Message.recipient_id == user_id).all()
      print(message_list)
      
      return senders_schema.dump(message_list), 200
    except Exception as e:
      return {'message': str(e)}

class ShowConversation(Resource):
  def get(self, user_id, recipient_id):
    # sender_list = User.query.join(Message, Message.user_id == User.id).filter(Message.recipient_id == recipient_id, Message.user_id == user_id).first()
    # receiver_list = User.query.join(Message, Message.user_id == User.id).filter(Message.recipient_id == user_id, Message.user_id == recipient_id).first()
    
    # receiver_list = Message.query.join(User, Message.user_id == User.id).filter(Message.recipient_id == user_id, Message.user_id == recipient_id).all()
    # sender_list = Message.query.join(User, Message.user_id == User.id).filter(Message.recipient_id == recipient_id, Message.user_id == user_id).all()
    
    # return convos_schema.dump([*sender_list, *receiver_list]), 201
    # sender_list = User.query.join(Message, and_(Message.user_id == recipient_id, Message.recipient_id == user_id)).filter(User.id == recipient_id, Message.user_id == recipient_id).first()
    # receiver_list = User.query.join(Message, and_(Message.user_id == user_id, Message.recipient_id == recipient_id)).filter(User.id == user_id, Message.user_id == user_id).first()
    
    users = User.query.filter((User.id == user_id) | (User.id == recipient_id)).all()
    receiver_list = Message.query.join(User, Message.user_id == User.id).filter(Message.recipient_id == user_id, Message.user_id == recipient_id).all()
    sender_list = Message.query.join(User, Message.user_id == User.id).filter(Message.recipient_id == recipient_id, Message.user_id == user_id).all()
    messages_list = [*receiver_list, *sender_list]

    return {
      'users': users_schema.dump(users),
      'messages': convos_schema.dump(messages_list)
    }
