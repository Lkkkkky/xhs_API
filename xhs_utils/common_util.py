import os
from loguru import logger
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_manager import DatabaseCookieManager

def load_env():
    """从数据库获取cookies"""
    load_dotenv()
    
    # 获取数据库配置
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    
    if not db_user or not db_password:
        logger.error("数据库用户名或密码未配置，请在.env文件中设置DB_USER和DB_PASSWORD")
        return None
    
    # 初始化数据库cookie管理器
    db_manager = DatabaseCookieManager(
        user=db_user,
        password=db_password
    )
    
    # 从数据库获取随机cookie
    cookies_str = db_manager.get_random_cookie()
    
    if not cookies_str:
        logger.warning("从数据库获取cookie失败，尝试从环境变量获取")
        cookies_str = os.getenv('COOKIES')
    
    return cookies_str

def init():
    media_base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../datas/media_datas'))
    excel_base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../datas/excel_datas'))
    for base_path in [media_base_path, excel_base_path]:
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            logger.info(f'创建目录 {base_path}')
    cookies_str = load_env()
    base_path = {
        'media': media_base_path,
        'excel': excel_base_path,
    }
    return cookies_str, base_path

