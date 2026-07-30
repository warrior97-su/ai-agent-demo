from tools.registry import register_tool


@register_tool(
    "get_weather",
    "查询城市天气",
    {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "城市名称",
            },
        },
        "required": ["city"],
    },
)
def get_weather(city):
    weather_data = {
        "北京": {"weather": "晴天", "temperature": 20, "unit": "摄氏度"},
        "上海": {"weather": "雨天", "temperature": 18, "unit": "摄氏度"},
        "广州": {"weather": "小雨", "temperature": 22, "unit": "摄氏度"},
        "深圳": {"weather": "晴天", "temperature": 24, "unit": "摄氏度"},
        "成都": {"weather": "多云", "temperature": 25, "unit": "摄氏度"},
        "重庆": {"weather": "小雨", "temperature": 26, "unit": "摄氏度"},
        "西安": {"weather": "晴天", "temperature": 27, "unit": "摄氏度"},
        "武汉": {"weather": "多云", "temperature": 28, "unit": "摄氏度"},
        "南京": {"weather": "小雨", "temperature": 29, "unit": "摄氏度"},
        "杭州": {"weather": "晴天", "temperature": 30, "unit": "摄氏度"},
        "周口": {"weather": "晴天", "temperature": 5, "unit": "摄氏度"},
    }
    return weather_data.get(city, {"error": "没有这个城市的数据"})
