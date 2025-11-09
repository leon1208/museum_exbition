import os
from typing import List
from jinja2 import Template
from ruoyi_common.utils import StringUtil
from ruoyi_generator.domain.entity import GenTable
from ruoyi_generator.config import GeneratorConfig
import zipfile
from io import BytesIO
from datetime import datetime
import re


def to_underscore(name: str) -> str:
    """
    将驼峰命名转换为下划线命名
    
    Args:
        name (str): 驼峰命名的字符串
        
    Returns:
        str: 下划线命名的字符串
    """
    # 在大写字母前添加下划线，然后转为小写
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class GenUtils:
    @staticmethod
    def get_file_name(template_file: str, table: GenTable) -> str:
        """
        根据模板文件名和表信息生成文件名
        
        Args:
            template_file (str): 模板文件名
            table (GenTable): 表信息
            
        Returns:
            str: 生成的文件名
        """
        # 标准化路径分隔符
        template_file = template_file.replace('\\', '/')
        
        # 移除.vm后缀
        base_name = template_file[:-3] if template_file.endswith('.vm') else template_file
        
        # 根据模板类型生成文件名和路径
        if 'py/entity.py' in template_file:
            # 根据包名生成目录结构
            package_path = table.package_name.replace('.', '/') if table.package_name else ''
            return f"{package_path}/domain/{table.class_name}.py"
        elif 'py/controller.py' in template_file:
            package_path = table.package_name.replace('.', '/') if table.package_name else ''
            # 使用下划线命名法
            controller_name = f"{to_underscore(table.class_name)}_controller"
            return f"{package_path}/controller/{controller_name}.py"
        elif 'py/service.py' in template_file:
            package_path = table.package_name.replace('.', '/') if table.package_name else ''
            # 使用下划线命名法
            service_name = f"{to_underscore(table.class_name)}_service"
            return f"{package_path}/service/{service_name}.py"
        elif 'py/mapper.py' in template_file:
            package_path = table.package_name.replace('.', '/') if table.package_name else ''
            # 使用下划线命名法
            mapper_name = f"{to_underscore(table.class_name)}_mapper"
            return f"{package_path}/mapper/{mapper_name}.py"
        elif 'py/po.py' in template_file:
            package_path = table.package_name.replace('.', '/') if table.package_name else ''
            # PO文件使用表名作为文件名
            po_name = f"{table.class_name}PO"
            return f"{package_path}/domain/{po_name}.py"
        elif 'vue/index.vue' in template_file:
            # 无论是树表还是普通表，Vue文件名都是index.vue
            return f"vue/{table.business_name}/index.vue"
        elif 'js/api.js' in template_file:
            return f"js/api/{table.business_name}.js"
        elif 'sql/menu.sql' in template_file:
            return f"sql/{table.business_name}_menu.sql"
        elif 'README.md' in template_file:
            return f"{table.business_name}_README.md"
        else:
            # 处理其他模板文件，保持原有目录结构
            filename = os.path.basename(base_name)
            if '.' not in filename:
                filename += '.py'  # 默认添加.py扩展名
            return filename

    @staticmethod
    def get_table_prefix() -> str:
        """
        获取表前缀
        
        Returns:
            str: 表前缀
        """
        return GeneratorConfig.table_prefix or ""

    @staticmethod
    def remove_table_prefix(table_name: str) -> str:
        """
        移除表前缀
        
        Args:
            table_name (str): 表名
            
        Returns:
            str: 移除前缀后的表名
        """
        prefix = GenUtils.get_table_prefix()
        if prefix and table_name.startswith(prefix):
            return table_name[len(prefix):]
        return table_name

    @staticmethod
    def table_to_class_name(table_name: str) -> str:
        """
        将表名转换为类名
        
        Args:
            table_name (str): 表名
            
        Returns:
            str: 类名
        """
        # 移除表前缀
        clean_table_name = GenUtils.remove_table_prefix(table_name)
        # 转换为驼峰命名
        return GenUtils.to_camel_case(clean_table_name)

    @staticmethod
    def get_business_name(table_name: str) -> str:
        """
        获取业务名
        
        Args:
            table_name (str): 表名
            
        Returns:
            str: 业务名
        """
        # 移除表前缀
        clean_table_name = GenUtils.remove_table_prefix(table_name)
        # 获取下划线分隔的第一部分
        return GenUtils.substring_before(clean_table_name, "_") if "_" in clean_table_name else clean_table_name

    @staticmethod
    def get_import_path(package_name: str, module_type: str, class_name: str = None) -> str:
        """
        生成导入路径
        
        Args:
            package_name (str): 包名，如 "com.yy.project" 或 "ruoyi_generator"
            module_type (str): 模块类型，如 "domain", "service", "mapper", "controller"
            class_name (str): 类名（可选，用于PO导入）
            
        Returns:
            str: 导入路径，Python包名保持点分隔格式
        """
        if not package_name:
            return f"ruoyi_generator.{module_type}"
        
        # Python导入路径使用点分隔，保持原样
        # 例如: "com.yy.project" -> "com.yy.project"
        # 例如: "ruoyi_generator" -> "ruoyi_generator" (保持不变)
        python_package = package_name
        
        # 生成导入路径
        if module_type == "domain" and class_name:
            return f"{python_package}.domain.po"
        elif module_type == "domain":
            return f"{python_package}.domain.entity"
        else:
            return f"{python_package}.{module_type}"

    @staticmethod
    def to_camel_case(name: str) -> str:
        """
        将下划线命名转换为驼峰命名
        
        Args:
            name (str): 下划线命名
            
        Returns:
            str: 驼峰命名
        """
        if hasattr(StringUtil, 'to_camel_case'):
            return StringUtil.to_camel_case(name)
        # 如果StringUtil没有to_camel_case方法，则手动实现
        parts = name.split('_')
        if len(parts) == 1:
            return parts[0]
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    @staticmethod
    def substring_before(string: str, separator: str) -> str:
        """
        获取字符串中分隔符之前的部分
        
        Args:
            string (str): 输入字符串
            separator (str): 分隔符
            
        Returns:
            str: 分隔符之前的部分
        """
        if hasattr(StringUtil, 'substring_before'):
            return StringUtil.substring_before(string, separator)
        # 如果StringUtil没有substring_before方法，则手动实现
        if separator in string:
            return string.split(separator, 1)[0]
        return string

    @staticmethod
    def substring_after(string: str, separator: str) -> str:
        """
        获取字符串中分隔符之后的部分
        
        Args:
            string (str): 输入字符串
            separator (str): 分隔符
            
        Returns:
            str: 分隔符之后的部分
        """
        if hasattr(StringUtil, 'substring_after'):
            return StringUtil.substring_after(string, separator)
        # 如果StringUtil没有substring_after方法，则手动实现
        if separator in string:
            return string.split(separator, 1)[1]
        return ""
        
    @staticmethod
    def generator_code(table: GenTable) -> BytesIO:
        """
        生成代码
        
        Args:
            table (GenTable): 表信息
            
        Returns:
            BytesIO: 生成的代码文件
        """
        # 设置列的 list_index 属性
        GenUtils.set_column_list_index(table)
        
        # 设置主键列
        pk_columns = [column for column in table.columns if column.is_pk == '1']
        if pk_columns:
            table.pk_column = pk_columns[0]
        else:
            table.pk_column = None
        
        # 获取模板目录
        template_dir = os.path.join(os.path.dirname(__file__), 'vm')
        
        # 定义核心模板文件
        core_templates = [
            'py/entity.py.vm',
            'py/po.py.vm', 
            'py/controller.py.vm',
            'py/service.py.vm',
            'py/mapper.py.vm',
            'js/api.js.vm',
            'sql/menu.sql.vm'
        ]
        
        # 根据表类型添加相应的Vue模板
        if table.tpl_category == 'tree':
            core_templates.append('vue/index-tree.vue.vm')
        else:
            core_templates.append('vue/index.vue.vm')
        
        # 创建内存中的ZIP文件
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # 处理每个核心模板文件
            for relative_path in core_templates:
                template_path = os.path.join(template_dir, relative_path)
                if os.path.exists(template_path):
                    # 读取模板内容
                    try:
                        with open(template_path, 'r', encoding='utf-8') as f:
                            template_content = f.read()
                            
                        # 准备模板上下文
                        context = {
                            'table': table,
                            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'underscore': to_underscore,  # 添加自定义过滤器
                            'get_import_path': GenUtils.get_import_path  # 添加导入路径生成函数
                        }
                        
                        # 使用Jinja2渲染模板
                        template = Template(template_content)
                        rendered_content = template.render(**context)
                        
                        # 生成文件名
                        output_file_name = GenUtils.get_file_name(relative_path, table)
                        
                        # 检查渲染后的内容是否为空
                        if rendered_content.strip():
                            # 将渲染后的内容写入ZIP文件
                            zip_file.writestr(output_file_name, rendered_content)
                        else:
                            print(f"警告: 模板 {relative_path} 渲染后内容为空")
                    except Exception as e:
                        print(f"处理模板 {relative_path} 时出错: {e}")
        
        zip_buffer.seek(0)
        return zip_buffer
        
    @staticmethod
    def batch_generator_code(tables: List[GenTable]) -> BytesIO:
        """
        批量生成代码
        
        Args:
            tables (List[GenTable]): 表列表
            
        Returns:
            BytesIO: 生成的代码文件
        """
        # 为每个表设置列的 list_index 属性和主键列
        for table in tables:
            GenUtils.set_column_list_index(table)
            # 设置主键列
            pk_columns = [column for column in table.columns if column.is_pk == '1']
            if pk_columns:
                table.pk_column = pk_columns[0]
            else:
                table.pk_column = None
        
        # 定义核心模板文件
        core_templates = [
            'py/entity.py.vm',
            'py/po.py.vm', 
            'py/controller.py.vm',
            'py/service.py.vm',
            'py/mapper.py.vm',
            'js/api.js.vm',
            'sql/menu.sql.vm'
        ]
        
        # 创建内存中的ZIP文件
        zip_buffer = BytesIO()
        
        # 获取模板目录
        template_dir = os.path.join(os.path.dirname(__file__), 'vm')
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # 跟踪已添加的文件名以避免重复
            added_files = set()
            
            # 处理每个表
            for table in tables:
                # 根据表类型添加相应的Vue模板
                if table.tpl_category == 'tree':
                    current_templates = core_templates + ['vue/index-tree.vue.vm']
                else:
                    current_templates = core_templates + ['vue/index.vue.vm']
                
                # 处理每个核心模板文件
                for relative_path in current_templates:
                    template_path = os.path.join(template_dir, relative_path)
                    if os.path.exists(template_path):
                        # 读取模板内容
                        try:
                            with open(template_path, 'r', encoding='utf-8') as f:
                                template_content = f.read()
                                
                            # 准备模板上下文
                            context = {
                                'table': table,
                                'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'underscore': to_underscore,  # 添加自定义过滤器
                                'get_import_path': GenUtils.get_import_path  # 添加导入路径生成函数
                            }
                            
                            # 使用Jinja2渲染模板
                            template = Template(template_content)
                            rendered_content = template.render(**context)
                            
                            # 生成文件名
                            output_file_name = GenUtils.get_file_name(relative_path, table)
                            
                            # 检查是否已添加同名文件
                            if output_file_name in added_files:
                                # 为重复文件添加序号
                                name, ext = os.path.splitext(output_file_name)
                                counter = 1
                                new_name = f"{name}_{counter}{ext}"
                                while new_name in added_files:
                                    counter += 1
                                    new_name = f"{name}_{counter}{ext}"
                                output_file_name = new_name
                            
                            # 检查渲染后的内容是否为空
                            if rendered_content.strip():
                                # 将渲染后的内容写入ZIP文件
                                zip_file.writestr(output_file_name, rendered_content)
                                added_files.add(output_file_name)
                            else:
                                print(f"警告: 模板 {relative_path} 渲染后内容为空")
                        except Exception as e:
                            print(f"处理表 {table.table_name} 的模板 {relative_path} 时出错: {e}")
        
        zip_buffer.seek(0)
        return zip_buffer
        
    @staticmethod
    def set_column_list_index(table: GenTable):
        """
        为表的列设置 list_index 属性，用于 Vue 模板中的 columns 数组索引
        
        Args:
            table (GenTable): 表信息
        """
        if not table.columns:
            return
        
        list_index = 0
        for column in table.columns:
            if column.is_list == '1':
                # 使用 setattr 动态添加属性
                setattr(column, 'list_index', list_index)
                list_index += 1

    @staticmethod
    def preview_code(table: GenTable) -> dict:
        """
        预览代码
        
        Args:
            table (GenTable): 表信息
            
        Returns:
            dict: 预览代码
        """
        # 设置列的 list_index 属性
        GenUtils.set_column_list_index(table)
        
        # 设置主键列
        pk_columns = [column for column in table.columns if column.is_pk == '1']
        if pk_columns:
            table.pk_column = pk_columns[0]
        else:
            table.pk_column = None
        
        # 获取模板目录
        template_dir = os.path.join(os.path.dirname(__file__), 'vm')
        
        # 存储预览代码的字典
        preview_data = {}
        
        # 定义需要预览的核心模板文件
        core_templates = [
            'py/entity.py.vm',
            'py/po.py.vm', 
            'py/controller.py.vm',
            'py/service.py.vm',
            'py/mapper.py.vm',
            'js/api.js.vm',
            'sql/menu.sql.vm'
        ]
        
        # 根据表类型添加相应的Vue模板，但预览时都使用index.vue.vm作为文件名
        if table.tpl_category == 'tree':
            core_templates.append('vue/index-tree.vue.vm')
        else:
            core_templates.append('vue/index.vue.vm')
        
        # 处理每个核心模板文件
        for relative_path in core_templates:
            template_path = os.path.join(template_dir, relative_path)
            if os.path.exists(template_path):
                # 读取模板内容
                try:
                    with open(template_path, 'r', encoding='utf-8') as f:
                        template_content = f.read()
                        
                    # 准备模板上下文
                    context = {
                        'table': table,
                        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'underscore': to_underscore,  # 添加自定义过滤器
                        'get_import_path': GenUtils.get_import_path  # 添加导入路径生成函数
                    }
                    
                    # 使用Jinja2渲染模板
                    template = Template(template_content)
                    rendered_content = template.render(**context)
                    
                    # 存储渲染后的内容
                    preview_data[relative_path] = rendered_content
                except Exception as e:
                    # 如果渲染失败，存储错误信息
                    preview_data[relative_path] = f"模板渲染失败: {str(e)}"
            else:
                preview_data[relative_path] = "模板文件不存在"
        
        return preview_data
