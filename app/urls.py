from flask_restful import Api

from .controllers.tweet_controller import *
from .controllers.users_controller import *
from .controllers.comments_controller import *
from .controllers.messages_controller import *

api = Api()

# User URLS
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(UsersList, '/users')
api.add_resource(VerifyUser, '/verify')
api.add_resource(GetUserInfo, '/users/<int:user_id>')
api.add_resource(UpdateUser, '/users/<int:user_id>')

# Tweet URLS

api.add_resource(ShowAllTweets, '/tweets')
api.add_resource(ShowUserTweets, '/tweets/<int:user_id>')
api.add_resource(CreateTweet, '/tweet')
api.add_resource(ShowTweet, '/tweet/<int:id>')
api.add_resource(ChangeTweet, '/tweet/<int:id>')
api.add_resource(DeleteTweet, '/tweet/<int:id>')

# Comments

api.add_resource(CreateComment, '/comment')

# Messages

api.add_resource(SendMessage, '/messages')
api.add_resource(ShowUserMessages, '/messages/<int:user_id>')
api.add_resource(ShowConversation, '/messages/<int:user_id>/<int:recipient_id>')