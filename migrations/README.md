# Alembic 数据库迁移指南

## 概述

Alembic 是一个用于 SQLAlchemy 的数据库迁移工具，用于管理数据库模式的变更。本项目使用 Alembic 来处理数据库结构的升级和降级。使用前需确保/ruoyi_admin/config/.env中配置的数据库连接字符串正确。

## 基本命令

### 生成迁移脚本

```bash
# 自动检测模型变更并生成迁移脚本
alembic revision --autogenerate -m "描述迁移内容"

# 生成空的迁移脚本（手动编写变更内容）
alembic revision -m "描述迁移内容"
```

### 执行迁移

```bash
# 应用所有未应用的迁移（升级到最新版本）
alembic upgrade head

# 回滚到上一个版本
alembic downgrade -1

# 回滚到指定版本
alembic downgrade <revision_id>

# 回滚到初始状态
alembic downgrade base

# 升级到指定版本
alembic upgrade <revision_id>
```

### 查看状态

```bash
# 查看当前数据库版本
alembic current

# 查看历史记录
alembic history

# 查看历史记录的详细信息
alembic history -v

# 查看待应用的迁移
alembic show head
```

## 配置文件说明

### alembic.ini

- `script_location`: 迁移脚本存放位置（默认为 `migrations`）
- `sqlalchemy.url`: 数据库连接字符串，这里不需要修改，alembic会根据项目的配置自动读取/ruoyi_admin/config/.env中配置的数据库连接进行schema迁移。
- `truncate_slug_length`: 迁移文件名描述的最大长度

### migrations/env.py

此文件配置了 Alembic 的运行环境，主要功能包括：

- 设置 Flask 应用上下文
- 配置 SQLAlchemy 数据库连接
- 导入项目中的所有模型，确保 Alembic 能识别所有表结构

## 迁移脚本结构

每个迁移脚本包含以下部分：

- `revision`: 当前迁移的唯一标识符
- `down_revision`: 上一个迁移的标识符
- `upgrade()`: 升级数据库的函数
- `downgrade()`: 降级数据库的函数

## 常用操作示例

### 1. 添加新表

```bash
# 修改模型后，生成迁移脚本
alembic revision --autogenerate -m "添加用户表"

# 应用迁移
alembic upgrade head
```

### 2. 修改表结构

```bash
# 修改模型后，生成迁移脚本
alembic revision --autogenerate -m "修改用户表添加邮箱字段"

# 应用迁移
alembic upgrade head
```

### 3. 删除表或字段

```bash
# 修改模型后，生成迁移脚本
alembic revision --autogenerate -m "删除用户表的电话字段"

# 注意：删除操作需要谨慎，建议先备份数据
alembic upgrade head
```

## 注意事项

1. **模型导入**: 在 `migrations/env.py` 中必须导入所有需要跟踪的模型，否则 Alembic 无法检测到这些表的变更。

2. **数据库连接**: 确保 `alembic.ini` 中的数据库连接字符串正确配置。

3. **备份数据**: 在执行可能破坏性操作（如删除表）之前，请务必备份数据库。

4. **测试迁移**: 在生产环境执行迁移前，先在开发或测试环境中测试迁移脚本。

5. **手动编辑**: 有时自动生成的迁移脚本可能不完全准确，需要手动编辑以确保正确性。

## 常见问题

### 1. 自动迁移未检测到变更

- 检查是否在 `migrations/env.py` 中导入了相关模型
- 确认模型确实发生了结构上的变更

### 2. 迁移冲突

- 如果多人同时进行数据库变更，可能出现版本冲突
- 需要手动合并迁移历史或重新生成迁移脚本

### 3. 回滚失败

- 某些操作（如删除表）可能无法安全回滚
- 在执行迁移前应仔细检查 `downgrade()` 函数的实现

## 版本管理

- 每个迁移文件都有唯一的 revision ID
- 迁移文件存放在 `migrations/versions/` 目录中
- Alembic 会自动跟踪已应用的迁移版本