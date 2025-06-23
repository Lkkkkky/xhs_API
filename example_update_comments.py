# -*- coding: utf-8 -*-
"""
示例：使用update_note_comments_count函数更新笔记评论数量
"""

import os
from dotenv import load_dotenv
from db_manager import DatabaseCookieManager

def example_update_comments_count():
    """演示如何使用update_note_comments_count函数"""
    
    # 加载环境变量
    load_dotenv()
    
    # 初始化数据库管理器
    db_manager = DatabaseCookieManager(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    # 测试数据库连接
    if not db_manager.test_connection():
        print("❌ 数据库连接失败，无法继续操作")
        return
    
    print("\n=== 更新笔记评论数量示例 ===")
    
    # 示例1：更新单个笔记的评论数量
    note_url = "https://www.xiaohongshu.com/explore/12345"  # 替换为实际的笔记URL
    new_comment_count = 150  # 新的评论数量
    
    print(f"\n📝 正在更新笔记评论数量...")
    print(f"   笔记URL: {note_url}")
    print(f"   新评论数量: {new_comment_count}")
    
    success = db_manager.update_note_comments_count(note_url, new_comment_count)
    
    if success:
        print("\n✅ 评论数量更新成功！")
        
        # 验证更新结果
        current_count = db_manager.get_note_comments_count(note_url)
        print(f"\n🔍 验证更新结果:")
        print(f"   当前评论数量: {current_count}")
        
        if current_count == new_comment_count:
            print("✅ 验证成功：评论数量已正确更新")
        else:
            print("⚠️  验证失败：评论数量不匹配")
    else:
        print("\n❌ 评论数量更新失败")

def example_batch_update_comments():
    """演示批量更新多个笔记的评论数量"""
    
    # 加载环境变量
    load_dotenv()
    
    # 初始化数据库管理器
    db_manager = DatabaseCookieManager(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    print("\n=== 批量更新笔记评论数量示例 ===")
    
    # 批量更新数据（笔记URL和对应的新评论数量）
    update_data = [
        ("https://www.xiaohongshu.com/explore/12345", 150),
        ("https://www.xiaohongshu.com/explore/67890", 89),
        ("https://www.xiaohongshu.com/explore/11111", 234),
    ]
    
    success_count = 0
    failed_count = 0
    
    for note_url, comment_count in update_data:
        print(f"\n📝 更新笔记: {note_url}")
        print(f"   新评论数量: {comment_count}")
        
        success = db_manager.update_note_comments_count(note_url, comment_count)
        
        if success:
            success_count += 1
        else:
            failed_count += 1
    
    print(f"\n📊 批量更新结果统计:")
    print(f"   成功更新: {success_count} 条")
    print(f"   更新失败: {failed_count} 条")
    print(f"   总计处理: {len(update_data)} 条")

def example_update_with_validation():
    """演示带验证的评论数量更新"""
    
    # 加载环境变量
    load_dotenv()
    
    # 初始化数据库管理器
    db_manager = DatabaseCookieManager(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    print("\n=== 带验证的评论数量更新示例 ===")
    
    note_url = "https://www.xiaohongshu.com/explore/12345"  # 替换为实际的笔记URL
    new_comment_count = 200
    
    # 获取更新前的评论数量
    old_count = db_manager.get_note_comments_count(note_url)
    print(f"\n📊 更新前评论数量: {old_count}")
    
    # 执行更新
    print(f"\n📝 正在更新为: {new_comment_count}")
    success = db_manager.update_note_comments_count(note_url, new_comment_count)
    
    if success:
        # 获取更新后的评论数量
        new_count = db_manager.get_note_comments_count(note_url)
        print(f"\n📊 更新后评论数量: {new_count}")
        
        # 计算变化量
        change = new_count - old_count
        if change > 0:
            print(f"📈 评论数量增加了: {change}")
        elif change < 0:
            print(f"📉 评论数量减少了: {abs(change)}")
        else:
            print(f"➡️  评论数量无变化")
    else:
        print("\n❌ 更新失败")

if __name__ == "__main__":
    print("🚀 开始演示update_note_comments_count函数的使用")
    
    # 运行示例
    try:
        # 示例1：基本更新
        example_update_comments_count()
        
        # 示例2：批量更新
        example_batch_update_comments()
        
        # 示例3：带验证的更新
        example_update_with_validation()
        
    except Exception as e:
        print(f"\n❌ 运行示例时出错: {e}")
    
    print("\n✅ 示例演示完成")