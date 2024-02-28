import os
import json
import shutil
import PyPDF2
import markdown

class FileProcessor:
    def __init__(self, base_path: str = None) -> None:
        """��ʼ���ļ�������"""
        if base_path is None:
            self.base_path = os.path.dirname(__file__)
        else:
            self.base_path = base_path

    def get_full_path(self, relative_path: str) -> str:
        """��ȡ�ļ�������·��"""
        return os.path.join(self.base_path, relative_path)

    def create_and_write_json(self, folder_path: str, filename: str, data: dict) -> None:
        """��ָ���ļ����д��� JSON �ļ���д������"""
        full_folder_path = self.get_full_path(folder_path)
        full_file_path = os.path.join(full_folder_path, f"{filename}.json")

        # ����ļ���·�������ڣ��򴴽��ļ���
        if not os.path.exists(full_folder_path):
            os.makedirs(full_folder_path)

        with open(full_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"JSON �ļ� '{filename}.json' ���ļ��� '{folder_path}' �д�����д��ɹ�.")

    def read_file(self, file_path: str) -> str:
        """�����ļ�����ѡ���ʵ��Ķ�ȡ����"""
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
        """��ȡ�ı��ļ�"""
        with open(self.get_full_path(file_path), 'r', encoding='utf-8') as file:
            return file.read()

    def read_json_file(self, file_path: str) -> dict:
        """��ȡJSON�ļ�"""
        with open(self.get_full_path(file_path), 'r', encoding='utf-8') as file:
            return json.load(file)

    def read_pdf_file(self, file_path: str) -> str:
        """��ȡPDF�ļ�����Ҫʹ���ⲿ��"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except FileNotFoundError:
            return "�ļ�δ�ҵ��������ļ�·����"
        except PyPDF2.utils.PdfReadError:
            return "�޷���ȡPDF�ļ�����ȷ���ļ���ʽ��ȷ��"

    def write_file(self, file_path: str, content: str) -> None:
        """д���ļ��������ļ�����ѡ���ʵ���д�뷽��"""
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
        """д���ı��ļ�"""
        with open(self.get_full_path(file_path), 'w', encoding='utf-8') as file:
            file.write(content)

    def write_json_file(self, file_path: str, content: dict) -> None:
        """д��JSON�ļ�"""
        with open(self.get_full_path(file_path), 'w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)

    def write_pdf_file(self, file_path: str, content: str) -> None:
        """д��PDF�ļ�"""
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.addPage(PyPDF2.PageObject.createTextPage(content))
        with open(self.get_full_path(file_path), 'wb') as file:
            pdf_writer.write(file)

    def delete_file(self, file_path: str) -> None:
        """ɾ���ļ�"""
        os.remove(self.get_full_path(file_path))

    def move_file(self, source_path: str, destination_path: str) -> None:
        """�ƶ��ļ�"""
        shutil.move(self.get_full_path(source_path), self.get_full_path(destination_path))
        
    def parse_md_to_html(self, file_path):
        """��Markdown�ļ�����ΪHTML"""
        md_content = self.read_text_file(file_path)
        html_content = markdown.markdown(md_content)
        return html_content