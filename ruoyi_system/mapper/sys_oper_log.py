# -*- coding: utf-8 -*-
# @Author  : YY

import re
from typing import List, Optional
from flask import g
from sqlalchemy import delete, insert, select

from ruoyi_common.base.model import ExtraModel
from ruoyi_common.sqlalchemy.model import ColumnEntityList
from ruoyi_common.sqlalchemy.transaction import Transactional
from ruoyi_system.domain.entity import SysOperLog
from ruoyi_admin.ext import db
from ruoyi_system.domain.po import SysOperLogPo


class SysOperLogMapper:
    
    """
    操作日志的数据访问层
    """
    
    default_fields = {
        "oper_id", "title", "business_type", "method", "request_method",
        "operator_type", "oper_name", "dept_name", "oper_url", "oper_ip",
        "oper_location", "oper_param", "json_result", "status", "error_msg",
        "oper_time"
    }
    
    default_columns = ColumnEntityList(SysOperLogPo, default_fields)
    
    @classmethod
    def select_operlog_list(cls, oper: Optional[SysOperLog])-> List[SysOperLog]:
        '''
        查询系统操作日志集合
        
        Args:
            oper (Optional[SysOperLog]): 操作日志对象
            
        Returns:
            List[SysOperLog]: 操作日志集合
        '''
        criterions = []
        if oper:
            if oper.oper_ip:
                criterions.append(SysOperLogPo.oper_ip.like(f'%{oper.oper_ip}%'))
            if oper.status is not None:
                criterions.append(SysOperLogPo.status == oper.status)
            if oper.oper_name:
                criterions.append(SysOperLogPo.oper_name.like(f'%{oper.oper_name}%'))
            cls._append_extra_criterions(criterions)
        stmt = select(*cls.default_columns)
        if criterions:
            stmt = stmt.where(*criterions)
        stmt = cls._apply_sorting(stmt)
        
        if "criterian_meta" in g and g.criterian_meta.page:
            g.criterian_meta.page.stmt = stmt
        
        rows = db.session.execute(stmt).all()
        return [cls.default_columns.cast(row, SysOperLog) for row in rows]
    
    @classmethod
    @Transactional(db.session)
    def insert_operlog(cls, oper: SysOperLog) -> int:
        '''
        新增操作日志
        
        Args:
            oper (SysOperLog): 操作日志对象
            
        Returns:
            int: 新增记录的ID
        '''
        fields = {
            "title", "business_type", "method", "request_method","oper_time",
            "operator_type", "oper_name", "dept_name", "oper_url", "oper_ip",
            "oper_location", "oper_param", "json_result", "status", "error_msg"
        }
        data = oper.model_dump(
            include=fields, exclude_none=True
        )
        stmt = insert(SysOperLogPo).values(data)
        out = db.session.execute(stmt).inserted_primary_key
        return out[0] if out else 0

    @classmethod
    def _append_extra_criterions(cls, criterions:list):
        if "criterian_meta" not in g or not g.criterian_meta.extra:
            return
        extra:ExtraModel = g.criterian_meta.extra
        if getattr(extra, "begin_time", None):
            criterions.append(SysOperLogPo.oper_time >= extra.begin_time)
        if getattr(extra, "end_time", None):
            criterions.append(SysOperLogPo.oper_time <= extra.end_time)

    @classmethod
    def _apply_sorting(cls, stmt):
        sort = getattr(getattr(g, "criterian_meta", None), "sort", None)
        order_columns = []
        if sort and sort.order_by_column:
            for alias in sort.order_by_column:
                field_name = cls._camel_to_snake(alias)
                column = getattr(SysOperLogPo, field_name, None)
                if not column:
                    continue
                if sort.is_asc == "asc":
                    order_columns.append(column.asc())
                else:
                    order_columns.append(column.desc())
        if not order_columns:
            order_columns.append(SysOperLogPo.oper_time.desc())
        return stmt.order_by(*order_columns)

    @staticmethod
    def _camel_to_snake(value:str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @classmethod
    @Transactional(db.session)
    def delete_operlog_by_ids(cls, ids: List[int]) -> int:
        '''
        批量删除系统操作日志
        
        Args:
            ids (List[int]): 操作日志ID列表
            
        Returns:
            int: 删除的记录数
        '''
        stmt = delete(SysOperLogPo).where(SysOperLogPo.oper_id.in_(ids))
        return db.session.execute(stmt).rowcount
    
    @classmethod
    @Transactional(db.session)
    def clean_operlog(cls) -> int:
        '''
        清空操作日志
        
        Returns:
            int: 删除的记录数
        '''
        stmt = delete(SysOperLogPo)
        return db.session.execute(stmt).rowcount
    
    @classmethod
    def select_operlog_by_id(cls, id:int) -> Optional[SysOperLog]:
        '''
        查询操作日志详细
        
        Args:
            id (int): 操作日志ID
            
        Returns:
            Optional[SysOperLog]: 操作日志对象
        '''
        stmt = select(*cls.default_columns).where(SysOperLogPo.oper_id == id)
        row = db.session.execute(stmt).one_or_none()
        return cls.default_columns.cast(row, SysOperLog) if row else None
