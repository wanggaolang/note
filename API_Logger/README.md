# 功能说明



# 表结构

详见[日志记录字段说明](./日志记录字段说明.xlsx)﻿



## 表创建

- clickhouse

```sql
CREATE TABLE IF NOT EXISTS viz_annotation_api_access_log (
    id UUID,
    interface_name String NOT NULL,
    access_time DateTime NOT NULL,
    client_ip String,
    request_method String,
    request_url String NOT NULL,
    request_header String,
    request_body String,
    request_body_size Int64 DEFAULT -1,
    request_identifier String,
    request_user String,
    client_environment String,
    response_time DateTime,
    interface_duration Float32,
    response_status Int32 DEFAULT -1,
    response_data String,
    response_size Int64 DEFAULT -1,
    server_environment String,
    service_instance_id String,
    server_ip String,
    log_source String,
    reserved_field_1 String,
    reserved_field_2 String
) ENGINE = MergeTree()
ORDER BY (response_time);
```



# 基于python tornado的实现

- 跑起来：
  - 启动命令：python3 python_tornado_implement.py
  - 客户端访问：http://localhost:8888/test_api

- 代码详见：[python_tornado_implement](./python_tornado_implement/python_tornado_implement.py)