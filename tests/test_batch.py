"""Tests for batch estimate → aggregate → format."""

import pytest

from kitchen_prep import estimate_prep_time
from kitchen_prep.batch import (
    aggregate_batch,
    estimate_prep_time_batch,
    format_batch_report,
)
from kitchen_prep.predictors import StubMlPredictor


def _ord(oid: str, item_minutes: int, load: int = 0):
    return {
        "order_id": oid,
        "items": [{"sku": "x", "qty": 1, "prep_minutes": item_minutes}],
        "kitchen_load": load,
    }


def test_batch_estimates_each_order():
    orders = [_ord("a", 10, 2), _ord("b", 5, 0)]
    results = estimate_prep_time_batch(orders)
    assert [r["order_id"] for r in results] == ["a", "b"]
    assert results[0]["estimate_minutes"] == 12
    assert results[1]["estimate_minutes"] == 5


def test_batch_with_predictor():
    orders = [_ord("a", 10, 3)]  # heuristic 13; w_item=2 -> 20+3=23
    results = estimate_prep_time_batch(
        orders, predictor=StubMlPredictor(w_item=2.0, w_load=1.0)
    )
    assert results[0]["estimate_minutes"] == 23
    assert results[0]["breakdown"]["items"] == 10


def test_batch_propagates_validation_error():
    orders = [_ord("ok", 4), {"items": [{"sku": "x", "qty": 1, "prep_minutes": 1}]}]
    with pytest.raises(ValueError):
        estimate_prep_time_batch(orders)


def test_aggregate_batch():
    results = estimate_prep_time_batch([_ord("a", 10, 2), _ord("b", 5, 1)])
    summary = aggregate_batch(results)
    assert summary == {
        "order_count": 2,
        "total_estimate_minutes": 18,  # 12 + 6
        "avg_estimate_minutes": 9.0,
        "max_estimate_minutes": 12,
        "min_estimate_minutes": 6,
    }


def test_aggregate_empty():
    assert aggregate_batch([]) == {
        "order_count": 0,
        "total_estimate_minutes": 0,
        "avg_estimate_minutes": 0.0,
        "max_estimate_minutes": 0,
        "min_estimate_minutes": 0,
    }


def test_format_batch_report():
    results = estimate_prep_time_batch([_ord("a", 10, 2), _ord("b", 5, 0)])
    summary = aggregate_batch(results)
    report = format_batch_report(results, summary)
    assert report == (
        "Batch prep-time report\n"
        "orders: 2\n"
        "total_minutes: 17\n"
        "avg_minutes: 8.5\n"
        "min_minutes: 5\n"
        "max_minutes: 12\n"
        "---\n"
        "a: 12m\n"
        "b: 5m\n"
    )


def test_single_api_untouched():
    raw = _ord("solo", 8, 1)
    assert estimate_prep_time(raw)["estimate_minutes"] == 9
