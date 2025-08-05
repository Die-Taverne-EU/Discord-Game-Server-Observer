import sqlite3
import os
import mysql.connector
from numpy import insert

db_connection = os.getenv('DB_CONNECTION', 'sqlite')

def connect_to_sqlite():
    """Connect to a SQLite database."""
    return sqlite3.connect(os.getenv('DB_NAME', 'database.db'))

def connect_to_mysql():
    """Connect to a MySQL database."""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'database_name')
    )

def build_connection():
    """Build a database connection based on environment variables."""
    
    if db_connection == 'sqlite':
        return connect_to_sqlite()
    elif db_connection == 'mysql':
        return connect_to_mysql()
    else:
        raise ValueError("Unsupported database connection type.")

def create_server_table(conn):
    if db_connection == 'sqlite':
        query = """CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL,
            port INTEGER NOT NULL,
            description TEXT DEFAULT NULL,
            channel_id INTEGER DEFAULT NULL
        );
        """
    elif db_connection == 'mysql':
        query = """CREATE TABLE IF NOT EXISTS servers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            address VARCHAR(255) NOT NULL,
            port INT NOT NULL,
            description TEXT DEFAULT NULL,
            channel_id INT DEFAULT NULL
        );
        """
    else:
        raise ValueError("Unsupported database connection type.")

    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()

def create_settings_table(conn):
    if db_connection == 'sqlite':
        query = """CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL
        );
        """
    elif db_connection == 'mysql':
        query = """CREATE TABLE IF NOT EXISTS settings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            key VARCHAR(255) NOT NULL UNIQUE,
            value TEXT NOT NULL
        );
        """
    else:
        raise ValueError("Unsupported database connection type.")

    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()

def fill_default_settings(conn):
    """Fill the settings table with default values if it is empty."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM settings")
    count = cursor.fetchone()[0]

    if count == 0:
        default_settings = [
            ('language', 'de'),
            ('timezone', 'Europe/Berlin'),
            ('notification_channel_id', ''),
        ]
        cursor.executemany("INSERT INTO settings (key, value) VALUES (?, ?)", default_settings)
        conn.commit()

    cursor.close()

def migrate_database():
    """Migrate the database schema if necessary."""
    conn = build_connection()
    create_server_table(conn)
    create_settings_table(conn)
    fill_default_settings(conn)
    conn.close()

# prepared statements
prepq_get_setting = "SELECT value FROM settings WHERE key = ?;"
prepq_update_settings = "UPDATE settings SET value = ? WHERE key = ?;"
prepq_insert_server = "INSERT INTO servers (address, port, description, channel_id) VALUES (?, ?, ?, ?);"

async def build_cursor():
    """Build a cursor based on the database connection type."""
    conn = build_connection()
    if db_connection == 'sqlite':
        return conn.cursor()
    elif db_connection == 'mysql':
        return conn.cursor(prepared=True)
    else:
        raise ValueError("Unsupported database connection type.")

# database operations
async def get_setting(key):
    cursor = await build_cursor()
    cursor.execute(prepq_get_setting, (key,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

async def get_all_settings():
    cursor = await build_cursor()
    cursor.execute("SELECT key, value FROM settings;")
    results = cursor.fetchall()
    cursor.close()
    return {key: value for key, value in results}

async def update_setting(key, value):
    cursor = await build_cursor()
    cursor.execute(prepq_update_settings, (value, key))
    cursor.connection.commit()
    cursor.close()

async def insert_server(address, port, description=None, channel_id=None):
    cursor = await build_cursor()
    cursor.execute(prepq_insert_server, (address, port, description, channel_id))
    cursor.connection.commit()
    cursor.close()