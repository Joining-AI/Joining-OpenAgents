class EssayWriterStatus:
    def __init__(self):
        # 初始化时，各步骤的状态和提示
        self.initial_status = [
            {'procedure': "draft", 'status': 0},
            {'procedure': "writing", 'status': 0}
            # 可以继续添加其他步骤
        ]
        self.current_status = self.initial_status.copy()  # 使用.copy()确保原始列表不被修改
        self.current_prompt = [
            {'procedure': "draft", 'prompt': 'promptstr1'},
            {'procedure': "writing", 'prompt': 'promptstr2'}
            # 可以继续添加其他步骤的提示
        ]

    def update_(self, instruction):
        self.current_status

    def update_status(self, procedure, new_status):
        """更新特定步骤的状态"""
        for status in self.current_status:
            if status['procedure'] == procedure:
                status['status'] = new_status
                return True  # 更新成功
        return False  # 未找到步骤，更新失败

    def update_prompt(self, procedure, new_prompt):
        """更新特定步骤的提示"""
        for prompt in self.current_prompt:
            if prompt['procedure'] == procedure:
                prompt['prompt'] = new_prompt
                return True  # 更新成功
        return False  # 未找到步骤，更新失败
    
    def get_current_prompt(self, procedure):
        """获取特定步骤的当前提示"""
        for prompt in self.current_prompt:
            if prompt['procedure'] == procedure:
                return prompt['prompt']
        return None  # 未找到步骤

    def add_step(self, procedure, status=0, prompt=''):
        """添加新的步骤"""
        self.current_status.append({'procedure': procedure, 'status': status})
        self.current_prompt.append({'procedure': procedure, 'prompt': prompt})

    def complete_step(self, procedure):
        """标记步骤为完成状态"""
        self.update_status(procedure, 1)

    def reset(self):
        """重置状态到初始状态"""
        self.current_status = self.initial_status.copy()
        self.current_prompt = self.current_prompt.copy()  # 根据需要决定是否也重置提示
