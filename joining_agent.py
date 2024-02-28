import os
import json
from dotenv import load_dotenv
from LLM_API import AuthenticatedRequestSender
from LLM_API import OpenAIService
from FileProcess import FileProcessor
from Memory import Embedding, LocalMemory
from Chat import JoiningChat
from WebExecuter import WebSearch
from FileProcess import CodeAnalyser
from Tools import FunctionManager
import re
import importlib
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import whisper

class JoiningAgent:
    def __init__(self, service_type, root_path) -> None:
        if service_type in ['sensetime', None]:
            self.service = AuthenticatedRequestSender()
        elif service_type == 'openai':
            self.service = OpenAIService()
        else:
            raise ValueError('未知的服务类型')
        self.chat= JoiningChat(service_type=service_type, root_path=root_path)
        if root_path is None:
            root_path = os.getcwd()
        dotenv_path = os.path.join(root_path, '.env')
        load_dotenv(dotenv_path)
        self.file_handler = FileProcessor(root_path)
        self.embedder = Embedding()
        self.local_memory = LocalMemory(service_type, root_path)
