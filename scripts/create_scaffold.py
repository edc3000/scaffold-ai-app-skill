#!/usr/bin/env python3
"""Create a production-oriented AI app scaffold."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "production-ai-app"


def titleize(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-") if part)


def py_module_stub(name: str, description: str) -> str:
    return f'"""{description}."""\n\n\nclass {name}:\n    """Placeholder boundary for {description.lower()}."""\n\n    pass\n'


def prompt_schema_module() -> str:
    return '''"""Typed prompt registry contracts."""

from dataclasses import dataclass
from typing import Literal

PromptKind = Literal["system", "routing", "grading", "rewriting"]


@dataclass(frozen=True)
class PromptSpec:
    key: str
    kind: PromptKind
    version: str
    template: str
    owner: str = "ai-platform"
'''


def prompt_templates_module() -> str:
    return '''SYSTEM_PROMPT_V1 = "You are a helpful AI assistant."
ROUTING_PROMPT_V1 = "Choose the smallest reliable route for the user request."
GRADING_PROMPT_V1 = "Grade whether the retrieved document is relevant to the query."
REWRITING_PROMPT_V1 = "Rewrite the query for retrieval while preserving intent."
'''


def prompt_registry_module() -> str:
    return '''"""Versioned, typed, hot-swappable prompt registry."""

from app.prompts.schema import PromptSpec
from app.prompts.templates import (
    GRADING_PROMPT_V1,
    REWRITING_PROMPT_V1,
    ROUTING_PROMPT_V1,
    SYSTEM_PROMPT_V1,
)

PROMPT_REGISTRY: dict[tuple[str, str], PromptSpec] = {
    ("default-system", "v1"): PromptSpec(
        key="default-system",
        kind="system",
        version="v1",
        template=SYSTEM_PROMPT_V1,
    ),
    ("query-routing", "v1"): PromptSpec(
        key="query-routing",
        kind="routing",
        version="v1",
        template=ROUTING_PROMPT_V1,
    ),
    ("document-grading", "v1"): PromptSpec(
        key="document-grading",
        kind="grading",
        version="v1",
        template=GRADING_PROMPT_V1,
    ),
    ("query-rewriting", "v1"): PromptSpec(
        key="query-rewriting",
        kind="rewriting",
        version="v1",
        template=REWRITING_PROMPT_V1,
    ),
}


def get_prompt(key: str, version: str = "v1") -> PromptSpec:
    return PROMPT_REGISTRY[(key, version)]
'''


def observability_events_module() -> str:
    return '''"""Shared observability event contracts."""

from dataclasses import dataclass, field
from time import time


@dataclass(frozen=True)
class TraceContext:
    trace_id: str
    query_id: str
    stage: str = "request"


@dataclass(frozen=True)
class FeedbackEvent:
    trace_id: str
    query_id: str
    rating: int
    comment: str = ""
    created_at: float = field(default_factory=time)


@dataclass(frozen=True)
class CostEvent:
    trace_id: str
    query_id: str
    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    created_at: float = field(default_factory=time)
'''


def tracer_module() -> str:
    return '''"""Per-stage tracing with trace_id/query_id propagation."""

from typing import Optional
from uuid import uuid4

from observability.events import TraceContext


class Tracer:
    def start_query(self, query_id: Optional[str] = None) -> TraceContext:
        return TraceContext(trace_id=str(uuid4()), query_id=query_id or str(uuid4()))

    def stage(self, context: TraceContext, stage: str) -> TraceContext:
        return TraceContext(trace_id=context.trace_id, query_id=context.query_id, stage=stage)
'''


def feedback_module() -> str:
    return '''"""Feedback capture linked to trace IDs."""

from observability.events import FeedbackEvent, TraceContext


class FeedbackCollector:
    def __init__(self) -> None:
        self.events: list[FeedbackEvent] = []

    def record(self, context: TraceContext, rating: int, comment: str = "") -> FeedbackEvent:
        event = FeedbackEvent(
            trace_id=context.trace_id,
            query_id=context.query_id,
            rating=rating,
            comment=comment,
        )
        self.events.append(event)
        return event
'''


def cost_tracker_module() -> str:
    return '''"""Per-query cost tracking linked to trace IDs."""

from observability.events import CostEvent, TraceContext


class CostTracker:
    def __init__(self) -> None:
        self.events: list[CostEvent] = []

    def record(
        self,
        context: TraceContext,
        provider: str,
        model: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost_usd: float = 0.0,
    ) -> CostEvent:
        event = CostEvent(
            trace_id=context.trace_id,
            query_id=context.query_id,
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost_usd,
        )
        self.events.append(event)
        return event
'''


def files(project_name: str, include_frontend: bool) -> dict[str, str]:
    title = titleize(project_name)
    base: dict[str, str] = {
        ".env.example": "APP_ENV=development\nLOG_LEVEL=INFO\nOPENAI_API_KEY=\nVECTOR_STORE_URL=\n",
        "README.md": f"# {title}\n\nProduction-oriented AI application scaffold.\n\n## Layout\n\n- `app/`: API, retrieval, five service layers, versioned prompts, agents, tools, and safety layers.\n- `evaluation/`: golden data and offline/online evaluation runners.\n- `observability/`: shared trace/query event contracts, feedback, and cost tracking.\n- `.claude/` and `.codex/`: coding-agent project context and rules.\n- `data/`: raw data, processed data, and index config.\n- `tests/`: focused tests for retrieval, cache, and routing.\n",
        "pyproject.toml": f"[build-system]\nrequires = [\"setuptools>=68\"]\nbuild-backend = \"setuptools.build_meta\"\n\n[project]\nname = \"{project_name}\"\nversion = \"0.1.0\"\ndescription = \"Production-oriented AI application\"\nrequires-python = \">=3.9\"\ndependencies = [\n    \"fastapi>=0.110\",\n    \"uvicorn[standard]>=0.27\",\n    \"pydantic>=2\",\n    \"pydantic-settings>=2\",\n]\n\n[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\n",
        "docker-compose.yml": "services:\n  api:\n    build:\n      context: .\n      dockerfile: app/Dockerfile\n    env_file: .env\n    ports:\n      - \"8000:8000\"\n",
        "AGENTS.md": "# Agent Instructions\n\nKeep retrieval, services, prompts, agents, tools, security, evaluation, and observability as separate layers. Prefer small, testable changes and update docs when contracts move.\n",
        "CLAUDE.md": "# Claude Context\n\nStart with `.claude/context.md`, then follow AGENTS.md for shared coding-agent rules. Use tests and docs as the source of truth when changing behavior.\n",
        ".claude/context.md": "# Claude Project Context\n\nThis codebase is a layered AI application. Keep services, agents, prompts, security, evaluation, and observability independently replaceable.\n\nAlways preserve trace_id and query_id across request handling, feedback, and cost records.\n",
        ".claude/rules.md": "# Claude Rules\n\nDo not hardcode prompts in service or agent logic. Use `app/prompts/registry.py` and version prompt changes.\n",
        ".codex/rules/code-style.md": "# Code Style\n\nUse typed Python, explicit boundaries, and concise comments only where they clarify non-obvious logic.\n",
        ".codex/rules/testing.md": "# Testing\n\nAdd focused tests for routing, retrieval, caching, safety filters, and evaluation contracts.\n",
        "app/__init__.py": "",
        "app/main.py": "from fastapi import FastAPI\n\napp = FastAPI(title=\"Production AI App\")\n\n\n@app.get(\"/health\")\ndef health() -> dict[str, str]:\n    return {\"status\": \"ok\"}\n",
        "app/config.py": "from pydantic_settings import BaseSettings\n\n\nclass Settings(BaseSettings):\n    app_env: str = \"development\"\n    log_level: str = \"INFO\"\n\n\nsettings = Settings()\n",
        "app/models.py": "from pydantic import BaseModel\n\n\nclass QueryRequest(BaseModel):\n    query: str\n\n\nclass QueryResponse(BaseModel):\n    answer: str\n    sources: list[str] = []\n",
        "app/Dockerfile": "FROM python:3.11-slim\nWORKDIR /app\nCOPY pyproject.toml README.md ./\nCOPY app ./app\nRUN pip install --no-cache-dir .\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n",
        "app/components/__init__.py": "",
        "app/components/hybrid_retriever.py": py_module_stub("HybridRetriever", "Hybrid search retrieval adapter"),
        "app/components/reranker.py": py_module_stub("Reranker", "Reranking adapter"),
        "app/services/__init__.py": "",
        "app/services/rag_pipeline.py": py_module_stub("RagPipeline", "RAG pipeline orchestration"),
        "app/services/semantic_cache.py": py_module_stub("SemanticCache", "Semantic cache interface"),
        "app/services/conversation.py": py_module_stub("ConversationService", "Conversation state management"),
        "app/services/query_rewriter.py": py_module_stub("QueryRewriter", "Query rewriting"),
        "app/services/query_router.py": py_module_stub("QueryRouter", "Query routing"),
        "app/prompts/__init__.py": "",
        "app/prompts/schema.py": prompt_schema_module(),
        "app/prompts/templates.py": prompt_templates_module(),
        "app/prompts/registry.py": prompt_registry_module(),
        "app/agents/__init__.py": "",
        "app/agents/document_grader.py": py_module_stub("DocumentGrader", "Document relevance grading"),
        "app/agents/query_decomposer.py": py_module_stub("QueryDecomposer", "Query decomposition"),
        "app/agents/adaptive_router.py": py_module_stub("AdaptiveRouter", "Adaptive model and tool routing"),
        "app/agents/tools/__init__.py": "",
        "app/agents/tools/vector_search.py": py_module_stub("VectorSearchTool", "Vector search tool"),
        "app/tools/__init__.py": "",
        "app/tools/web_search.py": py_module_stub("WebSearchTool", "Web search tool"),
        "app/tools/code_search.py": py_module_stub("CodeSearchTool", "Code search tool"),
        "app/security/__init__.py": "",
        "app/security/input_guard.py": py_module_stub("InputGuard", "Input safety checks"),
        "app/security/content_filter.py": py_module_stub("ContentFilter", "Content filtering"),
        "app/security/output_filter.py": py_module_stub("OutputFilter", "Output safety checks"),
        "evaluation/golden_dataset.json": "[]\n",
        "evaluation/offline_eval.py": "def main() -> None:\n    print(\"offline evaluation placeholder\")\n\n\nif __name__ == \"__main__\":\n    main()\n",
        "evaluation/online_monitor.py": "def main() -> None:\n    print(\"online monitor placeholder\")\n\n\nif __name__ == \"__main__\":\n    main()\n",
        "observability/__init__.py": "",
        "observability/events.py": observability_events_module(),
        "observability/tracer.py": tracer_module(),
        "observability/feedback.py": feedback_module(),
        "observability/cost_tracker.py": cost_tracker_module(),
        "scripts/seed.py": "def main() -> None:\n    print(\"seed placeholder\")\n\n\nif __name__ == \"__main__\":\n    main()\n",
        "scripts/migrate.py": "def main() -> None:\n    print(\"migration placeholder\")\n\n\nif __name__ == \"__main__\":\n    main()\n",
        "scripts/healthcheck.py": "import urllib.request\n\n\ndef main() -> None:\n    with urllib.request.urlopen(\"http://127.0.0.1:8000/health\", timeout=5) as response:\n        print(response.read().decode())\n\n\nif __name__ == \"__main__\":\n    main()\n",
        "tests/test_retrieval.py": "def test_retrieval_placeholder() -> None:\n    assert True\n",
        "tests/test_cache.py": "def test_cache_placeholder() -> None:\n    assert True\n",
        "tests/test_routing.py": "def test_routing_placeholder() -> None:\n    assert True\n",
        "docs/architecture.md": f"# {title} Architecture\n\nDocument the request flow, retrieval path, agent decisions, security checks, evaluation loop, and observability events.\n",
        "docs/api-reference.md": "# API Reference\n\nStart with `/health`, then document user-facing routes as they are added.\n",
        "docs/deployment.md": "# Deployment\n\nDocument runtime environment variables, container build steps, and release checks.\n",
    }
    if include_frontend:
        base.update(
            {
                "frontend/app.py": "def main() -> None:\n    print(\"frontend placeholder\")\n\n\nif __name__ == \"__main__\":\n    main()\n",
                "frontend/requirements.txt": "",
                "frontend/Dockerfile": "FROM python:3.11-slim\nWORKDIR /frontend\nCOPY frontend ./frontend\nCMD [\"python\", \"frontend/app.py\"]\n",
                "frontend/static/.gitkeep": "",
            }
        )
    return base


def dirs(include_frontend: bool) -> list[str]:
    values = [
        "data/raw",
        "data/processed",
        "data/index_config",
        "evaluation/eval_results",
    ]
    if include_frontend:
        values.append("frontend/static")
    return values


def write_file(path: Path, content: str, overwrite: bool) -> bool:
    if path.exists() and not overwrite:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a production AI app scaffold.")
    parser.add_argument("target", type=Path, help="Destination project directory")
    parser.add_argument("--name", help="Project name. Defaults to target directory name.")
    parser.add_argument("--force", action="store_true", help="Allow creating files in an existing directory.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files. Use carefully.")
    parser.add_argument("--no-frontend", action="store_true", help="Skip the frontend placeholder.")
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    project_name = slugify(args.name or target.name)
    include_frontend = not args.no_frontend

    if target.exists() and any(target.iterdir()) and not args.force and not args.overwrite:
        raise SystemExit(f"Refusing to write into non-empty directory without --force: {target}")

    target.mkdir(parents=True, exist_ok=True)
    for directory in dirs(include_frontend):
        (target / directory).mkdir(parents=True, exist_ok=True)

    created = 0
    skipped = 0
    for relative, content in sorted(files(project_name, include_frontend).items()):
        if write_file(target / relative, content, args.overwrite):
            created += 1
        else:
            skipped += 1

    print(f"Created scaffold at {target}")
    print(f"Project name: {project_name}")
    print(f"Files created: {created}")
    if skipped:
        print(f"Files skipped: {skipped}")


if __name__ == "__main__":
    main()
