"""
API Key 数据模型
"""
import secrets
from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class ApiKey(Model):
    """API Key 模型"""

    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=64, unique=True, description="API Key")
    name = fields.CharField(max_length=100, description="Key 名称/用途说明")
    is_active = fields.BooleanField(default=True, description="是否启用")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    expires_at = fields.DatetimeField(null=True, description="过期时间")
    last_used_at = fields.DatetimeField(null=True, description="最后使用时间")
    usage_count = fields.IntField(default=0, description="使用次数")

    class Meta:
        table = "api_keys"
        table_description = "API Key 管理"

    @classmethod
    def generate_key(cls) -> str:
        """生成随机 API Key"""
        return f"tb_{secrets.token_hex(24)}"

    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

    def is_valid(self) -> bool:
        """检查是否有效"""
        return self.is_active and not self.is_expired()

    def __str__(self) -> str:
        return f"ApiKey({self.name})"