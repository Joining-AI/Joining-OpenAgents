import os
import importlib
from dotenv import load_dotenv

class OpenAIService:
    def __init__(self):
        # 加载当前目录的.env文件
        load_dotenv()

        self.openai = None
        self.initialized = False
        # 从环境变量中导入API密钥和基础URL
        self.user_key = os.getenv('OPENAI_API', None)
        self.base_url = os.getenv('OPENAI_URL', None)
        self.init_service(self.user_key, self.base_url)

    def init_service(self, user_key: str, base_url: str) -> bool:
        openai = importlib.import_module('openai')
        self.openai = openai
        self.openai.api_key = user_key
        self.openai.api_base = base_url
        self.initialized = True
        return True

    def ask_once(self, prompt: str) -> str:
        if not self.initialized:
            raise ValueError("服务未初始化，请先调用 init_service 方法初始化服务。")
        
        if not self.openai:
            raise ValueError("OpenAI 模块未正确导入，请检查安装。")
        response = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        if response and 'choices' in response and len(response['choices']) > 0:
            return print(response['choices'][0]['message']['content'])
        else:
            return ""
