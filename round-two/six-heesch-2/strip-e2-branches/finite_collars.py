"""Uniform literal contact exclusions extracted from finite raw proofs.

Input points are hypotheses for the all-k reduction, not extrapolated facts:
complete supplier enumeration and exact critical cuts prove the reduction.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import signal
import sys
import time

H = Path(__file__).absolute().parent
import deps
import strip_local_pair_certificate as C
import strip_contact_reader as R
from strip_point_suppliers import finite_suppliers, IDENTITY


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', action='append')
    args = parser.parse_args()
    start = time.monotonic(); ops = Path('/scratch/research-team-sol61-six-20260929/state')
    def guard():
        if any((ops/n).exists() for n in ('PAUSED', 'PAUSED.json', 'HANDOVER.json')):
            raise RuntimeError('Operational pause barrier; unfinished proof inconclusive')
        if time.monotonic()-start >= 43:
            raise RuntimeError('43s work guard; unfinished proof inconclusive')
    def alarm(a, b):
        raise RuntimeError('45s signal guard; unfinished proof inconclusive')
    signal.signal(signal.SIGALRM, alarm); signal.alarm(45)
    inputs = json.loads((H/'inputs.json').read_text())
    mode = 'normal' if __debug__ else 'optimized'
    folder = H/'generated/finite'; folder.mkdir(parents=True,exist_ok=True)
    summary = []
    for entry in inputs['cases']:
        name = entry['name']
        if name not in ('side4','angle2_short_at_shift','reflection_at_shift'):
            continue
        if args.case and name not in args.case:
            continue
        guard(); fixed = (IDENTITY, R.freeze(entry['pose'])); points = R.freeze(entry['points'])
        suppliers = [finite_suppliers(p, fixed) for p in points]
        if not all(s['finite'] for s in suppliers):
            summary.append({'case': name, 'complete': False, 'reason': 'Growing supplier family retained'})
            print(json.dumps(summary[-1]), flush=True); continue
        atlas = sorted(set().union(*(set(s['atlas']) for s in suppliers)))
        if len(atlas) > 128:
            raise RuntimeError('128-pose memory guard; no mathematical rejection')
        part, samples, universal = C.matrices(fixed, atlas, points, guard)
        proof = C.cover_certificate(universal, len(points), guard)
        record = {'agent': 'six-heesch-2', 'role': 'researcher', 'case': name,
                  'fixed': fixed, 'points': points, 'supplier_records': suppliers, 'atlas': atlas,
                  'partition': part, 'samples': samples, 'universal': universal,
                  'proof': proof, 'individual': [], 'complete': proof['rejected'],
                  'scope': 'Only the literal uniform E1 exclusion; no full E2 inclusion or global upper'}
        if record['complete']:
            R.local_check(json.loads(json.dumps(record)), guard)
        else:
            record['individual'] = [{'k': s['k'], 'proof': C.cover_certificate(s['matrix'], len(points), guard)}
                                    for s in samples]
        record.update(source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      input_sha256=hashlib.sha256((H/'inputs.json').read_bytes()).hexdigest(),
                      checked_utc=datetime.now(timezone.utc).isoformat())
        (folder/f'{name}-{mode}.json').write_text(json.dumps(record, indent=2)+'\n')
        row = {'case': name, 'complete': record['complete'], 'points': len(points), 'atlas': len(atlas),
               'DAG_nodes': len(proof['nodes']), 'partition': part}
        summary.append(row); print(json.dumps(row), flush=True)
    guard(); signal.alarm(0)
    result = {'agent': 'six-heesch-2', 'role': 'researcher', 'cases': summary,
              'seconds': round(time.monotonic()-start, 3),
              'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'all_selected_complete': all(x['complete'] for x in summary),
              'mathematics_sha256': R.sha(summary)}
    (folder/f'summary-{mode}.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
