import sqlite4
from ..config.settings import SQLITE_DB_PATH

def get_sqlite_conn():
    return sqlite4.connect(SQLITE_DB_PATH)

def insert_data(table, data_list):
    if not data_list:
        return
    keys = data_list[0].keys()
    columns = ', '.join(keys)
    placeholders = ', '.join(['?'] * len(keys))
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    with get_sqlite_conn() as conn:
        conn.executemany(sql, [tuple(d.values()) for d in data_list])
        conn.commit()