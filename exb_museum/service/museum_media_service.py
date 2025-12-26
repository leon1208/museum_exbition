# -*- coding: utf-8 -*-
# @Author  : leeon
# @FileName: museum_media_service.py
# @Time    : 2024-05-20 14:00:00

from typing import List, Optional
from werkzeug.datastructures import FileStorage
from datetime import datetime
from exb_museum.domain.entity import MuseumMedia
from exb_museum.domain.po import MuseumMediaPo
from exb_museum.mapper.museum_media_mapper import MuseumMediaMapper
from ruoyi_common.sqlalchemy.transaction import Transactional
from ruoyi_common.utils import FileUploadUtil
from ruoyi_admin.ext import db



class MuseumMediaService:
    """
    博物馆媒体表业务逻辑层
    """
    
    def __init__(self):
        self.museum_media_mapper = MuseumMediaMapper()
    
    def select_museum_media_list(self, museum_id: int = None, media_type: str = None) -> List[MuseumMedia]:
        """
        查询博物馆媒体列表
        
        Args:
            museum_id (int, optional): 博物馆ID
            media_type (str, optional): 媒体类型
            
        Returns:
            List[MuseumMedia]: 博物馆媒体列表
        """
        return self.museum_media_mapper.select_museum_media_list(museum_id, media_type)
    
    def select_museum_media_by_id(self, media_id: int) -> MuseumMedia:
        """
        通过ID查询博物馆媒体
        
        Args:
            media_id (int): 媒体ID
            
        Returns:
            MuseumMedia: 博物馆媒体对象
        """
        return self.museum_media_mapper.select_museum_media_by_id(media_id)
    
    @Transactional(db.session)
    def upload_museum_media(self, museum_id: int, file: FileStorage, media_type: str, description: str = None) -> MuseumMedia:
        """
        上传博物馆媒体
        
        Args:
            museum_id (int): 博物馆ID
            file: 文件对象
            media_type (str): 媒体类型
            description (str, optional): 媒体描述
            user (dict, optional): 当前用户信息
            
        Returns:
            MuseumMedia: 博物馆媒体对象
        """
        # 上传文件
        # upload_result = FileUploadUtil.upload(file)
        upload_result, stat = FileUploadUtil.upload_minio(file, base_path="/museum/media")
        # 创建媒体PO对象
        media_po = MuseumMediaPo()
        media_po.museum_id = museum_id
        media_po.media_name = file.filename
        media_po.media_type = media_type
        media_po.media_url = upload_result
        media_po.is_cover = 0
        media_po.sort = 999
        media_po.cover_url = upload_result
        media_po.duration = 0
        media_po.size = stat.size
        media_po.status = 0
        media_po.del_flag = 0
        media_po.update_time = datetime.now()
        media_po.create_time = datetime.now()
                
        # 保存到数据库
        media_id = self.museum_media_mapper.insert_museum_media(media_po)
        
        # 返回实体对象
        return self.select_museum_media_by_id(media_id)
        
    @Transactional(db.session)
    def update_museum_media(self, museum_media: MuseumMedia) -> int:
        """
        更新博物馆媒体
        
        Args:
            museum_media (MuseumMedia): 博物馆媒体对象
            user (dict, optional): 当前用户信息
            
        Returns:
            int: 影响行数
        """
        pass
        # 转换为PO对象
        # media_po = model_to_model(museum_media, MuseumMediaPo)
        
        # 设置更新用户信息
        # self.update_by_user(media_po, user)
        
        # 更新数据库
        # return self.museum_media_mapper.update_museum_media(media_po)
    
    @Transactional(db.session)
    def delete_museum_media_by_id(self, media_id: int) -> int:
        """
        通过ID删除博物馆媒体
        
        Args:
            media_id (int): 媒体ID
            
        Returns:
            int: 影响行数
        """
        return self.museum_media_mapper.delete_museum_media_by_id(media_id)
