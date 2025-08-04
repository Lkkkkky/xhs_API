from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv
from xhs_api_class import XhsAPI
from db_manager import DatabaseCookieManager

# 加载环境变量
load_dotenv()

# 创建FastAPI应用实例
app = FastAPI(
    title="小红书API服务",
    description="基于FastAPI封装的小红书数据获取API",
    version="1.0.0"
)

# 创建XhsAPI实例
xhs_api = XhsAPI()

# 初始化数据库管理器
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_manager = DatabaseCookieManager(
    user=db_user,
    password=db_password
)

def get_cookies_str() -> str:
    """获取随机cookies字符串"""
    cookies_str = db_manager.get_random_cookie()
    if not cookies_str:
        raise HTTPException(status_code=500, detail="无法获取有效的cookies")
    return cookies_str

# 请求模型定义
class CommentRequest(BaseModel):
    note_url: str
    cursor: Optional[str] = ""

class SearchRequest(BaseModel):
    keyword: str
    num: int = 10

class NoteInfoRequest(BaseModel):
    note_url: str

class MonitorRequest(BaseModel):
    note_url: str
    user_info: str
    keyword: str
    interval: Optional[int] = 60

class ReplyRequest(BaseModel):
    note_url: str
    comment_id: str
    content: str

# API路由定义
@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "小红书API服务",
        "version": "1.0.0",
        "endpoints": [
            "/comments - 获取笔记评论",
            "/search - 搜索笔记",
            "/note-info - 获取笔记信息",
            "/monitor - 监控笔记评论",
            "/reply - 回复评论"
        ]
    }

@app.post("/get_comments")
async def get_comments(request: CommentRequest):
    """获取小红书笔记评论
    
    Args:
        request: 包含note_url, cursor的请求体
        
    Returns:
        评论列表
    """
    try:
        cookies_str = get_cookies_str()
        comments_list = []
        result = xhs_api.get_comments(
            cookies_str=cookies_str,
            ori_url=request.note_url,
            cursor=request.cursor,
            comments_list=comments_list
        )
        return {
            "success": True,
            "data": result,
            "count": len(result) if result else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取评论失败: {str(e)}")

@app.post("/search_comments_by_keyword")
async def search_comments_by_keyword(request: SearchRequest):
    """根据关键词搜索笔记下的评论
    
    Args:
        request: 包含keyword, num的请求体
        
    Returns:
        评论列表
    """
    try:
        cookies_str = get_cookies_str()
        # 清空之前的搜索结果
        xhs_api.comments_list = []
        xhs_api.comments_list = xhs_api.search_comments_by_keyword(
            cookies_str=cookies_str,
            keyword=request.keyword,
            num=request.num,
            comments_list=xhs_api.comments_list
        )
        return {
            "success": True,
            "data": xhs_api.comments_list if xhs_api.comments_list else [],
            "count": len(xhs_api.comments_list) if xhs_api.comments_list else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

@app.post("/search_notes")
async def search_notes(request: SearchRequest):
    """根据关键词搜索笔记
    
    Args:
        request: 包含keyword, num的请求体
        
    Returns:
        搜索结果
    """
    try:
        cookies_str = get_cookies_str()
        # 清空之前的搜索结果
        xhs_api.note_list = []
        xhs_api.search_notes_by_keyword(
            cookies_str=cookies_str,
            keyword=request.keyword,
            num=request.num
        )
        return {
            "success": True,
            "data": xhs_api.note_list,
            "count": len(xhs_api.note_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

@app.post("/get_note_info")
async def get_note_info(request: NoteInfoRequest):
    """获取笔记详细信息
    
    Args:
        request: 包含note_url的请求体
        
    Returns:
        笔记信息
    """
    try:
        cookies_str = get_cookies_str()
        result = xhs_api.get_note_info(
            cookies_str=cookies_str,
            url=request.note_url
        )
        if result:
            return {
                "success": True,
                "data": result
            }
        else:
            raise HTTPException(status_code=404, detail="笔记信息获取失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取笔记信息失败: {str(e)}")

@app.post("/monitor")
async def monitor_comments(request: MonitorRequest):
    """监控笔记评论变化
    
    Args:
        request: 包含note_url, user_info, keyword, interval的请求体
        
    Returns:
        监控结果
    """
    try:
        cookies_str = get_cookies_str()
        result = xhs_api.monitor_comments(
            cookies_str=cookies_str,
            note_url=request.note_url,
            userInfo=request.user_info,
            keyword=request.keyword,
            interval=request.interval
        )
        if result:
            return {
                "success": True,
                "data": result,
                "count": len(result)
            }
        else:
            return {
                "success": False,
                "message": "没有获取到评论数据"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"监控失败: {str(e)}")

@app.post("/reply_comment")
async def reply_comment(request: ReplyRequest):
    """回复评论
    
    Args:
        request: 包含note_url, comment_id, content的请求体
        
    Returns:
        回复结果
    """
    try:
        cookies_str = get_cookies_str()
        result = xhs_api.reply_comment(
            cookies_str=cookies_str,
            note_url=request.note_url,
            comment_id=request.comment_id,
            content=request.content
        )
        return {
            "success": True,
            "message": "回复成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"回复失败: {str(e)}")

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": "小红书API服务"}

if __name__ == "__main__":
    # 启动服务器
    uvicorn.run(
        "fastapi_app:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info"
    )