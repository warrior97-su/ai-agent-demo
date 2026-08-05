import unittest
from agent.memory import ConversationMemory as AgentConversationMemory


class ConversationMemoryTests(unittest.TestCase):
    def test_clear_removes_conversation_messages(self):
        memory = AgentConversationMemory("你是一个智能助手", max_messages=20)
        memory.add({"role": "user", "content": "你好"})
        memory.add({"role": "assistant", "content": "你好，有什么可以帮助你？"})
        memory.clear()
        messages = memory.get_messages()
        self.assertEqual(messages, [{"role": "system", "content": "你是一个智能助手"}])

    def test_clear_preserves_all_system_messages(self):
        memory = AgentConversationMemory("你是一个智能助手", max_messages=10)
        memory.add({"role": "system", "content": "用户长期事实：用户住在南京"})
        memory.add({"role": "user", "content": "我住在哪里？"})
        memory.clear()
        messages = memory.get_messages()
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "system")
        self.assertIn("南京", messages[1]["content"])

    def test_get_messages_keeps_recent_messages(self):
        memory = AgentConversationMemory("你是一个智能助手", max_messages=2)
        memory.add({"role": "user", "content": "问题一"})
        memory.add({"role": "assistant", "content": "回答一"})
        memory.add({"role": "user", "content": "问题二"})
        memory.add({"role": "assistant", "content": "回答二"})
        messages = memory.get_messages()
        self.assertEqual(
            messages,
            [
                {
                    "role": "system",
                    "content": "你是一个智能助手",
                },
                {
                    "role": "user",
                    "content": "问题二",
                },
                {
                    "role": "assistant",
                    "content": "回答二",
                },
            ],
        )

    def test_system_messages_do_not_count_toward_limit(self):
        memory = AgentConversationMemory(
            "你是一个智能助手",
            max_messages=2,
        )
        memory.add(
            {
                "role": "system",
                "content": "用户长期事实：用户喜欢简洁回答",
            }
        )
        memory.add({"role": "user", "content": "问题一"})
        memory.add({"role": "assistant", "content": "回答一"})
        memory.add({"role": "user", "content": "问题二"})
        memory.add({"role": "assistant", "content": "回答二"})

        messages = memory.get_messages()

        system_messages = [
            message for message in messages if message["role"] == "system"
        ]
        conversation_messages = [
            message for message in messages if message["role"] != "system"
        ]

        self.assertEqual(len(system_messages), 2)
        self.assertEqual(len(conversation_messages), 2)
        self.assertEqual(conversation_messages[0]["content"], "问题二")
        self.assertEqual(conversation_messages[1]["content"], "回答二")

    def test_tool_call_chain_is_not_split(self):
        memory = AgentConversationMemory(
            "你是一个智能助手",
            max_messages=1,
        )
        memory.add({"role": "user", "content": "帮我查天气"})
        memory.add(
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": "call-1",
                        "type": "function",
                        "function": {
                            "name": "get_weather",
                            "arguments": '{"city": "北京"}',
                        },
                    }
                ],
            }
        )
        memory.add(
            {"role": "tool", "tool_call_id": "call-1", "content": '{"temperature":20}'}
        )
        messages = memory.get_messages()
        self.assertEqual(
            [message["role"] for message in messages],
            ["system", "user", "assistant", "tool"]
        )

if __name__ == "__main__":
    unittest.main()
