<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="88px">
      <el-form-item label="藏品名" prop="collectionName">
        <el-input
          v-model="queryParams.collectionName"
          placeholder="请输入藏品名"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="类型" prop="collectionType">
        <el-select v-model="queryParams.collectionType" placeholder="请选择类型" clearable filterable>
          <el-option v-for="item in collectionTypeOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="所属展览" prop="exhibitionId">
        <el-select v-model="queryParams.exhibitionId" placeholder="请选择所属展览" clearable @change="handleExhibitionChange" filterable>
          <el-option
            v-for="exhibition in exhibitionOptions"
            :key="exhibition.exhibitionId"
            :label="exhibition.exhibitionName"
            :value="exhibition.exhibitionId"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="所属博物馆" prop="museumId">
        <el-select v-model="queryParams.museumId" placeholder="请选择所属博物馆" clearable :disabled="!!queryParams.exhibitionId" filterable>
          <el-option
            v-for="museum in museumOptions"
            :key="museum.museumId"
            :label="museum.museumName"
            :value="museum.museumId"
          />
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
          v-hasPermi="['exb_museum:collection:add']"
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
          v-hasPermi="['exb_museum:collection:edit']"
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
          v-hasPermi="['exb_museum:collection:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['exb_museum:collection:export']"
        >导出</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="el-icon-upload2"
          size="mini"
          @click="handleImport"
          v-hasPermi="['exb_museum:collection:import']"
        >导入</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" :columns="columns"></right-toolbar>
    </el-row>

    <el-table :loading="loading" :data="collectionList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="藏品名" :show-overflow-tooltip="true" v-if="columns[0].visible" prop="collectionName" />
      <el-table-column label="类型" align="center" :show-overflow-tooltip="true" v-if="columns[1].visible" prop="collectionType" :formatter="dict_collectionType_format" />
      <el-table-column label="材质" align="center" :show-overflow-tooltip="true" v-if="columns[2].visible" prop="material" />
      <el-table-column label="年代" align="center" :show-overflow-tooltip="true" v-if="columns[3].visible" prop="age" />
      <el-table-column label="所属展览" align="center" :show-overflow-tooltip="true" v-if="columns[4].visible" prop="exhibitionName" :formatter="dict_exhibitionId_format" />
      <el-table-column label="所属博物馆" align="center" :show-overflow-tooltip="true" v-if="columns[5].visible" prop="museumName" :formatter="dict_museumId_format" />
      <el-table-column label="状态" align="center" :show-overflow-tooltip="true" v-if="columns[6].visible" prop="status" :formatter="dict_status_format" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['exb_museum:collection:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['exb_museum:collection:remove']"
          >删除</el-button>
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

    <!-- 添加或修改藏品信息表对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="藏品名" prop="collectionName">
          <el-input v-model="form.collectionName" placeholder="请输入藏品名" />
        </el-form-item>
        <el-form-item label="类型" prop="collectionType">
          <el-select v-model="form.collectionType" placeholder="请选择类型" clearable filterable>
            <el-option v-for="item in collectionTypeOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="尺寸" prop="sizeInfo">
          <el-input v-model="form.sizeInfo" placeholder="请输入尺寸" />
        </el-form-item>
        <el-form-item label="材质" prop="material">
          <el-select v-model="materialValues" multiple filterable placeholder="请选择材质" style="width: 100%">
            <el-option v-for="material in materialOptions" :key="material.value" :label="material.label" :value="material.value"/>
          </el-select>
        </el-form-item>
        <el-form-item label="年代" prop="age">
          <el-select v-model="form.age" placeholder="请选择年代" clearable>
            <el-option v-for="dict in ageOptions" :key="dict.value" :label="dict.label" :value="dict.value"/>
          </el-select>
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="form.author" placeholder="请输入作者" />
        </el-form-item>
        <el-form-item label="藏品简介" prop="description">
          <el-input v-model="form.description" placeholder="请输入藏品简介" />
        </el-form-item>
        <el-form-item label="所属展览" prop="exhibitionId">
          <el-select v-model="form.exhibitionId" placeholder="请选择所属展览" clearable @change="handleExhibitionChangeForForm" filterable>
            <el-option v-for="exhibition in exhibitionOptions" :key="exhibition.exhibitionId" :label="exhibition.exhibitionName" :value="exhibition.exhibitionId"/>
          </el-select>
        </el-form-item>
        <el-form-item label="所属博物馆" prop="museumId">
          <el-select v-model="form.museumId" placeholder="请选择所属博物馆" clearable :disabled="!!form.exhibitionId" filterable>
            <el-option v-for="museum in museumOptions" :key="museum.museumId" :label="museum.museumName" :value="museum.museumId"/>
          </el-select>
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
            <el-checkbox v-model="upload.updateSupport" /> 是否更新已经存在的藏品信息表数据
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
      :objectType="'collection'"
      :objectId="currentCollectionId"
      :visible.sync="mediaDialogVisible"
    />
  </div>
</template>

<script>
import { listCollection, getCollection, delCollection, addCollection, updateCollection } from "@/api/exb_museum/collection";
import { listMuseum } from "@/api/exb_museum/museum"; // 导入博物馆API
import { listExhibition } from "@/api/exb_museum/exhibition"; // 导入展览API
import { getToken } from "@/utils/auth";
import MediaUpload from "@/components/MediaUpload/index.vue";

export default {
  name: "Collection",
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
      // 藏品信息表表格数据
      collectionList: [],
      // 博物馆选项列表
      museumOptions: [],
      // 展览选项列表
      exhibitionOptions: [],
      // 材质选项列表
      materialOptions: [
        { label: '布面', value: '布面' },
        { label: '纸张', value: '纸张' },
        { label: '丝绸', value: '丝绸' },
        { label: '木头', value: '木头' },
        { label: '竹子', value: '竹子' },
        { label: '陶瓷', value: '陶瓷' },
        { label: '瓷器', value: '瓷器' },
        { label: '青铜', value: '青铜' },
        { label: '铁', value: '铁' },
        { label: '银', value: '银' },
        { label: '金', value: '金' },
        { label: '玉石', value: '玉石' },
        { label: '象牙', value: '象牙' },
        { label: '骨', value: '骨' },
        { label: '漆', value: '漆' },
        { label: '玻璃', value: '玻璃' },
        { label: '水晶', value: '水晶' },
        { label: '宝石', value: '宝石' },
        { label: '珍珠', value: '珍珠' },
      ],
      // 材质选中值（用于多选控件）
      materialValues: [],
      // 年代选项列表
      ageOptions: [
        { label: '史前时期', value: '史前时期' },
        { label: '夏商周', value: '夏商周' },
        { label: '春秋战国', value: '春秋战国' },
        { label: '秦汉', value: '秦汉' },
        { label: '魏晋南北朝', value: '魏晋南北朝' },
        { label: '隋唐', value: '隋唐' },
        { label: '五代十国', value: '五代十国' },
        { label: '宋元', value: '宋元' },
        { label: '明清', value: '明清' },
        { label: '民国', value: '民国' },
        { label: '现代', value: '现代' },
        { label: '当代', value: '当代' },
        { label: '其他', value: '其他' },
      ],
      // 表格列信息
      columns: [
        { key: 0, label: '藏品名', visible: true },
        { key: 1, label: '类型', visible: true },
        { key: 2, label: '材质', visible: true },
        { key: 3, label: '年代', visible: true },
        { key: 4, label: '所属展览', visible: true },
        { key: 5, label: '所属博物馆', visible: true },
        { key: 6, label: '状态', visible: true },
      ],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        collectionName: null,
        collectionType: null,
        exhibitionId: null,
        museumId: null,
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
        // 是否更新已经存在的藏品信息表数据
        updateSupport: 0,
        // 设置上传的请求头部
        headers: { Authorization: "Bearer " + getToken() },
        // 上传的地址
        url: process.env.VUE_APP_BASE_API + "/exb_museum/collection/importData"
      },
      // 表单校验
      rules: {
        collectionId: [
          { required: true, message: "藏品ID不能为空", trigger: "blur" }
        ],
        collectionName: [
          { required: true, message: "藏品名不能为空", trigger: "blur" }
        ],
        collectionType: [
          { required: true, message: "类型不能为空", trigger: "change" }
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
      // 藏品类型字典
      collectionTypeOptions: [
        { value: '油画', label: '油画' },
        { value: '国画', label: '国画' },
        { value: '书法', label: '书法' },
        { value: '素描', label: '素描' },
        { value: '水彩画', label: '水彩画' },
        { value: '版画', label: '版画' },
        { value: '雕塑', label: '雕塑' },
        { value: '瓷器', label: '瓷器' },
        { value: '陶器', label: '陶器' },
        { value: '青铜器', label: '青铜器' },
        { value: '玉器', label: '玉器' },
        { value: '金银器', label: '金银器' },
        { value: '珠宝首饰', label: '珠宝首饰' },
        { value: '纺织品', label: '纺织品' },
        { value: '家具', label: '家具' },
        { value: '古籍善本', label: '古籍善本' },
        { value: '碑帖', label: '碑帖' },
        { value: '印章', label: '印章' },
        { value: '钱币', label: '钱币' },
        { value: '邮票', label: '邮票' },
        { value: '文房四宝', label: '文房四宝' },
        { value: '乐器', label: '乐器' },
        { value: '兵器', label: '兵器' },
        { value: '交通工具', label: '交通工具' },
        { value: '生活用品', label: '生活用品' },
        { value: '科学仪器', label: '科学仪器' },
        { value: '医疗器械', label: '医疗器械' },
        { value: '宗教用品', label: '宗教用品' },
        { value: '民俗用品', label: '民俗用品' },
      ],
      
      // 媒体上传相关
      mediaDialogVisible: false,
      currentCollectionId: null,
    };
  },
  created() {
    this.getList();
    this.getMuseumList(); // 获取博物馆列表
    this.getExhibitionList(); // 获取展览列表
  },
  methods: {
    /** 获取博物馆列表 */
    getMuseumList() {
      listMuseum().then(response => {
        this.museumOptions = response.rows;
      });
    },
    /** 获取展览列表 */
    getExhibitionList() {
      listExhibition().then(response => {
        this.exhibitionOptions = response.rows;
      });
    },
    /** 查询藏品信息表列表 */
    getList() {
      this.loading = true;
      listCollection(this.queryParams).then(response => {
        this.collectionList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 状态（0正常 1停用）字典翻译
    dict_status_format(row, column) {
      return this.selectDictLabel(this.statusOptions, row.status);
    },
    // 藏品类型字典翻译
    dict_collectionType_format(row, column) {
      return this.selectDictLabel(this.collectionTypeOptions, row.collectionType);
    },
    // 所属展览字典翻译
    dict_exhibitionId_format(row, column) {
      // 遍历展览列表，找到匹配的展览名称
      let exhibitionName = '';
      this.exhibitionOptions.forEach(item => {
        if (item.exhibitionId === row.exhibitionId) {
          exhibitionName = item.exhibitionName;
        }
      });
      return exhibitionName;
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
        collectionId: null,
        collectionName: null,
        collectionType: null,
        sizeInfo: null,
        material: null,
        age: null,
        author: null,
        description: null,
        exhibitionId: null,
        museumId: null,
        status: null,
        delFlag: null,
        createBy: null,
        createTime: null,
        updateBy: null,
        updateTime: null,
        remark: null
      };
      this.materialValues = [];
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
      this.ids = selection.map(item => item.collectionId)
      this.single = selection.length!==1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加藏品信息表";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const collectionId = row.collectionId || this.ids
      getCollection(collectionId).then(response => {
        this.form = response.data;
        // 将材质字符串转换为数组
        if (this.form.material) {
          this.materialValues = this.form.material.split(',');
        } else {
          this.materialValues = [];
        }
        this.open = true;
        this.title = "修改藏品信息表";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          const submitData = this.buildSubmitData();
          if (submitData.collectionId != null) {
            updateCollection(submitData).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addCollection(submitData).then(response => {
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
      const collectionIds = row.collectionId || this.ids;
      this.$modal.confirm('是否确认删除藏品信息表编号为"' + collectionIds + '"的数据项？').then(function() {
        return delCollection(collectionIds);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    // 查询表单中展览选择变化的处理方法
    handleExhibitionChange(val) {
      if (val) {
        // 根据选择的展览获取对应的博物馆ID并设置到博物馆字段
        const exhibition = this.exhibitionOptions.find(item => item.exhibitionId === val);
        if (exhibition && exhibition.museumId) {
          this.queryParams.museumId = exhibition.museumId;
        }
      }
    },
    // 添加/修改表单中展览选择变化的处理方法
    handleExhibitionChangeForForm(val) {
      if (val) {
        // 根据选择的展览获取对应的博物馆ID并设置到博物馆字段
        const exhibition = this.exhibitionOptions.find(item => item.exhibitionId === val);
        if (exhibition && exhibition.museumId) {
          this.form.museumId = exhibition.museumId;
        }
      }
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('exb_museum/collection/export', {
        ...this.queryParams
      }, `collection_${new Date().getTime()}.xlsx`)
    },
    /** 导入按钮操作 */
    handleImport() {
      this.upload.title = "藏品信息表导入";
      this.upload.open = true;
    },
    /** 下载模板操作 */
    importTemplate() {
      this.download(
        "exb_museum/collection/importTemplate",
        {},
        "collection_template_" + new Date().getTime() + ".xlsx"
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
      // 将材质选中值转换为逗号分隔的字符串
      if (this.materialValues && this.materialValues.length > 0) {
        data.material = this.materialValues.join(',');
      } else {
        data.material = null;
      }
      
      if (data.collectionId !== null && data.collectionId !== undefined && data.collectionId !== "") {
        data.collectionId = parseInt(data.collectionId, 10);
      } else {
        data.collectionId = null;
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

    /** 打开媒体上传对话框 */
    openMediaDialog(row) {
      this.currentCollectionId = row.collectionId;
      this.mediaDialogVisible = true;
      this.loadMediaList();
    },
  }
};
</script>