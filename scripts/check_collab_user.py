import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'backend')

from ai_coach.collaboration_scorer import CollaborationScorer, EVIDENCE_MARKERS
from ai_coach import chat_store

turns = chat_store.read_turns('28876ecf-7bde-4854-b70d-a4696be11788')
typed = [r['text'] for r in turns if r.get('from') == 'you' and r.get('kind') == 'typed']
print('Typed count:', len(typed))
for i, t in enumerate(typed, 1):
    print(f"  {i}. {t}")

texts = [t.lower().replace("’", "'") for t in typed]
marked = {dim: sum(1 for t in texts if rx.search(t)) for dim, rx in EVIDENCE_MARKERS.items()}
print('\nMarked dimensions count:', marked)

res = CollaborationScorer().score_stored_history(typed)
print('\nCurrent CollaborationScorer output:', res)
