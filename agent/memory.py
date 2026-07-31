class ConversationMemory:
    def __init__(self, system_prompt: str):
        self._messages = [
            {"role": "system", "content": system_prompt.strip()},
        ]

    def add(self, message):
        self._messages.append(message)

    def get_messages(self):
        return self._messages

    def clear(self):
        system = self._messages[0]
        self._messages = [system]
