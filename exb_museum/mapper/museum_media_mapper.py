# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: museum_media_mapper.py
# @Time    : 2024-05-20 14:00:00

from typing import List, Optional
from datetime import datetime
from sqlalchemy import and_, or_
from exb_museum.domain.po import MuseumMediaPo
from exb_museum.domain.entity import MuseumMedia
from ruoyi_admin.ext import db


class MuseumMediaMapper:
    """
    博物馆媒体表数据访问层
    """
    
    def select_museum_media_list(self, museum_id: int = None, media_type: str = None) -> List[MuseumMedia]:
        """
        查询博物馆媒体列表
        
        Args:
            museum_id (int, optional): 博物馆ID
            media_type (str, optional): 媒体类型
            
        Returns:
            List[MuseumMediaPo]: 博物馆媒体列表
        """
        query = db.session.query(MuseumMediaPo).filter(MuseumMediaPo.del_flag == 0)
        
        if museum_id:
            query = query.filter(MuseumMediaPo.museum_id == museum_id)
        
        if media_type:
            query = query.filter(MuseumMediaPo.media_type == media_type)
        
        result = query.order_by(MuseumMediaPo.create_time.desc()).all()
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
    
    def insert_museum_media(self, museum_media_po: MuseumMediaPo) -> int:
        """
        新增博物馆媒体
        
        Args:
            museum_media_po (MuseumMediaPo): 博物馆媒体PO对象
            
        Returns:
            int: 影响行数
        """
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
            'create_time': museum_media_po.create_time,
            'update_time': museum_media_po.update_time or now
        })
    
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
    
    def delete_museum_media_by_museum_id(self, museum_id: int) -> int:
        """
        通过博物馆ID删除媒体
        
        Args:
            museum_id (int): 博物馆ID
            
        Returns:
            int: 影响行数
        """
        return db.session.query(MuseumMediaPo).filter(
            MuseumMediaPo.museum_id == museum_id
        ).delete()