# 小红书监控 Flask API 文档

## 概述

本API服务将原本的 `monitor_task` 函数封装为RESTful API接口，提供小红书评论监控功能。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements_flask.txt
```

### 2. 配置环境变量

在项目根目录创建 `.env` 文件：

```env
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

### 3. 启动API服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

### 4. 测试API

```bash
python api_example.py
```

## API 接口文档

### 基础信息

- **基础URL**: `http://localhost:5000`
- **内容类型**: `application/json`
- **字符编码**: `UTF-8`

### 接口列表

#### 1. 获取API信息

**请求**
```
GET /
```

**响应示例**
```json
{
  "message": "小红书监控API服务",
  "version": "1.0.0",
  "endpoints": {
    "POST /api/monitor": "执行监控任务",
    "GET /api/health": "健康检查"
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 2. 健康检查

**请求**
```
GET /api/health
```

**响应示例**
```json
{
  "status": "healthy",
  "message": "API服务正常运行",
  "database": "connected",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 3. 执行监控任务

**请求**
```
POST /api/monitor
Content-Type: application/json

{
  "email": "user@example.com",
  "keyword": "关键词"
}
```

**请求参数**

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| email | string | 是 | 用户邮箱，用于获取监控URL列表 |
| keyword | string | 是 | 监控关键词 |

**成功响应示例**
```json
{
  "success": true,
  "message": "监控任务执行成功",
  "data": {
    "email": "user@example.com",
    "keyword": "关键词",
    "monitor_url": "https://www.xiaohongshu.com/explore/...",
    "previous_comment_count": 10,
    "new_comments_found": 2,
    "save_result": true,
    "timestamp": "2024-01-01T12:00:00"
  }
}
```

**失败响应示例**
```json
{
  "success": false,
  "message": "监控任务执行失败: 用户 user@example.com 没有需要监控的URL",
  "error": "用户 user@example.com 没有需要监控的URL",
  "timestamp": "2024-01-01T12:00:00"
}
```

## 错误处理

### HTTP状态码

- `200`: 请求成功
- `400`: 请求参数错误
- `404`: 接口不存在
- `405`: 请求方法不被允许
- `500`: 服务器内部错误

### 错误响应格式

```json
{
  "success": false,
  "message": "错误描述",
  "timestamp": "2024-01-01T12:00:00"
}
```

### 常见错误

#### 1. 参数验证错误

```json
{
  "success": false,
  "message": "缺少必需参数: email",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 2. 邮箱格式错误

```json
{
  "success": false,
  "message": "邮箱格式不正确",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 3. 数据库连接错误

```json
{
  "success": false,
  "message": "数据库配置缺失，请检查环境变量 DB_USER 和 DB_PASSWORD",
  "timestamp": "2024-01-01T12:00:00"
}
```

## 使用示例

### Python 示例

```python
import requests
import json

# API配置
api_url = "http://localhost:5000/api/monitor"

# 请求数据
data = {
    "email": "user@example.com",
    "keyword": "测试关键词"
}

# 发送请求
response = requests.post(
    api_url,
    json=data,
    headers={'Content-Type': 'application/json'}
)

# 处理响应
if response.status_code == 200:
    result = response.json()
    if result['success']:
        print("监控任务执行成功")
        print(f"新评论数量: {result['data']['new_comments_found']}")
    else:
        print(f"任务失败: {result['message']}")
else:
    print(f"请求失败: {response.status_code}")
```

### cURL 示例

```bash
# 健康检查
curl -X GET http://localhost:5000/api/health

# 执行监控任务
curl -X POST http://localhost:5000/api/monitor \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "keyword": "测试关键词"
  }'
```

### JavaScript 示例

```javascript
// 使用 fetch API
const monitorTask = async (email, keyword) => {
  try {
    const response = await fetch('http://localhost:5000/api/monitor', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        keyword: keyword
      })
    });
    
    const result = await response.json();
    
    if (response.ok && result.success) {
      console.log('监控任务执行成功');
      console.log('新评论数量:', result.data.new_comments_found);
    } else {
      console.error('任务失败:', result.message);
    }
  } catch (error) {
    console.error('请求失败:', error);
  }
};

// 调用示例
monitorTask('user@example.com', '测试关键词');
```

## 部署说明

### 开发环境

```bash
# 启动开发服务器
python app.py
```

### 生产环境

推荐使用 Gunicorn 部署：

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动生产服务器
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker 部署

创建 `Dockerfile`：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements_flask.txt .
RUN pip install -r requirements_flask.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

构建和运行：

```bash
# 构建镜像
docker build -t xhs-monitor-api .

# 运行容器
docker run -p 5000:5000 --env-file .env xhs-monitor-api
```

## 监控和日志

### 日志配置

API服务使用Python标准日志库，日志级别为INFO。可以通过修改 `app.py` 中的日志配置来调整：

```python
logging.basicConfig(
    level=logging.DEBUG,  # 修改为DEBUG级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 性能监控

可以集成APM工具如New Relic、DataDog等进行性能监控。

## 安全考虑

1. **环境变量**: 敏感信息（如数据库密码）通过环境变量配置
2. **输入验证**: API对所有输入参数进行验证
3. **错误处理**: 避免在错误信息中泄露敏感信息
4. **CORS**: 已配置CORS支持，生产环境建议限制允许的域名

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查 `.env` 文件中的数据库配置
   - 确认数据库服务正在运行
   - 验证网络连接

2. **Cookie获取失败**
   - 检查数据库中是否有有效的cookie记录
   - 确认 `xhs_cookies` 表结构正确

3. **监控URL为空**
   - 检查 `xhs_notes` 表中是否有对应用户的监控记录
   - 确认 `is_monitor` 字段设置为1

### 调试模式

开发环境下，API运行在调试模式，会显示详细的错误信息。生产环境建议关闭调试模式：

```python
app.run(debug=False)  # 关闭调试模式
```

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 实现监控任务API接口
- 添加健康检查功能
- 完善错误处理和参数验证