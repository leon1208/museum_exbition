<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="88px">
      <el-form-item label="展名" prop="exhibitionName">
        <el-input
          v-model="queryParams.exhibitionName"
          placeholder="请输入展名"
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
      <el-form-item label="主办单位" prop="organizer">
        <el-input
          v-model="queryParams.organizer"
          placeholder="请输入主办单位"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="展览类型" prop="exhibitionType">
        <el-select v-model="queryParams.exhibitionType" placeholder="请选择展览类型" clearable>
          <el-option v-for="item in exhibitionTypeOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
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
          v-hasPermi="['exb_museum:exhibition:add']"
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
          v-hasPermi="['exb_museum:exhibition:edit']"
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
          v-hasPermi="['exb_museum:exhibition:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['exb_museum:exhibition:export']"
        >导出</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="el-icon-upload2"
          size="mini"
          @click="handleImport"
          v-hasPermi="['exb_museum:exhibition:import']"
        >导入</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" :columns="columns"></right-toolbar>
    </el-row>

    <el-table :loading="loading" :data="exhibitionList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="展名" :show-overflow-tooltip="true" v-if="columns[0].visible" prop="exhibitionName" />
      <el-table-column label="所属博物馆" align="center" :show-overflow-tooltip="true" v-if="columns[1].visible" prop="museumName" :formatter="dict_museumId_format" />
      <el-table-column label="展厅" align="center" :show-overflow-tooltip="true" v-if="columns[2].visible" prop="hall" />
      <el-table-column label="展览开始时间" align="center" v-if="columns[3].visible" prop="startTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.startTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="展览结束时间" align="center" v-if="columns[4].visible" prop="endTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.endTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="主办单位" align="center" :show-overflow-tooltip="true" v-if="columns[5].visible" prop="organizer" />
      <el-table-column label="展览类型" align="center" :show-overflow-tooltip="true" v-if="columns[6].visible" prop="exhibitionType" :formatter="dict_exhibitionType_format" />
      <el-table-column label="内容标签" align="center" :show-overflow-tooltip="true" v-if="columns[7].visible" prop="contentTags" />
      <el-table-column label="状态" align="center" :show-overflow-tooltip="true" v-if="columns[8].visible" prop="status" :formatter="dict_status_format" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['exb_museum:exhibition:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['exb_museum:exhibition:remove']"
          >删除</el-button>
          <el-button
            size="mini"
type="text"
            icon="el-icon-folder-opened"
            @click="openExhibitionUnitDialog(scope.row)"
            v-hasPermi="['exb_museum:unit:list']"
          >展览单元管理</el-button>
          <el-button
size="mini"
            type="text"
            icon="el-icon-picture-outline"
            @click="openMediaDialog(scope.row)"
            v-hasPermi="['exb_museum:media:add']"
          >媒体管理</el-button>
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

    <!-- 添加或修改展览信息表对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="展名" prop="exhibitionName">
          <el-input v-model="form.exhibitionName" placeholder="请输入展名" />
        </el-form-item>
        <el-form-item label="展览简介" prop="description">
          <el-input v-model="form.description" placeholder="请输入展览简介" />
        </el-form-item>
        <el-form-item label="所属博物馆" prop="museumId">
          <el-select v-model="form.museumId" placeholder="请选择所属博物馆" @change="handleMuseumChange">
            <el-option v-for="museum in museumOptions" :key="museum.museumId" :label="museum.museumName" :value="museum.museumId"/>
          </el-select>
        </el-form-item>
        <el-form-item label="展厅" prop="hall">
          <el-select v-model="selectedHalls" multiple filterable placeholder="请选择展厅" style="width: 100%">
            <el-option v-for="hall in hallOptions" :key="hall.hallId" :label="hall.hallName" :value="hall.hallId"/>
          </el-select>
        </el-form-item>
        <el-form-item label="展览开始时间" prop="startTime">
          <el-date-picker clearable
            v-model="form.startTime"
            type="date"
            value-format="yyyy-MM-dd"
            placeholder="选择展览开始时间">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="展览结束时间" prop="endTime">
          <el-date-picker clearable
            v-model="form.endTime"
            type="date"
            value-format="yyyy-MM-dd"
            placeholder="选择展览结束时间">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="主办单位" prop="organizer">
          <el-input v-model="form.organizer" placeholder="请输入主办单位" />
        </el-form-item>
        <el-form-item label="展览类型" prop="exhibitionType">
          <el-select v-model="form.exhibitionType" placeholder="请选择展览类型">
            <el-option v-for="item in exhibitionTypeOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="内容标签" prop="contentTags">
<el-select v-model="contentTagValues" multiple filterable placeholder="请选择内容标签" style="width: 100%">
            <el-option v-for="tag in contentTagOptions" :key="tag.value" :label="tag.label" :value="tag.value"/>
          </el-select>
        </el-form-item>

        <el-form-item label="展览章节" prop="sections">
          <div class="section-container">
            <div v-for="(section, index) in form.sections" :key="index" class="section-item">
              <el-card class="section-card">
                <div class="section-content" style="display: flex; align-items: center;">
                  <el-input v-model="section.content" placeholder="请输入章节标题" style="flex: 1; margin-right: 2px;" />
                  <el-button-group>
                    <el-button type="text" size="mini" @click="moveSectionUp(index)" :disabled="index === 0" icon="el-icon-arrow-up"></el-button>
                    <el-button type="text" size="mini" @click="moveSectionDown(index)" :disabled="index === form.sections.length - 1" icon="el-icon-arrow-down"></el-button>
                    <el-button type="text" size="mini" @click="removeSection(index)" style="color: #f56c6c" icon="el-icon-delete"></el-button>
                  </el-button-group>
                </div>
              </el-card>
            </div>
            <el-button type="primary" size="mini" @click="addSection" icon="el-icon-plus">添加章节</el-button>
          </div>
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
            <el-checkbox v-model="upload.updateSupport" /> 是否更新已经存在的展览信息表数据
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

    <!-- 媒体上传对话框 - 使用可复用组件 -->
    <MediaUpload 
      :objectType="'exhibition'"
      :objectId="currentExhibitionId"
      :visible.sync="mediaDialogVisible"
    />

    <!-- 展览单元管理对话框 -->
    <el-dialog 
      :title="currentExhibition ? '展览单元管理 - ' + currentExhibition.exhibitionName : '展览单元管理'" 
      :visible.sync="exhibitionUnitDialogVisible" 
      width="80%" 
      append-to-body
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <ExhibitionUnit 
        v-if="exhibitionUnitDialogVisible"
        :exhibitionId="currentExhibition ? currentExhibition.exhibitionId : null"
        :museumId="currentExhibition ? currentExhibition.museumId : null"
        @close="exhibitionUnitDialogVisible = false"
      />
    </el-dialog>

  </div>
</template>

<script>
import { listExhibition, getExhibition, delExhibition, addExhibition, updateExhibition } from "@/api/exb_museum/exhibition";
import { listMuseum } from "@/api/exb_museum/museum"; // 导入博物馆API
import { getToken } from "@/utils/auth";
import MediaUpload from "@/components/MediaUpload/index.vue";
import ExhibitionUnit from "@/views/exb_museum/exhibition_unit/index.vue";
import { listMuseumHall } from "@/api/exb_museum/museum_hall"; // 导入展厅API

export default {
  name: "Exhibition",
  components: {
    MediaUpload,
    ExhibitionUnit,
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
      // 展览信息表表格数据
      exhibitionList: [],
      // 博物馆选项列表
      museumOptions: [],
      // 展厅选项列表
      hallOptions: [],
      // 已选中的展厅ID列表
      selectedHalls: [],
      // 内容标签选项列表
      contentTagOptions: [
        { label: '艺术', value: '艺术' },
        { label: '历史', value: '历史' },
        { label: '文化', value: '文化' },
        { label: '科技', value: '科技' },
        { label: '考古', value: '考古' },
{ label: '古代', value: '古代' },
        { label: '现代', value: '现代' },
        { label: '当代', value: '当代' },
        { label: '文物', value: '文物' },
        { label: '绘画', value: '绘画' },
        { label: '雕塑', value: '雕塑' },
        { label: '陶瓷', value: '陶瓷' },
        { label: '青铜器', value: '青铜器' },
        { label: '玉器', value: '玉器' },
        { label: '金银器', value: '金银器' },
        { label: '服饰', value: '服饰' },
        { label: '家具', value: '家具' },
        { label: '文献', value: '文献' },
        { label: '自然', value: '自然' },
        { label: '生物', value: '生物' },
        { label: '矿物', value: '矿物' },
        { label: '地质', value: '地质' },
        { label: '民俗', value: '民俗' },
        { label: '民族', value: '民族' },
        { label: '宗教', value: '宗教' },
        { label: '建筑', value: '建筑' },
        { label: '军事', value: '军事' },
        { label: '航海', value: '航海' },
        { label: '天文', value: '天文' },
        { label: '医学', value: '医学' },
      ],
      // 内容标签选中值（用于多选控件）
      contentTagValues: [],
      // 表格列信息
      columns: [
        { key: 0, label: '展名', visible: true },
        { key: 1, label: '所属博物馆', visible: true },
        { key: 2, label: '展厅', visible: true },
        { key: 3, label: '展览开始时间', visible: true },
        { key: 4, label: '展览结束时间', visible: true },
        { key: 5, label: '主办单位', visible: true },
        { key: 6, label: '展览类型（0长期 1临时）', visible: true },
        { key: 7, label: '内容标签', visible: true },
        { key: 8, label: '状态（0正常 1停用）', visible: true },
      ],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 展览开始时间时间范围
      dateRangeStartTime: [],
      // 展览结束时间时间范围
      dateRangeEndTime: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        exhibitionName: null,
        museumId: null,
        organizer: null,
        exhibitionType: null,
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
        // 是否更新已经存在的展览信息表数据
        updateSupport: 0,
        // 设置上传的请求头部
        headers: { Authorization: "Bearer " + getToken() },
        // 上传的地址
        url: process.env.VUE_APP_BASE_API + "/exb_museum/exhibition/importData"
      },
      // 表单校验
      rules: {
        exhibitionId: [
          { required: true, message: "展览ID不能为空", trigger: "blur" }
        ],
        exhibitionName: [
          { required: true, message: "展名不能为空", trigger: "blur" }
        ],
        museumId: [
          { required: true, message: "所属博物馆不能为空", trigger: "change" }
        ],
        startTime: [
          { required: true, message: "展览开始时间不能为空", trigger: "blur" }
        ],
        endTime: [
          { required: true, message: "展览结束时间不能为空", trigger: "blur" }
        ],
        exhibitionType: [
          { required: true, message: "展览类型不能为空", trigger: "change" }
        ],
        status: [
          { required: true, message: "状态不能为空", trigger: "change" }
        ],
        createTime: [
          { required: true, message: "创建时间不能为空", trigger: "blur" }
        ],
        updateTime: [
          { required: true, message: "更新时间不能为空", trigger: "blur" }
        ]
      },
      // 状态（0正常 1停用）字典
      statusOptions: [
        { value: 0, label: '正常' },
        { value: 1, label: '停用' },
      ],
      // 展览类型（0长期 1临时）字典
      exhibitionTypeOptions: [
        { value: 0, label: '长期' },
        { value: 1, label: '临时' },
      ],
      // 媒体上传相关
      mediaDialogVisible: false,
      currentExhibitionId: 0,
      // 展览单元管理对话框
      exhibitionUnitDialogVisible: false,
      currentExhibition: null,
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
    /** 根据博物馆ID获取展厅列表 */
    getHallListByMuseumId(museumId) {
      if (!museumId) {
        this.hallOptions = [];
        return Promise.resolve(); // 返回resolved promise
      }
      
      const query = { museumId: museumId };
      return listMuseumHall(query).then(response => {
        this.hallOptions = response.rows || [];
      });
    },
    /** 当博物馆改变时，更新展厅选项 */
    handleMuseumChange(museumId) {
      this.selectedHalls = []; // 清空已选展厅
      this.getHallListByMuseumId(museumId);
    },
    /** 查询展览信息表列表 */
    getList() {
      this.loading = true;
      this.queryParams.params = {};
      if (null != this.dateRangeStartTime && '' != this.dateRangeStartTime.toString()) {
        this.queryParams.params["beginstartTime"] = this.dateRangeStartTime[0];
        this.queryParams.params["endstartTime"] = this.dateRangeStartTime[1];
      }
      this.queryParams.params = {};
      if (null != this.dateRangeEndTime && '' != this.dateRangeEndTime.toString()) {
        this.queryParams.params["beginendTime"] = this.dateRangeEndTime[0];
        this.queryParams.params["endendTime"] = this.dateRangeEndTime[1];
      }
      listExhibition(this.queryParams).then(response => {
        this.exhibitionList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 状态（0正常 1停用）字典翻译
    dict_status_format(row, column) {
      return this.selectDictLabel(this.statusOptions, row.status);
    },
    // 展览类型（0长期 1临时）字典翻译
    dict_exhibitionType_format(row, column) {
      return this.selectDictLabel(this.exhibitionTypeOptions, row.exhibitionType);
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
        exhibitionId: null,
        exhibitionName: null,
        description: null,
        museumId: null,
        hall: null,
        startTime: null,
        endTime: null,
        organizer: null,
        exhibitionType: null,
        contentTags: null,
        sections: [],
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
      this.dateRangeStartTime = [];
      this.dateRangeEndTime = [];
      this.resetForm("queryForm");
      this.handleQuery();
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.exhibitionId)
      this.single = selection.length!==1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加展览信息表";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const exhibitionId = row.exhibitionId || this.ids
      getExhibition(exhibitionId).then(response => {
        this.form = response.data;
        // 将内容标签字符串转换为数组
        if (this.form.contentTags) {
          this.contentTagValues = this.form.contentTags.split(',');
        } else {
          this.contentTagValues = [];
        }
        // 将展览章节字符串转换为数组
        if (this.form.sections) {
          this.form.sections = JSON.parse(this.form.sections);
        } else {
          this.form.sections = [];
        }
        
        // 将展厅字符串转换为展厅ID数组
        if (this.form.hall) {
          // 先获取对应博物馆的展厅列表
          this.getHallListByMuseumId(this.form.museumId).then(() => {
            // 等待展厅列表加载完成后，根据展厅名称找到对应的ID
            const hallNames = this.form.hall.split(',');
            this.selectedHalls = [];
            hallNames.forEach(name => {
              const hall = this.hallOptions.find(h => h.hallName === name.trim());
              if (hall) {
                this.selectedHalls.push(hall.hallId);
              }
            });
          });
        } else {
          this.selectedHalls = [];
        }
        
        this.open = true;
        this.title = "修改展览信息表";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          const submitData = this.buildSubmitData();
          if (submitData.exhibitionId != null) {
            updateExhibition(submitData).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addExhibition(submitData).then(response => {
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
      const exhibitionIds = row.exhibitionId || this.ids;
      this.$modal.confirm('是否确认删除展览信息表编号为"' + exhibitionIds + '"的数据项？').then(function() {
        return delExhibition(exhibitionIds);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('exb_museum/exhibition/export', {
        ...this.queryParams
      }, `exhibition_${new Date().getTime()}.xlsx`)
    },
    /** 导入按钮操作 */
    handleImport() {
      this.upload.title = "展览信息表导入";
      this.upload.open = true;
    },
    /** 下载模板操作 */
    importTemplate() {
      this.download(
        "exb_museum/exhibition/importTemplate",
        {},
        "exhibition_template_" + new Date().getTime() + ".xlsx"
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
    buildSubmitData() {
      const data = { ...this.form };
      
      // 将选中的展厅ID转换为展厅名称并拼接成逗号分隔的字符串
      if (this.selectedHalls && this.selectedHalls.length > 0) {
        const selectedHallNames = this.selectedHalls.map(id => {
          const hall = this.hallOptions.find(h => h.hallId === id);
          return hall ? hall.hallName : '';
        }).filter(name => name !== '');
        data.hall = selectedHallNames.join(',');
      } else {
        data.hall = null;
      }
      
      // 将内容标签选中值转换为逗号分隔的字符串
      if (this.contentTagValues && this.contentTagValues.length > 0) {
        data.contentTags = this.contentTagValues.join(',');
      } else {
        data.contentTags = null;
      }
      // 将展览章节数组转换为JSON字符串
      if (data.sections && Array.isArray(data.sections)) {
        data.sections = JSON.stringify(data.sections);
      } else {
        data.sections = null;
      }
      if (data.exhibitionId !== null && data.exhibitionId !== undefined && data.exhibitionId !== "") {
        data.exhibitionId = parseInt(data.exhibitionId, 10);
      } else {
        data.exhibitionId = null;
      }
      if (data.museumId !== null && data.museumId !== undefined && data.museumId !== "") {
        data.museumId = parseInt(data.museumId, 10);
      } else {
        data.museumId = null;
      }
      if (data.exhibitionType !== null && data.exhibitionType !== undefined && data.exhibitionType !== "") {
        data.exhibitionType = parseInt(data.exhibitionType, 10);
      } else {
        data.exhibitionType = null;
      }
      if (data.status !== null && data.status !== undefined && data.status !== "") {
        data.status = parseInt(data.status, 10);
      } else {
        data.status = null;
      }
      if (data.delFlag !== null && data.delFlag !== undefined && data.delFlag !== "") {
        data.delFlag = parseInt(data.delFlag, 10);
      } else {
        data.delFlag = null;
      }
      return data;
    },
    // 提交上传文件
    submitFileForm() {
      this.$modal.loading("导入中请稍后")
      this.$refs.upload.submit();
    },

    /** 打开展览单元管理对话框 */
    openExhibitionUnitDialog(row) {
      this.currentExhibition = row;
      this.exhibitionUnitDialogVisible = true;
    },

    /** 打开媒体上传对话框 */
    openMediaDialog(row) {
      this.currentExhibitionId = row.exhibitionId;
      this.mediaDialogVisible = true;
    },

    addSection() {
      if (!this.form.sections) {
        this.form.sections = [];
      }
      this.form.sections.push({
        content: ''
      });
    },
    removeSection(index) {
      this.form.sections.splice(index, 1);
    },
    moveSectionUp(index) {
      if (index > 0) {
        // 使用数组解构交换元素位置
        [this.form.sections[index], this.form.sections[index - 1]] = [this.form.sections[index - 1], this.form.sections[index]];
        // 触发响应式更新
        this.$set(this.form, 'sections', [...this.form.sections]);
      }
    },
    moveSectionDown(index) {
      if (index < this.form.sections.length - 1) {
        // 使用数组解构交换元素位置
        [this.form.sections[index], this.form.sections[index + 1]] = [this.form.sections[index + 1], this.form.sections[index]];
        // 触发响应式更新
        this.$set(this.form, 'sections', [...this.form.sections]);
      }
    }
  }
};
</script>

<style scoped>
/* 添加一些样式以美化章节编辑界面 */
.section-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 10px;
}

.section-item {
  margin-bottom: 5px;
}

.section-card {
  margin-bottom: 5px;
  padding: 5px;
}
</style>