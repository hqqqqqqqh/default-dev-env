"""
API Key 认证中间件
拦截请求进行 API Key 校验和频率限制
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.common.services.auth_service import auth_service
from app.core.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    """API Key 认证中间件"""

    async def dispatch(self, request: Request, call_next):
        """请求拦截处理"""

        # 1. 检查是否为白名单路径
        if auth_service.is_whitelisted(request.url.path):
            return await call_next(request)

        # 2. 检查是否禁用认证（开发环境可关闭）
        if not settings.API_KEY_REQUIRED:
            return await call_next(request)

        # 3. 获取 API Key
        api_key = request.headers.get(settings.API_KEY_HEADER)
        if not api_key:
            return self._error_response(401, "缺少 API Key，请在请求头中添加 X-API-Key")

        # 4. 校验 API Key
        try:
            await auth_service.validate_api_key(api_key)
        except Exception as e:
            error_msg = str(e.detail) if hasattr(e, "detail") else str(e)
            status_code = e.status_code if hasattr(e, "status_code") else 401
            return self._error_response(status_code, error_msg)

        # 5. 检查频率限制
        if not await auth_service.check_rate_limit(api_key):
            return self._error_response(429, f"请求频率超限，每分钟最多 {settings.RATE_LIMIT_PER_MINUTE} 次")

        # 6. 更新使用记录（异步，不影响响应速度）
        try:
            await auth_service.update_usage(api_key)
        except Exception:
            # 使用记录更新失败不影响请求处理
            pass

        # 7. 继续处理请求
        return await call_next(request)

    def _error_response(self, status_code: int, message: str) -> JSONResponse:
        """返回错误响应"""
        return JSONResponse(
            status_code=status_code,
            content={"code": status_code, "message": message, "data": None},
        )