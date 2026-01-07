from dotenv import load_dotenv
import os

import pymysql
import pymysql.cursors

import sqlglot
from sqlglot.errors import ParseError, TokenError  # Import both

load_dotenv()

class MySQLExecutor:
    def __init__(self, host: str = 'localhost', user: str = 'user', database: str = 'db', password: str = 'password'):
        self.host = host
        self.user = user
        self.database = database
        self.password = password

    def __make_connection(self):
        return pymysql.connect(host=self.host,
                            user=self.user,
                            password=self.password,
                            database=self.database,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    def __is_parsable_sql(self, query: str) -> bool:
        try:
            sqlglot.parse_one(query)
            return True
        except SqlglotError:
            print("NOT PARSABLE")
            return False

    def run_query(self, query: str):
        try:
            if self.__is_parsable_sql(query):
                connection = self.__make_connection()
                
                with connection:
                    with connection.cursor() as cursor:
                        cursor.execute(query)
                        result = cursor.fetchall()
                    connection.commit()
                
                return result
            else:
                return None
        except Exception:
            return None