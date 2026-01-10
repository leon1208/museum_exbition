<template>
  <el-dialog 
    :title="dialogTitle" 
    :visible.sync="mediaDialogVisible" 
    width="800px" 
    append-to-body
    @close="handleClose"
  >
    <div class="media-upload-section">
      <el-form :model="mediaUpload" inline>
        <el-form-item label="媒体类型">
          <el-select v-model="mediaUpload.mediaType" placeholder="请选择媒体类型" @change="handleMediaTypeChange">
            <el-option label="图片" value="1">图片</el-option>
            <el-option label="视频" value="2">视频</el-option>
            <el-option label="音频" value="3">音频</el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-upload
            class="upload-demo"
            :headers="mediaUpload.headers"
            :action="''"
            :on-change="uploadMedia"
            :before-upload="() => false"
            :multiple="true"
            :limit="10"
            :disabled="mediaUpload.isUploading"
            :accept="acceptedFileTypes"
          >
            <el-button size="small" type="primary">{{ mediaUpload.isUploading ? '上传中...' : '选择文件' }}</el-button>
            <!-- <span slot="tip" class="el-upload__tip">支持{{ acceptedFileTypesText }}文件上传</span> -->
          </el-upload>
        </el-form-item>
      </el-form>
    </div>

    <!-- 图片列表 -->
    <div class="media-list-section" style="margin-top: 20px;" v-if="imageList.length > 0">
      <h4>图片列表</h4>
      <div class="image-gallery" ref="imageGallery">  <!-- 添加ref便于访问 -->
        <div 
          v-for="(image, index) in imageList" 
          :key="image.mediaId" 
          class="image-card"
          @mouseenter="showImageActions(image)"
          @mouseleave="hideImageActions(image)"
        >
          <img :src="minioBase + image.mediaUrl" class="image-preview" alt="图片预览">
          <div class="image-info-overlay">
            <div class="file-info">
              <p class="file-size">{{ (image.size / 1024).toFixed(2) }} KB</p>
              <p class="upload-time">{{ image.createTime }}</p>
            </div>
          </div>
          <div class="image-actions" v-show="image.showActions">
            <div class="action-btn preview-btn" @click="previewImage(image.mediaUrl)">
              <i class="el-icon-view"></i>
            </div>
            <div class="action-btn delete-btn" @click="deleteMedia(image.mediaId)">
              <i class="el-icon-delete"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 视频列表 -->
    <div class="media-list-section" style="margin-top: 20px;" v-if="videoList.length > 0">
      <h4>视频列表</h4>
      <div class="video-gallery" ref="videoGallery">
        <div 
          v-for="(video, index) in videoList" 
          :key="video.mediaId" 
          class="video-card"
          @mouseenter="showVideoActions(video)"
          @mouseleave="hideVideoActions(video)"
        >
          <div class="video-preview">
            <i class="el-icon-video-camera-solid video-icon"></i>
            <span class="video-label">{{ video.mediaName }}</span>
          </div>
          <div class="video-info-overlay">
            <div class="file-info">
              <p class="file-size">{{ (video.size / 1024).toFixed(2) }} KB</p>
              <p class="upload-time">{{ video.createTime }}</p>
            </div>
          </div>
          <div class="video-actions" v-show="video.showActions">
            <div class="action-btn preview-btn" @click="previewVideo(video.mediaUrl)">
              <i class="el-icon-view"></i>
            </div>
            <div class="action-btn delete-btn" @click="deleteMedia(video.mediaId)">
              <i class="el-icon-delete"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 音频列表 -->
    <div class="media-list-section" style="margin-top: 20px;" v-if="audioList.length > 0">
      <h4>音频列表</h4>
      <div class="audio-gallery" ref="audioGallery">
        <div 
          v-for="(audio, index) in audioList" 
          :key="audio.mediaId" 
          class="audio-card"
          @mouseenter="showAudioActions(audio)"
          @mouseleave="hideAudioActions(audio)"
        >
          <div class="audio-preview">
            <i class="el-icon-headset audio-icon"></i>
            <span class="audio-label">{{ audio.mediaName }}</span>
          </div>
          <div class="audio-info-overlay">
            <div class="file-info">
              <p class="file-size">{{ (audio.size / 1024).toFixed(2) }} KB</p>
              <p class="upload-time">{{ audio.createTime }}</p>
            </div>
          </div>
          <div class="audio-actions" v-show="audio.showActions">
            <div class="action-btn preview-btn" @click="previewAudio(audio.mediaUrl)">
              <i class="el-icon-view"></i>
            </div>
            <div class="action-btn delete-btn" @click="deleteMedia(audio.mediaId)">
              <i class="el-icon-delete"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div slot="footer" class="dialog-footer">
      <el-button @click="handleClose">关闭</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { listMuseumMedia, uploadMuseumMedia, deleteMuseumMedia } from "@/api/exb_museum/museum_media";
