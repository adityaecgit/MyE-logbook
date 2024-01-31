# controller/user/user.py
import configparser
from tokenize import generate_tokens
from flask import Blueprint, jsonify, make_response,request
from flask_restful import Resource
from connection import create_connection
from datetime import datetime,timedelta
from flask_jwt_extended import create_access_token

# Resource to get all users from the database
config = configparser.ConfigParser()
config.read('config.ini')

class User(Resource):
    def get(self):
        connection = create_connection()

        if connection:
            try:
                cursor = connection.cursor()
                # Example: Execute a SQL query
                cursor.execute("SELECT * FROM tblUsers")
                columns = [column[0] for column in cursor.description]
                result = [dict(zip(columns, row)) for row in cursor.fetchall()]

                # Return the data as JSON
                return jsonify(result)
            except Exception as e:
                # Handle query errors
                print(f"Error executing SQL query: {str(e)}")
                return jsonify({"error": "Internal Server Error"}), 500
            finally:
                cursor.close()
                connection.close()
        else:
            # Return an error response if the connection is not established
            return jsonify({"error": "Internal Server Error"}), 500

    def post(self):
        connection = create_connection()

        if connection:
            try:
                # Get data from the request
                user_data = request.json
                id = user_data.get('Id')
                user_id = user_data.get('UserId')
                email = user_data.get('Email')
                user_name = user_data.get('UserName')
                user_manager = user_data.get('UserManager')
                is_active = user_data.get('is_active')
                is_new = user_data.get('is_new')

                # Example: Execute a SQL query to insert user data
                cursor = connection.cursor()
                cursor.execute("SET IDENTITY_INSERT tblUsers ON")
                cursor.execute("""
                    INSERT INTO tblUsers (Id, UserId, Email, UserName, UserManager, is_active, is_new)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (id, user_id, email, user_name, user_manager, is_active, is_new))

                # Commit the transaction
                connection.commit()

                # Return a JSON serializable response
                return {"message": "User created successfully"}, 201
            except Exception as e:
                # Handle query errors
                print(f"Error executing SQL query: {str(e)}")
                return {"error": "Internal Server Error"}, 500
            finally:
                cursor.close()
                connection.close()
        else:
            # Return an error response if the connection is not established
            return {"error": "Internal Server Error"}, 500
    
    
    def put(self,id):
        connection = create_connection()

        if connection:
            try:
                update_data = request.json
                # Example: Execute a SQL query to update user data
                cursor = connection.cursor()
                update_query = """
                    UPDATE tblUsers
                    SET UserId = ?,
                        Email = ?,
                        UserName = ?,
                        UserManager = ?,
                        is_active = ?,
                        is_new = ?
                    WHERE Id = ?
                """
                cursor.execute(update_query, (
                    update_data.get('UserId'),
                    update_data.get('Email'),
                    update_data.get('UserName'),
                    update_data.get('UserManager'),
                    update_data.get('is_active'),
                    update_data.get('is_new'),
                    id
                ))

                # Commit the transaction
                connection.commit()

                # Check if any rows were affected
                if cursor.rowcount > 0:
                    return {"message": "User updated successfully"}, 200
                else:
                    return {"error": "User not found"}, 404
            except Exception as e:
                # Handle query errors
                print(f"Error executing SQL query: {str(e)}")
                return {"error": "Internal Server Error"}, 500
            finally:
                connection.close()
        else:
            # Return an error response if the connection is not established
            return {"error": "Internal Server Error"}, 500

    def delete(self,id):
        connection = create_connection()

        if connection:
            try:
                cursor = connection.cursor()

                # Use proper parameter placeholder (e.g., ?, %s) based on your database driver
                cursor.execute("""
                    DELETE FROM tblUsers
                    WHERE Id=?
                """, (id))

                # No need to explicitly commit for DELETE operations
                connection.commit()


                return {"message": "User deleted successfully"}, 200
            except Exception as e:
                # Handle query errors
                print(f"Error executing SQL query: {str(e)}")
                return {"error": "Internal Server Error"}, 500
            finally:
                cursor.close()
                connection.close()
        else:
            # Return an error response if the connection is not established
            return {"error": "Internal Server Error"}, 500

class Login(Resource):
    def post(self):
        connection = create_connection()

        if connection:
            try:
                # Get credentials from the request
                login_data = request.json
                email = login_data.get('Email')
                password = "123456789"  # Retrieve the password field

                # Example: Execute a SQL query to authenticate the user
                cursor = connection.cursor()
                cursor.execute("SELECT UserId FROM tblUsers WHERE Email = ?", (email))
                user_id = cursor.fetchone()

                if user_id:
                    user = user_id[0]

                    # Generate a JWT token
                    jwt_token = create_access_token(identity=user)
                    response = make_response(jsonify({"token": jwt_token}), 200)
                    return response
                else:
                    return jsonify({"error": "Invalid credentials"}), 401
            except Exception as e:
                # Handle query errors
                print(f"Error executing SQL query: {str(e)}")
                return jsonify({"error": "Internal Server Error"}), 500
            finally:
                cursor.close()
                connection.close()
        else:
            # Return an error response if the connection is not established
            return jsonify({"error": "Internal Server Error"}), 500