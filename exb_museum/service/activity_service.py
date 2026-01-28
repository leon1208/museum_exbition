# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: activity_service.py
# @Time    : 2024-12-19 10:30:00

from typing import List

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_common.utils import security_util
from ruoyi_admin.ext import db
from ruoyi_common.sqlalchemy.transaction import Transactional
from exb_museum.domain.entity import Activity
from exb_museum.mapper.activity_mapper import ActivityMapper


class ActivityService:
    """活动信息表服务类"""

    def select_activity_list(self, activity: Activity) -> List[Activity]:
        """
        查询活动信息表列表

        Args:
            activity (Activity): 活动信息表对象

        Returns:
            List[Activity]: 活动信息表列表
        """
        return ActivityMapper.select_activity_list(activity)

    
    def select_activity_by_id(self, activity_id: int) -> Activity:
        """
        根据ID查询活动信息表

        Args:
            activity_id (int): 活动ID

        Returns:
            Activity: 活动信息表对象
        """
        return ActivityMapper.select_activity_by_id(activity_id)
    
    @Transactional(db.session)
    def insert_activity(self, activity: Activity) -> int:
        """
        新增活动信息表

        Args:
            activity (Activity): 活动信息表对象

        Returns:
            int: 插入的记录数
        """
        # 设置创建人
        activity.create_by_user(security_util.get_username())
        activity.update_by_user(security_util.get_username()) 
        return ActivityMapper.insert_activity(activity)

    @Transactional(db.session)    
    def update_activity(self, activity: Activity) -> int:
        """
        修改活动信息表

        Args:
            activity (Activity): 活动信息表对象

        Returns:
            int: 更新的记录数
        """
        # 设置更新人
        activity.update_by_user(security_util.get_username()) 
        return ActivityMapper.update_activity(activity)
    
    @Transactional(db.session)
    def delete_activity_by_ids(self, ids: List[int]) -> int:
        """
        批量删除活动信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return ActivityMapper.delete_activity_by_ids(ids)
    
    @Transactional(db.session)
    def import_activity(self, activity_list: List[Activity], is_update: bool = False) -> str:
        """
        导入活动信息表数据

        Args:
            activity_list (List[Activity]): 活动信息表列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not activity_list:
            raise ServiceException("导入活动信息表数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for activity in activity_list:
            try:
                display_value = activity
                
                display_value = getattr(activity, "activity_id", display_value)
                existing = None
                if activity.activity_id is not None:
                    existing = ActivityMapper.select_activity_by_id(activity.activity_id)
                if existing:
                    if is_update:
                        result = ActivityMapper.update_activity(activity)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = ActivityMapper.insert_activity(activity)
                
                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入活动信息表失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg