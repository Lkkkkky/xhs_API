import requests
import json

def test_search_comments_by_keyword():
    """测试修改后的search_comments_by_keyword功能"""
    url = "http://localhost:8000/search_comments_by_keyword"
    
    # 测试数据
    data = {
        "keyword": "美食",
        "num": 5  # 设置较小的数量便于测试
    }
    
    try:
        print(f"正在测试搜索评论功能...")
        print(f"请求URL: {url}")
        print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(url, json=data, timeout=60)  # 增加超时时间
        
        print(f"\n响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"响应数据类型: {type(result)}")
            
            if isinstance(result, dict) and 'data' in result:
                comments_data = result['data']
                print(f"返回的评论数量: {len(comments_data)}")
                print(f"成功状态: {result.get('success', False)}")
                print(f"总计数量: {result.get('count', 0)}")
                
                if comments_data:
                    print(f"\n前3条评论示例:")
                    for i, comment in enumerate(comments_data[:3]):
                        print(f"评论{i+1}: {json.dumps(comment, ensure_ascii=False, indent=2)}")
                else:
                    print("返回的评论列表为空")
            else:
                print(f"返回数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
        else:
            print(f"请求失败: {response.text}")
            
    except requests.exceptions.Timeout:
        print("请求超时")
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

if __name__ == "__main__":
    test_search_comments_by_keyword()