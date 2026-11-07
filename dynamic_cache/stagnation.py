"""Stagnation Plateau Detector for Layer C difficulty engine.

Hackathon Scenario 2 (The Stagnation Plateau):
- Requirement: Detect flatline performance (consistently average scores across multiple sessions with zero trend).
- Condition: Must break the endless loop of identical tasks.
- Action: AI Coach must trigger an exercise format change or suggest a new strategy to break stagnation.

Implements a rolling window variance and moving average check across historical session/trial scores.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence


@dataclass(frozen=True)
class StagnationResult:
    is_stagnant: bool
    rolling_mean: float
    rolling_variance: float
    trend_slope: float
    sessions_analyzed: int
    recommended_action: str
    suggested_strategy: Optional[str] = None


class StagnationPlateauDetector:
    """Detects stagnation plateau (flatline performance with zero trend) in cognitive sessions."""

    def __init__(
        self,
        min_window: int = 3,
        variance_threshold: float = 0.006,  # Low variance = flatline
        slope_threshold: float = 0.02,     # Zero / near-zero slope
        average_band_min: float = 0.35,    # Average performance zone
        average_band_max: float = 0.80,
    ):
        self.min_window = min_window
        self.variance_threshold = variance_threshold
        self.slope_threshold = slope_threshold
        self.average_band_min = average_band_min
        self.average_band_max = average_band_max

    def analyze_scores(self, scores: Sequence[float]) -> StagnationResult:
        """Analyze a sequence of normalized scores (0.0 to 1.0) for stagnation."""
        n = len(scores)
        if n < self.min_window:
            return StagnationResult(
                is_stagnant=False,
                rolling_mean=float(sum(scores) / n) if n > 0 else 0.0,
                rolling_variance=0.0,
                trend_slope=0.0,
                sessions_analyzed=n,
                recommended_action="continue_standard_progression",
            )

        window = [float(s) for s in scores[-max(self.min_window, min(n, 10)):]]
        w_len = len(window)
        mean_score = sum(window) / w_len
        variance = sum((x - mean_score) ** 2 for x in window) / w_len

        # Linear regression slope over session indices
        x_indices = list(range(w_len))
        x_mean = sum(x_indices) / w_len
        denom = sum((i - x_mean) ** 2 for i in x_indices)
        if denom > 0:
            numer = sum((i - x_mean) * (window[i] - mean_score) for i in x_indices)
            slope = numer / denom
        else:
            slope = 0.0

        in_average_band = self.average_band_min <= mean_score <= self.average_band_max
        is_flatline = variance <= self.variance_threshold
        is_zero_trend = abs(slope) <= self.slope_threshold

        if in_average_band and is_flatline and is_zero_trend:
            return StagnationResult(
                is_stagnant=True,
                rolling_mean=round(mean_score, 4),
                rolling_variance=round(variance, 6),
                trend_slope=round(slope, 6),
                sessions_analyzed=w_len,
                recommended_action="switch_exercise_format",
                suggested_strategy=(
                    "Shift exercise format and introduce cross-dimensional perturbation "
                    "to break cognitive equilibrium."
                ),
            )

        return StagnationResult(
            is_stagnant=False,
            rolling_mean=round(mean_score, 4),
            rolling_variance=round(variance, 6),
            trend_slope=round(slope, 6),
            sessions_analyzed=w_len,
            recommended_action="continue_standard_progression",
        )


_DEFAULT_DETECTOR = StagnationPlateauDetector()


def detect_stagnation(scores: Sequence[float]) -> StagnationResult:
    """Convenience helper using default plateau detector thresholds."""
    return _DEFAULT_DETECTOR.analyze_scores(scores)
