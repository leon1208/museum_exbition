# 导入项目的 SQLAlchemy 实例和模型
import sys
import os

# 添加项目根目录到 Python 路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from alembic import context
from sqlalchemy import engine_from_config, pool
from flask import Flask

# 导入项目的 SQLAlchemy 实例
from ruoyi_admin.ext import db
# 从 ruoyi_common.ruoyi.config 导入 RuoYiConfigLoader
from ruoyi_common.ruoyi.config import RuoYiConfigLoader

# 导入所有模型，确保它们被 Alembic 识别
from ruoyi_system.domain.po import *
from ruoyi_generator.domain.po import *
from ruoyi_apscheduler.domain.po import *
from exb_museum.domain.po import *

# 创建 Flask 应用实例
app = Flask(__name__)

# 加载配置
config_loader = RuoYiConfigLoader(os.path.join(PROJECT_ROOT, 'ruoyi_admin'))
# 设置应用配置
app.config.update(config_loader._raw_data.get("flask", {}))

# 初始化 SQLAlchemy 实例
with app.app_context():
    db.init_app(app)

# 从 context 获取 config 对象
config = context.config

# 配置 target_metadata，使用项目的 SQLAlchemy metadata
target_metadata = db.metadata

# 修改 run_migrations_offline 函数
def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# 修改 run_migrations_online 函数
def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    with app.app_context():
        connectable = db.engine

        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata
            )

            with context.begin_transaction():
                context.run_migrations()

# 根据命令行参数决定使用哪种迁移模式
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()