#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库中URL格式的脚本
"""

import os
from dotenv import load_dotenv
from db_manager import DatabaseCookieManager
import urllib.parse

def check_url_formats():
    """检查数据库中的URL格式"""
    
    # 加载环境变量
    load_dotenv()
    
    # 初始化数据库管理器
    db_manager = DatabaseCookieManager(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    connection = db_manager.get_connection()
    if not connection:
        print("❌ 数据库连接失败")
        return
    
    try:
        with connection.cursor() as cursor:
            # 查询前10条URL记录
            cursor.execute("SELECT note_url FROM xhs_notes LIMIT 10")
            results = cursor.fetchall()
            
            print("=== 数据库中存储的URL格式 ===")
            for i, (url,) in enumerate(results, 1):
                print(f"\nURL {i}:")
                print(f"原始: {url}")
                print(f"长度: {len(url)}")
                
                # 检查是否包含特殊字符
                if '?' in url:
                    print("包含查询参数: ✓")
                if '%' in url:
                    print("包含URL编码: ✓")
                if '&' in url:
                    print("包含多个参数: ✓")
                    
    except Exception as e:
        print(f"❌ 查询失败: {e}")
    finally:
        connection.close()

def test_url_matching():
    """测试URL匹配问题"""
    
    # 用户提供的URL
    user_url = "https://www.xiaohongshu.com/discovery/item/684fd43f000000002100143d?app_platform=android&ignoreEngage=true&app_version=8.72.0&share_from_user_hidden=true&xsec_source=app_share&type=normal&xsec_token=CB-ePnQKXDGTmKxrd6ndNn7rD5J3vw6wnfXwnQ_kDP6w4%3D&author_share=1&xhsshare=CopyLink&shareRedId=OD4zQUg9OkI2NzUyOTgwNjY7OTg7OT5B&apptime=1750669931&share_id=28f821f2659148538ec4fec718c559e5&share_channel=copy_link"
    
    print("\n=== URL匹配测试 ===")
    print(f"用户URL: {user_url}")
    print(f"URL长度: {len(user_url)}")
    
    # 提取核心ID
    if '/item/' in user_url:
        item_id = user_url.split('/item/')[1].split('?')[0]
        print(f"提取的ID: {item_id}")
    
    # URL解码测试
    decoded_url = urllib.parse.unquote(user_url)
    print(f"\n解码后URL: {decoded_url}")
    print(f"解码后长度: {len(decoded_url)}")
    
    # 检查数据库中是否有类似的URL
    load_dotenv()
    db_manager = DatabaseCookieManager(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    connection = db_manager.get_connection()
    if not connection:
        print("❌ 数据库连接失败")
        return
    
    try:
        with connection.cursor() as cursor:
            # 查找包含相同ID的URL
            if '/item/' in user_url:
                item_id = user_url.split('/item/')[1].split('?')[0]
                cursor.execute("SELECT note_url FROM xhs_notes WHERE note_url LIKE %s", (f"%{item_id}%",))
                results = cursor.fetchall()
                
                print(f"\n=== 数据库中包含ID '{item_id}' 的URL ===")
                if results:
                    for i, (url,) in enumerate(results, 1):
                        print(f"匹配 {i}: {url}")
                        # 比较差异
                        if url != user_url:
                            print(f"  差异: 数据库URL与用户URL不完全匹配")
                else:
                    print("❌ 未找到包含该ID的URL")
                    
    except Exception as e:
        print(f"❌ 查询失败: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    print("🔍 URL格式检查工具")
    print("=" * 50)
    
    # 检查数据库中的URL格式
    check_url_formats()
    
    # 测试URL匹配
    test_url_matching()