"""exact R-isotropic cap dual; no solver status is a proof."""
from fractions import Fraction as F
from math import lcm, gcd
from functools import reduce
from pathlib import Path
import json
import orbits
from literal import require


def quadratic(matrix, vector):
    return sum(vector[i]*matrix[i][j]*vector[j] for i in range(len(vector))
               for j in range(len(vector)))


def congruence(matrix, columns):
    return [[sum(columns[i][a]*matrix[a][b]*columns[j][b]
                 for a in range(len(matrix)) if columns[i][a]
                 for b in range(len(matrix)) if columns[j][b])
             for j in range(len(columns))] for i in range(len(columns))]


def negative_vector(matrix):
    """Return an explicit exact negative direction or None if exact PSD."""
    n = len(matrix)
    A = [list(map(F, row)) for row in matrix]
    columns = [[F(i == j) for i in range(n)] for j in range(n)]
    for k in range(n):
        p = A[k][k]
        if p < 0:
            result = columns[k]
            require(quadratic(matrix, result) == p < 0, 'exact original negative pivot certificate')
            return result
        if not p:
            for j in range(k+1, n):
                if A[k][j]:
                    a = -A[k][j]/(abs(A[j][j])+1)
                    result = [x+a*y for x, y in zip(columns[k], columns[j])]
                    require(quadratic(matrix, result) < 0, 'zero-pivot original negative direction')
                    return result
            continue
        factors = {j: A[k][j]/p for j in range(k+1, n)}
        for i in range(k+1, n):
            for j in range(i, n):
                A[i][j] -= A[k][i]*factors[j]
                A[j][i] = A[i][j]
        for j in range(k+1, n):
            columns[j] = [x-factors[j]*y for x, y in zip(columns[j], columns[k])]
    return None


def integer(vector):
    den = lcm(*(x.denominator for x in vector))
    out = [int(x*den) for x in vector]
    divisor = reduce(gcd, out)
    return [x//divisor for x in out]


def probe(q, k):
    data = orbits.forms(q, k)
    index = {key: i for i, key in enumerate(data['keys'])}
    tied = [index[(c, 0, 0)] for c in (1, 3, 5)]
    # Original amplitudes at a,ab,ac are identical, hence w'Rw=0
    # for EVERY vector in this entire 21-dimensional linear space.
    cols = [[F(i in tied) for i in range(23)]]
    cols += [[F(i == j) for i in range(23)] for j in range(23) if j not in tied]
    A = congruence(data['U0'], cols)
    require(not any(x for row in congruence(data['R'], cols) for x in row), 'entire R-isotropic subspace')
    direction = negative_vector(A)
    if direction is None:
        return {'q': q, 'k': k, 'status': 'NO negative dual in tested exact 21-space; ansatz undecided'}
    original = [sum(direction[j]*cols[j][i] for j in range(21)) for i in range(23)]
    pairs = [quadratic(data[x], original) for x in ('U0', 'Delta', 'R')]
    require(pairs[0] < 0 and pairs[2] == 0, 'original negative cap and repair-annihilating pairing')
    scale = max(original, key=abs)
    original = [x/scale for x in original]
    compact = None
    for den in (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096):
        candidate = [F(round(x*den), den) for x in original]
        got = [quadratic(data[x], candidate) for x in ('U0', 'Delta', 'R')]
        if got[0] < 0 and got[1] >= 0 and got[2] == 0:
            compact = integer(candidate)
            break
    vector = compact if compact is not None else original
    final = [quadratic(data[x], vector) for x in ('U0', 'Delta', 'R')]
    require(final[0] < 0 and final[1] >= 0 and final[2] == 0, 'exact original all-kappa>=0 dual certificate')
    return {'agent': 'six-downset-3', 'role': 'researcher', 'q': q, 'k': k,
            'status': 'exact all-real-parameter ansatz exclusion with credited9434 kappa orientation',
            'keys': data['keys'], 'sizes': data['sizes'], 'vector': [str(x) for x in vector],
            'original_U0': str(final[0]), 'original_Delta': str(final[1]), 'original_R': str(final[2]),
            'compact_rounding_accepted_only_after_exact_pairings': compact is not None,
            'whole_real_parameter_bridge': 'lower9434 kernel forces kappa>=0; upper pairing=U0-kappa*Delta-t*R<0',
            'trust_boundary': 'calibrated counted forms and ordinary original dual bridge, unformalized, independently unreviewed'}


if __name__ == '__main__':
    result = probe(74, 15)
    Path(__file__).with_name('K15-DUAL.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True, indent=2))
