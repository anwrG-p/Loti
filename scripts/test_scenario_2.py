"""Test Scenario 2: The Stagnation Plateau (Layer C).

Run from repository root:
    .venv\\Scripts\\python scripts/test_scenario_2.py
"""

import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dynamic_cache.stagnation import StagnationPlateauDetector

print("=" * 60)
print("TESTING SCENARIO 2: The Stagnation Plateau (Layer C)")
print("=" * 60)

detector = StagnationPlateauDetector()

# 1. Normal progressing user
prog_scores = [0.45, 0.52, 0.60, 0.68, 0.74, 0.82]
res_prog = detector.analyze_scores(prog_scores)
print("[+] Testing progressing scores:", prog_scores)
print(f"  * Is Stagnant: {res_prog.is_stagnant} (expected: False)")

# 2. Flatlined performance (stagnation)
flat_scores = [0.55, 0.551, 0.549, 0.550, 0.552, 0.548]
res_stag = detector.analyze_scores(flat_scores)
print("\n[+] Testing flatline scores across 6 sessions:", flat_scores)
print(f"  * Is Stagnant:          {res_stag.is_stagnant} (expected: True)")
print(f"  * Rolling Variance:     {res_stag.rolling_variance:.6f} (expected: < 0.001)")
print(f"  * Trend Slope:          {res_stag.trend_slope:.6f} (expected: ~0.0)")
print(f"  * Recommended Action:   {res_stag.recommended_action} (expected: 'switch_exercise_format')")
print(f"  * Suggested Strategy:   {res_stag.suggested_strategy}")

if res_stag.is_stagnant and res_stag.recommended_action == "switch_exercise_format":
    print("\n>>> RESULT: [PASS] - Stagnation Plateau detected and task loop broken!")
else:
    print("\n>>> RESULT: [FAIL] - Failed to detect stagnation.")
print("=" * 60)
