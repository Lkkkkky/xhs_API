#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask API 使用示例
演示如何调用监控任务API接口
"""

import requests
import json
from datetime import datetime

# API服务器配置
API_BASE_URL = "http://localhost:5000"

def test_health_check():
    """
    测试健康检查接口
    """
    print("=== 测试健康检查接口 ===")
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def test_monitor_api(email, keyword):
    """
    测试监控任务API接口
    
    Args:
        email (str): 用户邮箱
        keyword (str): 监控关键词
    """
    print(f"\n=== 测试监控任务API - Email: {email}, Keyword: {keyword} ===")
    
    # 准备请求数据
    data = {
        "email": email,
        "keyword": keyword
    }
    
    try:
        # 发送POST请求
        response = requests.post(
            f"{API_BASE_URL}/api/monitor",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"API调用失败: {e}")
        return False

def test_invalid_requests():
    """
    测试无效请求的处理
    """
    print("\n=== 测试无效请求处理 ===")
    
    # 测试1: 缺少email参数
    print("\n1. 测试缺少email参数:")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/monitor",
            json={"keyword": "测试关键词"},
            headers={'Content-Type': 'application/json'}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试2: 缺少keyword参数
    print("\n2. 测试缺少keyword参数:")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/monitor",
            json={"email": "test@example.com"},
            headers={'Content-Type': 'application/json'}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试3: 无效邮箱格式
    print("\n3. 测试无效邮箱格式:")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/monitor",
            json={"email": "invalid-email", "keyword": "测试关键词"},
            headers={'Content-Type': 'application/json'}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试4: 非JSON请求
    print("\n4. 测试非JSON请求:")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/monitor",
            data="email=test@example.com&keyword=测试关键词",
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {e}")

def test_api_info():
    """
    测试API信息接口
    """
    print("\n=== 测试API信息接口 ===")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"API信息获取失败: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("🧪 Flask API 测试")
    print("=" * 50)
    print(f"API服务器: {API_BASE_URL}")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 测试API信息
    test_api_info()
    
    # 测试健康检查
    if not test_health_check():
        print("\n❌ 健康检查失败，请确保API服务器正在运行")
        print("启动命令: python app.py")
        return
    
    # 测试无效请求
    test_invalid_requests()
    
    # 测试正常的监控任务（使用示例数据）
    print("\n" + "=" * 50)
    print("📝 注意: 以下测试需要有效的数据库配置和监控URL")
    print("如果没有配置，测试可能会失败")
    print("=" * 50)
    
    # 测试监控任务API
    test_monitor_api("luyao-operate@lucy.ai", "测试关键词")
    
    print("\n" + "=" * 50)
    print("🎉 API测试完成")
    print("=" * 50)

if __name__ == "__main__":
    main()