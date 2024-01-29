# controller/user/user.py
from flask import Blueprint, jsonify,request
from connection import create_connection

user_blueprint = Blueprint('user', __name__)

class User:
    @staticmethod
    def get_user_data():
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

    def create_user():
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
                """, id, user_id, email, user_name, user_manager, is_active, is_new)

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