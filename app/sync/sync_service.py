from db.postgres import fetch_data, get_pg_conn
from db.sqlite import insert_data, get_sqlite_conn
from models.mapping import PG_TO_SQLITE_MAPPING
from utils.logger import logger

class DataSyncService:
    def __init__(self, pg_table):
        self.pg_table = pg_table
        self.mapping = PG_TO_SQLITE_MAPPING[pg_table]

    def sync(self):
        logger.info(f"Start syncing table: {self.pg_table}")
        # 1. 从PG取数据
        data = fetch_data(f"SELECT * FROM {self.pg_table}")
        if not data:
            logger.warning("No data found.")
            return

        # 2. 拆分数据并写入SQLite
        for sqlite_table, fields in self.mapping.items():
            data_to_insert = [
                {k: row[k] for k in fields if k in row}
                for row in data
            ]
            insert_data(sqlite_table, data_to_insert)
            logger.info(f"Inserted {len(data_to_insert)} rows into {sqlite_table}")

        logger.info("Sync completed.")

# 可扩展为增量同步、字段转换、数据校验等

class ReverseDataSyncService:
    """
    支持将SQLite表同步到PostgreSQL，支持自定义同步逻辑。
    """

    def __init__(self, sqlite_table, pg_table, field_mapping=None, transform_func=None):
        """
        sqlite_table: str, SQLite中的表名
        pg_table: str, PostgreSQL中的表名
        field_mapping: dict or None, SQLite字段到PG字段映射，默认为一一对应
        transform_func: callable or None, 自定义数据转换函数，接收SQLite数据字典列表，返回PG数据字典列表
        """
        self.sqlite_table = sqlite_table
        self.pg_table = pg_table
        # 默认字段映射是直接使用SQLite字段名作为PG字段
        self.field_mapping = field_mapping or {}
        self.transform_func = transform_func

    def sync(self):
        logger.info(f"Start syncing from SQLite table '{self.sqlite_table}' to PostgreSQL table '{self.pg_table}'")
        from db.sqlite import fetch_data as fetch_sqlite_data

        # 1. 从SQLite读取数据
        sqlite_data = fetch_sqlite_data(f"SELECT * FROM {self.sqlite_table}")
        if not sqlite_data:
            logger.warning("No data found in SQLite table.")
            return

        # 2. 处理映射和数据转换
        if self.transform_func:
            pg_data = self.transform_func(sqlite_data)
        else:
            # 默认映射字段转换
            pg_data = []
            for row in sqlite_data:
                new_row = {}
                if self.field_mapping:
                    # 有映射关系时
                    for sqlite_field, pg_field in self.field_mapping.items():
                        if sqlite_field in row:
                            new_row[pg_field] = row[sqlite_field]
                else:
                    # 无映射，字段名相同直接复制
                    new_row = row.copy()
                pg_data.append(new_row)

        if not pg_data:
            logger.warning("No data to insert into PostgreSQL after transformation.")
            return

        # 3. 插入数据到PostgreSQL
        placeholders = ', '.join(['%s'] * len(pg_data[0]))
        columns = ', '.join(pg_data[0].keys())
        insert_sql = f"INSERT INTO {self.pg_table} ({columns}) VALUES ({placeholders})"

        try:
            with get_pg_conn() as conn:
                with conn.cursor() as cur:
                    values = [tuple(item.values()) for item in pg_data]
                    cur.executemany(insert_sql, values)
                conn.commit()
            logger.info(f"Inserted {len(pg_data)} rows into PostgreSQL table '{self.pg_table}'.")
        except Exception as e:
            logger.error(f"Failed to insert data into PostgreSQL: {e}")
