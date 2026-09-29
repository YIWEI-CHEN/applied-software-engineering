"""Pluggable prep-time predictors (ASE: swap heuristic for model.predict)."""

from __future__ import annotations

from typing import Any, Protocol


class PrepTimePredictor(Protocol):
    """Anything with ``predict(features) -> minutes`` can be injected."""

    def predict(self, features: dict[str, Any]) -> int:
        ...


class HeuristicPredictor:
    """Baseline: item_minutes + kitchen_load (same math as estimate_prep_time)."""

    def predict(self, features: dict[str, Any]) -> int:
        return features["item_minutes"] + features["kitchen_load"]


class StubMlPredictor:
    """Fake ML model: linear combo of features (no sklearn needed).

    Default weights mimic the heuristic so happy-path still lands on 23:
      estimate = w_item * item_minutes + w_load * kitchen_load
               + w_skus * num_skus + w_units * num_units + bias

    With defaults (1, 1, 0, 0, 0) -> same as heuristic.
    Tests will also inject custom weights to prove the model path is live.
    """

    def __init__(
        self,
        w_item: float = 1.0,
        w_load: float = 1.0,
        w_skus: float = 0.0,
        w_units: float = 0.0,
        bias: float = 0.0,
    ) -> None:
        self.w_item = w_item
        self.w_load = w_load
        self.w_skus = w_skus
        self.w_units = w_units
        self.bias = bias

    def predict(self, features: dict[str, Any]) -> int:
        """Linear score rounded to int.

        Uses keys: item_minutes, kitchen_load, num_skus, num_units.
        """
        score = (
            self.w_item * features["item_minutes"]
            + self.w_load * features["kitchen_load"]
            + self.w_skus * features["num_skus"]
            + self.w_units * features["num_units"]
            + self.bias
        )
        return round(score)
