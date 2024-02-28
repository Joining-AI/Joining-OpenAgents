import os
import json
import shutil
import PyPDF2
import markdown
import ast
import re
import textwrap

class FileProcessor:
    def __init__(self, base_path: str = None) -> None:
        """初始化文件处理器"""
        if base_path is None:
            self.base_path = os.path.dirname(__file__)
        else:
            self.base_path = base_path

    def get_full_path(self, relative_path: str) -> str:
        """获取文件的完整路径"""
        return os.path.join(self.base_path, relative_path)

    def create_and_write_json(self, folder_path: str, filename: str, data: dict) -> None:
        """在指定文件夹中创建 JSON 文件并写入数据"""
        full_folder_path = self.get_full_path(folder_path)
        full_file_path = os.path.join(full_folder_path, f"{filename}.json")

        # 如果文件夹路径不存在，则创建文件夹
        if not os.path.exists(full_folder_path):
            os.makedirs(full_folder_path)

        with open(full_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"JSON 文件 '{filename}.json' 在文件夹 '{folder_path}' 中创建并写入成功.")

    def read_file(self, file_path: str) -> str:
        """根据文件类型选择适当的读取方法"""
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() in ['.txt', '.md']:
            return self.read_text_file(file_path)
        elif file_extension.lower() == '.json':
            return self.read_json_file(file_path)
        elif file_extension.lower() == '.pdf':
            return self.read_pdf_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def read_text_file(self, file_path: str) -> str:
        """读取文本文件"""
        with open(self.get_full_path(file_path), 'r', encoding='utf-8') as file:
            return file.read()

    def read_json_file(self, file_path: str) -> dict:
        """读取JSON文件"""
        with open(self.get_full_path(file_path), 'r', encoding='utf-8') as file:
            return json.load(file)

    def read_pdf_file(self, file_path: str) -> str:
        """读取PDF文件，需要使用外部库"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except FileNotFoundError:
            return "文件未找到，请检查文件路径。"
        except PyPDF2.utils.PdfReadError:
            return "无法读取PDF文件，请确保文件格式正确。"

    def write_file(self, file_path: str, content: str) -> None:
        """写入文件，根据文件类型选择适当的写入方法"""
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() == '.json':
            self.write_json_file(file_path, content)
        elif file_extension.lower() == '.md':
            self.write_text_file(file_path, content)
        elif file_extension.lower() == '.pdf':
            self.write_pdf_file(file_path, content)
        else:
            self.write_text_file(file_path, content)

    def write_text_file(self, file_path: str, content: str) -> None:
        """写入文本文件"""
        with open(self.get_full_path(file_path), 'w', encoding='utf-8') as file:
            file.write(content)

    def write_json_file(self, file_path: str, content: dict) -> None:
        """写入JSON文件"""
        with open(self.get_full_path(file_path), 'w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)

    def write_pdf_file(self, file_path: str, content: str) -> None:
        """写入PDF文件"""
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.addPage(PyPDF2.PageObject.createTextPage(content))
        with open(self.get_full_path(file_path), 'wb') as file:
            pdf_writer.write(file)

    def delete_file(self, file_path: str) -> None:
        """删除文件"""
        os.remove(self.get_full_path(file_path))

    def move_file(self, source_path: str, destination_path: str) -> None:
        """移动文件"""
        shutil.move(self.get_full_path(source_path), self.get_full_path(destination_path))
        
    def parse_md_to_html(self, file_path):
        """将Markdown文件解析为HTML"""
        md_content = self.read_text_file(file_path)
        html_content = markdown.markdown(md_content)
        return html_content
    
import ast
import re
import textwrap

class CodeAnalyser:
    def __init__(self):
        pass       
    #解析方法
    def get_functions_and_classes(self, code_content: str) ->  tuple:
        """
        提取所有函数、类及其参数（如果有）以及它们之间的层次关系。

        输出示例：[('FunctionDef', 'AI_give_params', 86, 95, None, ['param1', 'param2']), ('ClassDef', 'PipelineEngine', 97, 104, None, []), ('FunctionDef', 'get_all_pys', 99, 104, 'PipelineEngine', ['param1'])]
        在示例中，PipelineEngine 是 get_all_pys 的父结构。

        参数：
            code_content：要解析的整个文件的代码内容。

        返回：
            包含节点类型（FunctionDef、ClassDef、AsyncFunctionDef）、节点名称、起始行号、结束行号、父节点名称和参数列表（如果有）的元组列表。
        """

        tree = ast.parse(code_content)
        self.add_parent_references(tree)
        functions_and_classes = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                start_line = node.lineno
                end_line = self.get_end_lineno(node)

                def get_recursive_parent_name(node):
                    now = node
                    while "parent" in dir(now):
                        if isinstance(
                            now.parent,
                            (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef),
                        ):
                            assert "name" in dir(now.parent)
                            return now.parent.name
                        now = now.parent
                    return None

                parent_name = get_recursive_parent_name(node)
                parameters = (
                    [arg.arg for arg in node.args.args] if "args" in dir(node) else []
                )
                all_names = [item[1] for item in functions_and_classes]
                if node.name not in all_names:
                    functions_and_classes.append(
                        (
                            type(node).__name__,
                            node.name,
                            start_line,
                            end_line,
                            parent_name,
                            parameters,
                        )
                    )
                else:
                    print(
                        f"检测到循环定义，已跳过：{type(node).__name__}: {node.name}"
                    )
        return functions_and_classes
    
    def get_end_lineno(self, node) -> int:
        """
        获取给定节点的结束行号。

        Args:
            node: 要查找结束行号的节点。

        Returns:
            int: 节点的结束行号。如果节点没有行号，则返回-1。
        """
        if not hasattr(node, "lineno"):
            return -1  # 返回-1表示此节点没有行号

        end_lineno = node.lineno
        for child in ast.iter_child_nodes(node):
            child_end = getattr(child, "end_lineno", None) or self.get_end_lineno(child)
            if child_end > -1:  # 只更新当子节点有有效行号时
                end_lineno = max(end_lineno, child_end)
        return end_lineno

    def add_parent_references(self, node, parent=None) -> None:
        """
        向AST中的每个节点添加父节点引用。

        Args:
            node: AST中的当前节点。

        Returns:
            None
        """
        for child in ast.iter_child_nodes(node):
            child.parent = node
            self.add_parent_references(child, node)

    def extract_code_segment(self, code_content: str, start_line: int, end_line: int) -> str:
            """
            从给定的代码内容中提取指定起始行和结束行之间的代码段，并将其作为字符串返回。

            参数:
            - code_content (str): 包含源代码的字符串，将从中提取代码段。
            - start_line (int): 代码段的起始行号。
            - end_line (int): 代码段的结束行号。

            返回:
            - code_segment (str): 提取的代码段，包括起始行和结束行，以换行符分隔。
            """
            code_segment = '\n'.join(code_content.splitlines()[start_line - 1:end_line])
            return code_segment
        
    def extract_dependencies(self, code_content: str) -> list:
        # 正则表达式匹配 import 和 from ... import 语句
        pattern = re.compile(r'^\s*(?:import|from)\s+([^\s.]+)', re.MULTILINE)
        
        # 查找所有匹配项
        matches = pattern.findall(code_content)
        
        # 去除重复的库名
        unique_dependencies = list(set(matches))
        
        return unique_dependencies
    
    def reorganize_tree(self, tuples):
        """
        任何没有父节点的元素都被认为是根节点。
        如果元素有父节点，那么它的父节点应该已经在之前的遍历中被处理过了。
        
        返回一个字典，表示组织树图，其中包含节点名称和行信息以及连接关系。
        """
        tree = {}  # 初始化空树
        name_to_line_mapping = {}  # 用于快速查找节点名称对应的行号

        # 首先，创建一个映射，用于存储每个节点名称对应的行号
        for item in tuples:
            _, name, line, _, _, _ = item
            # 由于可能存在同名函数或方法，这里选择最后出现的行号
            name_to_line_mapping[name] = line

        # 遍历元组，构建树
        for item in tuples:
            item_type, name, line, _, parent_name, _ = item
            
            # 生成当前节点的标识
            node_id = (name, line)
            # 如果存在父节点名称，尝试从映射中获取父节点的行号
            if parent_name and parent_name in name_to_line_mapping:
                parent_line = name_to_line_mapping[parent_name]
                parent_id = (parent_name, parent_line)
            else:
                parent_id = None

            # 处理无父节点的情况，即根节点
            if parent_id is None:
                if node_id not in tree:
                    tree[node_id] = []
            else:
                # 有父节点的情况，将当前节点作为父节点的直接子节点添加
                if parent_id in tree:
                    if node_id not in tree[parent_id]:  # 确保不重复添加子节点
                        tree[parent_id].append(node_id)
                else:
                    # 如果父节点不存在，这里应该不会发生，因为假设程序完整
                    tree[parent_id] = [node_id]

        return tree

    def calculate_function_locations(self, tuples, tree):
        # 构建初始的函数或方法定义映射并构建树状结构
        definitions = {}
        for t in tuples:
            key = (t[1], t[2])  # 使用(name, line)作为键
            definitions[key] = {
                'name': t[1],
                'location': set(range(t[2], t[3] + 1)),
                'children': []
            }

        # 更新定义中的子节点信息，根据新的tree结构
        for parent_key, children_keys in tree.items():
            if parent_key in definitions:
                definitions[parent_key]['children'] = children_keys

        # 递归函数计算每个节点的位置
        def subtract_locations(node, child_keys):
            child_locations = set()
            for child_key in child_keys:
                if child_key in definitions:
                    child = definitions[child_key]
                    child_locations = child_locations.union(child['location'])
                    if child['children']:
                        subtract_locations(child, child['children'])
            node['location'] -= child_locations

        # 对根节点执行位置计算
        for key, node in definitions.items():
            if node['children']:  # 如果有子节点，则计算位置
                subtract_locations(node, node['children'])

        # 转换结果格式，仅包含名称和位置信息
        result = [
            {
                'name': info['name'],
                'location': sorted(list(info['location'])),  # 将位置集合转换为排序列表
            } for key, info in definitions.items()
        ]

        # 计算整个程序的行索引集合
        program_lines = set()
        for info in definitions.values():
            program_lines = program_lines.union(info['location'])

        return result
    
    def extract_variables_from_code(self, func_code, name) -> list:
        '''
        {'name': ..., 
        'type': ..., 
        'program': ...}
        '''
        adjusted_code = textwrap.dedent(func_code)
        # 解析函数代码
        tree = ast.parse(adjusted_code)

        # 用于存储变量的列表
        variables = []
        
        # 辅助函数，用于遍历AST节点
        def visit_node(node):
            if isinstance(node, ast.Name):
                # 检查变量是否已存在
                variable_name = node.id
                if not any(var['name'] == variable_name for var in variables):
                    # 添加变量名称、类型和程序名称到列表中
                    variable_info = {'name': variable_name, 'type': None, 'program': name}
                    variables.append(variable_info)
            elif isinstance(node, ast.FunctionDef):
                # 递归遍历函数定义中的节点
                for n in node.body:
                    visit_node(n)
            elif isinstance(node, ast.Return):
                # 处理返回语句
                if isinstance(node.value, ast.Name):
                    # 返回值是变量
                    variable_name = node.value.id
                    if not any(var['name'] == variable_name for var in variables):
                        variable_info = {'name': variable_name, 'type': None, 'program': name}
                        variables.append(variable_info)
                elif isinstance(node.value, ast.Tuple):
                    # 返回值是元组，处理每个元素
                    for element in node.value.elts:
                        if isinstance(element, ast.Name):
                            variable_name = element.id
                            if not any(var['name'] == variable_name for var in variables):
                                variable_info = {'name': variable_name, 'type': None, 'program': name}
                                variables.append(variable_info)
            elif isinstance(node, ast.Assign):
                # 处理赋值语句
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        # 被赋值的是变量
                        variable_name = target.id
                        if not any(var['name'] == variable_name for var in variables):
                            variable_info = {'name': variable_name, 'type': None, 'program': name}
                            variables.append(variable_info)
            elif isinstance(node, ast.arg):
                # 处理函数参数
                variable_name = node.arg
                if not any(var['name'] == variable_name for var in variables):
                    variable_info = {'name': variable_name, 'type': None, 'program': name}
                    variables.append(variable_info)
            
        # 遍历AST树
        for node in ast.walk(tree):
            visit_node(node)
        
        return variables

    def extract_variables_from_source_code(self, source_code, function_locations):
        '''
        输入完整的源代码和一个包含函数对应行数的数据结构。
        输出是各个变量对应的名称，格式类型和所属程序标签的字典列表，其中程序标签为元组形式。
        '''
        # 用于存储所有变量的列表
        all_variables = []

        # 分割源代码为行
        source_lines = source_code.split('\n')

        # 遍历每个函数的位置信息
        for function_info in function_locations:
            name = function_info['name']
            start_line = function_info['location'][0]  # 起始行号
            end_line = function_info['location'][-1]

            # 提取函数的代码片段
            func_code = '\n'.join(source_lines[start_line - 1:end_line])

            # 调用现有方法分析这段代码，传递包含方法名称和起始行的元组作为程序标签
            program_label = (name, start_line)
            variables = self.extract_variables_from_code(func_code, program_label)

            # 添加到总列表中
            all_variables.extend(variables)

        return all_variables

    def variable_trace(self, source_code):
        tuples=self.get_functions_and_classes(source_code)
        tree=self.reorganize_tree(tuples)
        function_locations = self.calculate_function_locations(tuples, tree)
        variables = self.extract_variables_from_source_code(source_code, function_locations)

        return variables
    
    def analyze_variable_type_relations(self, func_code, variable_info):
        '''
        分析并返回具有相同格式类型的变量之间的关系。
        :param func_code: 函数的源代码字符串。
        :param variable_info: 包含变量名称和所属函数的列表。
        :return: 维护相同格式类型变量的字典。
        '''
        # 解析函数代码
        tree = ast.parse(func_code)
        
        # 用于存储参数和它们被赋值的变量之间的关系
        type_relations = []
        
        # 收集函数参数
        parameters = [node.arg for node in ast.walk(tree) if isinstance(node, ast.arg)]
        
        # 参数名称到其格式类型的映射
        parameter_type_mapping = {}

        # 初始化参数的格式类型
        for param in parameters:
            parameter_type_mapping[param] = param  # 初始时，参数的格式类型为其自身的名称

        # 辅助函数，用于遍历AST节点，寻找赋值关系
        def visit_node(node):
            if isinstance(node, ast.Assign):
                # 对于赋值语句，检查右侧是否包含函数参数
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assigned_var_name = target.id
                        if isinstance(node.value, ast.Name) and node.value.id in parameters:
                            # 如果赋值的是函数参数，则记录类型关系
                            parameter_type_mapping[assigned_var_name] = parameter_type_mapping[node.value.id]

        # 遍历AST树
        for node in ast.walk(tree):
            visit_node(node)
        
        # 维护一个字典，同一格式类型的变量对应的键值应该相同
        type_groups = {}
        for var in variable_info:
            var_name = var['name']
            var_program = var['program']
            if var_name in parameter_type_mapping:
                var_type = parameter_type_mapping[var_name]
                if var_type not in type_groups:
                    type_groups[var_type] = []
                type_groups[var_type].append({'name': var_name, 'program': var_program})

        return type_groups
