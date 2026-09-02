#!/usr/bin/env python3
"""Upper-bound search in the sealed S-pool: start from a valid X = Y ∪ Q5 (Y ⊆ S hitting the
S-only family, grown to validity), then repeated greedy removal sweeps (Q5 points first, then
S vertices; random orders) until a full sweep removes nothing.  Φ(X) := L ∪ X not 4-colourable
(20 interface patterns, one SAT call each).  Any final |X| < 135 would be a 5-chromatic
unit-distance graph L ∪ X with fewer than 509 vertices."""
import json, random, sys, time, argparse
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from sgadget import SGadget
ap = argparse.ArgumentParser()
ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--state', default='ihs_Sonly/state.json')
ap.add_argument('--out', default='minpool')
ap.add_argument('--start', default=None, help='json file with X to start from')
ap.add_argument('--order', default='q5first', choices=['q5first','mixed','sfirst','freq'])
ap.add_argument('--family', default=None, help="for --order freq: killing-set family (jsonl) whose vertex frequencies order the S sweep (rare first)")
ap.add_argument('--protect-q5', action='store_true', help='never remove Q5 points (S-only minimisation: upper bound on h_S)')
args = ap.parse_args()
rng = random.Random(args.seed)
from pathlib import Path
out = Path(args.out); out.mkdir(exist_ok=True)
g = SGadget()
S = set(g.S135); Q5 = set(g.Q5)
def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)
if args.start:
    X = set(json.load(open(args.start))['X'])
else:
    hs = set(json.load(open(args.state))['hs'])
    X = hs | Q5
    p = g.find_sat_pattern(sorted(X), rng)
    while p is not None:
        D, _ = g.minimal_killing(g.Uset - X, p, rng)
        X |= set(D)
        p = g.find_sat_pattern(sorted(X), rng)
    log(f'grown start: |X|={len(X)} (S {len(X & S)}, Q5 {len(X & Q5)})')
assert g.phi(sorted(X))
sweep = 0
while True:
    sweep += 1
    removed = 0
    order = sorted(X & Q5); rng.shuffle(order)
    order2 = sorted(X & S); rng.shuffle(order2)
    if args.order == 'freq':
        freq = {}
        for line in open(args.family):
            if line.strip():
                for v in json.loads(line)['D']:
                    freq[v] = freq.get(v, 0) + 1
        order2.sort(key=lambda v: (freq.get(v, 0), rng.random()))
        seq = order2 + order
    else:
        seq = order + order2 if args.order == 'q5first' else order2 + order if args.order == 'sfirst' else rng.sample(order + order2, len(order) + len(order2))
    for v in seq:
        if v not in X: continue
        if args.protect_q5 and v in Q5: continue
        if len(g.adj[v] & (X | set(g.L))) <= 3:  # degree rule: always removable
            X.discard(v); removed += 1; continue
        if g.phi(sorted(X - {v})):
            X.discard(v); removed += 1
            log(f'  sweep {sweep}: removed {v} ({"Q5" if v in Q5 else "S"}), |X|={len(X)} (S {len(X & S)}, Q5 {len(X & Q5)})')
    log(f'sweep {sweep} done: removed {removed}; |X|={len(X)} (S {len(X & S)}, Q5 {len(X & Q5)}); sat calls {g.calls}, sat time {g.time:.0f}s')
    (out / f'seed{args.seed}_current.json').write_text(json.dumps({'X': sorted(X), 'size': len(X), 'S': len(X & S), 'Q5': len(X & Q5), 'sweep': sweep}))
    if removed == 0:
        break
assert g.phi(sorted(X))
log(f'FINAL |X|={len(X)} (S {len(X & S)}, Q5 {len(X & Q5)}); record={len(X) < 135}')
(out / f'seed{args.seed}_final.json').write_text(json.dumps({'X': sorted(X), 'size': len(X), 'S': len(X & S), 'Q5': len(X & Q5), 'record': len(X) < 135}))
