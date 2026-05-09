# Scaffold AI App Skill

Turn a blank folder into a production-shaped AI application skeleton in one Codex request.

`scaffold-ai-app` gives Codex a reusable blueprint for modern AI apps: RAG services, semantic cache, memory, query rewriting, routing, versioned prompts, self-checking agents, pluggable tools, three-layer safety, evaluation, observability, data pipelines, tests, docs, containers, and coding-agent context. It is meant for the moment when a prototype is about to become a real system and `main.py` is no longer enough.

中文说明：[README.zh-CN.md](./README.zh-CN.md)

## Install

Install the skill with the open skills CLI:

```bash
npx skills add https://github.com/edc3000/scaffold-ai-app-skill --skill scaffold-ai-app
```

This reads the public GitHub repository, finds the `scaffold-ai-app` skill, and installs it for your detected agent environment.

Restart Codex or start a new session if the skill list has not refreshed.

## Trigger The Skill

Use the skill explicitly in Codex:

```text
Use $scaffold-ai-app to create a production-ready AI app scaffold at ./production-ai-app.
```

You can also describe the goal naturally:

```text
Create a new RAG/agent application scaffold with services, prompts, agents, safety, evals, observability, docs, and deployment files.
```

Good trigger phrases include:

- scaffold a production AI app
- create a RAG app skeleton
- bootstrap an agent application
- structure a FastAPI AI project
- add evaluation, observability, prompts, agents, and security layers from the start

## What It Generates

The default scaffold includes:

- `app/`: FastAPI entrypoint, config, schemas, retrieval components, five service layers, agents, tools, and security filters.
- `app/prompts/`: typed, versioned prompt schema, templates, and registry so prompt text stays out of service logic.
- `evaluation/`: golden dataset, offline evaluation, online monitor, and result folder.
- `observability/`: shared `trace_id` / `query_id` contracts, tracing, feedback, and cost tracking.
- `.claude/` and `.codex/`: coding-agent context and rules.
- `data/`, `scripts/`, `frontend/`, `tests/`, `docs/`, `Dockerfile`, and `docker-compose.yml`.

## Example Request

```text
Use $scaffold-ai-app to create a project named customer-support-ai in ./customer-support-ai. Keep the default production layers and make the README describe a support-ticket RAG assistant.
```

Codex will use the skill, generate the scaffold, and adapt the placeholder files to the project you described.
