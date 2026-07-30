# 学习示例

这些脚本记录了项目从 Demo 到 Framework 的演进过程，供学习参考。
日常使用请运行项目根目录的 `main.py`。

| 文件 | 说明 | 运行方式 |
|------|------|----------|
| `demo.py` | 最简 OpenAI 对话 | `python examples/demo.py` |
| `agent.py` | 单次 Tool Call 流程 | `python examples/agent.py` |
| `agent_loop.py` | Agent Loop 脚本版（Framework 之前的写法） | `python examples/agent_loop.py` |

请在项目根目录下运行，并确保已激活虚拟环境、配置好 `.env`。

---

## 工具注册：两种写法对比（v0.3 → v0.8）

项目里工具注册方式经历过一次演进，方便你对照理解。

### 旧写法：手动注册（v0.3 ~ v0.7）

**思路：** 每个工具文件单独定义 `TOOL_SCHEMA`，再在 `registry.py` 里手动汇总。

```text
weather.py      → 写 TOOL_SCHEMA + get_weather()
calculator.py   → 写 TOOL_SCHEMA + calculate()
registry.py     → import 两个 schema 和函数
                → 手动填入 TOOL_SCHEMAS 列表
                → 手动填入 AVAILABLE_TOOLS 字典
```

**新增工具要改 3 处：** 工具文件、`registry.py` 的 schema 列表、函数字典。

**缺点：** 容易漏改、重复维护；schema 和函数名要对齐。

查看旧代码：`git show 6cf5b6b:tools/registry.py`

---

### 新写法：装饰器自动注册（v0.8+，当前用法）

**思路：** 用 `@register_tool` 把 schema 和函数绑在一起，import 时自动进 `_registry`。

```text
weather.py      → @register_tool(...) 装饰 get_weather()
calculator.py   → @register_tool(...) 装饰 calculate()
registry.py     → 定义 register_tool 装饰器 + _registry
                → import tools.weather / tools.calculator（触发注册）
                → 自动生成 TOOL_SCHEMAS 和 AVAILABLE_TOOLS
```

**新增工具只改 2 处：** 工具文件加装饰器、`registry.py` 末尾加一行 import。

**优点：** schema 和函数不会分离；列表自动生成，不易漏。

当前实现见：`tools/registry.py`、`tools/weather.py`

---

### 怎么选？

| | 手动注册 | 装饰器注册 |
|---|---------|-----------|
| 适合 | 学习理解原理 | 日常开发、扩展工具 |
| 复杂度 | 简单直观 | 多一层装饰器概念 |
| 维护成本 | 工具多了很繁琐 | 低 |

建议：先用旧写法理解「注册表是什么」，再用装饰器写法做实际开发。
