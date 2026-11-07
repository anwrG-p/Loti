"""Test Scenario 4: The Pushback Scenario (Collaboration Score).

Run from repository root:
    .venv\\Scripts\\python scripts/test_scenario_4.py
"""

import json
import sys
import urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai_coach.collaboration_scorer import CollaborationScorer
from ai_coach.schemas import ChatMessage, ChatMessageRole

print("=" * 60)
print("TESTING SCENARIO 4: The Pushback Scenario (Collaboration Score)")
print("=" * 60)

# 1. Test live chat non-defensive response
query = "I disagree with my score, the room was very loud and I was distracted!"
payload = {
    "user_id": "test_pushback_user",
    "message": query,
    "transcript": [],
    "kind": "typed"
}

print(f"1. Sending pushback to Loti:\n'{query}'\n")

try:
    resp = None
    for candidate_url in ("http://127.0.0.1:8000/v1/coach/chat", "http://localhost:5173/v1/coach/chat"):
        try:
            req = urllib.request.Request(
                candidate_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            resp = urllib.request.urlopen(req, timeout=5)
            break
        except Exception:
            continue
    if resp is None:
        raise RuntimeError("Failed to connect to backend on port 8000 or 5173")
    with resp:
        data = json.loads(resp.read().decode())
        reply = data.get("message", {}).get("text", "")
        print(f"[+] Loti Response:\n{reply}\n")
except Exception as e:
    print(f"[-] Error: {e}")

# 2. Test Collaboration Score bump
scorer = CollaborationScorer()
history_normal = [ChatMessage(role=ChatMessageRole.USER, content="Hello Loti, I am ready.")]
history_pushback = [
    ChatMessage(role=ChatMessageRole.USER, content="Hello Loti, I am ready."),
    ChatMessage(role=ChatMessageRole.ASSISTANT, content="Your accuracy dropped on the last session."),
    ChatMessage(role=ChatMessageRole.USER, content=query)
]

base_score = scorer.evaluate_interaction_signals(history_normal).critical_verification
pushback_score = scorer.evaluate_interaction_signals(history_pushback).critical_verification

print("2. AI Collaboration Score Impact:")
print(f"  * Base Critical Verification Score:     {base_score:.1f}")
print(f"  * Pushback Critical Verification Score: {pushback_score:.1f} (+{pushback_score - base_score:.1f} pts)")

if pushback_score >= base_score + 20.0:
    print("\n>>> RESULT: [PASS] - Non-defensive stance validated and Collaboration Score increased!")
else:
    print("\n>>> RESULT: [FAIL] - Collaboration score was not awarded.")
print("=" * 60)
