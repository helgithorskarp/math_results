"""Replay the odd16 exclusion and its exact two-child original-class bridge."""
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
P = ((8, 0), (9, 0), (10, 1), (14, 0), (12, 4))
ROOT = P + ((16, 1),)


def require_domain(tree):
    if (type(tree.get('L')) is not int or tree['L'] != N or
            type(tree.get('minimum')) is not int or tree['minimum'] != 8 or
            tree.get('complete') is not True):
        raise ValueError('Wrong period, minimum or incomplete tree')
    if tuple(map(tuple, tree['root_anchors'])) != ROOT:
        raise ValueError('Wrong prescribed six-class root')


def application_data():
    cases = []
    for a in (2, 4):
        root = P + ((16, a),)
        mask = sum(1 << x for x in range(N) if all(x % m != b for m, b in root))
        cases.append({'root': root, 'residual': mask.bit_count(),
                      'residual_bitset_hex': hex(mask)[2:], 'proof_status': 'OPEN'})
    return json.loads(json.dumps({
        'period': N, 'minimum_exactly': 8, 'parent_prefix': P,
        'parent_residual': sum(all(x % m != a for m, a in P) for x in range(N)),
        'all_unused_moduli': [m for m in range(8, N + 1)
                             if N % m == 0 and m not in dict(ROOT)],
        'four_top_resources': [288, 1440, 2016, 10080], 'top_phases': 'ALL FREE',
        'roots': cases}))


def require_applications(data):
    if data != application_data():
        raise ValueError('Wrong residual, remaining root or complete resource pool')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--generate', action='store_true')
    ap.add_argument('--tree', type=Path, default=HERE / 'generated/tree-sixteen-one.json')
    ap.add_argument('--batches', type=int, default=12,
                    help='Voluntary allowance; each batch remains180s/700new nodes')
    ap.add_argument('--require-manifest', action='store_true')
    args = ap.parse_args()
    if args.batches < 1:
        raise ValueError('Positive voluntary allowance required')
    expected = json.loads((HERE / 'manifest.json').read_text())
    for filename, digest in expected['dependency_source_sha256'].items():
        if sha256((PARENT / filename).read_bytes()).hexdigest() != digest:
            raise ValueError('Dependency source changed: ' + filename)
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
            raise SystemExit('INCOMPLETE: voluntary allowance exhausted; no exclusion asserted')
    tree = json.loads(args.tree.read_text())
    require_domain(tree)
    sys.path.insert(0, str(PARENT))
    from check import check_tree
    from phase_controls import check as phase_check
    result = json.loads(json.dumps(check_tree(tree)))
    phases = json.loads(json.dumps(phase_check()))
    if phases != expected['phase_controls']:
        raise ValueError('Complete phase transport record differs')
    require_applications(json.loads((HERE / 'application-next.json').read_text()))
    matched = result == expected['tree']
    if args.require_manifest and not matched:
        raise ValueError('Exact proof passed; author manifest differs')
    print(json.dumps({
        'agent': 'six-covering-2', 'role': 'researcher', 'period': N,
        'minimum_exactly': 8, 'parent_prefix': P,
        'proved': 'Original16 present and even, phase not0mod8; F existence iff F+16:2 or F+16:4 existence',
        'directly_checked_root': ROOT, 'nodes': result['nodes'],
        'strict_leaves': result['nodes'] - result['cuts']['expanded'],
        'author_manifest_match': matched, 'remaining_canonical16_phases': [2, 4],
        'credited_five_class_frontier_count': 13, 'global_numerical_improvement': False,
        'written_bridge': 'unformalized; see proof.md'}, sort_keys=True))


if __name__ == '__main__':
    main()
