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
            <div slot="tip" class="el-upload__tip">支持{{ acceptedFileTypesText }}文件上传</div>
          </el-upload>
        </el-form-item>
      </el-form>
    </div>

    <!-- 图片列表 -->
    <div class="media-list-section" style="margin-top: 20px;" v-if="imageList.length > 0">
      <h4>图片列表</h4>
      <div class="image-gallery">
        <div 
          v-for="image in imageList" 
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
      <el-table :data="videoList" border style="width: 100%">
        <el-table-column label="预览图" prop="mediaName" width="150">
          <template slot-scope="scope">
            <div class="media-preview">
              <div 
                class="preview-video" 
                @click="previewVideo(scope.row.mediaUrl)"
              >
                <i class="el-icon-video-camera-solid"></i>
                <span class="media-name">{{ scope.row.mediaName }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="文件大小" align="right" prop="size">
          <template slot-scope="scope">{{ (scope.row.size / 1024).toFixed(2) }} KB</template>
        </el-table-column>
        <el-table-column label="上传时间" prop="createTime" width="200" />
        <el-table-column label="操作" align="center" width="150">
          <template slot-scope="scope">
            <el-button 
              size="mini" 
              type="text" 
              @click="previewVideo(scope.row.mediaUrl)"
            >
              预览
            </el-button>
            <el-button 
              size="mini" 
              type="text" 
              @click="deleteMedia(scope.row.mediaId)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 音频列表 -->
    <div class="media-list-section" style="margin-top: 20px;" v-if="audioList.length > 0">
      <h4>音频列表</h4>
      <el-table :data="audioList" border style="width: 100%">
        <el-table-column label="预览图" prop="mediaName" width="150">
          <template slot-scope="scope">
            <div class="media-preview">
              <div 
                class="preview-audio" 
                @click="previewAudio(scope.row.mediaUrl)"
              >
                <i class="el-icon-headset"></i>
                <span class="media-name">{{ scope.row.mediaName }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="文件大小" align="right" prop="size">
          <template slot-scope="scope">{{ (scope.row.size / 1024).toFixed(2) }} KB</template>
        </el-table-column>
        <el-table-column label="上传时间" prop="createTime" width="200" />
        <el-table-column label="操作" align="center" width="150">
          <template slot-scope="scope">
            <el-button 
              size="mini" 
              type="text" 
              @click="previewAudio(scope.row.mediaUrl)"
            >
              播放
            </el-button>
            <el-button 
              size="mini" 
              type="text" 
              @click="deleteMedia(scope.row.mediaId)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    
    <div slot="footer" class="dialog-footer">
      <el-button @click="handleClose">关闭</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { listMuseumMedia, uploadMuseumMedia, deleteMuseumMedia } from "@/api/exb_museum/museum_media";
import { getToken } from "@/utils/auth";

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
      isProcessingBatchUpload: false, // 新增：标记是否正在处理批量上传
      mediaUpload: {
        headers: { Authorization: "Bearer " + getToken() },
        isUploading: false,
        mediaType: '1', // image/video/audio
        description: '' // 保留字段，但不再使用
      }
    };
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
      this.videoList = this.mediaList.filter(item => item.mediaType == 2);
      this.audioList = this.mediaList.filter(item => item.mediaType == 3);
    },

    /** 处理媒体类型变化 */
    handleMediaTypeChange() {
      // 类型改变时更新接受的文件类型提示
    },

    /** 上传媒体文件 */
    uploadMedia(file, fileList) {
      // 防止重复触发批量上传
      if (this.isProcessingBatchUpload) {
        return;
      }
      console.log(file, fileList)
      // 如果是多文件上传，依次上传每个文件
      if (fileList && fileList.length > 1) {
        // 设置批量上传标志
        this.isProcessingBatchUpload = true;
        
        // 过滤出未上传的文件
        const newFiles = fileList.filter(f => !f.uid || !this.mediaList.some(m => m.mediaName === f.name));
        this.uploadMultipleFilesSequentially(newFiles);
      } else {
        // 单文件上传
        this.uploadSingleFile(file);
      }

    },

    /** 依次上传多个文件 */
    async uploadMultipleFilesSequentially(files) {
      if (!files || files.length === 0) return;
      
      this.mediaUpload.isUploading = true;
      
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        try {
          await this.uploadSingleFileAsync(file);
        } catch (error) {
          console.error(`文件 ${file.name} 上传失败:`, error);
          // 可以选择继续上传下一个文件或中断上传
          // 这里我们继续上传其他文件
        }
      }
      
      this.isProcessingBatchUpload = true;
      this.mediaUpload.isUploading = false;
      this.$modal.msgSuccess("批量上传完成");
      this.loadMediaList();
    },
    
    /** 异步上传单个文件 */
    uploadSingleFileAsync(file) {
      return new Promise((resolve, reject) => {
        const formData = new FormData();
        formData.append('file', file.raw);
        // 添加对象类型和ID参数
        formData.append('objectId', this.objectId);
        formData.append('objectType', this.objectType);
        formData.append('mediaType', this.mediaUpload.mediaType);
        formData.append('description', this.mediaUpload.description); // 仍传空字符串
        
        uploadMuseumMedia(formData)
          .then(response => {
            this.$modal.msgSuccess(`${file.name} 上传成功`);
            resolve(response);
          })
          .catch(error => {
            this.$modal.msgError(`${file.name} 上传失败`);
            reject(error);
          });
      });
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
      formData.append('description', this.mediaUpload.description); // 仍传空字符串
      
      uploadMuseumMedia(formData).then(response => {
        this.$modal.msgSuccess(`${file.name} 上传成功`);
        this.loadMediaList();
        this.mediaUpload.isUploading = false;
      }).catch(() => {
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
      });
    },

    /** 预览视频 */
    previewVideo(url) {
      this.$alert(`<video src="${this.minioBase + url}" controls style="max-width: 100%;"></video>`, '视频预览', {
        dangerouslyUseHTMLString: true
      });
    },

    /** 播放音频 */
    previewAudio(url) {
      this.$alert(`<audio src="${this.minioBase + url}" controls style="max-width: 100%;"></audio>`, '音频播放', {
        dangerouslyUseHTMLString: true
      });
    },

    /** 关闭对话框 */
    handleClose() {
      this.mediaDialogVisible = false;
      this.$emit('update:visible', false);
    }
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
</style>