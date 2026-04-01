"""
数据库连接配置
"""
from tortoise import Tortoise

from app.core.config import settings

# Tortoise ORM 配置
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": settings.MYSQL_HOST,
                "port": settings.MYSQL_PORT,
                "user": settings.MYSQL_USER,
                "password": settings.MYSQL_PASSWORD,
                "database": settings.MYSQL_DATABASE,
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


async def init_db() -> None:
    """初始化数据库连接"""
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_db() -> None:
    """关闭数据库连接"""
    await Tortoise.close_connections()


# Redis 客户端
_redis_client: None = None


async def get_redis():
    """获取 Redis 客户端"""
    global _redis_client
    if _redis_client is None:
        import redis.asyncio as aioredis
        _redis_client = aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client


async def close_redis() -> None:
    """关闭 Redis 连接"""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None