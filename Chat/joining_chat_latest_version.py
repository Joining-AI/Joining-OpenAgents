import os
import json
import time
from dotenv import load_dotenv
from LLM_API import AuthenticatedRequestSender, OpenAIService
from FileProcess import FileProcessor
from Memory import Embedding


class JoiningChat:
    def __init__(self, service_type=None, root_path=None, conversation_list=None):
        if root_path is None:
            root_path = os.getcwd()
        dotenv_path = os.path.join(root_path, '.env')
        load_dotenv(dotenv_path)

        self.file_handler = FileProcessor(root_path)
        self.embedder = Embedding()

        if service_type in ['sensetime', None]:
            self.service = AuthenticatedRequestSender()
        elif service_type == 'openai':
            self.service = OpenAIService()
        else:
            raise ValueError('未知的服务类型')

        self.window_length = 4096
        self.conversation_info = {}
        self.conversation_list = conversation_list if conversation_list else [{"role": "system", "content": "Your setting is:"}]
        self.current_conversation_name = ""

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

    def renew_conversation_info(self, response: str):
        self.conversation_list.append({"role": "assistant", "content": response})
        self.conversation_info[self.current_conversation_name] = self.conversation_list

    def generate_conversation_name(self, conversation_content: str) -> str:
        """
        根据对话内容自动生成对话名称。
        """
        timestamp = time.strftime("%Y%m%d%H%M%S")
        summary = conversation_content + "..."
        request = f'Please generate a name for the conversation based on the summary of following contents within 30 tokens: {summary}'
        name = self.service.ask_once(request)
        return name

    def name_conversation(self, name=None):
        """
        给当前对话命名并保存。如果没有提供名称，将自动生成一个。
        """
        content = "".join([c["content"] for c in self.conversation_list[-2:]])
        if name is None:
            name = self.generate_conversation_name(content)

        self.add_conversation_info(name, self.conversation_list)
        print(f"[系统]: 对话已命名为 '{name}' 并保存。")
        self.current_conversation_name = name

    def summarize_conversation(self) -> bool:
        """
        对当前的对话背景信息进行总结，以减少长度，并保证essential_conversations的内容不被修改。
        """
        window_length = self.window_length
        essential_conversations = [self.conversation_list[1], self.conversation_list[-1]]
        essential_length = sum(len(conv["content"]) for conv in essential_conversations)

        if essential_length > window_length:
            print("[系统]: 输入过长，请减少必要对话内容的长度。")
            return False

        non_essential_conversations = self.conversation_list[1:-1]
        if not non_essential_conversations:
            return True

        summarized_content = non_essential_conversations
        while essential_length + sum(len(conv["content"]) for conv in summarized_content) > window_length:
            storage = []
            current_summary = ""
            for conv in summarized_content:
                if len(current_summary) + len(conv["content"]) > window_length:
                    summary = self.service.ask_once(current_summary) if current_summary else ""
                    storage.append({"role": "system", "content": summary})
                    current_summary = conv["content"]
                else:
                    current_summary += " " + conv["content"]

            if current_summary:
                summary = self.service.ask_once(current_summary)
                storage.append({"role": "system", "content": summary})
            summarized_content = storage

        new_total_length = essential_length + sum(len(conv["content"]) for conv in summarized_content)
        if new_total_length <= window_length:
            self.conversation_list = [self.conversation_list[0]] + [essential_conversations[0]] + summarized_content + [essential_conversations[1]]
            return True
        else:
            print("[系统]: 即使经过总结，输入长度仍然过长。")
            return False

    def process_input(self, input):
        self.conversation_list.append({"role": "user", "content": input})
        if len(self.conversation_list) >= 2:
            if not self.summarize_conversation():
                return "[系统]: 无法继续处理，因为对话内容过长。"

        response = self.service.ask_once(input)
        self.renew_conversation_info(response)
        if len(self.conversation_list) == 3:
            self.name_conversation()

        return response
