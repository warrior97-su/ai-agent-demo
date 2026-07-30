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
    expression = expression.replace(" ", "")
    allowed = set("0123456789+-*/().")
    if not all(c in allowed for c in expression):
        return {"error": "表达式包含无效字符"}
    try:
        result = eval(expression)  # 简单，但必须先做第 2 步安全检查
        return result
    except Exception:
        return {"error": "计算失败"}
