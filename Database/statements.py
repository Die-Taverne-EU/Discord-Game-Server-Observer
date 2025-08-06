from enum import Enum
from pickle import GET

class PreparedStatements(str, Enum):
    def __str__(self):
        return str(self.value)
    CREATE_SERVER_TABLE = """
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_type TEXT NOT NULL,
            address TEXT NOT NULL,
            port INTEGER NOT NULL,
            channel_id BIGINT NOT NULL,
            message_id BIGINT,
            country TEXT NOT NULL,
            lang TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    INSERT_SERVER = """
        INSERT INTO servers (game_type, address, port, channel_id, country, lang)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
    UPDATE_SERVER = """
        UPDATE servers
        SET game_type = ?, address = ?, port = ?, channel_id = ?, message_id = ?, country = ?, lang = ?
        WHERE id = ?
    """,
    ADD_SERVER_MESSAGE_ID = """
        UPDATE servers
        SET message_id = ?
        WHERE id = ?
    """,
    GET_SERVER = """
        SELECT * FROM servers WHERE id = ?
    """,
    GET_ALL_SERVERS = """
        SELECT * FROM servers
    """,
    GET_SERVER_BY_MESSAGE_ID = """
        SELECT * FROM servers WHERE message_id = ?
    """,
    GET_SERVER_BY_ADDRESS_PORT = """
        SELECT * FROM servers WHERE address = ? AND port = ?
    """,
    DELETE_SERVER = """
        DELETE FROM servers WHERE id = ?
    """,