"""
Taskiq Broker 配置
"""
from taskiq import InMemoryBroker
from taskiq_redis import RedisQueueBroker

from app.core.config import settings

# 使用 Redis 作为 broker（生产环境）
# 开发环境可使用 InMemoryBroker
if settings.DEBUG:
    broker = InMemoryBroker()
else:
    broker = RedisQueueBroker(
        url=settings.redis_url,
        queue_name="taskiq:queue",
    )