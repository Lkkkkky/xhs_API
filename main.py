from xhs_utils.common_util import init,load_env
from xhs_api_class import XhsAPI
import os
import sys
from dotenv import load_dotenv
from db_manager import DatabaseCookieManager
load_dotenv()
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_manager = DatabaseCookieManager(
        user=db_user,
        password=db_password
    )
random_cookie = db_manager.get_random_cookie()    
cookies_str=random_cookie

xhs = XhsAPI()
# xhs.search_comment_by_keyword(cookies_str,'猫咪', 10)

xhs.reply_comment(cookies_str,'https://www.xiaohongshu.com/explore/68898e840000000005007a2b?xsec_token=ABc5ZocMJCuX4U6G5dslWmpXyGtOW0-0eNkqxb1Rvzueg=&xsec_source=pc_feed','688a0633000000002a00b0a6','笑死我了')

# db_manager.mark_cookie_status(1,'abRequestId=de44367b-c7a9-5122-808b-38640866adb1; a1=1961f17e510hyvnpzr412x2mslk91zpxk9csb4tcb50000213780; webId=c89bbad4fd530edd2fe7e6307c3816a0; gid=yjKyiyWiSYT2yjKyiyWd2j49y8xvhIUuF4yJSSDCJ6M1TM28jyuUCD888JyqWY880DfJi4W4; x-user-id-creator.xiaohongshu.com=64e4e88b000000000100cb12; customerClientId=742074612603293; access-token-creator.xiaohongshu.com=customer.creator.AT-68c517514234907575773164v6acmpkdbgewrwve; galaxy_creator_session_id=wAgBUoJ14GxuEOy9MqGWP3NSXbUd1DmfHVi3; galaxy.creator.beaker.session.id=1749544150823021998416; xsecappid=xhs-pc-web; webBuild=4.68.0; web_session=040069b9593484798b5fbcaf613a4bbc966555; loadts=1750402446172; acw_tc=0a4a1d1e17504026803042870e9c2188716ee2895c9a702adb3e977981ec72; websectiga=2a3d3ea002e7d92b5c9743590ebd24010cf3710ff3af8029153751e41a6af4a3; sec_poison_id=21d53c82-f3f7-483c-bad1-864951a28021; unread={%22ub%22:%226847e80000000000220040dd%22%2C%22ue%22:%2268513a26000000002301c094%22%2C%22uc%22:24}')
# data=xhs.monitor_comments(cookies_str,'https://www.xiaohongshu.com/explore/68886ebf0000000005004501?xsec_token=ABUS3D2BSXOTlc7DytK1Gw1axuVg6oOYlFsR_r--d1DR4=&xsec_source=pc_feed','qq@com','ha')
#保存到数据库
# db_manager.save_to_monitor_comments(data)
