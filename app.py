# app.py
from flask import Flask
from flask_restful import Api, Resource
from controllers.user.user import user_blueprint, User
from connection import create_connection

app = Flask(__name__)
api = Api(app)

# Create a connection when the app starts
connection = create_connection()

# Register the user blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

# Define a simple API resource
class UserDataResource(Resource):
    def get(self):
        return User.get_user_data()

# Add the API resource to the API with a specific route
api.add_resource(UserDataResource, '/api/user/data')

if __name__ == '__main__':
    app.run(debug=True)
