from tools.registry import register_tool
from datetime import datetime


@register_tool(
    "get_time",
    "查询当前时间",
    {
        "type": "object",
        "properties": {},
    },
)
def get_time():
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "weekday": datetime.now().weekday() + 1,
    }
