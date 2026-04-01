"""
pytest 测试配置
使用内存 SQLite + 测试 Redis
"""
import asyncio

import pytest
from tortoise import Tortoise
from tortoise.contrib.test import finalizer, initializer

# 测试数据库配置
TEST_DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {
                "file_path": ":memory:",
            },
        },
    },
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    """初始化测试数据库"""
    initializer(["app.models"], db_url="sqlite://:memory:")
    yield
    finalizer()


@pytest.fixture
async def redis_client():
    """测试 Redis 客户端"""
    import redis.asyncio as aioredis
    from app.core.config import settings

    client = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_TEST_DB}",
        encoding="utf-8",
        decode_responses=True,
    )
    yield client
    await client.close()
    # 清理测试数据
    await client.flushdb()


@pytest.fixture
def app():
    """测试 FastAPI 应用"""
    from fastapi.testclient import TestClient
    from app.main import app as fastapi_app
    return TestClient(fastapi_app)