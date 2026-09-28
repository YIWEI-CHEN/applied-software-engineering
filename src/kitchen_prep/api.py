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
          "estimate_minutes": 19,
          "breakdown": {"items": 16, "load_penalty": 3},
        }
    """
    raise NotImplementedError("Implement estimate_prep_time for ASE practice")
