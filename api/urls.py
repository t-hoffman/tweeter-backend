from flask_restful import Api

from .controllers.tweet_controller import *
from .controllers.users_controller import *
from .controllers.comments_controller import *
from .controllers.messages_controller import *

api = Api()

# User URLS
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')
api.add_resource(UsersList, '/api/users')
api.add_resource(VerifyUser, '/api/verify')
api.add_resource(GetUserInfo, '/api/users/<int:user_id>')
api.add_resource(UpdateUser, '/api/users/<int:user_id>')

# Tweet URLS

api.add_resource(ShowAllTweets, '/api/tweets')
api.add_resource(ShowUserTweets, '/api/tweets/<int:user_id>')
api.add_resource(CreateTweet, '/api/tweet')
api.add_resource(ShowTweet, '/api/tweet/<int:id>')
api.add_resource(ChangeTweet, '/api/tweet/<int:id>')
api.add_resource(DeleteTweet, '/api/tweet/<int:id>')

# Comments

api.add_resource(CreateComment, '/api/comment')
api.add_resource(DeleteComment, '/api/comment/<int:id>')

# Messages

api.add_resource(SendMessage, '/api/messages')
api.add_resource(ShowUserMessages, '/api/messages/<int:user_id>')
api.add_resource(ShowConversation, '/api/messages/<int:user_id>/<int:recipient_id>')