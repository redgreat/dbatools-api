-- 修复数据库权限脚本
-- 解决 "permission denied for schema public" 错误

-- 连接到目标数据库
\c dbatools;

-- 授予用户在public schema中的所有权限
GRANT ALL PRIVILEGES ON SCHEMA public TO user_dba;

-- 授予用户在public schema中创建表的权限
GRANT CREATE ON SCHEMA public TO user_dba;

-- 授予用户对现有表的所有权限
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO user_dba;

-- 授予用户对现有序列的所有权限
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO user_dba;

-- 设置默认权限，确保新创建的对象也有相应权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO user_dba;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO user_dba;

-- 如果需要，也可以让用户成为数据库的所有者
-- ALTER DATABASE dbatools OWNER TO user_dba;

-- 验证权限设置
\du user_dba
\l+ dbatools

COMMIT;