# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: museum_media_mapper.py
# @Time    : 2024-05-20 14:00:00

from typing import List, Optional
from datetime import datetime
from sqlalchemy import and_, or_, func
from exb_museum.domain.po import MuseumMediaPo
from exb_museum.domain.entity import MuseumMedia
from ruoyi_admin.ext import db


class MuseumMediaMapper:
    """
    博物馆媒体表数据访问层
    """
    
    def select_museum_media_list(self, object_id: int = None, object_type: str = None, media_type: str = None) -> List[MuseumMedia]:
        """
        查询博物馆媒体列表
        
        Args:
            museum_id (int, optional): 博物馆ID
            media_type (str, optional): 媒体类型
            
        Returns:
            List[MuseumMediaPo]: 博物馆媒体列表
        """
        query = db.session.query(MuseumMediaPo).filter(MuseumMediaPo.del_flag == 0)
        
        if object_id and object_type:
            query = query.filter(and_(MuseumMediaPo.object_id == object_id, MuseumMediaPo.object_type == object_type))
        
        if media_type:
            query = query.filter(MuseumMediaPo.media_type == media_type)
        
        result = query.order_by(MuseumMediaPo.sort.asc(), MuseumMediaPo.create_time.desc()).all()
        return [MuseumMedia.model_validate(item) for item in result] if result else []
    
    def select_museum_media_by_id(self, media_id: int) -> MuseumMedia:
        """
        通过ID查询博物馆媒体
        
        Args:
            media_id (int): 媒体ID
            
        Returns:
            MuseumMedia: 博物馆媒体对象
        """
        result = db.session.query(MuseumMediaPo).filter(
            and_(MuseumMediaPo.media_id == media_id, MuseumMediaPo.del_flag == 0)
        ).first()
        return MuseumMedia.model_validate(result) if result else None
    
    def select_max_sort_by_obj_id_and_obj_type(self, object_id: int, object_type: str, media_type: str) -> int:
        """
        根据object_id和object_type和media_type查询最大的sort值
        
        Args:
            object_id (int): 对象ID
            object_type (str): 对象类型
            media_type (str): 媒体类型
            
        Returns:
            int: 最大sort值，如果没有记录则返回0
        """
        result = db.session.query(func.max(MuseumMediaPo.sort)).filter(
            and_(MuseumMediaPo.object_id == object_id, 
                 MuseumMediaPo.object_type == object_type, 
                 MuseumMediaPo.media_type == media_type)
        ).scalar()
        return result if result is not None else 0
    
    def insert_museum_media(self, museum_media_po: MuseumMediaPo) -> int:
        """
        新增博物馆媒体
        
        Args:
            museum_media_po (MuseumMediaPo): 博物馆媒体PO对象
            
        Returns:
            int: 影响行数
        """
        # 如果传入的sort值为None或未设置，则自动计算
        if museum_media_po.sort is None or museum_media_po.sort == 999:
            # 获取相同object_id和object_type的最大sort值，并加1
            max_sort = self.select_max_sort_by_obj_id_and_obj_type(
                museum_media_po.object_id, museum_media_po.object_type, museum_media_po.media_type)
            museum_media_po.sort = max_sort + 1
        
        db.session.add(museum_media_po)
        return museum_media_po.media_id
    
    def update_museum_media(self, museum_media_po: MuseumMediaPo) -> int:
        """
        更新博物馆媒体
        
        Args:
            museum_media_po (MuseumMediaPo): 博物馆媒体PO对象
            
        Returns:
            int: 影响行数
        """
        return db.session.query(MuseumMediaPo).filter(
            and_(MuseumMediaPo.media_id == museum_media_po.media_id, MuseumMediaPo.del_flag == 0)
        ).update({
            'media_name': museum_media_po.media_name,
            'media_type': museum_media_po.media_type,
            'media_url': museum_media_po.media_url,
            'cover_url': museum_media_po.cover_url,
            'duration': museum_media_po.duration,
            'size': museum_media_po.size,
            'is_cover': museum_media_po.is_cover,
            'status': museum_media_po.status,
            'del_flag': museum_media_po.del_flag,
            'sort': museum_media_po.sort
        })
    
    def update_media_sort_order(self, object_id: int, object_type: str, media_type: str, sorted_media_ids: List[int]) -> int:
        """
        根据给定的顺序更新媒体文件的排序
        
        Args:
            object_id (int): 对象ID
            object_type (str): 对象类型
            media_type (str): 媒体类型
            sorted_media_ids (List[int]): 按照新顺序排列的媒体ID列表
            
        Returns:
            int: 更新的记录数量
        """
        updated_count = 0
        
        # 批量更新排序
        for idx, media_id in enumerate(sorted_media_ids):
            # 更新每个媒体的排序值
            result = db.session.query(MuseumMediaPo).filter(
                and_(
                    MuseumMediaPo.media_id == media_id,
                    MuseumMediaPo.object_id == object_id,
                    MuseumMediaPo.object_type == object_type,
                    MuseumMediaPo.media_type == media_type
                )
            ).update({'sort': idx + 1})
            updated_count += result
        
        return updated_count
    
    def delete_museum_media_by_id(self, media_id: int) -> int:
        """
        通过ID删除博物馆媒体
        
        Args:
            media_id (int): 媒体ID
            
        Returns:
            int: 影响行数
        """
        return db.session.query(MuseumMediaPo).filter(
            MuseumMediaPo.media_id == media_id
        ).delete()