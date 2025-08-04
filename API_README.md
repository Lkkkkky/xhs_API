# 小红书API FastAPI服务

基于FastAPI框架封装的小红书数据获取API服务，提供获取评论、搜索笔记、获取笔记信息等功能。

## 功能特性

- 🔍 **搜索笔记**: 根据关键词搜索小红书笔记
- 💬 **获取评论**: 获取指定笔记的所有评论（包括子评论）
- 📝 **笔记信息**: 获取笔记的详细信息（标题、作者、点赞数等）
- 👀 **监控评论**: 监控笔记评论变化
- 💭 **回复评论**: 回复指定评论
- 🏥 **健康检查**: 服务状态检查

## 安装和启动

### 1. 环境配置

创建 `.env` 文件并配置数据库连接信息：
```env
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

**方法一：直接运行**
```bash
python fastapi_app.py
```

**方法二：使用uvicorn**
```bash
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```

服务启动后，访问 `http://localhost:8000` 查看API文档。

## API接口文档

### 1. 根路径
- **GET** `/`
- **描述**: 获取API基本信息

### 2. 获取笔记评论
- **POST** `/comments`
- **描述**: 获取指定笔记的所有评论
- **请求体**:
```json
{
  "note_url": "https://www.xiaohongshu.com/explore/note_id?xsec_token=xxx",
  "cursor": ""  // 可选，用于分页
}
```

### 3. 搜索笔记
- **POST** `/search`
- **描述**: 根据关键词搜索笔记
- **请求体**:
```json
{
  "keyword": "搜索关键词",
  "num": 10
}
```

### 3. 获取笔记信息

**接口**: `POST /note-info`

**请求体**:
```json
{
    "note_url": "https://www.xiaohongshu.com/explore/note_id?xsec_token=xxx"
}
```

### 4. 监控笔记评论

**接口**: `POST /monitor`

**请求体**:
```json
{
    "note_url": "https://www.xiaohongshu.com/explore/note_id?xsec_token=xxx",
    "user_info": "客户标识",
    "keyword": "关键词",
    "interval": 60
}
```

### 5. 回复评论

**接口**: `POST /reply`

**请求体**:
```json
{
    "note_url": "https://www.xiaohongshu.com/explore/note_id?xsec_token=xxx",
    "comment_id": "评论ID",
    "content": "回复内容"
}
```

### 7. 健康检查
- **GET** `/health`
- **描述**: 检查服务状态

## 使用示例

### Python客户端示例

```python
import requests
import json

# API基础URL
base_url = "http://localhost:8000"

# 获取笔记评论
def get_comments_example():
    url = f"{base_url}/comments"
    data = {
        "note_url": "https://www.xiaohongshu.com/explore/your_note_id?xsec_token=xxx"
    }
    response = requests.post(url, json=data)
    return response.json()

# 搜索笔记
def search_notes_example():
    url = f"{base_url}/search"
    data = {
        "keyword": "美食",
        "num": 5
    }
    response = requests.post(url, json=data)
    return response.json()

# 获取笔记信息
def get_note_info_example():
    url = f"{base_url}/note-info"
    data = {
        "note_url": "https://www.xiaohongshu.com/explore/your_note_id?xsec_token=xxx"
    }
    response = requests.post(url, json=data)
    return response.json()
```

### curl示例

```bash
# 获取笔记评论
curl -X POST "http://localhost:8000/comments" \
     -H "Content-Type: application/json" \
     -d '{
       "note_url": "https://www.xiaohongshu.com/explore/your_note_id?xsec_token=xxx"
     }'

# 搜索笔记
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{
       "keyword": "美食",
       "num": 5
     }'
```

## 注意事项

1. **数据库配置**: 确保数据库中有有效的cookies数据，系统会自动从数据库获取cookies
2. **请求频率**: 建议控制请求频率，避免被限制
3. **URL格式**: 确保笔记URL格式正确，包含必要的参数
4. **错误处理**: API会返回详细的错误信息，请根据错误信息调整请求

## 响应格式

### 成功响应
```json
{
  "success": true,
  "data": [...],  // 具体数据
  "count": 10     // 数据数量（可选）
}
```

### 错误响应
```json
{
  "detail": "错误描述信息"
}
```

## 自动化文档

启动服务后，可以访问以下地址查看自动生成的API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 技术栈

- **FastAPI**: 现代、快速的Web框架
- **Pydantic**: 数据验证和序列化
- **Uvicorn**: ASGI服务器
- **curl-cffi**: HTTP客户端库

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规和平台使用条款。