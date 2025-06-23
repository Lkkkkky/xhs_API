#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试mark_cookie_invalid_by_string函数
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_manager import DatabaseCookieManager
from dotenv import load_dotenv

def test_mark_cookie_invalid_by_string():
    """测试根据cookie字符串标记cookie为无效的功能"""
    print("=== 测试mark_cookie_invalid_by_string函数 ===")
    
    # 加载环境变量
    load_dotenv()
    
    # 获取数据库配置
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    
    if not db_user or not db_password:
        print("错误: 数据库用户名或密码未配置")
        return
    
    # 创建数据库管理器
    db_manager = DatabaseCookieManager(
        user=db_user,
        password=db_password
    )
    
    # 测试数据库连接
    print("\n1. 测试数据库连接...")
    if not db_manager.test_connection():
        print("数据库连接失败")
        return
    print("数据库连接成功")
    
    # 获取当前可用cookie数量
    print("\n2. 获取当前可用cookie数量...")
    count_before = db_manager.get_cookie_count()
    print(f"当前可用cookie数量: {count_before}")
    
    if count_before == 0:
        print("没有可用的cookie进行测试")
        return
    
    # 获取一个随机cookie用于测试
    print("\n3. 获取一个cookie用于测试...")
    test_cookie = db_manager.get_random_cookie()
    if not test_cookie:
        print("无法获取测试cookie")
        return
    print(f"测试cookie: {test_cookie[:50]}...")
    
    # 测试mark_cookie_invalid_by_string函数
    print("\n4. 测试mark_cookie_invalid_by_string函数...")
    result = db_manager.mark_cookie_invalid_by_string(test_cookie)
    
    if result:
        print("✓ 成功标记cookie为无效")
    else:
        print("✗ 标记cookie失效失败")
    
    # 验证cookie数量是否减少
    print("\n5. 验证cookie数量变化...")
    count_after = db_manager.get_cookie_count()
    print(f"标记后可用cookie数量: {count_after}")
    
    if count_after == count_before - 1:
        print("✓ cookie数量正确减少了1个")
    else:
        print(f"✗ cookie数量变化异常，预期减少1个，实际变化: {count_before - count_after}")
    
    # 测试标记不存在的cookie
    print("\n6. 测试标记不存在的cookie...")
    fake_cookie = "fake_cookie_string_that_does_not_exist"
    result = db_manager.mark_cookie_invalid_by_string(fake_cookie)
    
    if not result:
        print("✓ 正确处理了不存在的cookie")
    else:
        print("✗ 不应该成功标记不存在的cookie")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_mark_cookie_invalid_by_string()