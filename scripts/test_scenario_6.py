"""Test Scenario 6: The Asymmetrical Mind (Generalisation).

Run from repository root:
    .venv\\Scripts\\python scripts/test_scenario_6.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dynamic_cache.asymmetrical_planner import AsymmetricalPlanner

print("=" * 60)
print("TESTING SCENARIO 6: The Asymmetrical Mind (Generalisation)")
print("=" * 60)

# Profile with huge variance: Flawless Focus (95), Failing Agility (32)
profile = {
    "focus": 95.0,
    "agility": 32.0,
    "impulse": 55.0,
    "memory": 52.0,
    "visual": 50.0,
}

print("Evaluating asymmetrical profile:")
for k, v in profile.items():
    print(f"  * {k.title():<10}: {v:.1f}")

planner = AsymmetricalPlanner()
res = planner.evaluate_profile(profile)

print(f"\n[+] Analysis Results:")
print(f"  * Is Asymmetrical: {res.is_asymmetrical} (Spread: {res.spread:.1f} pts)")
print(f"  * Radar Split:     Advanced: {res.radar_split['advanced']}, Foundational: {res.radar_split['foundational']}")

print("\n[+] Prescriptions (Split difficulty vs. generic average):")
for p in res.prescriptions:
    print(f"  - {p.dimension.upper():<10}: Tier={p.tier:<12} Prescribed Theta={p.prescribed_theta:.2f}")

presc_map = {p.dimension: p for p in res.prescriptions}
if presc_map["focus"].tier == "advanced" and presc_map["agility"].tier == "foundational":
    print("\n>>> RESULT: [PASS] - Successfully split difficulty into Advanced strengths and Foundational support!")
else:
    print("\n>>> RESULT: [FAIL] - Curriculum collapsed to generic average.")
print("=" * 60)
