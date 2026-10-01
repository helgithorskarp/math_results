"""Replay the three new roots; import the published exceptional reduction.

No theorem is printed until all three complete trees pass independent literal
checking. Earlier intrinsic exclusions are credited rather than replayed.
"""
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
R = ((8, 0), (9, 0), (10, 0), (14, 1), (12, 10), (16, 4))
PHASES = (2, 4, 5)


def require_domain(tree, phase):
    if phase not in PHASES:
        raise ValueError('Wrong twenty phase')
    if (tree.get('L'), tree.get('minimum'), tree.get('complete')) != (N, 8, True):
        raise ValueError('Wrong period, minimum or incomplete tree')
    if tuple(map(tuple, tree['root_anchors'])) != R + ((20, phase),):
        raise ValueError('Wrong conditional root')


def application_data(prefixes):
    moduli = [n for n in range(8, N+1) if N % n == 0 and n not in dict(prefixes[0])]
    cases = []
    for root in prefixes:
        if [n for n, _ in root] != [8, 9, 10, 14, 12]:
            raise ValueError('Wrong five-class application domain')
        bitset = sum(1 << x for x in range(N) if all(x % n != a for n, a in root))
        cases.append({'root': root, 'residual': bitset.bit_count(),
                      'residual_bitset_hex': hex(bitset)[2:], 'proof_status': 'OPEN'})
    return {'period': N, 'minimum_exactly': 8, 'all_unused_moduli': moduli,
            'four_top_resources': [288, 1440, 2016, 10080],
            'top_phases': 'ALL FREE', 'roots': cases}


def check_applications(data, prefixes):
    if data != application_data(prefixes):
        raise ValueError('Wrong application root, support or full resource family')
    return len(data['roots'])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--generate', action='store_true')
    ap.add_argument('--generated', type=Path, default=HERE / 'generated')
    ap.add_argument('--require-manifest', action='store_true')
    ap.add_argument('--batches', type=int, default=12,
                    help='Voluntary allowance per root; each batch remains180s/700new nodes')
    args = ap.parse_args()
    if args.batches < 1:
        raise ValueError('Positive voluntary batch allowance required')
    expected = json.loads((HERE / 'manifest.json').read_text())
    for filename, digest in expected['dependency_source_sha256'].items():
        if sha256((PARENT / filename).read_bytes()).hexdigest() != digest:
            raise ValueError('Dependency source changed: ' + filename)
    sys.path.insert(0, str(PARENT))
    from check import check_tree
    from frontier_ten_twelve import controls
    sys.path.insert(0, str(PARENT / 'exceptional-ten-twenty-presence'))
    from phase_controls import check as twenty_controls
    args.generated.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
                'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[key] = '1'
    results = {}
    for phase in PHASES:
        root = R + ((20, phase),)
        path = args.generated / f'tree-twenty-{phase}.json'
        if args.generate:
            for _ in range(args.batches):
                command = [sys.executable, '-B', str(PARENT / 'generate.py'),
                           '--prefix', ','.join(f'{n}:{a}' for n, a in root),
                           '--seconds', '180', '--nodes', '700', '--out', str(path)]
                result = subprocess.run(command, env=env)
                if result.returncode not in (0, 2):
                    raise SystemExit(result.returncode)
                if path.exists() and json.loads(path.read_text()).get('complete'):
                    break
            else:
                raise SystemExit('INCOMPLETE: voluntary allowance exhausted; no theorem asserted')
        tree = json.loads(path.read_text())
        require_domain(tree, phase)
        results[str(phase)] = json.loads(json.dumps(check_tree(tree)))
    frontier = json.loads(json.dumps(controls()))
    transports = json.loads(json.dumps(twenty_controls()))
    if frontier != expected['affine_frontier'] or transports != expected['credited_twenty_controls']:
        raise ValueError('Complete affine frontier or credited twenty transports differ')
    apps = json.loads((HERE / 'application-next.json').read_text())
    application_count = check_applications(apps, frontier['remaining_prefixes'])
    matched = results == expected['trees']
    if args.require_manifest and not matched:
        raise ValueError('Exact proof checks passed; author manifest differs')
    print(json.dumps({
        'agent': 'six-covering-2', 'role': 'researcher', 'period': N,
        'minimum_exactly': 8,
        'proved': 'A PRESENT ten- or twelve-class has parity opposite to the eight-class',
        'credited_intrinsic_dependencies': [8728, 8837, 8923, 8963],
        'directly_replayed_twenty_roots': list(PHASES),
        'author_manifest_match': matched,
        'nodes': sum(r['nodes'] for r in results.values()),
        'expanded': sum(r['cuts']['expanded'] for r in results.values()),
        'strict_leaves': sum(r['nodes']-r['cuts']['expanded'] for r in results.values()),
        'vectors': sum(r['vectors'] for r in results.values()),
        'raw_phases': sum(r['raw_branch_phases'] for r in results.values()),
        'positive_transports': sum(r['positive_transports'] for r in results.values()),
        'pair_entries': sum(r['pair_phase_entries'] for r in results.values()),
        'new_removed_forms': 1, 'new_removed_tuples': 5040,
        'combined_removed_forms': 11, 'combined_removed_tuples': 40320,
        'remaining_forms': 13, 'remaining_application_roots': application_count,
        'global_numerical_improvement': False,
        'written_bridge': 'unformalized; see proof.md'}, sort_keys=True))


if __name__ == '__main__':
    main()
