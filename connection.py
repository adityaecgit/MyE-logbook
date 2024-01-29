import configparser
import pyodbc

def create_connection():
    # Read the existing configuration from the config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get SQL Server credentials from the configuration
    server = config.get('SQLServer', 'server')
    database = config.get('SQLServer', 'database')
    username = config.get('SQLServer', 'username')
    password = config.get('SQLServer', 'password')
    driver = config.get('SQLServer', 'driver')

    # Create a connection string
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=yes;'

    try:
        # Attempt to establish a connection
        cnxn = pyodbc.connect(conn_str)
        return cnxn
    except Exception as e:
        # Handle connection errors
        print(f"Error connecting to SQL Server: {str(e)}")
        return None

# Example usage
connection = create_connection()
if connection:
    print("Connection successful.")
    # Perform operations with the connection
    # Don't forget to close the connection when done: connection.close()
