"""Comprehensive Automated Verification Suite for the 6 Hackathon Scenarios.

Scenarios tested:
1. The "Button Masher" Anomaly (Layer A)
2. The Stagnation Plateau (Layer C)
3. The "Why" Audit (Explainability)
4. The Pushback Scenario (Collaboration Score)
5. The Fortune Teller Trap (Projections)
6. The Asymmetrical Mind (Generalisation)
"""

import math
import pytest
from ai_coach.agent import (
    AICoachAgent,
    OFFLINE_ANOMALY_REPLY,
    OFFLINE_PUSHBACK_REPLY,
    OFFLINE_STAGNATION_REPLY,
)
from ai_coach.collaboration_scorer import CollaborationScorer
from ai_coach.safety_guardrails import FORTUNE_TELLER_REPLY, SafetyGuardrailEngine
from ai_coach.schemas import ChatMessage, ChatMessageRole, ChatRequest, ReplySource
from ai_coach.xai_explainer import XAIExplainer
from assessment_engine.anomaly_detector import ButtonMasherDetector, detect_button_masher
from brain_twin_jepa.features import pillar_scores, session_features, task_scores
from dynamic_cache.asymmetrical_planner import AsymmetricalPlanner, plan_asymmetrical_curriculum
from dynamic_cache.stagnation import StagnationPlateauDetector, detect_stagnation


# ==============================================================================
# SCENARIO 1: The "Button Masher" Anomaly (Layer A)
# ==============================================================================
def test_scenario_1_button_masher_anomaly_detection_and_score_protection():
    """1. The 'Button Masher' Anomaly (Layer A):
    - Requirement: Detect rapid click-throughs (impossibly fast response times + high error rates).
    - Condition: Must flag data as 'highly uncertain' rather than dropping the cognitive ability score.
    - Action: AI Coach must trigger a contextual intervention (asking about distraction/rushing).
    """
    detector = ButtonMasherDetector()

    # Normal trial: 650ms RT with correct response
    normal_trial = {
        "user_id": "u1",
        "session_id": "s1",
        "task_id": "matrix-1",
        "trial_index": 0,
        "dimension": "pattern_induction",
        "score_norm": 1.0,
        "response_time_ms": 650.0,
        "error_flag": False,
        "error_burst": 0,
        "hesitation_jitter": 15.0,
    }
    res_normal = detector.evaluate_trial(normal_trial)
    assert not res_normal.is_anomaly
    assert res_normal.confidence_score == 1.0
    assert not res_normal.high_uncertainty

    # Button masher trial: 110ms RT (impossibly fast) with error
    masher_trial = {
        "user_id": "u1",
        "session_id": "s1",
        "task_id": "matrix-2",
        "trial_index": 1,
        "dimension": "pattern_induction",
        "score_norm": 0.0,
        "response_time_ms": 110.0,
        "error_flag": True,
        "error_burst": 3,
        "hesitation_jitter": 2.0,
    }
    res_masher = detector.evaluate_trial(masher_trial)
    assert res_masher.is_anomaly
    assert res_masher.anomaly_type == "button_masher"
    assert res_masher.high_uncertainty
    assert res_masher.uncertainty_weight <= 0.20
    assert res_masher.confidence_score <= 0.20
    assert "rushed or distracted" in (res_masher.intervention_prompt or "")

    # Test Layer A scoring behavior: ensure cognitive score does NOT drop to 0,
    # and uncertainty is flagged as highly uncertain (>= 45.0 points)
    mashed_events = [
        {
            "user_id": "u1",
            "session_id": "s1",
            "task_id": f"matrix-{i}",
            "trial_index": i,
            "dimension": "pattern_induction",
            "score_norm": 0.0,
            "response_time_ms": 120.0,
            "error_flag": True,
            "error_burst": i + 1,
            "hesitation_jitter": 1.5,
            "trial_meta": {},
        }
        for i in range(5)
    ] + [
        {
            "user_id": "u1",
            "session_id": "s1",
            "task_id": f"tower-{i}",
            "trial_index": i + 5,
            "dimension": "executive_function",
            "score_norm": 0.0,
            "response_time_ms": 110.0,
            "error_flag": True,
            "error_burst": i + 1,
            "hesitation_jitter": 1.1,
            "trial_meta": {"l_min": 3, "l_user": 5, "solved": True, "planning_time_ms": 100},
        }
        for i in range(5)
    ]
    feat = session_features(mashed_events)
    focus_pillar = feat["pillars"]["focus"]
    fluid_input = feat["inputs"]["FluidMatrices"]

    # Condition: Input and pillar must flag data as highly uncertain rather than dropping cognitive ability score to 0
    assert fluid_input["score"] >= 50.0, f"Input score dropped to {fluid_input['score']}"
    assert focus_pillar["uncertainty"] >= 45.0, f"Expected high uncertainty, got {focus_pillar['uncertainty']}"
    assert focus_pillar["score"] is not None and focus_pillar["score"] >= 49.9, (
        f"Score dropped to {focus_pillar['score']}, should be protected from dropping to 0."
    )

    # Action: AI Coach contextual intervention
    agent = AICoachAgent()
    req = ChatRequest(
        user_id="u1",
        message="Why are my results like that? I was speed clicking",
        anomaly_flag="button_masher",
    )
    coach_resp = agent.handle_chat(req)
    assert OFFLINE_ANOMALY_REPLY == coach_resp.reply_text
    assert "Noticed super fast taps" in coach_resp.reply_text
    assert "rushed or distracted" in coach_resp.reply_text


