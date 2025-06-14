import os

POSTGRESQL_CONFIG = {
    "host": os.getenv("POSTGRESQL_HOST", "localhost"),
    "port": int(os.getenv("POSTGRESQL_PORT", 5432)),
    "dbname": os.getenv("POSTGRESQL_DBNAME", "n8n"),
    "user": os.getenv("POSTGRESQL_USER", "root"),
    "password": os.getenv("POSTGRESQL_PASSWORD", "admin123"),
}

SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "data/target.sqlite")
