from flask import request
from sqlalchemy.orm import lazyload, joinedload
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

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
      message_list = User.query.join(Message, Message.user_id == User.id).filter(Message.recipient_id == user_id).all()
      print(message_list)
      
      return senders_schema.dump(message_list), 200
    except Exception as e:
      return {'message': str(e)}

class ShowConversation(Resource):
  def get(self, user_id, recipient_id):
    # sender_list = User.query.join(Message, Message.user_id == User.id).filter(Message.recipient_id == recipient_id, Message.user_id == user_id).all()
    receiver_list = User.query.join(Message, Message.user_id == User.id).filter(Message.recipient_id == user_id, Message.user_id == recipient_id).all()
    # sender_list = Message.query.filter_by(recipient_id=user_id).options(lazyload(Message.sender))
    message_list = Message.query.options(lazyload(Message.sender)).filter_by(recipient_id=user_id).all()
    # message_list = Message.query.filter_by(recipient_id=user_id).join(User, User.id == Message.user_id).group_by(Message.id).all()
     
    
    return messages_schema.dump(message_list), 201
