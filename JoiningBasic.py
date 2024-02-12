from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal
import os
import json
import PyPDF2
import sys
import shutil
import subprocess
import importlib
import time

class JoiningManager:
    def __init__(self, api_url: str, api_key: str, conversation_list=None):
        self.api_url = api_url
        self.api_key = api_key
        self.api_type = 'openai'
        
        self.init_service()

        self.window_length = 4096

        self.helps = ''
        self.paper_structure = ''
        self.system_intel = ''
        
        self.conversation_info = {}
        self.conversation_list = []
        self.org_conversation = conversation_list
        self.current_conversation_name = ""
        self.rounds = 0        

        self.status_options = {
            'initiating': '初始化',
            'processing': '处理中',
            'completed': '已完成'
        }
        self.current_status = 'initiating'
        self.original_status = {'get_input': True, 'add_info': False, 'try_satisfy': False}
        self.status = self.original_status.copy()
        self.external_processor

        if conversation_list is None:
            self.conversation_list = [{"role": "system", "content": "System initialized"}]
        else:
            self.conversation_list = conversation_list
        
    def init_service(self, user_key: str, base_url: str) -> bool:
        import openai
        openai.api_key = user_key
        openai.api_base = base_url
        return True

    def add_conversation_info(self, conversation_name: str, conversation_list: list):
        """
        添加对话信息到字典中
        """
        self.conversation_info[conversation_name] = conversation_list

    def add_conversation(self, role: str, content: str) -> None:
        """
        添加对话记录
        """
        self.conversation_list.append({'role': role, 'content': content})

    def update_conversation_info(self, conversation_name: str, new_conversation_list: list):
        """
        更新指定对话名称的信息
        """
        if conversation_name in self.conversation_info:
            self.conversation_info[conversation_name] = new_conversation_list
        else:
            print(f"[系统]: 对话 '{conversation_name}' 不存在，无法更新信息。")

    def remove_conversation_info(self, conversation_name: str):
        """
        删除指定对话名称的信息
        """
        if conversation_name in self.conversation_info:
            del self.conversation_info[conversation_name]
        else:
            print(f"[系统]: 对话 '{conversation_name}' 不存在，无法删除信息。")

    def name_conversation(self, name: str = "DefaultConversation"):
        """
        将当前对话命名为指定名称，并添加到conversation_info
        """
        self.current_conversation_name = name
        if name not in self.conversation_info:
            self.add_conversation_info(name, self.conversation_list)
        print(f"[系统]: 当前对话已命名为 {name}。")

    def select_conversation(self, name: str):
        """
        选择指定名称的对话
        """
        if name in self.conversation_info:
            self.current_conversation_name = name
            print(f"[系统]: 已选择对话 '{name}'。")
        else:
            print(f"[系统]: 对话 '{name}' 不存在，请选择其他对话。")

    def get_conversation_info(self, conversation_name: str) -> dict:
        """
        获取指定对话名称的信息
        """
        return self.conversation_info.get(conversation_name, {})

    def clear_conversation(self):
        """
        清除对话记录，重置状态并清除当前对话名称及其相关信息
        """
        self.conversation_list = [{"role": "system", "content": "System initialized"}]
        self.status = self.original_status.copy()
        self.rounds = 0
        self.current_conversation_name = ""  # 清除当前对话名称

        # 清除相关的对话信息
        if self.current_conversation_name in self.conversation_info:
            del self.conversation_info[self.current_conversation_name]

        print("[系统]: 对话记录已清除。")


    def save_conversation(self, filename: str = "conversation.json"):
        """
        保存对话记录到文件中
        """
        import json
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.conversation_list, file, ensure_ascii=False, indent=4)
        print(f"[系统]: 对话记录已保存到 {filename}。")

    def generate_conversation_name(self, conversation_content: str) -> str:
        """
        生成对话名称
        """
        # 在这里编写生成对话名称的逻辑，可以根据对话内容进行生成
        return "GeneratedName"

    def summarize_conversation(self) -> bool:
        """
        对当前的对话背景信息进行总结，以减少长度，并保证essential_conversations的内容不被修改。
        """
        window_length = self.window_length  # 可设置的窗口长度
        essential_conversations = [self.conversation_list[1], self.conversation_list[-1]]

        # 计算essential_conversations的长度
        essential_length = sum(len(conv["content"]) for conv in essential_conversations)

        # 如果essential_conversations的长度已经超过窗口长度
        if essential_length > window_length :
            print("[系统]: 输入过长，请减少必要对话内容的长度。")
            return False

        # 初始化非必要对话内容的处理
        non_essential_conversations = self.conversation_list[2:-1]
        summarized_content = non_essential_conversations
        while essential_length + sum(len(conv["content"]) for conv in summarized_content) > window_length :
            storage=[]
            # 按照窗口长度切割并总结非必要对话内容
            current_summary = ""
            for conv in summarized_content:
                if len(current_summary) + len(conv["content"]) > window_length :
                    # 如果加上当前对话后超过窗口长度，则先对之前的内容进行总结
                    summary = self.ask_once(current_summary) if current_summary else ""
                    storage.append({"role": "system", "content": summary})
                    current_summary = conv["content"]  # 开始新的内容段
                else:
                    current_summary += " " + conv["content"]

            # 对最后一个段落进行总结
            if current_summary:
                summary = self.ask_once(current_summary)
                storage.append({"role": "system", "content": summary})
            summarized_content = storage

        # 计算新的总长度，检查是否满足要求
        new_total_length = essential_length + sum(len(conv["content"]) for conv in summarized_content)
        if new_total_length <= window_length :
            # 如果满足要求，更新对话列表
            self.conversation_list = [self.conversation_list[0]] + [essential_conversations[0]] + summarized_content + [essential_conversations[1]]
            return True
        else:
            print("[系统]: 即使经过总结，输入长度仍然过长。")
            return False

    def process_input(self, input_content: str):
        pass

    def set_api_type(self, api_type: str):
        """设置API类型，以决定与哪个API进行交互。"""
        self.api_type = api_type

    def ask_once(self, question: str) -> str:
        """根据配置的API类型向服务提出单次问题并获取回答。"""
        if self.api_type == 'openai':
            try:
                temp_conversation_list = [{"role": "user", "content": question}]
                response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=temp_conversation_list,
                    api_key=self.api_key
                )
                answer = response['choices'][0]['message']['content']
                return answer
            except openai.error.APIError as e:
                return f"OpenAI API错误: {str(e)}"
            except Exception as e:
                return f"处理错误: {str(e)}"
        # 这里可以添加其他API的逻辑
        else:
            return "未知API类型或未实现的API类型"

    def update_status(self, new_status: str) -> None:
        """
        更新对话状态
        """
        if new_status in self.status_options:
            self.current_status = new_status
        else:
            print("Invalid status.")

    def get_status(self) -> str:
        """
        获取当前状态
        """
        return self.status_options[self.current_status]

    def process_input(self, input_content: str) -> None:
        """
        处理输入，这里将留空，供外部逻辑实现
        """
        pass

    def set_external_processor(self, processor: callable) -> None:
        """
        设置外部处理逻辑
        """
        self.external_processor = processor

    def invoke_external_processor(self, input_content: str) -> None:
        """
        调用外部处理逻辑
        """
        if hasattr(self, 'external_processor'):
            self.external_processor(input_content)
        else:
            print("No external processor defined.")
            