# ==============================================================================
# SCENARIO 2: The Stagnation Plateau (Layer C)
# ==============================================================================
def test_scenario_2_stagnation_plateau_detection_and_loop_break():
    """2. The Stagnation Plateau (Layer C):
    - Requirement: Detect flatline performance (consistently average scores across multiple sessions with zero trend).
    - Condition: Must break the endless loop of identical tasks.
    - Action: AI Coach must trigger an exercise format change or suggest a new strategy to break stagnation.
    """
    detector = StagnationPlateauDetector()

    # Dynamic progression scores (variable, increasing trend) -> not stagnant
    progressing_scores = [0.45, 0.52, 0.60, 0.68, 0.74, 0.82]
    res_prog = detector.analyze_scores(progressing_scores)
    assert not res_prog.is_stagnant

    # Flatline performance: consistently ~0.55 across 6 sessions with zero variance/trend
    flatline_scores = [0.55, 0.552, 0.548, 0.551, 0.549, 0.550]
    res_stag = detector.analyze_scores(flatline_scores)
    assert res_stag.is_stagnant
    assert res_stag.rolling_variance < 0.001
    assert abs(res_stag.trend_slope) < 0.005
    assert res_stag.recommended_action == "switch_exercise_format"
    assert "break cognitive equilibrium" in (res_stag.suggested_strategy or "")

    # Action: AI Coach triggers exercise format change / strategy intervention
    agent = AICoachAgent()
    req = ChatRequest(
        user_id="u1",
        message="I feel like my progress has reached a plateau lately.",
        adaptation_reason="plateau_detected",
    )
    resp = agent.handle_chat(req)
    assert OFFLINE_STAGNATION_REPLY == resp.reply_text
    assert "flatlined" in resp.reply_text
    assert "switched formats" in resp.reply_text
    assert "new strategy" in resp.reply_text


