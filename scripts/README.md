# 数据库权限问题解决方案

## 问题描述

在运行 `python main.py` 时遇到以下错误：
```
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.InsufficientPrivilege) permission denied for schema public
```

## 问题原因

当前数据库用户 `user_dba` 没有在 `public` schema 中创建表的权限。这通常发生在：
1. 数据库用户权限配置不完整
2. PostgreSQL 15+ 版本默认限制了 public schema 的权限

## 解决方案

### 方案一：使用自动化脚本（推荐）

1. 在项目根目录运行：
```powershell
.\scripts\fix_permissions.ps1
```

2. 按提示输入PostgreSQL管理员密码

3. 脚本执行完成后，重新运行：
```bash
python main.py
```

### 方案二：手动执行SQL

1. 使用管理员账户连接数据库：
```bash
psql -h 124.70.167.242 -p 5432 -U postgres -d dbatools
```

2. 执行以下SQL命令：
```sql
-- 授予用户在public schema中的所有权限
GRANT ALL PRIVILEGES ON SCHEMA public TO user_dba;

-- 授予用户在public schema中创建表的权限
GRANT CREATE ON SCHEMA public TO user_dba;

-- 授予用户对现有表的所有权限
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO user_dba;

-- 授予用户对现有序列的所有权限
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO user_dba;

-- 设置默认权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO user_dba;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO user_dba;
```

### 方案三：修改配置使用超级用户（临时方案）

如果无法修改权限，可以临时修改 `.env` 文件中的数据库连接：
```env
DATABASE_URL=postgresql://postgres:your_password@124.70.167.242:5432/dbatools
```

## 验证解决方案

权限修复后，运行以下命令验证：
```bash
python main.py
```

如果看到类似以下输出，说明数据库表创建成功：
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 文件说明

- `fix_database_permissions.sql`: SQL权限修复脚本
- `fix_permissions.ps1`: PowerShell自动化执行脚本
- `README.md`: 本说明文档