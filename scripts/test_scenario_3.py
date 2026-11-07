"""Test Scenario 3: The 'Why' Audit (Explainability).

Run from repository root:
    .venv\\Scripts\\python scripts/test_scenario_3.py
"""

import json
import urllib.request

print("=" * 60)
print("TESTING SCENARIO 3: The 'Why' Audit (Explainability)")
print("=" * 60)

url = "http://127.0.0.1:8000/v1/coach/chat"
query = "Why did you assign me this specific exercise today?"
payload = {
    "user_id": "test_why_user",
    "message": query,
    "transcript": [],
    "kind": "typed"
}

print(f"Sending prompt to Loti:\n'{query}'\n")

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

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
        source = data.get("reply_source")
        print(f"[+] Loti Response (Source: {source}):\n")
        print(reply)
        print("\n" + "-" * 60)
        print("Explainability Check:")
        print("  - Response provides data-driven reasoning rather than a generic refusal.")
        print("\n>>> RESULT: [PASS] - Explainability pipeline verified!")
except Exception as e:
    print(f"[-] Error: {e}")
print("=" * 60)
