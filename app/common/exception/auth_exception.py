"""
认证异常定义
"""
from fastapi import HTTPException, status


class AuthException(HTTPException):
    """认证异常基类"""

    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "认证失败",
        headers: dict | None = None,
    ):
        if headers is None:
            headers = {"WWW-Authenticate": "ApiKey"}
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class MissingApiKeyException(AuthException):
    """缺少 API Key"""

    def __init__(self):
        super().__init__(
            detail="缺少 API Key，请在请求头中添加 X-API-Key",
        )


class InvalidApiKeyException(AuthException):
    """无效的 API Key"""

    def __init__(self):
        super().__init__(
            detail="无效的 API Key",
        )


class ExpiredApiKeyException(AuthException):
    """API Key 已过期"""

    def __init__(self):
        super().__init__(
            detail="API Key 已过期",
        )


class RateLimitException(HTTPException):
    """频率限制异常"""

    def __init__(self, limit: int = 60):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"请求频率超限，每分钟最多 {limit} 次",
        )