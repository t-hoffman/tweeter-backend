from flask import request
from sqlalchemy.orm import lazyload
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..serializers import *

# Comments

class CreateComment(Resource):
  @jwt_required()
  def post(self):
    try: 
      comment_json = request.get_json()

      new_comment = Comment(
        user_id = get_jwt_identity(),
        tweet_id = comment_json['tweet_id'],
        comment = comment_json['comment'],
      )

      db.session.add(new_comment)
      # flush() allows us to show the new id when returning new_activity
      db.session.flush()
      return comment_schema.dump(new_comment), 201
    except Exception as e:
      db.session.rollback()
      return {'error': str(e)}, 418
    finally:
      db.session.commit()


class DeleteComment(Resource):
  @jwt_required()
  def delete(self, id):
    try:
      delete_comment = Comment.query.get_or_404(id)
      db.session.delete(delete_comment)
      db.session.commit()

      return True
    except Exception as e:
      return {'error': str(e)}, 418