import { getToken } from "@/utils/auth";
import Sortable from 'sortablejs'

export default {
  name: "MediaUpload",
  props: {
    // 对象类型 (museum, exhibition, collection)
    objectType: {
      type: String,
      required: true,
      validator: value => ['museum', 'exhibition', 'collection'].includes(value)
    },
    // 对象ID
    objectId: {
      type: Number,
      required: true
    },
    // 是否显示对话框
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      minioBase: process.env.VUE_APP_MINIO_BASE_URL,
      mediaDialogVisible: this.visible,
      mediaList: [],
      imageList: [],
      videoList: [],
      audioList: [],
      fileCount: 0,
      mediaUpload: {
        headers: { Authorization: "Bearer " + getToken() },
        isUploading: false,
        mediaType: '1', // image/video/audio
      },
      sortable: null,
      videoSortable: null,
      audioSortable: null,
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initImageDragSort(); // 初始化图片拖拽排序
      this.initVideoDragSort(); // 初始化视频拖拽排序
      this.initAudioDragSort(); // 初始化音频拖拽排序
    });
  },
  updated() {
    this.$nextTick(() => {
      this.initImageDragSort(); // 数据更新后重新初始化图片排序
      this.initVideoDragSort(); // 数据更新后重新初始化视频排序
      this.initAudioDragSort(); // 数据更新后重新初始化音频排序
    })
  },
  computed: {
    dialogTitle() {
      const typeMap = {
        museum: '博物馆',
        exhibition: '展览',
        collection: '藏品'
      };
      return `${typeMap[this.objectType]}多媒体管理`;
    },
    acceptedFileTypes() {
      switch(this.mediaUpload.mediaType) {
        case '1': // 图片
          return 'image/*';
        case '2': // 视频
          return 'video/*';
        case '3': // 音频
          return 'audio/*';
        default:
          return 'image/*,video/*,audio/*';
      }
    },
    acceptedFileTypesText() {
      switch(this.mediaUpload.mediaType) {
        case '1': // 图片
          return '图片';
        case '2': // 视频
          return '视频';
        case '3': // 音频
          return '音频';
        default:
          return '图片、视频、音频';
      }
    }
  },
  watch: {
    visible(newVal) {
      this.mediaDialogVisible = newVal;
      if (newVal) {
        this.loadMediaList();
        this.$nextTick(() => {
            this.initImageDragSort();
            this.initVideoDragSort();
            this.initAudioDragSort();
        });
      }
    },
    mediaDialogVisible(newVal) {
      if (!newVal) {
        this.$emit('update:visible', false);
      }
    }
  },
  methods: {
    /** 加载媒体列表并分类 */
    loadMediaList() {
      // 根据对象类型调用不同的API参数
      const params = {};
      params['objectId'] = this.objectId;
      params['objectType'] = this.objectType;
      
      listMuseumMedia(params).then(response => {
        this.mediaList = response.rows || response.data || [];
        this.categorizeMediaList();
      });
    },

    /** 将媒体列表按类型分类 */
    categorizeMediaList() {
      this.imageList = this.mediaList.filter(item => item.mediaType == 1).map(item => ({ ...item, showActions: false }));
      this.videoList = this.mediaList.filter(item => item.mediaType == 2).map(item => ({ ...item, showActions: false }));
      this.audioList = this.mediaList.filter(item => item.mediaType == 3).map(item => ({ ...item, showActions: false }));
    },

    /** 处理媒体类型变化 */
    handleMediaTypeChange() {
      // 类型改变时更新接受的文件类型提示
    },

    /** 上传媒体文件 */
    uploadMedia(file, fileList) {
      //多个文件上传为了不触发重复提交，暂停500ms
      setTimeout(() => {
        this.fileCount --

        this.uploadSingleFile(file)
      }, 1100*this.fileCount++);
    },

    /** 上传单个文件（保留原有同步方法供单文件上传使用） */
    uploadSingleFile(file) {
      this.mediaUpload.isUploading = true;
      const formData = new FormData();
      formData.append('file', file.raw);
      // 添加对象类型和ID参数
      formData.append('objectId', this.objectId);
      formData.append('objectType', this.objectType);
      formData.append('mediaType', this.mediaUpload.mediaType);
      
      uploadMuseumMedia(formData).then(response => {
        this.$modal.msgSuccess(`${file.name} 上传成功`);
        this.loadMediaList();
      }).catch(() => {
      }).finally(() => {
        this.mediaUpload.isUploading = false;
      });
      return false; // 阻止自动上传
    },

    /** 显示图片操作按钮 */
    showImageActions(image) {
      this.imageList.forEach(img => {
        if(img.mediaId === image.mediaId) {
          img.showActions = true;
        }
      });
    },

    /** 隐藏图片操作按钮 */
    hideImageActions(image) {
      this.imageList.forEach(img => {
        if(img.mediaId === image.mediaId) {
          img.showActions = false;
        }
      });
    },

    /** 显示视频操作按钮 */
    showVideoActions(video) {
      this.videoList.forEach(v => {
        if(v.mediaId === video.mediaId) {
          v.showActions = true;
        }
      });
    },

    /** 隐藏视频操作按钮 */
    hideVideoActions(video) {
      this.videoList.forEach(v => {
        if(v.mediaId === video.mediaId) {
          v.showActions = false;
        }
      });
    },

    /** 显示音频操作按钮 */
    showAudioActions(audio) {
      this.audioList.forEach(a => {
        if(a.mediaId === audio.mediaId) {
          a.showActions = true;
        }
      });
    },

    /** 隐藏音频操作按钮 */
    hideAudioActions(audio) {
      this.audioList.forEach(a => {
        if(a.mediaId === audio.mediaId) {
          a.showActions = false;
        }
      });
    },

    /** 删除媒体文件 */
    deleteMedia(mediaId) {
      this.$modal.confirm('是否确认删除该媒体文件？').then(() => {
        deleteMuseumMedia(mediaId).then(() => {
          this.$modal.msgSuccess("删除成功");
          this.loadMediaList();
        });
      }).catch(() => {});
    },

    /** 预览图片 */
    previewImage(url) {
      this.$alert('<img src="' + this.minioBase + url + '" style="max-width: 100%;" />', '图片预览', {
        dangerouslyUseHTMLString: true,
        customClass: 'preview-image-dialog'
      }).catch(() => {
        // 捕获关闭时的Promise cancel错误，避免控制台报错
      });
    },

    /** 预览视频 */
    previewVideo(url) {
      this.$alert(`<video src="${this.minioBase + url}" controls style="max-width: 100%;"></video>`, '视频预览', {
        dangerouslyUseHTMLString: true
      }).catch(() => {
        // 捕获关闭时的Promise cancel错误，避免控制台报错
      });
    },

    /** 播放音频 */
    previewAudio(url) {
      this.$alert(`<audio src="${this.minioBase + url}" controls style="max-width: 100%;"></audio>`, '音频播放', {
        dangerouslyUseHTMLString: true
      }).catch(() => {
        // 捕获关闭时的Promise cancel错误，避免控制台报错
      });
    },

    /** 关闭对话框 */
    handleClose() {
      this.mediaDialogVisible = false;
      this.$emit('update:visible', false);
    },

    /** 初始化图片拖拽排序功能 */
    initImageDragSort() {
      this.$nextTick(() => {
        const imageGallery = this.$refs.imageGallery;
        if (imageGallery) {
          // 如果已有Sortable实例且父元素相同，不需要重新创建
          if (this.sortable && this.sortable.el === imageGallery) {
            return;
          }
          
          // 如果已有Sortable实例但父元素不同，先销毁
          if (this.sortable) {
            this.destroyImageSortable();
          }
          
          this.sortable = new Sortable(imageGallery, {
            animation: 150,
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            dragClass: 'sortable-drag',
            handle: '.image-preview', // 只能通过图片区域拖拽
            onEnd: (evt) => {
              // 拖拽结束后的回调
              this.onImageOrderChange(evt);
            }
          });
        }
      })
    },
    
    /** 图片顺序改变处理 */
    onImageOrderChange(evt) {
      const oldIndex = evt.oldIndex;
      const newIndex = evt.newIndex;
      
      // 更新 imageList 数组顺序
      const movedItem = this.imageList.splice(oldIndex, 1)[0];
      this.imageList.splice(newIndex, 0, movedItem);
      
      // 触发更新，确保视图响应
      this.$forceUpdate();
      
      // TODO: 如果需要保存排序信息到后端，可以在这里调用 API
      console.log('图片顺序已更新:', this.imageList.map(img => img.mediaName));
      // this.saveImageOrder();
    },

    /** 销毁图片拖拽排序实例 */
    destroyImageSortable() {
      if (this.sortable) {
        try {
          this.sortable.destroy();
        } catch (error) {
          console.warn('Error destroying sortable instance:', error);
        }
        this.sortable = null;
      }
    },

    /** 初始化视频拖拽排序功能 */
    initVideoDragSort() {
      this.$nextTick(() => {
        const videoGallery = this.$refs.videoGallery;
        if (videoGallery) {
          // 如果已有Sortable实例且父元素相同，不需要重新创建
          if (this.videoSortable && this.videoSortable.el === videoGallery) {
            return;
          }
          
          // 如果已有Sortable实例但父元素不同，先销毁
          if (this.videoSortable) {
            this.destroyVideoSortable();
          }
          
          this.videoSortable = new Sortable(videoGallery, {
            animation: 150,
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            dragClass: 'sortable-drag',
            handle: '.video-preview', // 只能通过视频区域拖拽
            onEnd: (evt) => {
              // 拖拽结束后的回调
              this.onVideoOrderChange(evt);
            }
          });
        }
      })
    },
    
    /** 视频顺序改变处理 */
    onVideoOrderChange(evt) {
      const oldIndex = evt.oldIndex;
      const newIndex = evt.newIndex;
      
      // 更新 videoList 数组顺序
      const movedItem = this.videoList.splice(oldIndex, 1)[0];
      this.videoList.splice(newIndex, 0, movedItem);
      
      // 触发更新，确保视图响应
      this.$forceUpdate();
      
      // TODO: 如果需要保存排序信息到后端，可以在这里调用 API
      console.log('视频顺序已更新:', this.videoList.map(vid => vid.mediaName));
      // this.saveVideoOrder();
    },

    /** 销毁视频拖拽排序实例 */
    destroyVideoSortable() {
      if (this.videoSortable) {
        try {
          this.videoSortable.destroy();
        } catch (error) {
          console.warn('Error destroying sortable instance:', error);
        }
        this.videoSortable = null;
      }
    },

    /** 初始化音频拖拽排序功能 */
    initAudioDragSort() {
      this.$nextTick(() => {
        const audioGallery = this.$refs.audioGallery;
        if (audioGallery) {
          // 如果已有Sortable实例且父元素相同，不需要重新创建
          if (this.audioSortable && this.audioSortable.el === audioGallery) {
            return;
          }
          
          // 如果已有Sortable实例但父元素不同，先销毁
          if (this.audioSortable) {
            this.destroyAudioSortable();
          }
          
          this.audioSortable = new Sortable(audioGallery, {
            animation: 150,
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            dragClass: 'sortable-drag',
            handle: '.audio-preview', // 只能通过音频区域拖拽
            onEnd: (evt) => {
              // 拖拽结束后的回调
              this.onAudioOrderChange(evt);
            }
          });
        }
      })
    },
    
    /** 音频顺序改变处理 */
    onAudioOrderChange(evt) {
      const oldIndex = evt.oldIndex;
      const newIndex = evt.newIndex;
      
      // 更新 audioList 数组顺序
      const movedItem = this.audioList.splice(oldIndex, 1)[0];
      this.audioList.splice(newIndex, 0, movedItem);
      
      // 触发更新，确保视图响应
      this.$forceUpdate();
      
      // TODO: 如果需要保存排序信息到后端，可以在这里调用 API
      console.log('音频顺序已更新:', this.audioList.map(aud => aud.mediaName));
      // this.saveAudioOrder();
    },

    /** 销毁音频拖拽排序实例 */
    destroyAudioSortable() {
      if (this.audioSortable) {
        try {
          this.audioSortable.destroy();
        } catch (error) {
          console.warn('Error destroying audio sortable instance:', error);
        }
        this.audioSortable = null;
      }
    },
  },

  beforeDestroy() {
    // 组件销毁前销毁 videoSortable 实例
    this.destroyImageSortable();
    this.destroyVideoSortable();
    this.destroyAudioSortable();
  }
};
</script>