class FileHandler:
    def __init__(self, base_path: str = None) -> None:
        """初始化文件处理器"""
        if base_path is None:
            self.base_path = os.path.dirname(__file__)
        else:
            self.base_path = base_path

    def get_full_path(self, relative_path: str) -> str:
        """获取文件的完整路径"""
        return os.path.join(self.base_path, relative_path)

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

class JoiningCodeRunner:
    def __init__(self, code_directory=None):
        self.code_directory = code_directory or os.path.join(os.getcwd(), 'TempCode')

    def run_code(self):
        if not os.path.exists(self.code_directory):
            print(f"目录 {self.code_directory} 不存在")
            return

        for filename in os.listdir(self.code_directory):
            if filename.endswith(".py"):
                filepath = os.path.join(self.code_directory, filename)
                print(f"正在运行: {filepath}")
                try:
                    self._execute_python_script(filepath)
                except Exception as e:
                    print(f"运行 {filename} 时出错: {e}")

    def _execute_python_script(self, filepath):
        result = subprocess.run(["python", filepath], capture_output=True, text=True)
        print(f"输出:\n{result.stdout}")
        if result.stderr:
            print(f"错误:\n{result.stderr}")

class JoiningPresenter(QWidget):
    message_sent = pyqtSignal(str)  # 定义一个信号，用于发送消息

    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        """初始化用户界面"""
        self.setWindowTitle('Chat Application')
        self.setGeometry(300, 300, 600, 400)
        
        layout = QVBoxLayout()
        
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)
        
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)
        
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.on_send_clicked)
        layout.addWidget(self.send_button)
        
        self.setLayout(layout)
        
    def on_send_clicked(self) -> None:
        """发送按钮点击事件处理"""
        user_input = self.input_field.text()
        if user_input:  # 确保输入不为空
            self.message_sent.emit(user_input)  # 发射信号，传递用户输入
            self.add_message_to_history(f"You: {user_input}")
            self.input_field.clear()

    def add_message_to_history(self, message: str) -> None:
        """将消息添加到聊天历史记录中"""
        self.chat_history.append(message)
