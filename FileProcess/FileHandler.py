import os
import json
import shutil
import PyPDF2
import markdown

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