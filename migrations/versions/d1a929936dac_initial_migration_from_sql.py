"""Initial migration from SQL

Revision ID: d1a929936dac
Revises: 
Create Date: 2025-12-18 14:01:38.899107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import re


# revision identifiers, used by Alembic.
revision: str = 'd1a929936dac'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def remove_sql_comments(sql_content):
    """移除SQL文件中的注释"""
    # 移除单行注释 (--)
    sql_content = re.sub(r'--.*?\n', '\n', sql_content)
    
    # 移除多行注释 (/* */)
    sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
    
    return sql_content


def upgrade() -> None:
    # 执行SQL初始化文件
    import os
    
    # 读取SQL文件内容
    sql_file = os.path.join(os.path.dirname(__file__), '../sql/init.sql')
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 移除注释
    sql_content = remove_sql_comments(sql_content)
    
    # 将SQL内容按语句分割
    # 匹配分号后面跟着换行符或文件结束的模式
    sql_statements = re.split(r';\s*(?=\n|$)', sql_content)
    
    # 获取数据库连接
    conn = op.get_bind()
    
    # 使用原生连接执行SQL，绕过SQLAlchemy的参数解析
    raw_conn = conn.connection
    cursor = raw_conn.cursor()
    
    try:
        # 逐个执行SQL语句
        for statement in sql_statements:
            statement = statement.strip()
            if statement:  # 跳过空语句
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print(f"执行SQL语句失败: {statement[:100]}...")
                    print(f"错误信息: {e}")
                    raw_conn.rollback()
                    raise
        
        # 提交事务
        raw_conn.commit()
    finally:
        # 关闭游标
        cursor.close()


def downgrade() -> None:
    """Downgrade schema."""
    pass