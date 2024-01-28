import configparser
import pyodbc

def create_connection():
    # Replace these with your SQL Server credentials
    server = 'ECGIT2023001212\SQLEXPRESS'
    database = 'elogbook_dev1'
    username = 'ECGIT2023001212\\user'
    password = ''
    driver = 'SQL Server'

    # Create a connection string
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Add a section named 'SQLServer' to the config object
    config.add_section('SQLServer')

    # Set the options in the 'SQLServer' section
    config.set('SQLServer', 'server', server)
    config.set('SQLServer', 'database', database)
    config.set('SQLServer', 'username', username)
    config.set('SQLServer', 'password', password)
    config.set('SQLServer', 'driver', driver)

    # Write the config object to a file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    try:
        # Attempt to establish a connection
        cnxn = pyodbc.connect(conn_str)
        return cnxn
    except Exception as e:
        # Handle connection errors
        print(f"Error connecting to SQL Server: {str(e)}")
        return None
