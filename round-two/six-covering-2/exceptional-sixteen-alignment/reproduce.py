"""Replay the two new six-class exclusions; root16:4 is not replayed here."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from phase_controls import NEW_ROOTS, OPEN_ROOT, controls, check_application

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
sys.path.insert(0, str(PARENT))
from check import check_tree


def require_domain(tree, root):
    if (tree.get('L'), tree.get('minimum'), tree.get('complete')) != (10080, 8, True):
        raise ValueError('Wrong period, minimum or incomplete tree')
    if tuple(map(tuple, tree['root_anchors'])) != root:
        raise ValueError('Wrong conditional root')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--generate', action='store_true')
    ap.add_argument('--generated', type=Path, default=HERE / 'generated')
    ap.add_argument('--require-manifest', action='store_true')
    ap.add_argument('--batches', type=int, default=16)
    args = ap.parse_args()
    if args.batches < 1:
        raise ValueError('Positive voluntary generation allowance required')
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
    for root in NEW_ROOTS:
        a = root[-1][1]
        path = args.generated / f'tree-exception-16-{a}.json'
        if args.generate:
            for batch in range(args.batches):
                outcome = subprocess.run([
                    sys.executable, '-B', str(PARENT / 'generate.py'),
                    '--prefix', ','.join(f'{m}:{b}' for m, b in root),
                    '--seconds', '180', '--nodes', '700', '--out', str(path)], env=env)
                if outcome.returncode not in (0, 2):
                    raise SystemExit(outcome.returncode)
                if path.exists() and json.loads(path.read_text()).get('complete'):
                    break
            else:
                raise SystemExit('INCOMPLETE: voluntary allowance exhausted; no exclusion asserted')
        tree = json.loads(path.read_text())
        require_domain(tree, root)
        results[str(a)] = json.loads(json.dumps(check_tree(tree)))
    phase_controls = json.loads(json.dumps(controls()))
    if phase_controls != expected['phase_controls']:
        raise ValueError('Complete physical phase controls differ')
    application = check_application(json.loads((HERE / 'application-next.json').read_text()))
    matched = results == expected['trees']
    if args.require_manifest and not matched:
        raise ValueError('Exact proof checks passed; author manifest differs')
    print(json.dumps({
        'agent': 'six-covering-2', 'role': 'researcher', 'period': 10080,
        'minimum_exactly': 8, 'author_manifest_match': matched,
        'directly_replayed_roots': [1, 2], 'credited_intrinsic_dependency': '8837',
        'proved': 'In the exceptional case, original16 is present with a16-a8=4mod8',
        'nodes': sum(r['nodes'] for r in results.values()),
        'expanded': sum(r['cuts']['expanded'] for r in results.values()),
        'raw_phases': sum(r['raw_branch_phases'] for r in results.values()),
        'positive_transports': sum(r['positive_transports'] for r in results.values()),
        'pair_entries': sum(r['pair_phase_entries'] for r in results.values()),
        'exceptional_six_tuples': phase_controls['exceptional_six_tuples'],
        'allowed_six_tuples': phase_controls['allowed_six_tuples'],
        'remaining_exception_root': OPEN_ROOT, 'remaining_root_status': 'OPEN',
        'open_comparison': application,
        'five_class_frontier': 14, 'global_numerical_improvement': False}, sort_keys=True))


if __name__ == '__main__':
    main()
