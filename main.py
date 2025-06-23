from xhs_utils.common_util import init,load_env
from xhs_api_class import XhsAPI
import os
import sys
from dotenv import load_dotenv
from db_manager import DatabaseCookieManager

def monitor_task(email,keyword):
    load_dotenv()
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_manager = DatabaseCookieManager(
            user=db_user,
            password=db_password
        )
    random_cookie = db_manager.get_random_cookie()    
    cookies_str=random_cookie
    print(f'Cookies: {cookies_str}')
    xhs = XhsAPI()
    monitor_urls=db_manager.get_monitor_urls(email)
    cnt=db_manager.get_note_comments_count(monitor_urls[0])
    
    for url in monitor_urls:
        print(f'监控链接: {url},监控评论数量: {cnt}')
        data=xhs.monitor_comments(cookies_str,url,email,keyword,cnt)
        db_manager.save_to_monitor_comments(data)

monitor_task('luyao-operate@lucy.ai','keyword')