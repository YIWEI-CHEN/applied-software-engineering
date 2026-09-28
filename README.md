# Applied Software Engineering practice

Atoms ASE-style drills (FP + API), starting with kitchen prep-time estimation.

## Setup (uv)

```bash
cd C:\Users\yiweichen\VSCode_Projects\applied-software-engineering
uv sync --group dev
```

## Run tests

```bash
uv run pytest -q
```

Implement `estimate_prep_time` in `src/kitchen_prep/api.py`.
Rules are in that function docstring and mirrored by tests.
