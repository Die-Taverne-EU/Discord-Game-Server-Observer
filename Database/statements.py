from enum import Enum

class PreparedStatements(Enum):
    CREATE_SERVER_TABLE = """
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_type TEXT NOT NULL,
            address TEXT NOT NULL,
            port INTEGER NOT NULL,
            channel_id BIGINT NOT NULL,
            message_id BIGINT NOT NULL
        )
    """