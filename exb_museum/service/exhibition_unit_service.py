# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exhibition_unit_service.py
# @Time    : 

from typing import List

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_common.utils import security_util
from ruoyi_admin.ext import db
from ruoyi_common.sqlalchemy.transaction import Transactional
from exb_museum.domain.entity import ExhibitionUnit
from exb_museum.mapper.exhibition_unit_mapper import ExhibitionUnitMapper
from exb_museum.mapper.museum_media_mapper import MuseumMediaMapper

class ExhibitionUnitService:
    """展览单元信息表服务类"""

    def select_exhibition_unit_list(self, exhibition_unit: ExhibitionUnit) -> List[ExhibitionUnit]:
        """
        查询展览单元信息表列表

        Args:
            exhibition_unit (ExhibitionUnit): 展览单元信息表对象

        Returns:
            List[ExhibitionUnit]: 展览单元信息表列表
        """
        return ExhibitionUnitMapper.select_exhibition_unit_list(exhibition_unit)

    
    def select_exhibition_unit_by_id(self, unit_id: int) -> ExhibitionUnit:
        """
        根据ID查询展览单元信息表

        Args:
            unit_id (int): 展览单元ID

        Returns:
            ExhibitionUnit: 展览单元信息表对象
        """
        return ExhibitionUnitMapper.select_exhibition_unit_by_id(unit_id)
    
    def select_exhibition_units_by_exhibition_id(self, exhibition_id: int) -> List[ExhibitionUnit]:
        """
        根据展览ID查询所有展览单元

        Args:
            exhibition_id (int): 展览ID

        Returns:
            List[ExhibitionUnit]: 展览单元列表
        """
        return ExhibitionUnitMapper.select_exhibition_units_by_exhibition_id(exhibition_id)
    
    @Transactional(db.session)
    def insert_exhibition_unit(self, exhibition_unit: ExhibitionUnit) -> int:
        """
        新增展览单元信息表
    
        Args:
            exhibition_unit (ExhibitionUnit): 展览单元信息表对象
    
        Returns:
            int: 插入的记录数
        """
        # 如果没有手动设置排序值，则自动计算排序值
        if exhibition_unit.sort_order is None or exhibition_unit.sort_order == 0:
            # 获取同一展览、同一篇章的最大排序值
            max_sort_order = ExhibitionUnitMapper.get_max_sort_order_by_exhibition_and_section(
                exhibition_unit.exhibition_id, 
                exhibition_unit.section
            )
            # 设置排序值为最大值+1，如果不存在则设为1
            exhibition_unit.sort_order = (max_sort_order or 0) + 1
        
        # 设置创建人
        exhibition_unit.create_by_user(security_util.get_username())
        exhibition_unit.update_by_user(security_util.get_username()) 
        
        # 如果是展品单元且需要复制藏品媒体
        result = ExhibitionUnitMapper.insert_exhibition_unit(exhibition_unit)
        
        # 如果勾选了复制藏品媒体至展览单元，需要处理关联的藏品媒体
        if result > 0 and exhibition_unit.unit_type == 0 and exhibition_unit.collections and exhibition_unit.copy_collection_media:
            # 复制裁品媒体到展览单元
            self._copy_collection_media_to_exhibition_unit(exhibition_unit.unit_id, exhibition_unit.collections)
        
        return result        

    @Transactional(db.session)
    def update_exhibition_unit(self, exhibition_unit: ExhibitionUnit) -> int:
        """
        修改展览单元信息表

        Args:
            exhibition_unit (ExhibitionUnit): 展览单元信息表对象

        Returns:
            int: 更新的记录数
        """
        # 设置更新人
        exhibition_unit.update_by_user(security_util.get_username()) 
        
        # 如果是展品单元且需要复制藏品媒体
        result = ExhibitionUnitMapper.update_exhibition_unit(exhibition_unit)
        
        # 如果勾选了复制藏品媒体至展览单元，需要处理关联的藏品媒体
        if exhibition_unit.copy_collection_media:
            # 复制关联的藏品媒体
            self._copy_collection_media_to_exhibition_unit(exhibition_unit.unit_id, exhibition_unit.collections)
        
        return result

    @Transactional(db.session)
    def _copy_collection_media_to_exhibition_unit(self, unit_id: int, collections_json: str):
        """
        将藏品的媒体数据复制到展览单元
        :param unit_id: 展览单元ID
        :param collections_json: 关联藏品ID列表(JSON字符串)
        """
        # 解析藏品ID列表
        import json
        try:
            collection_ids = json.loads(collections_json) if collections_json else []
        except json.JSONDecodeError:
            collection_ids = []
        
        if not collection_ids:
            return
        
        # 遍历每个藏品，复制其媒体到展览单元
        for collection_id in collection_ids:
            # 调用新添加的拷贝方法，从藏品(对象类型2)拷贝到展览单元(对象类型3)
            MuseumMediaMapper.copy_media_from_object_to_object(
                from_object_id=collection_id,
                from_object_type='collection',
                to_object_id=unit_id,
                to_object_type='exhibition_unit'
            )

    
    @Transactional(db.session)
    def delete_exhibition_unit_by_ids(self, ids: List[int]) -> int:
        """
        批量删除展览单元信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return ExhibitionUnitMapper.delete_exhibition_unit_by_ids(ids)
    

    @Transactional(db.session)
    def import_exhibition_unit(self, exhibition_unit_list: List[ExhibitionUnit], is_update: bool = False) -> str:
        """
        导入展览单元信息表数据

        Args:
            exhibition_unit_list (List[ExhibitionUnit]): 展览单元信息表列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not exhibition_unit_list:
            raise ServiceException("导入展览单元信息表数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for exhibition_unit in exhibition_unit_list:
            try:
                display_value = exhibition_unit
                
                display_value = getattr(exhibition_unit, "unit_id", display_value)
                existing = None
                if exhibition_unit.unit_id is not None:
                    existing = ExhibitionUnitMapper.select_exhibition_unit_by_id(exhibition_unit.unit_id)
                if existing:
                    if is_update:
                        result = ExhibitionUnitMapper.update_exhibition_unit(exhibition_unit)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = ExhibitionUnitMapper.insert_exhibition_unit(exhibition_unit)
                
                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入展览单元信息表失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg

    @Transactional(db.session)
    def move_up_exhibition_unit(self, unit_id: int) -> bool:
        """
        向上移动展览单元
        
        Args:
            unit_id (int): 展览单元ID
            
        Returns:
            bool: 是否移动成功
        """
        # 获取当前展览单元信息
        current_unit = ExhibitionUnitMapper.select_exhibition_unit_by_id(unit_id)
        if not current_unit:
            return False
            
        # 获取同展览和同章节的所有展览单元，按排序值升序排列
        units = ExhibitionUnitMapper.select_exhibition_units_by_exhibition_and_section(
            current_unit.exhibition_id, current_unit.section
        )
        
        # 找到当前单元在列表中的位置
        current_index = -1
        for i, unit in enumerate(units):
            if unit.unit_id == unit_id:
                current_index = i
                break
                
        if current_index <= 0:  # 已经是第一个，无法再向上移动
            return False
            
        # 获取前一个单元
        prev_unit = units[current_index - 1]
        
        # 交换两个单元的排序值
        result1 = ExhibitionUnitMapper.update_sort_order(prev_unit.unit_id, current_unit.sort_order)
        result2 = ExhibitionUnitMapper.update_sort_order(current_unit.unit_id, prev_unit.sort_order)
        
        return result1 > 0 and result2 > 0

    @Transactional(db.session)
    def move_down_exhibition_unit(self, unit_id: int) -> bool:
        """
        向下移动展览单元
        
        Args:
            unit_id (int): 展览单元ID
            
        Returns:
            bool: 是否移动成功
        """
        # 获取当前展览单元信息
        current_unit = ExhibitionUnitMapper.select_exhibition_unit_by_id(unit_id)
        if not current_unit:
            return False
            
        # 获取同展览和同章节的所有展览单元，按排序值升序排列
        units = ExhibitionUnitMapper.select_exhibition_units_by_exhibition_and_section(
            current_unit.exhibition_id, current_unit.section
        )
        
        # 找到当前单元在列表中的位置
        current_index = -1
        for i, unit in enumerate(units):
            if unit.unit_id == unit_id:
                current_index = i
                break
                
        if current_index == -1 or current_index >= len(units) - 1:  # 已经是最后一个，无法再向下移动
            return False
            
        # 获取后一个单元
        next_unit = units[current_index + 1]
        
        # 交换两个单元的排序值
        result1 = ExhibitionUnitMapper.update_sort_order(next_unit.unit_id, current_unit.sort_order)
        result2 = ExhibitionUnitMapper.update_sort_order(current_unit.unit_id, next_unit.sort_order)
        
        return result1 > 0 and result2 > 0