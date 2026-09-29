"""Tests for predictor-backed prep-time API (does not replace estimate_prep_time)."""

import pytest

from kitchen_prep import (
    HeuristicPredictor,
    StubMlPredictor,
    estimate_prep_time,
    estimate_prep_time_with_predictor,
)


def _sample_order():
    return {
        "order_id": "ord_123",
        "items": [
            {"sku": "burger", "qty": 2, "prep_minutes": 8},
            {"sku": "fries", "qty": 1, "prep_minutes": 4},
        ],
        "kitchen_load": 3,
        "ordered_at": "2026-09-28T14:00:00Z",
    }


def test_heuristic_predictor_matches_baseline_api():
    raw = _sample_order()
    baseline = estimate_prep_time(raw)
    with_model = estimate_prep_time_with_predictor(raw, HeuristicPredictor())

    assert with_model["order_id"] == baseline["order_id"]
    assert with_model["estimate_minutes"] == baseline["estimate_minutes"] == 23
    assert with_model["breakdown"]["items"] == 20
    assert with_model["breakdown"]["load_penalty"] == 3


def test_stub_ml_default_weights_match_heuristic():
    raw = _sample_order()
    result = estimate_prep_time_with_predictor(raw, StubMlPredictor())
    assert result["estimate_minutes"] == 23


def test_stub_ml_custom_weights_change_estimate():
    """Prove predict() is used: double item weight -> 40 + 3 = 43."""
    raw = _sample_order()
    predictor = StubMlPredictor(w_item=2.0, w_load=1.0)
    result = estimate_prep_time_with_predictor(raw, predictor)
    assert result["estimate_minutes"] == 43


def test_with_predictor_reuses_validation():
    raw = {"items": [{"sku": "burger", "qty": 1, "prep_minutes": 5}]}
    with pytest.raises(ValueError):
        estimate_prep_time_with_predictor(raw, HeuristicPredictor())
