"""Exact coefficient/budget audit; does not replay the external GFCN theorem."""
from argparse import ArgumentParser
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from math import isqrt, lcm
from pathlib import Path
import ast
import json
import re
import zipfile

INPUTS = {
    'rational_dual.txt': 'c30e2b3d3e7b50c01fe3bcdc17df80cf7053f0e73a756ec9965088c8dd50c106',
    'congruences.txt': 'f6374e5f79cd4565c36c613656d3b75410c9258a010bf859a1c7cff526f87110',
}
Z = Fraction(4000716307, 1000000018)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_inputs(archive):
    # Read only two text members. No unpickling, extraction, or external code.
    with zipfile.ZipFile(archive) as z:
        data = {name: z.read('snail_reproduction/' + name) for name in INPUTS}
    for name, value in data.items():
        require(sha256(value).hexdigest() == INPUTS[name], 'input hash: ' + name)
    return data


def parse(data):
    y = []
    for line in data['rational_dual.txt'].decode().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        entries = line.split()
        require(len(entries) == 2, 'dual row format')
        a, b = map(int, entries)
        require(b > 0, 'dual denominator')
        y.append(Fraction(a, b))
    congruences = []
    pattern = re.compile(r'^\S+\s+(\[.*?\])\s*=\s*(\[.*?\])$')
    for line in data['congruences.txt'].decode().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        match = pattern.fullmatch(line.strip())
        require(match is not None, 'congruence row format')
        pair = []
        for part in (match[1], match[2]):
            values = ast.literal_eval(part)
            require(isinstance(values, list) and len(values) > 0, 'empty shape')
            require(all(type(v) is int and 0 <= v < 29 for v in values), 'vertex index')
            require(len(set(values)) == len(values), 'duplicate shape vertex')
            pair.append(tuple(sorted(values)))
        require(len(pair[0]) == len(pair[1]), 'shape size mismatch')
        congruences.append(tuple(pair))
    require(len(y) == len(congruences), 'coefficient/congruence count mismatch')
    return y, congruences


def fraction_coefficients(y, congruences):
    """Aggregate signed terms at identical subsets, using rational numbers."""
    coefficients = defaultdict(Fraction)
    adjacency = defaultdict(set)
    raw_norm = Fraction(0)
    for a, (s, t) in zip(y, congruences):
        if len(s) == 1:
            continue  # Regular colourings give every singleton aggregate 1.
        raw_norm += abs(a)
        coefficients[s] += a
        coefficients[t] -= a
        adjacency[s].add(t)
        adjacency[t].add(s)
    unseen = set(adjacency)
    classes = []
    while unseen:
        seed = min(unseen)
        unseen.remove(seed)
        todo, members = [seed], []
        while todo:
            s = todo.pop()
            members.append(s)
            for t in adjacency[s]:
                if t in unseen:
                    unseen.remove(t)
                    todo.append(t)
        require(sum((coefficients[s] for s in members), Fraction(0)) == 0,
                'class not balanced')
        classes.append(members)
    norm = sum((abs(a) for a in coefficients.values()), Fraction(0)) / 2
    return dict(coefficients), classes, raw_norm, norm


def integer_audit(y, congruences):
    """Common-denominator accumulation by bit masks, without graph traversal."""
    denominator = lcm(*(a.denominator for a in y))
    values = {}
    for a, (left, right) in zip(y, congruences):
        if len(left) == 1:
            continue
        amount = a.numerator * (denominator // a.denominator)
        for vertices, sign in ((left, 1), (right, -1)):
            mask = sum(1 << v for v in vertices)
            values[mask] = values.get(mask, 0) + sign * amount
    require(sum(values.values()) == 0, 'integer total not balanced')
    positive = sum(max(a, 0) for a in values.values())
    return values, denominator, Fraction(positive, denominator)


def unit_edge_bound(n):
    require(type(n) is int and n >= 1, 'invalid physical order')
    # 2*m*m - n*m <= n*n*(n-1), from at most two common neighbours.
    return (n + isqrt(n * n * (8 * n - 7))) // 4


def run(data):
    y, congruences = parse(data)
    coefficients, classes, raw_norm, norm = fraction_coefficients(y, congruences)
    integers, denominator, second_norm = integer_audit(y, congruences)
    require(norm == second_norm, 'norm audit mismatch')
    for shape, coefficient in coefficients.items():
        mask = sum(1 << v for v in shape)
        require(coefficient == Fraction(integers[mask], denominator),
                'entrywise coefficient mismatch')
    gap = Z - 4
    require(gap > 0 and norm > 0, 'nonpositive certificate data')
    r_min = (norm / gap).__floor__() + 1  # Strict inequality is required.
    edge_max = unit_edge_bound(508)
    r_max = 4 * edge_max
    require(norm / r_max > gap, 'claimed cap rejection does not follow')
    n = 3
    while 4 * unit_edge_bound(n) < r_min:
        n += 1
    rows = [[list(s), str(coefficients[s])] for s in sorted(coefficients)]
    stream = json.dumps(rows, separators=(',', ':')).encode()
    return {
        'claim': 'Fixed-dual uniform global-Folner error criterion fails at order <=508.',
        'not_a_physical_graph_exclusion': True,
        'external_dual_inequalities_replayed': False,
        'congruence_geometry_replayed': False,
        'dual_rows': len(y),
        'non_singleton_rows': sum(len(s) > 1 for s, t in congruences),
        'listed_non_singleton_classes': len(classes),
        'distinct_non_singleton_shapes': len(coefficients),
        'coefficient_stream_sha256': sha256(stream).hexdigest(),
        'dual_value': str(Z), 'gap_over_four': str(gap),
        'raw_non_singleton_l1': str(raw_norm),
        'regrouped_range_error_coefficient': str(norm),
        'required_distinct_transformations_at_least': r_min,
        'physical_order_cap': 508, 'unit_edges_upper_bound_at_cap': edge_max,
        'distinct_transformations_upper_bound_at_cap': r_max,
        'smallest_error_budget_at_cap_from_this_estimate': str(norm / r_max),
        'necessary_order_from_this_criterion_only': n,
        'entrywise_integer_audit_matches': True,
        'record_candidate': False,
    }


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--supplement', type=Path, required=True)
    parser.add_argument('--check-expected', action='store_true')
    args = parser.parse_args()
    result = run(load_inputs(args.supplement))
    if args.check_expected:
        expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
        require(result == expected, 'expected result mismatch')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
