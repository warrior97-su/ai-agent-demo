import os

from dotenv import load_dotenv
from openai import OpenAI
import json


load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("OPENAI_BASE_URL"),
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询城市天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称",
                    },
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_computed",
            "description": "计算数学表达式",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，例如2*2",
                    },
                },
                "required": ["expression"],
            },
        },
    },
]


# 工具
def get_weather(city):
    weather_data = {
        "北京": {"weather": "晴天", "temperature": 20, "unit": "摄氏度"},
        "上海": {"weather": "雨天", "temperature": 18, "unit": "摄氏度"},
        "广州": {"weather": "小雨", "temperature": 22, "unit": "摄氏度"},
        "深圳": {"weather": "晴天", "temperature": 24, "unit": "摄氏度"},
        "成都": {"weather": "多云", "temperature": 25, "unit": "摄氏度"},
        "重庆": {
            "weather": "小雨",
            "temperature": 26,
            "unit": "摄氏度",
        },
        "武汉": {
            "weather": "多云",
            "temperature": 28,
            "unit": "摄氏度",
        },
        "南京": {
            "weather": "小雨",
            "temperature": 29,
            "unit": "摄氏度",
        },
        "杭州": {
            "weather": "晴天",
            "temperature": 30,
            "unit": "摄氏度",
        },
        "周口": {
            "weather": "晴天",
            "temperature": 5,
            "unit": "摄氏度",
        },
    }
    return weather_data.get(city, {"error": "没有这个城市的数据"})


def get_computed(expression):
    computed_data = {
        "1*1": "1",
        "2*2": "4",
        "3*3": "9",
        "4*4": "16",
        "5*5": "25",
    }
    return computed_data.get(expression, {"error": "没有这个值的计算结果"})


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
        model="gpt-5.6-sol",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    message = response.choices[0].message
    # 保存模型消息
    messages.append(message)
    # =====================
    # 没有工具调用
    # =====================

    if not message.tool_calls:
        print("\n最终回答：")
        print(message.content)

        break

    # =====================
    # 有工具调用
    # =====================

    for tool_call in message.tool_calls:
        function_name = tool_call.function.name

        arguments = json.loads(tool_call.function.arguments)

        print("\n调用工具:", function_name)

        print("参数:", arguments)

        # 执行工具

        if function_name == "get_weather":
            result = get_weather(arguments["city"])
        elif function_name == "get_computed":
            result = get_computed(arguments["expression"])

        print("工具结果:", result)

        # 返回工具结果给模型

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False),
            }
        )
