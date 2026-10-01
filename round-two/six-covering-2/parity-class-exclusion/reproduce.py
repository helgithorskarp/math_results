"""Regenerate and literally check all four even-parity prefix exclusions."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from frontier import PHASES, EVEN_FORMS, controls, check_application

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
sys.path.insert(0, str(PARENT))
from check import check_tree

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--generate', action='store_true')
ap.add_argument('--generated', type=Path, default=HERE / 'generated')
ap.add_argument('--require-manifest', action='store_true',
                help='Also require the exact author-run manifest')
args = ap.parse_args()
args.generated.mkdir(parents=True, exist_ok=True)
expected = json.loads((HERE / 'manifest.json').read_text())
for filename, digest in expected['dependency_source_sha256'].items():
    if sha256((PARENT / filename).read_bytes()).hexdigest() != digest:
        raise ValueError('Dependency source differs: ' + filename)
env = os.environ.copy()
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    env[key] = '1'
results = {}
for phase, root in zip(PHASES, EVEN_FORMS):
    path = args.generated / f'tree-normal-0-0-{phase}.json'
    if args.generate:
        for batch in range(8):
            command = [sys.executable, '-B', str(PARENT / 'generate.py'), '--prefix',
                       ','.join(f'{m}:{a}' for m, a in root), '--seconds', '180',
                       '--nodes', '700', '--out', str(path)]
            outcome = subprocess.run(command, env=env)
            if outcome.returncode not in (0, 2):
                raise SystemExit(outcome.returncode)
            if path.exists() and json.loads(path.read_text()).get('complete'):
                break
        else:
            raise SystemExit('INCOMPLETE: voluntary batch allowance exhausted; no exclusion asserted')
    tree = json.loads(path.read_text())
    if (tree.get('L'), tree.get('minimum'), tree.get('complete')) != (10080, 8, True):
        raise ValueError('Wrong period, minimum or incomplete tree')
    if tuple(map(tuple, tree['root_anchors'])) != root:
        raise ValueError('Wrong prescribed prefix')
    results[str(phase)] = json.loads(json.dumps(check_tree(tree)))
phase_controls = controls()
if phase_controls != expected['affine_frontier']:
    raise ValueError('Complete affine frontier differs')
application = check_application(json.loads((HERE / 'application-next.json').read_text()))
if application != expected['application_next']:
    raise ValueError('Next application summary differs')
matched = results == expected['trees']
if args.require_manifest and not matched:
    raise ValueError('Author manifest differs; all four exact proof checks nevertheless passed')
print(json.dumps({'author': 'six-covering-2', 'role': 'researcher', 'period': 10080,
                  'proved': 'a present10/12/14 class has parity opposite to the8-class',
                  'author_manifest_match': matched,
                  'nodes': sum(r['nodes'] for r in results.values()),
                  'expanded': sum(r['cuts']['expanded'] for r in results.values()),
                  'raw_phases': sum(r['raw_branch_phases'] for r in results.values()),
                  'positive_transports': sum(r['positive_transports'] for r in results.values()),
                  'pair_entries': sum(r['pair_phase_entries'] for r in results.values()),
                  'new_removed_forms': 4, 'new_removed_physical_tuples': 15120,
                  'combined_removed_forms': 5, 'combined_removed_physical_tuples': 20160,
                  'remaining_forms': 19, 'application_next': application}, sort_keys=True))
