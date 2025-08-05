import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
DB_CONNECTION = os.getenv('DB_CONNECTION', 'sqlite')
DB_NAME = os.getenv('DB_NAME', 'database.db')

def get_connection():
    if DB_CONNECTION == 'sqlite':
        return sqlite3.connect(DB_NAME)
    else:
        raise ValueError("Unsupported database connection type.")