from dotenv import load_dotenv
import os

import pymysql
import pymysql.cursors

import sqlglot
from sqlglot.errors import ParseError, TokenError  # Import both

load_dotenv()

class MySQLSchemaInitializer:
    def __init__(self, host: str = 'localhost', admin_user: str = 'user', database: str = 'db', admin_password: str = 'password'):
        self.host = host
        self.admin_user = admin_user
        self.database = database
        self.admin_password = admin_password

    def __make_connection(self):
        return pymysql.connect(host=self.host,
                            user=self.admin_user,
                            password=self.admin_password,
                            database=self.database,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    def set_schema(self, schema: str):
        try:
            connection = self.__make_connection()
            
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(schema)
                connection.commit()
        except Exception as e:
            return

    def insert_data(self, insert: str):
        try:
            connection = self.__make_connection()
            
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(insert)
                connection.commit()
        except Exception as e:
            print(str(e))
            return
