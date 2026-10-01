"""Solver-free exact audit: partition rows, linear elimination, blue stars.

Actual author six-books-3, researcher. Imports no generator. The credited
nine-core classification is a premise; this audits the new exclusion.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, combinations_with_replacement, product
import json
from math import lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASKS = (30083408, 51316320, 51317328, 54986080, 54987088,
         55740996, 126126276, 126158020, 126158146)
TEN_PAIRS = tuple(combinations(range(10), 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def graph(mask):
    adjacency = [[False] * 10 for _ in range(10)]
    for bit, (i, j) in enumerate(combinations(range(8), 2)):
        if mask & (1 << bit):
            adjacency[i + 2][j + 2] = adjacency[j + 2][i + 2] = True
    for low, i, j in ((0, 2, 3), (1, 4, 5)):
        adjacency[low][i] = adjacency[i][low] = True
        adjacency[low][j] = adjacency[j][low] = True
    degrees = [sum(r) for r in adjacency]
    require(degrees == [2, 2] + [3] * 8, 'Bad local degree sequence')
    require(not any(adjacency[i][j] and adjacency[i][k] and adjacency[j][k]
                    for i, j, k in combinations(range(10), 3)), 'Local triangle')
    return adjacency, degrees


def spine_bounds(adjacency, degrees):
    target = [d + 2 for d in degrees]
    caps = {}
    for i, j in TEN_PAIRS:
        if adjacency[i][j]:
            # Root + local red pages + outside baseline (joint misses variable).
            baseline = (1 + sum(adjacency[i][k] and adjacency[j][k] for k in range(10))
                        + 11 - target[i] - target[j])
            caps[i, j] = 3 - baseline
        else:
            blue_local = sum(not adjacency[i][k] and not adjacency[j][k]
                             for k in range(10) if k not in (i, j))
            caps[i, j] = 6 - blue_local
    require(min(caps.values()) >= 0, 'Negative joint-miss capacity')
    return target, caps


def partition_rows(adjacency, degrees, caps):
    """Four patterns per triple and every subset of the remaining four points."""
    result = []
    first = (1 << 0, (1 << 2) | (1 << 3), 1 << 2, 1 << 3)
    second = (1 << 1, (1 << 4) | (1 << 5), 1 << 4, 1 << 5)
    for a, b, rest in product(first, second, range(16)):
        z = a | b | (rest << 6)
        selected = {i for i in range(10) if z & (1 << i)}
        size = len(selected)
        if not 4 <= size <= 8:
            continue
        if any(caps[i, j] == 0 for i, j in combinations(sorted(selected), 2)):
            continue
        good = True
        for i in range(10):
            if i not in selected:
                local_red = sum(adjacency[i][j] for j in range(10) if j not in selected)
                least_outside_red = max(0, size + (8 - degrees[i]) - 10)
                if local_red + least_outside_red > 3:
                    good = False
            elif sum(not adjacency[i][j] for j in selected if j != i) > 6:
                good = False
        if good:
            result.append(z)
    require(len(result) == len(set(result)), 'Duplicate partition row')
    return sorted(result)


def digest(records):
    return hashlib.sha256(b''.join(json.dumps(x, separators=(',', ':')).encode('ascii')
                                  + b'\n' for x in records)).hexdigest()


def row_histogram(rows):
    return {str(k): n for k, n in sorted(Counter(z.bit_count() for z in rows).items())}


def certify(cut, rows, target, caps):
    require(len(cut['alpha']) == 10 and all(type(x) is int for x in cut['alpha']),
            'Malformed column coefficients')
    require(type(cut['gamma']) is int and type(cut['rhs']) is int,
            'Malformed cut constant')
    weights = {}
    for i, j, weight in cut['beta']:
        require(type(i) is int and type(j) is int and type(weight) is int
                and (i, j) in caps and weight > 0 and (i, j) not in weights,
                'Malformed nonnegative pair weight')
        weights[i, j] = weight
    scores = {}
    for z in rows:
        selected = [i for i in range(10) if z & (1 << i)]
        scores[z] = (cut['gamma'] + sum(cut['alpha'][i] for i in selected)
                     + sum(weights.get((i, j), 0) for i, j in combinations(selected, 2)))
    require(min(scores.values()) >= 0, 'A permitted row has negative score')
    bound = (11 * cut['gamma'] + sum(a * t for a, t in zip(cut['alpha'], target))
             + sum(weight * caps[pair] for pair, weight in weights.items()))
    require(bound == cut['rhs'] and bound <= 0, 'False cut bound')
    return ([z for z in rows if scores[z] == 0] if bound == 0 else []), weights


def reduction(matrix):
    """Exact RREF and an independently checked transformation identity."""
    m, n = len(matrix), len(matrix[0])
    augmented = [[Fraction(x) for x in row]
                 + [Fraction(i == j) for j in range(m)] for i, row in enumerate(matrix)]
    pivots = []
    for c in range(n):
        r = len(pivots)
        pivot = next((i for i in range(r, m) if augmented[i][c]), None)
        if pivot is None:
            continue
        augmented[r], augmented[pivot] = augmented[pivot], augmented[r]
        scale = augmented[r][c]
        augmented[r] = [x / scale for x in augmented[r]]
        for i in range(m):
            if i != r and augmented[i][c]:
                multiple = augmented[i][c]
                augmented[i] = [a - multiple * b for a, b in zip(augmented[i], augmented[r])]
        pivots.append(c)
    rref = [r[:n] for r in augmented]
    transform = [r[n:] for r in augmented]
    require(all(sum(transform[i][k] * matrix[k][j] for k in range(m)) == rref[i][j]
                for i in range(m) for j in range(n)), 'RREF transformation identity fails')
    free = [c for c in range(n) if c not in pivots]
    denominator = lcm(*(x.denominator for row in augmented for x in row))
    integer = [[int(x * denominator) for x in row] for row in augmented]
    return pivots, free, denominator, [r[:n] for r in integer], [r[n:] for r in integer]


def all_incidences(zero, target, caps, weights):
    by_size = {k: [z for z in zero if z.bit_count() == k] for k in range(4, 9)}
    require(not by_size[8], 'Unexpected size-eight row')
    fours = by_size[4]
    saturation_pairs = sorted(weights)
    equations = ([('column', i) for i in range(10)]
                 + [('pair', p) for p in saturation_pairs] + [('count', 0)])

    def entries(z):
        return [int(bool(z & (1 << arg))) if kind == 'column' else
                int(bool(z & (1 << arg[0]) and z & (1 << arg[1]))) if kind == 'pair'
                else 1 for kind, arg in equations]

    matrix = [[entries(z)[j] for z in fours] for j in range(len(equations))]
    pivots, free, denominator, rref, transform = reduction(matrix)
    require(len(free) == 2, 'Unexpected four-row nullity')
    features = {z: ([int(bool(z & (1 << i))) for i in range(10)],
                    [int(bool(z & (1 << i) and z & (1 << j))) for i, j in TEN_PAIRS])
                for z in zero}
    cap_vector = [caps[p] for p in TEN_PAIRS]
    result = []
    high_counts = Counter()
    raw_counts = Counter()

    def high_patterns():
        for seven, five in product(by_size[7], by_size[5]):
            yield (seven, five)
        yield from combinations_with_replacement(by_size[6], 2)
        for six in by_size[6]:
            for fives in combinations_with_replacement(by_size[5], 2):
                yield (six,) + fives
        yield from combinations_with_replacement(by_size[5], 4)

    for high in high_patterns():
        pattern = tuple(sorted((z.bit_count() for z in high), reverse=True))
        raw_counts[pattern] += 1
        column = [sum(features[z][0][i] for z in high) for i in range(10)]
        pair = [sum(features[z][1][p] for z in high) for p in range(45)]
        if any(a > b for a, b in zip(column, target)) or any(a > b for a, b in zip(pair, cap_vector)):
            continue
        high_counts[pattern] += 1
        need_column = [b - a for a, b in zip(column, target)]
        need_pair = {p: caps[p] - pair[ix] for ix, p in enumerate(TEN_PAIRS)}
        wanted = 11 - len(high)
        rhs = need_column + [need_pair[p] for p in saturation_pairs] + [wanted]
        transformed = [sum(a * b for a, b in zip(row, rhs)) for row in transform]
        if any(transformed[i] for i in range(len(pivots), len(equations))):
            continue
        free_bounds = [min(need_column[i] for i in range(10) if fours[f] & (1 << i))
                       for f in free]
        for choices in product(*(range(b + 1) for b in free_bounds)):
            counts = [0] * len(fours)
            for f, value in zip(free, choices):
                counts[f] = value
            good = True
            for r, p in enumerate(pivots):
                numerator = transformed[r] - sum(rref[r][f] * value for f, value in zip(free, choices))
                if numerator < 0 or numerator % denominator:
                    good = False
                    break
                counts[p] = numerator // denominator
            if not good:
                continue
            low = [z for z, count in zip(fours, counts) for _ in range(count)]
            require(len(low) == wanted, 'Elimination lost row count')
            if any(sum(features[z][1][p] for z in low) > need_pair[pair_key]
                   for p, pair_key in enumerate(TEN_PAIRS)):
                continue
            rows = sorted(list(high) + low)
            require(all(sum(bool(z & (1 << i)) for z in rows) == target[i] for i in range(10)),
                    'Elimination lost a column count')
            result.append(rows)
    result.sort()
    require(len(result) == len({tuple(r) for r in result}), 'Duplicate reconstructed matrix')
    audit = {'linear_equations': len(equations), 'four_variables': len(fours),
             'rank': len(pivots), 'free_row_words': [fours[f] for f in free],
             'denominator': denominator,
             'raw_high_patterns': [[list(k), v] for k, v in sorted(raw_counts.items())],
             'high_multisets': [[list(k), v] for k, v in sorted(high_counts.items())]}
    return result, audit


def red_frame(adjacency, rows):
    """Known full red neighborhoods of the ten A vertices, on literal 22 labels."""
    result = []
    for i in range(10):
        mask = 1  # root label 0
        mask |= sum(1 << (j + 1) for j in range(10) if adjacency[i][j])
        mask |= sum(1 << (b + 11) for b, z in enumerate(rows) if not z & (1 << i))
        require(mask.bit_count() == 10, 'Frame is not ten-regular at A')
        result.append(mask)
    return result


def empty_blue_stars(adjacency, rows, b):
    """Visit binary blue stars; common pages use full 22-point neighbor masks."""
    require(type(b) is int and 0 <= b < 11, 'Bad selected star row')
    red_a = red_frame(adjacency, rows)
    vertex = b + 11
    whole = (1 << 22) - 1
    other_b = [c for c in range(11) if c != b]
    red_a_b = sum(1 << (i + 1) for i in range(10) if not rows[b] & (1 << i))
    wanted_blue = 10 - rows[b].bit_count()
    checked = 0
    for word in range(1024):
        if word.bit_count() != wanted_blue:
            continue
        red_b = red_a_b | sum(1 << (c + 11) for ix, c in enumerate(other_b)
                             if not word & (1 << ix))
        require(red_b.bit_count() == 10, 'Star has wrong total red degree')
        failed = False
        for i in range(10):
            if red_b & (1 << (i + 1)):
                pages = (red_a[i] & red_b).bit_count()
                failed |= pages > 3
            else:
                blue_i = whole ^ (red_a[i] | (1 << (i + 1)))
                blue_b = whole ^ (red_b | (1 << vertex))
                pages = (blue_i & blue_b).bit_count()
                failed |= pages > 6
        require(failed, 'A selected outside star meets every A--B cap')
        checked += 1
    return checked


def baseline():
    path = HERE / 'primary21.txt'
    require(hashlib.sha256(path.read_bytes()).hexdigest()
            == '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55',
            'Primary matrix bytes differ')
    matrix = json.loads(path.read_text().split('\n\n', 1)[0])
    require(len(matrix) == 21 and all(len(row) == 21 for row in matrix), 'Primary order differs')
    require(all(matrix[i][i] == 0 for i in range(21)), 'Primary diagonal differs')
    require(all(matrix[i][j] == matrix[j][i] and matrix[i][j] in (0, 1)
                for i, j in combinations(range(21), 2)), 'Primary matrix malformed')
    counts = Counter()
    maxima = [0, 0]
    for i, j in combinations(range(21), 2):
        color = matrix[i][j]
        pages = sum(matrix[i][k] == color and matrix[j][k] == color
                    for k in range(21) if k not in (i, j))
        counts[color] += 1
        maxima[color] = max(maxima[color], pages)
    require([counts[0], counts[1]] == [93, 117] and maxima == [3, 6], 'Primary book baseline differs')


def audit(cuts_path=HERE / 'cuts.json', fixture_path=HERE / 'incidences.json',
          expected_path=HERE / 'expected.json', check_baseline=True):
    cuts = json.loads(cuts_path.read_text())
    require(cuts['schema'] == 1, 'Cut schema differs')
    require(tuple(c['F_mask'] for c in cuts['cuts']) == MASKS, 'Credited nine-core domain differs')
    core_records = []
    remaining = []
    for cut in cuts['cuts']:
        adjacency, degrees = graph(cut['F_mask'])
        target, caps = spine_bounds(adjacency, degrees)
        rows = partition_rows(adjacency, degrees, caps)
        zero, weights = certify(cut, rows, target, caps)
        core_records.append({'F_mask': cut['F_mask'], 'row_sizes': row_histogram(rows),
                             'rows_sha256': digest(rows), 'cut_rhs': cut['rhs'],
                             'zero_row_sizes': row_histogram(zero)})
        if zero:
            remaining.append((cut['F_mask'], adjacency, target, caps, weights, zero))
    require(len(remaining) == 1, 'More than one residual core')
    mask, adjacency, target, caps, weights, zero = remaining[0]
    matrices, linear_audit = all_incidences(zero, target, caps, weights)
    fixture = json.loads(fixture_path.read_text())
    require(fixture['schema'] == 1 and fixture['F_mask'] == mask, 'Incidence fixture header differs')
    require([r['rows'] for r in fixture['records']] == matrices,
            'Complete incidence matrices differ entrywise')
    star_tests = sum(empty_blue_stars(adjacency, r['rows'], r['empty_star_row'])
                     for r in fixture['records'])
    expected = json.loads(expected_path.read_text())
    require(expected['complete'] is True and expected['cores'] == core_records,
            'Core/row coverage differs')
    require(expected['surviving_F_mask'] == mask, 'Residual core differs')
    require(expected['high_multisets'] == linear_audit['high_multisets'], 'High-row coverage differs')
    patterns = Counter(tuple(sorted((z.bit_count() for z in rows if z.bit_count() > 4), reverse=True))
                       for rows in matrices)
    require(expected['incidence_patterns'] == [[list(k), v] for k, v in sorted(patterns.items())],
            'Incidence row patterns differ')
    require(expected['incidence_matrices'] == len(matrices)
            and expected['incidences_sha256'] == digest(matrices), 'Incidence digest differs')
    require(expected['empty_star_records'] == len(matrices)
            and expected['selected_star_tests'] == star_tests
            and expected['extendible_matrices'] == 0, 'Star coverage differs')
    if check_baseline:
        baseline()
    return {'verified': True, 'cores': len(core_records), 'strict_cuts': 8,
            'incidence_matrices': len(matrices), 'incidences_sha256': digest(matrices),
            'selected_star_tests': star_tests, 'linear_audit': linear_audit,
            'baseline_red_edges': 93 if check_baseline else None,
            'baseline_page_maxima': [3, 6] if check_baseline else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cuts', type=Path, default=HERE / 'cuts.json')
    parser.add_argument('--incidences', type=Path, default=HERE / 'incidences.json')
    parser.add_argument('--expected', type=Path, default=HERE / 'expected.json')
    args = parser.parse_args()
    print(json.dumps(audit(args.cuts, args.incidences, args.expected), sort_keys=True))


if __name__ == '__main__':
    main()
