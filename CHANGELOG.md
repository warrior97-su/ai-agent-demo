# 更新日志

本文件记录每个版本的变更。版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- **主版本号**：不兼容的大改动
- **次版本号**：向下兼容的新功能
- **修订号**：向下兼容的问题修复

---

## [0.11.0] - 2026-08-03

新增基于 SQLite 的长期记忆，使 Agent 能在重启后恢复用户明确保存的信息。

### 新增
- `agent/memory_store.py`：`SQLiteMemoryStore`，支持长期事实的保存、读取、更新、忘记和用户隔离
- `tools/memory_tool.py`：`remember_fact`、`forget_fact` 工具
- `tests/test_memory_store.py`：SQLite 长期记忆离线单元测试

### 变更
- `agent/core.py`：启动时加载长期记忆，并作为参考上下文传递给模型
- `agent/core.py`：system prompt 增加明确记住/忘记的工具调用规则与敏感信息限制
- `main.py`：忽略空输入，避免空消息触发模型调用
- `agent/__init__.py`：惰性导出，避免记忆工具注册时的循环导入
- `.gitignore`：忽略本地长期记忆数据库 `data/*.db`

### 对比上一版本
| 项目 | v0.10.0 | v0.11.0 |
|------|---------|---------|
| 对话记忆 | 仅当前 Agent 实例的短期上下文 | 短期上下文 + SQLite 长期记忆 |
| 用户资料 | 重启后丢失 | 明确保存后可跨重启恢复 |
| 记忆管理 | 无 | 支持记住与忘记工具 |

---

## [0.10.0] - 2026-07-31

将对话历史抽离为独立记忆模块，并增加 API 备用通道。

### 新增
- `agent/memory.py`：`ConversationMemory` 类，提供 `add()`、`get_messages()`、`clear()`
- `config/settings.py`：`chat_create()` 主线路失败时自动切换 WorkBuddy 备用通道
- 备用 API 支持独立 Key（`OPENAI_FALLBACK_API_KEY`）与 HTTP/2 连接

### 变更
- `agent/core.py`：`self.messages` 改为 `self.memory`；`SYSTEM_PROMPT` 单点定义
- `agent/__init__.py` 导出 `ConversationMemory`
- `agent/core.py` 通过 `chat_create()` 调用模型
- `.env.example` 补充备用 API 配置项
- `requirements.txt` 增加 `httpx[http2]`

### 对比上一版本
| 项目 | v0.9.0 | v0.10.0 |
|------|--------|---------|
| 对话历史 | Agent 内部 list | 独立 Memory 模块 |
| REPL 多轮 | 同一 Agent 实例累积 messages | 不变，底层走 Memory |
| API 调用 | 单线路 | 主备自动切换，成功后 sticky |

---

## [0.9.0] - 2026-07-30

新增时间工具，完成第 3 个工具的注册接入。

### 新增
- `tools/time_tool.py`：`get_time` 工具，返回当前日期时间与星期
- `examples/README.md` 补充手动注册 vs 装饰器注册对比说明

### 变更
- `agent/core.py` system prompt 增加时间工具调用规则
- `tools/registry.py` 注册 `time_tool` 模块

### 对比上一版本
| 项目 | v0.8.0 | v0.9.0 |
|------|--------|--------|
| 内置工具 | 天气、计算器 | + 时间查询 |
| 工具总数 | 2 | 3 |

---

## [0.8.0] - 2026-07-30

工具自动注册：`@register_tool` 装饰器替代手动维护注册表。

### 新增
- `tools/registry.py` 新增 `@register_tool` 装饰器
- 工具模块 import 时自动注册，`TOOL_SCHEMAS` / `AVAILABLE_TOOLS` 自动生成

### 变更
- `tools/weather.py`、`tools/calculator.py` 改用装饰器注册，移除独立 `TOOL_SCHEMA`
- 新增工具只需：写函数 + `@register_tool` + 在 `registry.py` 末尾 import

