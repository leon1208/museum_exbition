<template>
  <div class="app-container">
    
    <el-form :model="form" ref="form" label-width="120px" style="max-width: 600px;">
      <el-form-item label="网页URL" prop="url">
        <el-input v-model="form.url" placeholder="请输入网页URL，例如：https://example.com" clearable required />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="convertToMarkdown" :loading="loading">转换为Markdown</el-button>
      </el-form-item>
    </el-form>
    
    <el-alert v-if="message.show" :title="message.text" :type="message.type" show-icon :closable="true" @close="message.show = false" style="margin-top: 20px; max-width: 600px;"></el-alert>
    
    <el-card v-if="showResult" shadow="hover" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>转换结果</span>
          <el-button type="primary" size="small" @click="copyToClipboard">复制到剪贴板</el-button>
        </div>
      </template>
      <el-input type="textarea" v-model="resultText" :rows="20" readonly style="font-family: monospace;"></el-input>
    </el-card>
  </div>
</template>

<script>
import { Message } from 'element-ui'
import request from '@/utils/request'

export default {
  name: 'WebToMarkdown',
  data() {
    return {
      form: {
        url: ''
      },
      message: {
        show: false,
        text: '',
        type: 'success'
      },
      loading: false,
      showResult: false,
      resultText: ''
    }
  },
  methods: {
    convertToMarkdown() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true
          this.showResult = false
          this.message.show = false
          
          request({
            url: '/aicrawl/convert-url',
            method: 'post',
            data: this.form
          }).then(res => {
            this.loading = false
            if (res.code === 200) {
              this.showResult = true
              this.resultText = `# ${res.data.title}\n\n来源: ${res.data.url}\n\n${res.data.markdown}`
              this.message = {
                show: true,
                text: '转换成功！',
                type: 'success'
              }
            } else {
              this.message = {
                show: true,
                text: res.msg || '转换失败',
                type: 'error'
              }
            }
          }).catch(error => {
            this.loading = false
            this.message = {
              show: true,
              text: '请求失败: ' + error.message,
              type: 'error'
            }
          })
        }
      })
    },
    copyToClipboard() {
      const textarea = document.createElement('textarea')
      textarea.value = this.resultText
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
      Message.success('已复制到剪贴板！')
    }
  }
}
</script>

<style scoped>
.app-container {
  padding: 20px;
}

.title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #303133;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
