# AI Agent Demo

基于 OpenAI SDK 的 AI Agent 入门示例，通过兼容 OpenAI 接口的 API 调用大模型。

## 功能

- 使用 OpenAI Python SDK 发起对话请求
- 通过 `.env` 文件管理 API Key，避免密钥写入代码
- 支持自定义 `base_url`，可对接 OpenAI 兼容接口

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

复制环境变量模板并填入真实配置：

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
```

### 4. 运行示例

```bash
python demo.py
```

## 项目结构

```text
ai-agent-demo/
├── demo.py           # 示例脚本
├── requirements.txt  # Python 依赖
├── .env.example      # 环境变量模板
├── .gitignore
└── README.md
```

## 注意事项

- `.env` 文件已被 Git 忽略，请勿将 API Key 提交到仓库
- 如需更换模型，修改 `demo.py` 中的 `model` 参数即可

## License

MIT
