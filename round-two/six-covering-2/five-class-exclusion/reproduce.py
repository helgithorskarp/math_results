"""Regenerate when requested and exactly replay the complete five-class exclusion."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from normal_forms import controls, check_application, EXCLUDED

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
sys.path.insert(0, str(PARENT))
from check import check_tree, transport

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--generate', action='store_true')
ap.add_argument('--generated', type=Path, default=HERE / 'generated')
ap.add_argument('--require-manifest', action='store_true',
                help='Require the exact author-run manifest, in addition to a valid exact proof')
args = ap.parse_args()
args.generated.mkdir(parents=True, exist_ok=True)
expected = json.loads((HERE / 'manifest.json').read_text())
for filename, digest in expected['parent_source_sha256'].items():
    if sha256((PARENT / filename).read_bytes()).hexdigest() != digest:
        raise ValueError('Parent source differs from the declared publication: ' + filename)
env = os.environ.copy()
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    env[key] = '1'
results = {}
for phase in range(5):
    path = args.generated / f'tree-16-{phase}.json'
    if args.generate:
        for batch in range(8 if phase == 4 else 3):
            command = [sys.executable, '-B', str(PARENT / 'generate.py'), '--prefix',
                       '8:0,9:0,10:1,14:1,12:3,16:' + str(phase), '--seconds', '180',
                       '--nodes', '700', '--out', str(path)]
            outcome = subprocess.run(command, env=env)
            if outcome.returncode not in (0, 2):
                raise SystemExit(outcome.returncode)
            if path.exists() and json.loads(path.read_text()).get('complete'):
                break
        else:
            raise SystemExit('INCOMPLETE: batch allowance exhausted; no exclusion asserted')
    tree = json.loads(path.read_text())
    if (tree.get('L'), tree.get('minimum')) != (10080, 8):
        raise ValueError('Wrong period or minimum for the declared theorem')
    if tuple(map(tuple, tree['root_anchors'])) != EXCLUDED + ((16, phase),):
        raise ValueError('Wrong conditional root')
    results[str(phase)] = json.loads(json.dumps(check_tree(tree)))
bins = {str(b): [a for a in range(16) if transport(10080, EXCLUDED, 16, a, b) is not None]
        for b in range(5)}
if bins != {'0': [0, 8], '1': [1, 5, 9, 13], '2': [2, 6, 10, 14],
            '3': [3, 7, 11, 15], '4': [4, 12]}:
    raise ValueError('Incomplete modulus16 classification')
forms = controls()
if forms != expected['affine_controls']:
    raise ValueError('Complete affine reduction changed')
application = check_application(json.loads((HERE / 'application-root.json').read_text()))
matched = results == expected['trees']
if args.require_manifest and not matched:
    raise ValueError('Author manifest differs; all roots still passed exact proof checks')
print(json.dumps({'author': 'six-covering-2', 'role': 'researcher', 'period': 10080,
                  'proved': 'five-class prefix excluded; complete reduction leaves23 normal forms',
                  'author_manifest_match': matched,
                  'nodes': sum(r['nodes'] for r in results.values()),
                  'expanded': sum(r['cuts']['expanded'] for r in results.values()),
                  'raw_phases': sum(r['raw_branch_phases'] for r in results.values()),
                  'positive_transports': sum(r['positive_transports'] for r in results.values()),
                  'pair_entries': sum(r['pair_phase_entries'] for r in results.values()),
                  'affine_raw_tuples': forms['raw_phase_tuples'],
                  'excluded_raw_tuples': forms['excluded_raw_tuples'], 'remaining_forms': 23,
                  'application_root': application},
                 sort_keys=True))