# ==============================================================================
# SCENARIO 3: The "Why" Audit (Explainability)
# ==============================================================================
def test_scenario_3_why_audit_explainability_pipeline():
    """3. The 'Why' Audit (Explainability):
    - Requirement: AI Coach must answer 'Why did you assign me this specific exercise today?' with zero black-box reasoning.
    - Condition: Must directly query the Brain Twin data pipeline.
    - Action: Must cite specific data-driven justifications (e.g. referencing recent RT drops or heatmaps).
    """
    explainer = XAIExplainer()

    # Query pipeline with recent response time drop
    why_rt_drop = explainer.explain_assignment_from_pipeline(
        schema_type="relational",
        recent_rt_drop_ms=45.0,
    )
    assert "45ms" in why_rt_drop
    assert "recent training pipeline" in why_rt_drop
    assert len(why_rt_drop.split("\n\n")) <= 3

    # Query pipeline with fatigue heatmap
    why_heatmap = explainer.explain_assignment_from_pipeline(
        schema_type="tower",
        fatigue_bucket="afternoon",
    )
    assert "afternoon fatigue heatmap" in why_heatmap
    assert "focus dips" in why_heatmap

    # AI Coach handle chat query for why exercise was assigned
    agent = AICoachAgent(explainer=explainer)
    req = ChatRequest(
        user_id="u1",
        message="Why did you assign me this specific exercise today?",
        adaptation_reason="Your reaction time dropped 45ms on recent rounds.",
    )
    resp = agent.handle_chat(req)
    assert "training pipeline" in resp.reply_text or "45ms" in resp.reply_text
    # Ensure zero black-box reasoning: check that specific data evidence is cited
    assert any(term in resp.reply_text for term in ["45ms", "telemetry", "rounds", "pipeline"])


# ==============================================================================
# SCENARIO 4: The Pushback Scenario (Collaboration Score)
# ==============================================================================
def test_scenario_4_pushback_collaboration_score_and_uncertainty():
    """4. The Pushback Scenario (Collaboration Score):
    - Requirement: Handle user disagreement regarding poor performance (e.g., blaming environmental distraction).
    - Condition: Must NOT stubbornly defend the profile.
    - Action: Dynamically increase the data's uncertainty metric AND increase the user's 'AI Collaboration Score' for critical verification.
    """
    scorer = CollaborationScorer()

    # Base conversation without pushback
    history_standard = [
        ChatMessage(role=ChatMessageRole.USER, content="Hello Loti, how does this work?"),
        ChatMessage(role=ChatMessageRole.ASSISTANT, content="Welcome! Let's try a round."),
        ChatMessage(role=ChatMessageRole.USER, content="Okay, ready."),
    ]
    scores_standard = scorer.evaluate_interaction_signals(history_standard)
    crit_base = scores_standard.critical_verification

    # Conversation with user pushback / environmental distraction disagreement
    history_pushback = [
        ChatMessage(role=ChatMessageRole.USER, content="Hello Loti, how does this work?"),
        ChatMessage(role=ChatMessageRole.ASSISTANT, content="Your accuracy dropped on the last session."),
        ChatMessage(
            role=ChatMessageRole.USER,
            content="I disagree with that score! I was distracted because my dog barked and made loud noise, it's not my fault!",
        ),
    ]
    # Check pushback detection
    assert scorer.detect_pushback(history_pushback[-1].content)

    scores_pushback = scorer.evaluate_interaction_signals(history_pushback)
    crit_pushback = scores_pushback.critical_verification

    # Action 1: Must increase the user's AI Collaboration Score for critical verification
    assert crit_pushback > crit_base + 20.0, (
        f"Critical verification should increase significantly on pushback (was {crit_base}, now {crit_pushback})"
    )

    # Action 2: AI Coach must NOT stubbornly defend the profile and must increase data uncertainty
    agent = AICoachAgent(scorer=scorer)
    req = ChatRequest(
        user_id="u1",
        message="I was distracted by noisy neighbors, I disagree with this poor score!",
        uncertainty=0.15,
    )
    resp = agent.handle_chat(req)

    # Coach reply must validate context and not defend the profile
    assert resp.reply_text == OFFLINE_PUSHBACK_REPLY
    assert "External distractions definitely impact your focus." in resp.reply_text
    assert "increased the uncertainty" in resp.reply_text
    assert "verifying your real context" in resp.reply_text


