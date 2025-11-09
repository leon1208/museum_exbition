# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: column_service.py

from typing import List, Tuple
from ruoyi_generator.domain.entity import GenTableColumn
from ruoyi_generator.mapper import gen_table_column_mapper


class GenTableColumnService:
    """代码生成表列服务类"""
    
    def select_gen_table_column_list_by_table_id(self, table_id: int) -> Tuple[List[GenTableColumn], int]:
        """
        根据表ID查询代码生成表列列表
        
        Args:
            table_id (int): 表ID
            
        Returns:
            Tuple[List[GenTableColumn], int]: 代码生成表列列表和总数
        """
        columns = gen_table_column_mapper.select_list_by_table_id(table_id)
        # 编辑表时应该显示所有字段，不需要分页
        # 返回所有字段和总数
        return columns, len(columns) if columns else 0

    def insert_gen_table_column(self, gen_table_column: GenTableColumn) -> bool:
        """
        插入代码生成表列
        
        Args:
            gen_table_column (GenTableColumn): 代码生成表列对象
            
        Returns:
            bool: 是否成功
        """
        try:
            gen_table_column.create_by = "admin"
            result = gen_table_column_mapper.insert(gen_table_column)
            return result > 0
        except Exception as e:
            print(f"插入代码生成表列失败: {e}")
            return False

    def update_gen_table_column(self, gen_table_column: GenTableColumn) -> bool:
        """
        更新代码生成表列
        
        Args:
            gen_table_column (GenTableColumn): 代码生成表列对象
            
        Returns:
            bool: 是否成功
        """
        try:
            gen_table_column.update_by = "admin"
            gen_table_column_mapper.update(gen_table_column)
            return True
        except Exception as e:
            print(f"更新代码生成表列失败: {e}")
            return False

    def delete_gen_table_column_by_id(self, column_id: int) -> bool:
        """
        根据ID删除代码生成表列
        
        Args:
            column_id (int): 列ID
            
        Returns:
            bool: 是否成功
        """
        try:
            gen_table_column_mapper.delete_by_id(column_id)
            return True
        except Exception as e:
            print(f"删除代码生成表列失败: {e}")
            return False
