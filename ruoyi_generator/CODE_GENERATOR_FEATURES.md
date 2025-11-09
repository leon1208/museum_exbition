# 代码生成器功能说明

## 已实现的功能

### 1. 核心功能
- ✅ 数据库表导入
- ✅ 代码生成配置
- ✅ 模板引擎生成代码
- ✅ 前后端代码生成
- ✅ ZIP打包下载
- ✅ 代码预览
- ✅ 批量生成代码
- ✅ 数据库表结构同步
- ✅ 表信息查询

### 2. 生成的代码文件
- ✅ Python后端代码
  - Entity实体类 (`domain/{ClassName}.py`)
  - PO查询对象 (`domain/po.py`)
  - Mapper数据访问层 (`mapper/{class_name}_mapper.py`)
  - Service业务逻辑层 (`service/{class_name}_service.py`)
  - Controller控制层 (`controller/{class_name}_controller.py`)
- ✅ Vue前端代码
  - 页面组件 (`vue/{business_name}/index.vue`)
  - API接口 (`api/{module_name}/{business_name}.js`)
- ✅ SQL脚本
  - 菜单权限SQL (`sql/menu.sql`)
- ✅ 文档
  - README说明文档 (`README.md`)

### 3. 模板特性
- ✅ 支持Jinja2模板引擎
- ✅ 动态字段生成
- ✅ 权限控制集成
- ✅ 分页查询支持
- ✅ 表单验证集成
- ✅ 字典数据支持
- ✅ 查询条件动态生成

### 4. 数据库支持
- ✅ MySQL数据库表结构读取
- ✅ 字段类型自动映射
- ✅ 主键自动识别
- ✅ 自增字段识别
- ✅ 字段注释读取
- ✅ 表注释读取

### 5. API接口
- ✅ 表列表查询 (`GET /list`)
- ✅ 数据库表列表 (`GET /db/list`)
- ✅ 表详情查询 (`GET /{tableId}`)
- ✅ 表导入 (`POST /importTable`)
- ✅ 表信息更新 (`PUT /{tableId}`)
- ✅ 表删除 (`DELETE /{tableIds}`)
- ✅ 代码预览 (`GET /preview/{tableId}`)
- ✅ 代码下载 (`GET /download/{table_name}`)
- ✅ 代码生成 (`GET /genCode/{table_name}`)
- ✅ 批量生成 (`GET /batchGenCode`)
- ✅ 数据库同步 (`GET /synchDb/{table_name}`)
- ✅ 字段列表查询 (`GET /column/list`)
- ✅ 数据导出 (`GET /export`)
- ✅ 表信息查询 (`GET /tableInfo/{table_name}`)

### 6. 配置功能
- ✅ 作者配置
- ✅ 包名配置
- ✅ 表前缀配置
- ✅ 自动移除表前缀
- ✅ 模板分类支持

### 7. 代码规范
- ✅ Python代码规范
- ✅ 类型注解支持
- ✅ 文档字符串
- ✅ 异常处理
- ✅ 日志记录
- ✅ 权限验证

## 使用说明

### 1. 导入数据库表
```python
# 通过API导入表
POST /tool/gen/importTable?tables=sys_user,sys_role
```

### 2. 配置生成参数
- 设置包名、模块名、业务名
- 配置字段属性（是否查询、编辑、列表显示等）
- 设置HTML控件类型

### 3. 生成代码
```python
# 预览代码
GET /tool/gen/preview/{tableId}

# 下载代码
GET /tool/gen/download/{table_name}

# 批量生成
GET /tool/gen/batchGenCode?tables=sys_user,sys_role
```

### 4. 同步数据库
```python
# 同步表结构
GET /tool/gen/synchDb/{table_name}
```

## 模板文件结构
```
ruoyi_generator/vm/
├── py/                    # Python后端模板
│   ├── entity.py.vm      # 实体类模板
│   ├── po.py.vm          # 查询对象模板
│   ├── mapper.py.vm      # 数据访问层模板
│   ├── service.py.vm     # 业务逻辑层模板
│   └── controller.py.vm  # 控制层模板
├── vue/                   # Vue前端模板
│   └── index.vue.vm      # 页面模板
├── js/                    # JavaScript模板
│   └── api.js.vm         # API接口模板
├── sql/                   # SQL模板
│   └── menu.sql.vm       # 菜单权限模板
└── README.md.vm          # 说明文档模板
```

## 权限配置
- `tool:gen:list` - 查询权限
- `tool:gen:query` - 详情查询权限
- `tool:gen:add` - 新增权限
- `tool:gen:edit` - 编辑权限
- `tool:gen:remove` - 删除权限
- `tool:gen:code` - 代码生成权限
- `tool:gen:preview` - 代码预览权限
- `tool:gen:export` - 导出权限

## 技术栈
- **后端**: Flask + SQLAlchemy + Jinja2
- **前端**: Vue.js + Element UI
- **数据库**: MySQL
- **模板引擎**: Jinja2
- **权限控制**: 基于注解的权限控制

## 扩展性
- 支持自定义模板
- 支持多种数据库
- 支持多种前端框架
- 支持自定义字段类型映射
- 支持自定义生成规则

