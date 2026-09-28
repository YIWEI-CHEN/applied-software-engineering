"""Kitchen prep-time estimation API (ASE practice)."""

from __future__ import annotations

from typing import Any


def estimate_prep_time(raw: dict[str, Any]) -> dict[str, Any]:
    """Estimate prep minutes for one order payload.

    Expected input shape::

        {
          "order_id": "ord_123",
          "items": [
            {"sku": "burger", "qty": 2, "prep_minutes": 8},
            {"sku": "fries", "qty": 1, "prep_minutes": 4},
          ],
          "kitchen_load": 3,
          "ordered_at": "2026-09-28T14:00:00Z",  # optional for this exercise
        }

    Business rules:
    - Each item contributes ``prep_minutes * qty``.
    - ``items_total`` is the sum of item contributions (simplified additive model).
    - ``load_penalty = kitchen_load * 1`` minute; ``kitchen_load`` must be >= 0.
    - ``estimate_minutes = items_total + load_penalty``, and must be >= 1.
    - Reject missing ``order_id``, empty ``items``, or non-positive int
      ``qty`` / ``prep_minutes`` with ``ValueError``.

    Returns::

        {
          "order_id": "ord_123",
          "estimate_minutes": 23,
          "breakdown": {"items": 20, "load_penalty": 3},
        }
    """
    order_id = raw.get("order_id")
    if not order_id:
        raise ValueError("Missing order_id")

    kitchen_load = raw.get("kitchen_load", 0)
    if not isinstance(kitchen_load, int) or kitchen_load < 0:
        raise ValueError(f"Invalid kitchen_load: {kitchen_load}")
    load_penalty = kitchen_load * 1

    items = raw.get("items")
    if not items:
        raise ValueError("Missing or empty items")
    items_total = 0
    for item in items:
        qty = item.get("qty")
        if not isinstance(qty, int) or qty <= 0:
            raise ValueError(f"Invalid qty for item {item.get('sku')}: {qty}")
        prep_minutes = item.get("prep_minutes")
        if not isinstance(prep_minutes, int) or prep_minutes <= 0:
            raise ValueError(f"Invalid prep_minutes for item {item.get('sku')}: {prep_minutes}")
        items_total += qty * prep_minutes
    res = {
        "order_id": order_id,
        "estimate_minutes": items_total + load_penalty,
        "breakdown": {"items": items_total, "load_penalty": load_penalty},
    }
    return res