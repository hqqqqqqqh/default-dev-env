# 项目说明

## 项目概述

**项目名称**: Toolbox API
**项目描述**: 工具站后台服务，提供多种实用功能的 API 接口，支持灵活扩展

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

## 开发规范

### 模块组织

- `router/` 路由注册，`view/` 处理器实现
- `common/` 只放模块文件夹，不放单独文件
- 新业务模块统一在 `common/` 下创建
- 配置项都写在 `app/core/config.py`

### API 设计

- RESTful 风格
- 统一响应格式 (`app/common/base/base_response.py`)
- ORM 字段定义每行一个，便于 diff

### 代码风格

- 4 空格缩进
- `async def` 流程保持异步 I/O
- 模块/函数: `snake_case`
- 类: `PascalCase`
- 常量: `UPPER_SNAKE_CASE`

## 常用命令

```bash
# 开发
uv sync                              # 安装依赖
uv run python app/main.py            # 启动服务
uv run uvicorn app.main:app --reload # 热重载模式

# 数据库迁移
uv run aerich init-db                # 初始化
uv run aerich migrate --name <name>  # 生成迁移
uv run aerich upgrade                # 执行迁移
uv run aerich downgrade              # 回滚

# 异步任务
uv run taskiq worker app.taskiq.broker:broker  # 启动 worker

# 测试
uv run pytest                        # 运行测试
uv run pytest tests/api/test_xxx.py  # 单文件测试
```

## 测试规范

- 不要主动写测试，除非明确要求
- 测试使用内存 SQLite + 真实 Redis
- 建议通过 `REDIS_DB` 使用专用测试数据库

## Git 协作规范

### 分支策略

- `main`: 主分支，受保护，禁止直接推送
- `feature/*`: 功能分支，如 `feature/gold-api`
- `fix/*`: 修复分支，如 `fix/translate-error`

### 提交信息

```
<type>(<scope>): <description>

# 示例
feat(gold): 添加实时金价接口
fix(translate): 修复翻译超时问题
docs: 更新 API 文档
```

### AI 辅助开发规范

使用 AI 辅助开发时，AI 应遵循以下流程：

#### 强制规则

1. **严禁在 main 分支上直接开发**
   - 任何功能开发都必须从 main 创建新分支
   - 分支命名：`feature/<功能名>` 或 `fix/<问题名>`

2. **开发前必须创建分支**
   - AI 收到开发任务后，第一步就是创建分支
   - 即使是"小改动"也需要创建分支

3. **完成有意义的功能后主动提交**
   - 触发提交的时机：
     - 完成一个完整功能模块（如 API 校验机制）
     - 完成一个独立的修复（如某个 bug）
     - 完成一个独立文件（如新建 services/auth.py）
     - 任何逻辑上完整的改动
   - 目的：保留工作进度，支持最小代价回滚

4. **测试通过后才合并**
   - 合并前必须验证功能正常工作
   - 合并顺序：创建分支 → 开发 → 测试 → 提交 → 合并到 main → 删除分支

#### 执行流程

```
收到开发任务
    ↓
[第一步] git checkout main && git pull
    ↓
[第二步] git checkout -b feature/xxx
    ↓
[第三步] 开发代码
    ↓
[第四步] 完成功能后提交: git add + git commit
    ↓
[第五步] 功能测试（启动服务，curl 测试）
    ↓
[第六步] git checkout main && git merge feature/xxx
    ↓
[第七步] git branch -d feature/xxx
```

#### 提交规范

- commit message 遵循上述格式
- 一个 commit 对应一个逻辑功能
- 不要提交半成品代码

#### 禁止行为

- ❌ 在 main 分支上直接修改代码
- ❌ 跳过测试直接合并
- ❌ 一次性提交大量无关改动
- ❌ 开发到一半就合并（除非明确要求）

### PR 流程

1. 从 main 创建功能分支
2. 完成开发后创建 PR
3. 通过 Review 后合并

## 跨平台协作

### 换行符

- 统一使用 LF
- 配置: `git config --global core.autocrlf input`

### .gitignore

确保以下内容不被提交：
- `__pycache__/`、`*.pyc`
- `.venv/`、`venv/`
- `.env`、`.env.local`
- `*.log`、`logs/`

## 安全规范

### 禁止提交

- API Key、Token、证书
- 数据库密码、连接字符串
- `.env` 文件
- 私钥文件（`.pem`、`.key`）

### 检查方法

提交前告诉 AI：检查是否有敏感文件被暂存

## 重要规则

- 禁止硬编码 API Key
- 禁止跳过测试提交代码
- 禁止直接推送到 main 分支
- 新 API 必须有错误处理和日志

## 回复要求

全程使用中文回复

---

- 创建日期: 2026-04-01