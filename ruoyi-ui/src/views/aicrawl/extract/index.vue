<template>
  <div class="app-container">
    <el-form :model="form" ref="form" label-width="120px" style="max-width: 600px;">
      <el-form-item label="网页URL" prop="url">
        <el-input v-model="form.url" placeholder="请输入网页URL，例如：https://example.com" clearable required />
      </el-form-item>
      <el-form-item label="栏目标题" prop="section_title">
        <el-input v-model="form.section_title" placeholder="请输入要提取的栏目标题，例如：新闻、文章、产品等" clearable required />
      </el-form-item>
      <el-form-item label="关注关键词">
        <el-input v-model="form.keywords" placeholder="请输入关注的关键词（多个关键词用逗号分隔）" clearable />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="extractSectionContent" :loading="loading">提取栏目内容</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
    
    <el-alert v-if="message.show" :title="message.text" :type="message.type" show-icon :closable="true" @close="message.show = false" style="margin-top: 20px; max-width: 600px;"></el-alert>
    
    <el-card v-if="showResult" shadow="hover" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>提取结果</span>
        </div>
      </template>
      <el-table v-loading="loading" :data="resultData" border style="width: 100%">
        <el-table-column prop="title" label="标题" min-width="200" :show-overflow-tooltip="true" />
        <el-table-column prop="publish_time" label="发布时间" width="180" />
        <el-table-column prop="link" label="链接" min-width="200">
          <template slot-scope="scope">
            <a v-if="scope.row.link && scope.row.link !== '无'" :href="scope.row.link" target="_blank" rel="noopener noreferrer">
              {{ scope.row.link }}
            </a>
            <span v-else>无链接</span>
          </template>
        </el-table-column>
        <el-table-column prop="detail_content" label="详细内容" min-width="300">
          <template slot-scope="scope">
            <div class="detail-content">
              {{ scope.row.detail_content ? (scope.row.detail_content.length > 200 ? scope.row.detail_content.substring(0, 200) + '...' : scope.row.detail_content) : '无详细内容' }}
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import request from '@/utils/request'

export default {
  name: 'ExtractSection',
  data() {
    return {
      form: {
        url: '',
        section_title: '',
        keywords: ''
      },
      message: {
        show: false,
        text: '',
        type: 'success'
      },
      loading: false,
      showResult: false,
      resultData: []
    }
  },
  methods: {
    extractSectionContent() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true
          this.showResult = false
          this.message.show = false
          
          request({
            url: '/aicrawl/extract-section',
            method: 'post',
            data: this.form,
            timeout: 600000
          }).then(res => {
            this.loading = false
            if (res.code === 200) {
              this.resultData = res.data.section_data || []
              if (this.resultData.length > 0) {
                this.showResult = true
                this.message = {
                  show: true,
                  text: '提取成功！',
                  type: 'success'
                }
              } else {
                this.message = {
                  show: true,
                  text: '未找到匹配的栏目内容',
                  type: 'warning'
                }
              }
            } else {
              this.message = {
                show: true,
                text: res.msg || '提取失败',
                type: 'error'
              }
            }
          }).catch(error => {
            this.loading = false
            this.message = {
              show: true,
              text: '请求失败: ' + (error.msg || error.message),
              type: 'error'
            }
          })
        }
      })
    },
    resetForm() {
      this.$refs.form.resetFields()
      this.showResult = false
      this.message.show = false
      this.resultData = []
    }
  }
}
</script>

<style scoped>
.app-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-content {
  background-color: #f8f9fa;
  border-left: 4px solid #007bff;
  padding: 10px;
  margin-top: 5px;
  white-space: pre-wrap;
  font-size: 0.9em;
  border-radius: 0 4px 4px 0;
}
</style>
