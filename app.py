#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask API 服务器
将monitor_task函数封装为REST API接口
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv
from db_manager import DatabaseCookieManager
from xhs_api_class import XhsAPI
from xhs_utils.common_util import init, load_env
import traceback
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 加载环境变量
load_dotenv()

def monitor_task(email, keyword):
    """
    监控任务函数（从main.py移植）
    
    Args:
        email (str): 用户邮箱
        keyword (str): 关键词
        
    Returns:
        dict: 包含执行结果的字典
    """
    try:
        # 获取数据库配置
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        
        if not db_user or not db_password:
            raise ValueError("数据库配置缺失，请检查环境变量 DB_USER 和 DB_PASSWORD")
        
        # 初始化数据库管理器
        db_manager = DatabaseCookieManager(
            user=db_user,
            password=db_password
        )
        
        # 获取随机cookie
        random_cookie = db_manager.get_random_cookie()
        if not random_cookie:
            raise ValueError("无法获取有效的cookie")
        
        cookies_str = random_cookie
        logger.info(f'使用Cookies: {cookies_str[:50]}...')
        
        # 初始化小红书API
        xhs = XhsAPI()
        
        # 获取监控URL列表
        monitor_urls = db_manager.get_monitor_urls(email)
        if not monitor_urls:
            raise ValueError(f"用户 {email} 没有需要监控的URL")
        # 执行监控任务
        for url in monitor_urls:
            # 获取当前评论数量
            cnt = db_manager.get_note_comments_count(url)
            logger.info(f'开始监控链接: {url}, 当前评论数量: {cnt}')
            
            data = xhs.monitor_comments(cookies_str, url, email, keyword, cnt)
            
            db_manager.update_note_comments_count(url, data[0]['comments'])
            print(url)
            # 保存监控数据
            db_manager.save_to_monitor_comments(data)
            
        return {
            'success': True,
            'message': '监控任务执行成功',
            'data': {
                'email': email,
                'keyword': keyword,
                'monitor_url': monitor_urls,
                'timestamp': datetime.now().isoformat()
            }
        }
            
    except Exception as e:
        logger.error(f"监控任务执行失败: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            'success': False,
            'message': f'监控任务执行失败: {str(e)}',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

@app.route('/', methods=['GET'])
def index():
    """API根路径"""
    return jsonify({
        'message': '小红书监控API服务',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/monitor': '执行监控任务',
            'GET /api/health': '健康检查'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    try:
        # 测试数据库连接
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        
        if not db_user or not db_password:
            return jsonify({
                'status': 'unhealthy',
                'message': '数据库配置缺失',
                'timestamp': datetime.now().isoformat()
            }), 500
        
        db_manager = DatabaseCookieManager(
            user=db_user,
            password=db_password
        )
        
        # 测试数据库连接
        if db_manager.test_connection():
            return jsonify({
                'status': 'healthy',
                'message': 'API服务正常运行',
                'database': 'connected',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'unhealthy',
                'message': '数据库连接失败',
                'timestamp': datetime.now().isoformat()
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'健康检查失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/monitor', methods=['POST'])
def api_monitor_task():
    """
    监控任务API接口
    
    请求体:
    {
        "email": "user@example.com",
        "keyword": "关键词"
    }
    
    响应:
    {
        "success": true/false,
        "message": "执行结果消息",
        "data": {...},  // 成功时包含详细数据
        "error": "...",  // 失败时包含错误信息
        "timestamp": "2024-01-01T12:00:00"
    }
    """
    try:
        # 获取请求数据
        if not request.is_json:
            return jsonify({
                'success': False,
                'message': '请求必须是JSON格式',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        data = request.get_json()
        
        # 验证必需参数
        if not data:
            return jsonify({
                'success': False,
                'message': '请求体不能为空',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        email = data.get('email')
        keyword = data.get('keyword')
        
        if not email:
            return jsonify({
                'success': False,
                'message': '缺少必需参数: email',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        if not keyword:
            return jsonify({
                'success': False,
                'message': '缺少必需参数: keyword',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # 验证邮箱格式
        if '@' not in email or '.' not in email:
            return jsonify({
                'success': False,
                'message': '邮箱格式不正确',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        logger.info(f"开始执行监控任务 - Email: {email}, Keyword: {keyword}")
        
        # 执行监控任务
        result = monitor_task(email, keyword)
        
        # 根据执行结果返回相应的HTTP状态码
        if result['success']:
            logger.info(f"监控任务执行成功 - Email: {email}")
            return jsonify(result), 200
        else:
            logger.error(f"监控任务执行失败 - Email: {email}, Error: {result.get('error')}")
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"API接口异常: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'服务器内部错误: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'success': False,
        'message': '接口不存在',
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """405错误处理"""
    return jsonify({
        'success': False,
        'message': '请求方法不被允许',
        'timestamp': datetime.now().isoformat()
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        'success': False,
        'message': '服务器内部错误',
        'timestamp': datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    # 开发环境运行配置
    app.run(
        host='0.0.0.0',  # 允许外部访问
        port=5000,       # 端口号
        debug=True       # 开启调试模式
    )