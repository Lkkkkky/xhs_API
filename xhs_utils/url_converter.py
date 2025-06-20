#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书URL转换工具
将discovery格式的URL转换为explore格式
"""

from urllib.parse import urlparse, parse_qs, urlencode

def convert_discovery_to_explore_url(discovery_url):
    """将discovery格式的URL转换为explore格式
    
    Args:
        discovery_url (str): discovery格式的小红书链接
        
    Returns:
        str: explore格式的小红书链接，只保留xsec_source、type、xsec_token参数
        
    Example:
        输入: https://www.xiaohongshu.com/discovery/item/6851829e000000002102cb05?app_platform=android&xsec_source=app_share&type=normal&xsec_token=CBdXOVVtUIw-vYe_hwvxF7T9SFM2KAdwiE2MWDtPM_1kM%3D&author_share=1
        输出: https://www.xiaohongshu.com/explore/6851829e000000002102cb05?xsec_source=app_share&type=normal&xsec_token=CBdXOVVtUIw-vYe_hwvxF7T9SFM2KAdwiE2MWDtPM_1kM%3D
    """
    try:
        parsed = urlparse(discovery_url)
        
        # 提取note_id
        path_segments = parsed.path.strip("/").split("/")
        if len(path_segments) >= 3 and path_segments[0] == "discovery" and path_segments[1] == "item":
            note_id = path_segments[2]
        else:
            raise ValueError("无效的discovery URL格式")
        
        # 解析查询参数
        query_params = parse_qs(parsed.query)
        
        # 只保留需要的参数
        filtered_params = {}
        for param in ['xsec_source', 'type', 'xsec_token']:
            if param in query_params:
                filtered_params[param] = query_params[param][0]  # 取第一个值
        
        # 构建新的explore URL
        explore_url = f"https://www.xiaohongshu.com/explore/{note_id}"
        if filtered_params:
            explore_url += "?" + urlencode(filtered_params)
        
        return explore_url
        
    except Exception as e:
        print(f"URL转换失败: {e}")
        return None

def main():
    """测试函数"""
    # 测试URL
    test_url = "https://www.xiaohongshu.com/discovery/item/68519a5900000000230144ad?app_platform=android&ignoreEngage=true&app_version=8.72.0&share_from_user_hidden=true&xsec_source=app_share&type=normal&xsec_token=CBdXOVVtUIw-vYe_hwvxF7TynDO5PGe_mv0xnQZUdOzg4%3D&author_share=1&xhsshare=CopyLink&shareRedId=OD41NTdGNE82NzUyOTgwNjdFOTk2Pjo-&apptime=1750247117&share_id=650c2946716f4364a344222d43d4affc&share_channel=copy_link"
    
    print("原始URL:")
    print(test_url)
    print("\n" + "="*100 + "\n")
    
    # 转换URL
    result = convert_discovery_to_explore_url(test_url)
    
    if result:
        print("转换后的URL:")
        print(result)
        print("\n转换成功！")
        
        # 验证结果
        expected = "https://www.xiaohongshu.com/explore/6851829e000000002102cb05?xsec_source=app_share&type=normal&xsec_token=CBdXOVVtUIw-vYe_hwvxF7T9SFM2KAdwiE2MWDtPM_1kM%3D"
        print(f"\n期望结果: {expected}")
        print(f"实际结果: {result}")
        print(f"结果匹配: {result == expected}")
    else:
        print("转换失败！")

if __name__ == "__main__":
    main()