<style scoped>
/* 添加预览图样式 */
.media-preview {
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-image {
  width: 80px;
  height: 60px;
  object-fit: cover;
  cursor: pointer;
  border-radius: 4px;
  border: 1px solid #eee;
}

.preview-video, .preview-audio {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 60px;
  background-color: #f5f7fa;
  border-radius: 4px;
  cursor: pointer;
  flex-direction: column;
}

.preview-video i, .preview-audio i {
  font-size: 24px;
  color: #606266;
  margin-bottom: 4px;
}

.media-name {
  font-size: 12px;
  color: #606266;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

/* 图片画廊样式 */
.image-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.video-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.image-card {
  position: relative;
  width: 148px;
  height: 148px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.image-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.video-card {
  position: relative;
  width: 148px;
  height: 148px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  transition: all 0.3s;
}

.video-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.video-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.video-icon {
  font-size: 48px;
  color: #606266;
  margin-bottom: 10px;
}

.video-label {
  font-size: 14px;
  color: #606266;
}

.image-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.image-info-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0,0,0,0.6));
  color: white;
  padding: 15px 5px 5px;
  transform: translateY(0);
  transition: transform 0.3s ease;
}

.video-info-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0,0,0,0.6));
  color: white;
  padding: 15px 5px 5px;
  transform: translateY(0);
  transition: transform 0.3s ease;
}

