"""Regenerate and literally replay the two new exceptional-alignment exclusions."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from frontier_alignment import NEW_FORMS, controls

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
sys.path.insert(0, str(PARENT))
from check import check_tree

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--generate', action='store_true')
ap.add_argument('--generated', type=Path, default=HERE / 'generated')
ap.add_argument('--require-manifest', action='store_true')
args = ap.parse_args()
expected = json.loads((HERE / 'manifest.json').read_text())
for filename, digest in expected['dependency_source_sha256'].items():
    if sha256((PARENT / filename).read_bytes()).hexdigest() != digest:
        raise ValueError('Dependency source changed: ' + filename)
args.generated.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
            'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    env[key] = '1'
results = {}
for root in NEW_FORMS:
    d = root[4][1]
    path = args.generated / f'tree-normal-0-1-{d}.json'
    if args.generate:
        for batch in range(8):
            command = [sys.executable, '-B', str(PARENT / 'generate.py'),
                       '--prefix', ','.join(f'{m}:{a}' for m, a in root),
                       '--seconds', '180', '--nodes', '700', '--out', str(path)]
            outcome = subprocess.run(command, env=env)
            if outcome.returncode not in (0, 2):
                raise SystemExit(outcome.returncode)
            if path.exists() and json.loads(path.read_text()).get('complete'):
                break
        else:
            raise SystemExit('INCOMPLETE: voluntary allowance exhausted; no theorem asserted')
    tree = json.loads(path.read_text())
    if (tree.get('L'), tree.get('minimum'), tree.get('complete')) != (10080, 8, True):
        raise ValueError('Wrong period, minimum or incomplete tree')
    if tuple(map(tuple, tree['root_anchors'])) != root:
        raise ValueError('Wrong conditional root')
    results[str(d)] = json.loads(json.dumps(check_tree(tree)))
phase_controls = controls()
if phase_controls != expected['affine_frontier']:
    raise ValueError('Complete affine frontier differs')
matched = results == expected['trees']
if args.require_manifest and not matched:
    raise ValueError('Exact proof checks passed; author manifest differs')
print(json.dumps({'author': 'six-covering-2', 'role': 'researcher', 'period': 10080,
                  'proved_roots': [str(d) for d in (4, 6)],
                  'intrinsic_lemma': 'If no present10 opposes8 parity and12 has8 parity, '
                                     '14 is present/opposite8,9 is present/different12mod3, '
                                     'and12 equals8+2mod4',
                  'intrinsic_dependencies': ['8680', '8728'],
                  'author_manifest_match': matched,
                  'nodes': sum(r['nodes'] for r in results.values()),
                  'expanded': sum(r['cuts']['expanded'] for r in results.values()),
                  'raw_phases': sum(r['raw_branch_phases'] for r in results.values()),
                  'positive_transports': sum(r['positive_transports'] for r in results.values()),
                  'pair_entries': sum(r['pair_phase_entries'] for r in results.values()),
                  'new_removed_forms': 2, 'new_removed_tuples': 7560,
                  'combined_removed_forms': 10, 'combined_removed_tuples': 35280,
                  'remaining_forms': 14,
                  'exception_root_status': 'OPEN; not replayed by this wrapper'}, sort_keys=True))
