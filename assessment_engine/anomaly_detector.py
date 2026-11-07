"""Anomaly detection engine for Layer A telemetry events.

Detects behavioral anomalies such as:
1. The "Button Masher" Anomaly:
   - Rapid click-throughs / impossibly fast response times (< 200-250ms) paired with high error rates.
   - Crucial constraint: MUST flag data as "highly uncertain" (e.g. low uncertainty_weight / confidence_score)
     rather than penalizing or dropping the user's cognitive ability score.
   - Triggers an AI Coach intervention prompt inquiring about distraction or rushing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

# Physiological minimum reaction time floor for 2AFC and cognitive choice tasks (ms)
PHYSIOLOGICAL_RT_FLOOR_MS = 220.0
# High error burst threshold indicating non-deliberate mashing
MASHING_ERROR_BURST_THRESHOLD = 2


@dataclass(frozen=True)
class AnomalyDetectionResult:
    is_anomaly: bool
    anomaly_type: Optional[str] = None
    confidence_score: float = 1.0
    uncertainty_weight: float = 1.0
    high_uncertainty: bool = False
    intervention_prompt: Optional[str] = None
    reason: Optional[str] = None


class ButtonMasherDetector:
    """Detects rapid click-through and button mashing patterns in Layer A telemetry."""

    def __init__(
        self,
        rt_floor_ms: float = PHYSIOLOGICAL_RT_FLOOR_MS,
        mashing_error_burst: int = MASHING_ERROR_BURST_THRESHOLD,
    ):
        self.rt_floor_ms = rt_floor_ms
        self.mashing_error_burst = mashing_error_burst

    def evaluate_trial(self, event: Dict[str, Any]) -> AnomalyDetectionResult:
        """Evaluate a single telemetry event for button mashing anomaly."""
        rt = float(event.get("response_time_ms", 1000.0))
        error_flag = bool(event.get("error_flag", False))
        error_burst = int(event.get("error_burst", 0))

        # Check for impossibly fast response time with error
        is_too_fast = rt > 0 and rt < self.rt_floor_ms
        is_mashing = (is_too_fast and error_flag) or (is_too_fast and error_burst >= self.mashing_error_burst)

        if is_mashing:
            return AnomalyDetectionResult(
                is_anomaly=True,
                anomaly_type="button_masher",
                confidence_score=0.15,
                uncertainty_weight=0.10,
                high_uncertainty=True,
                intervention_prompt="Noticed super fast taps with some misses. Feeling rushed or distracted right now?",
                reason=(
                    f"Rapid click-through detected: RT ({rt:.1f}ms) below physiological "
                    f"threshold ({self.rt_floor_ms}ms) with error burst {error_burst}."
                ),
            )

        return AnomalyDetectionResult(
            is_anomaly=False,
            confidence_score=1.0,
            uncertainty_weight=1.0,
            high_uncertainty=False,
        )

    def evaluate_batch(self, events: Sequence[Dict[str, Any]]) -> AnomalyDetectionResult:
        """Evaluate a sequence of trials for overall session button mashing."""
        if not events:
            return AnomalyDetectionResult(is_anomaly=False)

        rapid_errors = 0
        total_trials = len(events)
        total_rt = 0.0

        for e in events:
            rt = float(e.get("response_time_ms", 1000.0))
            err = bool(e.get("error_flag", False))
            total_rt += rt
            if rt > 0 and rt < self.rt_floor_ms and err:
                rapid_errors += 1

        rapid_error_ratio = rapid_errors / max(1, total_trials)
        avg_rt = total_rt / max(1, total_trials)

        if rapid_error_ratio >= 0.3 or (avg_rt < self.rt_floor_ms and rapid_errors > 0):
            return AnomalyDetectionResult(
                is_anomaly=True,
                anomaly_type="button_masher",
                confidence_score=0.10,
                uncertainty_weight=0.10,
                high_uncertainty=True,
                intervention_prompt="Noticed super fast taps with some misses. Feeling rushed or distracted right now?",
                reason=(
                    f"Session button mashing pattern: {rapid_errors}/{total_trials} rapid error trials "
                    f"(avg RT: {avg_rt:.1f}ms)."
                ),
            )

        return AnomalyDetectionResult(
            is_anomaly=False,
            confidence_score=1.0,
            uncertainty_weight=1.0,
            high_uncertainty=False,
        )


_DEFAULT_DETECTOR = ButtonMasherDetector()


def detect_button_masher(event_or_events: Dict[str, Any] | Sequence[Dict[str, Any]]) -> AnomalyDetectionResult:
    """Convenience function to evaluate event(s) against the default ButtonMasherDetector."""
    if isinstance(event_or_events, dict):
        return _DEFAULT_DETECTOR.evaluate_trial(event_or_events)
    return _DEFAULT_DETECTOR.evaluate_batch(event_or_events)
