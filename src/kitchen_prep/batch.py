"""Batch prep-time estimation: many orders -> aggregate -> format."""

from __future__ import annotations

from typing import Any

from kitchen_prep.api import estimate_prep_time, estimate_prep_time_with_predictor
from kitchen_prep.predictors import PrepTimePredictor


def estimate_prep_time_batch(
    orders: list[dict[str, Any]],
    *,
    predictor: PrepTimePredictor | None = None,
) -> list[dict[str, Any]]:
    """Estimate each order; invalid orders raise (do not skip).

    If ``predictor`` is None, use ``estimate_prep_time`` per order.
    Otherwise use ``estimate_prep_time_with_predictor``.

    Returns a list of per-order response dicts (same shape as the single-order API).
    """
    if predictor is None:
        return [estimate_prep_time(order) for order in orders]
    else:
        return [estimate_prep_time_with_predictor(order, predictor) for order in orders]


def aggregate_batch(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate per-order results into batch summary stats.

    Required keys:
      - order_count: int
      - total_estimate_minutes: int   (sum of estimate_minutes)
      - avg_estimate_minutes: float   (total / order_count; 0.0 if empty)
      - max_estimate_minutes: int     (0 if empty)
      - min_estimate_minutes: int     (0 if empty)
    """
    order_count = len(results)
    total_estimate_minutes = sum(r["estimate_minutes"] for r in results)
    avg_estimate_minutes = total_estimate_minutes / order_count if order_count > 0 else 0.0
    max_estimate_minutes = max((r["estimate_minutes"] for r in results), default=0)
    min_estimate_minutes = min((r["estimate_minutes"] for r in results), default=0)

    return {
        "order_count": order_count,
        "total_estimate_minutes": total_estimate_minutes,
        "avg_estimate_minutes": avg_estimate_minutes,
        "max_estimate_minutes": max_estimate_minutes,
        "min_estimate_minutes": min_estimate_minutes,
    }


def format_batch_report(
    results: list[dict[str, Any]],
    summary: dict[str, Any],
) -> str:
    """Format a plain-text report.

    Exact layout (one trailing newline at end of string)::

        Batch prep-time report
        orders: {order_count}
        total_minutes: {total_estimate_minutes}
        avg_minutes: {avg_estimate_minutes:.1f}
        min_minutes: {min_estimate_minutes}
        max_minutes: {max_estimate_minutes}
        ---
        {order_id}: {estimate_minutes}m
        ...

    Per-order lines follow ``results`` order. Empty results still print the
    header + summary lines (avg 0.0, min/max 0) then ``---`` and nothing after.
    """
    lines = [
        "Batch prep-time report",
        f"orders: {summary['order_count']}",
        f"total_minutes: {summary['total_estimate_minutes']}",
        f"avg_minutes: {summary['avg_estimate_minutes']:.1f}",
        f"min_minutes: {summary['min_estimate_minutes']}",
        f"max_minutes: {summary['max_estimate_minutes']}",
        "---",
    ]
    for r in results:
        lines.append(f"{r['order_id']}: {r['estimate_minutes']}m")

    return "\n".join(lines) + "\n"
