from xhs_utils.common_util import init
from xhs_api_class import XhsAPI
cookies_str, base_path = init()
print(f'Cookies: {cookies_str}')
xhs = XhsAPI()
# xhs.search_comment_by_keyword(cookies_str,'猫咪', 10)
xhs.get_comments(cookies_str,'https://www.xiaohongshu.com/explore/68519a5900000000230144ad?xsec_source=app_share&type=normal&xsec_token=CBdXOVVtUIw-vYe_hwvxF7TynDO5PGe_mv0xnQZUdOzg4%3D')

