from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    app_code = os.environ.get('APP_CODE')

    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB')

    MYSQL_CURSORCLASS = 'DictCursor'    # ensures that query results are returned as dictionaries
