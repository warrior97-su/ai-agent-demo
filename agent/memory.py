class ConversationMemory:
    """管理 Agent 对话历史（内存记忆）。"""

    def __init__(self, system_prompt: str):
        self._messages = [{"role": "system", "content": system_prompt.strip()}]

    def add(self, message):
        self._messages.append(message)

    def get_messages(self):
        return self._messages

    def clear(self):
        """清空对话，保留 system prompt。"""
        system = self._messages[0]
        self._messages = [system]
