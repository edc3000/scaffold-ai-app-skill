# Scaffold AI App Skill

让 Codex 用一句话把空目录变成一个有生产架构感的 AI 应用脚手架。

`scaffold-ai-app` 给 Codex 一套可复用的现代 AI 应用蓝图：RAG 服务、语义缓存、记忆、查询重写、路由、版本化 prompt、自检 agent、可插拔工具、三层安全防护、评测、可观测性、数据管线、测试、文档、容器化，以及 AI 编码助手上下文。它适合用在原型快要变成真实系统的时候，因为这时只靠一个 `main.py` 已经不够了。

English documentation: [README.md](./README.md)

## 安装

使用 open skills CLI 安装：

```bash
npx skills add https://github.com/edc3000/scaffold-ai-app-skill --skill scaffold-ai-app
```

这个命令会读取公开 GitHub 仓库，找到 `scaffold-ai-app` 这个 skill，并安装到当前检测到的 agent 环境中。

如果 Codex 的 skill 列表还没有刷新，重启 Codex 或开启一个新会话。

## 如何触发这个 Skill

在 Codex 中显式调用：

```text
Use $scaffold-ai-app to create a production-ready AI app scaffold at ./production-ai-app.
```

也可以用自然语言描述目标：

```text
创建一个新的 RAG/agent 应用脚手架，需要 services、prompts、agents、安全、评测、可观测性、文档和部署文件。
```

适合触发它的表达包括：

- 搭建一个生产级 AI 应用脚手架
- 创建一个 RAG 应用骨架
- 初始化一个 agent 应用
- 组织一个 FastAPI AI 项目结构
- 从一开始就加入 evaluation、observability、prompts、agents、security 等层

## 它会生成什么

默认脚手架包含：

- `app/`：FastAPI 入口、配置、schema、检索组件、五层 service、agents、tools、安全过滤。
- `app/prompts/`：类型化、版本化的 prompt schema、模板和注册表，避免在 service 逻辑里硬编码 prompt。
- `evaluation/`：黄金数据集、离线评测、在线监控和结果目录。
- `observability/`：统一的 `trace_id` / `query_id` 契约、链路追踪、反馈和成本统计。
- `.claude/` 和 `.codex/`：AI 编码助手上下文和规则。
- `data/`、`scripts/`、`frontend/`、`tests/`、`docs/`、`Dockerfile`、`docker-compose.yml`。

## 示例请求

```text
Use $scaffold-ai-app to create a project named customer-support-ai in ./customer-support-ai. Keep the default production layers and make the README describe a support-ticket RAG assistant.
```

Codex 会使用这个 skill 生成脚手架，并根据你描述的项目方向调整占位文件。
