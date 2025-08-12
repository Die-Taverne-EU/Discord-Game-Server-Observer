import sqlite3
from dotenv import load_dotenv
import os
from enum import Enum
import Database.statements as statements

load_dotenv()

class Driver(Enum):
    SQLITE = "sqlite"

drivers = [driver.value for driver in Driver]

class InvalidDriverError(Exception):
    pass

class Database:
    """Database connection manager for different database drivers."""

    def __init__(self):
        self.connect()

    def connect(self):
        driver = os.getenv('DB_DRIVER', 'sqlite').lower()
        if driver not in drivers:
            raise InvalidDriverError(f"Unsupported driver: {driver}. Supported drivers: {drivers}")
        
        match driver:
            case Driver.SQLITE.value:
                self.driver = Driver.SQLITE
                self.database = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), 'database.db'
                )
            case _:
                raise InvalidDriverError(f"Unsupported driver: {driver}. Supported drivers: {drivers}")
            
    def cursor(self):
        match self.driver:
            case Driver.SQLITE:
                conn = sqlite3.connect(self.database)
                cursor = conn.cursor()
                return conn, cursor
            
    def close(self, conn: sqlite3.Connection, cursor: sqlite3.Cursor):
        cursor.close()
        conn.close()

    def create_tables(self):
        conn, cursor = self.cursor()
        cursor.execute(statements.PreparedStatements.CREATE_SERVER_TABLE.__str__())
        conn.commit()
        self.close(conn, cursor)

    def insert_server(self, game_type, address, port, channel_id, country, lang):
        print(f"Inserting server: {game_type}, {address}, {port}, {channel_id}, {country}, {lang}")
        conn, cursor = self.cursor()
        cursor.execute(statements.PreparedStatements.INSERT_SERVER.__str__(), 
                       (game_type, address, port, channel_id, country, lang))
        conn.commit()
        self.close(conn, cursor)

    def update_server(self, server_id, game_type, address, port, channel_id, country, lang):
        conn, cursor = self.cursor()
        cursor.execute(statements.PreparedStatements.UPDATE_SERVER.__str__(), 
                       (game_type, address, port, channel_id, country, lang, server_id))
        conn.commit()
        self.close(conn, cursor)

    def update_server_message_id(self, server_id, message_id):
        conn, cursor = self.cursor()
        cursor.execute(statements.PreparedStatements.ADD_SERVER_MESSAGE_ID.__str__(), (message_id, server_id))
        conn.commit()
        self.close(conn, cursor)

    def update_server_name(self, server_id, name):
        conn, cursor = self.cursor()
        cursor.execute(statements.PreparedStatements.UPDATE_SERVER_NAME.__str__(), (name, server_id))
        conn.commit()
        self.close(conn, cursor)
    
    def get_server(self, server_id):
        conn, cursor = self.cursor()
        cursor.execute(statements.PreparedStatements.GET_SERVER.__str__(), (server_id,))
        server = cursor.fetchone()
        self.close(conn, cursor)
        return server

    def get_all_servers(self):
        conn, cursor = self.cursor()
        cursor.execute(statements.PreparedStatements.GET_ALL_SERVERS.__str__())
        servers = cursor.fetchall()
        self.close(conn, cursor)
        return servers

    def get_server_by_message_id(self, message_id):
        conn, cursor = self.cursor()
        cursor.execute(statements.PreparedStatements.GET_SERVER_BY_MESSAGE_ID.__str__(), (message_id,))
        server = cursor.fetchone()
        self.close(conn, cursor)
        return server
    
    def get_server_by_address_port(self, address, port):
        conn, cursor = self.cursor()
        cursor.execute(statements.PreparedStatements.GET_SERVER_BY_ADDRESS_PORT.__str__(), (address, port))
        server = cursor.fetchone()
        self.close(conn, cursor)
        return server

    def delete_server(self, server_id):
        conn, cursor = self.cursor()
        cursor.execute(statements.PreparedStatements.DELETE_SERVER.__str__(), (server_id,))
        conn.commit()
        self.close(conn, cursor)

    def count_servers(self):
        conn, cursor = self.cursor()
        cursor.execute(statements.PreparedStatements.COUNT_SERVERS.__str__())
        count = cursor.fetchone()[0]
        self.close(conn, cursor)
        return count
