"""Generate six all-parameter E1 exclusions and the two-demand E2 cut."""
from datetime import datetime, timezone
import json
from pathlib import Path
import resource
import signal
import time

import deps
import model as M
import supplier_trees as T
import strip_contact_reader as R
import strip_local_pair_certificate as C
import strip_parametric_geometry as G
from strip_columns import require
from strip_point_suppliers import IDENTITY, finite_suppliers

HERE = Path(__file__).absolute().parent


def finite(entry, guard):
    fixed = (IDENTITY, R.freeze(entry['pose'])); points = R.freeze(entry['points'])
    suppliers = [finite_suppliers(p, fixed) for p in points]
    require(all(s['finite'] for s in suppliers), 'Growing supplier family retained')
    atlas = sorted(set().union(*(set(s['atlas']) for s in suppliers)))
    require(len(atlas) <= 128, '128-pose guard; incomplete work inconclusive')
    partition, samples, universal = C.matrices(fixed, atlas, points, guard)
    proof = C.cover_certificate(universal, len(points), guard)
    require(proof['rejected'], 'Conservative collar admits a cover')
    return {'agent': 'six-heesch-2', 'role': 'researcher', 'case': entry['name'], 'method': 'finite',
            'fixed': fixed, 'points': points, 'supplier_records': suppliers, 'atlas': atlas,
            'partition': partition, 'samples': samples, 'universal': universal, 'proof': proof,
            'complete': True}


def shift_cut(entries, guard):
    suppliers = [finite_suppliers(p, M.FIXED) for p in M.POINTS]
    require(all(s['finite'] for s in suppliers), 'Growing original-halo supplier family')
    atlas = sorted(set().union(*(set(s['atlas']) for s in suppliers)))
    require(len(atlas) <= 128, '128-pose guard; incomplete cut inconclusive')
    rows = M.predicates(atlas, entries)
    coverage, eligibility, clashes, demanded = rows
    partition = G.partition(M.flat(rows)); n = len(atlas)
    universal = {'cover': [0]*n, 'conflicts': [(1 << n)-1]*n, 'available': 0}
    samples = []
    for k in partition['representatives']:
        guard(); require(all(G.evaluate(p, k) for p in demanded), 'Not an original unfilled demand')
        cover = [sum(1 << j for j, p in enumerate(row) if G.evaluate(p, k)) for row in coverage]
        conflict = [1 << i for i in range(n)]
        for (i, j), predicate in clashes.items():
            if G.evaluate(predicate, k):
                conflict[i] |= 1 << j; conflict[j] |= 1 << i
        available = sum(1 << i for i, p in enumerate(eligibility) if cover[i] and G.evaluate(p, k))
        matrix = {'cover': cover, 'conflicts': conflict, 'available': available}
        samples.append({'k': k, 'matrix': matrix})
        universal['available'] |= available
        for i in range(n):
            universal['cover'][i] |= cover[i]; universal['conflicts'][i] &= conflict[i]
    proof = C.cover_certificate(universal, len(M.POINTS), guard)
    require(proof['rejected'], 'P branch has a conservative two-demand cover')
    return {'agent': 'six-heesch-2', 'role': 'researcher', 'fixed': M.FIXED, 'points': M.POINTS,
            'supplier_records': suppliers, 'atlas': atlas, 'partition': partition, 'samples': samples,
            'universal': universal, 'proof': proof, 'complete': True}


def main():
    start = time.monotonic(); calls = 0
    def guard():
        nonlocal calls
        calls += 1
        if deps.paused() or time.monotonic()-start >= 43 or calls > 100000:
            raise RuntimeError('Operational/43s/100000 guard; incomplete work inconclusive')
    def alarm(a, b): raise RuntimeError('45s signal guard; incomplete work inconclusive')
    signal.signal(signal.SIGALRM, alarm); signal.alarm(45)
    entries = json.loads((HERE/'inputs.json').read_text())['cases']
    mode = 'normal' if __debug__ else 'optimized'
    folder = HERE/'generated'/mode; folder.mkdir(parents=True, exist_ok=True)
    hashes = []
    for entry in entries:
        guard()
        if entry['method'] == 'finite': record = finite(entry, guard)
        else:
            fixed = (IDENTITY, R.freeze(entry['pose']))
            record = {'agent': 'six-heesch-2', 'role': 'researcher', 'case': entry['name'], 'method': 'tree',
                      'fixed': fixed, 'points': entry['points'],
                      'tree': T.build(T.freeze_plan(entry['plan']), fixed, guard), 'complete': True}
        (folder/f"{entry['name']}.json").write_text(json.dumps(record, indent=1)+'\n')
        hashes.append([entry['name'], R.sha(record)])
    record = shift_cut(entries, guard)
    (folder/'shift-cut.json').write_text(json.dumps(record, indent=1)+'\n')
    math = {'case_hashes': hashes, 'shift_cut_sha256': R.sha(record)}
    signal.alarm(0)
    out = {'agent': 'six-heesch-2', 'role': 'researcher', 'complete': True, 'evidence': math,
           'mathematics_sha256': R.sha(math), 'seconds': round(time.monotonic()-start, 3),
           'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
           'checked_utc': datetime.now(timezone.utc).isoformat()}
    (folder/'generator-summary.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'evidence'}), flush=True)


if __name__ == '__main__': main()
