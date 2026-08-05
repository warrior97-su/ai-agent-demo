class ConversationMemory:
    def __init__(self, system_prompt: str, max_messages: int | None = 20):
        if max_messages is not None and max_messages < 1:
            raise ValueError("max_messages 必须大于 0")
        self.max_messages = max_messages
        self._messages = [
            {"role": "system", "content": system_prompt.strip()},
        ]

    def add(self, message):
        self._messages.append(message)

    def get_messages(self):
        system_messages = [
            message for message in self._messages if self._get_role(message) == "system"
        ]
        conversation_messages = [
            message for message in self._messages if self._get_role(message) != "system"
        ]
        if (
            self.max_messages is not None
            and len(conversation_messages) > self.max_messages
        ):
            conversation_messages = self._keep_recent_messages(conversation_messages)
            # conversation_messages = conversation_messages[-self.max_messages:]
        return system_messages + conversation_messages

    def clear(self):
        self._messages = [
            message for message in self._messages if self._get_role(message) == "system"
        ]

    def _keep_recent_messages(self, messages):
        start = len(messages) - self.max_messages

        while start > 0:
            message = messages[start]
            role = self._get_role(message)
            # 如果从 tool 消息开始，向前寻找对应的 assistant
            if role == "tool":
                start -= 1
                continue
            # 如果第一条是带 tool_calls 的 assistant，
            # 再把对应的 user 消息一起保留
            if (
                role == "assistant"
                and self._has_tool_calls(message)
                and self._get_role(messages[start - 1]) == "user"
            ):
                start -= 1
            break
        return messages[start:]
    @staticmethod
    def _has_tool_calls(message):
        if isinstance(message, dict):
            return bool(message.get("tool_calls"))
        return bool(getattr(message, "tool_calls", None))
    @staticmethod
    def _get_role(message):
        if isinstance(message, dict):
            return message.get("role")
        return getattr(message, "role", None)
