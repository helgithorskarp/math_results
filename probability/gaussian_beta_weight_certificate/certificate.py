"""Rational beta-row certificate on a squared-distance cell, at variance one.

Only seven *distinct* labels need enclosure: PROOF.md signs every coefficient
with at most six distinct labels analytically. No weight mesh is used.
"""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
from math import comb, lcm
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
BOUNDS_SHA256 = '60ff5166c623797055f37442d5532b1a29c06275b8871fa4fdf34dcd12f54fc7'
FIXTURE_SHA256 = '2edec28b8738cb0713c0ba70e4e8ec80147857503fbe2d801b43dbef4861ac08'
N, M, DIGITS = 5, 7, 30
MARGINS = tuple(map(F, ('1/100', '1/500', '1/3000', '1/50000',
                        '1/1500000', '1/125000000')))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pinned(path, digest):
    data = path.read_bytes()
    require(sha256(data).hexdigest() == digest, 'changed dependency: ' + path.name)
    return data


boundfile = BASE / 'gaussian_majorisation_hankel_transport/bounds.py'
pinned(boundfile, BOUNDS_SHA256)
spec = spec_from_file_location('beta_weight_bounds', boundfile)
bounds = module_from_spec(spec)
sys.modules[spec.name] = bounds
spec.loader.exec_module(bounds)
I, exp_negative, sqrt_integer = bounds.I, bounds.exp_negative, bounds.sqrt_integer


def geometry():
    """Reconstruct the ordered classical fixture, then check its pinned bytes."""
    vertices = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    x, y = list(vertices), list(vertices)
    labels = ['anchor_' + str(i) for i in range(4)]
    for i in range(4):
        for j in range(4):
            if i != j:
                x.append(tuple(b-a for a, b in zip(vertices[i], vertices[j])))
                y.append(tuple(b+a for a, b in zip(vertices[i], vertices[j])))
                labels.append('flap_' + str(i) + '_' + str(j))
    data = json.loads(pinned(BASE / 'gaussian_majorisation_rank_abel/flap_fixture.json',
                             FIXTURE_SHA256))
    require(x == list(map(tuple, data['input'])), 'source fixture mismatch')
    require(y == list(map(tuple, data['output'])), 'target fixture mismatch')
    require(labels == data['labels'], 'label ordering mismatch')
    return x, y


def distance_matrix(points):
    return tuple(tuple(sum((a-b)**2 for a, b in zip(u, v))
                       for v in points) for u in points)


def distance_sum(points, row):
    """Independent centroid formula, used to audit every enumerated subset."""
    return len(row)*sum(sum(a*a for a in points[i]) for i in row) - sum(
        sum(points[i][j] for i in row)**2 for j in range(3))


class Cell:
    """Enclose kernels for all Euclidean contractions in a metric box.

    Each source/target squared distance differs from the supplied centre by
    at most eta. Actual pairs MUST be contractions in R3; this class checks
    the centre, not an arbitrary caller's perturbed geometry. Variance is 1.
    """
    def __init__(self, x, y, eta, digits=DIGITS):
        self.x = tuple(tuple(F(a) for a in p) for p in x)
        self.y = tuple(tuple(F(a) for a in p) for p in y)
        require(len(x) == len(y) and len(x) >= M, 'need equally many, >=7 labels')
        require(all(len(p) == 3 for p in self.x + self.y), 'dimension must be 3')
        self.eta, self.digits = F(eta), digits
        require(self.eta >= 0, 'negative cell radius')
        require(type(digits) is int and 10 <= digits <= 100, 'invalid precision')
        self.scale = 10**digits
        self.dx, self.dy = distance_matrix(self.x), distance_matrix(self.y)
        require(all(self.dx[i][j] >= self.dy[i][j] for i, j in combinations(range(len(x)), 2)),
                'centre is not a contraction')
        self.kernel = lru_cache(None)(self._kernel)
        self.row = lru_cache(None)(self._row)

    def _kernel(self, m, sy, sx):
        if self.eta == 0 and sy == sx:
            return 0, 0
        e = comb(m, 2)*self.eta
        yl, yh = max(F(0), sy-e)/(2*m), (sy+e)/(2*m)
        xl, xh = max(F(0), sx-e)/(2*m), (sx+e)/(2*m)
        digits = self.digits + 10
        raw = I(max(F(0), exp_negative(-yh, digits).lo - exp_negative(-xl, digits).hi),
                max(F(0), exp_negative(-yl, digits).hi - exp_negative(-xh, digits).lo))
        enclosed = (raw/(m*sqrt_integer(m, digits))).rounded(self.digits)
        lo, hi = enclosed.lo*self.scale, enclosed.hi*self.scale
        require(lo.denominator == hi.denominator == 1, 'fixed-point conversion')
        return lo.numerator, hi.numerator

    def _row(self, row):
        sy = sum(self.dy[i][j] for i, j in combinations(row, 2))
        sx = sum(self.dx[i][j] for i, j in combinations(row, 2))
        require(sx == distance_sum(self.x, row), 'source exponent disagreement')
        require(sy == distance_sum(self.y, row), 'target exponent disagreement')
        return self.kernel(len(row), sy, sx)


