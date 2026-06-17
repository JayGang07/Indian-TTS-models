import json, sys
sys.stdout.reconfigure(encoding='utf-8')
nb = json.load(open('Evaluating_TTS_models.ipynb', 'r', encoding='utf-8'))
for i, c in enumerate(nb['cells']):
    ct = c.get('cell_type', '?')
    src = ''.join(c.get('source', []))
    print(f"--- Cell {i} [{ct}] ---")
    print(src[:300])
    print()
