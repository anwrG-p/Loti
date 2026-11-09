# Loti: An Uncertainty-Aware, Privacy-Preserving Cognitive Assessment Architecture and Digital Twin

**Authors:** AI4Brain Research & Development Team  
**Release Version:** 1.0.0 (Production Verified)  
**System Repository:** [Loti Open Source](https://github.com/anwrG-p/Loti)  
**Verification Status:** 3,100+ Automated Tests Passing (Frontend QA Green + Backend Pytest Green)  

---

### Abstract

Conventional digital cognitive assessment tools suffer from three fundamental limitations: (1) **the reliability paradox**, where classical experimental difference scores fail to capture stable individual variance; (2) **measurement noise in unconstrained web environments**, caused by display refresh disparities, motor response artifacts, and practice familiarity; and (3) **clinical anxiety and stigmatization**, where rigid diagnostic labels induce user disengagement. 

In this work, we introduce **Loti**, a calm, closed-loop cognitive training and assessment architecture that reconciles rigorous psychometrics with user empowerment. Loti delivers 11 web-accessible neuropsychological exercise paradigms governed by an adaptive procedural generation engine paired with mathematical solvers proving single-solution validity. Cognitive state is continuously modeled using a **Soft-Anchored Temporal Joint-Embedding Predictive Architecture (SAT-JEPA)** digital twin alongside **Bounded Dynamic Gaussian Mixture Model (GMM)** clustering with Schmitt-trigger hysteresis. Guidance is delivered by an explainable, non-clinical AI coach bounded by a 4-tier defense-in-depth safety hierarchy. Loti operates on a strictly non-biometric default, incorporates anonymous device identifiers, client-side scoring, and guarantees full compliance with GDPR and EU AI Act regulations.

---

## 1. System Philosophy & Ethical Architecture

Traditional computerized cognitive testing subjects individuals to anxiety-inducing, one-off diagnostic batteries that label users with clinical pathology. In contrast, Loti establishes an uncertainty-aware, closed-loop growth companion.

```
       ┌────────────────────────────────────────────────────────┐
       │                   LOTI CLOSED LOOP                     │
       └────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │    1. ASSESS                  │
                    │  11 Neuropsychological Tasks  │
                    │  Reaction Time, Jitter, Error │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │   2. UNDERSTAND (Profiling)   │
                    │  5 Cognitive Pillars + Sigma  │
                    │  Dynamic GMM Archetypes       │
                    │  SAT-JEPA Longitudinal Twin   │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │     3. COACH                  │
                    │  Loti (Axolotl Guide)         │
                    │  Deterministic Safety Gates   │
                    │  Explainable XAI Adaptations  │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │    4. IMPROVE                 │
                    │  85% Rule IRT Staircasing     │
                    │  Dynamic Task Cache & Pools   │
                    │  Interactive Visual Dashboard │
                    └───────────────┬───────────────┘
                                    │
                                    └────────────► Loops to 1. ASSESS
```

### Core Tenets

1. **Non-Clinical Mandate (Spec U5 — "We don't measure your brain"):**  
   Loti is designed strictly for personal training and self-reflection. It rigorously eliminates clinical diagnostic jargon (e.g., ADHD, autism, dementia, cognitive deficit, cortical brain-region mappings). Cognitive fitness is framed in accessible, empowering consumer vocabulary.
2. **Privacy-First Anonymous Architecture (ADR 0001):**  
   Telemetry is tied to anonymous, client-generated device identifiers (`anon_dev_*`) without requiring account registration. Raw trial scoring occurs client-side on the device; zero telemetry leaves the client without explicit opt-in ("Save my answers").
3. **Rigorous Uncertainty & Scientific Truth (ADR 0001):**  
   Real human cognitive performance is inherently noisy. Loti represents performance as interval estimates (score $\pm$ uncertainty $\sigma$) rather than deceptive point estimates. Forward projection ribbons are kept strictly in shadow mode until empirically validated on human cohorts.
4. **Zero Server-Side Emotion Recognition (ADR 0002 & EU AI Act Art 50(3)):**  
   Affective support (Momo the Dolphin) relies on client-side heuristic mood proposals that users can freely adjust. Telemetry jitter is never fed into server-side emotion recognition models, fully protecting user autonomy and privacy under EU AI Act Annex III regulations.

---

## 2. Subsystem Architecture Overview

Loti operates as a decoupled, multi-tier distributed platform:

```
                                    ┌────────────────────────────────────────────────────────┐
                                    │                 LOTI SYSTEM ARCHITECTURE               │
                                    └────────────────────────────────────────────────────────┘
                                                                │
         ┌──────────────────────────────────────────────────────┼──────────────────────────────────────────────────────┐
         ▼                                                      ▼                                                      ▼
┌─────────────────────────────────┐                    ┌─────────────────────────────────┐                    ┌─────────────────────────────────┐
│       AI & ML INNOVATIONS       │                    │    PSYCHOMETRIC & SAFETY MOATS  │                    │    PRODUCTION & UX EXCELLENCE   │
├─────────────────────────────────┤                    ├─────────────────────────────────┤                    ├─────────────────────────────────┤
│ • SAT-JEPA Leaky Integrator     │                    │ • Algorithmic 7-Bias Mitigators │                    │ • Dimensionality Stress Test    │
│ • EMA Target Encoder (τ=0.996)  │                    │ • 4-Layer Crisis Intervention   │                    │ • TimedBloom Deduplication      │
│ • Split-Conformal Calibrations  │                    │ • Strict Banned-Terms Linter    │                    │ • 100% WCAG AAA Design Tokens   │
│ • Bounded Dynamic GMM ($k^*$)   │                    │ • Reliable Change Index (RCI)   │                    │ • Dynamic Colorblind Ink Sets   │
│ • Schmitt-Trigger Hysteresis    │                    │ • Two-Tier Stereotype Shield    │                    │ • 3,100+ Automated Tests Suite  │
└─────────────────────────────────┘                    └─────────────────────────────────┘                    └─────────────────────────────────┘
```

1. **Continuous Assessment Execution (`frontend/src/features/assessment/`):** 11 web-accessible cognitive exercises recording sub-millisecond reaction times, trial accuracy, hesitation jitter, and motor dynamics.
2. **Behavioral Feature Engineering & SAT-JEPA Digital Twin (`brain_twin_jepa/`):** Extracts 14 canonical behavioral features per session, fits soft-anchored joint-embedding predictive representations, and projects future trajectories with conformal bounds.
3. **Dynamic Archetype Clustering (`clustering_engine/`):** Bounded Gaussian Mixture Models with automatic $k^*$ model selection via Bayesian Information Criterion (BIC), cluster mass gating ($w_k \ge 0.05$), and Schmitt-trigger hysteresis.
4. **Explainable AI Coach (`ai_coach/`):** Conversational agent (Loti the Axolotl) featuring 4-tier defense-in-depth safety guardrails, dynamic collaboration scoring, and transparent adaptation justifications.
5. **Procedural Assessment Generator & Cache Dispatcher (`dynamic_cache/`):** 11 procedural generators backed by mathematical solvers, delivering pre-validated, single-solution puzzles in $<10\text{ ms}$ from hot priority queues.
6. **Adaptive Analytics Dashboard (`frontend/src/pages/`):** Uncertainty radar visualization, monotonic progress curves, past session heatmaps, and habit-forming weekly goal tracking.

---

## 3. The 11 Neuropsychological Tasks & Cognitive Pillars

Loti translates validated experimental psychology paradigms into engaging, game-like micro-exercises. User-facing terminology groups these into 5 core **Skills (Pillars)**:

| Skill (Pillar) | Exercise | Schema Type | Telemetry Dimension | Paradigm / Measurement Metric |
| :--- | :--- | :--- | :--- | :--- |
| **Focus & Strategy** | Logic Web | `relational` | `pattern_induction` | Relational reasoning across multi-step graph traversals |
| | Strategic Blueprint | `tower` | `executive_function` | Tower of London planning time & move efficiency ($l_{\min}/l_{\text{user}}$) |
| | Pattern Puzzle | `matrix` | `pattern_induction` | Visual matrix completion (Raven-style abstract induction) |
| | Memory Gauntlet | `n_back` | `working_memory` | Dual-stream n-back working memory ($d'$ signal detection) |
| **Mental Agility** | Arrow Focus | `flanker` | `executive_function` | Eriksen flanker spatial conflict resolution & cue processing |
| | Shape Turn | `mental_rotation` | `spatial_orientation` | 2D/3D polygon angular matching and rotational speed |
| | Color Clash | `stroop` | `executive_function` | Stroop interference cost & executive conflict resolution |
| | *Cross-Task* | *all tasks* | `multi-dimensional` | `ErrorRecovery`: accuracy on trials immediately following an error |
| **Impulse Control** | Stop Light | `stop_signal` | `executive_function` | Stop-Signal Reaction Time (SSRT, Verbruggen integration) |
| | Strategic Blueprint | `tower` | `executive_function` | `OTS_Execution`: ratio of counter-intuitive moves executed |
| | *Cross-Task* | `stop_signal`, `flanker` | `executive_function` | `DDM_Caution`: Ratcliff EZ-diffusion boundary separation ($a$) |
| **Deep Memory** | Precision Archive | `mst` | `episodic_memory` | Mnemonic Similarity Task (Lure Discrimination Index, LDI) |
| | Pair Finder | `pal` | `episodic_memory` | Paired Associate Learning (CANTAB first-attempt accuracy) |
| **Visual Radar** | Perceptual Radar | `ufov` | `processing_speed` | Useful Field of View (QUEST+ adaptive threshold & peripheral accuracy) |

---

## 4. Algorithmic Mitigation of 7 Real-World Measurement Biases

Unconstrained web environments introduce systematic hardware, motor, and psychological biases that invalidate naive cognitive scoring. Loti incorporates active algorithmic defenses for each:

| Bias Type | Threat to Measurement Validity | Loti Algorithmic Mitigation |
| :--- | :--- | :--- |
| **1. Display Refresh Rate** | Variable monitor refresh ($60\text{Hz}$ vs $144\text{Hz}$) distorts sub-second stimulus presentation times. | UFOV logs `shown_ms` derived from `requestAnimationFrame` hardware timestamps rather than theoretical intervals. |
| **2. Random / Rapid Guessing** | Disengaged participants mash buttons, artificially inflating speed metrics. | Integrated chance floor gates ($p_0 = 1/k$); rapid button mashing yields a 0 score rather than high agility. |
| **3. Interruption & Inattention** | Browser tab switching or background notifications pollute trial reaction times. | Page Visibility API auto-pauses tasks on `document.hidden`; interrupted trials are flagged and discarded. |
| **4. Color Vision Deficiency (CVD)** | Protanopia/Deuteranopia degrades Stroop test performance independently of cognitive inhibition. | Server serves `inks=cvd_safe` (Cobalt Blue, Lemon Yellow, Vermilion, Jet Black) mapped onto high-contrast plates. |
| **5. Practice & Test-Retest Effects** | Early score gains reflect interface familiarity rather than genuine cognitive growth. | Chelune (1993) Reliable Change Index ($RCI \ge 1.96$); progress status requires session stability before celebrating growth. |
| **6. Small-Sample Noise** | Short sessions with $<10$ trials produce extreme variance and deceptive peaks. | Minimum trial thresholds per input; dashboard displays "Building your profile" until 30% coverage is achieved. |
| **7. Device & Motor Latency** | Touchscreens vs mechanical keyboards induce systematic motor latency differentials. | Automated low-effort flagging: reaction times $<150\text{ ms}$, timeout rates $>50\%$, or repetitive key presses $>90\%$. |

---

## 5. Machine Learning Architecture & Psychometric Modeling

### 5.1 Soft-Anchored Temporal JEPA (SAT-JEPA)

Predicting longitudinal cognitive progression requires modeling non-stationary human behavioral dynamics while preventing representation collapse.

```
x_t (Telemetry Features) ──────► [ Context Encoder f_θ ] ──────► s_t (Context Latent)
                                                                       │
                                                                       ▼
                                                             [ Leaky Integrator ]
                                                             s̄_t = a ⊙ s̄_{t-1} + (1-a) ⊙ e_t
                                                                       │
                                                                       ▼
x_{t+1} (Next Session)    ──────► [ Target Encoder f_θ̄ ] ──────► y_{t+1} (Target Latent)
                                       (EMA Updated, τ=0.996)
```

1. **Context Encoder ($f_\theta$):** Multi-Layer Perceptron (MLP) with LayerNorm and GELU activations mapping raw 14-dimensional session features $x_t$ into latent space $s_t \in \mathbb{R}^{32}$.
2. **Exponential Moving Average (EMA) Target Encoder ($f_{\bar{\theta}}$):** Weights are updated via momentum to provide a stable regression target:
   $$\bar{\theta}_t = \tau \bar{\theta}_{t-1} + (1 - \tau) \theta_t, \quad \tau = 0.996$$
3. **Learned Leaky Temporal Integrator:** Human cognitive adaptation exhibits temporal inertia. State memory evolves as:
   $$\bar{s}_t = a \odot \bar{s}_{t-1} + (1 - a) \odot e_t, \quad a = \sigma(\mathbf{w}_a)$$
4. **Soft-Anchor Regularizer:** Prevents representation collapse to trivial constant representations without requiring contrastive negative pairs:
   $$\mathcal{L}_{\text{anchor}} = \frac{1}{d} \sum_{j=1}^d \max(0, \gamma - \text{Var}(s_{:, j}))$$
5. **Conformal Uncertainty Prediction:** Forward projections provide calibrated split-conformal interval estimates:
   $$\hat{y}_{t+h} \pm q_{1-\alpha} \cdot \sqrt{\text{Var}_h}, \quad \text{Var}_h = a + b \cdot h$$

---

### 5.2 Bounded Dynamic GMM Clustering & Hysteresis Gating

Rather than forcing users into a static, arbitrary number of clusters, Loti uses **Bounded Dynamic Model Selection**:

1. **Optimal $k^*$ Selection:** Searches $k \in [k_{\min}, k_{\max}]$ (default $2 \le k \le 6$, up to 9) to minimize the Bayesian Information Criterion (BIC):
   $$\text{BIC}(k) = -2 \ln \hat{L} + p_k \ln N$$
2. **Cluster Mass Gate ($\text{min\_weight} \ge 0.05$):** Prevents the model from creating spurious, fragmented micro-clusters containing less than 5% of training samples.
3. **Schmitt-Trigger Hysteresis Gating:** To prevent oscillating between two neighboring archetypes (boundary chattering):
   $$\text{Switch to } k_{\text{new}} \iff \gamma(k_{\text{new}}) - \gamma(k_{\text{current}}) > \Delta_{\text{hyst}} \quad \text{for } N_{\text{confirm}} \ge 3 \text{ frames}$$
4. **Procedural Archetype Naming:** Archetypes are named dynamically based on dominant cognitive pillars (e.g., *Focus Strategist*, *Nimble Scout*, *Attentive Navigator*, *Balanced Builder*).

---

## 6. Procedural Task Synthesis & Hot-Pool Caching Engine

The `dynamic_cache/` service eliminates repetitive gameplay through algorithmic procedural synthesis:

```
[ Request Task ] ───► [ Hot-Pool Cache (<10ms) ] ───► [ Serve to Client ]
                             │
                      Low-Water Trigger
                             │
                             ▼
                  [ Background Worker ] ──► [ Procedural Generator ]
                                                   │
                                                   ▼
                                          [ Algorithmic Solver ]
                                          (Verifies Single Solution)
                                                   │
                                                   ▼
                                         [ TimedBloom Filter ]
                                         (Deduplicates Recent Tasks)
```

1. **Algorithmic Solvers:** Every procedurally generated task is validated by an internal solver prior to caching, guaranteeing that every presented problem has **exactly one valid solution**.
2. **TimedBloom Deduplication (`bloom.py`):** High-speed probabilistic Bloom filter preventing recently encountered problem configurations from being re-served to the same user.
3. **Hot-Pool Dispatching:** Pre-warmed priority queues indexed by difficulty step ($1–10$) deliver tasks in $<10\text{ ms}$ at p99.
4. **Adaptive Difficulty Staircasing (The 85% Rule):** Grounded in learning theory (Wilson et al., 2019), difficulty adjusts along calibrated Item Response Theory (IRT) staircases to target an optimal $85\%$ challenge-to-skill ratio.

---

## 7. Explainable AI Coach & Safety Architecture

Loti provides natural-language coaching through an axolotl companion bounded by a 4-tier defense-in-depth safety hierarchy:

```
[ Incoming User Message ]
          │
          ▼
[ Tier 1: Deterministic Keyword Crisis Gate ] ────► Tripped? ──► [ Emergency Crisis Redirect ]
          │ Safe
          ▼
[ Tier 2: Health Signposting Gate ]           ────► Tripped? ──► [ "I can't assess health. A doctor can." ]
          │ Safe
          ▼
[ Tier 3: LLM Backup Crisis Classifier ]      ────► Tripped? ──► [ Secondary Crisis Intervention ]
          │ Safe
          ▼
[ AI Coach LLM Generation ]
          │
          ▼
[ Tier 4: Output Banned-Terms Linter ]        ────► Tripped? ──► [ Withhold & Send Safe Fallback ]
          │ Clean
          ▼
[ Deliver Safe, Scannable Bubble Reply ]
```

### Dynamic AI Collaboration Scorer ($S_{\text{collab}}$)

Quantifies how effectively the user collaborates with the AI guide:
$$S_{\text{collab}} = \sum_{i=1}^5 w_i \cdot V_i, \quad \sum_{i=1}^5 w_i = 1.0$$

- **Clarification ($20\%$):** Proactively clarifying objectives before attempting complex tasks.
- **Critical Verification ($25\%$):** Autonomously checking answers rather than blindly accepting AI hints.
- **Iteration ($20\%$):** Adapting strategy following mistakes.
- **Autonomy ($20\%$):** Attempting exercises unprompted before requesting hints.
- **Responsible Use ($15\%$):** Adhering to rest boundaries and healthy pacing.

---

## 8. Verification, Performance Benchmarks & Accessibility

| Metric | Target / Benchmark | Achieved Result | Verification Method |
| :--- | :--- | :--- | :--- |
| **Hot Pool Task Latency** | $<10\text{ ms}$ p99 | **$0.48\text{ ms}$ p50 / $8.9\text{ ms}$ p99** | Asynchronous load generator (900 calls/s wave) |
| **Automated Test Coverage** | $>2,000$ tests | **3,100+ automated tests** | Vitest (1,460+ tests) + Pytest (1,650+ tests) |
| **WCAG Contrast Compliance** | WCAG 2.1 AA | **100% WCAG 2.1 AAA** | Automated `check:contrast` script (128 token pairs) |
| **UI Accessibility (a11y)** | 0 axe violations | **0 automated violations** | `@axe-core/playwright` end-to-end audit |
| **Dimensionality Generalisation**| 5 dimensions | **3, 6, 7, 8, and 10 dimensions** | Real-time `FULL_DIMENSION_POOL` dynamic switcher |
| **Privacy & Data Rights** | GDPR compliance | **100% Art 17 / Art 20** | Atomic JSONL export, erasure, 30-day retention |

---

## 9. Conclusion

Loti demonstrates that digital cognitive assessment does not require compromising between psychometric validity, user trust, and engineering performance. By combining procedural algorithmic generation, hardware-accurate timing, self-supervised representation learning (SAT-JEPA), and defense-in-depth safety guardrails, Loti establishes an open, production-ready foundation for the next generation of cognitive growth applications.

---

### Historical Acknowledgement

*Loti was originally conceived and engineered for the IEEE CISTAC 1.0 (AI4Brain) Challenge, organized by IEEE FSS SB Chapter, IEEE Tunisia Section, IEEE Computational Intelligence Society, and the Faculty of Sciences of Sfax. The comprehensive challenge-specific competition report and jury defense documentation are preserved in [`docs/archive/CISTAC_AI4Brain_Loti_Comprehensive_Report.md`](archive/CISTAC_AI4Brain_Loti_Comprehensive_Report.md).*
