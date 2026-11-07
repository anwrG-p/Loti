"""Interactive & Dynamic Test for Scenario 1 (The Button Masher Anomaly).

Usage:
  # 1. Custom Reaction Time & error test:
  .venv\\Scripts\\python scripts/test_scenario_1.py --rt 850 --error false
  .venv\\Scripts\\python scripts/test_scenario_1.py --rt 95  --error true

  # 2. Inspect real browser telemetry files recorded from the web UI:
  .venv\\Scripts\\python scripts/test_scenario_1.py --inspect

  # 3. Run automated side-by-side comparison (deliberate vs masher):
  .venv\\Scripts\\python scripts/test_scenario_1.py --compare
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TELEMETRY_DIR = Path("data/raw/telemetry")
API_URL = "http://localhost:5173/v1/telemetry/event"


def inspect_live_telemetry():
    """Inspect all telemetry records in data/raw/telemetry/ from browser or scripts."""
    print("=" * 65)
    print("INSPECTING STORED TELEMETRY IN data/raw/telemetry/")
    print("=" * 65)
    jsonl_files = list(TELEMETRY_DIR.glob("*.jsonl"))
    if not jsonl_files:
        print("No telemetry files found in data/raw/telemetry/ yet.")
        print("Note: In the browser UI, click 'Save my answers' / 'Grant consent' to flush browser events.")
        return

    for f in jsonl_files:
        lines = [line.strip() for line in f.read_text(encoding="utf-8").strip().split("\n") if line.strip()]
        print(f"\n[File: {f.name}] ({len(lines)} total trials)")
        rts = []
        errors = 0
        anomalies = []
        for line in lines:
            try:
                row = json.loads(line)
                rt = row.get("response_time_ms", 0.0)
                rts.append(rt)
                if row.get("error_flag"):
                    errors += 1
                if row.get("anomaly_flag"):
                    anomalies.append(row.get("anomaly_flag"))
            except Exception:
                pass
        
        avg_rt = sum(rts) / max(1, len(rts))
        print(f"  * Average Reaction Time: {avg_rt:.1f} ms (Min: {min(rts) if rts else 0:.1f} ms, Max: {max(rts) if rts else 0:.1f} ms)")
        print(f"  * Total Errors:          {errors} / {len(rts)} trials")
        print(f"  * Anomalies Flagged:     {set(anomalies) if anomalies else 'None (Clean)'}")
        print("  * Latest trial preview: ", lines[-1][:120], "...")
    print("=" * 65)


def send_trial(rt_ms: float, is_error: bool, user_id: str = "dynamic_test_user"):
    """Send a single trial with custom RT and error flag through the live API."""
    user_file = TELEMETRY_DIR / f"{user_id}.jsonl"
    if user_file.exists():
        user_file.unlink()

    payload = {
        "user_id": user_id,
        "session_id": "interactive_session",
        "task_id": "matrix",
        "trial_index": 0,
        "dimension": "pattern_induction",
        "score_norm": 0.0 if is_error else 1.0,
        "response_time_ms": float(rt_ms),
        "error_flag": bool(is_error),
        "error_burst": 4 if is_error and rt_ms < 220 else (1 if is_error else 0),
        "hesitation_jitter": 2.0,
        "client_ts": "2026-11-07T00:00:00Z",
    }

    print(f"\n>> Sending Trial to API: RT={rt_ms}ms, Error={is_error}")
    sent = False
    for url in ("http://127.0.0.1:8000/v1/telemetry/event", API_URL):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status == 202:
                    sent = True
                    break
        except Exception:
            continue
    assert sent, "Failed to connect to backend on port 8000 or 5173"

    # Read back what the server stored
    saved = json.loads(user_file.read_text(encoding="utf-8").strip())
    flag = saved.get("anomaly_flag")
    conf = saved.get("confidence_score")
    unc = saved.get("uncertainty_weight")

    print(f">> Server Ingest Result:")
    print(f"   - Stored Anomaly Flag:    {flag}")
    print(f"   - Stored Confidence:      {conf}")
    print(f"   - Stored Uncertainty Wt:  {unc}")

    if rt_ms < 220 and is_error:
        if flag == "button_masher":
            print("   => [PASS] Button Masher detected! High uncertainty applied.")
        else:
            print("   => [FAIL] Button Masher was not detected.")
    else:
        if flag is None:
            print("   => [PASS] Normal response correctly processed with no false alarm.")
        else:
            print("   => [FAIL] Normal trial was falsely flagged as an anomaly!")


def compare_modes():
    """Run side-by-side comparison of normal vs mashing."""
    print("=" * 65)
    print("SIDE-BY-SIDE COMPARISON: DELIBERATE vs BUTTON MASHER")
    print("=" * 65)
    print("Test 1: Deliberate Thoughtful User (RT = 720ms, Correct)")
    send_trial(rt_ms=720.0, is_error=False, user_id="user_deliberate")

    print("\nTest 2: Deliberate Thoughtful User Making an Error (RT = 850ms, Wrong)")
    send_trial(rt_ms=850.0, is_error=True, user_id="user_honest_error")

    print("\nTest 3: Rapid Button Masher (RT = 85ms, Wrong)")
    send_trial(rt_ms=85.0, is_error=True, user_id="user_rapid_masher")
    print("=" * 65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Scenario 1 (Button Masher)")
    parser.add_argument("--rt", type=float, default=None, help="Custom reaction time in ms")
    parser.add_argument("--error", type=str, default="true", help="Whether trial was an error (true/false)")
    parser.add_argument("--inspect", action="store_true", help="Inspect real telemetry saved from browser UI")
    parser.add_argument("--compare", action="store_true", help="Run automated side-by-side comparison")

    args = parser.parse_args()

    if args.inspect:
        inspect_live_telemetry()
    elif args.compare or args.rt is None:
        compare_modes()
    else:
        err = args.error.lower() in ("true", "1", "yes")
        send_trial(args.rt, err)
