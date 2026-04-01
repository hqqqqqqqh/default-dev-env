# Toolbox API

工具站后台服务，提供多种实用功能的 API 接口。

## 技术栈

- Python >= 3.10
- FastAPI
- Tortoise ORM + MySQL
- Redis
- Taskiq (异步任务)

## 快速开始

```bash
# 安装依赖
uv sync

# 复制环境变量
cp .env.example .env

# 启动服务
uv run python app/main.py
```

## 数据库迁移

```bash
uv run aerich init-db
uv run aerich migrate --name <name>
uv run aerich upgrade
```

## 测试

```bash
uv run pytest
```
