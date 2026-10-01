#!/usr/bin/env python3
"""Complete independent review evidence and stable expected-record comparison."""
from pathlib import Path
from copy import deepcopy
from hashlib import sha256
import argparse
import json
import resource
import time

import audit
import bridge
from exact import insist, encoded, mask, pairs, plane


def rejected(check):
    try:
        check()
    except ValueError:
        return
    raise ValueError('invalid rejection certificate accepted')


def controls(target, work):
    carrier = json.loads((work / 'carrier.json').read_text())
    source = json.loads((target / 'pair_two_certificate.json').read_text())
    record = carrier['records'][0]
    rows = tuple(tuple(e) for e in record['rows'])
    columns = tuple(tuple(q) for q in record['columns'])
    root = source['cases'][0]['tree']
    controls = []
    def test(name, node):
        rejected(lambda: audit.tree_check(rows, columns, node))
        controls.append(name)
    bad = deepcopy(root); bad[1].pop(); test('omitted_root_branch', bad)
    bad = deepcopy(root); bad[1].append(deepcopy(bad[1][0])); test('duplicated_root_branch', bad)
    bad = deepcopy(root); bad[0] = len(rows); test('out_of_range_pivot', bad)
    bad = deepcopy(root); bad[0] = True; test('boolean_pivot', bad)
    bad = deepcopy(root); bad[1][0][0] = len(columns); test('out_of_range_column', bad)
    try:
        audit.tree_check(rows, columns, root, limit=0)
    except RuntimeError as e:
        insist('INCOMPLETE' in str(e), 'zero guard failure not incomplete')
    else:
        raise ValueError('zero guard accepted')
    # A genuine eleven-block pair cover; no target search kernel is imported.
    known = tuple(plane()[9:])
    count = [e for q in known for e in pairs(q)]
    insist(len(count) == len(set(count)) == 66 and len(known) == 11, 'positive cover fixture')
    positive_rows = tuple(sorted(count))
    positive_columns = tuple(tuple(audit.bits(q)) for q in known)
    rejected(lambda: audit.tree_check(positive_rows, positive_columns, [0, []]))
    # Force a cover to reach empty remaining rows; such a leaf must be rejected.
    four_rows = tuple(sorted(pairs(15)))
    rejected(lambda: audit.tree_check(four_rows, ((0, 1, 2, 3),), [0, [[0, [0, []]]]]))
    return {'invalid_tree_controls': controls, 'zero_guard_incomplete': True,
            'positive_eleven_block_cover_rows': 66, 'false_positive_cover_rejection_trees_rejected': 2}


def stable(value):
    if isinstance(value, dict):
        return {k: stable(v) for k, v in value.items() if k not in ('seconds', 'peak_rss_kib')}
    if isinstance(value, list):
        return [stable(v) for v in value]
    return value


def main(args):
    started = time.monotonic()
    audit.main(args)
    result = {'completion': stable(json.loads((args.work / 'summary.json').read_text())),
              'tail_coverage': audit.tail_coverage(),
              'controls': controls(args.target, args.work), 'one_word_interfaces': bridge.data(),
              'known_hypothesis_counterexample': bridge.baseline(args.target / 'baseline69.txt'),
              'claim': 'If r_u=r_v=20 and d_uv=2 then |F|<=60, using the audited upper57 input.',
              'status': 'COMPLETE independent review and upper60 bridge evidence'}
    raw = encoded(result)
    if args.record:
        args.expected.write_bytes(raw)
    else:
        insist(raw == args.expected.read_bytes(), 'stable complete expected record differs')
    metrics = {'status': result['status'], 'expected_sha256': sha256(raw).hexdigest(),
               'seconds': time.monotonic() - started, 'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               'residual_cases': 198, 'tree_nodes': 351, 'strengthened_upper_bound': 60}
    (args.work / 'metrics.json').write_bytes(encoded(metrics))
    print(json.dumps(metrics, sort_keys=True))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--target', type=Path, default=Path(__file__).resolve().parents[1] / 'constant_weight_18_6_5_equality_structure')
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    p.add_argument('--record', action='store_true', help='Record a new baseline explicitly; not expected comparison')
    main(p.parse_args())
