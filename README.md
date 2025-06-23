# 小红书 API

这个项目提供了一个用于访问和处理小红书数据的Python API封装。

## 功能特点

- 获取小红书笔记评论
- 根据关键词搜索评论
- 支持URL转换（从discovery到explore格式）
- 数据导出为CSV格式
- **数据库Cookie管理**: 从MySQL数据库动态获取cookies
- **智能Cookie轮换**: 自动选择最少使用的cookies
- **Cookie状态管理**: 自动标记无效cookies

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
创建一个`.env`文件，并添加数据库配置:
```
# 数据库配置（推荐）
DB_USER=your_database_username
DB_PASSWORD=your_database_password

# 备用cookies配置（当数据库连接失败时使用）
COOKIES=your_cookies_string_here
```

4. 设置数据库:
- 在MySQL数据库中执行 `database_schema.sql` 文件创建所需的表结构
- 向 `xhs_cookies` 表中添加有效的cookies数据

## 使用方法

### 测试数据库连接

```python
# 测试数据库cookie管理器
python test_db_cookies.py
```

### 获取笔记评论

```python
from xhs_utils.common_util import init
from xhs_api_class import XhsAPI

# 现在会自动从数据库获取cookies
cookies_str, base_path = init()
xhs = XhsAPI()
xhs.get_comments(cookies_str, 'https://www.xiaohongshu.com/explore/note_id')
```

### 直接使用数据库Cookie管理器

```python
from db_manager import DatabaseCookieManager
import os
from dotenv import load_dotenv

load_dotenv()
db_manager = DatabaseCookieManager(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

# 获取随机cookie
cookie = db_manager.get_random_cookie()

# 获取最少使用的cookie
cookie = db_manager.get_least_used_cookie()

# 添加新cookie
db_manager.add_cookie('your_new_cookie_string')

# 标记cookie为无效
db_manager.mark_cookie_invalid(cookie_id)
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
