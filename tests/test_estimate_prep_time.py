"""Tests for kitchen prep-time API."""

import pytest

from kitchen_prep import estimate_prep_time


def test_happy_path():
    raw = {
        "order_id": "ord_123",
        "items": [
            {"sku": "burger", "qty": 2, "prep_minutes": 8},
            {"sku": "fries", "qty": 1, "prep_minutes": 4},
        ],
        "kitchen_load": 3,
        "ordered_at": "2026-09-28T14:00:00Z",
    }

    result = estimate_prep_time(raw)

    assert result["order_id"] == "ord_123"
    assert result["estimate_minutes"] == 23
    assert result["breakdown"] == {"items": 20, "load_penalty": 3}


def test_missing_order_id_raises():
    raw = {
        "items": [{"sku": "burger", "qty": 1, "prep_minutes": 5}],
        "kitchen_load": 0,
    }
    with pytest.raises(ValueError):
        estimate_prep_time(raw)


def test_empty_items_raises():
    raw = {"order_id": "ord_1", "items": [], "kitchen_load": 0}
    with pytest.raises(ValueError):
        estimate_prep_time(raw)


def test_non_positive_qty_raises():
    raw = {
        "order_id": "ord_1",
        "items": [{"sku": "burger", "qty": 0, "prep_minutes": 5}],
        "kitchen_load": 0,
    }
    with pytest.raises(ValueError):
        estimate_prep_time(raw)
