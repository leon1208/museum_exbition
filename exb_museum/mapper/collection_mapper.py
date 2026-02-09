# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: collection_mapper.py
# @Time    : 2026-01-08 11:23:01

from typing import List
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from exb_museum.domain.entity import Collection
from exb_museum.domain.po import CollectionPo, MuseumPo
from ruoyi_system.domain.po import SysDeptPo

class CollectionMapper:
    """藏品信息表Mapper"""

    @staticmethod
    def select_collection_list(collection: Collection) -> List[Collection]:
        """
        查询藏品信息表列表

        Args:
            collection (collection): 藏品信息表对象

        Returns:
            List[collection]: 藏品信息表列表
        """
        # 构建查询条件
        stmt = select(CollectionPo) \
            .join(MuseumPo, CollectionPo.museum_id == MuseumPo.museum_id) \
            .join(SysDeptPo, MuseumPo.dept_id == SysDeptPo.dept_id)

        if collection.collection_name:
            stmt = stmt.where(CollectionPo.collection_name.like("%" + str(collection.collection_name) + "%"))

        if collection.collection_type is not None:
            stmt = stmt.where(CollectionPo.collection_type == collection.collection_type)

        if collection.exhibition_id is not None:
            stmt = stmt.where(CollectionPo.exhibition_id == collection.exhibition_id)

        if collection.museum_id is not None:
            stmt = stmt.where(CollectionPo.museum_id == collection.museum_id)

        if collection.status is not None:
            stmt = stmt.where(CollectionPo.status == collection.status)

        if "criterian_meta" in g and g.criterian_meta.scope is not None:
            stmt = stmt.where(g.criterian_meta.scope)

        if "criterian_meta" in g and g.criterian_meta.page:
            g.criterian_meta.page.stmt = stmt

        result = db.session.execute(stmt).scalars().all()
        return [Collection.model_validate(item) for item in result] if result else []

    
    @staticmethod
    def select_collection_by_id(collection_id: int) -> Collection:
        """
        根据ID查询藏品信息表

        Args:
            collection_id (int): 藏品ID

        Returns:
            collection: 藏品信息表对象
        """
        result = db.session.get(CollectionPo, collection_id)
        return Collection.model_validate(result) if result else None
    
    def select_collection_by_ids(collection_ids: List[int]) -> List[Collection]:
        """
        根据ID列表查询藏品信息表列表

        Args:
            collection_ids (List[int]): 藏品ID列表

        Returns:
            List[collection]: 藏品信息表列表
        """
        if not collection_ids or len(collection_ids) == 0:
            return []

        stmt = select(CollectionPo).where(CollectionPo.collection_id.in_(collection_ids))
        result = db.session.execute(stmt).scalars().all()
        return [Collection.model_validate(item) for item in result] if result else []

    @staticmethod
    def insert_collection(collection: Collection) -> int:
        """
        新增藏品信息表

        Args:
            collection (collection): 藏品信息表对象

        Returns:
            int: 插入的记录数
        """
        now = datetime.now()
        new_po = CollectionPo()
        new_po.collection_id = collection.collection_id
        new_po.collection_name = collection.collection_name
        new_po.collection_type = collection.collection_type
        new_po.size_info = collection.size_info
        new_po.material = collection.material
        new_po.age = collection.age
        new_po.author = collection.author
        new_po.description = collection.description
        new_po.exhibition_id = collection.exhibition_id
        new_po.museum_id = collection.museum_id
        new_po.status = collection.status
        new_po.del_flag = collection.del_flag
        new_po.create_by = collection.create_by
        new_po.create_time = collection.create_time or now
        new_po.update_by = collection.update_by
        new_po.update_time = collection.update_time or now
        new_po.remark = collection.remark
        db.session.add(new_po)
        
        db.session.flush()
        collection.collection_id = new_po.collection_id
        return 1

    @staticmethod
    def update_collection(collection: Collection) -> int:
        """
        修改藏品信息表

        Args:
            collection (collection): 藏品信息表对象

        Returns:
            int: 更新的记录数
        """
        existing = db.session.get(CollectionPo, collection.collection_id)
        if not existing:
            return 0
        now = datetime.now()
        # 主键不参与更新
        existing.collection_name = collection.collection_name
        existing.collection_type = collection.collection_type
        existing.size_info = collection.size_info
        existing.material = collection.material
        existing.age = collection.age
        existing.author = collection.author
        existing.description = collection.description
        existing.exhibition_id = collection.exhibition_id
        existing.museum_id = collection.museum_id
        existing.status = collection.status
        existing.del_flag = collection.del_flag
        existing.create_by = collection.create_by
        existing.create_time = collection.create_time
        existing.update_by = collection.update_by
        existing.update_time = collection.update_time or now
        existing.remark = collection.remark
        return 1

    @staticmethod
    def delete_collection_by_ids(ids: List[int]) -> int:
        """
        批量删除藏品信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        stmt = delete(CollectionPo).where(CollectionPo.collection_id.in_(ids))
        result = db.session.execute(stmt)
        return result.rowcount