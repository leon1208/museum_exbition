# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: collection_service.py
# @Time    : 2026-01-08 11:23:01

from typing import List

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from exb_museum.domain.entity import Collection
from exb_museum.mapper.collection_mapper import CollectionMapper

class CollectionService:
    """藏品信息表服务类"""

    def select_collection_list(self, collection: Collection) -> List[Collection]:
        """
        查询藏品信息表列表

        Args:
            collection (collection): 藏品信息表对象

        Returns:
            List[collection]: 藏品信息表列表
        """
        return CollectionMapper.select_collection_list(collection)

    
    def select_collection_by_id(self, collection_id: int) -> Collection:
        """
        根据ID查询藏品信息表

        Args:
            collection_id (int): 藏品ID

        Returns:
            collection: 藏品信息表对象
        """
        return CollectionMapper.select_collection_by_id(collection_id)
    

    def insert_collection(self, collection: Collection) -> int:
        """
        新增藏品信息表

        Args:
            collection (collection): 藏品信息表对象

        Returns:
            int: 插入的记录数
        """
        return CollectionMapper.insert_collection(collection)

    
    def update_collection(self, collection: Collection) -> int:
        """
        修改藏品信息表

        Args:
            collection (collection): 藏品信息表对象

        Returns:
            int: 更新的记录数
        """
        return CollectionMapper.update_collection(collection)
    

    
    def delete_collection_by_ids(self, ids: List[int]) -> int:
        """
        批量删除藏品信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return CollectionMapper.delete_collection_by_ids(ids)
    

    def import_collection(self, collection_list: List[Collection], is_update: bool = False) -> str:
        """
        导入藏品信息表数据

        Args:
            collection_list (List[collection]): 藏品信息表列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not collection_list:
            raise ServiceException("导入藏品信息表数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for collection in collection_list:
            try:
                display_value = collection
                
                display_value = getattr(collection, "collection_id", display_value)
                existing = None
                if collection.collection_id is not None:
                    existing = CollectionMapper.select_collection_by_id(collection.collection_id)
                if existing:
                    if is_update:
                        result = CollectionMapper.update_collection(collection)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = CollectionMapper.insert_collection(collection)
                
                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入藏品信息表失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg