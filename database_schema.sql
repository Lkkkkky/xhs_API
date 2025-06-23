-- 小红书Cookie管理数据库表结构
-- 数据库: xhs_db
-- 主机: gz-cdb-grqtft0j.sql.tencentcdb.com:24238

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS xhs_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE xhs_db;

-- 小红书Cookie管理数据库表（用户实际表结构）
CREATE TABLE `xhs_cookies` ( 
    `id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key', 
    `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'Create Time', 
    `is_survive` int DEFAULT NULL COMMENT 'Cookie是否有效: 1=有效, 0=无效', 
    `val` text COMMENT 'Cookie字符串', 
    PRIMARY KEY (`id`) 
) ENGINE = InnoDB AUTO_INCREMENT = 2 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- 插入示例数据
INSERT INTO `xhs_cookies` (`val`, `is_survive`) VALUES
('a1=18e0ca70c46l1h6c9q0q; webId=xxx; web_session=xxx', 1),
('a1=28e0ca70c46l1h6c9q0q; webId=yyy; web_session=yyy', 1),
('a1=38e0ca70c46l1h6c9q0q; webId=zzz; web_session=zzz', 0);

-- 常用查询语句

-- 1. 查看所有有效的cookies
SELECT id, val, is_survive, create_time 
FROM xhs_cookies 
WHERE is_survive = 1 
ORDER BY id ASC;

-- 2. 查看cookie状态统计
SELECT 
    CASE 
        WHEN is_survive = 1 THEN '有效'
        WHEN is_survive = 0 THEN '无效'
        ELSE '未知'
    END as status,
    COUNT(*) as count
FROM xhs_cookies 
GROUP BY is_survive;

-- 3. 获取最早创建的有效cookie
SELECT id, val, create_time 
FROM xhs_cookies 
WHERE is_survive = 1 
ORDER BY id ASC 
LIMIT 1;

-- 4. 标记cookie为无效
-- UPDATE xhs_cookies SET is_survive = 0 WHERE id = ?;

-- 5. 添加新的cookie
-- INSERT INTO xhs_cookies (val, is_survive) VALUES (?, 1);

-- 6. 删除无效的cookies（可选，定期清理）
-- DELETE FROM xhs_cookies WHERE is_survive = 0 AND create_time < DATE_SUB(NOW(), INTERVAL 30 DAY);