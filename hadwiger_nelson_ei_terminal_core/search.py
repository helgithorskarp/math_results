"""Optional bounded discovery reproduction, with all generated state private."""
import json, time, argparse
from pathlib import Path
from itertools import combinations
from pysat.solvers import Cadical195
import geometry as G
from source_audit import parent
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
O = args.output.resolve()
G.require(not O.is_relative_to(G.ROOT.parent.resolve()), 'output must be outside repository')
O.mkdir(parents=True, exist_ok=True)
rows = parent()
n = len(rows)
es = G.half_edges(rows)
pins = [rows.index(p) for p in [(0, 0, 0, 0), (0, 0, 96, 0)]]
start = time.monotonic()
cs = []
for i in range(n):
    cs.append([-(4 * n + i + 1)] + [4 * i + c + 1 for c in range(4)])
    cs.extend(([-(4 * i + c + 1), -(4 * i + d + 1)] for c, d in combinations(range(4), 2)))
for a, b in es:
    cs.extend(([-(4 * a + c + 1), -(4 * b + c + 1)] for c in range(4)))
cs.extend([[4 * pins[0] + 1], [4 * pins[1] + 2]])
s = Cadical195(bootstrap_with=cs)
s.conf_budget(200000)
r = s.solve_limited(assumptions=list(range(4 * n + 1, 5 * n + 1)))
print('initial', r, s.accum_stats(), time.monotonic() - start, flush=True)
if r is not False:
    raise ValueError('initial equality gate not proven')
keep = set((v - 4 * n - 1 for v in s.get_core())) | set(pins)
degrees = [0] * n
for a, b in es:
    degrees[a] += 1
    degrees[b] += 1
order = sorted(keep - set(pins), key=lambda v: (degrees[v], v))
history = []
words = {}
spent = 0
print('core', len(keep), 'initial queries', len(order), flush=True)
for v in order:
    if v not in keep:
        continue
    if spent >= 2000000:
        break
    trial = keep - {v}
    before = s.accum_stats()['conflicts']
    s.conf_budget(min(10000, 2000000 - spent))
    r = s.solve_limited(assumptions=[4 * n + i + 1 for i in sorted(trial)])
    spent += s.accum_stats()['conflicts'] - before
    if r is False:
        keep = set((i - 4 * n - 1 for i in s.get_core())) | set(pins)
    elif r:
        positive = {a for a in s.get_model() if a > 0}
        word = ''.join((str(next((c for c in range(4) if 4 * i + c + 1 in positive), 0)) for i in range(n)))
        if not all((word[a] != word[b] for a, b in es if a in trial and b in trial)):
            raise ValueError('invalid witness')
        words[str(v)] = word
    history.append({'removed': v, 'answer': r, 'retained': len(keep), 'spent': spent})
    result = {'retained': sorted(keep), 'pins': pins, 'history': history, 'words': words, 'spent': spent, 'elapsed': time.monotonic() - start, 'stats': s.accum_stats(), 'initial_order': order}
    temporary = O / 'reduction.pending.json'
    temporary.write_text(json.dumps(result, separators=(',', ':')))
    temporary.replace(O / 'reduction.json')
    if len(history) % 20 == 0 or r is None:
        print('progress', len(history), r, 'keep', len(keep), 'spent', spent, 'sec', round(time.monotonic() - start, 1), flush=True)
print('done', len(keep), len(history), 'unknown', sum((h['answer'] is None for h in history)), spent, time.monotonic() - start, flush=True)
active = set(keep)
adj = {v: set() for v in active}
peeled = []
for a, b in es:
    if a in active and b in active:
        adj[a].add(b)
        adj[b].add(a)
while True:
    candidates = [v for v in active - set(pins) if len(adj[v]) <= 3]
    if not candidates:
        break
    v = min(candidates)
    active.remove(v)
    peeled.append(v)
    for w in adj[v]:
        adj[w].remove(v)
G.require(sorted(active) == G.read('source_certificate.json')['retained_source_indices'], 'bounded search result differs')
(O / 'peeling.json').write_text(json.dumps({'peeled': peeled, 'remaining': sorted(active)}, indent=2) + '\n')
print(json.dumps({'retained_after_peeling': len(active), 'peeled': len(peeled), 'certificate_reproduced': True}, sort_keys=True))
