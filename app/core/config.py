"""
配置管理模块
使用 pydantic-settings 从环境变量加载配置
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # 应用配置
    APP_NAME: str = "Toolbox API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # 服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # MySQL 配置
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "toolbox"

    # Redis 配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0

    # 测试配置
    REDIS_TEST_DB: int = 15

    # API 校验配置
    API_KEY_HEADER: str = "X-API-Key"
    API_KEY_REQUIRED: bool = True
    API_KEY_CACHE_TTL: int = 300  # Key 缓存时间(秒)
    RATE_LIMIT_PER_MINUTE: int = 60  # 每分钟限制次数
    RATE_LIMIT_ENABLED: bool = True  # 是否启用频率限制

    # API 校验白名单路径（无需校验）
    API_WHITELIST_PATHS: list[str] = [
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
    ]

    @property
    def mysql_url(self) -> str:
        """MySQL 连接 URL"""
        return (
            f"mysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )

    @property
    def redis_url(self) -> str:
        """Redis 连接 URL"""
        if self.REDIS_PASSWORD:
            return (
                f"redis://:{self.REDIS_PASSWORD}"
                f"@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
            )
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


@lru_cache
def get_settings() -> Settings:
    """获取配置实例（缓存）"""
    return Settings()


settings = get_settings()