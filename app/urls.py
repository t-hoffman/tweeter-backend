from flask_restful import Api

from .controllers import *

api = Api()

api.add_resource(ActivityList, '/activities/')
api.add_resource(ActivityCreate, '/activities/')
api.add_resource(ActivityDetail, '/activity/<int:id>')
api.add_resource(ActivityUpdate, '/activity/<int:id>')
api.add_resource(ActivityDelete, '/activity/<int:id>')

# User URLS
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Test, '/test')
api.add_resource(UsersList, '/users')
api.add_resource(UserInfo, '/verify')