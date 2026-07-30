TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "calculate",
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
}


def calculate(expression):
    computed_data = {
        "1*1": "1",
        "2*2": "4",
        "3*3": "9",
        "4*4": "16",
        "5*5": "25",
    }
    return computed_data.get(expression, {"error": "没有这个值的计算结果"})
