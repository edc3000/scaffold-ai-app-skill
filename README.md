# Scaffold AI App Skill

`scaffold-ai-app` is a Codex skill for generating a production-oriented AI application scaffold. It is based on a nine-layer AI app layout: API entrypoints, retrieval components, service orchestration, versioned prompts, agents, tools, security filters, evaluation, observability, data, tests, docs, deployment files, and coding-agent context.

Chinese documentation: [README.zh-CN.md](./README.zh-CN.md)

## Install

Install directly from GitHub with `npx`:

```bash
npx github:edc3000/scaffold-ai-app-skill
```

This copies the skill into:

```bash
${CODEX_HOME:-$HOME/.codex}/skills/scaffold-ai-app
```

Replace an existing local copy:

```bash
npx github:edc3000/scaffold-ai-app-skill --force
```

Install to a custom directory:

```bash
npx github:edc3000/scaffold-ai-app-skill --target /path/to/skills/scaffold-ai-app
```

If this package is later published to npm, the same installer can be run in the usual npm form:

```bash
npx scaffold-ai-app-skill
```

## Use In Codex

After installation, restart Codex or start a new session if the skill list has not refreshed. Then ask Codex something like:

```text
Use $scaffold-ai-app to create a production-ready AI app scaffold at ./production-ai-app.
```

## Use The Generator Directly

You can also run the bundled generator:

```bash
python3 ~/.codex/skills/scaffold-ai-app/scripts/create_scaffold.py ./production-ai-app --name production-ai-app
```

Useful options:

```bash
python3 ~/.codex/skills/scaffold-ai-app/scripts/create_scaffold.py ./my-ai-app --name my-ai-app --no-frontend
python3 ~/.codex/skills/scaffold-ai-app/scripts/create_scaffold.py ./my-ai-app --name my-ai-app --force
```

The script refuses to write into a non-empty directory unless `--force` or `--overwrite` is passed. `--force` fills missing files without replacing existing files; `--overwrite` replaces existing files.

## Generated Structure

The default scaffold includes:

- `app/`: FastAPI entrypoint, config, schemas, retrieval components, five service layers, prompts, agents, tools, and security filters.
- `app/prompts/`: typed, versioned prompt schema, templates, and registry.
- `evaluation/`: golden dataset, offline evaluation, online monitor, and result folder.
- `observability/`: shared `trace_id` / `query_id` contracts, tracing, feedback, and cost tracking.
- `.claude/` and `.codex/`: coding-agent context and rules.
- `data/`, `scripts/`, `frontend/`, `tests/`, and `docs/`.

## Validate A Generated Project

```bash
python3 -m compileall -q ./production-ai-app
PYTHONPATH=./production-ai-app python3 -c "from app.prompts.registry import get_prompt; print(get_prompt('query-routing').version)"
```
