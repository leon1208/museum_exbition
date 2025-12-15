<template>
  <div class="screenshot-tool app-container">
    <el-form :model="formData" ref="screenshotForm" class="screenshot-form" label-width="100px">
      <el-form-item label="网站URL" prop="url">
        <el-input
          v-model="formData.url"
          placeholder="例如: https://www.example.com"
          clearable
          prefix-icon="el-icon-link"
        ></el-input>
      </el-form-item>

      <el-form-item>
        <el-checkbox v-model="formData.fullPage">截取完整页面（可能较慢）</el-checkbox>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" icon="el-icon-camera" @click="submitForm">生成截图</el-button>
      </el-form-item>
    </el-form>

    <!-- 结果展示 -->
    <el-card v-if="showResult" shadow="hover" class="result-card">
      <template #header>
        <div class="result-header">
          <span>{{ result.title }}</span>
          <span class="url-text">{{ result.url }}</span>
        </div>
      </template>

      <div class="screenshot-container">
        <img 
          class="screenshot-image"
          :src="'data:image/png;base64,' + result.screenshot" 
          alt="网站截图"
        >
      </div>

      <div class="result-footer">
        <el-button 
          type="success" 
          icon="el-icon-download" 
          @click="downloadScreenshot"
        >
          下载截图
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "ScreenshotTool",

  data() {
    return {
      formData: {
        url: "",
        fullPage: false
      },
      loading: false,
      showResult: false,
      result: {
        title: "",
        url: "",
        screenshot: ""
      }
    };
  },

  methods: {
    async submitForm() {
      this.$refs.screenshotForm.validate(async (valid) => {
        if (valid) {
          this.loading = true;
          this.showResult = false;
          
          try {
            this.$message.info("正在生成截图，请稍候...");
            
            const response = await fetch(process.env.VUE_APP_BASE_API + "/aicrawl/take-screenshot", {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                url: this.formData.url,
                fullPage: this.formData.fullPage
              })
            });

            const data = await response.json();

            if (data.code === 200) {
              this.$message.success("截图生成成功！");
              
              this.result = {
                title: data.data.title,
                url: data.data.url,
                screenshot: data.data.screenshot
              };

              this.showResult = true;
            } else {
              this.$message.error(data.message || "截图生成失败");
            }
          } catch (err) {
            this.$message.error("请求处理失败: " + err.message);
          } finally {
            this.loading = false;
          }
        }
      });
    },
    
    downloadScreenshot() {
      const link = document.createElement('a');
      link.href = 'data:image/png;base64,' + this.result.screenshot;
      link.download = 'screenshot.png';
      link.click();
    }
  }
};
</script>

<style scoped>
.screenshot-form {
  max-width: 800px;
  margin-bottom: 20px;
}

.result-card {
  max-width: 800px;
}

.result-header {
  display: flex;
  flex-direction: column;
}

.url-text {
  font-size: 12px;
  color: #606266;
  margin-top: 5px;
}

.screenshot-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
  overflow: auto;
}

.screenshot-image {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.result-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>