# ==============================================================================
# SCENARIO 5: The Fortune Teller Trap (Projections)
# ==============================================================================
def test_scenario_5_fortune_teller_trap_guardrails():
    """5. The Fortune Teller Trap (Projections):
    - Requirement: Handle queries asking for exact future cognitive scores.
    - Condition: Strict guardrails preventing absolute claims.
    - Action: Pivot to probabilistic language using statistical confidence intervals.
    """
    guardrail = SafetyGuardrailEngine()

    fortune_queries = [
        "What will my score be next week?",
        "Predict my score for next month.",
        "Will I reach 90 next week?",
        "Can you predict my future score?",
    ]

    for q in fortune_queries:
        gate_res = guardrail.fortune_teller_check(q)
        assert gate_res.hit, f"Query '{q}' should trigger the Fortune Teller guardrail"
        reply = gate_res.reply or ""

        # Condition: Strict guardrails preventing absolute claims
        assert "you will reach" not in reply.lower()
        assert "i cannot predict exact future scores" in reply.lower()

        # Action: Pivot to probabilistic language using statistical confidence intervals
        assert "statistical confidence intervals" in reply.lower()
        assert "uncertainty band" in reply.lower()

    # Test through AICoachAgent input gate
    agent = AICoachAgent()
    req = ChatRequest(user_id="u1", message="Tell me what my score will be next month. Will I reach 95?")
    resp = agent.handle_chat(req)
    assert resp.reply_source == ReplySource.FORTUNE_TELLER
    assert resp.reply_text == FORTUNE_TELLER_REPLY


# ==============================================================================
# SCENARIO 6: The Asymmetrical Mind (Generalisation)
# ==============================================================================
def test_scenario_6_asymmetrical_mind_curriculum_and_radar_split():
    """6. The Asymmetrical Mind (Generalisation):
    - Requirement: Handle extreme variance across cognitive dimensions (e.g. flawless logic, failing attention).
    - Condition: Layer C must NOT calculate a generic 'average' difficulty.
    - Action: Generate an asymmetrical training plan (advanced tasks in strong dimensions + foundational tasks in weak ones)
      and feed this split to the radar chart UI.
    """
    planner = AsymmetricalPlanner()

    # Extreme variance profile: flawless Focus (95.0), failing Agility (32.0), moderate others
    asym_profile = {
        "focus": 95.0,
        "agility": 32.0,
        "impulse": 55.0,
        "memory": 52.0,
        "visual": 50.0,
    }

    result = planner.evaluate_profile(asym_profile)
    assert result.is_asymmetrical
    assert result.spread >= 60.0

    # Condition: Layer C must NOT calculate a generic "average" difficulty
    # Average would be ~56.8 (theta ~0.57). Instead, prescriptions must split into advanced & foundational!
    prescriptions = {p.dimension: p for p in result.prescriptions}

    # Advanced in strong dimension (Focus)
    assert prescriptions["focus"].tier == "advanced"
    assert prescriptions["focus"].prescribed_theta >= 0.80

    # Foundational in weak dimension (Agility)
    assert prescriptions["agility"].tier == "foundational"
    assert prescriptions["agility"].prescribed_theta <= 0.35

    # Feed split to the radar chart UI
    assert "focus" in result.radar_split["advanced"]
    assert "agility" in result.radar_split["foundational"]

    # Verify curriculum generation in AICoachAgent
    agent = AICoachAgent()
    path = agent.generate_learning_path(
        user_id="u1",
        cluster_id=4,
        pillar_scores=asym_profile,
    )
    assert path["is_asymmetrical"] is True
    assert "radar_split" in path
    assert "focus" in path["radar_split"]["advanced"]
    assert "agility" in path["radar_split"]["foundational"]
    assert "Asymmetrical Adaptive Track" in path["learning_path_title"]
