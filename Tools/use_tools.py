import os
import json
import ast
from FileProcess import CodeAnalyser
from LLM_API import AuthenticatedRequestSender, OpenAIService

class FunctionManager:
    def __init__(self, project_root: str, service_type):
        self.project_root = project_root
        self.functions_info_path = os.path.join(project_root, "Tools", "functions_info.json")
        self.functions_info = self.load_functions_info()    #dict
        self.tools_path = os.path.join(project_root, "Tools", "tools.py")
        self.tools_code = self.load_tools_code()            #str
        self.save_path = os.path.join("Tools", "tools.py")
        self.processor = CodeAnalyser()
        if service_type in ['sensetime', None]:
            self.service = AuthenticatedRequestSender()
        elif service_type == 'openai':
            self.service = OpenAIService()
        else:
            raise ValueError('未知的服务类型')
    
    def load_functions_info(self):
        if os.path.exists(self.functions_info_path):
            with open(self.functions_info_path, 'r') as file:
                return json.load(file)
        else:
            return {"functions": []}
        
    def load_tools_code(self):
        with open(self.tools_path, 'r') as file:
            return file.read()
        
    def update_functions_info(self, function_name, function_code):
        self.functions_info["functions"].append({"name": function_name, "code": function_code})

    def save_functions_info(self):
        with open(self.functions_info_path, 'w') as file:
            json.dump(self.functions_info, file, indent=4)

    def parse_functions_from_code(self):
        tree = ast.parse(self.tools_code)
        functions_and_classes = self.processor.get_functions_and_classes(self.tools_code)

        # 获取所有没有父节点的函数，将其视为独立的方法
        standalone_functions = []
        for node_type, name, start_line, end_line, parent_name, parameters in functions_and_classes:
            if parent_name is None:
                # 获取函数源代码
                source_code = self.get_function_source_code(name, start_line, end_line)
                
                # 解析函数
                function_node = ast.parse(source_code).body[0]
                return_expr = self.get_return_expression(function_node)

                standalone_functions.append((node_type, name, start_line, end_line, None, parameters, source_code, return_expr))

        return standalone_functions

    def get_return_expression(self, function_node):
        for node in ast.walk(function_node):
            if isinstance(node, ast.Return):
                if node.value:
                    return ast.dump(node.value)
                else:
                    return None
        return None


    def get_function_source_code(self, name, start_line, end_line):
        # 从原始代码中提取函数的源代码
        lines = self.tools_code.split('\n')
        source_lines = lines[start_line - 1:end_line]
        source_code = '\n'.join(source_lines)
        return source_code

    def compare_functions(self, parsed_functions):
        existing_functions = {func['name']: func for func in self.functions_info['functions']}
        new_functions = []
        updated_functions = []

        for node_type, name, start_line, end_line, parent_name, parameters, source_code, return_expr in parsed_functions:
            if name in existing_functions:
                existing_func = existing_functions[name]
                # 检查是否有需要更新的描述字段
                updated_fields = {}
                if existing_func.get('description') is None:
                    # 如果原描述为空，尝试用代码解析补充
                    update_description=self.service.ask_once(f"please return a description for the function '{name}', of the following content:'{source_code}' focusing on its use, don't return any other irrelevant information.")
                    updated_fields['description'] = update_description
                # 其他字段的更新逻辑，比如输入参数、输出参数、依赖项等

                # 如果有需要更新的字段，更新函数信息
                if updated_fields:
                    existing_func.update(updated_fields)
                    updated_functions.append(existing_func)
            else:
                # 如果函数不存在于已有描述中，视为新函数
                update_description=self.service.ask_once(f"please return a description for the function '{name}', of the following content:'{source_code}' focusing on its use, don't return any other irrelevant information.")
                new_functions.append({
                    "name": name,
                    "description": update_description,
                    "input": parameters,  # 这里将参数作为输入
                    "output": return_expr,  # 输出字段为空，您可以自行补充
                    "file_path": self.save_path,  # 统一的文件路径
                    "dependencies": []  # 暂时将依赖项设置为空列表
                })

        return new_functions, updated_functions

    def update_functions_info(self, new_functions, updated_functions):
        # 将新函数添加到 functions_info 中
        self.functions_info['functions'].extend(new_functions)
        # 更新已有函数的信息
        for func in updated_functions:
            for i, existing_func in enumerate(self.functions_info['functions']):
                if existing_func['name'] == func['name']:
                    self.functions_info['functions'][i] = func

        # 保存更新后的信息到文件
        self.save_functions_info()
        
    def update_func_json(self):
        parsed_functions = self.parse_functions_from_code()
        new_functions, updated_functions = self.compare_functions(parsed_functions)
        self.update_functions_info(new_functions, updated_functions)