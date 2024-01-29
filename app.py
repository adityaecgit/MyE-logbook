# app.py
from flask import Flask
from flask_restful import Api, Resource
from controllers.user.user import user_blueprint, User
from controllers.user.userrole import userrole_blueprint, UserRole
from connection import create_connection

app = Flask(__name__)
api = Api(app)

# Create a connection when the app starts
connection = create_connection()

# Register the user and user role blueprints
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(userrole_blueprint, url_prefix='/userrole')


# Define API resources
class UserDataResource(Resource):
    def get(self):
        return User.get_user_data()

class UserRoleResource(Resource):
    def get(self):
        return UserRole.get_user_roles()

class CreateUserResource(Resource):
    def post(self):
        return User.create_user()
    
# Add the API resources to the API with specific routes
api.add_resource(UserDataResource, '/api/user/data')
api.add_resource(UserRoleResource, '/api/user/roles')
api.add_resource(CreateUserResource, '/api/user/create')


if __name__ == '__main__':
    app.run(debug=True)
