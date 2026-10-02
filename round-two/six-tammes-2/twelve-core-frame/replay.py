"""Strict G20 literal replay in bounded ranges; no adaptive selector.

Each invocation checks only its explicit range. A saved cursor or hash is
not proof that another range was executed. Reproduction must execute all
ranges from zero with this fixed source and certificate.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import signal
import time

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('twelve_frame_model', BASE/'model.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
LABELS = [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12]
CODES = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSUVWXY'
LITERAL_BUDGET = 2500
NODE_BUDGET_PER_TREE = 20000
DEPTH_BUDGET = 22
HARD_SECONDS = 55
LOGICAL_SECONDS = 50


def require(ok, message):
    if not ok:
        raise ValueError(message)


def describe():
    raw = (BASE/'PLAN.json').read_bytes()
    require(len(raw) <= 50000, 'compact fixed certificate size')
    data = json.loads(raw)
    table = json.loads((BASE/'LITERALS.json').read_bytes())
    expected = ([['chart'], ['empty-necessary-intersection'], ['no-real-V'],
                 ['outside-target-g-half']] +
                [['W-pair', 7, j] for j in (1, 2, 4, 8, 10)] +
                [['pair', *p] for p in m.PAIRS])
    require(len(expected) == 42 and len(m.PAIRS) == 33, 'twelve-core literal count')
    require(len(m.CONTACTS) == 20 and all(set(p) <= set(LABELS) for p in m.CONTACTS),
            'twenty surviving contacts')
    require(all(13 not in w[1:] for w in expected), 'no removed-point literal')
    require(table['format'] == 1 and table['literals'] == expected and
            table['codes'] == CODES[:len(expected)], 'fixed typed literal table')
    lookup = dict(zip(table['codes'], table['literals']))
    require(data['format'] == 1 and data['lattice_bits'] == 80,
            'fixed format and outward precision')
    require(data['labels'] == LABELS and
            data['contacts'] == [list(p) for p in sorted(m.CONTACTS)], 'exact core binding')
    require(data['box'] == ['14/25', '593/1000', '-5/2', '5/2'],
            'entire fixed closed rectangle')
    targets = [('bad', -1, -1), ('bad', 1, -1), ('bad', 1, 1), ('g-half', -1, 1)]
    require([(t['mode'], t['epsilon'], t['eta']) for t in data['trees']] == targets,
            'all four targets in fixed order')
    leaves, trees = [], []
    for tree in data['trees']:
        mode, eps, eta = tree['mode'], tree['epsilon'], tree['eta']
        require(isinstance(tree['tree'], str), 'literal prefix string')
        tokens = iter(tree['tree'])
        nodes = count = maximum = 0
        area = Fraction(0)
        kinds = Counter()
        first = len(leaves)
        def walk(a, i, c, j):
            nonlocal nodes, count, maximum, area
            nodes += 1
            require(nodes <= NODE_BUDGET_PER_TREE, 'fixed tree node guard')
            maximum = max(maximum, a+c)
            require(a+c <= DEPTH_BUDGET, 'fixed depth guard')
            code = next(tokens, None)
            require(code is not None, 'truncated prefix tree')
            if code in ('T', 'Z'):
                require(a+c < DEPTH_BUDGET, 'permitted subdivision depth')
                if code == 'T':
                    walk(a+1, 2*i, c, j)
                    walk(a+1, 2*i+1, c, j)
                else:
                    walk(a, i, c+1, 2*j)
                    walk(a, i, c+1, 2*j+1)
                return
            require(code in lookup, 'known surviving-point predicate')
            witness = lookup[code]
            require(witness != ['outside-target-g-half'] or mode == 'g-half',
                    'target-specific g-half predicate')
            leaves.append((mode, eps, eta, a, i, c, j, witness))
            count += 1
            area += Fraction(1, 2**(a+c))
            kinds[witness[0]] += 1
        walk(0, 0, 0, 0)
        require(next(tokens, None) is None, 'no unused prefix tokens')
        require(area == 1 and nodes == 2*count-1, 'exact closed root partition')
        trees.append({'mode': mode, 'epsilon': eps, 'eta': eta, 'nodes': nodes,
                      'leaves': count, 'maximum_depth': maximum,
                      'leaf_range': [first, len(leaves)], 'normalized_area': str(area),
                      'witness_kinds': dict(sorted(kinds.items()))})
    pins = {name: hashlib.sha256((BASE/name).read_bytes()).hexdigest()
            for name in ('PLAN.json', 'LITERALS.json', 'model.py', 'replay.py')}
    summary = {'actual_agent': 'six-tammes-2', 'role': 'researcher',
               'status': 'EXACT_FULL_PREFIX_STRUCTURE_CHECKED', 'source_pins': pins,
               'total_literal_leaves': len(leaves),
               'total_prefix_nodes': sum(t['nodes'] for t in trees), 'trees': trees,
               'no_removed_point_in_model_or_literal_table': True,
               'entire_closed_rectangle_partitioned_for_each_target': True,
               'interval_predicates_checked_by_describe': False}
    return leaves, summary


def check_range(start, output):
    require(not output.exists(), 'output must be new')
    started = time.monotonic()
    leaves, structure = describe()
    require(0 <= start < len(leaves), 'valid explicit range start')
    stop = min(start+LITERAL_BUDGET, len(leaves))
    done, guard = start, None
    counts = Counter()
    for index in range(start, stop):
        if time.monotonic()-started >= LOGICAL_SECONDS:
            guard = '50-second logical range guard'
            break
        mode, eps, eta, a, i, c, j, witness = leaves[index]
        t, z = m.box(a, i, c, j)
        require(m.verify_witness(t, z, eps, eta, mode, witness) is True,
                f'strict interval predicate failed at leaf{index}: '
                f'{(mode, eps, eta, a, i, c, j, witness)}')
        done = index+1
        counts[witness[0]] += 1
    if done-start == LITERAL_BUDGET:
        guard = '2500-literal range budget'
    result = {'actual_agent': 'six-tammes-2', 'role': 'researcher',
              'status': 'CHECKED_COMPLETE_REQUESTED_RANGE' if done == stop
                        else 'CHECKED_PARTIAL_REQUESTED_RANGE',
              'source_pins': structure['source_pins'],
              'checked_range': [start, done], 'requested_range': [start, stop],
              'checked_literals_this_invocation': done-start,
              'total_certificate_literals': len(leaves),
              'guard': guard, 'seconds': round(time.monotonic()-started, 6),
              'witness_kinds': dict(sorted(counts.items())),
              'all_requested_literal_predicates_executed': done == stop,
              'other_ranges_verified_by_this_invocation': False,
              'whole_certificate_replayed_by_this_invocation': False,
              'independent_person_review': 'pending', 'new_global_bound': False}
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--describe', action='store_true')
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('55-second replay guard')))
    signal.alarm(HARD_SECONDS)
    if args.describe:
        print(json.dumps(describe()[1], indent=2))
    else:
        require(args.output is not None, 'explicit private output path required')
        check_range(args.start, args.output)
