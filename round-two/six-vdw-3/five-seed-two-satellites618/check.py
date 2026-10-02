#!/usr/bin/env python3
"""Audit the four derived signed heads against a pinned actual-cyclic common-base checker.

The helper check.py from source b18c33b5 supplies parse/cyclic_base only; its
old singleton literal/witness routines are never used for these new words.
The general signed-word frontend is credited to source00dd57d6; production tables below are new.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
import time
from pathlib import Path

HELPER_SHA256 = 'f8da83bf139e57887b28ce67d4f3cd2fd5a53d848bbb1beae0fd16cdb33c7bdf'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def helper(path):
    need(hashlib.sha256(path.read_bytes()).hexdigest() == HELPER_SHA256,
         'Imported actual-cyclic checker source changed')
    spec = importlib.util.spec_from_file_location('credited_cyclic_checker', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parameters(q, case):
    if q == 103:
        need(case in (1,2,3,4), 'Invalid production head')
        holes = (5,53,101)
        core = ((0,1,2,3,4,29,52,54,55,80,102) if case in (1,2) else
                (0,1,2,3,4,28,29,52,54,55,80,81,102))
        opposite = ((52,80,102),(29,52,102),(28,52,81,102),(29,52,80,102))[case-1]
    else:
        need(q in (7,11,13) and case in (1,2,3), 'Unsupported small control')
        holes = (0,1,case+1)
        core = tuple(x for x in range(q) if x not in holes)[:4]
        opposite = core[1:]
    regular = tuple(x for x in range(q) if x not in holes)
    pairs = tuple(itertools.combinations(regular, 2))
    index = {pair: j+1 for j,pair in enumerate(pairs)}
    return holes, core, opposite, regular, pairs, index


def audit(path, q, case, common):
    started = time.monotonic()
    holes, core, opposite, regular, pairs, index = parameters(q,case)
    root = regular[0]
    need(root in core and root not in opposite, 'Invalid gauge')
    base, details = common.cyclic_base(q,1 if q==103 else case)
    units = {(index[(root,x)] if x in opposite else -index[(root,x)],)
             for x in core if x != root}
    expected = set(base) | units
    actual = common.parse(path,len(pairs))
    need(actual == expected, 'Actual cyclic / new signed-word model mismatch')
    need(all(len(row) in (1,3,4) for row in actual), 'Extra assumption or variable')
    return {'q': q, 'case': case, 'holes': list(holes), 'root': root,
            'fixed_core_bits': [[x,int(x in opposite)] for x in core],
            'regular_columns': list(regular), 'variables': len(pairs),
            'fixed_core_units': len(units), 'positive_core_units': len(opposite),
            'clauses': len(actual), 'other_regular_bits_free': len(regular)-len(core),
            'extra_growth_cuts': 0, 'no_five_assumption': False,
            'no_six_assumption': False, 'counter_variables': 0, 'weight_cap': None,
            'reflection_invariance_imposed': False,
            'cnf_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'credited_actual_cyclic_checker_sha256': HELPER_SHA256,
            **details, 'seconds': time.monotonic()-started}


def literal(q, case, bits):
    holes, core, opposite, regular, _, _ = parameters(q,case)
    need(len(bits) == len(regular) and all(type(x) is int and x in (0,1) for x in bits),
         'Bad orientation domain')
    values = dict(zip(regular,bits))
    if any(values[x] != int(x in opposite) for x in core):
        return False, {'failure': 'Wrong derived-head or small fixed word'}
    length = 6*q
    colors = [None if t%q in holes else values[t%q] ^ int(t%6 >= 3)
              for t in range(length)]
    checked = skipped = 0
    for step in range(1,length):
        for start in range(length):
            row = tuple(colors[(start+j*step)%length] for j in range(7))
            if None in row:
                skipped += 1
                continue
            checked += 1
            if len(set(row)) == 1:
                return False, {'failure': 'Cyclic seven AP', 'start': start, 'step': step}
    return True, {'outside_seven_pairs_checked': checked, 'seven_pairs_skipped': skipped}


def decode(assignment, q, case):
    _, _, _, regular, pairs, index = parameters(q,case)
    need(type(assignment) is list and len(assignment) == len(pairs) and
         all(type(x) is int and x != 0 for x in assignment), 'Malformed pair assignment')
    values = {abs(x): int(x > 0) for x in assignment}
    need(set(values) == set(range(1,len(pairs)+1)), 'Missing or duplicated pair variable')
    word = {regular[0]: 0}
    for x in regular[1:]:
        word[x] = values[index[(regular[0],x)]]
    need(all(values[index[(x,y)]] == word[x]^word[y] for x,y in pairs),
         'Pair assignment is not an orientation coboundary')
    return tuple(word[x] for x in regular)


def witness(path, q, case):
    assignment = json.loads(path.read_text())
    bits = decode(assignment,q,case)
    good, details = literal(q,case,bits)
    need(good, 'Literal full outside-cyclic witness rejected: '+str(details))
    holes, core, opposite, regular, _, _ = parameters(q,case)
    return {'q': q, 'case': case, 'holes': list(holes),
            'fixed_core_bits': [[x,int(x in opposite)] for x in core],
            'regular_point_order': list(regular), 'orientation': ''.join(map(str,bits)),
            'outside_cyclic_AP_free': True, 'full_coloring_AP_free': False,
            'W_bound_improved': False, **details}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path',type=Path)
    parser.add_argument('--q',type=int,default=103)
    parser.add_argument('--case',type=int,default=1)
    parser.add_argument('--helper',type=Path)
    parser.add_argument('--witness',action='store_true')
    args = parser.parse_args()
    if args.witness:
        print(json.dumps(witness(args.path,args.q,args.case)))
    else:
        need(args.helper is not None, 'Byte-pinned cyclic helper required')
        print(json.dumps(audit(args.path,args.q,args.case,helper(args.helper))))