### 对比上一版本
| 项目 | v0.7.0 | v0.8.0 |
|------|--------|--------|
| 工具注册 | 手动维护两个列表 | 装饰器自动注册 |
| 新增工具 | 改 3 处 | 改 2 处（工具文件 + 一行 import） |

---

## [0.7.0] - 2026-07-30

计算器工具增强：支持任意简单数学表达式计算。

### 变更
- `tools/calculator.py`：由硬编码字典改为 `eval` 动态计算
- 自动去除表达式空格，支持 `2 * 3` 与 `2*3`
- 增加字符白名单校验，拒绝非法输入

### 对比上一版本
| 项目 | v0.6.0 | v0.7.0 |
|------|--------|--------|
| 计算范围 | 仅预设式子（如 2*2） | 任意数字表达式（如 3*203） |
| 带空格表达式 | 不支持 | 支持 |

---

## [0.6.0] - 2026-07-30

新增多轮对话 REPL：同一 Agent 实例可连续提问，上下文自动保留。

### 新增
- 无命令行参数时进入交互模式，持续接收用户输入
- 输入 `quit` 退出 REPL

### 对比上一版本
| 项目 | v0.5.0 | v0.6.0 |
|------|--------|--------|
| 运行模式 | 单次问答 | 单次问答 + 多轮 REPL |
| 上下文 | 单次 run 内保留 | 多轮 run 间保留 |

---

## [0.5.0] - 2026-07-30

Framework 易用性提升：支持命令行传参，`run()` 返回最终答案。

### 新增
- `main.py` 支持命令行传入问题：`python main.py 北京天气怎么样`
- `Agent.run()` 返回模型最终回答（`return message.content`）

### 对比上一版本
| 项目 | v0.4.1 | v0.5.0 |
|------|--------|--------|
| 提问方式 | 写死在代码里 | 命令行参数传入 |
| `run()` 返回值 | 无（仅 print） | 返回最终答案字符串 |

---

## [0.4.1] - 2026-07-30

项目清理：归档旧示例脚本，根目录只保留 Framework 入口。

### 变更
- 将 `demo.py`、`agent.py`、`agent_loop.py` 移至 `examples/` 目录
- 新增 `examples/README.md` 说明各示例用途与运行方式
- 更新 `README.md` 项目结构与运行说明
- 补全 `.env.example` 中的 `MODEL` 配置项

### 对比上一版本
| 项目 | v0.4.0 | v0.4.1 |
|------|--------|--------|
| 根目录脚本 | Framework + 旧示例混杂 | 仅 `main.py` 入口 |
| 学习示例 | 散落在根目录 | 统一在 `examples/` |

---

## [0.4.0] - 2026-07-30

小型 Agent Framework 初版：配置层、Agent 核心、程序入口三层分离。

### 新增
- `config/settings.py`：集中管理 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`MODEL`、`client`
- `agent/core.py`：`Agent` 类，封装 Agent Loop（问模型 → 调工具 → 再问模型）
- `agent/__init__.py`：导出 `Agent` 类
- `main.py`：程序入口，通过 `agent.run()` 发起对话
- `CHANGELOG.md`：版本更新日志

### 变更
- 更新 `README.md`：补充项目结构、模块职责、架构进度
- `agent_loop.py`：引入 `config.settings` 中的 `MODEL`（保留作学习参考）

### 对比上一版本
| 项目 | v0.3.1 | v0.4.0 |
|------|--------|--------|
| 配置管理 | 散落在各脚本 | `config/settings.py` 统一管理 |
| Agent 逻辑 | 写在 `agent_loop.py` | 封装为 `Agent` 类 |
| 启动方式 | `python agent_loop.py` | `python main.py`（推荐） |
| 项目定位 | Demo + 工具模块 | 小型 Agent Framework |

---

## [0.3.1] - 2026-07-30

