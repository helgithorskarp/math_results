"""Independent bitset validation; no imports from check.py or generator.

The exhaustive scan is supplementary: PROOF.md is an ordinary proof.
"""
import argparse
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FULL = (1 << 11)-1
UNIVERSE = (1 << 22)-1


def ensure(test, message):
    if not test:
        raise RuntimeError(message)


def rotate(mask, k):
    k %= 11
    return ((mask << k) | (mask >> (11-k))) & FULL


def read_graph6(path):
    data = path.read_bytes().strip()
    ensure(len(data) == 40 and data[0] == 85, 'expected a22-vertex graph6')
    value = 0
    for char in data[1:]:
        ensure(63 <= char <= 126, 'graph6 character out of range')
        value = value*64+char-63
    ensure(value & 7 == 0, 'nonzero graph6 padding')
    value >>= 3
    rows = [0]*22
    for j in range(1, 22):
        for i in range(j):
            position = j*(j-1)//2+i
            if value >> (230-position) & 1:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
    return rows


def adjacency(da, db, s):
    rows = []
    reverse = sum(1 << ((-i) % 11) for i in range(11) if s >> i & 1)
    for i in range(11):
        rows.append(rotate(da, i) | (rotate(s, i) << 11))
    for i in range(11):
        rows.append(rotate(reverse, i) | (rotate(db, i) << 11))
    return rows


def validate_rows(da, db, s, supplied=None):
    rows = adjacency(da, db, s)
    if supplied is not None:
        ensure(rows == supplied, 'literal primary graph disagrees with orbit masks')
    c = s.bit_count()
    degree = (da.bit_count()+c, db.bit_count()+c)
    hist = [{}, {}]
    for i in range(22):
        ensure(not rows[i] >> i & 1, 'literal loop')
        for j in range(i+1, 22):
            red = rows[i] >> j & 1
            ensure(red == (rows[j] >> i & 1), 'literal asymmetry')
            common = (rows[i] & rows[j]).bit_count()
            if j < 11:
                k = (j-i) % 11
                orbit = (da & rotate(da, k)).bit_count()+(s & rotate(s, k)).bit_count()
                dsum = 2*degree[0]
            elif i >= 11:
                k = (j-i) % 11
                orbit = (db & rotate(db, k)).bit_count()+(s & rotate(s, k)).bit_count()
                dsum = 2*degree[1]
            else:
                k = (j-11-i) % 11
                orbit = (s & rotate(da, k)).bit_count()+(s & rotate(db, k)).bit_count()
                dsum = degree[0]+degree[1]
            ensure(common == orbit, 'literal red orbit identity')
            if red:
                pages = common
                index = 0
            else:
                pages = (UNIVERSE & ~(rows[i] | rows[j] | (1 << i) | (1 << j))).bit_count()
                ensure(pages == 20-dsum+orbit, 'literal blue orbit identity')
                index = 1
            hist[index][pages] = hist[index].get(pages, 0)+1
    return hist


def compute(fixture):
    internal = []
    by_size = {}
    for word in range(32):
        mask = 0
        for i in range(1, 6):
            if word >> (i-1) & 1:
                mask |= (1 << i) | (1 << (11-i))
        internal.append(mask)
        by_size.setdefault(mask.bit_count(), []).append(mask)
    ensure(len(set(internal)) == 32, 'internal domain')
    correlations = [tuple((s & rotate(s, k)).bit_count() for k in range(1, 6))
                    for s in range(2048)]
    rotated = {d: tuple(rotate(d, k) for k in range(11)) for d in internal}
    literal = read_graph6(fixture)
    da = literal[0] & FULL
    db = literal[11] >> 11
    s = literal[0] >> 11
    hist = validate_rows(da, db, s, literal)
    ensure(max(hist[0]) == 4 and max(hist[1]) == 5, 'known baseline caps')
    ensure(len({r.bit_count() for r in literal}) == 2, 'known baseline degree classes')
    controls = 0
    for number in range(44):
        da = internal[(number*7+3) % 32]
        db = internal[(number*17+5) % 32]
        if number < 12:
            s = (1 << number)-1
        else:
            s = ((number+29)*683) % 2048
        validate_rows(da, db, s)
        controls += 1
    families = {}
    for degree_a, degree_b in ((8, 8), (8, 10), (9, 9), (10, 10)):
        counts = {'templates': 0, 'A_violation': 0, 'B_violation': 0,
                  'cross_violation': 0, 'survivors': 0}
        for s in range(2048):
            c = s.bit_count()
            avec = by_size.get(degree_a-c, ())
            bvec = by_size.get(degree_b-c, ())
            cs = correlations[s]
            for da in avec:
                ca = correlations[da]
                bad_a = any(ca[k-1]+cs[k-1] >
                            (3 if da >> k & 1 else 2*degree_a-14)
                            for k in range(1, 6))
                for db in bvec:
                    counts['templates'] += 1
                    if bad_a:
                        counts['A_violation'] += 1
                        continue
                    cb = correlations[db]
                    if any(cb[k-1]+cs[k-1] >
                           (3 if db >> k & 1 else 2*degree_b-14)
                           for k in range(1, 6)):
                        counts['B_violation'] += 1
                        continue
                    found = False
                    for k in range(11):
                        q = (s & rotated[da][k]).bit_count()+(s & rotated[db][k]).bit_count()
                        limit = 3 if s >> k & 1 else degree_a+degree_b-14
                        if q > limit:
                            found = True
                            break
                    if found:
                        counts['cross_violation'] += 1
                    else:
                        counts['survivors'] += 1
        ensure(sum(counts[x] for x in ('A_violation', 'B_violation', 'cross_violation', 'survivors'))
               == counts['templates'], 'incomplete scan accounting')
        ensure(counts['survivors'] == 0, 'a two-orbit host survived')
        families[f'{degree_a},{degree_b}'] = counts
    total = sum(f['templates'] for f in families.values())
    ensure(total == 265912, 'incomplete degree-compatible template coverage')
    return {
        'families': families, 'total_templates': total,
        'baseline_masks': {'A': da_from_rows(literal), 'B': db_from_rows(literal),
                           'cross': literal[0] >> 11},
        'baseline_red_histogram': {str(k): v for k, v in sorted(hist[0].items())},
        'baseline_blue_histogram': {str(k): v for k, v in sorted(hist[1].items())},
        'literal_control_graphs': controls+1, 'literal_control_spines': 231*(controls+1),
    }


def da_from_rows(rows):
    return rows[0] & FULL


def db_from_rows(rows):
    return rows[11] >> 11


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=HERE/'expected.json')
    parser.add_argument('--fixture', type=Path, default=HERE/'primary22.g6')
    args = parser.parse_args()
    actual = compute(args.fixture)
    expected = json.loads(args.expected.read_text())['verify']
    ensure(actual == expected, 'compact expected verifier output mismatch')
    print(json.dumps(actual, sort_keys=True))


if __name__ == '__main__':
    main()
