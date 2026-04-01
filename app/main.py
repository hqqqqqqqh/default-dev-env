"""
FastAPI 应用入口
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db import init_db, close_db, close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    try:
        await init_db()
    except Exception as e:
        # 开发阶段允许数据库未启动
        if settings.DEBUG:
            print(f"数据库连接失败: {e}")
        else:
            raise
    yield
    # 关闭时清理
    await close_db()
    await close_redis()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="工具站后台服务，提供多种实用功能的 API 接口",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok", "version": settings.APP_VERSION}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )