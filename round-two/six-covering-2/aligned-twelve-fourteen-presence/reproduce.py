"""Exact full-F replay and the original14 bridge; generated trees stay local."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
N = 10080
ROOT = ((8, 0), (9, 0), (10, 1), (14, 0), (12, 4))


def require_domain(tree):
    if (type(tree.get('L')) is not int or tree['L'] != N
            or type(tree.get('minimum')) is not int or tree['minimum'] != 8
            or tree.get('complete') is not True):
        raise ValueError('Wrong period/minimum or incomplete certificate')
    anchors = tree.get('root_anchors')
    if (type(anchors) is not list or any(type(row) is not list or len(row) != 2
            or any(type(x) is not int for x in row) for row in anchors)
            or anchors != [list(row) for row in ROOT]):
        raise ValueError('Wrong prescribed five-class domain')


def application_data():
    from frontier_fourteen import REMAINING
    cases = []
    for root in REMAINING:
        mask = sum(1 << x for x in range(N) if all(x % m != a for m, a in root))
        cases.append({'root': root, 'residual': mask.bit_count(),
                      'residual_bitset_hex': hex(mask)[2:], 'proof_status': 'OPEN'})
    return json.loads(json.dumps({
        'period': N, 'minimum_exactly': 8,
        'all_unused_moduli': [m for m in range(8, N + 1)
                             if N % m == 0 and m not in dict(ROOT)],
        'four_top_resources': [288, 1440, 2016, 10080], 'top_phases': 'ALL FREE',
        'roots': cases}))


def require_applications(data):
    if data != application_data():
        raise ValueError('Wrong remaining roots, literal residuals or original resource pool')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--generate', action='store_true')
    ap.add_argument('--tree', type=Path, default=HERE / 'generated/tree-F.json')
    ap.add_argument('--batches', type=int, default=12,
                    help='Finite voluntary allowance; each batch remains180s/700new nodes')
    ap.add_argument('--require-manifest', action='store_true')
    ap.add_argument('--controls-only', action='store_true')
    args = ap.parse_args()
    if args.batches < 1 or args.controls_only and args.generate:
        raise ValueError('Invalid voluntary allowance or incompatible modes')
    expected = json.loads((HERE / 'manifest.json').read_text())
    for filename, digest in expected['dependency_source_sha256'].items():
        if sha256((PARENT / filename).read_bytes()).hexdigest() != digest:
            raise ValueError('Dependency source changed: ' + filename)
    from frontier_fourteen import controls
    frontier = json.loads(json.dumps(controls()))
    if frontier != expected['affine_frontier']:
        raise ValueError('Complete intrinsic/affine controls differ')
    require_applications(json.loads((HERE / 'application-next.json').read_text()))
    if args.controls_only:
        print(json.dumps({'status': 'CONTROLS ONLY; no certificate replay or exclusion asserted',
                          'phase_tuples': frontier['physical_phase_tuples'],
                          'remaining_forms': frontier['remaining_forms']}, sort_keys=True))
        return
    if args.generate:
        args.tree.parent.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ)
        for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
                    'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
            env[key] = '1'
        for _ in range(args.batches):
            command = [sys.executable, '-B', str(PARENT / 'generate.py'),
                       '--prefix', ','.join(f'{m}:{a}' for m, a in ROOT),
                       '--seconds', '180', '--nodes', '700', '--out', str(args.tree)]
            result = subprocess.run(command, env=env)
            if result.returncode not in (0, 2):
                raise SystemExit(result.returncode)
            if args.tree.exists() and json.loads(args.tree.read_text()).get('complete'):
                break
        else:
            raise SystemExit('INCOMPLETE: allowance exhausted; no exclusion asserted')
    tree = json.loads(args.tree.read_text())
    require_domain(tree)
    sys.path.insert(0, str(PARENT))
    from check import check_tree
    result = json.loads(json.dumps(check_tree(tree)))
    matched = result == expected['tree']
    if args.require_manifest and not matched:
        raise ValueError('Exact certificate passed; author manifest differs')
    print(json.dumps({'agent': 'six-covering-2', 'role': 'researcher',
                      'status': 'FULL F EXCLUDED; original14 bridge uses credited8728/9065',
                      'period': N, 'minimum_exactly': 8, 'excluded_root': ROOT,
                      'nodes': result['nodes'],
                      'strict_leaves': result['nodes'] - result['cuts']['expanded'],
                      'remaining_five_class_forms': frontier['remaining_forms'],
                      'author_manifest_match': matched, 'global_numerical_improvement': False,
                      'written_bridge': 'unformalized; see proof.md'}, sort_keys=True))


if __name__ == '__main__':
    main()
