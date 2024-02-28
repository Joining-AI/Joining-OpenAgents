class EssayWriterStatus:
    def __init__(self):
        # ��ʼ��ʱ���������״̬����ʾ
        self.initial_status = [
            {'procedure': "draft", 'status': 0},
            {'procedure': "writing", 'status': 0}
            # ���Լ��������������
        ]
        self.current_status = self.initial_status.copy()  # ʹ��.copy()ȷ��ԭʼ�б����޸�
        self.current_prompt = [
            {'procedure': "draft", 'prompt': 'promptstr1'},
            {'procedure': "writing", 'prompt': 'promptstr2'}
            # ���Լ�����������������ʾ
        ]

    def update_(self, instruction):
        self.current_status

    def update_status(self, procedure, new_status):
        """�����ض������״̬"""
        for status in self.current_status:
            if status['procedure'] == procedure:
                status['status'] = new_status
                return True  # ���³ɹ�
        return False  # δ�ҵ����裬����ʧ��

    def update_prompt(self, procedure, new_prompt):
        """�����ض��������ʾ"""
        for prompt in self.current_prompt:
            if prompt['procedure'] == procedure:
                prompt['prompt'] = new_prompt
                return True  # ���³ɹ�
        return False  # δ�ҵ����裬����ʧ��
    
    def get_current_prompt(self, procedure):
        """��ȡ�ض�����ĵ�ǰ��ʾ"""
        for prompt in self.current_prompt:
            if prompt['procedure'] == procedure:
                return prompt['prompt']
        return None  # δ�ҵ�����

    def add_step(self, procedure, status=0, prompt=''):
        """����µĲ���"""
        self.current_status.append({'procedure': procedure, 'status': status})
        self.current_prompt.append({'procedure': procedure, 'prompt': prompt})

    def complete_step(self, procedure):
        """��ǲ���Ϊ���״̬"""
        self.update_status(procedure, 1)

    def reset(self):
        """����״̬����ʼ״̬"""
        self.current_status = self.initial_status.copy()
        self.current_prompt = self.current_prompt.copy()  # ������Ҫ�����Ƿ�Ҳ������ʾ
