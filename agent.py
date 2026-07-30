import os

from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("OPENAI_BASE_URL"),
)


def get_weather(city):
    weather_data = {
        "北京": "晴天,20度",
        "上海": "多云,22度",
        "广州": "小雨,23度",
        "深圳": "晴天,24度",
        "成都": "多云,25度",
        "重庆": "小雨,26度",
        "西安": "晴天,27度",
        "武汉": "多云,28度",
        "南京": "小雨,29度",
        "杭州": "晴天,30度",
        "周口": {"weather": "晴天", "temperature": 5, "unit": "摄氏度"},
    }
    return weather_data.get(city, "暂无天气数据")
# 工具描述
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
]
# 第一次请求
response = client.chat.completions.create(
    model="gpt-5.6-sol",
    messages=[
        {
            "role": "user",
            "content": "周口天气怎么样",
        },
    ],
    timeout=60,
    tools=tools,
    tool_choice="auto",
)
message = response.choices[0].message


tool_call = message.tool_calls[0]

function_name = tool_call.function.name

arguments = json.loads(tool_call.function.arguments)

print("调用工具：", function_name)
print("参数：", arguments)
if function_name == "get_weather":
    weather = get_weather(arguments["city"])
    print("工具返回：", weather)
messages = [
    {"role": "user", "content": "周口天气怎么样"},
    message,
    {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(weather, ensure_ascii=False),
    },
]
response2 = client.chat.completions.create(
    model="gpt-5.6-sol",
    messages=messages,
)


print(response2.choices[0].message.content)
