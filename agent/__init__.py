__all__ = ["Agent", "ConversationMemory"]


def __getattr__(name):
    """Delay imports so storage-backed tools can import agent submodules safely."""
    if name == "Agent":
        from agent.core import Agent

        return Agent
    if name == "ConversationMemory":
        from agent.memory import ConversationMemory

        return ConversationMemory
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
