from tools.registry import register_tool


@register_tool(
    "calculate",
    "计算数学表达式",
    {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "数学表达式，例如2*2",
            },
        },
        "required": ["expression"],
    },
)
def calculate(expression):
    expression = expression.replace(" ", "")
    allowed = set("0123456789+-*/().")
    if not all(c in allowed for c in expression):
        return {"error": "表达式包含无效字符"}
    try:
        result = eval(expression)
        return result
    except Exception:
        return {"error": "计算失败"}
