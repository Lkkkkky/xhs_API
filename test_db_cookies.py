#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据库Cookie管理器
"""

import os
import sys
from dotenv import load_dotenv
from db_manager import DatabaseCookieManager
from xhs_utils.common_util import load_env

def test_database_connection():
    """测试数据库连接"""
    print("=== 测试数据库连接 ===")
    
    load_dotenv()
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    
    if not db_user or not db_password:
        print("❌ 数据库配置缺失，请在.env文件中设置DB_USER和DB_PASSWORD")
        return False
    
    db_manager = DatabaseCookieManager(
        user=db_user,
        password=db_password
    )
    
    if db_manager.test_connection():
        print("✅ 数据库连接成功")
        return True
    else:
        print("❌ 数据库连接失败")
        return False

def test_cookie_operations():
    """测试cookie操作"""
    print("\n=== 测试Cookie操作 ===")
    
    load_dotenv()
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    
    db_manager = DatabaseCookieManager(
        user=db_user,
        password=db_password
    )
    
    # 获取cookie数量
    count = db_manager.get_cookie_count()
    print(f"📊 可用cookie数量: {count}")
    
    if count == 0:
        print("⚠️  数据库中没有可用的cookies")
        return
    
    # 获取所有cookies
    cookies = db_manager.get_all_cookies()
    print(f"📋 获取到 {len(cookies)} 个cookies:")
    for i, cookie in enumerate(cookies[:3]):  # 只显示前3个
        print(f"   {i+1}. ID: {cookie['id']}, Is Survive: {cookie['is_survive']}, Create Time: {cookie['create_time']}")
    
    # 获取随机cookie
    print("\n🎲 获取随机cookie:")
    random_cookie = db_manager.get_random_cookie()
    if random_cookie:
        print(f"   获取成功: {random_cookie[:50]}...")
    else:
        print("   获取失败")
    
    # 获取最少使用的cookie
    print("\n⏰ 获取最少使用的cookie:")
    least_used_cookie = db_manager.get_least_used_cookie()
    if least_used_cookie:
        print(f"   获取成功: {least_used_cookie[:50]}...")
    else:
        print("   获取失败")

def test_load_env_function():
    """测试修改后的load_env函数"""
    print("\n=== 测试load_env函数 ===")
    
    cookies_str = load_env()
    if cookies_str:
        print(f"✅ 成功获取cookies: {cookies_str[:50]}...")
    else:
        print("❌ 获取cookies失败")

def main():
    """主测试函数"""
    print("🧪 数据库Cookie管理器测试")
    print("=" * 50)
    
    # 测试数据库连接
    if not test_database_connection():
        print("\n❌ 数据库连接失败，无法继续测试")
        return
    
    # 测试cookie操作
    test_cookie_operations()
    
    # 测试load_env函数
    test_load_env_function()
    
    print("\n" + "=" * 50)
    print("🎉 测试完成")

if __name__ == "__main__":
    main()