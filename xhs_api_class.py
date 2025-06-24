import json
import time
import os
from pathlib import Path
from curl_cffi import requests
from urllib.parse import urlencode, urlparse, parse_qs
import csv
from datetime import datetime
from mimetypes import guess_extension
import math
import random
from xhs_utils.xhs_util import splice_str, generate_request_params, generate_x_b3_traceid, get_common_headers
from xhs_utils.url_converter import convert_discovery_to_explore_url

class XhsAPI():
    """小红书API类，封装了获取评论、搜索笔记等功能"""
    
    def __init__(self):
        """初始化XhsAPI类
        
        Args:
            
        """
        self.note_list = []
        
    def extract_url_params(self, url):
        """从URL中提取参数
        
        Args:
            url (str): 小红书笔记URL
            
        Returns:
            dict: 包含note_id、xsec_token、xsec_source的字典
        """
        parsed = urlparse(url)

        # 提取 note_id
        path_segments = parsed.path.strip("/").split("/")
        note_id = path_segments[1] if len(path_segments) >= 2 and path_segments[0] == "explore" else None

        # 提取查询参数
        query_params = parse_qs(parsed.query)
        params = {
            "note_id": note_id,
            "xsec_token": query_params.get("xsec_token", [""])[0],
            "xsec_source": query_params.get("xsec_source", [""])[0]
        }
        return params
  
    def get_comments(self, cookies_str, ori_url, cursor='',comments_list: list = []):
        """获取小红书笔记下的评论
        
        Args:
            ori_url (str): 笔记URL
            cursor (str): 分页游标，默认为空
        """
        # 生成加密参数
        if "discovery" in  ori_url:
            ori_url=convert_discovery_to_explore_url(ori_url)
            print(ori_url)
        note_params = self.extract_url_params(ori_url)
        uri = "/api/sns/web/v2/comment/page"
        params = {
            "note_id": note_params['note_id'],
            "cursor": cursor,
            "top_comment_id": "",
            "image_formats": "jpg,webp,avif",
            "xsec_token": note_params['xsec_token'],
        }
        
        # 使用硬编码的cookies字符串（与search_by_keyword相同的逻辑）
        
        
        headers, cookies, data = generate_request_params(cookies_str, uri, params)
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"

        response = requests.get(url, headers=headers, cookies=cookies, params=params).json()
        comments = response.get('data', {}).get('comments', [])
        
        print(f"成功获取{len(comments)}条评论")
        if response.get('code') == 0 :
            for comment in comments:
                format_dict = {
                    'content': comment.get('content', ''),  # 内容
                    'like_count': comment.get('like_count', 0),  # 点赞数
                    'nickname': comment.get('user_info', {}).get('nickname', ''),  # 昵称
                    'comment_id': comment.get('id', ''),  # 评论ID
                    'comment_location': comment.get('ip_location', ''),  # IP位置
                    'note_time': datetime.fromtimestamp(int(int(comment.get('create_time', ''))/1000)).strftime("%Y-%m-%d %H:%M:%S"),  # 笔记创建时间
                    
                }
                comments_list.append(format_dict)
                print(format_dict)
                
                
                # if comment.get('pictures'):
                #     for image_list in comment.get('pictures'):
                #         image_url = image_list.get('url_default', '')  # 获取图片链接
                #         self.download_image_with_date(image_url, date_format="%Y%m%d_%H%M%S")
        
                for sub_comment in comment['sub_comments']:  # 一级评论会自带一个子评论
                    format_dict = {
                        'content': sub_comment.get('content', ''),  # 内容
                        'like_count': sub_comment.get('like_count', 0),  # 点赞数
                        'nickname': sub_comment.get('user_info', {}).get('nickname', ''),  # 昵称
                        'comment_id': sub_comment.get('id', ''),  # 评论ID
                        'comment_location': sub_comment.get('ip_location', ''),  # IP位置
                        'note_time': datetime.fromtimestamp(int(int(sub_comment.get('create_time', ''))/1000)).strftime("%Y-%m-%d %H:%M:%S"),  # 笔记创建时间
                        
                    }
                    comments_list.append(format_dict)
                    print(format_dict)
                    
                if comment.get('sub_comment_has_more') == True:  # 自带的子评论是否还可展开
                    time.sleep(2)
                    self.get_sub_comments(
                        cookies_str,
                        comment.get('note_id', note_params['note_id']),
                        comment.get('id', ''),
                        comment.get('sub_comment_cursor', ''),
                        note_params['xsec_token'],
                        comments_list
                    )
            
            if response.get('data').get('has_more') == True:  # 是否有下一页
                new_cursor = response.get('data', {}).get('cursor', '')
                self.get_comments(cookies_str,ori_url, new_cursor,comments_list)
            return comments_list   
        else:
            print(f"获取评论失败，错误代码: {response.get('code')}, 错误信息: {response.get('message')}")
            print('尝试更换cookies')
            # 这里可以添加更换cookies的逻辑
            return False
    def get_sub_comments(self, cookies_str, note_id, root_comment_id, cursor, xsec_token,comments_list: list = []):
        """获取小红书笔记的二级评论
        
        Args:
            note_id (str): 笔记ID
            root_comment_id (str): 根评论ID
            cursor (str): 分页游标
            xsec_token (str): 安全令牌
        """
        # 生成加密参数
        uri = "/api/sns/web/v2/comment/sub/page"
        params = {
            "note_id": note_id,
            "root_comment_id": root_comment_id,
            "num": "10",
            "cursor": cursor,
            "image_formats": "jpg,webp,avif",
            "top_comment_id": "",
            "xsec_token": xsec_token
        }
        splice_api = splice_str(uri, params)
        headers, cookies, data = generate_request_params(cookies_str, splice_api)
        # url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        
        
        response = requests.get("https://edith.xiaohongshu.com"+splice_api, headers=headers, cookies=cookies).json()
        print(f"获取二级评论成功，共{len(response.get('data', {}).get('comments', []))}条")
        
        comments = response.get('data', {}).get('comments', [])
        for comment in comments:
            format_dict = {
                'content': comment.get('content', ''),  # 内容
                'like_count': comment.get('like_count', 0),  # 点赞数
                'nickname': comment.get('user_info', {}).get('nickname', ''),  # 昵称
                'comment_id': comment.get('id', ''),  # 评论ID,
                'comment_location': comment.get('ip_location', ''),  # IP位置
                'note_time': datetime.fromtimestamp(int(int(comment.get('create_time', ''))/1000)).strftime("%Y-%m-%d %H:%M:%S"),  # 笔记创建时间
                
            }
            
            comments_list.append(format_dict)
            print(format_dict)
            
            if comment.get('pictures'):
                for image_list in comment.get('pictures'):
                    image_url = image_list.get('url_default', '')  # 获取图片链接
                    self.download_image_with_date(image_url, date_format="%Y%m%d_%H%M%S")
        
        time.sleep(2)
        # 如果还有更多评论，继续获取
        # print(f'二级评论response{response}')
        if response and response.get('data').get('has_more') == True:
            new_sub_cursor = response.get('data', {}).get('cursor', '')
            self.get_sub_comments(cookies_str,note_id, root_comment_id, new_sub_cursor, xsec_token,comments_list)
    
    def download_image_with_date(self, url, save_dir="images", date_format="%Y%m%d_%H%M%S", 
                                include_original_name=False, avoid_overwrite=True):
        """下载图片并按日期命名
        
        Args:
            url (str): 图片URL
            save_dir (str): 保存目录
            date_format (str): 日期格式
            include_original_name (bool): 是否包含原文件名
            avoid_overwrite (bool): 是否避免覆盖同名文件
            
        Returns:
            bool: 下载是否成功
        """
        try:
            os.makedirs(save_dir, exist_ok=True)
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()

            # 生成基础日期部分
            timestamp = datetime.now().strftime(date_format)

            # 处理原始文件名（可选）
            original_name = ""
            if include_original_name:
                original_name = os.path.splitext(os.path.basename(url))[0]  # 去扩展名
                original_name = f"_{original_name}" if original_name else ""

            # 确定扩展名
            content_type = response.headers.get("Content-Type", "")
            ext = guess_extension(content_type.split(";")[0].strip()) or ".jpg"

            # 组合基础文件名
            base_filename = f"{timestamp}{original_name}{ext}"
            save_path = os.path.join(save_dir, base_filename)

            # 防止文件覆盖（可选）
            if avoid_overwrite:
                counter = 1
                while os.path.exists(save_path):
                    name, extension = os.path.splitext(base_filename)
                    save_path = os.path.join(save_dir, f"{name}_{counter}{extension}")
                    counter += 1

            # 保存文件
            with open(save_path, "wb") as f:
                for chunk in response.iter_content():
                    if chunk:
                        f.write(chunk)

            print(f"保存成功: {save_path}")
            return True

        except Exception as e:
            print(f"错误: {str(e)}")
            return False
    
    def search_comment_by_keyword(self, cookies_str,keyword, num):
        """根据关键词搜索的笔记下面的评论
        
        Args:
            keyword (str): 搜索关键词
            num (int): 搜索数量
        """
        for p in range(1000):
            uri = "/api/sns/web/v1/search/notes"
            params = {
                "keyword": keyword,
                "page": 1,
                "page_size": 20,
                "search_id": generate_x_b3_traceid(21),
                "sort": "general",
                "note_type": 0,
                "ext_flags": [],
                "filters": [
                    {
                        "tags": [
                            "general"
                        ],
                        "type": "sort_type"
                    },
                    {
                        "tags": [
                            "不限"
                        ],
                        "type": "filter_note_type"
                    },
                    {
                        "tags": [
                            "不限"
                        ],
                        "type": "filter_note_time"
                    },
                    {
                        "tags": [
                            "不限"
                        ],
                        "type": "filter_note_range"
                    },
                    {
                        "tags": [
                            "不限"
                        ],
                        "type": "filter_pos_distance"
                    }
                ],
                "geo": "",
                "image_formats": [
                    "jpg",
                    "webp",
                    "avif"
                ]
            }
            
            final_uri = f"{uri}?{params}"
            print(final_uri)
            
            # 这里需要实现具体的搜索逻辑
            # 暂时使用硬编码的cookies字符串
            headers, cookies, data = generate_request_params(cookies_str, uri, params)
            url = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
            response = requests.post(url, headers=headers, cookies=cookies, data=data.encode('utf-8')).json()
            for item in response.get('data', {}).get('items', []):
                note_id = item.get('id')
                xsec_token = item.get('xsec_token')
                if item.get('note_card'):
                    format_dict = {
                        'title': item.get('note_card').get('display_title'),
                        'note_id': note_id,
                        'xsec_token': xsec_token,
                        'url': f'https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}&xsec_source=pc_feed'
                    }
                    print(format_dict)
                    self.note_list.append(format_dict['url'])
                    if len(self.note_list) >= num:
                        self.get_comments_by_search(cookies_str)
                        return

    def get_comments_by_search(self,cookies_str):
        """根据搜索结果获取评论"""
        for url in self.note_list:
            self.get_comments(cookies_str,url)

    def merge_note_info_with_comments(self, note_info, comments_list,userInfo,kerword):
        """将笔记信息与评论列表合并
        
        Args:
            note_info (dict): get_note_info函数返回的笔记信息字典
            comments_list (list): get_comments函数返回的评论列表
            userInfo (str): 客户标识
            
        Returns:
            list: 合并后的数据列表，每个元素包含笔记信息和单条评论信息
        """
        merged_data = []
        
        for comment in comments_list:
            # 创建合并后的数据字典
            merged_item = {
                # 笔记信息
                'keyword':kerword,
                'title': note_info.get('title', ''),
                'note_author': note_info.get('author', ''),
                'userInfo': userInfo,  # 客户标识
                'note_likes': note_info.get('note_likes', 0),
                'collects': note_info.get('collected_count', 0),
                'comments': note_info.get('comment_count', 0),
                'note_url': note_info.get('note_url', ''),
                'collect_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 收集时间
                'note_time': note_info.get('note_time', ''),  # 笔记创建时间
                'note_location': note_info.get('location', ''),
                'note_type': note_info.get('note_type', ''),
                'note_content': note_info.get('note_content', '').replace('\n', ''),  # 笔记内容
                
                # 评论信息
                'comment_location': comment.get('comment_location', ''),
                'comment_id': comment.get('comment_id', ''),
                'comment_author': comment.get('nickname', ''),
                'comment_like_count': comment.get('like_count', 0),  # 评论点赞数
                'comment_content': comment.get('content', ''),  # 评论内容
            }
            merged_data.append(merged_item)
            
        return merged_data

    def get_note_info(self, cookies_str, url):
        """获取小红书笔记信息
        Args:
            cookies_str (str): Cookies字符串
            note_id (str): 笔记ID
            xsec_token (str): 安全令牌
        """
        ori_url=url
        if "discovery" in  url:
            url=convert_discovery_to_explore_url(url)
        note_params = self.extract_url_params(url)
        uri = "/api/sns/web/v1/feed"
        params = {
            "source_note_id": note_params['note_id'],
            "xsec_token": note_params['xsec_token'],
            "xsec_source": note_params['xsec_source'],
            "image_formats": [
                "jpg",
                "webp",
                "avif"
            ],
            "extra": {
                "need_body_topic": "1"
            }
        }
        # splice_api = splice_str(uri, params)
        headers, cookies, data = generate_request_params(cookies_str, uri, params)
        response = requests.post("https://edith.xiaohongshu.com"+uri, headers=headers, cookies=cookies, data=data.encode('utf-8')).json()
        
        if response.get('code') == 0 :
            info_data={
                'note_type': response.get('data', {}).get('items', {})[0].get('model_type', {}),#笔记类型
                'note_id': response.get('data', {}).get('items', {})[0].get('note_card').get('note_id', ''),  # 笔记ID
                'title': response.get('data', {}).get('items', {})[0].get('note_card').get('title', ''),  # 笔记标题
                'note_likes': response.get('data', {}).get('items', {})[0].get('note_card').get('interact_info').get('liked_count', 0),  # 点赞数
                'collected_count': response.get('data', {}).get('items', {})[0].get('note_card').get('interact_info').get('collected_count', 0),  # 收藏数
                'comment_count': response.get('data', {}).get('items', {})[0].get('note_card').get('interact_info').get('comment_count', 0),  # 评论数
                'note_url': ori_url,  # 笔记URL
                'xsec_token': note_params['xsec_token'],  # 安全令牌
                'location': response.get('data', {}).get('items', {})[0].get('note_card').get('ip_location', ''),  # 位置
                'author': response.get('data', {}).get('items', {})[0].get('note_card', {}).get('user', '').get('nickname'),  # 作者昵称
                'note_content': response.get('data', {}).get('items', {})[0].get('note_card').get('desc', '').replace('\n',''),  # 笔记内容
            }
            
            return info_data
        else:
            print(f"获取笔记信息失败: {response.get('message', '未知错误')}")
            return False
        print(response)
    
    def monitor_comments(self, cookies_list, note_url,userInfo,keyword,comment_cnt, interval=60):
        """监控笔记评论变化
        Args:
            cookies_list (List): Cookies列表
            note_url (str): 笔记URL
            userInfo (str): 客户标识
            keyword (str): 关键词
            interval (int): 检查间隔时间（秒）
        """
        #笔记基本信息
        cookies_str = random.choice(cookies_list)  # 随机选择一个cookie
        dead_cookies_list = []
        print(f'使用的Cookies: {cookies_str}')
        # 获取笔记信息
        note_info=self.get_note_info(cookies_str,note_url)
        if not note_info:
            #笔记失效则重新获取cookies并将该cookie从cookie_list中删除
            cookies_list.remove(cookies_str)
            dead_cookies_list.append(cookies_str)
            print(f"获取笔记信息失败，当前cookie已失效: {cookies_str}")
            cookies_str = random.choice(self.get_all_cookies())  # 随机更换一个cookie
        if int(note_info.get('comment_count', 0)) != int(comment_cnt): #如果笔记的评论数和上一次获取的评论数不同，才监控
        #笔记的评论内容
            print(f"笔记评论数已变化，当前评论数: {note_info.get('comment_count', 0)}，上次获取的评论数: {comment_cnt},开始监控")
            comments_list = []
            comments_list = self.get_comments(cookies_str, note_url, comments_list=comments_list)
            print(f'一共收集到{len(comments_list)}条评论')
            merge_info = self.merge_note_info_with_comments(note_info, comments_list,userInfo,keyword)
            
            print(merge_info)
            if not comments_list:
                #更换cookies
                cookies_list.remove(cookies_str)
                dead_cookies_list.append(cookies_str)
                print(f"获取笔记信息失败，当前cookie已失效: {cookies_str}")
                cookies_str = random.choice(self.get_all_cookies())  # 随机更换一个cookie
            return merge_info,dead_cookies_list
        else:
            print(f"笔记评论数未变化，当前评论数: {note_info.get('comment_count', 0)}，上次获取的评论数: {comment_cnt},不进行监控")
            return None
    
