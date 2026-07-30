from tools import TOOL_SCHEMAS, execute_tool
import json
from config.settings import MODEL, client


class Agent:
    def __init__(self):
        self.client = client
        self.tools = TOOL_SCHEMAS
        self.messages = [
            {
                "role": "system",
                "content": """
                你是一个智能助手。
                规则：
                1. 如果用户的问题需要查询天气，调用天气工具。
                2. 如果用户的问题需要计算，调用计算工具。
                3. 如果用户的问题需要查询时间，调用时间工具。
                4. 工具返回的数据必须作为最终答案依据。
                5. 不要编造工具不存在的信息。
                """,
            },
        ]

    def run(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
        while True:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=self.messages,
                tools=self.tools,
                tool_choice="auto",
            )

            message = response.choices[0].message
            self.messages.append(message)
            if not message.tool_calls:
                print("\n最终回答：")
                print(message.content)
                return message.content

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name

                arguments = json.loads(tool_call.function.arguments)

                print("\n调用工具:", function_name)

                print("参数:", arguments)

                tool_result = execute_tool(function_name, arguments)
                print("工具结果:", tool_result)

                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result, ensure_ascii=False),
                    }
                )
