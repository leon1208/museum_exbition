# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: exhibition_service.py
# @Time    : 2026-01-08 08:54:20

from typing import List

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_common.utils import security_util
from ruoyi_admin.ext import db
from ruoyi_common.sqlalchemy.transaction import Transactional
from exb_museum.domain.entity import Exhibition
from exb_museum.mapper.exhibition_mapper import ExhibitionMapper

class ExhibitionService:
    """展览信息表服务类"""

    def select_exhibition_list(self, exhibition: Exhibition) -> List[Exhibition]:
        """
        查询展览信息表列表

        Args:
            exhibition (exhibition): 展览信息表对象

        Returns:
            List[exhibition]: 展览信息表列表
        """
        return ExhibitionMapper.select_exhibition_list(exhibition)

    
    def select_exhibition_by_id(self, exhibition_id: int) -> Exhibition:
        """
        根据ID查询展览信息表

        Args:
            exhibition_id (int): 展览ID

        Returns:
            exhibition: 展览信息表对象
        """
        return ExhibitionMapper.select_exhibition_by_id(exhibition_id)
    
    @Transactional(db.session)
    def insert_exhibition(self, exhibition: Exhibition) -> int:
        """
        新增展览信息表

        Args:
            exhibition (exhibition): 展览信息表对象

        Returns:
            int: 插入的记录数
        """
        # 设置创建人
        exhibition.create_by_user(security_util.get_username())
        exhibition.update_by_user(security_util.get_username()) 
        return ExhibitionMapper.insert_exhibition(exhibition)

    @Transactional(db.session)    
    def update_exhibition(self, exhibition: Exhibition) -> int:
        """
        修改展览信息表

        Args:
            exhibition (exhibition): 展览信息表对象

        Returns:
            int: 更新的记录数
        """
        # 设置更新人
        exhibition.update_by_user(security_util.get_username()) 
        return ExhibitionMapper.update_exhibition(exhibition)
    
    @Transactional(db.session)
    def delete_exhibition_by_ids(self, ids: List[int]) -> int:
        """
        批量删除展览信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return ExhibitionMapper.delete_exhibition_by_ids(ids)
    
    @Transactional(db.session)
    def import_exhibition(self, exhibition_list: List[Exhibition], is_update: bool = False) -> str:
        """
        导入展览信息表数据

        Args:
            exhibition_list (List[exhibition]): 展览信息表列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not exhibition_list:
            raise ServiceException("导入展览信息表数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for exhibition in exhibition_list:
            try:
                display_value = exhibition
                
                display_value = getattr(exhibition, "exhibition_id", display_value)
                existing = None
                if exhibition.exhibition_id is not None:
                    existing = ExhibitionMapper.select_exhibition_by_id(exhibition.exhibition_id)
                if existing:
                    if is_update:
                        result = ExhibitionMapper.update_exhibition(exhibition)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = ExhibitionMapper.insert_exhibition(exhibition)
                
                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入展览信息表失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg