# 小红书 API

这个项目提供了一个用于访问和处理小红书数据的Python API封装。

## 功能特点

- 获取小红书笔记评论
- 根据关键词搜索评论
- 支持URL转换（从discovery到explore格式）
- 数据导出为CSV格式

## 安装

1. 克隆此仓库:
```bash
git clone <repository-url>
cd xhs_API
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

3. 配置环境变量:
创建一个`.env`文件，并添加您的小红书cookies:
```
COOKIES=your_cookies_string_here
```

## 使用方法

### 获取笔记评论

```python
from xhs_utils.common_util import init
from xhs_api_class import XhsAPI

cookies_str, base_path = init()
xhs = XhsAPI()
xhs.get_comments(cookies_str, 'https://www.xiaohongshu.com/explore/note_id')
```

### 搜索评论

```python
from xhs_utils.common_util import init
from xhs_api_class import XhsAPI

cookies_str, base_path = init()
xhs = XhsAPI()
xhs.search_comment_by_keyword(cookies_str, '关键词', 10)  # 10是搜索结果数量
```

## 项目结构

- `xhs_api_class.py`: 主API类
- `xhs_utils/`: 工具函数
  - `common_util.py`: 通用工具函数
  - `cookie_util.py`: Cookie处理工具
  - `url_converter.py`: URL转换工具
  - `xhs_util.py`: 小红书特定工具函数
- `main.py`: 示例用法

## 注意事项

- 使用前请确保您有有效的小红书cookies
- 请遵守小红书的使用条款和API使用限制
- 数据将保存在`datas/`目录下的相应子目录中

## 依赖

详见`requirements.txt`文件。
