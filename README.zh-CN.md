# Scaffold AI App Skill

面向 Agent CLI 的生产级 AI 应用脚手架。用一句指令，把空目录变成一个可扩展、可维护、方便 AI 编码助手继续开发的项目骨架。

`scaffold-ai-app` 适用于 Codex、Claude Code 以及其他支持 skills / rules / project context 的 Agent CLI。它会生成一套 production-shaped AI app 结构，内置 FastAPI 入口、RAG 服务层、Agent、工具层、Prompt 版本管理、安全过滤、评测、可观测性、Docker、测试、文档，以及 `.codex` / `.claude` 编码助手上下文。

如果你正在从一个 `main.py` 原型走向真实项目，它可以帮你先把关键工程边界搭好，让后续功能开发、评测、部署和协作都有清晰落点。

## 为什么值得用

- **一句话生成完整骨架**：不用反复手写目录、占位文件、Docker、测试和文档入口。
- **为真实 AI 应用预留边界**：RAG、Agent、Prompt、Tools、Security、Evaluation、Observability 各自独立，后续替换实现更清楚。
- **适合 AI 编码助手继续接手**：内置 `.codex`、`.claude`、`AGENTS.md`、`CLAUDE.md`，让 Agent CLI 能快速理解项目约束。
- **默认安全不覆盖**：生成脚本默认不会覆盖已有文件，适合在空目录或已有项目中补齐缺失结构。

## 安装

使用 open skills CLI 安装：

```bash
npx skills add https://github.com/edc3000/scaffold-ai-app-skill --skill scaffold-ai-app
```

这个命令会从公开 GitHub 仓库读取 skill，并安装到当前检测到的 agent 环境中。

如果你的 Agent CLI 暂时不支持 open skills，也可以直接复用仓库里的生成脚本：

```bash
python3 scripts/create_scaffold.py ./my-ai-app --name my-ai-app
```

## 如何使用

在支持 skill 调用的 Agent CLI 中，可以显式调用：

```text
Use $scaffold-ai-app to create a production-ready AI app scaffold at ./production-ai-app.
```

也可以直接用自然语言描述目标：

```text
创建一个新的 RAG/Agent 应用脚手架，需要 FastAPI、services、prompts、agents、安全、评测、可观测性、文档和部署文件。
```

适合触发它的表达包括：

- 搭建一个生产级 AI 应用脚手架
- 创建一个 RAG 应用骨架
- 初始化一个 Agent 应用
- 组织一个 FastAPI AI 项目结构
- 从一开始就加入 evaluation、observability、prompts、agents、security 等层

## 默认生成内容

- `app/`：FastAPI 入口、配置、schema、检索组件、服务层、agents、tools 和安全过滤。
- `app/prompts/`：类型化、版本化的 prompt schema、模板和注册表，避免在 service 逻辑里硬编码 prompt。
- `evaluation/`：黄金数据集、离线评测、在线监控和结果目录。
- `observability/`：统一的 `trace_id` / `query_id` 契约、链路追踪、反馈和成本统计。
- `.claude/` 和 `.codex/`：面向 AI 编码助手的项目上下文和规则。
- `data/`、`scripts/`、`frontend/`、`tests/`、`docs/`、`app/Dockerfile` 和 `docker-compose.yml`。

## 示例请求

```text
Use $scaffold-ai-app to create a project named customer-support-ai in ./customer-support-ai. Keep the default production layers and make the README describe a support-ticket RAG assistant.
```

Agent CLI 会使用这个 skill 生成脚手架，并根据你描述的项目方向调整占位文件。