DENOM = lcm(*(m*(m-1)*comb(M, m) for m in range(2, M+1)))


def factors(k):
    result = []
    for m in range(k+2, M+1):
        denominator = m*(m-1)*comb(M, m)
        require(DENOM % denominator == 0, 'nonintegral coefficient multiplier')
        factor = ((N+1)*comb(N, k)*(-1)**(m-k-2)*comb(N-k, m-k-2)
                  * (DENOM//denominator))
        result.append((m, factor))
    return result


def coefficient_bounds(cell, alpha):
    """All six coefficients, numerator intervals over DENOM*cell.scale."""
    require(len(alpha) == M, 'wrong tuple size')
    sums = {m: [0, 0] for m in range(2, M+1)}
    for m in range(2, M+1):
        for row in combinations(alpha, m):
            lo, hi = cell.row(row)
            sums[m][0] += lo
            sums[m][1] += hi
    result = []
    for k in range(N+1):
        lo = sum(f*sums[m][0 if f >= 0 else 1] for m, f in factors(k))
        hi = sum(f*sums[m][1 if f >= 0 else 0] for m, f in factors(k))
        require(lo <= hi, 'reversed coefficient enclosure')
        result.append((lo, hi))
    return result


def run_certificate():
    x, y = geometry()
    cell = Cell(x, y, F(1, 100))
    minimum, minimizers = [None]*(N+1), [None]*(N+1)
    digest, count = sha256(), 0
    denominator = DENOM*cell.scale
    for alpha in combinations(range(len(x)), M):
        enclosed = coefficient_bounds(cell, alpha)
        for k, (lo, hi) in enumerate(enclosed):
            require(F(lo, denominator) > MARGINS[k], 'cell not certified: ' + str((alpha, k)))
            if minimum[k] is None or lo < minimum[k]:
                minimum[k], minimizers[k] = lo, alpha
        digest.update((json.dumps([alpha, enclosed], separators=(',', ':')) + '\n').encode())
        count += 1
    require(count == comb(len(x), M), 'incomplete seven-distinct enumeration')
    subset_count = sum(comb(len(x), m) for m in range(2, M+1))
    require(cell.row.cache_info().misses == subset_count, 'incomplete subset coverage')
    strict_pairs = sum(cell.dx[i][j] > cell.dy[i][j] for i, j in combinations(range(len(x)), 2))
    require(max(cell.dx[0]) + cell.eta < 36 and max(cell.dy[0]) + cell.eta < 36,
            'not in the claimed anchored radius-six cell')
    require(min(cell.dx[i][j] for i, j in combinations(range(len(x)), 2)) > cell.eta,
            'source labels might collide')
    return {
        'claim': 'beta row N=5, all prior weights, contraction-restricted squared-distance cell',
        'variance': '1', 'squared_distance_radius': '1/100', 'labels': len(x),
        'decimal_digits': cell.digits, 'coefficient_denominator': denominator,
        'all_weight_coefficients_per_test': comb(len(x)+M-1, M),
        'analytically_pruned_per_test': comb(len(x)+M-1, M)-count,
        'distinct_coefficients_per_test': count, 'enclosed_signs': (N+1)*count,
        'distinct_subset_checks': subset_count, 'distinct_kernel_enclosures': cell.kernel.cache_info().misses,
        'strict_pairs_at_centre': strict_pairs,
        'proved_coefficient_margins': list(map(str, MARGINS)),
        'minimum_lower_bounds': [str(F(a, denominator)) for a in minimum],
        'lexicographically_first_minimizers': list(map(list, minimizers)),
        'coefficient_stream_sha256': digest.hexdigest(),
        'bounds_sha256': BOUNDS_SHA256, 'fixture_sha256': FIXTURE_SHA256,
    }


if __name__ == '__main__':
    print(json.dumps(run_certificate(), indent=2, sort_keys=True))
