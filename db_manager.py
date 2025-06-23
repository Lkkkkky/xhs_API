#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库Cookie管理器
从MySQL数据库获取小红书cookies
"""

import pymysql
import random
import logging
from typing import Optional, List, Dict
from datetime import datetime

class DatabaseCookieManager:
    def __init__(self, host: str = "gz-cdb-grqtft0j.sql.tencentcdb.com", 
                 port: int = 24238, 
                 database: str = "xhs_db", 
                 user: str = None, 
                 password: str = None):
        """
        初始化数据库连接
        
        Args:
            host: 数据库主机地址
            port: 数据库端口
            database: 数据库名称
            user: 数据库用户名
            password: 数据库密码
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        
        
    def get_connection(self):
        """获取数据库连接"""
        try:
            connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except Exception as e:
            print.error(f"数据库连接失败: {e}")
            return None
    
    def get_all_cookies(self) -> List[Dict]:
        """获取所有可用的cookies"""
        connection = self.get_connection()
        if not connection:
            return []
            
        try:
            with connection.cursor() as cursor:
                # 查询所有有效的cookies
                sql = """
                SELECT id, val as cookie_string, is_survive, create_time 
                FROM xhs_cookies 
                WHERE is_survive = 1 
                ORDER BY id ASC
                """
                cursor.execute(sql)
                cookies = cursor.fetchall()
                print(f"从数据库获取到 {len(cookies)} 个可用cookies")
                return cookies
        except Exception as e:
            print.error(f"获取cookies失败: {e}")
            return []
        finally:
            connection.close()
    
    def get_random_cookie(self) -> Optional[str]:
        """随机获取一个可用的cookie"""
        cookies = self.get_all_cookies()
        if not cookies:
            print("没有可用的cookies")
            return None
            
        # 随机选择一个cookie
        selected_cookie = random.choice(cookies)
        cookie_string = selected_cookie['cookie_string']
        
        # 更新最后使用时间
        self.update_last_used(selected_cookie['id'])
        
        print(f"随机选择cookie ID: {selected_cookie['id']}")
        return cookie_string
    
    def get_least_used_cookie(self) -> Optional[str]:
        """获取最少使用的cookie"""
        cookies = self.get_all_cookies()
        if not cookies:
            print("没有可用的cookies")
            return None
            
        # 选择最少使用的cookie（按last_used排序，第一个就是最少使用的）
        selected_cookie = cookies[0]
        cookie_string = selected_cookie['cookie_string']
        
        # 更新最后使用时间
        self.update_last_used(selected_cookie['id'])
        
        print(f"选择最少使用的cookie ID: {selected_cookie['id']}")
        return cookie_string
    
    def update_last_used(self, cookie_id: int) -> bool:
        """更新cookie的最后使用时间"""
        connection = self.get_connection()
        if not connection:
            return False
            
        try:
            with connection.cursor() as cursor:
                # 注意：原表结构没有last_used字段，这里只记录日志
                # 如果需要记录使用时间，需要在表中添加相应字段
                pass
                connection.commit()
                return True
        except Exception as e:
            print.error(f"更新cookie使用时间失败: {e}")
            return False
        finally:
            connection.close()
    
    def mark_cookie_status(self,status:int, cookie_string: str) -> bool:
        """根据cookie字符串标记cookie为无效
        Args:
            status (int): 0表示无效，1表示有效
            cookie_string (str): 需要标记的cookie字符串
        Returns:
            bool: 标记成功返回True，失败返回False
        """
        connection = self.get_connection()
        if not connection:
            return False
            
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE xhs_cookies 
                SET is_survive = %s 
                WHERE val = %s
                """
                cursor.execute(sql, (status,cookie_string,))
                affected_rows = cursor.rowcount
                connection.commit()
                
                if affected_rows > 0:
                    if status == 0:
                        print(f"成功标记cookie为无效，影响行数: {affected_rows}")
                        return True
                    if status == 1:
                        print(f"成功标记cookie为有效，影响行数: {affected_rows}")
                        return True
                else:
                    print("未找到匹配的cookie")
                    return False
        except Exception as e:
            print.error(f"根据cookie字符串标记无效失败: {e}")
            return False
        finally:
            connection.close()
    
    def add_cookie(self, cookie_string: str, status: str = 'active') -> bool:
        """添加新的cookie到数据库"""
        connection = self.get_connection()
        if not connection:
            return False
            
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO xhs_cookies (val, is_survive) 
                VALUES (%s, %s)
                """
                survive_status = 1 if status == 'active' else 0
                cursor.execute(sql, (cookie_string, survive_status))
                connection.commit()
                print("成功添加新cookie到数据库")
                return True
        except Exception as e:
            print.error(f"添加cookie失败: {e}")
            return False
        finally:
            connection.close()
    
    def get_cookie_count(self) -> int:
        """获取可用cookie数量"""
        connection = self.get_connection()
        if not connection:
            return 0
            
        try:
            with connection.cursor() as cursor:
                sql = "SELECT COUNT(*) as count FROM xhs_cookies WHERE is_survive = 1"
                cursor.execute(sql)
                result = cursor.fetchone()
                return result['count'] if result else 0
        except Exception as e:
            print.error(f"获取cookie数量失败: {e}")
            return 0
        finally:
            connection.close()
    
    def save_to_monitor_comments(self, merged_data):
            """将合并后的数据保存到monitor_comments数据库表中
            Args:
                merged_data (list): merge_note_info_with_comments函数返回的合并数据

                
            Returns:
                bool: 保存是否成功
            """
            try:
                connection = self.get_connection()
                with connection.cursor() as cursor:
                    # 准备插入SQL语句
                    insert_sql = """
                    INSERT INTO monitor_comments (
                        keyword, title, note_author, userInfo, content, 
                        likes, collects, comments, note_url, collect_time, 
                        note_time, note_location, note_type, comment_location, 
                        comment_id, comment_author
                    ) VALUES (
                        %(keyword)s, %(title)s, %(note_author)s, %(userInfo)s, %(content)s,
                        %(likes)s, %(collects)s, %(comments)s, %(note_url)s, %(collect_time)s,
                        %(note_time)s, %(note_location)s, %(note_type)s, %(comment_location)s,
                        %(comment_id)s, %(comment_author)s
                    )
                    """
                    
                    # 批量插入数据
                    for item in merged_data:
                        # 处理时间格式
                        collect_time = item.get('collect_time')
                        note_time = item.get('note_time')
                        
                        # 如果时间是字符串格式，转换为datetime对象
                        if isinstance(collect_time, str):
                            try:
                                collect_time = datetime.strptime(collect_time, "%Y-%m-%d %H:%M:%S")
                            except:
                                collect_time = datetime.now()
                        
                        if isinstance(note_time, str):
                            try:
                                note_time = datetime.strptime(note_time, "%Y-%m-%d %H:%M:%S")
                            except:
                                note_time = datetime.now()
                        
                        # 准备插入数据
                        data = {
                            'keyword': item.get('keyword', ''),
                            'title': item.get('title', ''),
                            'note_author': item.get('note_author', ''),
                            'userInfo': item.get('userInfo', ''),
                            'content': item.get('content', ''),
                            'likes': item.get('likes', 0),
                            'collects': item.get('collects', 0),
                            'comments': item.get('comments', 0),
                            'note_url': item.get('note_url', ''),
                            'collect_time': collect_time,
                            'note_time': note_time,
                            'note_location': item.get('note_location', ''),
                            'note_type': item.get('note_type', ''),
                            'comment_location': item.get('comment_location', ''),
                            'comment_id': item.get('comment_id', ''),
                            'comment_author': item.get('commenter_nickname', '')
                        }
                        
                        cursor.execute(insert_sql, data)
                    
                    # 提交事务
                    connection.commit()
                    print(f"成功保存 {len(merged_data)} 条数据到 monitor_comments 表")
                    return True
                    
            except Exception as e:
                print(f"保存数据到数据库时出错: {e}")
                if 'connection' in locals():
                    connection.rollback()
                return False
                
            finally:
                if 'connection' in locals():
                    connection.close()

    def test_connection(self) -> bool:
        """测试数据库连接"""
        connection = self.get_connection()
        if connection:
            connection.close()
            print("数据库连接测试成功")
            return True
        else:
            print.error("数据库连接测试失败")
            return False

# 创建数据库表的SQL语句（仅供参考）
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS xhs_cookies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cookie_string TEXT NOT NULL,
    status ENUM('active', 'invalid', 'expired') DEFAULT 'active',
    last_used DATETIME NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    INDEX idx_status (status),
    INDEX idx_last_used (last_used)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

if __name__ == "__main__":
    # 测试代码
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # 从环境变量获取数据库配置
    db_manager = DatabaseCookieManager(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    # 测试连接
    if db_manager.test_connection():
        print("数据库连接成功")
        
        # 获取cookie数量
        count = db_manager.get_cookie_count()
        print(f"可用cookie数量: {count}")
        
        # 获取随机cookie
        cookie = db_manager.get_random_cookie()
        if cookie:
            print(f"获取到cookie: {cookie[:50]}...")
        else:
            print("没有可用的cookie")
    else:
        print("数据库连接失败")