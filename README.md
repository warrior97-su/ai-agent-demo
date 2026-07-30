# AI Agent Demo

基于 OpenAI SDK 的小型 Agent Framework，支持 Tool Call 与 Agent Loop。

## 功能

- **Agent Framework**（`main.py` + `agent/` + `config/` + `tools/`）
- 学习示例（`examples/`，含 demo、单次 Tool Call、Agent Loop 脚本版）
- 工具模块化（`tools/`）
- 配置集中管理（`config/`）

## 环境要求

- Python 3.10+
- pip

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/warrior97-su/ai-agent-demo.git
cd ai-agent-demo
```

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

编辑 `.env` 文件：

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.freemodel.dev/v1
MODEL=gpt-5.6-sol
```

### 4. 运行

```bash
# 命令行提问（推荐）
python main.py 北京天气怎么样
python main.py 帮我算一下 2*2

# 不传参数时使用默认问题
python main.py

# 学习示例（可选）
python examples/demo.py
python examples/agent.py
python examples/agent_loop.py
```

## 项目结构

```text
ai-agent-demo/
├── main.py              # 程序入口
├── config/              # 配置层
│   ├── __init__.py
│   └── settings.py      # 读取 .env，提供 MODEL、client 等
├── agent/               # Agent 核心
│   ├── __init__.py
│   └── core.py          # Agent 类，封装 Agent Loop
├── tools/               # 工具层
│   ├── __init__.py      # 对外导出 TOOL_SCHEMAS、execute_tool
│   ├── registry.py      # 工具注册表与调度
│   ├── weather.py       # 天气工具
│   └── calculator.py    # 计算器工具
├── examples/            # 学习示例（演进过程）
│   ├── README.md
│   ├── demo.py
│   ├── agent.py
│   └── agent_loop.py
├── requirements.txt
├── .env.example
├── README.md
└── CHANGELOG.md         # 版本更新日志
```

## 架构进度

| 步骤 | 模块 | 状态 | 说明 |
|------|------|------|------|
| 1 | `config/settings.py` | ✅ 完成 | 集中读取 API Key、BASE_URL、MODEL |
| 2 | `agent/core.py` | ✅ 完成 | Agent 类封装 Agent Loop |
| 3 | `main.py` | ✅ 完成 | 程序入口 |
| 4 | 清理 | ✅ 完成 | 旧脚本归档至 `examples/` |
| 5 | 命令行传参 | ✅ 完成 | `python main.py <问题>` |
| 6 | 多轮对话 REPL | 进行中 | 终端持续提问，输入 quit 退出 |

## 模块职责

| 模块 | 职责 |
|------|------|
| `config` | 环境变量与 OpenAI 客户端配置 |
| `agent` | Agent Loop：问模型 → 调工具 → 再问模型 |
| `tools` | 工具定义、注册与执行 |
| `main` | 程序入口 |

## 添加新工具

1. 在 `tools/` 下新建文件，定义 `TOOL_SCHEMA` 和工具函数
2. 在 `tools/registry.py` 中注册
3. 如需对外暴露，更新 `tools/__init__.py`

## 注意事项

- `.env` 已被 Git 忽略，请勿提交 API Key
- 运行前请激活虚拟环境：`.venv\Scripts\activate`
- 学习示例见 [examples/README.md](./examples/README.md)
- 版本变更记录见 [CHANGELOG.md](./CHANGELOG.md)

## License

MIT
