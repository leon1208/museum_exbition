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
    
    @staticmethod
    def select_museum_media_list(object_id: int = None, object_type: str = None, media_type: str = None) -> List[MuseumMedia]:
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
    
    @staticmethod
    def select_museum_media_by_id(media_id: int) -> MuseumMedia:
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
    
    @staticmethod
    def select_max_sort_by_obj_id_and_obj_type(object_id: int, object_type: str, media_type: str) -> int:
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
    
    @staticmethod
    def insert_museum_media(museum_media_po: MuseumMediaPo) -> int:
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
            max_sort = MuseumMediaMapper.select_max_sort_by_obj_id_and_obj_type(
                museum_media_po.object_id, museum_media_po.object_type, museum_media_po.media_type)
            museum_media_po.sort = max_sort + 1
        
        db.session.add(museum_media_po)
        return museum_media_po.media_id
    
    @staticmethod
    def update_museum_media(museum_media_po: MuseumMediaPo) -> int:
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
    
    @staticmethod
    def update_media_sort_order(object_id: int, object_type: str, media_type: str, sorted_media_ids: List[int]) -> int:
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
    
    @staticmethod
    def delete_museum_media_by_id(media_id: int) -> int:
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
    
    @staticmethod
    def copy_media_from_object_to_object(from_object_id: int, from_object_type: str, to_object_id: int, to_object_type: str) -> int:
        """
        拷贝两个object_id之间的多媒体，只拷贝from_object_id有，但to_object_id中没有的，根据media_url来判断是否存在
        
        Args:
            from_object_id (int): 源对象ID
            from_object_type (str): 源对象类型
            to_object_id (int): 目标对象ID
            to_object_type (str): 目标对象类型
            
        Returns:
            int: 拷贝成功的记录数量
        """
        # 查询源对象的所有媒体
        from_medias = db.session.query(MuseumMediaPo).filter(
            and_(
                MuseumMediaPo.object_id == from_object_id,
                MuseumMediaPo.object_type == from_object_type,
                MuseumMediaPo.del_flag == 0
            )
        ).all()
        
        # 查询目标对象已有的媒体URL，用于去重
        to_existing_urls = db.session.query(MuseumMediaPo.media_url).filter(
            and_(
                MuseumMediaPo.object_id == to_object_id,
                MuseumMediaPo.object_type == to_object_type,
                MuseumMediaPo.del_flag == 0
            )
        ).all()
        
        # 将已存在的URL转换为集合便于比较
        existing_urls_set = {media.media_url for media in to_existing_urls}
        
        copied_count = 0
        # 遍历源对象的媒体，只复制目标对象中不存在的
        for from_media in from_medias:
            if from_media.media_url not in existing_urls_set:
                # 创建新的媒体记录，关联到目标对象
                new_media = MuseumMediaPo()
                new_media.object_type = to_object_type
                new_media.object_id = to_object_id
                new_media.media_type = from_media.media_type
                new_media.media_name = from_media.media_name
                new_media.media_url = from_media.media_url
                new_media.cover_url = from_media.cover_url
                new_media.duration = from_media.duration
                new_media.size = from_media.size
                new_media.is_cover = from_media.is_cover
                new_media.status = from_media.status
                new_media.del_flag = from_media.del_flag
                
                # 计算新记录的排序值
                max_sort = MuseumMediaMapper.select_max_sort_by_obj_id_and_obj_type(to_object_id, to_object_type, from_media.media_type)
                new_media.sort = max_sort + 1
                
                # 设置时间戳
                new_media.create_time = datetime.now()
                new_media.update_time = datetime.now()
                
                # 插入新记录
                db.session.add(new_media)
                copied_count += 1
        
        return copied_count