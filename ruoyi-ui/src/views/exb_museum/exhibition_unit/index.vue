<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="100px">
      <el-form-item label="所属展览章节" prop="section">
        <el-select
          v-model="queryParams.section"
          placeholder="请选择所属展览章节"
          clearable
          style="width: 200px;"
        >
          <el-option
            v-for="section in sectionOptions"
            :key="section.content"
            :label="section.content"
            :value="section.content"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="单元名称" prop="unitName">
        <el-input
          v-model="queryParams.unitName"
          placeholder="请输入单元名称"
          clearable
          @keyup.enter.native="handleQuery"
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
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['exb_museum:unit:add']"
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
          v-hasPermi="['exb_museum:unit:edit']"
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
          v-hasPermi="['exb_museum:unit:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['exb_museum:unit:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" :columns="columns"></right-toolbar>
    </el-row>

    <!-- 按展览章节分组显示 -->
    <el-collapse v-model="activeNames">
    <!-- <el-collapse v-model="activeNames" accordion> -->
      <el-collapse-item 
        v-for="(section, index) in orderedSections" 
        :key="section.content"
        :title="section.content" 
        :name="section.content"
      >
        <el-table 
          :data="getUnitsBySection(section.content)" 
          :row-class-name="tableRowClassName"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="expand">
            <template slot-scope="scope">
              <div>导览词:{{ scope.row.guideText }}</div>
              <div v-if="scope.row.mediaList && scope.row.mediaList.length > 0" class="media-list">
                <el-image 
                  v-for="(media, index) in scope.row.mediaList" 
                  :key="media.mediaId" 
                  :src="minioBase + media.mediaUrl" 
                  :preview-src-list="scope.row.mediaList.map(m => minioBase + m.mediaUrl)"
                  fit="cover"
                  style="width: 100px; height: 100px; margin-right: 10px; margin-bottom: 10px; cursor: pointer;"
                ></el-image>
              </div>
              <span v-else>暂无媒体</span>
            </template>
          </el-table-column>

          <el-table-column type="selection" width="55" align="center" />
          <el-table-column label="单元名称" :show-overflow-tooltip="true" v-if="columns[0].visible" prop="unitName" />
          <el-table-column label="单元类型" align="center" :show-overflow-tooltip="true" v-if="columns[1].visible" prop="unitType" :formatter="dict_unitType_format" />
          <el-table-column label="展厅" align="center" :show-overflow-tooltip="true" v-if="columns[2].visible" prop="hallId" :formatter="dict_hallId_format" />
          <el-table-column label="所属展览章节" align="center" :show-overflow-tooltip="true" v-if="columns[3].visible" prop="section" />
          <el-table-column label="顺序" align="center" prop="sortOrder" width="100">
            <template #default="scope">
              <div class="sort-buttons">
                <el-button size="medium" type="text" icon="el-icon-arrow-up"
                  @click="moveUp(scope.row)" :disabled="scope.$index === 0 || !canMoveUp(scope.row, scope.$index)"
                />
                <span class="sort-value">{{ scope.row.sortOrder}}</span>
                <el-button size="medium" type="text" icon="el-icon-arrow-down"
                  @click="moveDown(scope.row)" :disabled="!canMoveDown(scope.row, scope.$index)"
                />
              </div>
            </template>
          </el-table-column>          
          <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="text"
                icon="el-icon-edit"
                @click="handleUpdate(scope.row)"
                v-hasPermi="['exb_museum:unit:edit']"
              >修改</el-button>
              <el-button
                size="mini"
                type="text"
                icon="el-icon-delete"
                @click="handleDelete(scope.row)"
                v-hasPermi="['exb_museum:unit:remove']"
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
      </el-collapse-item>
    </el-collapse>

    <!-- 如果没有分组数据，则显示原始表格 -->
    <!-- <el-table 
      v-if="orderedSections.length === 0" 
      :loading="loading" 
      :data="exhibitionUnitList" 
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="单元名称" :show-overflow-tooltip="true" v-if="columns[0].visible" prop="unitName" />
      <el-table-column label="单元类型" align="center" :show-overflow-tooltip="true" v-if="columns[1].visible" prop="unitType" :formatter="dict_unitType_format" />
      <el-table-column label="展厅" align="center" :show-overflow-tooltip="true" v-if="columns[2].visible" prop="hallId" :formatter="dict_hallId_format" />
      <el-table-column label="所属展览章节" align="center" :show-overflow-tooltip="true" v-if="columns[3].visible" prop="section" />
      <el-table-column label="顺序" align="center" v-if="columns[4].visible" prop="sortOrder" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['exb_museum:unit:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['exb_museum:unit:remove']"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table> -->

    <!-- <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    /> -->

    <!-- 添加或修改展览单元信息表对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="800px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="单元名称" prop="unitName">
          <el-input v-model="form.unitName" placeholder="请输入单元名称" />
        </el-form-item>
        <el-form-item label="单元类型" prop="unitType">
          <el-select v-model="form.unitType" placeholder="请选择单元类型" @change="handleUnitTypeChange">
            <el-option v-for="item in unitTypeOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="展厅" prop="hallId">
          <el-select v-model="form.hallId" placeholder="请选择展厅" filterable>
            <el-option v-for="hall in hallOptions" :key="hall.hallId" :label="hall.hallName" :value="hall.hallId" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属展览章节" prop="section">
          <el-select v-model="form.section" placeholder="请选择所属展览章节" filterable style="width: 100%;">
            <el-option
              v-for="section in sectionOptions"
              :key="section.content"
              :label="section.content"
              :value="section.content"
            />
          </el-select>
        </el-form-item>
        <!-- <el-form-item label="顺序" prop="sortOrder">
          <el-input-number v-model="form.sortOrder" placeholder="请输入顺序" :min="0" :max="999" />
        </el-form-item> -->
        <el-form-item label="展签" prop="exhibitLabel">
          <el-input v-model="form.exhibitLabel" type="textarea" placeholder="请输入展签" rows="4" />
        </el-form-item>
        <el-form-item label="导览词" prop="guideText">
          <el-input v-model="form.guideText" type="textarea" placeholder="请输入导览词" rows="8" />
        </el-form-item>
        <el-form-item v-if="showCopyMediaCheckbox" label="关联藏品" prop="collections">
          <el-select v-model="collectionValues" multiple filterable placeholder="请选择关联藏品" style="width: 100%" @change="handleCollectionChange">
            <el-option v-for="collection in collectionOptions" :key="collection.collectionId" :label="collection.collectionName" :value="collection.collectionId" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="showCopyMediaCheckbox" label=" ">
          <el-checkbox v-model="copyCollectionMedia">
            是否复制藏品媒体至展览单元
          </el-checkbox>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
    
    <!-- 媒体管理对话框 -->
    <MediaUpload 
      :objectType="'exhibition_unit'" 
      :objectId="currentUnitId" 
      :visible.sync="mediaDialogVisible" 
    />
  </div>
</template>

<script>
import { listExhibitionUnit, getExhibitionUnit, delExhibitionUnit, addExhibitionUnit, updateExhibitionUnit, moveUpExhibitionUnit, moveDownExhibitionUnit } from "@/api/exb_museum/exhibition_unit";
import { listMuseumHall } from "@/api/exb_museum/museum_hall";
import { listCollection } from "@/api/exb_museum/collection";
import { getExhibition } from "@/api/exb_museum/exhibition"; // 新增导入
import MediaUpload from "@/components/MediaUpload";
import { listMuseumMedia } from "@/api/exb_museum/museum_media";

export default {
  name: "ExhibitionUnit",
  components: {
    MediaUpload
  },
  props: {
    exhibitionId: {
      type: Number,
      required: true
    },
    museumId: {
      type: Number,
      required: true
    },
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
      // 展览单元信息表表格数据
      exhibitionUnitList: [],
      // 按章节分组的数据
      groupedExhibitionUnits: {},
      // 有序的章节列表
      orderedSections: [],
      // 当前激活的折叠面板
      activeNames: [],
      // 展厅选项列表
      hallOptions: [],
      // 藏品选项列表
      collectionOptions: [],
      // 藏品选中值（用于多选控件）
      collectionValues: [],
      // 是否复制藏品媒体至展览单元
      copyCollectionMedia: false,
      // 是否显示复制媒体复选框
      showCopyMediaCheckbox: false,
      // 章节选项列表
      sectionOptions: [], // 新增章节选项
      // MinIO 基础URL
      minioBase: process.env.VUE_APP_MINIO_BASE_URL,
      // 表格列信息
      columns: [
        { key: 0, label: '单元名称', visible: true },
        { key: 1, label: '单元类型', visible: true },
        { key: 2, label: '展厅', visible: true },
        { key: 3, label: '所属展览章节', visible: true },
        { key: 4, label: '顺序', visible: true },
      ],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 媒体管理对话框是否显示
      mediaDialogVisible: false,
      // 当前选中的展览单元ID
      currentUnitId: 0,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 1000,
        section: null,
        unitName: null,
        exhibitionId: null,
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        unitName: [
          { required: true, message: "单元名称不能为空", trigger: "blur" }
        ],
        unitType: [
          { required: true, message: "单元类型不能为空", trigger: "change" }
        ],
        hallId: [
          { required: true, message: "展厅不能为空", trigger: "change" }
        ],
        section: [
          { required: true, message: "所属展览章节不能为空", trigger: "change" }
        ],
        sortOrder: [
          { required: true, message: "顺序不能为空", trigger: "blur" }
        ],
        exhibitionId: [
          { required: true, message: "所属展览不能为空", trigger: "blur" }
        ],
      },
      // 单元类型选项
      unitTypeOptions: [
        { value: 0, label: '展品单元' },
        { value: 1, label: '文字单元' },
        { value: 2, label: '多媒体单元' },
      ],
    };
  },
  watch: {
    exhibitionId: {
      handler(newVal) {
        if (newVal) {
          this.queryParams.exhibitionId = newVal;
          this.getList();
          this.loadExhibitionSections(); // 加载展览章节数据
        }
      },
      immediate: true
    }
  },
  created() {
    this.getHallList();
    this.getCollectionList();
  },
  methods: {
    /** 查询展览单元信息表列表 */
    getList() {
      this.loading = true;
      listExhibitionUnit(this.queryParams).then(response => {
        this.exhibitionUnitList = response.rows;
        this.total = response.total;

      // 为每个展览单元获取媒体信息
      this.exhibitionUnitList.forEach(unit => {
        this.getUnitMedia(unit);
      });

        this.groupExhibitionUnitsBySection(); // 按章节分组数据
        this.loading = false;
      });
    },
    // 获取展览单元的媒体信息
    getUnitMedia(unit) {
      // 初始化媒体列表
      if (!unit.mediaList) {
        unit.mediaList = [];
      }
      
      // 构造查询参数
      const params = {
        objectId: unit.unitId,
        objectType: 'exhibition_unit', // 展览单元的对象类型
        mediaType: 1 // 图片类型
      };
      
      // 调用API获取媒体信息
      listMuseumMedia(params).then(response => {
        unit.mediaList = response.rows || [];
      });
    },
    /** 按展览章节分组数据 */
    groupExhibitionUnitsBySection() {
      // 清空现有分组
      this.groupedExhibitionUnits = {};
      
      // 按section字段对展览单元进行分组
      this.exhibitionUnitList.forEach(unit => {
        const section = unit.section || '未分类';
        if (!this.groupedExhibitionUnits[section]) {
          this.groupedExhibitionUnits[section] = [];
        }
        this.groupedExhibitionUnits[section].push(unit);
      });
      
      // 按照展览的sections数组顺序重新排序章节
      this.updateOrderedSections();
    },
    /** 获取指定章节的展览单元 */
    getUnitsBySection(sectionName) {
      return this.groupedExhibitionUnits[sectionName] || [];
    },
    /** 更新有序章节列表 */
    updateOrderedSections() {
      // 创建一个映射，将section内容映射到其在原数组中的索引
      const sectionIndexMap = {};
      this.sectionOptions.forEach((section, index) => {
        sectionIndexMap[section.content] = index;
      });
      
      // 按照原数组顺序排序章节
      this.orderedSections = this.sectionOptions.filter(section => 
        this.groupedExhibitionUnits[section.content] && 
        this.groupedExhibitionUnits[section.content].length > 0
      );
      
      // 添加未在原数组中定义但存在于数据中的章节（如"未分类"）
      Object.keys(this.groupedExhibitionUnits).forEach(sectionName => {
        if (!sectionIndexMap.hasOwnProperty(sectionName)) {
          // 检查是否已经在orderedSections中
          const exists = this.orderedSections.some(sec => sec.content === sectionName);
          if (!exists) {
            this.orderedSections.push({ content: sectionName });
          }
        }
      });
      
      // 设置默认展开第一个分组
      // if (this.orderedSections.length > 0) {
      //   this.activeNames = [this.orderedSections[0].content];
      // } else {
      //   this.activeNames = [];
      // }

      // 设置默认展开所有分组（移除accordion属性以允许多个同时展开）
      this.activeNames = this.orderedSections.map(section => section.content);
    },
    /** 加载展览章节数据 */
    loadExhibitionSections() {
      if (this.exhibitionId) {
        getExhibition(this.exhibitionId).then(response => {
          const exhibition = response.data;
          if (exhibition && exhibition.sections) {
            try {
              // 解析章节JSON数据
              const sections = typeof exhibition.sections === 'string' 
                ? JSON.parse(exhibition.sections) 
                : exhibition.sections;
              
              if (Array.isArray(sections)) {
                this.sectionOptions = sections;
              } else {
                this.sectionOptions = [];
              }
            } catch (error) {
              console.error('解析展览章节数据失败:', error);
              this.sectionOptions = [];
            }
          } else {
            this.sectionOptions = [];
          }
        }).catch(error => {
          console.error('获取展览章节数据失败:', error);
          this.sectionOptions = [];
        });
      }
    },
    /** 查询展厅列表 */
    getHallList() {
      listMuseumHall({ museumId: this.museumId }).then(response => {
        this.hallOptions = response.rows;
      });
    },
    /** 查询藏品列表 */
    getCollectionList() {
      listCollection({ museumId: this.museumId }).then(response => {
        this.collectionOptions = response.rows;
      });
    },
    // 为表格行添加样式
    tableRowClassName({ row, rowIndex }) {
      // 根据需要为特定行添加CSS类
      return '';
    },
    // 单元类型字典翻译
    dict_unitType_format(row, column) {
      const unitType = this.unitTypeOptions.find(item => item.value === row.unitType);
      return unitType ? unitType.label : '';
    },
    // 展厅字典翻译
    dict_hallId_format(row, column) {
      const hall = this.hallOptions.find(item => item.hallId === row.hallId);
      return hall ? hall.hallName : '';
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        unitId: null,
        unitName: null,
        exhibitionId: this.exhibitionId,
        exhibitLabel: null,
        guideText: null,
        unitType: null,
        hallId: null,
        section: null,
        sortOrder: null,
        collections: [],
      };
      this.collectionValues = [];
      this.copyCollectionMedia = false;
      this.showCopyMediaCheckbox = false;
      this.$refs["form"] && this.$refs["form"].resetFields();
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
      this.ids = selection.map(item => item.unitId)
      this.single = selection.length!==1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加展览单元信息表";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const unitId = row.unitId || this.ids
      getExhibitionUnit(unitId).then(response => {
        this.form = response.data;
        // 将关联藏品字符串转换为数组
        if (this.form.collections) {
          try {
            this.collectionValues = JSON.parse(this.form.collections);
          } catch (e) {
            this.collectionValues = [];
          }
        } else {
          this.collectionValues = [];
        }
        this.open = true;
        this.title = "修改展览单元信息表";
        // 在加载表单后，检查是否需要显示复选框
        this.$nextTick(() => {
          this.checkShowCopyMediaCheckbox();
        });
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          // 将藏品选中值转换为JSON字符串
          const submitData = { ...this.form };
          if (this.collectionValues && this.collectionValues.length > 0) {
            submitData.collections = JSON.stringify(this.collectionValues);
          } else {
            submitData.collections = null;
          }

           // 添加复制藏品媒体的字段
          submitData.copyCollectionMedia = this.copyCollectionMedia;
          
          if (submitData.unitId != null) {
            updateExhibitionUnit(submitData).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addExhibitionUnit(submitData).then(response => {
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
      const unitIds = row.unitId || this.ids;
      this.$modal.confirm('是否确认删除展览单元信息表编号为"' + unitIds + '"的数据项？').then(function() {
        return delExhibitionUnit(unitIds);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('exb_museum/unit/export', {
        ...this.queryParams
      }, `exhibition_unit_${new Date().getTime()}.xlsx`)
    },
    /** 打开媒体管理对话框 */
    openMediaDialog(row) {
      this.currentUnitId = row.unitId;
      this.mediaDialogVisible = true;
    },

    /** 向上移动展览单元 */
    async moveUp(row) {
      try {
        const response = await moveUpExhibitionUnit(row.unitId);
        if (response.code === 200) {
          this.$modal.msgSuccess(response.msg || "向上移动成功");
          this.getList(); // 重新加载列表
        } else {
          this.$modal.msgError(response.msg || "向上移动失败");
        }
      } catch (error) {
        this.$modal.msgError("向上移动失败：" + error.message);
      }
    },
    
    /** 向下移动展览单元 */
    async moveDown(row) {
      try {
        const response = await moveDownExhibitionUnit(row.unitId);
        if (response.code === 200) {
          this.$modal.msgSuccess(response.msg || "向下移动成功");
          this.getList(); // 重新加载列表
        } else {
          this.$modal.msgError(response.msg || "向下移动失败");
        }
      } catch (error) {
        this.$modal.msgError("向下移动失败：" + error.message);
      }
    },
    
    /** 判断是否可以向上移动 */
    canMoveUp(row, index) {
      // 检查是否在同一展览和章节内有其他项可以交换位置
      const sameSectionItems = this.groupedExhibitionUnits[row.section] || [];
      const currentIndex = sameSectionItems.findIndex(item => item.unitId === row.unitId);
      return currentIndex > 0;
    },
    
    /** 判断是否可以向下移动 */
    canMoveDown(row, index) {
      // 检查是否在同一展览和章节内有其他项可以交换位置
      const sameSectionItems = this.groupedExhibitionUnits[row.section] || [];
      const currentIndex = sameSectionItems.findIndex(item => item.unitId === row.unitId);
      return currentIndex < sameSectionItems.length - 1;
    },
    
    /** 处理单元类型变化 */
    handleUnitTypeChange(value) {
      this.checkShowCopyMediaCheckbox();
    },
    
    /** 处理藏品选择变化 */
    handleCollectionChange(value) {
      this.checkShowCopyMediaCheckbox();
    },
    
    /** 检查是否显示复制媒体复选框 */
    checkShowCopyMediaCheckbox() {
      // 当单元类型为展品单元(0)且已选择关联藏品时显示复选框
      this.showCopyMediaCheckbox = this.form.unitType === 0 //&& this.collectionValues && this.collectionValues.length > 0;
      // 如果不再满足条件，取消勾选
      if (!this.showCopyMediaCheckbox) {
        this.collectionValues = [];
        this.copyCollectionMedia = false;
      }
    }
    
  }
};
</script>

<style scoped>
.sort-buttons {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.sort-value {
  min-width: 20px;
  text-align: center;
  font-weight: bold;
}

.media-list {
  display: flex;
  flex-wrap: wrap;
}
</style>