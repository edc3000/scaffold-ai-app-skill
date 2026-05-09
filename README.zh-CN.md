# Scaffold AI App Skill

`scaffold-ai-app` 是一个 Codex skill，用来生成偏生产级的 AI 应用项目脚手架。它参考了常见的 9 层 AI 生产架构：API 入口、检索组件、业务服务、版本化 prompt、agent、工具、安全过滤、评测、可观测性、数据、测试、文档、部署文件，以及 AI 编码助手上下文。

英文文档见：[README.md](./README.md)

## 安装

从 GitHub 直接用 `npx` 安装：

```bash
npx github:edc3000/scaffold-ai-app-skill
```

安装器会把 skill 复制到：

```bash
${CODEX_HOME:-$HOME/.codex}/skills/scaffold-ai-app
```

如果本地已经有旧版本，可以覆盖安装：

```bash
npx github:edc3000/scaffold-ai-app-skill --force
```

也可以安装到自定义目录：

```bash
npx github:edc3000/scaffold-ai-app-skill --target /path/to/skills/scaffold-ai-app
```

如果后续把这个包发布到 npm，也可以使用最常规的 npm 包安装方式：

```bash
npx scaffold-ai-app-skill
```

## 在 Codex 中使用

安装后，如果 Codex 的 skill 列表还没有刷新，重启 Codex 或开启一个新会话。然后可以这样让 Codex 使用它：

```text
Use $scaffold-ai-app to create a production-ready AI app scaffold at ./production-ai-app.
```

## 直接运行脚手架生成器

也可以直接运行 skill 内置的生成脚本：

```bash
python3 ~/.codex/skills/scaffold-ai-app/scripts/create_scaffold.py ./production-ai-app --name production-ai-app
```

常用参数：

```bash
python3 ~/.codex/skills/scaffold-ai-app/scripts/create_scaffold.py ./my-ai-app --name my-ai-app --no-frontend
python3 ~/.codex/skills/scaffold-ai-app/scripts/create_scaffold.py ./my-ai-app --name my-ai-app --force
```

脚本默认不会写入非空目录，除非传入 `--force` 或 `--overwrite`。其中 `--force` 只补齐缺失文件，不覆盖已有文件；`--overwrite` 会覆盖已有文件，使用时要谨慎。

## 生成的项目结构

默认会生成：

- `app/`：FastAPI 入口、配置、schema、检索组件、五层 service、prompts、agents、tools、安全过滤。
- `app/prompts/`：类型化、版本化的 prompt schema、模板和注册表。
- `evaluation/`：黄金数据集、离线评测、在线监控和结果目录。
- `observability/`：统一的 `trace_id` / `query_id` 契约、链路追踪、反馈和成本统计。
- `.claude/` 和 `.codex/`：AI 编码助手上下文和规则。
- `data/`、`scripts/`、`frontend/`、`tests/`、`docs/`。

## 校验生成项目

```bash
python3 -m compileall -q ./production-ai-app
PYTHONPATH=./production-ai-app python3 -c "from app.prompts.registry import get_prompt; print(get_prompt('query-routing').version)"
```
