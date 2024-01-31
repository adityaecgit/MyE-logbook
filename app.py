# app.py
from datetime import timedelta
from flask import Flask,request,jsonify
from flask_restful import Api, Resource
from controllers.user.user import *
from controllers.user.userrole import *
from controllers.Shift_incharge.Log_Ebook.Parameters import *
from connection import create_connection
from flask_cors import CORS
from flask_jwt_extended import JWTManager


import configparser

# Setting the JWT Secret Key as a global variable
JWT_SECRET_KEY = "aff19e7bd3c44f3c929a9b00752dab6b"

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)

# Adding CORS to the app
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)

# Create a connection when the app starts
connection = create_connection()



# Setting the endpoints for users    
api.add_resource(User, 
                "/users/<int:id>", "/users")
api.add_resource(Role,
                 "/roles/<int:id>", "/roles")
api.add_resource(Login, "/users/login")
api.add_resource(Parameters,"/parameter")

if __name__ == '__main__':         
    app.run(debug=True)

