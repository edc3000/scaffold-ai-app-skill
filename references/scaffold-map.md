# Production AI App Scaffold Map

Use this reference when adapting the default scaffold. The structure is based on the user's image and preserves separate ownership for product logic, AI logic, safety, evaluation, observability, and deployment.

```text
production-ai-app/
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   ├── config.py               # Environment and settings
│   ├── models.py               # Shared data models
│   ├── Dockerfile              # Backend container
│   ├── components/
│   │   ├── hybrid_retriever.py # Hybrid search adapter
│   │   └── reranker.py         # Reranking adapter
│   ├── services/
│   │   ├── rag_pipeline.py     # Core orchestration
│   │   ├── semantic_cache.py   # Cache interface
│   │   ├── conversation.py     # Conversation state
│   │   ├── query_rewriter.py   # Query rewriting
│   │   └── query_router.py     # Routing logic
│   ├── prompts/
│   │   ├── schema.py           # Typed prompt contracts
│   │   ├── templates.py        # Prompt templates
│   │   └── registry.py         # Versioned prompt lookup
│   ├── agents/
│   │   ├── document_grader.py  # Relevance grading
│   │   ├── query_decomposer.py # Query planning
│   │   ├── adaptive_router.py  # Tool/model route selection
│   │   └── tools/vector_search.py
│   ├── tools/
│   │   ├── web_search.py       # Web search tool adapter
│   │   └── code_search.py      # Code search tool adapter
│   └── security/
│       ├── input_guard.py      # Input policy checks
│       ├── content_filter.py   # Content policy checks
│       └── output_filter.py    # Output policy checks
├── evaluation/
│   ├── golden_dataset.json     # Golden examples
│   ├── offline_eval.py         # Offline evaluation runner
│   ├── online_monitor.py       # Online quality monitor
│   └── eval_results/           # Evaluation outputs
├── observability/
│   ├── events.py               # trace_id/query_id event contracts
│   ├── tracer.py               # Per-stage tracing
│   ├── feedback.py             # Feedback capture linked to trace IDs
│   └── cost_tracker.py         # Per-query cost breakdown
├── data/
│   ├── raw/
│   ├── processed/
│   └── index_config/
├── scripts/
│   ├── seed.py
│   ├── migrate.py
│   └── healthcheck.py
├── frontend/
│   ├── app.py
│   ├── static/
│   ├── requirements.txt
│   └── Dockerfile
├── tests/
│   ├── test_retrieval.py
│   ├── test_cache.py
│   └── test_routing.py
├── docs/
│   ├── architecture.md
│   ├── api-reference.md
│   └── deployment.md
├── .codex/rules/
│   ├── code-style.md
│   └── testing.md
├── .claude/
│   ├── context.md
│   └── rules.md
├── AGENTS.md
├── CLAUDE.md
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

Keep these boundaries intact unless the user asks for a smaller scaffold. The point of the scaffold is to make production concerns visible from day one without forcing implementation details too early.
