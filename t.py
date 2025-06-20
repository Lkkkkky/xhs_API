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




url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
params = {
    "note_id": "67b83c8b000000000602b5dc",
    "root_comment_id": "67ded844000000001e034a91",
    "num": "10",
    "cursor": "67e02fa7000000001e01d723",
    "image_formats": "jpg,webp,avif",
    "top_comment_id": "",
    "xsec_token": "ABMliQUYGAQG2jCQqfLNei-CJdLl_Hn0zI_j2hockVWKE="
}
cookies_str="abRequestId=de44367b-c7a9-5122-808b-38640866adb1; a1=1961f17e510hyvnpzr412x2mslk91zpxk9csb4tcb50000213780; webId=c89bbad4fd530edd2fe7e6307c3816a0; gid=yjKyiyWiSYT2yjKyiyWd2j49y8xvhIUuF4yJSSDCJ6M1TM28jyuUCD888JyqWY880DfJi4W4; x-user-id-creator.xiaohongshu.com=64e4e88b000000000100cb12; customerClientId=742074612603293; access-token-creator.xiaohongshu.com=customer.creator.AT-68c517514234907575773164v6acmpkdbgewrwve; galaxy_creator_session_id=wAgBUoJ14GxuEOy9MqGWP3NSXbUd1DmfHVi3; galaxy.creator.beaker.session.id=1749544150823021998416; xsecappid=xhs-pc-web; webBuild=4.68.0; acw_tc=0a0b147517503935622507362e61e83e40d82c66e35e9244b2a37a911dcd89; websectiga=984412fef754c018e472127b8effd174be8a5d51061c991aadd200c69a2801d6; sec_poison_id=440ad5db-595f-4456-a7e8-da2b29e6134e; web_session=040069b9593484798b5fbcaf613a4bbc966555; loadts=1750394818095; unread={%22ub%22:%226853d48700000000170302d9%22%2C%22ue%22:%2268454e230000000022036bea%22%2C%22uc%22:25}"
uri = "/api/sns/web/v2/comment/sub/page"
splice_api = splice_str(uri, params)
headers, cookies, data = generate_request_params(cookies_str, splice_api)
print(f"headers:::{headers}")
print(f"cookies:::{cookies}")
response = requests.get("https://edith.xiaohongshu.com"+splice_api, headers=headers, cookies=cookies)

print(response.text)
print(response)