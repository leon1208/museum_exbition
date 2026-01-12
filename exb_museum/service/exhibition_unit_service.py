# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exhibition_unit_service.py
# @Time    : 

from typing import List

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_common.utils import security_util
from exb_museum.domain.entity import ExhibitionUnit
from exb_museum.mapper.exhibition_unit_mapper import ExhibitionUnitMapper

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
        return ExhibitionUnitMapper.insert_exhibition_unit(exhibition_unit)

    
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
        return ExhibitionUnitMapper.update_exhibition_unit(exhibition_unit)
    

    
    def delete_exhibition_unit_by_ids(self, ids: List[int]) -> int:
        """
        批量删除展览单元信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return ExhibitionUnitMapper.delete_exhibition_unit_by_ids(ids)
    

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