# 使用示例
if __name__ == "__main__":
    # 创建XhsAPI实例
    xhs_api = XhsAPI()
    
    # 示例：获取指定笔记的评论
    # note_url = "https://www.xiaohongshu.com/explore/your_note_id?xsec_token=your_token&xsec_source=pc_feed"
    # xhs_api.get_comments(note_url)
    
    # 示例：根据关键词搜索笔记
    # xhs_api.search_by_keyword("美食", 10)
    # xhs_api.get_comments_by_search()
    headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "origin": "https://www.xiaohongshu.com",
    "priority": "u=1, i",
    "referer": "https://www.xiaohongshu.com/",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
    "x-b3-traceid": "0da07b72e11f78dc",
    "x-mns": "unload",
    "x-s": "XYW_eyJzaWduU3ZuIjoiNTYiLCJzaWduVHlwZSI6IngyIiwiYXBwSWQiOiJ4aHMtcGMtd2ViIiwic2lnblZlcnNpb24iOiIxIiwicGF5bG9hZCI6ImNiMzNlMjJmZjdiZmM3YjFmNzA5OTgzNTI4ZjNiZmQ4YjE5MzdmMTEzZTRjNTE0YzBmMGYwMGIzYWE2MTU1NjBlYTA4MjFjZDMxM2VjNWFlMDFjODU4YzI0ZjU5ZWNhMDFmYjE3Yjg3ZGMzY2VkMjI1OWU3NDQwODQ3MDg4MGE3YTQ5MTMwZjcwYmQzOTQ1MjZhZDY2YjdlNWMwYjA2ZmY3MDRmODBkNjQ0OTMwNDQ4YTMyN2ExOTczOTZhODQ0ZTg2ZGM2NmY5N2ZhYWEyNTIwYzE5NjU2MGQ4ZmE1ZjhkZmQ3ZGM3ODg0YTY3MzNhNjA1NDA3MzBjNDgwZDI4ZmJiYTQ3MzQ2YTRkYjFlZDE1YTViZTdjM2YxYzc5ZWE1NDEwMGE0ZDA3OWYyMWIxZTU2YWMyNjE5MTVkZTFiNTA2ZGYzNjE4ZmE0MjMxY2YyNWVkNGM4YTE0Y2JmMDE3MDg1YTFmOGQwNTg2MzE5MjcwYzIyMDE5MzI3M2UyMGZiYzcyNzFmYmY0ZTk4ODRkYWQ3ODM1MGRkZWRmMzMwODk2In0=",
    "x-s-common": "2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1PahIHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHFN0GhN0ZjNsQh+aHCH0rE+0bfP/4S+/rIyoS9JdmCq0clPdWUJg+VyADl2dmhyAS0q9HF4B+j+/ZIPeZUP/P7weZjNsQh+jHCHjHVHdW7H0ijHjIj2eWjwjQQPAYUaBzdq9k6qB4Q4fpA8b878FSet9RQzLlTcSiM8/+n4MYP8F8LagY/P9Ql4FpUzfpS2BcI8nT1GFbC/L88JdbFyrSiafpr8DMra7pFLDDAa7+8J7QgabmFz7Qjp0mcwp4fanD68p40+fp8qgzELLbILrDA+9p3JpH9LLI3+LSk+d+DJfpSL98lnLYl49IUqgcMc0mrcDShtMmozBD6qM8FyFSh8o+h4g4U+obFyLSi4nbQz/+SPFlnPrDApSzQcA4SPopFJeQmzBMA/o8Szb+NqM+c4ApQzg8Ayp8FaDRl4AYs4g4fLomD8pzBpFRQ2ezLanSM+Skc47Qc4gcMag8VGLlj87PAqgzhagYSqAbn4FYQy7pTanTQ2npx87+8NM4L89L78p+l4BL6ze4AzB+IygmS8Bp8qDzFaLP98Lzn4AQQzLEAL7bFJBEVL7pwyS8Fag868nTl4e+0n04ApfuF8FSbL7SQyrpELLQl4LShyBEl20YdanTQ8fRl49TQc7bgzAqAq9zV/9pnLoqAag8m8/mf89pD8SzoanDMqA++J/ZU4gzmanSNq9SD4fp3nDESpbmF+BEm/9pgLo4bag8LwoiIcnpfpd4M/BENqM+n49QQPMQUagYb+LlM474Yqgq3qfp3qSmQ+nprJURSpSm7JLSiad+/JDbSy9MM4DSkcg+faaRA2rQk8rS34fLALo4VanYzyAQn4obOqgclagYSqMzn4BkQyAmAygb78rSiN7+x4gcA47pFJd+c4ApQc9+Va/+V+o4m+Bk7aLbApM87+rSb+obQyrRAL7bFnDQjpoc6c/mSyfkIPLS3zMmo4gzUqMm7LFS9cnphpdzMLoQ68/+V+d+LGfMjanYmqA8s+7+L4g4oqop7/FSeafpgpd4kanD68pGI4nMQ4DbSyfG68p+M4bYQ2rkApdb7yF4fwbmQzpqhag8tqM8PP9L98o8SzbP98nzn4rQQyFGla/+z+dQn4bbQ4f+iaLLMqA+BqLb7/BzSyMm7yDShabHFpd4oJnu68nDI+d+kqgziqgbFPLSkq0YQ4fQB/dbF2oQM4A+QyLEAyMpd8nzl4Fzt4gz9anY/PrEl4bkQygr749+yLLDA/9pDwLTSPbLI8nSc4ob7pdzDaLpBtFS9cgPl4g4eaLpt8pSfaLSQc9QCcSDh/FS9qozQcA+Sygp7J7kl4rEzLo4ragYBOaHVHdWEH0iTP/Ghw/Z7+0rlwsIj2erIH0iINsQhP/rjwjQ1J7QTGnIjKc==",
    "x-t": "1749555763020",
    "x-xray-traceid": "cbacd32ba29821f05762f69f9606ff38"
}
    cookies = {
        "abRequestId": "de44367b-c7a9-5122-808b-38640866adb1",
        "a1": "1961f17e510hyvnpzr412x2mslk91zpxk9csb4tcb50000213780",
        "webId": "c89bbad4fd530edd2fe7e6307c3816a0",
        "gid": "yjKyiyWiSYT2yjKyiyWd2j49y8xvhIUuF4yJSSDCJ6M1TM28jyuUCD888JyqWY880DfJi4W4",
        "web_session": "040069b590abc3569b441ed2003a4bcb364719",
        "webBuild": "4.68.0",
        "x-user-id-creator.xiaohongshu.com": "64e4e88b000000000100cb12",
        "customer-sso-sid": "68c517514234907575773163fjbguyd2fgeqstsz",
        "customerClientId": "742074612603293",
        "access-token-creator.xiaohongshu.com": "customer.creator.AT-68c517514234907575773164v6acmpkdbgewrwve",
        "galaxy_creator_session_id": "wAgBUoJ14GxuEOy9MqGWP3NSXbUd1DmfHVi3",
        "galaxy.creator.beaker.session.id": "1749544150823021998416",
        "loadts": "1749551971315",
        "xsecappid": "ugc",
        "unread": "{%22ub%22:%22682185cd000000000f032351%22%2C%22ue%22:%2268416bbc000000000303c45e%22%2C%22uc%22:33}",
        "acw_tc": "0a0bb12f17495548295027308e4f05246b73f9dc072cc64e3e2d5e9efa0bbb",
        "websectiga": "984412fef754c018e472127b8effd174be8a5d51061c991aadd200c69a2801d6",
        "sec_poison_id": "5d606d09-40ab-4fe9-bc03-078ac0a3ff2b"
    }
    url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
    params = {
        "note_id": "68370a5e000000002301ef65",
        "root_comment_id": "6837cc80000000000a037237",
        "num": "10",
        "cursor": "6838bd9e0000000009038832",
        "image_formats": "jpg,webp,avif",
        "top_comment_id": "",
        "xsec_token": "ABjE8zz4iq_2YHh2hHdkm13Fu8WL-xIQ58jvGBoC6_KZw="
    }

    response = requests.get(url, headers=headers, cookies=cookies, params=params)

    print(response.text)
    print(response)
    print("XhsAPI类已创建，请根据需要调用相应方法")
    
    # 记得在使用完毕后关闭资源
    # xhs_api.close()