# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exhibition_hall_service.py
# @Time    : 

from typing import List

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_common.utils import security_util
from ruoyi_common.sqlalchemy.transaction import Transactional
from exb_museum.domain.entity import MuseumHall
from exb_museum.mapper.museum_hall_mapper import MuseumHallMapper
from ruoyi_admin.ext import db

class MuseumHallService:
    """博物馆展厅信息表服务类"""

    def select_museum_hall_list(self, museum_hall: MuseumHall) -> List[MuseumHall]:
        """
        查询博物馆展厅信息表列表

        Args:
            museum_hall (MuseumHall): 博物馆展厅信息表对象

        Returns:
            List[MuseumHall]: 博物馆展厅信息表列表
        """
        return MuseumHallMapper.select_museum_hall_list(museum_hall)

    
    def select_museum_hall_by_id(self, hall_id: int) -> MuseumHall:
        """
        根据ID查询博物馆展厅信息表

        Args:
            hall_id (int): 展厅ID

        Returns:
            MuseumHall: 博物馆展厅信息表对象
        """
        return MuseumHallMapper.select_museum_hall_by_id(hall_id)
    

    @Transactional(db.session)
    def insert_museum_hall(self, museum_hall: MuseumHall) -> int:
        """
        新增博物馆展厅信息表

        Args:
            museum_hall (MuseumHall): 博物馆展厅信息表对象

        Returns:
            int: 插入的记录数
        """
        # 设置创建人
        museum_hall.create_by_user(security_util.get_username())
        museum_hall.update_by_user(security_util.get_username()) 
        return MuseumHallMapper.insert_museum_hall(museum_hall)

    
    @Transactional(db.session)
    def update_museum_hall(self, museum_hall: MuseumHall) -> int:
        """
        修改博物馆展厅信息表

        Args:
            museum_hall (MuseumHall): 博物馆展厅信息表对象

        Returns:
            int: 更新的记录数
        """
        # 设置更新人
        museum_hall.update_by_user(security_util.get_username()) 
        return MuseumHallMapper.update_museum_hall(museum_hall)
    

    
    @Transactional(db.session)
    def delete_museum_hall_by_ids(self, ids: List[int]) -> int:
        """
        批量删除博物馆展厅信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return MuseumHallMapper.delete_museum_hall_by_ids(ids)
    

    @Transactional(db.session)
    def import_museum_hall(self, museum_hall_list: List[MuseumHall], is_update: bool = False) -> str:
        """
        导入博物馆展厅信息表数据

        Args:
            museum_hall_list (List[MuseumHall]): 博物馆展厅信息表列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not museum_hall_list:
            raise ServiceException("导入博物馆展厅信息表数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for museum_hall in museum_hall_list:
            try:
                display_value = museum_hall.hall_name
                
                display_value = getattr(museum_hall, "hall_id", display_value)
                existing = None
                if museum_hall.hall_id is not None:
                    existing = MuseumHallMapper.select_museum_hall_by_id(museum_hall.hall_id)
                if existing:
                    if is_update:
                        result = MuseumHallMapper.update_museum_hall(museum_hall)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = MuseumHallMapper.insert_museum_hall(museum_hall)
                
                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入展厅信息表失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg