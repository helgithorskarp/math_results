"""Check the new twenty-phase root; import credited exceptional reductions."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from phase_controls import R, check as phase_controls

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
ROOT = R + ((20, 1),)


def require_domain(tree):
    if (tree.get('L'), tree.get('minimum')) != (10080, 8):
        raise ValueError('Wrong period or minimum')
    if tree.get('complete') is not True:
        raise ValueError('Incomplete tree is not an exclusion')
    if tuple(map(tuple, tree['root_anchors'])) != ROOT:
        raise ValueError('Wrong conditional root')


def check_applications(data):
    if data.get('period') != 10080 or data.get('minimum_exactly') != 8:
        raise ValueError('Wrong comparison domain')
    want = []
    for a in (2, 4, 5):
        root = R + ((20, a),)
        available = [n for n in range(8, 10081)
                     if 10080 % n == 0 and n not in dict(root)]
        bitset = sum(1 << x for x in range(10080)
                     if all(x % n != b for n, b in root))
        want.append({'root': [list(p) for p in root],
                     'residual': bitset.bit_count(),
                     'residual_bitset_hex': hex(bitset)[2:],
                     'available_moduli': available,
                     'four_top_resources': [288, 1440, 2016, 10080],
                     'top_phases': 'ALL FREE', 'proof_status': 'OPEN'})
    if data.get('roots') != want:
        raise ValueError('Wrong literal root, bitset or resource family')
    return [{'twenty_phase': r['root'][-1][1],
             'residual': r['residual'],
             'unused_resources': len(r['available_moduli']),
             'status': r['proof_status']} for r in want]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--generate', action='store_true')
    ap.add_argument('--generated', type=Path, default=HERE / 'generated')
    ap.add_argument('--batches', type=int, default=12)
    ap.add_argument('--require-manifest', action='store_true')
    args = ap.parse_args()
    if args.batches < 1:
        raise ValueError('Positive voluntary generation allowance required')
    expected = json.loads((HERE / 'manifest.json').read_text())
    for name, digest in expected['dependency_source_sha256'].items():
        if sha256((PARENT / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Dependency bytes changed: ' + name)
    sys.path.insert(0, str(PARENT))
    from check import check_tree
    args.generated.mkdir(parents=True, exist_ok=True)
    treefile = args.generated / 'tree-twenty-one.json'
    env = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
                 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[name] = '1'
    if args.generate:
        for batch in range(args.batches):
            outcome = subprocess.run([
                sys.executable, '-B', str(PARENT / 'generate.py'),
                '--prefix', ','.join(f'{n}:{a}' for n, a in ROOT),
                '--seconds', '180', '--nodes', '700', '--out', str(treefile)], env=env)
            if outcome.returncode not in (0, 2):
                raise SystemExit(outcome.returncode)
            if treefile.exists() and json.loads(treefile.read_text()).get('complete'):
                break
        else:
            raise SystemExit('INCOMPLETE: voluntary allowance exhausted; no exclusion asserted')
    tree = json.loads(treefile.read_text())
    require_domain(tree)
    result = json.loads(json.dumps(check_tree(tree)))
    controls = json.loads(json.dumps(phase_controls()))
    if controls != expected['phase_controls']:
        raise ValueError('Literal phase controls differ')
    comparison = check_applications(json.loads((HERE / 'application-next.json').read_text()))
    matched = result == expected['new_tree']
    if args.require_manifest and not matched:
        raise ValueError('Exact exclusion passes, but author manifest differs')
    print(json.dumps({
        'agent': 'six-covering-2', 'role': 'researcher',
        'period': 10080, 'minimum_exactly': 8,
        'directly_replayed_root': ROOT, 'author_manifest_match': matched,
        'credited_intrinsic_dependencies': [8837, 8923],
        'original_resources_forced': [10, 20],
        'phase_relation': 'a20-a8 odd iff a20-a10=0mod5',
        'written_presence_bridge': 'unformalized; see proof.md',
        'nodes': result['nodes'], 'strict_leaves': result['nodes']-result['cuts']['expanded'],
        'raw_phases': result['raw_branch_phases'],
        'positive_transports': result['positive_transports'],
        'pair_entries': result['pair_phase_entries'],
        'remaining_exceptional_roots': comparison,
        'five_class_frontier': 14, 'global_numerical_improvement': False}, sort_keys=True))


if __name__ == '__main__':
    main()
