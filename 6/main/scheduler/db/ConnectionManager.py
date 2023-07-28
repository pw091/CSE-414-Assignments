import pymssql
import os
from dotenv import load_dotenv

class ConnectionManager:
    def __init__(self):
        if load_dotenv()==False:
            print('ERROR: .env file not found')
            print('This implementation assumes a venv and uses dotenv for environment variable permanence')
            print('Create a plaintext file called ".env" in the same directory as ConnectionManager.py with these 4 lines:')
            print('Server={}\nDBName={}}\nUserID={}\nPassword={}')
            exit()
        self.server_name = os.getenv("Server") + ".database.windows.net"
        self.db_name = os.getenv("DBName")
        self.user = os.getenv("UserID")
        self.password = os.getenv("Password")
        self.conn = None

    def create_connection(self):
        try:
            self.conn = pymssql.connect(server=self.server_name, user=self.user, password=self.password, database=self.db_name)
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL connection processing! ")
            print(db_err)
            quit()
        return self.conn

    def close_connection(self):
        try:
            self.conn.close()
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL connection processing! ")
            print(db_err)
            quit()
