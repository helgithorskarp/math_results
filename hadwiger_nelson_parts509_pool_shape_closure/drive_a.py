#!/usr/bin/env python3
"""Run the pool-restricted delete-(a+1)-add-a closures for increasing a, accumulating
every killing set found so that later values start from a stronger family."""
import json, subprocess, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
PY = '/scratch/researcher-5-venv/bin/python'
avals = [int(x) for x in sys.argv[1].split(',')]
tl = float(sys.argv[2])
tag = sys.argv[3] if len(sys.argv) > 3 else ''
acc = HERE / 'accumulated_killing_sets.jsonl'
rf = HERE / f'a_closure_results{tag}.json'
results = json.loads(rf.read_text()) if rf.exists() else {}
for a in avals:
    out = HERE / f'ihs_a{a}{tag}'
    cmd = [PY, str(HERE / 'ihs_a.py'), '--a', str(a), '--out', str(out),
           '--time-limit', str(tl), '--family', str(HERE / 'family_min.json')]
    if acc.exists():
        cmd += ['--extra', str(acc)]
    t = time.time()
    print(f'=== a={a} start {time.strftime("%H:%M:%S")}', flush=True)
    subprocess.run(cmd, stdout=open(HERE / f'ihs_a{a}{tag}.log', 'w'), stderr=subprocess.STDOUT)
    r = json.loads((out / 'result.json').read_text()) if (out / 'result.json').exists() else {'result': 'crash'}
    r['wall'] = time.time() - t
    results[str(a)] = r
    rf.write_text(json.dumps(results, indent=1))
    nk = out / 'new_killing_sets.jsonl'
    if nk.exists():
        with acc.open('a') as f:
            f.write(nk.read_text())
    print(f'=== a={a} -> {r["result"]} in {r["wall"]:.0f}s', flush=True)
    if r['result'] == 'record':
        print('RECORD FOUND, stopping')
        break
