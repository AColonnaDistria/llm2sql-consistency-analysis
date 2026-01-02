from dotenv import load_dotenv
import os

import PyMySQL

load_dotenv()

class MySQLExecutor:
    def __init__(self, host: str, user: str, database: str, password: str):
        self.host = host
        self.user = user
        self.database = database
        self.password = password

    def run_query(self, query: str):
        connection = pymysql.connect(host=self.host,
                                     user=self.user,
                                     password=self.password,
                                     database=self.database,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        return result
