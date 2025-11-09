<template>
  <div class="app-container">
    <el-form v-show="showSearch" ref="queryForm" :model="queryParams" size="small" :inline="true" label-width="68px">
      <el-form-item label="表名称" prop="tableName">
        <el-input
          v-model="queryParams.tableName"
          placeholder="请输入表名称"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="表描述" prop="tableComment">
        <el-input
          v-model="queryParams.tableComment"
          placeholder="请输入表描述"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="创建时间">
        <el-date-picker
          v-model="dateRange"
          style="width: 240px"
          value-format="yyyy-MM-dd"
          type="daterange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          v-hasPermi="['tool:gen:code']"
          type="primary"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleGenTable"
        >生成</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          v-hasPermi="['tool:gen:import']"
          type="info"
          plain
          icon="el-icon-upload"
          size="mini"
          @click="openImportTable"
        >导入</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          v-hasPermi="['tool:gen:edit']"
          type="success"
          plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleEditTable"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          v-hasPermi="['tool:gen:remove']"
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
        >删除</el-button>
      </el-col>
      <right-toolbar :show-search.sync="showSearch" @queryTable="getList" />
    </el-row>

    <el-table v-loading="loading" :data="tableList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" align="center" width="55" />
      <el-table-column label="序号" type="index" width="50" align="center">
        <template slot-scope="scope">
          <span>{{ (queryParams.pageNum - 1) * queryParams.pageSize + scope.$index + 1 }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="表名称"
        align="center"
        prop="tableName"
        :show-overflow-tooltip="true"
        width="120"
      />
      <el-table-column
        label="表描述"
        align="center"
        prop="tableComment"
        :show-overflow-tooltip="true"
        width="120"
      />
      <el-table-column
        label="实体"
        align="center"
        prop="className"
        :show-overflow-tooltip="true"
        width="120"
      />
      <el-table-column label="创建时间" align="center" prop="createTime" width="160" />
      <el-table-column label="更新时间" align="center" prop="updateTime" width="160" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            v-hasPermi="['tool:gen:preview']"
            type="text"
            size="small"
            icon="el-icon-view"
            @click="handlePreview(scope.row)"
          >预览</el-button>
          <el-button
            v-hasPermi="['tool:gen:edit']"
            type="text"
            size="small"
            icon="el-icon-edit"
            @click="handleEditTable(scope.row)"
          >编辑</el-button>
          <el-button
            v-hasPermi="['tool:gen:remove']"
            type="text"
            size="small"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
          >删除</el-button>
          <el-button
            v-hasPermi="['tool:gen:edit']"
            type="text"
            size="small"
            icon="el-icon-refresh"
            @click="handleSynchDb(scope.row)"
          >同步</el-button>
          <el-button
            v-hasPermi="['tool:gen:code']"
            type="text"
            size="small"
            icon="el-icon-download"
            @click="handleGenTable(scope.row)"
          >生成代码</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />
    <!-- 预览界面 -->
    <el-dialog :title="preview.title" :visible.sync="preview.open" width="80%" top="5vh" append-to-body class="scrollbar">
      <el-tabs v-model="preview.activeName">
        <el-tab-pane
          v-for="(value, key, index) in preview.data"
          :key="index"
          :label="key.substring(key.lastIndexOf('/')+1,key.indexOf('.vm'))"
          :name="key.substring(key.lastIndexOf('/')+1,key.indexOf('.vm'))"
        >
          <el-link v-clipboard:copy="value" v-clipboard:success="clipboardSuccess" :underline="false" icon="el-icon-document-copy" style="float:right">复制</el-link>
          <pre><code class="hljs" v-html="highlightedCode(value, key)" /></pre>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
    <import-table ref="import" @ok="handleQuery" />
  </div>
</template>

<script>
import { listTable, previewTable, delTable, genCode, batchGenCode, synchDb } from '@/api/tool/gen'
import importTable from './importTable'
import hljs from 'highlight.js/lib/core'
import 'highlight.js/styles/github-gist.css'
import java from 'highlight.js/lib/languages/java'
import xml from 'highlight.js/lib/languages/xml'
import javascript from 'highlight.js/lib/languages/javascript'
import sql from 'highlight.js/lib/languages/sql'
import python from 'highlight.js/lib/languages/python'
import css from 'highlight.js/lib/languages/css'
import json from 'highlight.js/lib/languages/json'
import yaml from 'highlight.js/lib/languages/yaml'
import bash from 'highlight.js/lib/languages/bash'
import ini from 'highlight.js/lib/languages/ini'
import plaintext from 'highlight.js/lib/languages/plaintext'

hljs.registerLanguage('java', java)
hljs.registerLanguage('xml', xml)
hljs.registerLanguage('html', xml)
hljs.registerLanguage('vue', xml)
hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('sql', sql)
hljs.registerLanguage('python', python)
// 添加更多语言支持
hljs.registerLanguage('css', css)
hljs.registerLanguage('json', json)
hljs.registerLanguage('yaml', yaml)
hljs.registerLanguage('bash', bash)
hljs.registerLanguage('ini', ini)
hljs.registerLanguage('plaintext', plaintext)

export default {
  name: 'Gen',
  components: { importTable },
  data() {
    return {
      // 遮罩层
      loading: true,
      // 唯一标识符
      uniqueId: '',
      // 选中数组
      ids: [],
      // 选中表数组
      tableNames: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 表数据
      tableList: [],
      // 日期范围
      dateRange: '',
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        tableName: undefined,
        tableComment: undefined
      },
      // 预览参数
      preview: {
        open: false,
        title: '代码预览',
        data: {},
        activeName: 'entity.py'
      }
    }
  },
  created() {
    this.getList()
  },
  activated() {
    const time = this.$route.query.t
    if (time != null && time != this.uniqueId) {
      this.uniqueId = time
      this.queryParams.pageNum = Number(this.$route.query.pageNum)
      this.getList()
    }
  },
  methods: {
    /** 查询表集合 */
    getList() {
      this.loading = true
      listTable(this.addDateRange(this.queryParams, this.dateRange)).then(response => {
        this.tableList = response.rows
        this.total = response.total
        this.loading = false
      }
      )
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1
      this.getList()
    },
    /** 生成代码操作 */
    handleGenTable(row) {
      const tableNames = row.tableName || this.tableNames
      if (tableNames == '') {
        this.$modal.msgError('请选择要生成的数据')
        return
      }
      if (row.genType === '1') {
        genCode(row.tableName).then(response => {
          this.$modal.msgSuccess('成功生成到自定义路径：' + row.genPath)
        })
      } else {
        this.$download.zip('/tool/gen/batchGenCode?tables=' + tableNames, 'ruoyi')
      }
    },
    /** 同步数据库操作 */
    handleSynchDb(row) {
      const tableName = row.tableName
      this.$modal.confirm('确认要强制同步"' + tableName + '"表结构吗？').then(function() {
        return synchDb(tableName)
      }).then(() => {
        this.$modal.msgSuccess('同步成功')
      }).catch(() => {})
    },
    /** 打开导入表弹窗 */
    openImportTable() {
      this.$refs.import.show()
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.dateRange = []
      this.resetForm('queryForm')
      this.handleQuery()
    },
    /** 预览按钮 */
    handlePreview(row) {
      previewTable(row.tableId).then(response => {
        if (response.code === 200) {
          this.preview.data = response.data
          this.preview.open = true
          // 设置第一个标签为激活状态
          const firstKey = Object.keys(response.data)[0]
          if (firstKey) {
            this.preview.activeName = firstKey.substring(firstKey.lastIndexOf('/')+1,firstKey.indexOf('.vm'))
          }
        } else {
          this.$modal.msgError("预览失败：" + response.msg)
        }
      }).catch(error => {
        this.$modal.msgError("预览失败：" + error.message)
      })
    },
    /** 高亮显示 */
    highlightedCode(code, key) {
      // 根据文件扩展名确定语言
      let language = 'plaintext'
      if (key.endsWith('.java.vm')) {
        language = 'java'
      } else if (key.endsWith('.vue.vm')) {
        language = 'xml'  // 使用xml而不是vue，因为vue语言支持可能不完整
      } else if (key.endsWith('.js.vm') || key.endsWith('.javascript.vm')) {
        language = 'javascript'
      } else if (key.endsWith('.html.vm') || key.endsWith('.htm.vm')) {
        language = 'html'
      } else if (key.endsWith('.xml.vm')) {
        language = 'xml'
      } else if (key.endsWith('.sql.vm')) {
        language = 'sql'
      } else if (key.endsWith('.py.vm')) {
        language = 'python'
      }
      
      // 对代码进行高亮处理
      try {
        // 确保语言已注册
        if (hljs.getLanguage(language)) {
          return hljs.highlight(code, { language }).value
        } else {
          // 如果语言未注册，使用自动检测
          const highlighted = hljs.highlightAuto(code, ['sql', 'java', 'xml', 'javascript', 'python'])
          return highlighted.value
        }
      } catch (e) {
        // 如果高亮过程出错，尝试清理Python文件开头的编码声明后再试一次
        if (language === 'python' && code.startsWith('#')) {
          try {
            // 移除Python文件开头的编码声明行
            let cleanCode = code
            const lines = code.split('\n')
            if (lines.length > 0 && lines[0].trim().startsWith('#')) {
              // 查找连续的注释行并移除
              let startIndex = 0
              while (startIndex < lines.length && lines[startIndex].trim().startsWith('#')) {
                startIndex++
              }
              // 如果有空行也一并移除
              while (startIndex < lines.length && lines[startIndex].trim() === '') {
                startIndex++
              }
              cleanCode = lines.slice(startIndex).join('\n')
              return hljs.highlight(cleanCode, { language: 'python' }).value
            }
          } catch (innerError) {
            console.warn('清理Python代码后仍然高亮失败:', innerError)
          }
        }
        
        // 如果特定语言处理失败，返回转义后的原始代码
        console.warn('代码高亮失败，返回原始代码:', e)
        // 尝试使用plaintext作为后备方案
        try {
          return hljs.highlight(code, { language: 'plaintext' }).value;
        } catch (e2) {
          return this.escapeHtml(code);
        }
      }
    },
    /** 转义HTML特殊字符 */
    escapeHtml(text) {
      const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
      };
      
      return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    },
    /** 复制代码成功 */
    clipboardSuccess() {
      this.$modal.msgSuccess('复制成功')
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.tableId)
      this.tableNames = selection.map(item => item.tableName)
      this.single = selection.length != 1
      this.multiple = !selection.length
    },
    /** 修改按钮操作 */
    handleEditTable(row) {
      const tableId = row.tableId || this.ids[0]
      this.$router.push({ path: '/tool/gen-edit/index/' + tableId, query: { pageNum: this.queryParams.pageNum }})
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const tableIds = row.tableId || this.ids
      this.$modal.confirm('是否确认删除表编号为"' + tableIds + '"的数据项？').then(function() {
        return delTable(tableIds)
      }).then(() => {
        this.getList()
        this.$modal.msgSuccess('删除成功')
      }).catch(() => {})
    }
  }
}
</script>