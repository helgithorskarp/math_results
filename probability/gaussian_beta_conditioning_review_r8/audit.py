"""Exact algebra controls for affine Gaussian replica projection.

These controls supplement the written proof; they do not infer its
universal sign from finite cases. Only Python standard-library rationals.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import comb, factorial
from pathlib import Path
from collections import Counter
import argparse
import json


def require(test, message):
    if not test:
        raise ValueError(message)


def dot(a, b):
    require(len(a) == len(b), 'vector dimension')
    return sum((x*y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def total(points):
    return tuple(sum(row[j] for row in points) for j in range(len(points[0])))


def projection(points, block, remaining, d):
    require(block and remaining, 'nonempty blocks required by audit')
    require(set(block).isdisjoint(remaining), 'overlapping positions')
    require(len(set(block+remaining)) == len(block+remaining), 'repeated position')
    require(d >= 1, 'positive Gaussian dimension')
    points = [tuple(map(F, row)) for row in points]
    require(all(len(row) == len(points[0]) for row in points), 'mixed dimensions')
    origin = points[remaining[0]]
    centered = [sub(row, origin) for row in points]
    basis = []
    for i in remaining[1:]:
        v = centered[i]
        for u in basis:
            coefficient = dot(v, u)/dot(u, u)
            v = tuple(x-coefficient*y for x, y in zip(v, u))
        if dot(v, v):
            basis.append(v)
    require(len(basis) <= d, 'negative block affine rank exceeds dimension')
    projected = []
    for row in centered:
        v = [F(0)]*len(row)
        for u in basis:
            coefficient = dot(row, u)/dot(u, u)
            v = [x+coefficient*y for x, y in zip(v, u)]
        projected.append(tuple(v))
    residual = [sub(a, b) for a, b in zip(centered, projected)]
    require(all(dot(residual[i], residual[i]) == 0 for i in remaining),
            'remaining center outside affine subspace')
    require(all(dot(a, b) == 0 for a in projected for b in residual),
            'projection not orthogonal')
    energy = sum(dot(residual[i], residual[i]) for i in block)
    residual_sum = total([residual[i] for i in block])
    squared_sum = dot(residual_sum, residual_sum)
    return centered, projected, len(basis), energy, squared_sum


def variance(points, positions):
    rows = [points[i] for i in positions]
    result = sum(dot(row, row) for row in rows)-dot(total(rows), total(rows))/len(rows)
    pairs = sum(dot(sub(a, b), sub(a, b)) for a, b in combinations(rows, 2))/len(rows)
    require(result == pairs and result >= 0, 'independent variance identity')
    return result


def check_case(name, points, block, remaining, expected_rank):
    original, projected, rank, energy, squared_sum = projection(points, block, remaining, 5)
    require(rank == expected_rank, 'unexpected affine rank')
    require(squared_sum <= len(block)*energy, 'residual Cauchy bound')
    digest = sha256()
    count = 0
    for size in range(len(remaining)+1):
        for selected in combinations(remaining, size):
            positions = block+list(selected)
            correction = variance(original, positions)-variance(projected, positions)
            expected = energy-squared_sum/len(positions)
            require(correction == expected, 'affine correction identity')
            digest.update((str((selected, correction))+'\n').encode())
            count += 1
    return {'case': name, 'positive_positions': len(block),
            'remaining_positions': len(remaining), 'affine_rank': rank,
            'residual_energy': str(energy), 'squared_residual_sum': str(squared_sum),
            'subsets_verified': count, 'identity_sha256': digest.hexdigest()}


def generic_controls():
    # Six affine-independent remaining centers in a displaced five-plane.
    origin = (2, -1, 3, 0, 2, 5, -4)
    negative = [origin]+[tuple(origin[j]+int(i == j) for j in range(7)) for i in range(5)]
    positive = [(1, 2, -1, 3, 1, 8, -2), (3, -2, 4, 0, 5, 9, -1),
                (0, 3, 2, 1, -3, 4, -6)]
    rows = [check_case('off_centroid_five_plane', positive+negative,
                       list(range(3)), list(range(3, 9)), 5)]
    # Nine remaining positions, with repetitions, still lie on a line.
    negative = [(i % 3, 2, 0, -1, 4, 3) for i in range(9)]
    positive = [(i, i*i % 7, i % 2, 2, -i, 0) for i in range(7)]
    rows.append(check_case('many_remaining_positions', positive+negative,
                           list(range(7)), list(range(7, 16)), 1))
    # Zero residual sum: the original centroid projection is recovered.
    points = [(0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 0, -1),
              (0, 0, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0)]
    row = check_case('centroid_special_case', points, [0, 1], [2, 3], 1)
    require(row['squared_residual_sum'] == '0' and row['residual_energy'] == '2',
            'centroid control')
    rows.append(row)
    rows.append(check_case('coincident_remaining_centers', [(i, 2*i, 1) for i in range(4)]
                           +[(1, 0, 2)]*4, [0, 1, 2, 3], [4, 5, 6, 7], 0))
    return rows


def classical_fixture():
    v = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    x, y = list(v), list(v)
    for i in range(4):
        for j in range(4):
            if i != j:
                x.append(sub(v[j], v[i]))
                y.append(tuple(a+b for a, b in zip(v[j], v[i])))
    return x, y


def contraction_control():
    x, y = classical_fixture()
    deficits = {(i, j): dot(sub(x[i], x[j]), sub(x[i], x[j]))
                - dot(sub(y[i], y[j]), sub(y[i], y[j]))
                for i, j in combinations(range(16), 2)}
    require(min(deficits.values()) == 0 and max(deficits.values()) > 0,
            'classical fixture contraction')
    # t=9/25 gives a rational exact R6 realization at an interior time.
    z = [tuple(F(4, 5)*a for a in xx)+tuple(F(3, 5)*b for b in yy)
         for xx, yy in zip(x, y)]
    block, remaining = [8, 10], [0, 1, 2, 3, 4, 7]
    require(deficits[tuple(sorted(block))] > 0, 'distinguished pair must contract')
    row = check_case('actual_R3_contraction_lift', z, block, remaining, 5)
    require(F(row['squared_residual_sum']) > 0, 'nonzero affine correction required')
    row['distinguished_squared_distance_loss'] = str(deficits[tuple(sorted(block))])
    row['interpolation_time'] = '9/25'
    return row


def partition_coverage():
    """Independent position-level enumeration, not integer partitions."""
    count = nonzero_pairs = automatically_signed = 0
    residual = Counter()
    pairs = list(combinations(range(9), 2))

    def words(prefix, maximum):
        if len(prefix) == 9:
            yield prefix
        else:
            for label in range(maximum+2):
                yield from words(prefix+(label,), max(maximum, label))

    for word in words((0,), 0):
        count += 1
        multiplicities = Counter(word)
        pattern = tuple(sorted(multiplicities.values(), reverse=True))
        for a, b in pairs:
            if word[a] == word[b]:
                continue
            nonzero_pairs += 1
            # Test the actual positions left, independent of count subtraction.
            labels = {word[j] for j in range(9) if j not in (a, b)}
            if len(labels) <= 6:
                automatically_signed += 1
            else:
                require(len(labels) == 7, 'remaining-position count')
                pair_pattern = tuple(sorted((multiplicities[word[a]], multiplicities[word[b]]), reverse=True))
                residual[pattern, pair_pattern] += 1
    expected = {((2, 2, 1, 1, 1, 1, 1), (2, 2)): 1512,
                ((2, 1, 1, 1, 1, 1, 1, 1), (2, 1)): 504,
                ((1,)*9, (1, 1)): 36}
    require(dict(residual) == expected, 'residual coverage differs')
    require(count == 21147 and nonzero_pairs == 612252, 'set-partition enumeration')
    require(automatically_signed+sum(residual.values()) == nonzero_pairs, 'pair coverage')
    return {'position_partitions': count, 'distinct_label_pair_cases': nonzero_pairs,
            'automatically_signed_pair_cases': automatically_signed,
            'residual_pair_cases': sum(residual.values()),
            'residuals': [{'multiplicities': list(a), 'pair_multiplicities': list(b),
                          'position_pair_cases': n} for (a, b), n in sorted(residual.items())]}


def integer_determinant(matrix):
    """Fraction-free elimination, distinct from the reviewed Fraction method."""
    a = [list(row) for row in matrix]
    sign, previous = 1, 1
    for k in range(len(a)-1):
        pivot = next((j for j in range(k, len(a)) if a[j][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k+1, len(a)):
            for j in range(k+1, len(a)):
                value = a[i][j]*p-a[i][k]*a[k][j]
                require(value % previous == 0, 'fraction-free divisibility')
                a[i][j] = value//previous
        for i in range(k+1, len(a)):
            a[i][k] = 0
        previous = p
    return sign*a[-1][-1]


def rank_boundary():
    x, y = classical_fixture()
    labels = [0, 1, 2, 3, 4, 7, 10]
    z = [x[i]+y[i] for i in labels]
    det = integer_determinant([sub(row, z[0]) for row in z[1:]])
    require(det == -512, 'seven-site paired rank')
    loss = [dot(sub(x[i], x[j]), sub(x[i], x[j]))-dot(sub(y[i], y[j]), sub(y[i], y[j]))
            for i, j in combinations(labels, 2)]
    require(min(loss) == 0 and loss[3] == 16, 'boundary pair contraction')
    return {'labels': labels, 'paired_determinant': det,
            'midpoint_determinant': F(det, 8).__str__(),
            'endpoint_pairs': len(loss), 'strict_pairs': sum(v > 0 for v in loss),
            'distinguished_pair': [0, 4], 'distinguished_loss': str(loss[3])}


def compact_strip():
    frontier = 3
    n = 2**16*frontier**8-2
    coefficient = F(1)
    rows = []
    for q in range(7):
        if q:
            coefficient *= F(n-q+1, q)
        require(coefficient.denominator == 1, 'integer binomial recursion')
        j = n-q
        rows.append({'N': n, 'j': j, 'q': q,
                     'mantissa': str(F(n+1, 1024*3**q)*coefficient),
                     'negative_binary_exponent': 2*(j+2)*(18*frontier**2+8*frontier+4)})
    require(n == 429981694, 'compact row degree')
    require(F(1)+F(1, 2)+F(1, 8) > F(3, 2), 'Gaussian-complement bound')
    require(8**5 < 256**2, 'five-dimensional density prefactor')
    require(F(5, 2)+F(1, 6)/(1-F(1, 4)) == F(49, 18) < 4, 'exponential base')
    return {'frontier': frontier, 'entries': rows}


def finite_algebra():
    count = 0
    for n in range(13):
        for k in range(n+1):
            for q in range(k, n+1):
                lhs = F((n+1)*comb(n, k)*comb(n-k, q-k),
                        (q+2)*(q+1)*comb(n+2, q+2))
                require(lhs == F(comb(q, k), n+2), 'polarization factor')
                count += 1
    products = 0
    for r in range(10):
        # Inclusion-exclusion of a formal product has one term per subset.
        factors = [F(i+1, 2*r+3) for i in range(r)]
        for u in [F(0), F(1, 3), F(1)]:
            lhs = sum((-1)**len(c)*product(u*factors[i] for i in c)
                      for q in range(r+1) for c in combinations(range(r), q))
            require(lhs == product(1-u*v for v in factors), 'scaled positive product')
            require(lhs >= 0, 'product range')
            products += 1
    # Exact coefficients of the positive dimension expansion and its
    # geometric tail: no numerical exponential or Gaussian integral.
    tails = 0
    for b, energy, squared_sum in [(2, F(7), F(9)), (3, F(2), F(1)), (7, F(0), F(0))]:
        require(squared_sum <= b*energy, 'series control admissibility')
        z = squared_sum/(2*b)
        q = max(2, z.numerator//z.denominator+1)
        ratio = z/(q+2)
        require(ratio < 1, 'tail ratio')
        upper = z**(q+1)/factorial(q+1)/(1-ratio)
        prefix = sum(z**j/factorial(j) for j in range(q+1, q+21))
        require(0 <= prefix <= upper, 'positive series tail bound')
        for j in range(q+1, q+20):
            require(z/(j+1) <= ratio, 'tail term ratios')
        tails += 1
    return {'polarization_identities': count, 'scaled_product_checks': products,
            'positive_tail_controls': tails}


def product(values):
    result = F(1)
    for v in values:
        result *= v
    return result


def rejected_controls():
    rejected = []
    seven = [(0,)*6]+[tuple(int(i == j) for j in range(6)) for i in range(6)]
    for name, arguments in [
        ('seven_affinely_independent_remaining_centers', ([(2,)*6]+seven, [0], list(range(1, 8)), 5)),
        ('overlapping_positions', ([(0, 0), (1, 1)], [0], [0, 1], 5)),
        ('repeated_position', ([(0, 0), (1, 1)], [0], [1, 1], 5)),
    ]:
        try:
            projection(*arguments)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('bad input was accepted: '+name)
    # Omitting the inverse-cardinality correction is genuinely wrong.
    p = [(0, 0, 2), (0, 0, 1), (0, 0, 0), (1, 0, 0)]
    original, projected, _, energy, squared_sum = projection(p, [0, 1], [2, 3], 5)
    difference = variance(original, [0, 1, 2])-variance(projected, [0, 1, 2])
    require(squared_sum > 0 and difference != energy, 'omitted correction control')
    rejected.append('omitted_inverse_cardinality_correction')
    return rejected


def run():
    cases = generic_controls()+[contraction_control()]
    record = {'status': 'AFFINE_GAUSSIAN_PROJECTION_AUDIT_PASS', 'cases': cases,
              'algebra': finite_algebra(), 'rejected': rejected_controls(),
              'position_level_coverage': partition_coverage(),
              'rank_boundary': rank_boundary(), 'compact_strip': compact_strip(),
              'scope': 'Exact finite identity controls; universal positivity follows from the written proof.'}
    raw = json.dumps(record, sort_keys=True, separators=(',', ':')).encode()
    return {'record': record, 'sha256': sha256(raw).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.check:
        require(rendered == Path(__file__).with_name('EXPECTED.json').read_text(), 'expected output differs')
        print(result['record']['status'])
        print(result['sha256'])
    else:
        print(rendered, end='')
