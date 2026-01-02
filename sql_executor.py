load_dotenv()

env = {
    'HOST': os.getenv("MYSQL_HOST"),
    'USERNAME': os.getenv("MYSQL_USERNAME"),
    'DATABASE_NAME': os.getenv("MYSQL_DATABASE_NAME"),
    'PASSWORD': os.getenv("MYSQL_PASSWORD")
}

class MySQLExecutor:
    def __init__(self, host: str ='localhost', user: str = ''):
