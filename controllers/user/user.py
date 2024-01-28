# controller/user/user.py
from flask import Blueprint, jsonify
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
