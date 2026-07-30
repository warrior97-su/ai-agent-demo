import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import MODEL, client
from tools import TOOL_SCHEMAS, execute_tool

tools = TOOL_SCHEMAS

messages = [
    {
        "role": "system",
        "content": """
        你是一个智能助手。
        规则：
        1. 如果用户的问题需要查询天气，调用天气工具。
        2. 如果用户的问题需要计算，调用计算工具。
        3. 工具返回的数据必须作为最终答案依据。
        4. 不要编造工具不存在的信息。
        """,
    },
    {
        "role": "user",
        "content": "哈尔滨天气怎么样？现在温度是多少？，顺便帮我算一下2*3的计算结果",
    },
]

while True:
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        print("\n最终回答：")
        print(message.content)
        break

    for tool_call in message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print("\n调用工具:", function_name)
        print("参数:", arguments)

        tool_result = execute_tool(function_name, arguments)
        print("工具结果:", tool_result)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result, ensure_ascii=False),
            }
        )
