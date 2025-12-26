# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: museum_service.py
# @Time    : 2025-12-23 09:24:49

from typing import List

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_common.utils import security_util
from exb_museum.domain.entity import Museum
from exb_museum.mapper.museum_mapper import MuseumMapper

class MuseumService:
    """博物馆信息表服务类"""

    def select_museum_list(self, museum: Museum) -> List[Museum]:
        """
        查询博物馆信息表列表

        Args:
            museum (museum): 博物馆信息表对象

        Returns:
            List[museum]: 博物馆信息表列表
        """
        return MuseumMapper.select_museum_list(museum)

    
    def select_museum_by_id(self, museum_id: int) -> Museum:
        """
        根据ID查询博物馆信息表

        Args:
            museum_id (int): 博物馆ID

        Returns:
            museum: 博物馆信息表对象
        """
        return MuseumMapper.select_museum_by_id(museum_id)

    
    def insert_museum(self, museum: Museum) -> int:
        """
        新增博物馆信息表

        Args:
            museum (museum): 博物馆信息表对象

        Returns:
            int: 插入的记录数
        """
        # 设置创建人
        museum.create_by_user(security_util.get_username())
        museum.update_by_user(security_util.get_username())
        return MuseumMapper.insert_museum(museum)

    
    def update_museum(self, museum: Museum) -> int:
        """
        修改博物馆信息表

        Args:
            museum (museum): 博物馆信息表对象

        Returns:
            int: 更新的记录数
        """
        # 设置更新人
        museum.update_by_user(security_util.get_username())
        return MuseumMapper.update_museum(museum)

    
    
    def delete_museum_by_ids(self, ids: List[int]) -> int:
        """
        批量删除博物馆信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return MuseumMapper.delete_museum_by_ids(ids)

    
    def import_museum(self, museum_list: List[Museum], is_update: bool = False) -> str:
        """
        导入博物馆信息表数据

        Args:
            museum_list (List[museum]): 博物馆信息表列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not museum_list:
            raise ServiceException("导入博物馆信息表数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for museum in museum_list:
            try:
                display_value = museum
                
                display_value = getattr(museum, "museum_id", display_value)
                existing = None
                if museum.museum_id is not None:
                    existing = MuseumMapper.select_museum_by_id(museum.museum_id)
                if existing:
                    if is_update:
                        # 设置更新人
                        museum.update_by_user(security_util.get_username())
                        result = MuseumMapper.update_museum(museum)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    # 设置创建人
                    museum.create_by_user(security_util.get_username())
                    result = MuseumMapper.insert_museum(museum)
                
                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入博物馆信息表失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg