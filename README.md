# Music-tag-web 增强项目

## Feature

- [ ] 同步 navidrome 的播放记录到 mtw
- [ ] 对 mtw 的歌曲进行智能 ai 分类

## 数据库同步功能

本项目支持将SQLite数据库中的表同步到PostgreSQL中，需要自定义同步逻辑。  
例如可将SQLite的music-record表同步到PostgreSQL的pg-music-record表。

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
