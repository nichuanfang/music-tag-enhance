import os

POSTGRESQL_CONFIG = {
    "host": os.getenv("POSTGRESQL_HOST", "localhost"),
    "port": int(os.getenv("POSTGRESQL_PORT", 5432)),
    "dbname": os.getenv("POSTGRESQL_DBNAME", "your_db"),
    "user": os.getenv("POSTGRESQL_USER", "your_user"),
    "password": os.getenv("POSTGRESQL_PASSWORD", "your_password"),
}

SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "data/target.sqlite")
