import sqlite3
from ..config.settings import SQLITE_DB_PATH

def get_sqlite_conn():
    return sqlite3.connect(SQLITE_DB_PATH)

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

def fetch_data(sql, params=None):
    with get_sqlite_conn() as conn:
        cur = conn.execute(sql, params or ())
        columns = [d[0] for d in cur.description]
        rows = cur.fetchall()
        return [dict(zip(columns, row)) for row in rows]
