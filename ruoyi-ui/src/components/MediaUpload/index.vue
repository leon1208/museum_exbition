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
          <el-select v-model="mediaUpload.mediaType" placeholder="请选择媒体类型">
            <el-option label="图片" value="1">图片</el-option>
            <el-option label="视频" value="2">视频</el-option>
            <el-option label="音频" value="3">音频</el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input 
            v-model="mediaUpload.description" 
            placeholder="请输入媒体描述" 
            style="width: 200px;"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-upload
            class="upload-demo"
            :headers="mediaUpload.headers"
            :action="''"
            :on-change="uploadMedia"
            :before-upload="() => false"
            :limit="1"
            :disabled="mediaUpload.isUploading"
            accept="image/*,video/*,audio/*"
          >
            <el-button size="small" type="primary">{{ mediaUpload.isUploading ? '上传中...' : '选择文件' }}</el-button>
            <div slot="tip" class="el-upload__tip">支持图片、视频、音频文件上传</div>
          </el-upload>
        </el-form-item>
      </el-form>
    </div>
    <div class="media-list-section" style="margin-top: 20px;">
      <el-table :data="mediaList" border style="width: 100%">
        <!-- 将媒体名称列改为预览图 -->
        <el-table-column label="预览图" prop="mediaName" width="150">
          <template slot-scope="scope">
            <div class="media-preview">
              <!-- 图片预览 -->
              <img 
                v-if="scope.row.mediaType === 1" 
                :src="minioBase + scope.row.mediaUrl" 
                class="preview-image" 
                @click="previewImage(scope.row.mediaUrl)" 
                alt="图片预览" 
              />
              <!-- 视频预览 -->
              <div 
                v-else-if="scope.row.mediaType === 2" 
                class="preview-video" 
                @click="previewVideo(scope.row.mediaUrl)"
              >
                <i class="el-icon-video-camera-solid"></i>
                <span class="media-name">{{ scope.row.mediaName }}</span>
              </div>
              <!-- 音频预览 -->
              <div 
                v-else-if="scope.row.mediaType === 3" 
                class="preview-audio" 
                @click="previewAudio(scope.row.mediaUrl)"
              >
                <i class="el-icon-headset"></i>
                <span class="media-name">{{ scope.row.mediaName }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column 
          label="媒体类型" 
          prop="mediaType" 
          :formatter="(row) => {
            return row.mediaType === 1 ? '图片' : (row.mediaType === 2 ? '视频' : '音频')
          }" 
        />
        <el-table-column label="文件大小" align="right" prop="size">
          <template slot-scope="scope">{{ (scope.row.size / 1024).toFixed(2) }} KB</template>
        </el-table-column>
        <el-table-column label="上传时间" prop="createTime" width="200" />
        <el-table-column label="操作" align="center" width="150">
          <template slot-scope="scope">
            <el-button 
              v-if="scope.row.mediaType === 1" 
              size="mini" 
              type="text" 
              @click="previewImage(scope.row.mediaUrl)"
            >
              预览
            </el-button>
            <el-button 
              v-else-if="scope.row.mediaType === 2" 
              size="mini" 
              type="text" 
              @click="previewVideo(scope.row.mediaUrl)"
            >
              预览
            </el-button>
            <el-button 
              v-else-if="scope.row.mediaType === 3" 
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
      mediaUpload: {
        headers: { Authorization: "Bearer " + getToken() },
        isUploading: false,
        mediaType: '1', // image/video/audio
        description: ''
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
    /** 加载媒体列表 */
    loadMediaList() {
      // 根据对象类型调用不同的API参数
      const params = {};
      params['objectId'] = this.objectId;
      params['objectType'] = this.objectType;
      
      listMuseumMedia(params).then(response => {
        this.mediaList = response.rows || response.data || [];
      });
    },

    /** 上传媒体文件 */
    uploadMedia(file) {
      this.mediaUpload.isUploading = true;
      const formData = new FormData();
      formData.append('file', file.raw);
      // 添加对象类型和ID参数
      formData.append('objectId', this.objectId);
      formData.append('objectType', this.objectType);
      formData.append('mediaType', this.mediaUpload.mediaType);
      formData.append('description', this.mediaUpload.description);
      
      uploadMuseumMedia(formData).then(response => {
        this.$modal.msgSuccess("上传成功");
        this.loadMediaList();
        this.mediaUpload.isUploading = false;
        this.mediaUpload.description = '';
      }).catch(() => {
        this.mediaUpload.isUploading = false;
      });
      
      return false; // 阻止自动上传
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
      this.$alert(`<audio src="${this.minioBase + url}" controls style="max-width: 100%;"></audio>`, '音频预览', {
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
</style>