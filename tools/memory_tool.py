from pathlib import Path

from agent.memory_store import SQLiteMemoryStore
from tools.registry import register_tool


STORE = SQLiteMemoryStore(Path("data/memory.db"))
USER_ID = "default"


@register_tool(
    "remember_fact",
    "保存用户明确要求记住的长期信息。",
    {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "description": "记忆类别，例如 profile、preference、project、constraint。",
            },
            "key": {
                "type": "string",
                "description": "稳定的英文键名，例如 city、answer_style、primary_language。",
            },
            "value": {
                "type": "string",
                "description": "要记住的具体内容。",
            },
        },
        "required": ["category", "key", "value"],
        "additionalProperties": False,
    },
)
def remember_fact(category: str, key: str, value: str):
    STORE.upsert_fact(
        user_id=USER_ID,
        category=category,
        key=key,
        value=value,
        source="用户通过 Agent 明确要求记住",
    )
    return {
        "success": True,
        "message": f"已记住：{key}={value}",
    }


@register_tool(
    "forget_fact",
    "删除用户明确要求忘记的长期记忆。",
    {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "description": "记忆类别，例如 profile、preference、project、constraint。",
            },
            "key": {
                "type": "string",
                "description": "要忘记的英文键名。",
            },
        },
        "required": ["category", "key"],
        "additionalProperties": False,
    },
)
def forget_fact(category: str, key: str):
    forgotten = STORE.forget_fact(
        user_id=USER_ID,
        category=category,
        key=key,
    )
    return {
        "success": forgotten,
        "message": f"已忘记：{key}" if forgotten else "没有找到对应的长期记忆。",
    }
