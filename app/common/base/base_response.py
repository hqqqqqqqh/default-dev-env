"""
统一响应格式
"""
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """统一响应格式"""

    code: int = 0
    message: str = "success"
    data: T | None = None

    @classmethod
    def success(cls, data: T | None = None, message: str = "success") -> "BaseResponse[T]":
        """成功响应"""
        return cls(code=0, message=message, data=data)

    @classmethod
    def error(cls, code: int = 1, message: str = "error", data: T | None = None) -> "BaseResponse[T]":
        """错误响应"""
        return cls(code=code, message=message, data=data)