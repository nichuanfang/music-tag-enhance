import psycopg
from config.settings import POSTGRESQL_CONFIG

def get_pg_conn():
    return psycopg.connect(**POSTGRESQL_CONFIG)

def fetch_data(sql, params=None):
    with get_pg_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]