**Commit:** `f036c4b`

### 变更
- `agent_loop.py` 改为从 `tools` 模块导入 `TOOL_SCHEMAS` 和 `execute_tool`
- 移除 `agent_loop.py` 内联的工具定义与注册表（约 90 行）

### 对比上一版本
| 项目 | v0.3.0 | v0.3.1 |
|------|--------|--------|
| 工具定义位置 | `agent_loop.py` 内部 | `tools/` 模块 |
| 新增工具方式 | 改 agent_loop | 改 tools + registry |

---

## [0.3.0] - 2026-07-30

**Commit:** `cb5da83`

### 新增
- `tools/` 工具模块
  - `weather.py`：天气查询工具
  - `calculator.py`：数学表达式计算工具
  - `registry.py`：工具注册表与 `execute_tool` 调度
  - `__init__.py`：对外统一导出

### 对比上一版本
| 项目 | v0.2.1 | v0.3.0 |
|------|--------|--------|
| 工具组织 | 无独立模块 | `tools/` 模块化 |
| Agent Loop | 无 | 有（`agent_loop.py`） |
| 支持工具 | 无 | 天气、计算器 |

---

## [0.2.1] - 2026-07-30

**Commit:** `e147e30`

### 修复
- 更新 `.env.example` 中的 `OPENAI_BASE_URL`
- 格式化 `demo.py` 代码风格

---

## [0.2.0] - 2026-07-29

**Commits:** `9423431`, `70e9c55`

### 新增
- `README.md` 项目文档（安装、配置、运行说明）
- `requirements.txt` 锁定依赖版本

### 变更
- `openai==2.50.0`
- `python-dotenv==1.2.2`

### 对比上一版本
| 项目 | v0.1.0 | v0.2.0 |
|------|--------|--------|
| 依赖管理 | 无版本锁定 | 有 `requirements.txt` |
| 文档 | 无 | 有 `README.md` |

---

## [0.1.0] - 2026-07-29

**Commit:** `7652e41`

### 新增
- 项目初始化
- `demo.py`：最简 OpenAI 对话示例
- `.env` + `.env.example`：API Key 环境变量隔离
- `.gitignore`：忽略 `.env`、`.venv`

### 功能
- 支持自定义 `base_url`（OpenAI 兼容接口）
- 通过 `python-dotenv` 加载环境变量

---

## 版本演进路线

```text
v0.1.0  最简 Demo（对话）
  ↓
v0.2.0  工程化（依赖锁定 + 文档）
  ↓
v0.3.0  工具模块化（tools/）
  ↓
v0.3.1  agent_loop 接入 tools
  ↓
v0.4.0  Agent Framework（config + agent + main）
  ↓
v0.4.1  归档旧示例到 examples/
  ↓
v0.5.0  命令行传参 + run 返回值
  ↓
v0.6.0  多轮对话 REPL
  ↓
v0.7.0  计算器增强
  ↓
v0.8.0  工具自动注册（@register_tool）
  ↓
v0.9.0  新增时间工具
  ↓
v0.10.0 对话记忆模块（Memory）
  ↓
v1.0.0  [计划] 首个完整 Framework 版本
```

## 如何查看某个版本的代码

```bash
# 查看所有版本标签（未来打 tag 后可用）
git tag

# 查看某次提交的代码
git show cb5da83

# 切换到某次提交（只读，detached 状态）
git checkout f036c4b
```

## 发布新版本时

1. 在本文件顶部 `[未发布]` 区域写好变更内容
2. 将 `[未发布]` 改为 `[x.y.z] - 日期`
3. 提交并推送：

```bash
git add CHANGELOG.md
git commit -m "docs: 发布 v0.x.x 版本说明"
git push
```

4. （可选）打 Git 标签：

```bash
git tag -a v0.4.0 -m "v0.4.0: Agent Framework 配置层"
git push origin v0.4.0
```
