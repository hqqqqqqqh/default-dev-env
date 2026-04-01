#!/usr/bin/env python
"""
API Key 管理脚本
用于创建、查看、禁用 API Key
"""
import argparse
import asyncio
import sys
from datetime import datetime, timedelta

# 添加项目路径
sys.path.insert(0, ".")

from tortoise import Tortoise

from app.db import TORTOISE_ORM
from app.models.api_key import ApiKey


async def create_key(name: str, expire_days: int | None = None):
    """创建新的 API Key"""
    await Tortoise.init(config=TORTOISE_ORM)

    key = ApiKey.generate_key()
    expires_at = None
    if expire_days:
        expires_at = datetime.now() + timedelta(days=expire_days)

    api_key = await ApiKey.create(
        key=key,
        name=name,
        expires_at=expires_at,
    )

    print(f"✅ API Key 创建成功！")
    print(f"   ID: {api_key.id}")
    print(f"   名称: {api_key.name}")
    print(f"   Key: {api_key.key}")
    if api_key.expires_at:
        print(f"   过期时间: {api_key.expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"   过期时间: 永不过期")

    await Tortoise.close_connections()


async def list_keys():
    """列出所有 API Key"""
    await Tortoise.init(config=TORTOISE_ORM)

    keys = await ApiKey.all().order_by("-created_at")

    if not keys:
        print("暂无 API Key")
        return

    print(f"共有 {len(keys)} 个 API Key:")
    print("-" * 80)
    for k in keys:
        status = "✅ 有效" if k.is_valid() else ("⏰ 过期" if k.is_expired() else "❌ 禁用")
        expire_str = k.expires_at.strftime("%Y-%m-%d") if k.expires_at else "永不过期"
        print(f"  [{k.id}] {k.name}")
        print(f"       Key: {k.key}")
        print(f"       状态: {status} | 过期: {expire_str} | 使用次数: {k.usage_count}")
        print("-" * 80)

    await Tortoise.close_connections()


async def disable_key(key_id: int):
    """禁用 API Key"""
    await Tortoise.init(config=TORTOISE_ORM)

    api_key = await ApiKey.get_or_none(id=key_id)
    if not api_key:
        print(f"❌ 未找到 ID={key_id} 的 API Key")
        return

    api_key.is_active = False
    await api_key.save()

    print(f"✅ API Key 已禁用: {api_key.name}")

    await Tortoise.close_connections()


async def enable_key(key_id: int):
    """启用 API Key"""
    await Tortoise.init(config=TORTOISE_ORM)

    api_key = await ApiKey.get_or_none(id=key_id)
    if not api_key:
        print(f"❌ 未找到 ID={key_id} 的 API Key")
        return

    api_key.is_active = True
    await api_key.save()

    print(f"✅ API Key 已启用: {api_key.name}")

    await Tortoise.close_connections()


async def delete_key(key_id: int):
    """删除 API Key"""
    await Tortoise.init(config=TORTOISE_ORM)

    api_key = await ApiKey.get_or_none(id=key_id)
    if not api_key:
        print(f"❌ 未找到 ID={key_id} 的 API Key")
        return

    await api_key.delete()

    print(f"✅ API Key 已删除: {api_key.name}")

    await Tortoise.close_connections()


def main():
    parser = argparse.ArgumentParser(description="API Key 管理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 创建命令
    create_parser = subparsers.add_parser("create", help="创建新的 API Key")
    create_parser.add_argument("-n", "--name", required=True, help="Key 名称/用途")
    create_parser.add_argument("-e", "--expire", type=int, default=None, help="有效期(天)")

    # 列表命令
    subparsers.add_parser("list", help="列出所有 API Key")

    # 禁用命令
    disable_parser = subparsers.add_parser("disable", help="禁用 API Key")
    disable_parser.add_argument("-i", "--id", required=True, type=int, help="Key ID")

    # 启用命令
    enable_parser = subparsers.add_parser("enable", help="启用 API Key")
    enable_parser.add_argument("-i", "--id", required=True, type=int, help="Key ID")

    # 删除命令
    delete_parser = subparsers.add_parser("delete", help="删除 API Key")
    delete_parser.add_argument("-i", "--id", required=True, type=int, help="Key ID")

    args = parser.parse_args()

    if args.command == "create":
        asyncio.run(create_key(args.name, args.expire))
    elif args.command == "list":
        asyncio.run(list_keys())
    elif args.command == "disable":
        asyncio.run(disable_key(args.id))
    elif args.command == "enable":
        asyncio.run(enable_key(args.id))
    elif args.command == "delete":
        asyncio.run(delete_key(args.id))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()