.file-info p {
  margin: 2px 0;
  font-size: 12px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-size {
  margin-bottom: 2px;
}

.upload-time {
  font-size: 10px;
}

.image-actions {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  gap: 10px;
}

.video-actions {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  gap: 10px;
}

.action-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover {
  background-color: rgba(0, 0, 0, 0.7);
  transform: scale(1.1);
}

.preview-btn {
  margin-right: 5px;
}

.delete-btn {
  margin-left: 5px;
}

/* 拖拽相关样式 */
.sortable-ghost {
  opacity: 0.4;
}

.sortable-chosen {
  transform: scale(1.05);
  z-index: 1000;
}

.sortable-drag {
  user-select: none;
}

.image-card {
  cursor: move; /* 显示可拖拽光标 */
  transition: transform 0.2s ease;
}

.image-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.video-card {
  cursor: move; /* 显示可拖拽光标 */
  transition: transform 0.2s ease;
}

.video-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 音频画廊样式 */
.audio-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.audio-card {
  position: relative;
  width: 148px;
  height: 148px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  transition: all 0.3s;
  cursor: move; /* 显示可拖拽光标 */
}

.audio-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.audio-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.audio-icon {
  font-size: 48px;
  color: #606266;
  margin-bottom: 10px;
}

.audio-label {
  font-size: 14px;
  color: #606266;
}

.audio-info-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0,0,0,0.6));
  color: white;
  padding: 15px 5px 5px;
  transform: translateY(0);
  transition: transform 0.3s ease;
}

.audio-actions {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  gap: 10px;
}
</style>