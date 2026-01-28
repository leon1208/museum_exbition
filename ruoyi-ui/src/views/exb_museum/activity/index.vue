<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="88px">
      <el-form-item label="活动名称" prop="activityName">
        <el-input
          v-model="queryParams.activityName"
          placeholder="请输入活动名称"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="所属博物馆" prop="museumId">
        <el-select v-model="queryParams.museumId" placeholder="请选择所属博物馆" clearable>
          <el-option
            v-for="museum in museumOptions"
            :key="museum.museumId"
            :label="museum.museumName"
            :value="museum.museumId"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="活动类型" prop="activityType">
        <el-input
          v-model="queryParams.activityType"
          placeholder="请输入活动类型"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="活动地点" prop="location">
        <el-input
          v-model="queryParams.location"
          placeholder="请输入活动地点"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择状态" clearable>
          <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
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
          v-hasPermi="['exb_museum:activity:add']"
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
          v-hasPermi="['exb_museum:activity:edit']"
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
          v-hasPermi="['exb_museum:activity:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['exb_museum:activity:export']"
        >导出</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="el-icon-upload2"
          size="mini"
          @click="handleImport"
          v-hasPermi="['exb_museum:activity:import']"
        >导入</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" :columns="columns"></right-toolbar>
    </el-row>

    <el-table :loading="loading" :data="activityList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="活动名称" :show-overflow-tooltip="true" v-if="columns[0].visible" prop="activityName" />
      <el-table-column label="所属博物馆" align="center" :show-overflow-tooltip="true" v-if="columns[1].visible" prop="museumName" :formatter="dict_museumId_format" />
      <el-table-column label="活动类型" align="center" :show-overflow-tooltip="true" v-if="columns[2].visible" prop="activityType" />
      <el-table-column label="活动对象" align="center" :show-overflow-tooltip="true" v-if="columns[3].visible" prop="targetAudience" />
      <el-table-column label="活动地点" align="center" :show-overflow-tooltip="true" v-if="columns[4].visible" prop="location" />
      <el-table-column label="活动开始时间" align="center" v-if="columns[5].visible" prop="activityStartTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.activityStartTime, '{y}-{m}-{d} {h}:{i}:{s}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="活动结束时间" align="center" v-if="columns[6].visible" prop="activityEndTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.activityEndTime, '{y}-{m}-{d} {h}:{i}:{s}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="报名人数" align="center" v-if="columns[7].visible" prop="registrationCount" />
      <el-table-column label="最大报名人数" align="center" v-if="columns[8].visible" prop="maxRegistration" />
      <el-table-column label="主讲人或表演团队" align="center" :show-overflow-tooltip="true" v-if="columns[9].visible" prop="presenter" />
      <el-table-column label="状态" align="center" :show-overflow-tooltip="true" v-if="columns[10].visible" prop="status" :formatter="dict_status_format" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['exb_museum:activity:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['exb_museum:activity:remove']"
          >删除</el-button>
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

    <!-- 添加或修改活动信息表对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="活动名称" prop="activityName">
          <el-input v-model="form.activityName" placeholder="请输入活动名称" />
        </el-form-item>
        <el-form-item label="活动介绍" prop="introduction">
          <el-input v-model="form.introduction" placeholder="请输入活动介绍" type="textarea" :rows="4" :autosize="{ minRows: 4, maxRows: 8 }"/>
        </el-form-item>
        <el-form-item label="所属博物馆" prop="museumId">
          <el-select v-model="form.museumId" placeholder="请选择所属博物馆">
            <el-option v-for="museum in museumOptions" :key="museum.museumId" :label="museum.museumName" :value="museum.museumId"/>
          </el-select>
        </el-form-item>
        <el-form-item label="活动类型" prop="activityType">
          <el-input v-model="form.activityType" placeholder="请输入活动类型" />
        </el-form-item>
        <el-form-item label="活动对象" prop="targetAudience">
          <el-input v-model="form.targetAudience" placeholder="请输入活动对象" />
        </el-form-item>
        <el-form-item label="活动地点" prop="location">
          <el-input v-model="form.location" placeholder="请输入活动地点" />
        </el-form-item>
        <el-form-item label="活动开始时间" prop="activityStartTime">
          <el-date-picker clearable
            v-model="form.activityStartTime"
            type="datetime"
            value-format="yyyy-MM-dd HH:mm:ss"
            placeholder="选择活动开始时间">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="活动结束时间" prop="activityEndTime">
          <el-date-picker clearable
            v-model="form.activityEndTime"
            type="datetime"
            value-format="yyyy-MM-dd HH:mm:ss"
            placeholder="选择活动结束时间">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="主讲人或表演团队" prop="presenter">
          <el-input v-model="form.presenter" placeholder="请输入主讲人或表演团队" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio v-for="item in statusOptions" :key="item.value" :label="item.value">{{item.label}}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 导入对话框 -->
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
            <el-checkbox v-model="upload.updateSupport" /> 是否更新已经存在的活动信息表数据
          </div>
          <span>仅允许导入xls、xlsx格式文件。</span>
          <el-link type="primary" :underline="false" style="font-size:12px;vertical-align: baseline;" @click="importTemplate">下载模板</el-link>
        </div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitFileForm">确 定</el-button>
        <el-button @click="upload.open = false">取 消</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import { listActivity, getActivity, delActivity, addActivity, updateActivity } from "@/api/exb_museum/activity";
import { listMuseum } from "@/api/exb_museum/museum"; // 导入博物馆API
import { getToken } from "@/utils/auth";

export default {
  name: "Activity",
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
      // 活动信息表表格数据
      activityList: [],
      // 博物馆选项列表
      museumOptions: [],
      // 表格列信息
      columns: [
        { key: 0, label: '活动名称', visible: true },
        { key: 1, label: '所属博物馆', visible: true },
        { key: 2, label: '活动类型', visible: true },
        { key: 3, label: '活动对象', visible: true },
        { key: 4, label: '活动地点', visible: true },
        { key: 5, label: '活动开始时间', visible: true },
        { key: 6, label: '活动结束时间', visible: true },
        { key: 7, label: '报名人数', visible: true },
        { key: 8, label: '最大报名人数', visible: true },
        { key: 9, label: '主讲人或表演团队', visible: true },
        { key: 10, label: '状态', visible: true },
      ],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        activityName: null,
        museumId: null,
        activityType: null,
        location: null,
        status: null,
      },
      // 表单参数
      form: {},
      // 导入参数
      upload: {
        // 是否显示弹出层（导入）
        open: false,
        // 弹出层标题（导入）
        title: "",
        // 是否禁用上传
        isUploading: false,
        // 是否更新已经存在的活动信息表数据
        updateSupport: 0,
        // 设置上传的请求头部
        headers: { Authorization: "Bearer " + getToken() },
        // 上传的地址
        url: process.env.VUE_APP_BASE_API + "/exb_museum/activity/importData"
      },
      // 表单校验
      rules: {
        activityName: [
          { required: true, message: "活动名称不能为空", trigger: "blur" }
        ],
        museumId: [
          { required: true, message: "所属博物馆不能为空", trigger: "change" }
        ],
        activityType: [
          { required: true, message: "活动类型不能为空", trigger: "blur" }
        ],
        location: [
          { required: true, message: "活动地点不能为空", trigger: "blur" }
        ],
        activityStartTime: [
          { required: true, message: "活动开始时间不能为空", trigger: "blur" }
        ],
        activityEndTime: [
          { required: true, message: "活动结束时间不能为空", trigger: "blur" }
        ],
        status: [
          { required: true, message: "状态不能为空", trigger: "change" }
        ]
      },
      // 状态（0正常 1停用）字典
      statusOptions: [
        { value: 0, label: '正常' },
        { value: 1, label: '停用' },
      ],
    };
  },
  created() {
    this.getList();
    this.getMuseumList(); // 获取博物馆列表
  },
  methods: {
    /** 获取博物馆列表 */
    getMuseumList() {
      listMuseum().then(response => {
        this.museumOptions = response.rows;
      });
    },
    /** 查询活动信息表列表 */
    getList() {
      this.loading = true;
      listActivity(this.queryParams).then(response => {
        this.activityList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 状态（0正常 1停用）字典翻译
    dict_status_format(row, column) {
      return this.selectDictLabel(this.statusOptions, row.status);
    },
    // 所属博物馆字典翻译
    dict_museumId_format(row, column) {
      // 遍历博物馆列表，找到匹配的博物馆名称
      let museumName = '';
      this.museumOptions.forEach(item => {
        if (item.museumId === row.museumId) {
          museumName = item.museumName;
        }
      });
      return museumName;
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        activityId: null,
        activityName: null,
        introduction: null,
        activityType: null,
        targetAudience: null,
        location: null,
        activityStartTime: null,
        activityEndTime: null,
        registrationCount: 0,
        maxRegistration: 0,
        presenter: null,
        museumId: null,
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
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.activityId)
      this.single = selection.length!==1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加活动信息表";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const activityId = row.activityId || this.ids
      getActivity(activityId).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改活动信息表";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          // 数据类型转换
          const submitData = { ...this.form };
          
          // 将活动ID转为整数
          if (submitData.activityId !== null && submitData.activityId !== undefined && submitData.activityId !== "") {
            submitData.activityId = parseInt(submitData.activityId, 10);
          } else {
            submitData.activityId = null;
          }
          
          // 将博物馆ID转为整数
          if (submitData.museumId !== null && submitData.museumId !== undefined && submitData.museumId !== "") {
            submitData.museumId = parseInt(submitData.museumId, 10);
          } else {
            submitData.museumId = null;
          }
          
          // 将状态转为整数
          if (submitData.status !== null && submitData.status !== undefined && submitData.status !== "") {
            submitData.status = parseInt(submitData.status, 10);
          } else {
            submitData.status = null;
          }
          
          // 将报名人数转为整数
          if (submitData.registrationCount !== null && submitData.registrationCount !== undefined && submitData.registrationCount !== "") {
            submitData.registrationCount = parseInt(submitData.registrationCount, 10);
          } else {
            submitData.registrationCount = 0;
          }
          
          // 将最大报名人数转为整数
          if (submitData.maxRegistration !== null && submitData.maxRegistration !== undefined && submitData.maxRegistration !== "") {
            submitData.maxRegistration = parseInt(submitData.maxRegistration, 10);
          } else {
            submitData.maxRegistration = 0;
          }
          
          // 将删除标志转为整数
          if (submitData.delFlag !== null && submitData.delFlag !== undefined && submitData.delFlag !== "") {
            submitData.delFlag = parseInt(submitData.delFlag, 10);
          } else {
            submitData.delFlag = null;
          }
          
          if (submitData.activityId != null) {
            updateActivity(submitData).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addActivity(submitData).then(response => {
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
      const activityIds = row.activityId || this.ids;
      this.$modal.confirm('是否确认删除活动信息表编号为"' + activityIds + '"的数据项？').then(function() {
        return delActivity(activityIds);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('exb_museum/activity/export', {
        ...this.queryParams
      }, `activity_${new Date().getTime()}.xlsx`)
    },
    /** 导入按钮操作 */
    handleImport() {
      this.upload.title = "活动信息表导入";
      this.upload.open = true;
    },
    /** 下载模板操作 */
    importTemplate() {
      this.download(
        "exb_museum/activity/importTemplate",
        {},
        "activity_template_" + new Date().getTime() + ".xlsx"
      );
    },
    // 文件上传中处理
    handleFileUploadProgress(event, file, fileList) {
      this.upload.isUploading = true;
    },
    // 文件上传成功处理
    handleFileSuccess(response, file, fileList) {
      this.upload.open = false;
      this.upload.isUploading = false;
      this.$refs.upload.clearFiles();
      this.$alert("<div style='overflow: auto;overflow-x: hidden;max-height: 70vh;padding: 10px 20px 0;'>" + response.msg + "</div>", "导入结果", { dangerouslyUseHTMLString: true });
      this.$modal.closeLoading()
      this.getList();
    },
    // 提交上传文件
    submitFileForm() {
      this.$modal.loading("导入中请稍后")
      this.$refs.upload.submit();
    },
  }
};
</script>

<style scoped>
</style>