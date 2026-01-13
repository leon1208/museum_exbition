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
    
    def select_museum_media_list(self, object_id: int = None, object_type: str = None, media_type: str = None) -> List[MuseumMedia]:
        """
        查询博物馆媒体列表
        
        Args:
            object_id (int, optional): 对象ID
            object_type (str, optional): 对象类型
            media_type (str, optional): 媒体类型
            
        Returns:
            List[MuseumMedia]: 博物馆媒体列表
        """
        return MuseumMediaMapper.select_museum_media_list(object_id, object_type, media_type)
    
    def select_museum_media_by_id(self, media_id: int) -> MuseumMedia:
        """
        通过ID查询博物馆媒体
        
        Args:
            media_id (int): 媒体ID
            
        Returns:
            MuseumMedia: 博物馆媒体对象
        """
        return MuseumMediaMapper.select_museum_media_by_id(media_id)
    
    @Transactional(db.session)
    def upload_museum_media(self, object_id: int, object_type: str, file: FileStorage, media_type: str) -> MuseumMedia:
        """
        上传博物馆媒体
        
        Args:
            object_id (int): 对象ID
            object_type (str): 对象类型
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
        media_po.object_id = object_id
        media_po.object_type = object_type
        media_po.media_name = file.filename
        media_po.media_type = media_type
        media_po.media_url = upload_result
        media_po.is_cover = 0
        # 将sort设置为None，让mapper层自动计算
        media_po.sort = None

        # 当上传音频时，cover_url设置为None
        from ruoyi_common.utils.minio_util import MinioUtil        
        if media_type == '3':  # '3'代表音频类型
            d1 = MinioUtil.get_audio_duration_from_minio(object_name=upload_result)
            media_po.cover_url = None
            media_po.duration = int(d1)
        elif media_type == '2':  # '2'代表视频类型
            d1, first_frame = MinioUtil.get_video_duration_and_first_frame(object_name=upload_result)
            media_po.cover_url = first_frame
            media_po.duration = int(d1)
        else: # '1'代表图片类型
            media_po.cover_url = upload_result
            media_po.duration = 0
        media_po.size = stat.size
        media_po.status = 0
        media_po.del_flag = 0
        media_po.update_time = datetime.now()
        media_po.create_time = datetime.now()
                
        # 保存到数据库
        media_id = MuseumMediaMapper.insert_museum_media(media_po)
        
        # 返回实体对象
        return self.select_museum_media_by_id(media_id)

    @Transactional(db.session)
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
        return MuseumMediaMapper.update_media_sort_order(object_id, object_type, media_type, sorted_media_ids)
                
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
        return MuseumMediaMapper.delete_museum_media_by_id(media_id)
