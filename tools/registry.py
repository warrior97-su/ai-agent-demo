from tools.calculator import TOOL_SCHEMA as calculator_schema, calculate
from tools.weather import TOOL_SCHEMA as weather_schema, get_weather

TOOL_SCHEMAS = [
    weather_schema,
    calculator_schema,
]

AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "calculate": calculate,
}


def get_tool_schemas():
    return TOOL_SCHEMAS


def execute_tool(name, arguments):
    if name not in AVAILABLE_TOOLS:
        return {"error": f"未知工具: {name}"}
    return AVAILABLE_TOOLS[name](**arguments)
