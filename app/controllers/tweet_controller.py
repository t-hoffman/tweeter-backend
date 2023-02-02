from flask import request
from sqlalchemy.orm import lazyload
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..serializers import *
from ..models import db

# Tweets

class ShowAllTweets(Resource):
  def get(self):
    try:
      tweet_list = Tweet.query.options(lazyload(Tweet.user), lazyload(Tweet.comments)).order_by(Tweet.created_at.desc()).all()

      return tweets_schema.dump(tweet_list), 200
    except Exception as e:
      return {'message': str(e)}, 418

class ShowUserTweets(Resource):
  def get(self, user_id):
    try:
      user_info = User.query.get_or_404({'id': user_id})
      tweet_list = Tweet.query.order_by(Tweet.created_at.desc()).filter_by(user_id=user_id)

      return {
        'user': user_schema.dump(user_info),
        'tweets': tweets_schema.dump(tweet_list)
      }, 200
    except Exception as e:
      return {'message': str(e)}

class CreateTweet(Resource):
  @jwt_required()
  def post(self):
    try: 
      tweet_json = request.get_json()

      new_tweet = Tweet(
        user_id = get_jwt_identity(),
        content = tweet_json['content'],
        retweet_id = tweet_json['retweet_id']
      )

      db.session.add(new_tweet)
      # flush() allows us to show the new id when returning new_activity
      db.session.flush()
      return tweet_schema.dump(new_tweet), 201
    except Exception as e:
      db.session.rollback()
      return {'error': str(e)}, 418
    finally:
      db.session.commit()

class ShowTweet(Resource):
  def get(self, id):
    try:
      tweet = Tweet.query.get_or_404(id)
      return tweet_schema.dump(tweet), 200
    except Exception as e:
      return {'message': str(e)}, 418

class ChangeTweet(Resource):
  @jwt_required()
  def put(self, id):
    try:
      update_tweet = request.get_json()
      Tweet.query.filter_by(id=id).update(update_tweet)
      updated_tweet = Tweet.query.get_or_404(id)

      return tweet_schema.dump(updated_tweet), 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 418
    finally:
        db.session.commit()

class DeleteTweet(Resource):
  @jwt_required()
  def delete(self, id):
    try:
      delete_tweet = Tweet.query.get_or_404(id)
      db.session.delete(delete_tweet)
      db.session.commit()

      all_tweets = Tweet.query.all()
      return tweets_schema.dump(all_tweets), 200
    except Exception as e:
      return {'error': str(e)}, 418
