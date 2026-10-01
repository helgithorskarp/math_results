"""Validate the ordinary proof's small arithmetic and literal identities.

This is author validation, not a host enumeration premise or peer review.
Only Python's standard library is used; checks remain active under -O.
"""
import argparse
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = 11
INTERNAL = {
    (1, 2): (2, 1, 2, 1, 0), (1, 3): (0, 3, 0, 2, 1),
    (1, 4): (0, 1, 3, 0, 2), (1, 5): (1, 1, 0, 2, 2),
    (2, 3): (2, 0, 0, 1, 3), (2, 4): (0, 2, 1, 1, 2),
    (2, 5): (1, 0, 2, 3, 0), (3, 4): (2, 0, 1, 2, 1),
    (3, 5): (1, 2, 2, 0, 1), (4, 5): (3, 2, 1, 0, 0),
}
FOUR_GAPS = {
    (5, 2, 2, 2): (0, 3, 0, 2, 1),
    (4, 3, 2, 2): (0, 2, 1, 2, 1),
    (4, 2, 3, 2): (0, 2, 1, 1, 2),
    (4, 2, 2, 3): (0, 2, 1, 2, 1),
    (3, 3, 3, 2): (0, 1, 3, 0, 2),
}
FIVE_GAPS = {
    (1, 3, 3, 2, 2): (1, 2, 3, 2, 2),
    (1, 3, 2, 3, 2): (1, 2, 3, 1, 3),
    (1, 3, 2, 2, 3): (1, 2, 2, 3, 2),
    (1, 2, 3, 3, 2): (1, 2, 4, 0, 3),
    (1, 2, 3, 2, 3): (1, 2, 3, 1, 3),
    (1, 2, 2, 3, 3): (1, 2, 3, 2, 2),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def shift(points, k):
    return {(x + k) % P for x in points}


def symmetric(classes):
    return {x % P for i in classes for x in (i, -i)}


def vector(points):
    return tuple(len(points & shift(points, k)) for k in range(1, 6))


def canon_gaps(gaps):
    return min(gaps[i:] + gaps[:i] for i in range(len(gaps)))


def gaps_of(points):
    values = sorted(points)
    return tuple((values[(i+1) % len(values)] - x) % P
                 for i, x in enumerate(values))


def points_of(gaps):
    require(all(g > 0 for g in gaps) and sum(gaps) == P, 'bad gap word')
    return set(itertools.accumulate((0, *gaps[:-1])))


def validate_internal(table):
    require(set(table) == set(itertools.combinations(range(1, 6), 2)),
            'incomplete internal table')
    for classes, expected in table.items():
        points = symmetric(classes)
        actual = vector(points)
        require(actual == expected, 'internal table mismatch')
        literal = [0] * 5
        for x, y in itertools.combinations(points, 2):
            d = (y-x) % P
            literal[min(d, P-d)-1] += 1
        require(tuple(literal) == expected, 'unordered differences mismatch')


def validate_gaps(table, size, predicate):
    actual = {}
    count = 0
    for values in itertools.combinations(range(P), size):
        gaps = gaps_of(set(values))
        if not predicate(gaps):
            continue
        key = canon_gaps(gaps)
        corr = vector(set(values))
        require(key not in actual or actual[key] == corr, 'phase disagreement')
        actual[key] = corr
        count += 1
    claimed = {}
    for gaps, corr in table.items():
        require(vector(points_of(gaps)) == corr, 'gap vector mismatch')
        key = canon_gaps(gaps)
        require(key not in claimed, 'duplicate gap class')
        claimed[key] = corr
    require(actual == claimed, 'incomplete gap table')
    return count


def decode_graph6(line):
    require(len(line) == 40 and ord(line[0])-63 == 22, 'graph6 size mismatch')
    require(all(63 <= ord(ch) <= 126 for ch in line), 'graph6 character')
    bits = [(ord(ch)-63) >> k & 1 for ch in line[1:]
            for k in range(5, -1, -1)]
    require(not any(bits[231:]), 'graph6 padding')
    rows = [set() for _ in range(22)]
    pos = 0
    for j in range(1, 22):
        for i in range(j):
            if bits[pos]:
                rows[i].add(j)
                rows[j].add(i)
            pos += 1
    return rows


def literal_rows(da, db, cross):
    rows = [set() for _ in range(22)]
    for i, j in itertools.combinations(range(22), 2):
        if j < 11:
            red = (j-i) % P in da
        elif i >= 11:
            red = (j-i) % P in db
        else:
            red = (j-11-i) % P in cross
        if red:
            rows[i].add(j)
            rows[j].add(i)
    return rows


def verify_literal_identities(da, db, cross, rows=None):
    literal = literal_rows(da, db, cross)
    if rows is not None:
        require(literal == rows, 'primary fixture not the claimed block graph')
    rows = literal
    c = len(cross)
    degrees = (len(da)+c, len(db)+c)
    hist = [{}, {}]
    for i, j in itertools.combinations(range(22), 2):
        color = j in rows[i]
        common = len(rows[i] & rows[j])
        if j < 11:
            k = (j-i) % P
            formula = len(da & shift(da, k)) + len(cross & shift(cross, k))
            dsum = 2*degrees[0]
        elif i >= 11:
            k = (j-i) % P
            formula = len(db & shift(db, k)) + len(cross & shift(cross, k))
            dsum = 2*degrees[1]
        else:
            k = (j-11-i) % P
            formula = len(cross & shift(da, k)) + len(cross & shift(db, k))
            dsum = sum(degrees)
        require(common == formula, 'red correlation/literal mismatch')
        pages = common if color else len(set(range(22))-{i, j}-rows[i]-rows[j])
        if not color:
            require(pages == 20-dsum+formula, 'blue complement mismatch')
        bucket = hist[0 if color else 1]
        bucket[pages] = bucket.get(pages, 0)+1
    total_cross = sum(len(cross & shift(da, k))+len(cross & shift(db, k))
                      for k in cross)
    energy = sum(len(cross & shift(cross, h)) for h in da)
    energy += sum(len(cross & shift(cross, h)) for h in db)
    require(total_cross == energy, 'cross triangle sum mismatch')
    return hist


def compute(fixture):
    validate_internal(INTERNAL)
    all_d = {frozenset(symmetric(c)) for c in INTERNAL}
    type_sets = []
    for rep in ((1, 2), (1, 3)):
        orbit = {frozenset(a*x % P for x in symmetric(rep)) for a in range(1, P)}
        require(len(orbit) == 5, 'internal shape orbit')
        type_sets.append(orbit)
    require(type_sets[0].isdisjoint(type_sets[1]) and
            type_sets[0] | type_sets[1] == all_d, 'internal shape coverage')
    energy_rows = {}
    energy_states = 0
    for d in range(7, 11):
        values = []
        survivors = []
        for s in range(0, min(d, 10)+1, 2):
            c = d-s
            lhs = s*(s-1)+c*(c-1)
            rhs = 3*s+(2*d-14)*(10-s)
            quadratic = 2*s*s-17*s+d*d-21*d+140
            require(lhs-rhs == quadratic, 'energy expansion')
            values.append(quadratic)
            if quadratic <= 0:
                survivors.append([s, c])
            energy_states += 1
        energy_rows[str(d)] = {'values': values, 'surviving_sc': survivors}
    gap4 = validate_gaps(FOUR_GAPS, 4, lambda g: min(g) >= 2)
    gap5 = validate_gaps(FIVE_GAPS, 5,
                         lambda g: sorted(g) == [1, 2, 2, 3, 3])
    target4 = (0, 2, 2, 1, 1)
    require(target4 not in FOUR_GAPS.values(), 'four-point obstruction lost')
    equalities4 = 0
    for d in all_d:
        for values in itertools.combinations(range(P), 4):
            t = vector(set(values))
            if all(vector(set(d))[k-1]+t[k-1] == 2+int(k in d)
                   for k in range(1, 6)):
                equalities4 += 1
    require(equalities4 == 0, 'four-point equality survivor')
    five_total = five_antecedents = 0
    for values in itertools.combinations(range(P), 5):
        t = vector(set(values))
        if t[0]+t[2] <= 2:
            five_antecedents += 1
            require(t[1] >= 3, 'five-point implication false')
        five_total += 1
    nine_cases = []
    for ac in ((1, 2), (4, 5)):
        da = symmetric(ac)
        for gaps in FIVE_GAPS:
            cross = points_of(gaps)
            t = vector(cross)
            if any(vector(da)[k-1]+t[k-1] > (3 if k in da else 4)
                   for k in range(1, 6)):
                continue
            ta = 2*sum(t[k-1] for k in ac)
            for bc in INTERNAL:
                db = symmetric(bc)
                if any(vector(db)[k-1]+t[k-1] > (3 if k in db else 4)
                       for k in range(1, 6)):
                    continue
                tb = 2*sum(t[k-1] for k in bc)
                limit = 10 if da == db else 15
                require(ta+tb > limit, 'nine-case sum obstruction failed')
                require(any(len(cross & shift(da, k))+len(cross & shift(db, k)) > 3
                            for k in cross), 'nine-case literal red obstruction')
                nine_cases.append({'A': list(ac), 'gaps': list(gaps), 'B': list(bc),
                                   'triangle_sum': ta+tb, 'cap_sum': limit})
    ten_local = []
    adjacent = type_sets[0]
    for d in all_d:
        for values in itertools.combinations(range(P), 6):
            cross = set(values)
            t = vector(cross)
            if any(vector(set(d))[k-1]+t[k-1] > (3 if k in d else 6)
                   for k in range(1, 6)):
                continue
            require(d not in adjacent, 'ten adjacent internal mask survives')
            tx = sum(len(cross & shift(cross, h)) for h in d)
            require(tx >= 10, 'ten-case triangle lower bound failed')
            ten_local.append(tx)
    line = fixture.read_text().strip()
    rows = decode_graph6(line)
    da = {x for x in rows[0] if x < 11}
    db = {x-11 for x in rows[11] if x >= 11}
    cross = {x-11 for x in rows[0] if x >= 11}
    hist = verify_literal_identities(da, db, cross, rows)
    require(max(hist[0]) == 4 and max(hist[1]) == 5, 'prior fixture book caps')
    require(hist[0].get(4, 0) > 0, 'prior fixture incorrectly treated as target')
    controls = 0
    for a in range(32):
        da = symmetric(i+1 for i in range(5) if a >> i & 1)
        b = (a*13+7) % 32
        db = symmetric(i+1 for i in range(5) if b >> i & 1)
        word = (a*1013+17) % 2048
        cross = {i for i in range(11) if word >> i & 1}
        verify_literal_identities(da, db, cross)
        controls += 1
    # Reject incomplete or damaged small-case inputs; checks remain active under -O.
    failures = 0
    bad_internal = dict(INTERNAL)
    bad_internal[(1, 2)] = (1, 1, 2, 1, 0)
    bad_gap = dict(FOUR_GAPS)
    bad_gap[(4, 2, 3, 2)] = target4
    missing_gap = dict(FOUR_GAPS)
    del missing_gap[(5, 2, 2, 2)]
    bad_padding = line[:-1] + chr(ord(line[-1]) ^ 1)
    for operation in (
        lambda: validate_internal(bad_internal),
        lambda: validate_internal({k: v for k, v in INTERNAL.items() if k != (1, 2)}),
        lambda: validate_gaps(bad_gap, 4, lambda g: min(g) >= 2),
        lambda: validate_gaps(missing_gap, 4, lambda g: min(g) >= 2),
        lambda: decode_graph6(line[:-1]),
        lambda: decode_graph6(bad_padding),
    ):
        rejected = False
        try:
            operation()
        except ValueError:
            rejected = True
        require(rejected, 'damaged input was accepted')
        failures += 1
    # This deliberately wrong first cross term omits reflection of oriented S.
    da, db, cross = symmetric((1, 2)), symmetric((4, 5)), {0, 1, 4, 6, 8}
    require(any(len(da & shift(cross, k))+len(cross & shift(db, k)) !=
                len(cross & shift(da, k))+len(cross & shift(db, k))
                for k in range(11)), 'orientation fault not detected')
    failures += 1
    bad_rows = literal_rows(da, db, cross)
    bad_rows[0].discard(1)
    rejected = False
    try:
        verify_literal_identities(da, db, cross, bad_rows)
    except ValueError:
        rejected = True
    require(rejected, 'damaged literal graph accepted')
    failures += 1
    return {
        'internal_masks': len(all_d), 'energy_states': energy_states,
        'energy': energy_rows, 'four_gap_shapes': len(FOUR_GAPS),
        'four_gap_sets': gap4, 'four_point_equality_survivors': equalities4,
        'five_gap_shapes': len(FIVE_GAPS), 'five_gap_sets': gap5,
        'five_point_sets': five_total, 'implication_antecedents': five_antecedents,
        'nine_cases': nine_cases, 'ten_local_masks': len(ten_local),
        'ten_triangle_minimum': min(ten_local),
        'baseline_degrees': sorted({len(r) for r in rows}),
        'baseline_red_histogram': {str(k): v for k, v in sorted(hist[0].items())},
        'baseline_blue_histogram': {str(k): v for k, v in sorted(hist[1].items())},
        'literal_control_graphs': controls+1, 'literal_control_spines': 231*(controls+1),
        'damaged_or_fault_controls': failures,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=HERE/'expected.json')
    parser.add_argument('--fixture', type=Path, default=HERE/'primary22.g6')
    args = parser.parse_args()
    actual = compute(args.fixture)
    expected = json.loads(args.expected.read_text())['check']
    require(actual == expected, 'compact expected check output mismatch')
    print(json.dumps(actual, sort_keys=True))


if __name__ == '__main__':
    main()
