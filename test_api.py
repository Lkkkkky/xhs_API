#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书API FastAPI服务测试脚本

使用示例：
python test_api.py
"""

import requests
import json
from typing import Dict, Any

# API基础URL
BASE_URL = "http://localhost:8000"

def test_api_health() -> Dict[str, Any]:
    """测试API健康检查"""
    print("\n=== 测试API健康检查 ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return result
    except Exception as e:
        print(f"请求失败: {e}")
        return {}

def test_api_root() -> Dict[str, Any]:
    """测试根路径"""
    print("\n=== 测试根路径 ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return result
    except Exception as e:
        print(f"请求失败: {e}")
        return {}

def test_get_comments(note_url: str = "test_url") -> Dict[str, Any]:
    """测试获取评论接口"""
    print("\n=== 测试获取评论接口 ===")
    data = {
        "note_url": note_url,
        "cursor": ""
    }
    try:
        response = requests.post(f"{BASE_URL}/comments", json=data)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return result
    except Exception as e:
        print(f"请求失败: {e}")
        return {}

def test_search_notes(keyword: str = "美食", num: int = 5) -> Dict[str, Any]:
    """测试搜索笔记接口"""
    print("\n=== 测试搜索笔记接口 ===")
    data = {
        "keyword": keyword,
        "num": num
    }
    try:
        response = requests.post(f"{BASE_URL}/search", json=data)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return result
    except Exception as e:
        print(f"请求失败: {e}")
        return {}

def test_get_note_info(note_url: str = "test_url") -> Dict[str, Any]:
    """测试获取笔记信息接口"""
    print("\n=== 测试获取笔记信息接口 ===")
    data = {
        "note_url": note_url
    }
    try:
        response = requests.post(f"{BASE_URL}/note-info", json=data)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return result
    except Exception as e:
        print(f"请求失败: {e}")
        return {}

def test_monitor_comments(note_url: str = "test_url", 
                         user_info: str = "test_user", keyword: str = "测试") -> Dict[str, Any]:
    """测试监控评论接口"""
    print("\n=== 测试监控评论接口 ===")
    data = {
        "note_url": note_url,
        "user_info": user_info,
        "keyword": keyword,
        "interval": 60
    }
    try:
        response = requests.post(f"{BASE_URL}/monitor", json=data)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return result
    except Exception as e:
        print(f"请求失败: {e}")
        return {}

def test_reply_comment(note_url: str = "test_url",
                      comment_id: str = "test_comment_id", content: str = "测试回复") -> Dict[str, Any]:
    """测试回复评论接口"""
    print("\n=== 测试回复评论接口 ===")
    data = {
        "note_url": note_url,
        "comment_id": comment_id,
        "content": content
    }
    try:
        response = requests.post(f"{BASE_URL}/reply", json=data)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return result
    except Exception as e:
        print(f"请求失败: {e}")
        return {}

def main():
    """运行所有测试"""
    print("开始测试 FastAPI 服务...")
    
    # 测试基础接口
    test_api_health()
    test_api_root()
    
    # 测试业务接口（使用示例数据）
    test_get_comments()
    test_search_notes()
    test_get_note_info()
    test_monitor_comments()
    test_reply_comment()
    
    print("\n=== 测试完成 ===")
    print("注意：业务接口需要有效的数据库配置和真实的URL才能正常工作")

if __name__ == "__main__":
    main()