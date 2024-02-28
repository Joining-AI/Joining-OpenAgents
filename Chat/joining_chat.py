import os
import json
import time
from dotenv import load_dotenv
from LLM_API import AuthenticatedRequestSender
from LLM_API import OpenAIService
from FileProcess import FileProcessor
from Memory import Embedding

class JoiningChat:
    def __init__(self, service_type=None, dotenv_path=None, conversation_list=None):
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
            raise ValueError('δ֪�ķ�������')
        
        self.window_length = 4096

        self.conversation_info = {}
        self.conversation_list = []

        self.current_conversation_name = ""
        if conversation_list == None:
            self.conversation_list = [{"role": "system", "content": "Your setting is:"}]
            
    def add_conversation_info(self, conversation_name: str, conversation_list: list):
        """
        ��ӶԻ���Ϣ���ֵ���
        """
        self.conversation_info[conversation_name] = conversation_list   
        
    def add_conversation(self, role: str, content: str) -> None:
        """
        ��ӶԻ���¼
        """
        self.conversation_list.append({'role': role, 'content': content})         

    def renew_conversation_info(self, response: str):
        self.conversation_list.append({"role": "assistant", "content": response})
        self.conversation_info[self.current_conversation_name] = self.conversation_list
       
    def generate_conversation_name(self, conversation_content: str) -> str:
        """
        ���ݶԻ������Զ����ɶԻ����ơ�
        """
        # �����Ϊʹ��ʱ����ͶԻ����ݵ�ǰ��������Ϊ����
        timestamp = time.strftime("%Y%m%d%H%M%S")
        summary = conversation_content + "..." 
        request = 'Please generate a name for the conversation based on the summary of following contents within 30 tokens: ' + summary
        name = self.service.ask_once(request)
        return name
    
    def name_conversation(self, name=None):
        """
        ����ǰ�Ի����������档���û���ṩ���ƣ����Զ�����һ����
        """
        # ��ʹ��self.conversation_list���������Ԫ���е�content
        content = "".join([c["content"] for c in self.conversation_list[-2:]])
        if name is None:
            name = self.generate_conversation_name(content)
        
        self.add_conversation_info(name, self.conversation_list)
        print(f"[ϵͳ]: �Ի�������Ϊ '{name}' �����档")
        self.current_conversation_name = name  # ��¼��ǰ�Ի�������

    def summarize_conversation(self) -> bool:
        """
        �Ե�ǰ�ĶԻ�������Ϣ�����ܽᣬ�Լ��ٳ��ȣ�����֤essential_conversations�����ݲ����޸ġ�
        """
        window_length = self.window_length  # �����õĴ��ڳ���
        essential_conversations = [self.conversation_list[1], self.conversation_list[-1]]

        # ����essential_conversations�ĳ���
        essential_length = sum(len(conv["content"]) for conv in essential_conversations)
        # ���essential_conversations�ĳ����Ѿ��������ڳ���
        if essential_length > window_length :
            print("[ϵͳ]: �������������ٱ�Ҫ�Ի����ݵĳ��ȡ�")
            return False

        # ��ʼ���Ǳ�Ҫ�Ի����ݵĴ���
        non_essential_conversations = self.conversation_list[1:-1]
        if not non_essential_conversations:
            return True
        summarized_content = non_essential_conversations
        while essential_length + sum(len(conv["content"]) for conv in summarized_content) > window_length :
            storage=[]
            # ���մ��ڳ����и�ܽ�Ǳ�Ҫ�Ի�����
            current_summary = ""
            for conv in summarized_content:
                if len(current_summary) + len(conv["content"]) > window_length :
                    # ������ϵ�ǰ�Ի��󳬹����ڳ��ȣ����ȶ�֮ǰ�����ݽ����ܽ�
                    summary = self.service.ask_once(current_summary) if current_summary else ""
                    storage.append({"role": "system", "content": summary})
                    current_summary = conv["content"]  # ��ʼ�µ����ݶ�
                else:
                    current_summary += " " + conv["content"]

            # �����һ����������ܽ�
            if current_summary:
                summary = self.service.ask_once(current_summary)
                storage.append({"role": "system", "content": summary})
            summarized_content = storage
            
                    # �����µ��ܳ��ȣ�����Ƿ�����Ҫ��
        new_total_length = essential_length + sum(len(conv["content"]) for conv in summarized_content)
        if new_total_length <= window_length :
            # �������Ҫ�󣬸��¶Ի��б�
            self.conversation_list = [self.conversation_list[0]] + [essential_conversations[0]] + summarized_content + [essential_conversations[1]]
            return True
        else:
            print("[ϵͳ]: ��ʹ�����ܽᣬ���볤����Ȼ������")
            return False
            
    def process_input(self,input):
        self.conversation_list.append({"role": "user", "content": input})
            # �ڷ�������֮ǰ��ȷ��������Ϣ���ȷ���Ҫ��
        if len(self.conversation_list) >= 2:  # ���Ի��б���2��������ϵͳ��ʼ����Ϣ��ʱ��ʼ��鳤��
            if not self.summarize_conversation():
                return "[ϵͳ]: �޷�����������Ϊ�Ի����ݹ�����"
            
        response = self.service.ask_once(input)
        self.renew_conversation_info(response)
        if len(self.conversation_list) == 3:
            self.name_conversation()
        
        return response