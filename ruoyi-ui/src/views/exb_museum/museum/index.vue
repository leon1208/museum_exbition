<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="博物馆名称" prop="museumName" label-width="98px">
        <el-input
          v-model="queryParams.museumName"
          placeholder="请输入博物馆名称"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="博物馆地址" prop="address" label-width="98px">
        <el-input
          v-model="queryParams.address"
          placeholder="请输入博物馆地址"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
       <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择状态" clearable>
          <el-option
            v-for="dict in sys_yes_noOptions"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['exb_museum:museum:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['exb_museum:museum:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['exb_museum:museum:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['exb_museum:museum:export']"
        >导出</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="el-icon-upload2"
          size="mini"
          @click="handleImport"
          v-hasPermi="['exb_museum:museum:import']"
        >导入</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" :columns="columns"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="museumList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="博物馆名称" align="center" v-if="columns[0].visible" prop="museumName" />
      <el-table-column label="博物馆地址" align="center" v-if="columns[1].visible" prop="address" />
      <el-table-column label="状态" align="center" v-if="columns[2].visible" prop="status" :formatter="dict_status_format" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['exb_museum:museum:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['exb_museum:museum:remove']"
          >删除</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-picture-outline"
            @click="openMediaDialog(scope.row)"
            v-hasPermi="['exb_museum:media:add']"
          >媒体管理</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-office-building"
            @click="openHallManagement(scope.row)"
            v-hasPermi="['exb_museum:hall:list']"
          >展厅管理</el-button>
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

    <!-- 博物馆信息表导入对话框 -->
    <el-dialog :title="upload.title" :visible.sync="upload.open" width="400px" append-to-body>
      <el-upload
        ref="upload"
        :limit="1"
        accept=".xlsx, .xls"
        :headers="upload.headers"
        :action="upload.url + '?updateSupport=' + upload.updateSupport"
        :disabled="upload.isUploading"
        :on-progress="handleFileUploadProgress"
        :on-success="handleFileSuccess"
        :auto-upload="false"
        drag
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip text-center" slot="tip">
          <div class="el-upload__tip" slot="tip">
            <el-checkbox v-model="upload.updateSupport"/>
            是否更新已经存在的博物馆信息表数据
          </div>
          <span>仅允许导入xls、xlsx格式文件。</span>
          <el-link
            type="primary"
            :underline="false"
            style="font-size:12px;vertical-align: baseline;"
            @click="importTemplate"
          >下载模板
          </el-link>
        </div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitFileForm">确 定</el-button>
        <el-button @click="upload.open = false">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 添加或修改博物馆信息表（含子表） -->
    <el-dialog :title="title" :visible.sync="open" width="800px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="博物馆名称" prop="museumName">
          <el-input v-model="form.museumName" placeholder="请输入博物馆名称" />
        </el-form-item>
        <el-form-item label="博物馆地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入博物馆地址" />
        </el-form-item>
        <el-form-item label="博物馆简介" prop="description">
          <el-input 
            v-model="form.description" 
            placeholder="请输入博物馆简介"
            type="textarea"
            :rows="4"
            :autosize="{ minRows: 4, maxRows: 8 }"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio
              v-for="dict in sys_yes_noOptions" :key="dict.value" :label="dict.value">{{ dict.label }}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input 
            v-model="form.remark" 
            placeholder="请输入备注"
            type="textarea"
            :rows="4"
            :autosize="{ minRows: 4, maxRows: 8 }"
          />
        </el-form-item>
      
      </el-form>
      
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 展厅管理对话框 -->
    <el-dialog :title="hallDialogTitle" :visible.sync="hallDialogVisible" width="800px" append-to-body>
      <el-row :gutter="10" class="mb8">
        <el-col :span="1.5">
          <el-button
            type="primary"
            plain
            icon="el-icon-plus"
            size="mini"
            @click="handleAddHall"
            v-hasPermi="['exb_museum:hall:add']"
          >新增</el-button>
        </el-col>
        <el-col :span="1.5">
          <el-button
            type="danger"
            plain
            icon="el-icon-delete"
            size="mini"
            :disabled="hallMultiple"
            @click="handleDeleteHalls"
            v-hasPermi="['exb_museum:hall:remove']"
          >删除</el-button>
        </el-col>
      </el-row>

      <el-table v-loading="hallLoading" :data="hallList" @selection-change="handleHallSelectionChange">
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="展厅名称" align="center" prop="hallName" />
        <el-table-column label="位置" align="center" prop="location" />
        <el-table-column label="状态" align="center" prop="status" :formatter="dict_hallStatus_format" />
        <el-table-column label="备注" align="center" prop="remark" />
        <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="text"
              icon="el-icon-edit"
              @click="handleUpdateHall(scope.row)"
              v-hasPermi="['exb_museum:hall:edit']"
            >修改</el-button>
            <el-button
              size="mini"
              type="text"
              icon="el-icon-delete"
              @click="handleDeleteHall(scope.row)"
              v-hasPermi="['exb_museum:hall:remove']"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <pagination
        v-show="hallTotal>0"
        :total="hallTotal"
        :page.sync="hallQueryParams.pageNum"
        :limit.sync="hallQueryParams.pageSize"
        @pagination="getHallList"
      />

      <!-- 展厅新增/修改表单 -->
      <el-form v-if="showHallForm" ref="hallForm" :model="hallForm" :rules="hallRules" label-width="100px" style="margin-top: 20px;">
        <el-form-item label="展厅名称" prop="hallName">
          <el-input v-model="hallForm.hallName" placeholder="请输入展厅名称" />
        </el-form-item>
        <el-form-item label="位置" prop="location">
          <el-input v-model="hallForm.location" placeholder="请输入位置" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="hallForm.status">
            <el-radio
              v-for="dict in sys_yes_noOptions" :key="dict.value" :label="dict.value">{{ dict.label }}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input 
            v-model="form.remark" 
            placeholder="请输入备注"
            type="textarea"
            :rows="2"
            :autosize="{ minRows: 2, maxRows: 4 }"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitHallForm">确 定</el-button>
          <el-button @click="cancelHallForm">取 消</el-button>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="hallDialogVisible = false">关 闭</el-button>
      </div>
    </el-dialog>

  <!-- 媒体上传对话框 - 使用可复用组件 -->
  <MediaUpload 
    :objectType="'museum'"
    :objectId="currentMuseumId"
    :visible.sync="mediaDialogVisible"
  />

  </div>
</template>

<script>
import {
  listMuseum,
  getMuseum,
  delMuseum,
  addMuseum,
  updateMuseum
} from "@/api/exb_museum/museum";
import { getToken } from "@/utils/auth";
import MediaUpload from "@/components/MediaUpload/index.vue";
import { listMuseumHall, getMuseumHall, delMuseumHall, addMuseumHall, updateMuseumHall } from "@/api/exb_museum/museum_hall";

export default {
  name: "Museum",
  components: {
    MediaUpload,
  },
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 博物馆信息表表格数据
      museumList: [],
      // 表格列信息
      columns: [
        { key: 0, label: '博物馆名称', visible: true },
        { key: 1, label: '博物馆地址', visible: true },
        { key: 2, label: '状态', visible: true },
      ],
      // 状态（0正常 1停用）字典
      sys_yes_noOptions: [
        { value: 0, label: '正常' },
        { value: 1, label: '停用' },
      ],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 导入相关参数
      upload: {
        // 是否显示弹出层
        open: false,
        // 弹出层标题
        title: "",
        // 是否禁用上传
        isUploading: false,
        // 是否更新已经存在的数据
        updateSupport: 0,
        // 设置上传的请求头部
        headers: { Authorization: "Bearer " + getToken() },
        // 上传的地址
        url: process.env.VUE_APP_BASE_API + "/exb_museum/museum/importData"
      },
      // 查询参数（使用驼峰命名，匹配后端返回的数据结构）
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        museumName: null,
        address: null,
        status: null,
      },
      // 表单参数（提交前再统一处理需要转换的字段）
      form: {},
      // 表单校验（使用驼峰命名，匹配后端返回的数据结构）
      rules: {
        museumName: [
          { required: true, message: "博物馆名称不能为空", trigger: "blur" }
        ],
        address: [
          { required: true, message: "博物馆地址不能为空", trigger: "blur" }
        ],
        description: [
          { required: false, message: "博物馆简介不能为空", trigger: "blur" }
        ],
        status: [
          { required: true, message: "状态不能为空", trigger: "blur" }
        ],
        remark: [
          { required: false, message: "备注不能为空", trigger: "blur" }
        ]
      },
      // 媒体上传相关
      mediaDialogVisible: false,
      currentMuseumId: 0,

      // 展厅管理相关
      hallDialogVisible: false,
      hallDialogTitle: '',
      hallLoading: false,
      hallTotal: 0,
      hallList: [],
      hallIds: [],
      hallSingle: true,
      hallMultiple: true,
      currentMuseumIdForHall: null,
      hallQueryParams: {
        pageNum: 1,
        pageSize: 10,
        museumId: null,
        hallName: null,
        status: null,
      },
      hallForm: {},
      hallRules: {
        hallName: [
          { required: true, message: "展厅名称不能为空", trigger: "blur" }
        ],
        location: [
          { required: true, message: "位置不能为空", trigger: "blur" }
        ],
        status: [
          { required: true, message: "状态不能为空", trigger: "change" }
        ]
      },
      isHallEdit: false,
      showHallForm: false,
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询博物馆信息表列表 */
    getList() {
      this.loading = true;
      listMuseum(this.queryParams).then(response => {
        const rows = Array.isArray(response && response.rows) ? response.rows : (Array.isArray(response && response.data) ? response.data : []);
        this.museumList = rows;
        this.total = response.total || rows.length;
        this.loading = false;
      });
    },
    // 状态（0正常 1停用）字典翻译
    dict_status_format(row, column) {
      return this.selectDictLabel(this.sys_yes_noOptions, row.status);
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.museumId)
      this.single = selection.length!==1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加博物馆信息表";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const museumId = row.museumId || this.ids
      getMuseum(museumId).then(response => {
        this.form = response.data || {};
        this.open = true;
        this.title = "修改博物馆信息表";
      });
    },

    // 表单重置
    reset() {
      this.form = {
        museumId: null,
        museumName: null,
        address: null,
        description: null,
        status: null,
        delFlag: null,
        createBy: null,
        createTime: null,
        updateBy: null,
        updateTime: null,
        remark: null
      };
      this.resetForm("form");
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.resetForm("queryForm");
      this.handleQuery();
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download(
        "exb_museum/museum/export",
        { ...this.queryParams },
        "museum_" + new Date().getTime() + ".xlsx"
      );
    },
    /** 导入按钮操作 */
    handleImport() {
      this.upload.title = "博物馆信息表导入";
      this.upload.open = true;
    },
    /** 下载模板操作 */
    importTemplate() {
      this.download(
        "exb_museum/museum/importTemplate",
        {},
        "museum_template_" + new Date().getTime() + ".xlsx"
      );
    },
    // 文件上传中处理
    handleFileUploadProgress() {
      this.upload.isUploading = true;
    },
    // 文件上传成功处理
    handleFileSuccess(response) {
      this.upload.open = false;
      this.upload.isUploading = false;
      this.$refs.upload.clearFiles();
      this.$alert(
        "<div style='overflow: auto;overflow-x: hidden;max-height: 70vh;padding: 10px 20px 0;'>" +
          response.msg +
          "</div>",
        "导入结果",
        { dangerouslyUseHTMLString: true }
      );
      this.$modal.closeLoading()
      this.getList();
    },
    // 提交上传文件
    submitFileForm() {
      this.$modal.loading("导入中请稍后")
      this.$refs.upload.submit();
    },
    /** 提交按钮 */
    submitForm() {
      // 将子表行附加到主表提交数据中，示例：挂载到 children 字段
      const payload = Object.assign({}, this.form, {
        // 后端可按需解析：children 或 subRows
        // children: this.subRows.map(r => ({ key: r.key, value: r.value })),
        // subRows: this.subRows.map(r => ({ key: r.key, value: r.value })),
        // 写入子表外键字段（若后端按需使用）
        // parentId: this.form.museumId
      });
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.museumId != null) {
            updateMuseum(payload).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addMuseum(payload).then(response => {
              this.$modal.msgSuccess("新增成功");
              this.open = false;
              this.getList();
            });
          }
        }
      });
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      console.log("删除行数据:", row);
      const museumIds = row.museumId || this.ids;

      // 确保是单个ID字符串（如果是数组，取第一个或转换为逗号分隔）
      let deleteId;
      if (Array.isArray(museumIds)) {
        deleteId = museumIds.join(',');
      } else {
        deleteId = museumIds;
      }

      this.$modal.confirm('是否确认删除博物馆信息表编号为"' + deleteId + '"的数据项？').then(function() {
        return delMuseum(deleteId);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },

    /** 打开媒体上传对话框 */
    openMediaDialog(row) {
      this.currentMuseumId = row.museumId;
      this.mediaDialogVisible = true;
    },

    /** 打开展厅管理对话框 */
    openHallManagement(row) {
      this.currentMuseumIdForHall = row.museumId;
      this.hallDialogTitle = `${row.museumName} - 展厅管理`;
      this.hallQueryParams.museumId = row.museumId;
      this.showHallForm = false;
      this.getHallList();
      this.hallDialogVisible = true;
    },

    /** 查询展厅信息表列表 */
    getHallList() {
      this.hallLoading = true;
      listMuseumHall(this.hallQueryParams).then(response => {
        const rows = Array.isArray(response && response.rows) ? response.rows : (Array.isArray(response && response.data) ? response.data : []);
        this.hallList = rows;
        this.hallTotal = response.total || rows.length;
        this.hallLoading = false;
      });
    },

    // 展厅状态字典翻译
    dict_hallStatus_format(row, column) {
      return this.selectDictLabel(this.sys_yes_noOptions, row.status);
    },

    // 展厅多选框选中数据
    handleHallSelectionChange(selection) {
      this.hallIds = selection.map(item => item.hallId)
      this.hallSingle = selection.length!==1
      this.hallMultiple = !selection.length
    },

    /** 新增展厅按钮操作 */
    handleAddHall() {
      this.resetHallForm();
      this.isHallEdit = false;
      this.showHallForm = true;
    },

    /** 修改展厅按钮操作 */
    handleUpdateHall(row) {
      this.resetHallForm();
      const hallId = row.hallId;
      getMuseumHall(hallId).then(response => {
        this.hallForm = response.data || {};
        this.isHallEdit = true;
        this.showHallForm = true;
      });
    },

    // 展厅表单重置
    resetHallForm() {
      this.hallForm = {
        hallId: null,
        hallName: null,
        location: null,
        museumId: this.currentMuseumIdForHall,
        status: null,
        delFlag: null,
        createBy: null,
        createTime: null,
        updateBy: null,
        updateTime: null,
        remark: null
      };
      this.resetForm("hallForm");
    },

    /** 提交展厅表单 */
    submitHallForm() {
      this.$refs["hallForm"].validate(valid => {
        if (valid) {
          // 确保展厅关联到正确的博物馆
          this.hallForm.museumId = this.currentMuseumIdForHall;
          
          if (this.hallForm.hallId != null) {
            updateMuseumHall(this.hallForm).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.cancelHallForm();
              this.getHallList();
            });
          } else {
            addMuseumHall(this.hallForm).then(response => {
              this.$modal.msgSuccess("新增成功");
              this.cancelHallForm();
              this.getHallList();
            });
          }
        }
      });
    },

    /** 取消展厅表单 */
    cancelHallForm() {
      this.showHallForm = false;
      this.resetHallForm();
    },

    /** 删除单个展厅 */
    handleDeleteHall(row) {
      const hallId = row.hallId;
      this.$modal.confirm('是否确认删除展厅编号为"' + hallId + '"的数据项？').then(function() {
        return delMuseumHall(hallId);
      }).then(() => {
        this.getHallList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },

    /** 批量删除展厅 */
    handleDeleteHalls() {
      const hallIds = this.hallIds.join(',');
      this.$modal.confirm('是否确认删除编号为"' + hallIds + '"的展厅数据项？').then(function() {
        return delMuseumHall(hallIds);
      }).then(() => {
        this.getHallList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
  }
}
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