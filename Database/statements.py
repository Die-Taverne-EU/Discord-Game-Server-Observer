from enum import Enum

class PreparedStatements(Enum):
    CREATE_SERVER_TABLE = """
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            region TEXT NOT NULL
        )
    """