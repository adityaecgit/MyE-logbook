from flask import jsonify
from flask_restful import Resource
from connection import create_connection

class Parameters(Resource):
    def get(self):
        connection = create_connection()

        if connection:
            try:
                cursor = connection.cursor()
                # Example: Execute a SQL query
                cursor.execute("SELECT * FROM tblParameter")
                columns = [column[0] for column in cursor.description]
                result = [dict(zip(columns, row)) for row in cursor.fetchall()]

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
        
        