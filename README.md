# Applied Software Engineering Practice

A Python workspace for small, test-driven applied software engineering exercises: APIs, data validation, functional pipelines, and related design work.

Each exercise lives as its own package under `src/`, with matching tests under `tests/`. The first package here is `kitchen_prep` (kitchen order prep-time estimation); more exercises can be added the same way.

## Requirements

- Python 3.11 or later
- [uv](https://docs.astral.sh/uv/)

## Setup

From the repository root:

```bash
uv sync --group dev
```

## Run tests

```bash
uv run pytest
```

## Packages

### `kitchen_prep`

Estimates kitchen order preparation times.

- `estimate_prep_time` — single-order estimate
- `estimate_prep_time_with_predictor` — same response shape with a pluggable predictor
- `estimate_prep_time_batch` / `aggregate_batch` / `format_batch_report` — multi-order helpers

Example:

```python
from kitchen_prep import estimate_prep_time

result = estimate_prep_time(
    {
        "order_id": "order-123",
        "items": [
            {"sku": "burger", "qty": 2, "prep_minutes": 8},
            {"sku": "fries", "qty": 1, "prep_minutes": 4},
        ],
        "kitchen_load": 3,
    }
)

print(result["estimate_minutes"])
```

## Project layout

```text
src/                Exercise packages (e.g. kitchen_prep/)
tests/              Pytest suites for each package
pyproject.toml      Project metadata and tool configuration
```
