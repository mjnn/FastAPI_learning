import uvicorn

from app.core.config import settings

if __name__ == "__main__":
    """启动FastAPI应用"""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,  # 开发环境自动重载
        workers=1  # 生产环境可调整为多worker
    )