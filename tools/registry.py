_registry = {}


def register_tool(name, description, parameters):
    def decorator(func):
        _registry[name] = {
            "func": func,
            "schema": {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": parameters,
                },
            },
        }
        return func

    return decorator


def get_tool_schemas():
    return TOOL_SCHEMAS


def execute_tool(name, arguments):
    if name not in AVAILABLE_TOOLS:
        return {"error": f"未知工具: {name}"}
    return AVAILABLE_TOOLS[name](**arguments)


import tools.calculator  # noqa: E402, F401
import tools.weather  # noqa: E402, F401
import tools.time_tool  # noqa: E402, F401
import tools.memory_tool  # noqa: E402, F401
TOOL_SCHEMAS = [item["schema"] for item in _registry.values()]
AVAILABLE_TOOLS = {name: item["func"] for name, item in _registry.items()}
