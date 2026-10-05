"""Designated mathematical/scope and source-before-import rejection cases.

Semantic copies deliberately refresh their source pins, so a successful
semantic rejection must be its stated mathematical gate, not a checksum.
Source copies retain the original pins and prove no producer was imported.
Neither kind supplies independent review or authenticates a tampered seal.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time


CASES = [
    ('candidate-scale', 'coefficient denominator guard: CANDIDATE.json'),
    ('star-kernel', 'three whole original star-kernel vectors'),
    ('quarter-original-vector', 'ALL 58 fresh quarter-weight original vector coordinates'),
    ('comparison-cap', 'fresh aggregate exactly decodes published quarter-weight DATA'),
    ('individual-NS-entry', 'ALL 81 exact dual kernel rows'),
    ('dual-nullrow', 'ALL 81 exact dual kernel rows'),
    ('dual-physical-action', 'EVERY new exact physical dual action coordinate'),
    ('dual-factor-position', 'ALL new dual factor identity positions'),
    ('row-census', 'ALL58 literal original disjoint bad-neighbor counts'),
    ('row-kernel', 'ALL58 original aggregate coordinates have zero sum'),
    ('basic-primal', 'NEW full original zero-sum primal energy equality'),
    ('bcW-column-support', 'ALL nine actual bcW original column capacities'),
    ('coupling-slope', 'fixed bcW contribution removes162 apparent movable positive-row slots'),
    ('coupled-primal', 'new exact whole original primal/kernel/coupling/energy equality'),
    ('root-isolation', 'NEW exact strict coupled-threshold isolation in original M units'),
    ('extended-floor-claim', 'CLAIM licence/scope mismatch'),
    ('signed-weight-claim', 'CLAIM licence/scope mismatch'),
    ('original-distance-claim', 'CLAIM licence/scope mismatch'),
    ('expected-root-coefficient', 'whole EXPECTED semantic record mismatch'),
    ('expected-coordinate-omission', 'whole EXPECTED semantic record mismatch'),
]
SOURCES = [
    ('producer-before-import', 'source bytes mismatch: aggregate.py'),
    ('proof-before-import', 'source bytes mismatch: PROOF.md'),
    ('omitted-producer-pin', 'source file coverage mismatch'),
    ('unexpected-source', 'unexpected source file'),
]


def edit(root, name, old, new):
    p = root/name; text = p.read_text()
    if text.count(old) != 1:
        raise ValueError('mutation anchor: '+name+' '+old)
    p.write_text(text.replace(old, new))


def json_edit(root, name, change):
    p = root/name; d = json.loads(p.read_bytes()); change(d)
    p.write_text(json.dumps(d, indent=2)+'\n')


def mutate(root, case):
    if case == 'candidate-scale':
        json_edit(root, 'CANDIDATE.json', lambda d: d.update(denominator=0))
    elif case == 'star-kernel':
        edit(root, 'aggregate.py', '    require(all(sum(v) == 0 for v in columns),',
             '    columns[0][0] += 1\n    require(all(sum(v) == 0 for v in columns),')
    elif case == 'quarter-original-vector':
        p = root/'QUARTER-REFERENCE.json'; old = hashlib.sha256(p.read_bytes()).hexdigest()
        json_edit(root, p.name, lambda d: d['v_S_complete58_numerators'].__setitem__(0,
                  d['v_S_complete58_numerators'][0]+1))
        edit(root, 'aggregate.py', old, hashlib.sha256(p.read_bytes()).hexdigest())
    elif case == 'comparison-cap':
        edit(root, 'aggregate.py', '    qweights = [F(1, 4), F(1, 4), F(1)]',
             '    old_cap[0][0] += F(1)\n    qweights = [F(1, 4), F(1, 4), F(1)]')
    elif case == 'individual-NS-entry':
        edit(root, 'individual_dual.py', "    old_BB = literal['old_bad_by_bad_numerators']",
             "    original_NS[0][0] += 1\n    old_BB = literal['old_bad_by_bad_numerators']")
    elif case == 'dual-nullrow':
        edit(root, 'individual_dual.py', '    require(all(sum(row) == 0 for row in R),',
             '    R[0][0] += F(1)\n    require(all(sum(row) == 0 for row in R),')
    elif case == 'dual-physical-action':
        edit(root, 'individual_dual.py', '        gram = [[sum(v[i]*images[j][i] for i in range(n))',
             '        images[0][0] += F(1)\n        gram = [[sum(v[i]*images[j][i] for i in range(n))')
    elif case == 'dual-factor-position':
        edit(root, 'individual_dual.py', '    n = len(A)', '    n = len(A)\n    A[0][-1] += F(1)')
    elif case == 'row-census':
        edit(root, 'radius.py', '    require({k: degrees.count(k) for k in set(degrees)}',
             '    degrees[0] -= 1\n    require({k: degrees.count(k) for k in set(degrees)}')
    elif case == 'row-kernel':
        edit(root, 'radius.py', '    require(sum(values) == 0,',
             '    values[0] += 1\n    require(sum(values) == 0,')
    elif case == 'basic-primal':
        edit(root, 'radius.py', '        require(sum(q) == 0 and sum(x*x for x in q)',
             '        q[0] += F(1)\n        require(sum(q) == 0 and sum(x*x for x in q)')
    elif case == 'bcW-column-support':
        edit(root, 'coupled_radius.py', '    forbidden = sum(bool(masks[i] & t)',
             '    triples[0] = 1\n    forbidden = sum(bool(masks[i] & t)')
    elif case == 'coupling-slope':
        edit(root, 'coupled_radius.py', '    require(K == 285120 and V ==',
             '    K += 220\n    require(K == 285120 and V ==')
    elif case == 'coupled-primal':
        edit(root, 'coupled_radius.py', '        require(sum(q) == 0 and sum(q[i] for i in P)',
             '        q[0] += F(1)\n        require(sum(q) == 0 and sum(q[i] for i in P)')
    elif case == 'root-isolation':
        edit(root, 'coupled_radius.py', '    cage = [F(1, 363), F(1, 362)]',
             '    cage = [F(1, 365), F(1, 364)]')
    elif case == 'extended-floor-claim':
        json_edit(root, 'CLAIM.json', lambda d: d.update(full_real_tau_interval=['0', '1/128']))
    elif case == 'signed-weight-claim':
        json_edit(root, 'CLAIM.json', lambda d: d.update(individual_nonnegative_weight_domain='ALL signed real weights'))
    elif case == 'original-distance-claim':
        json_edit(root, 'CLAIM.json', lambda d: d.update(original_NS_matrix_at_threshold_or_best_original_distance_claimed=True))
    elif case == 'expected-root-coefficient':
        json_edit(root, 'EXPECTED.json', lambda d: d['math_records']['original58_coupled_radius']
                  ['primitive_threshold_polynomial_low_to_high'].__setitem__(0, 0))
    elif case == 'expected-coordinate-omission':
        json_edit(root, 'EXPECTED.json', lambda d: d['math_records']['original58_box_radius']
                  ['complete_original58_vector_numerators'].pop())
    else:
        raise ValueError('unknown semantic case')
    # Intentionally repin the laboratory copy; a checksum rejection is not
    # acceptable evidence for the designated mathematical/scope failure.
    p = root/'SOURCE.json'; seal = json.loads(p.read_bytes())
    for name, item in seal['files'].items():
        raw = (root/name).read_bytes()
        item.update(bytes=len(raw), SHA256=hashlib.sha256(raw).hexdigest())
    p.write_text(json.dumps(seal, indent=2)+'\n')


def source_fault(root, case):
    # All source cases install a harmless marker in the math producer. Its
    # absence after rejection proves that source checking preceded import.
    p = root/'aggregate.py'
    text = p.read_text()
    marker = "from pathlib import Path\nPath(__file__).with_name('IMPORT-RAN').write_text('bad import')\n"
    # Keep the initial docstring; insert the marker before the first import.
    anchor = 'from fractions import Fraction as F'
    if text.count(anchor) != 1:
        raise ValueError('producer marker anchor')
    p.write_text(text.replace(anchor, marker+anchor))
    if case == 'producer-before-import':
        return
    # Other faults must not be hidden by the marker's source mismatch.
    seal_path = root/'SOURCE.json'; seal = json.loads(seal_path.read_bytes())
    raw = p.read_bytes(); seal['files'][p.name].update(bytes=len(raw), SHA256=hashlib.sha256(raw).hexdigest())
    if case == 'proof-before-import':
        p = root/'PROOF.md'; p.write_text(p.read_text()+'\nchanged mathematical scope\n')
    elif case == 'omitted-producer-pin':
        del seal['files']['aggregate.py']
    elif case == 'unexpected-source':
        (root/'UNEXPECTED.py').write_text('raise RuntimeError("unexpected import")\n')
    else:
        raise ValueError('unknown source case')
    seal_path.write_text(json.dumps(seal, indent=2)+'\n')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--phase', choices=['semantic', 'source'], required=True)
    ap.add_argument('--start', type=int, default=0); ap.add_argument('--stop', type=int)
    args = ap.parse_args(); root = Path(__file__).resolve().parent
    if args.out.exists() or args.out.resolve().is_relative_to(root):
        raise ValueError('fresh adverse directory outside source required')
    args.out.mkdir(parents=True)
    cases = CASES if args.phase == 'semantic' else SOURCES
    selected = cases[args.start:args.stop]
    if not selected:
        raise ValueError('empty designated batch')
    seal = json.loads((root/'SOURCE.json').read_bytes())
    env = dict(os.environ)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
        env[key] = '1'
    results = []
    for case, gate in selected:
        for mode, options in [('normal', []), ('optimized', ['-O'])]:
            copy = args.out/(case+'-'+mode); copy.mkdir()
            for name in list(seal['files'])+['SOURCE.json']:
                shutil.copyfile(root/name, copy/name)
            if args.phase == 'semantic':
                mutate(copy, case)
            else:
                source_fault(copy, case)
            start = time.monotonic()
            p = subprocess.run([sys.executable, '-I', *options, str(copy/'reader.py')],
                               env=env, capture_output=True, timeout=45)
            elapsed = time.monotonic()-start
            try:
                failure = json.loads(p.stderr)
            except (ValueError, UnicodeDecodeError):
                raise ValueError('crash/unknown gate for '+case+': '+p.stderr.decode())
            if p.returncode != 2 or p.stdout or failure != {'accepted': False, 'gate': gate}:
                raise ValueError('wrong designated rejection '+case+': '+str(failure))
            if args.phase == 'source' and (copy/'IMPORT-RAN').exists():
                raise ValueError('source gate imported mathematics')
            results.append({'case': case, 'mode': mode, 'gate': gate,
                            'seconds': elapsed, 'returncode': p.returncode,
                            'source_checked_before_math_import': args.phase == 'source'})
            (args.out/'progress.json').write_text(json.dumps(results, indent=2)+'\n')
    receipt = {'actual_agent': 'six-downset-3', 'role': 'researcher',
               'UTC': datetime.now(timezone.utc).isoformat(), 'phase': args.phase,
               'designated_rejections': results, 'count': len(results),
               'peak_child_RSS_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'fixed_child_seconds': 45, 'serial_native_threads': 1,
               'unknown_timeout_memorykill_or_wrong_gate_counted_as_rejection': False,
               'source_snapshot_SHA256': hashlib.sha256((root/'SOURCE.json').read_bytes()).hexdigest(),
               'independent_review_or_formal_proof': False}
    (args.out/'RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
