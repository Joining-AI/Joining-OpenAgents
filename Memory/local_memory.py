import os
import json
from dotenv import load_dotenv
from LLM_API import AuthenticatedRequestSender
from LLM_API import OpenAIService
from FileProcess import FileProcessor
from Memory import Embedding

class LocalMemory:
    def __init__(self, service_type=None, dotenv_path=None):
        if dotenv_path == None:
            dotenv_path = os.path.join(os.getcwd(), '.env')
        root_path = dotenv_path.rstrip('.env')
        load_dotenv(dotenv_path)
        self.file_handler = FileProcessor(root_path)
        self.embedder = Embedding()
        if service_type in ['sensetime', None]:
            self.service = AuthenticatedRequestSender()
        elif service_type == 'openai':
            self.service = OpenAIService()
        else:
            raise ValueError('未知的服务类型')

    def embed_and_store(self, string=None, data_structure=None, service_processor=None, file_processor=None, folder_path='VectorData', filename='VecMemory'):
        """将消息嵌入并将结果与消息一起存储，并将数据写入 JSON 文件"""
        if service_processor is None:
            service_processor = self.service
        if file_processor is None:
            file_processor = self.file_handler
        if data_structure is None:
            data_structure = []

        embedding = service_processor.embed(string)
        data_structure.append({"message": string, "embedding": embedding})

        full_file_path = file_processor.get_full_path(os.path.join(folder_path, f"{filename}.json"))

        if os.path.exists(full_file_path):
            with open(full_file_path, 'r') as json_file:
                existing_data = json.load(json_file)
                is_existing = False
                for entry in existing_data:
                    if entry["message"] == string:
                        is_existing = True
                        break
                if is_existing:
                    return print(f'{string}已经存入')
            existing_data.extend(data_structure)

            with open(full_file_path, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)
        else:
            file_processor.create_and_write_json(folder_path, filename, data_structure)
        
    def similar_search(self, message, top_k=None):
        full_file_path = self.file_handler.get_full_path(os.path.join('VectorData', f"VecMemory.json"))
        data = self.file_handler.read_file(full_file_path)
        if top_k is None:
            return self.embedder.find_top_similar_messages(message, data)
        else:
            return self.embedder.find_top_similar_messages(message, data, top_n=top_k)
