# Music-tag-web 增强项目

## Feature

- [ ] 同步 navidrome 的播放记录到 mtw
- [ ] 对 mtw 的歌曲进行智能 ai 分类

## 数据库同步功能

本项目支持将SQLite数据库中的表同步到PostgreSQL中，支持自定义同步逻辑。  
例如可将SQLite的music-record表同步到PostgreSQL的pg-music-record表。

## 使用说明

- 配置 `docker-compose.yml` 中的数据库连接环境变量  
- 使用 `app/sync/sync_service.py` 中的 `DataSyncService` 或 `ReverseDataSyncService` 进行同步  
- 自定义同步逻辑可通过传入字段映射或自定义转换函数扩展

## 运行

```bash
docker-compose up --build
```

或者本地环境：

```bash
python app/main.py
```

## 依赖

- psycopg: PostgreSQL 连接
- sqlite3: SQLite 连接
```
