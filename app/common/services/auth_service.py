"""
API Key 认证服务
提供 Key 校验、缓存、频率限制功能
"""
from datetime import datetime

from app.core.config import settings
from app.db import get_redis
from app.models.api_key import ApiKey


class AuthService:
    """API Key 认证服务"""

    # Redis Key 前缀
    CACHE_PREFIX = "apikey:cache:"
    RATE_LIMIT_PREFIX = "apikey:ratelimit:"

    async def validate_api_key(self, api_key: str) -> ApiKey:
        """
        校验 API Key

        Args:
            api_key: 待校验的 API Key

        Returns:
            ApiKey: 校验成功返回 ApiKey 对象

        Raises:
            InvalidApiKeyException: 无效的 Key
            ExpiredApiKeyException: 已过期的 Key
        """
        from app.common.exception.auth_exception import (
            ExpiredApiKeyException,
            InvalidApiKeyException,
        )

        # 先尝试从 Redis 缓存获取
        cached = await self._get_cached_key(api_key)
        if cached:
            if cached.get("expired"):
                raise ExpiredApiKeyException()
            if not cached.get("active"):
                raise InvalidApiKeyException()
            # 返回一个简化的 ApiKey 对象（从缓存构造）
            return self._build_key_from_cache(cached)

        # 缓存不存在，从数据库查询
        key_obj = await ApiKey.filter(key=api_key).first()
        if key_obj is None:
            raise InvalidApiKeyException()

        if key_obj.is_expired():
            raise ExpiredApiKeyException()

        if not key_obj.is_active:
            raise InvalidApiKeyException()

        # 写入缓存
        await self._cache_key(key_obj)

        return key_obj

    async def check_rate_limit(self, api_key: str) -> bool:
        """
        检查频率限制

        Args:
            api_key: API Key

        Returns:
            bool: 是否允许请求（True=允许，False=超限）
        """
        if not settings.RATE_LIMIT_ENABLED:
            return True

        redis = await get_redis()
        key = f"{self.RATE_LIMIT_PREFIX}{api_key}"

        # 获取当前计数
        count = await redis.get(key)
        if count is None:
            # 第一次请求，设置计数并设置 60 秒过期
            await redis.setex(key, 60, 1)
            return True

        if int(count) >= settings.RATE_LIMIT_PER_MINUTE:
            return False

        # 增加计数
        await redis.incr(key)
        return True

    async def update_usage(self, api_key: str) -> None:
        """
        更新 API Key 使用记录

        Args:
            api_key: API Key
        """
        from tortoise.expressions import F

        # 更新数据库
        await ApiKey.filter(key=api_key).update(
            last_used_at=datetime.now(),
            usage_count=F("usage_count") + 1,
        )

    async def _get_cached_key(self, api_key: str) -> dict | None:
        """从 Redis 获取缓存的 Key 信息"""
        redis = await get_redis()
        key = f"{self.CACHE_PREFIX}{api_key}"
        data = await redis.get(key)
        if data:
            import json
            return json.loads(data)
        return None

    async def _cache_key(self, key_obj: ApiKey) -> None:
        """将 Key 信息缓存到 Redis"""
        redis = await get_redis()
        key = f"{self.CACHE_PREFIX}{key_obj.key}"
        import json

        data = {
            "id": key_obj.id,
            "name": key_obj.name,
            "active": key_obj.is_active,
            "expired": key_obj.is_expired(),
        }
        await redis.setex(key, settings.API_KEY_CACHE_TTL, json.dumps(data))

    def _build_key_from_cache(self, cached: dict) -> ApiKey:
        """从缓存数据构建 ApiKey 对象"""
        key_obj = ApiKey()
        key_obj.id = cached["id"]
        key_obj.name = cached["name"]
        key_obj.is_active = cached["active"]
        return key_obj

    def is_whitelisted(self, path: str) -> bool:
        """检查路径是否在白名单中"""
        for whitelist_path in settings.API_WHITELIST_PATHS:
            if path.startswith(whitelist_path):
                return True
        return False


# 全局认证服务实例
auth_service = AuthService()