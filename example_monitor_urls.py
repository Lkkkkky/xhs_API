# -*- coding: utf-8 -*-
"""
示例：获取需要监控的URL列表
"""

import os
from dotenv import load_dotenv
from db_manager import DatabaseCookieManager

def example_get_monitor_urls():
    """示例：获取需要监控的URL列表"""
    
    # 加载环境变量
    load_dotenv()
    
    # 初始化数据库管理器
    db_manager = DatabaseCookieManager(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    # 用户邮箱（实际使用时从用户输入或配置文件获取）
    user_email = "user@example.com"  # 请替换为实际的用户邮箱
    
    try:
        # 测试数据库连接
        if not db_manager.test_connection():
            print("数据库连接失败，无法获取监控URL列表")
            return
        
        # 获取指定用户需要监控的URL列表
        print(f"正在获取用户 {user_email} 需要监控的URL列表...")
        monitor_urls = db_manager.get_monitor_urls(user_email)
        
        if monitor_urls:
            print(f"\n成功获取 {len(monitor_urls)} 个需要监控的URL:")
            print("-" * 50)
            for i, url in enumerate(monitor_urls, 1):
                print(f"{i}. {url}")
            print("-" * 50)
            
            # 可以进一步处理这些URL，比如启动监控任务
            print("\n可以使用这些URL进行后续的监控操作...")
            
        else:
            print(f"用户 {user_email} 没有找到需要监控的URL")
            
    except Exception as e:
        print(f"获取监控URL列表时出错: {e}")

def example_with_monitoring_logic():
    """示例：结合监控逻辑使用URL列表"""
    
    # 加载环境变量
    load_dotenv()
    
    # 初始化数据库管理器
    db_manager = DatabaseCookieManager(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    # 用户邮箱
    user_email = "monitor@example.com"  # 请替换为实际的用户邮箱
    
    try:
        # 获取指定用户的监控URL列表
        monitor_urls = db_manager.get_monitor_urls(user_email)
        
        if not monitor_urls:
            print(f"用户 {user_email} 没有需要监控的URL")
            return
        
        print(f"开始为用户 {user_email} 监控 {len(monitor_urls)} 个URL...")
        
        # 模拟监控逻辑
        for url in monitor_urls:
            print(f"\n正在监控: {url}")
            
            # 这里可以调用相关的API函数
            # 例如：
            # 1. 获取笔记信息
            # 2. 获取评论列表
            # 3. 合并数据
            # 4. 保存到monitor_comments表
            
            # 模拟处理
            print(f"  - 获取笔记信息...")
            print(f"  - 获取评论列表...")
            print(f"  - 保存监控数据...")
            print(f"  - 完成监控: {url}")
        
        print(f"\n用户 {user_email} 的所有URL监控完成！")
        
    except Exception as e:
        print(f"监控过程中出错: {e}")

if __name__ == "__main__":
    print("=== 获取监控URL列表示例 ===")
    
    print("\n1. 基础示例：获取监控URL列表")
    example_get_monitor_urls()
    
    print("\n" + "=" * 60)
    print("\n2. 进阶示例：结合监控逻辑")
    example_with_monitoring_logic()