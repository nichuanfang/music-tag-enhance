from db.postgres import fetch_data
from db.sqlite import insert_data
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