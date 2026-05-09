---
name: scaffold-ai-app
description: Create production-oriented AI application project scaffolds inspired by the production-ai-app layout. Use when a user asks to initialize, scaffold, bootstrap, or structure a new AI agent/RAG/FastAPI project with directories for app entrypoints, retrieval, services, prompts, agents, tools, security, evaluation, observability, data, scripts, frontend, tests, docs, deployment, .claude context, and coding-agent context.
---

# Scaffold AI App

## Overview

Use this skill to create a clean starting structure for production-minded AI applications. Prefer the bundled script for new projects, then adapt the generated placeholders to the user's framework, model provider, retrieval stack, and deployment target.

## Workflow

1. Confirm or infer the destination path, project name, and stack. If unspecified, use the current working directory plus a hyphen-case project name.
2. Run `scripts/create_scaffold.py` to generate the directory tree and placeholder files.
3. Read `references/scaffold-map.md` only when you need the full tree rationale or need to customize which layers to keep.
4. After generation, inspect the tree and adjust names, README, dependency files, Docker files, or agent instructions for the concrete project.

## Quick Start

From this skill directory:

```bash
python3 scripts/create_scaffold.py /path/to/production-ai-app --name production-ai-app
```

Common options:

```bash
python3 scripts/create_scaffold.py /path/to/my-ai-app --name my-ai-app --force
python3 scripts/create_scaffold.py /path/to/my-ai-app --name my-ai-app --no-frontend
```

Use `--force` only when the user explicitly wants to fill missing files in an existing directory. The script never overwrites existing files unless `--overwrite` is passed.

## Generated Shape

The default scaffold includes these layers:

- `app/`: FastAPI entrypoint, config, schemas, Dockerfile, retrieval components, five service layers, versioned prompt contracts, agents, tools, and security filters.
- `evaluation/`: golden data, offline/online runners, and result folder.
- `observability/`: shared trace/query event contracts plus tracing, feedback capture, and cost tracking.
- `data/`: raw, processed, and index configuration folders.
- `scripts/`: seed, migration, and healthcheck commands.
- `frontend/`: separate UI placeholder and container file.
- `tests/`: retrieval, cache, and routing test placeholders.
- `docs/`: architecture, API reference, and deployment guide placeholders.
- `.codex/rules/` and `.claude/`: agent context, code style, and testing notes for coding assistants.

## Adaptation Rules

- Keep the scaffold boring and navigable; create files that name responsibilities instead of pretending implementation exists.
- Preserve layer boundaries from the image: retrieval, services, prompts, agents, tools, security, evaluation, and observability should remain independently swappable.
- Keep prompts versioned, typed, and registry-driven. Do not hardcode prompt text inside service or agent modules.
- Thread `trace_id` and `query_id` through tracing, feedback, and cost records so production incidents can be reconstructed.
- If the user asks for a specific stack, update only the relevant generated files after scaffolding, for example `pyproject.toml`, `app/Dockerfile`, `frontend/package.json`, or docs.
- For minimal prototypes, remove entire layers only when the user asks for a smaller scaffold. Do not flatten everything into `app/main.py`.
- For existing repositories, inspect current files first and use `--force` without `--overwrite` to avoid clobbering user work.

## Validation

After scaffolding, run a lightweight check:

```bash
find /path/to/my-ai-app -maxdepth 3 -type f | sort
python3 -m py_compile /path/to/my-ai-app/app/*.py /path/to/my-ai-app/app/**/*.py
```

If the shell does not expand `**`, compile with a short Python walk instead.
