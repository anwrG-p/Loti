"""Asymmetrical Cognitive Training Planner for Layer C difficulty engine.

Hackathon Scenario 6 (The Asymmetrical Mind):
- Requirement: Handle extreme variance across cognitive dimensions (e.g., flawless logic, failing attention).
- Condition: Layer C must NOT calculate a generic "average" difficulty.
- Action: Generate an asymmetrical training plan (advanced tasks in strong dimensions + foundational
  tasks in weak ones) and feed this split to the radar chart UI.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


@dataclass(frozen=True)
class DimensionPrescription:
    dimension: str
    score: float
    tier: str  # "advanced", "foundational", "balanced"
    prescribed_theta: float
    focus_objective: str


@dataclass(frozen=True)
class AsymmetricalPlanResult:
    is_asymmetrical: bool
    spread: float
    variance: float
    std_dev: float
    mean_score: float
    prescriptions: List[DimensionPrescription]
    radar_split: Dict[str, List[str]]
    curriculum_modules: List[Dict[str, Any]]
    explanation: str


# Mapping from pillar id to appropriate strong/weak exercise schemas
PILLAR_EXERCISES = {
    "focus": {"advanced": "tower", "foundational": "matrix"},
    "agility": {"advanced": "flanker", "foundational": "mental_rotation"},
    "impulse": {"advanced": "stop_signal", "foundational": "stroop"},
    "memory": {"advanced": "mst", "foundational": "pal"},
    "visual": {"advanced": "ufov", "foundational": "ufov"},
}


class AsymmetricalPlanner:
    """Analyzes cross-dimensional variance and generates asymmetric difficulty prescriptions."""

    def __init__(
        self,
        spread_threshold: float = 30.0,
        std_threshold: float = 12.0,
        advanced_score_floor: float = 68.0,
        foundational_score_ceiling: float = 48.0,
    ):
        self.spread_threshold = spread_threshold
        self.std_threshold = std_threshold
        self.advanced_score_floor = advanced_score_floor
        self.foundational_score_ceiling = foundational_score_ceiling

    def evaluate_profile(
        self, pillar_scores: Mapping[str, float | None]
    ) -> AsymmetricalPlanResult:
        """Evaluate pillar profile for asymmetric cognitive variance and generate split plan."""
        valid_scores = {
            k: float(v)
            for k, v in pillar_scores.items()
            if v is not None and not isinstance(v, bool) and math.isfinite(v)
        }

        if len(valid_scores) < 2:
            return AsymmetricalPlanResult(
                is_asymmetrical=False,
                spread=0.0,
                variance=0.0,
                std_dev=0.0,
                mean_score=float(sum(valid_scores.values()) / max(1, len(valid_scores))),
                prescriptions=[],
                radar_split={"advanced": [], "foundational": [], "balanced": list(valid_scores.keys())},
                curriculum_modules=[],
                explanation="Insufficient dimensions scored to determine variance.",
            )

        scores_list = list(valid_scores.values())
        mean_score = sum(scores_list) / len(scores_list)
        variance = sum((s - mean_score) ** 2 for s in scores_list) / len(scores_list)
        std_dev = math.sqrt(variance)
        max_score = max(scores_list)
        min_score = min(scores_list)
        spread = max_score - min_score

        is_asymmetrical = spread >= self.spread_threshold or std_dev >= self.std_threshold

        prescriptions: List[DimensionPrescription] = []
        radar_split: Dict[str, List[str]] = {
            "advanced": [],
            "foundational": [],
            "balanced": [],
        }
        curriculum_modules: List[Dict[str, Any]] = []

        for dim, score in sorted(valid_scores.items(), key=lambda item: item[1], reverse=True):
            if is_asymmetrical and (score >= self.advanced_score_floor or score >= mean_score + 0.5 * std_dev):
                tier = "advanced"
                theta = min(1.0, max(0.75, score / 100.0))
                objective = f"Push peak limits in {dim} with high-constraint challenges"
                radar_split["advanced"].append(dim)
            elif is_asymmetrical and (score <= self.foundational_score_ceiling or score <= mean_score - 0.5 * std_dev):
                tier = "foundational"
                theta = max(0.15, min(0.35, score / 100.0))
                objective = f"Build stable fundamentals in {dim} with scaffolded pacing"
                radar_split["foundational"].append(dim)
            else:
                tier = "balanced"
                theta = 0.50
                objective = f"Maintain balanced steady cadence in {dim}"
                radar_split["balanced"].append(dim)

            prescriptions.append(
                DimensionPrescription(
                    dimension=dim,
                    score=round(score, 1),
                    tier=tier,
                    prescribed_theta=round(theta, 2),
                    focus_objective=objective,
                )
            )

            schema_pair = PILLAR_EXERCISES.get(dim, {"advanced": "matrix", "foundational": "matrix"})
            chosen_schema = schema_pair["advanced"] if tier == "advanced" else schema_pair["foundational"]
            curriculum_modules.append({
                "module_id": f"ASYM-{dim[:3].upper()}-{tier[:3].upper()}",
                "dimension": dim,
                "tier": tier,
                "prescribed_theta": round(theta, 2),
                "recommended_schema": chosen_schema,
                "objective": objective,
                "target_duration_mins": 12 if tier == "advanced" else 8,
            })

        explanation = (
            f"Asymmetrical profile detected (spread: {spread:.1f}pts, std: {std_dev:.1f}pts). "
            f"Layer C generated an asymmetrical training plan: advanced tasks for strong skills "
            f"({', '.join(radar_split['advanced']) or 'none'}) and foundational scaffolding for weak skills "
            f"({', '.join(radar_split['foundational']) or 'none'})."
            if is_asymmetrical
            else "Balanced cognitive profile: standard difficulty progression applied."
        )

        return AsymmetricalPlanResult(
            is_asymmetrical=is_asymmetrical,
            spread=round(spread, 2),
            variance=round(variance, 2),
            std_dev=round(std_dev, 2),
            mean_score=round(mean_score, 2),
            prescriptions=prescriptions,
            radar_split=radar_split,
            curriculum_modules=curriculum_modules,
            explanation=explanation,
        )


_DEFAULT_PLANNER = AsymmetricalPlanner()


def plan_asymmetrical_curriculum(
    pillar_scores: Mapping[str, float | None]
) -> AsymmetricalPlanResult:
    """Convenience helper to evaluate and generate an asymmetrical curriculum."""
    return _DEFAULT_PLANNER.evaluate_profile(pillar_scores)
