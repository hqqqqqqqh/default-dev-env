# Toolbox API

工具站后台服务，提供多种实用功能的 API 接口，支持灵活扩展。

## 技术栈

- **语言**: Python >= 3.10
- **框架**: FastAPI
- **数据库**: Redis (缓存) + MySQL (持久化)
- **ORM**: Tortoise ORM
- **异步任务**: Taskiq
- **包管理**: uv

## 项目结构

```
.
├── app/                  # FastAPI 应用
│   ├── core/             # 配置文件
│   ├── router/           # 路由定义
│   ├── view/             # 请求处理器
│   ├── models/           # 数据模型 (ORM)
│   ├── common/           # 公共模块（只放模块文件夹）
│   │   ├── middlewares/  # 中间件
│   │   ├── utils/        # 工具函数
│   │   ├── exception/    # 异常定义与处理
│   │   ├── base/         # 基础类（响应基类等）
│   │   └── services/     # 公共服务
│   ├── db/               # 数据库/Redis 连接
│   ├── taskiq/           # 异步任务配置
│   │   └── tasks/        # 任务定义
│   └── main.py           # 应用入口
├── tests/                # pytest 测试
│   └── conftest.py       # 测试 fixtures
├── migrations/           # 数据库迁移 (Aerich)
├── docs/                 # 项目文档
├── scripts/              # 脚本文件
├── logs/                 # 日志文件
├── pyproject.toml        # 项目配置
└── .env.example          # 环境变量示例
```

## 快速开始

```bash
# 安装依赖
uv sync

# 复制环境变量
cp .env.example .env

# 启动服务
uv run python app/main.py

# 热重载模式
uv run uvicorn app.main:app --reload
```

## 数据库迁移

```bash
uv run aerich init-db                # 初始化
uv run aerich migrate --name <name>  # 生成迁移
uv run aerich upgrade                # 执行迁移
uv run aerich downgrade              # 回滚
```

## 异步任务

```bash
uv run taskiq worker app.taskiq.broker:broker  # 启动 worker
```

## 测试

```bash
uv run pytest                        # 运行测试
uv run pytest tests/api/test_xxx.py  # 单文件测试
```

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 开发规范

详见 [CLAUDE.md](./CLAUDE.md)

### AI 协作规范

使用 AI 辅助开发时，AI 应自动判断是否需要 commit：
- 完成有意义的功能或模块后，主动提交代码
- commit message 遵循 `<type>(<scope>): <description>` 格式
- 无需等待用户明确要求才提交