# controller/user/userrole.py
from flask import jsonify
from flask_restful import Resource
from connection import create_connection

class Role(Resource):
    def get(self):
        connection = create_connection()

        if connection:
            try:
                cursor = connection.cursor()
                # Example: Execute a SQL query to get user roles
                cursor.execute("SELECT * from tblUserRole")
                roles = [row[0] for row in cursor.fetchall()]

                # Return the roles as JSON
                return jsonify({"roles": roles})
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
