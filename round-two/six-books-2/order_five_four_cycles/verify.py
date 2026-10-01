"""Independent literal certificate and unnormalized cyclic-correlation check.

No generator code is imported. Full mode also examines 4,562,500 templates
with every phase and both possible five-cycle generators. See PROOF.md.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import random
import time

HERE = Path(__file__).resolve().parent
FULL = 4562500
POPC = [mask.bit_count() for mask in range(32)]
ROT = [[((mask << d) | (mask >> (5 - d))) & 31 if d else mask
        for d in range(5)] for mask in range(32)]
INV = [sum(1 << ((-d) % 5) for d in range(5) if mask >> d & 1) for mask in range(32)]
RED = [[[POPC[mask & ROT[other][d]] for d in range(5)]
        for other in range(32)] for mask in range(32)]
BLUE = [[[5 - POPC[mask] - POPC[other] + RED[mask][other][d] for d in range(5)]
         for other in range(32)] for mask in range(32)]
ORBIT_PAIRS = list(itertools.combinations(range(4), 2))
SPINES = ([(i, i, d) for i in range(4) for d in (1, 2)]
          + [(i, j, d) for i, j in ORBIT_PAIRS for d in range(5)])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matrix(internal, values):
    result = [[0] * 4 for _ in range(4)]
    for i in range(4):
        result[i][i] = internal[i]
    for (i, j), value in zip(ORBIT_PAIRS, values):
        result[i][j] = value
        result[j][i] = INV[value]
    return result


def neighbors(P, fixed):
    n = 20 + len(fixed)
    result = [set() for _ in range(n)]
    for i, j in itertools.combinations(range(n), 2):
        if j >= 20:
            color = 0 if i >= 20 else fixed[j - 20] >> (i // 5) & 1
        else:
            a, x = divmod(i, 5)
            b, y = divmod(j, 5)
            color = P[a][b] >> ((y - x) % 5) & 1
        if color:
            result[i].add(j)
            result[j].add(i)
    return result


def literal_pages(rows, i, j):
    color = int(j in rows[i])
    pages = (rows[i] & rows[j] if color else set(range(len(rows))) - {i, j} - rows[i] - rows[j])
    return color, pages


def orbit_pages(P, fixed, i, j, d):
    color = P[i][j] >> d & 1
    table = RED if color else BLUE
    count = sum(table[P[i][k]][P[j][k]][d] for k in range(4)) - (0 if color else 2)
    count += sum(((f >> i) & 1) == color and ((f >> j) & 1) == color for f in fixed)
    return color, count


def fixed_cycle_pages(P, fixed, f, orbit):
    color = fixed[f] >> orbit & 1
    count = sum((POPC[P[orbit][k]] if color else 5 - POPC[P[orbit][k]])
                for k in range(4) if (fixed[f] >> k & 1) == color)
    count -= 0 if color else 1
    count += sum(g != f and color == 0 and (fixed[g] >> orbit & 1) == 0
                 for g in range(len(fixed)))
    return color, count


def quotient_physical(P, fixed, i, j):
    if j < 20:
        a, x = divmod(i, 5)
        b, y = divmod(j, 5)
        return orbit_pages(P, fixed, a, b, (y - x) % 5)
    if i < 20:
        return fixed_cycle_pages(P, fixed, j - 20, i // 5)
    return 0, 5 * sum((fixed[i - 20] >> k & 1) == 0 and (fixed[j - 20] >> k & 1) == 0
                      for k in range(4))


def first_violation(P, fixed):
    for i, j, d in SPINES:
        color, count = orbit_pages(P, fixed, i, j, d)
        if count > (3 if color else 6):
            return i, j, d, color, count
    for f in range(2):
        for orbit in range(4):
            color, count = fixed_cycle_pages(P, fixed, f, orbit)
            if count > (3 if color else 6):
                return 4 + f, orbit, 0, color, count
    count = 5 * sum((fixed[0] >> k & 1) == 0 and (fixed[1] >> k & 1) == 0 for k in range(4))
    return (4, 5, 0, 0, count) if count > 6 else None


def identity_controls():
    rng = random.Random(20261001)
    tests = 0
    for _ in range(64):
        P = matrix([rng.choice((0, 12, 18, 30)) for _ in range(4)],
                   [rng.randrange(32) for _ in range(6)])
        fixed = [rng.randrange(16), rng.randrange(16)]
        rows = neighbors(P, fixed)
        for i, j in itertools.combinations(range(22), 2):
            color, pages = literal_pages(rows, i, j)
            require(quotient_physical(P, fixed, i, j) == (color, len(pages)), 'Correlation identity control')
            tests += 1
    P = matrix([12, 18, 0, 0], [4, 28, 28, 26, 26, 30])
    rows = neighbors(P, [3])
    roots = ([{t, (t + 1) % 5} for t in range(5)] + [{t, (t + 2) % 5} for t in range(5)]
             + [{t, 5} for t in range(5)] + [{t, 6} for t in range(5)] + [{5, 6}])
    hist = {0: collections.Counter(), 1: collections.Counter()}
    for i, j in itertools.combinations(range(21), 2):
        require((j in rows[i]) == roots[i].isdisjoint(roots[j]), 'Literal Kneser root control')
        color, pages = literal_pages(rows, i, j)
        require(quotient_physical(P, [3], i, j) == (color, len(pages)), 'Kneser correlation control')
        hist[color][len(pages)] += 1
    require(hist[1] == {3: 105} and hist[0] == {5: 105}, 'Kneser page histograms')
    print(tests, 'arbitrary literal correlation controls and 210 Kneser spines passed')


def reduction_controls():
    # These checks validate written algebra, not universal host enumeration.
    local_count = admitted = 0
    for g in (1, 2):
        for left, right in itertools.product(range(32), repeat=2):
            local_count += 1
            q = POPC[left] + POPC[right]
            actual = (4 <= q <= 6 and RED[left][left][g] + RED[right][right][g] <= 2
                      and BLUE[left][left][(2 * g) % 5] + BLUE[right][right][(2 * g) % 5] <= 2)
            predicted = False
            if POPC[left] in (2, 3) and POPC[right] in (2, 3):
                hleft = 1 if RED[left][left][1] == 1 else 2
                hright = 1 if RED[right][right][1] == 1 else 2
                predicted = hleft == hright and (g == hleft or q == 5)
            require(actual == predicted, 'Disjoint local-mask characterization')
            admitted += actual
    require(local_count == 2048 and admitted == 300, 'Disjoint local control domain')
    # Degree nine really permits the other generator: retain this case.
    require(RED[3][3][2] + RED[26][26][2] == 2 and BLUE[3][3][4] + BLUE[26][26][4] == 2,
            'Missing alternate degree-nine generator')
    multiplicity = 0
    for ac, ad, bc, bd in itertools.product((2, 3), repeat=4):
        totals = [ac + ad, bc + bd, ac + bc, ad + bd]
        multiplicity += 1 << sum(total == 5 for total in totals)
    require(multiplicity == 82, 'Disjoint cardinality/generator classes')
    singleton_or_empty = [m for m in range(32) if POPC[m] <= 1]
    count = 0
    for g in (1, 2):
        for a, b, c in itertools.product(singleton_or_empty, singleton_or_empty, range(32)):
            count += 1
            if not 8 <= 4 + POPC[a] + POPC[b] + POPC[c] <= 10:
                continue
            require(not (sum(RED[m][m][g] for m in (a, b, c)) <= 1
                         and sum(BLUE[m][m][(2 * g) % 5] for m in (a, b, c)) <= 6),
                    'Unexpected shared-cycle possibility')
    require(count == 2304, 'Shared-cycle control domain')
    found = []
    scalar_count = 0
    energy = lambda *degrees: sum((5 - x) * (4 - x) for x in degrees)
    for sb, sc, sd in itertools.product((0, 2), repeat=3):
        for a, b, c, f, d, e in itertools.product(range(6), repeat=6):
            scalar_count += 1
            degrees = [2 + a + b + c, 1 + sb + a + f + d,
                       1 + sc + b + f + e, sd + c + d + e]
            if not all(8 <= value <= 10 for value in degrees):
                continue
            if a > 3 or b > 3 or sb + a > 3 or sc + b > 3:
                continue
            if sc + e < 3 or sb + d < 3 or sd + d < 4 or sd + e < 4:
                continue
            if energy(a, b, c) > 12:
                continue
            if sb == 0 and energy(a, f, d) > 8:
                continue
            if sc == 0 and energy(b, f, e) > 8:
                continue
            if sd == 0 and energy(c, d, e) > 4:
                continue
            found.append([sb, sc, sd, a, b, c, f, d, e, degrees])
    require(scalar_count == 373248 and found == [[0, 0, 2, 3, 3, 2, 3, 3, 3, [10] * 4]],
            'Shared-independent scalar reduction')
    print('2048 disjoint local states, 82 size/generator classes, 2304 shared-cycle and 373248 scalar states checked')


def decode(key):
    require(isinstance(key, list) and key and key[0] in ('D', 'O'), 'Invalid template key')
    require(all(type(value) is int for value in key[1:]), 'Noninteger template key')
    if key[0] == 'D':
        require(len(key) == 9 and all(g in (1, 2) for g in key[1:5]) and key[5] in (3, 26), 'Disjoint gauge')
        allowed = {ROT[mask][shift] for mask in (3, 26) for shift in range(5)}
        require(all(mask in allowed for mask in key[6:]), 'Disjoint mask shape')
        _, ga, gb, gc, gd, ac, ad, bc, bd = key
        totals = [POPC[ac] + POPC[ad], POPC[bc] + POPC[bd], POPC[ac] + POPC[bc], POPC[ad] + POPC[bd]]
        require(all(total == 5 or g == 1 for g, total in zip((ga, gb, gc, gd), totals)),
                'Alternate generator outside degree nine')
        return matrix([(1 << g) | (1 << (5 - g)) for g in (ga, gb, gc, gd)],
                      [1, ac, ad, bc, bd, 1]), [3, 12]
    require(len(key) == 7 and all(value in (1, 2) for value in key[1:4]), 'Overlap gauge')
    _, a, b, c, ad, bc, cd = key
    require(0 <= ad < 32 and POPC[ad] == 2 and all(0 <= m < 32 and POPC[m] == 3 for m in (bc, cd)),
            'Overlap mask cardinalities')
    return matrix([0, 0, 0, 18], [31 ^ (1 | 1 << a), 31 ^ (1 | 1 << b), ad,
                                          bc, 31 ^ (1 | 1 << c), cd]), [3, 5]


def check_certificates(path, expected):
    data = json.loads(path.read_text())
    require(data.get('status') == 'complete' and data.get('templates_scanned') == 18250,
            'Incomplete normalized certificate domain')
    require(data.get('method') == 'literal-normalized' and data.get('survivors') == [], 'Unexpected producer state')
    records = data['records']
    require(len(records) == 18250, 'Missing certificate records')
    seen, counts, hist = set(), collections.Counter(), collections.Counter()
    for key, witness in records:
        P, fixed = decode(key)
        require(tuple(key) not in seen, 'Duplicate template')
        seen.add(tuple(key))
        counts[key[0]] += 1
        rows = neighbors(P, fixed)
        require(isinstance(witness, list) and len(witness) == 4, 'Malformed book witness')
        i, j, color, pages = witness
        require(all(type(x) is int for x in (i, j, color)) and 0 <= i < j < 22 and color in (0, 1),
                'Invalid witness spine')
        require(isinstance(pages, list) and all(type(k) is int and 0 <= k < 22 for k in pages),
                'Invalid witness vertices')
        require(len(pages) == (4 if color else 7) and len(set(pages)) == len(pages)
                and i not in pages and j not in pages, 'Invalid page count or repeated endpoint')
        actual_color, actual_pages = literal_pages(rows, i, j)
        require(actual_color == color and set(pages) <= actual_pages, 'Witness is not a literal forbidden book')
        require(quotient_physical(P, fixed, i, j) == (color, len(actual_pages)), 'Entrywise quotient/literal mismatch')
        hist[key[0], color, len(actual_pages)] += 1
    require(dict(counts) == {'D': 10250, 'O': 8000} == data['counts'], 'Certificate family coverage')
    # Distinct admissible keys and exact family sizes cover each normalized grid.
    digest = hashlib.sha256(json.dumps(records, separators=(',', ':')).encode()).hexdigest()
    require(digest == data['records_sha256'] == expected['literal_records_sha256'], 'Certificate digest differs')
    require([[list(k), v] for k, v in sorted(hist.items())] == data['first_violation_histogram'], 'Literal histogram')
    print('All 18250 distinct normalized witnesses verified literally and entrywise by correlation')
    return digest


def unnormalized():
    for h in (1, 2):
        allowed = sorted({ROT[mask][d] for mask in (1 | 1 << h, 31 ^ (1 | 1 << ((2 * h) % 5)))
                          for d in range(5)})
        singles = [1 << d for d in range(5)]
        for ab, cd, ac, ad, bc, bd in itertools.product(singles, singles, allowed, allowed, allowed, allowed):
            totals = [POPC[ac] + POPC[ad], POPC[bc] + POPC[bd], POPC[ac] + POPC[bc], POPC[ad] + POPC[bd]]
            choices = [(h, 3 - h) if total == 5 else (h,) for total in totals]
            for generators in itertools.product(*choices):
                internal = [(1 << g) | (1 << (5 - g)) for g in generators]
                yield 'D', matrix(internal, [ab, ac, ad, bc, bd, cd]), [3, 12]
    size_two = [m for m in range(32) if POPC[m] == 2]
    size_three = [m for m in range(32) if POPC[m] == 3]
    for g in (1, 2):
        cycle = (1 << g) | (1 << (5 - g))
        for ab, ac, ad, bc, bd, cd in itertools.product(size_three, size_three, size_two,
                                                      size_three, size_three, size_three):
            yield 'O', matrix([0, 0, 0, cycle], [ab, ac, ad, bc, bd, cd]), [3, 5]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--literal', type=Path)
    parser.add_argument('--output', type=Path, default=Path('orbit_results.json'))
    parser.add_argument('--limit', type=int, default=FULL)
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--certificates-only', action='store_true')
    args = parser.parse_args()
    if not 1 <= args.limit <= FULL:
        parser.error('--limit must be between 1 and 4562500')
    if not args.controls and args.literal is None:
        parser.error('Supply --literal or select --controls')
    identity_controls()
    reduction_controls()
    if args.controls:
        return
    expected = json.loads((HERE / 'expected.json').read_text())
    literal_digest = check_certificates(args.literal, expected)
    if args.certificates_only:
        print('Complete normalized certificates checked; unnormalized phase replay omitted')
        return
    start = time.perf_counter()
    counts, hist = collections.Counter(), collections.Counter()
    digest = hashlib.sha256()
    for rank, (family, P, fixed) in enumerate(unnormalized()):
        if rank == args.limit:
            break
        counts[family] += 1
        witness = first_violation(P, fixed)
        require(witness is not None, 'Unexpected unnormalized surviving template')
        hist[family, witness[3], witness[4]] += 1
        digest.update(bytes(witness))
        if (rank + 1) % 250000 == 0:
            print('Unnormalized templates', rank + 1, 'seconds', round(time.perf_counter() - start, 2), flush=True)
    result = {'status': 'complete' if args.limit == FULL else 'partial',
              'method': 'unnormalized-correlations', 'counts': dict(counts),
              'templates_scanned': sum(counts.values()), 'survivors': [],
              'witness_sha256': digest.hexdigest(), 'literal_records_sha256': literal_digest,
              'first_violation_histogram': [[list(k), v] for k, v in sorted(hist.items())],
              'seconds': round(time.perf_counter() - start, 3)}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    if args.limit == FULL:
        require(dict(counts) == {'D': 2562500, 'O': 2000000}, 'Unnormalized domain coverage')
        require(result['witness_sha256'] == expected['unnormalized_witness_sha256'], 'Unnormalized witness digest')
        require(result['first_violation_histogram'] == expected['unnormalized_histogram'], 'Unnormalized histogram')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
