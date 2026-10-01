#!/usr/bin/env python3
"""six-reviewer-4: independent Q(sqrt(5)) audit; no author code imports.

The ten proposed probes are input data, NOT trusted geometry. Reconstruct
all original points, supports, moments, planar fans and torque polynomials.
Use Cartesian polynomial coordinates before homogenizing; author works
directly with homogeneous Q(phi) polynomials. Python 3.11+ stdlib only.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial
from pathlib import Path
import hashlib
import json


def check(ok, why):
    if not ok:
        raise ValueError(why)


class S:
    """a+b sqrt(5); exact ordering by rational squares."""
    __slots__ = ('a', 'b')

    def __init__(self, a=0, b=0):
        self.a, self.b = F(a), F(b)

    def __add__(self, other):
        other = cast(other)
        return S(self.a+other.a, self.b+other.b)

    __radd__ = __add__

    def __neg__(self):
        return S(-self.a, -self.b)

    def __sub__(self, other):
        return self+-cast(other)

    def __rsub__(self, other):
        return cast(other)+-self

    def __mul__(self, other):
        other = cast(other)
        return S(self.a*other.a+5*self.b*other.b,
                 self.a*other.b+self.b*other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = cast(other)
        denominator = other.a**2-5*other.b**2
        check(denominator != 0, 'zero field divisor')
        return self*S(other.a/denominator, -other.b/denominator)

    def __rtruediv__(self, other):
        return cast(other)/self

    def __pow__(self, n):
        check(isinstance(n, int), 'integer power')
        if n < 0:
            return (1/self)**(-n)
        result = S(1)
        for _ in range(n):
            result = result*self
        return result

    def sign(self):
        if self.b == 0:
            return (self.a > 0)-(self.a < 0)
        if self.a == 0 or self.a*self.b > 0:
            return (self.b > 0)-(self.b < 0)
        value = self.a**2-5*self.b**2
        return ((value > 0)-(value < 0))*((self.a > 0)-(self.a < 0))

    def __eq__(self, other):
        other = cast(other)
        return self.a == other.a and self.b == other.b

    def __lt__(self, other):
        return (self-other).sign() < 0

    def __le__(self, other):
        return (self-other).sign() <= 0

    def __gt__(self, other):
        return (self-other).sign() > 0

    def __ge__(self, other):
        return (self-other).sign() >= 0

    def __hash__(self):
        return hash((self.a, self.b))

    def encoded(self):
        return [str(self.a), str(self.b)]


def cast(x):
    return x if isinstance(x, S) else S(x)


Z, O, PHI = S(), S(1), S(F(1, 2), F(1, 2))
BETA = (19-8*PHI)/29
R2 = 7+8*PHI
DELTA, D = F(1, 108), F(1, 22)


def dot(v, w):
    return sum((a*b for a, b in zip(v, w)), Z)


def sub(v, w):
    return tuple(a-b for a, b in zip(v, w))


def cross(v, w):
    return (v[1]*w[2]-v[2]*w[1], v[2]*w[0]-v[0]*w[2],
            v[0]*w[1]-v[1]*w[0])


def project(v, n):
    return tuple(x-dot(v, n)*y/dot(n, n) for x, y in zip(v, n))


def enc(v):
    return [x.encoded() for x in v]


def vertices():
    result = set()
    for row in [(O, O, PHI**3), (PHI**2, PHI, 2*PHI),
                (2+PHI, Z, PHI**2)]:
        for shift in range(3):
            row2 = row[shift:]+row[:shift]
            for signs in product((-1, 1), repeat=3):
                result.add(tuple(s*x for s, x in zip(signs, row2)))
    check(len(result) == 60 and all(dot(v, v) == R2 for v in result),
          'sixty common-radius original vertices')
    check(all(tuple(-x for x in v) in result for v in result), 'central symmetry')
    return sorted(result)


def radical_upper(x, digits=32):
    """Positive sqrt enclosure by exact field comparisons, fixed dyadic grid."""
    check(x >= 0, 'positive radical branch')
    denominator = 1 << digits
    upper = denominator
    while S(F(upper, denominator)**2) < x:
        upper *= 2
    lower = 0
    while upper-lower > 1:
        middle = (upper+lower)//2
        if S(F(middle, denominator)**2) >= x:
            upper = middle
        else:
            lower = middle
    result = F(upper, denominator)
    check(S(result**2) >= x, 'outward radical upper enclosure')
    return result


def reconstruct_moment(V, n):
    norm = dot(n, n)
    c = min(dot(v, n) for v in V if dot(v, n) > 0)
    active = sorted(v for v in V if dot(v, n) == c)
    check(len(active) == 4 and c*c/norm == BETA, 'threshold active originals')
    a, b = (11+3*PHI)/58, (18-3*PHI)/58
    weights = [a, b, b, a]
    check(min(weights) > 0 and sum(weights, Z) == 1, 'positive probability weights')
    check(tuple(sum((w*v[j] for w, v in zip(weights, active)), Z)
                for j in range(3)) == tuple(c*x/norm for x in n), 'first moment')
    matrix = [[sum((w*v[i]*v[j] for w, v in zip(weights, active)), Z)
               for j in range(3)] for i in range(3)]
    lx, lt = (49+45*PHI)/29, (135+195*PHI)/29
    eigenvectors = [(n, BETA), ((O, Z, Z), lx), ((Z, -n[2], n[1]), lt)]
    for v, value in eigenvectors:
        check(tuple(dot(row, v) for row in matrix) == tuple(value*x for x in v),
              'complete exact eigenbasis')
    check(sum((matrix[i][i] for i in range(3)), Z) == R2, 'moment trace')
    check(0 < BETA < lx < lt, 'positive ordered moment spectrum')
    check((F(19, 5)**2)*(BETA+lx) > 4*lt, 'full-angle coefficient')
    return {'originals': [enc(v) for v in active],
            'weights': enc(weights), 'matrix': [enc(row) for row in matrix],
            'spectrum': enc([BETA, lx, lt])}


def planar_fan(V, n):
    """All supporting directions from every projected pair; no author fan input."""
    shadows = sorted(set(project(v, n) for v in V))
    facets = {}
    for v, w in combinations(shadows, 2):
        mu = cross(n, sub(w, v))
        if dot(mu, mu) == 0:
            continue
        gaps = [dot(mu, sub(x, v)) for x in shadows]
        if max(gaps) <= 0:
            pass
        elif min(gaps) >= 0:
            mu = tuple(-x for x in mu)
        else:
            continue
        height = dot(mu, v)
        check(height > 0, 'origin inside shadow')
        key = tuple(x/height for x in mu)
        facets[key] = key
    check(len(facets) == 16, 'complete sixteen-facet reference fan')
    tied_heights, rows = [], []
    for mu in sorted(facets):
        mu2 = dot(mu, mu)
        for v in V:
            gap = 1-dot(mu, v)
            height2 = dot(v, n)**2/dot(n, n)
            height = radical_upper(height2)
            check(gap >= 0, 'reference support')
            needed = max(F(0), height-F(13, 10))*DELTA
            # Avoid division and a field enclosure: square this positive comparison.
            if gap == 0:
                check(height <= F(13, 10), 'full original tied height')
                tied_heights.append(height2)
            else:
                check(gap*gap > S(needed**2)*mu2, 'gap-aware whole receiving envelope')
            rows.append([enc(mu), enc(v), gap.encoded(), str(height), str(needed)])
    check(max(tied_heights) == (119+72*PHI)/145, 'sharp tied height')
    return {'facets': len(facets), 'comparisons': len(rows),
            'max_tied_height_squared': max(tied_heights).encoded(),
            'record_sha256': digest(rows)}


def threshold_contacts(V, n, index):
    """Find all original circle-endpoint/edge supports without a contact input."""
    c = min(abs_field(dot(v, n)) for v in V)
    circle = [v for v in V if abs_field(dot(v, n)) == c]
    check(len(circle) == 8, 'eight original circle preimages')
    probes = set()
    for v in circle:
        for w in V:
            e = sub(w, v)
            if dot(e, e) != 4:
                continue
            for sign in (-1, 1):
                edge = tuple(sign*x for x in e)
                mu = cross(edge, n)
                if dot(mu, mu) > 0 and all(dot(mu, sub(v, q)) >= 0 for q in V):
                    probes.add((v, edge))
    check(len(probes) == 16, 'all sixteen original circle contacts')
    ratios, zero = [], 0
    for v, e in sorted(probes):
        for w in V:
            a = cross(sub(v, w), e)
            g = dot(n, a)
            if g == 0:
                check(dot(a, a) == 0, 'identical vector tie persists at all normals')
                zero += 1
            else:
                check(g > 0 and g*g > S(DELTA**2)*dot(n, n)*dot(a, a),
                      'all original selected supports persist over the CLOSED cap')
                ratios.append(g*g/(dot(n, n)*dot(a, a)))
    minima = [(33-20*PHI)/145, (311-192*PHI)/435]
    check(zero == 32 and len(ratios) == 928 and min(ratios) == minima[index],
          'complete support stability and sharp gap ratio')
    T = sorted(set(cross(v, cross(e, n)) for v, e in probes))
    check(len(T) == 8, 'complete eight raw torques')
    distances, facets = [], set()
    for a, b, c0 in combinations(T, 3):
        normal = cross(sub(b, a), sub(c0, a))
        if dot(normal, normal) == 0:
            continue
        h = dot(normal, a)
        gaps = [dot(normal, p)-h for p in T]
        if max(gaps) <= 0 or min(gaps) >= 0:
            check(h > 0 if max(gaps) <= 0 else h < 0, 'threshold hull contains origin')
            facets.add(tuple(x/h for x in normal))
            distances.append(h*h/dot(normal, normal))
    check(len(facets) == 12, 'all threshold torque facets')
    check(min(distances) == [(1328+304*PHI)/14589,
                            (9692+15056*PHI)/164681][index], 'sharp threshold raw ball')
    stress = False
    for p in combinations(T, 4):
        cof = [(-1)**i*dot(p[j[0]], cross(p[j[1]], p[j[2]]))
               for i in range(4) for j in [[k for k in range(4) if k != i]]]
        if min(cof) > 0 or max(cof) < 0:
            check(all(sum((cof[i]*p[i][j] for i in range(4)), Z) == 0
                      for j in range(3)), 'threshold positive interior stress')
            stress = True
            break
    check(stress, 'threshold three-dimensional origin interiority')
    rho, ray = [(F(7, 20), F(51, 50)), (F(9, 20), F(11, 10))][index]
    check(min(distances) > S(rho*rho) and dot(n, n) < S(ray*ray),
          'strict raw-radius and ray-norm bounds')
    moving_ball = rho/(ray*F(9, 2))-2*DELTA
    check(moving_ball == [F(53, 918), F(43, 594)][index] and
          moving_ball > F(1, 20), 'moving normalized torque ball')
    # Complete original-circle separation is sufficient for radial injection.
    projections = [project(v, n) for v in circle]
    check(min(dot(sub(a, b), sub(a, b)) for a, b in combinations(projections, 2)) > F(9, 4),
          'every original source circle pair separated by more than 3/2')
    return {'circle_originals': len(circle), 'contacts': len(probes),
            'identical_vector_ties': zero, 'positive_comparisons': len(ratios),
            'minimum_support_ratio': min(ratios).encoded(),
            'torque_points': len(T), 'facets': len(facets),
            'raw_ball_squared': min(distances).encoded(),
            'moving_normalized_ball_lower': str(moving_ball)}


# Cartesian power polynomials in x,y. They are homogenized only at the end.
def padd(p, q):
    r = dict(p)
    for ij, value in q.items():
        r[ij] = r.get(ij, Z)+value
    return {ij: value for ij, value in r.items() if value != 0}


def pscale(p, scale):
    return {ij: value*scale for ij, value in p.items() if value*scale != 0}


def pmul(p, q):
    r = {}
    for (i, j), a in p.items():
        for (k, l), b in q.items():
            ij = (i+k, j+l)
            r[ij] = r.get(ij, Z)+a*b
    return {ij: value for ij, value in r.items() if value != 0}


def pdot(v, w):
    return sum_poly(pmul(a, b) for a, b in zip(v, w))


def sum_poly(polys):
    result = {}
    for p in polys:
        result = padd(result, p)
    return result


def psub(v, w):
    return tuple(padd(a, pscale(b, -1)) for a, b in zip(v, w))


def pcross(v, w):
    return tuple(padd(pmul(v[i], w[j]), pscale(pmul(v[j], w[i]), -1))
                 for i, j in ((1, 2), (2, 0), (0, 1)))


def homogenize(p, degree):
    r = {}
    for (i, j), value in p.items():
        power = degree-i-j
        check(power >= 0, 'Cartesian polynomial degree')
        for a in range(power+1):
            for b in range(power-a+1):
                c = power-a-b
                exponent = (a, b+i, c+j)
                coefficient = factorial(power)//(factorial(a)*factorial(b)*factorial(c))
                r[exponent] = r.get(exponent, Z)+coefficient*value
    return {ijk: v for ijk, v in r.items() if v != 0}


def restrictions(p, face):
    return [v for ijk, v in p.items() if all(ijk[i] == 0 for i in range(3) if i not in face)]


def strict_sign(p, face):
    values = restrictions(p, face)
    if values and min(values) > 0:
        return 1
    if values and max(values) < 0:
        return -1
    return 0


def peval(p, x, y):
    return sum((v*S(x)**i*S(y)**j for (i, j), v in p.items()), Z)


def torque_triangle(V, probes):
    A, B = (Z, Z, O), (Z, PHI**-2, O)
    DD = (1/(PHI*(PHI+2)), 1/(PHI+2), O)
    q = F(89, 200)
    s, t = (PHI-1-q)/PHI, (PHI-1-q)/(PHI-1)
    U = [B, tuple((1-s)*b+s*a for a, b in zip(A, B)),
         tuple((1-t)*b+t*d for b, d in zip(B, DD))]
    check(dot(cross(sub(U[1], B), sub(U[2], B)),
              cross(sub(U[1], B), sub(U[2], B))) > 0, 'nondegenerate cut triangle')
    supports = 0
    for u in U:
        check(dot(u, u) < S(F(27, 25)**2) and
              dot(sub(u, B), sub(u, B)) < S(F(1, 16)**2), 'whole triangle outer bounds')
        for v, e in probes:
            normal = cross(e, u)
            for w in V:
                check(dot(normal, sub(v, w)) >= 0, 'actual original support')
                supports += 1
    torques = []
    for v, e in probes:
        check(v in V and dot(e, e) == 4 and
              (tuple(a+b for a, b in zip(v, e)) in V or sub(v, e) in V), 'actual edge/endpoint')
        values = [cross(v, cross(e, u)) for u in U]
        torques.append(tuple({(0, 0): values[0][j], (1, 0): values[1][j]-values[0][j],
                              (0, 1): values[2][j]-values[0][j]} for j in range(3)))
    # Direct exhaustive center-facet ball certificate, not a supplied facet list.
    center = [tuple(peval(p, 0, 0) for p in T) for T in torques]
    center_facets = set()
    for a, b, c in combinations(center, 3):
        normal = cross(sub(b, a), sub(c, a))
        h = dot(normal, a)
        check(dot(normal, normal) > 0, 'nondegenerate center triple')
        gaps = [dot(normal, p)-h for p in center]
        if max(gaps) <= 0 or min(gaps) >= 0:
            check(h > 0 if max(gaps) <= 0 else h < 0, 'origin inside center hull')
            check(h*h >= (2-PHI)*dot(normal, normal), 'center ball phi-1')
            center_facets.add(tuple(x/h for x in normal))
    check(len(center_facets) == 15 and (PHI, Z, Z) in center_facets, 'complete sharp center ball')
    # A positive tetrahedral stress independently ensures origin interiority.
    stress = None
    for ids in combinations(range(10), 4):
        points = [center[i] for i in ids]
        cof = [(-1)**i*dot(points[j[0]], cross(points[j[1]], points[j[2]]))
               for i in range(4) for j in [[k for k in range(4) if k != i]]]
        if min(cof) > 0 or max(cof) < 0:
            check(all(sum((cof[i]*points[i][j] for i in range(4)), Z) == 0
                      for j in range(3)), 'interior tetrahedron balance')
            stress = ids
            break
    check(stress is not None and PHI-1 > F(3, 5), 'uniform origin interiority by perturbation')
    faces = [f for size in (1, 2, 3) for f in combinations(range(3), size)]
    counts = {'opposite': 0, 'distance': 0, 'degenerate': 0}
    records = []
    polynomial_records = []
    author_basis_hash = hashlib.sha256()
    for ids in combinations(range(10), 3):
        a, b, c = [torques[i] for i in ids]
        normal = pcross(psub(b, a), psub(c, a))
        h = pdot(normal, a)
        gaps = [padd(pdot(normal, v), pscale(h, -1)) for v in torques]
        distance = padd(pmul(h, h), pscale(pdot(normal, normal), -F(1, 4)))
        ng = [homogenize(p, 2) for p in normal]
        hg = homogenize(h, 3)
        gg = [homogenize(p, 3) for p in gaps]
        dg = homogenize(distance, 6)
        # Compare ALL newly reconstructed coefficients in the author's basis,
        # without calling any author arithmetic or importing its certificate.
        for p in [*ng, hg, *gg, dg]:
            encoded = [[list(k), [str(v.a-v.b), str(2*v.b)]] for k, v in sorted(p.items())]
            author_basis_hash.update(json.dumps(encoded, separators=(',', ':')).encode())
        polynomial_records.append([list(ids), [[[list(k), v.encoded()] for k, v in sorted(p.items())]
                                               for p in [*ng, *gg, dg]]])
        for face in faces:
            signs = [strict_sign(p, face) for p in gg]
            if 1 in signs and -1 in signs:
                kind = 'opposite'
            elif all(not restrictions(p, face) for p in ng):
                kind = 'degenerate'
            else:
                check(all(v >= 0 for v in restrictions(dg, face)),
                      'full facet distance on relative simplex face')
                kind = 'distance'
            counts[kind] += 1
            records.append([list(ids), list(face), kind])
    check(counts == {'opposite': 726, 'distance': 114, 'degenerate': 0}, 'all new 840 strata')
    check(author_basis_hash.hexdigest() ==
          '174c32f42dd40d77a0acd6b6ef260cf8f3645f8cc434b806e518df6e4d99906e',
          'entry-level agreement of every reconstructed new coefficient')
    return {'corners': [enc(u) for u in U], 'support_comparisons': supports,
            'center_facets': len(center_facets), 'positive_tetrahedron': list(stress),
            'all_triples': 120, 'relative_faces': [list(f) for f in faces],
            'classifications': counts, 'strata': len(records),
            'all_coefficients_in_author_basis_sha256': author_basis_hash.hexdigest(),
            'strata_sha256': digest(records), 'cartesian_polynomial_sha256': digest(polynomial_records)}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def decode_phi(v):
    return tuple(S(F(a)+F(b)/2, F(b)/2) for a, b in v)


def main():
    V = vertices()
    refs = [(Z, (2-PHI)/3, -O), (Z, O, (3*PHI-1)/11)]
    moments = [reconstruct_moment(V, n) for n in refs]
    envelopes = [planar_fan(V, n) for n in refs]
    contacts = [threshold_contacts(V, n, i) for i, n in enumerate(refs)]
    B = (Z, PHI**-2, O)
    height = min(dot(v, B) for v in V if dot(v, B) > 0)
    active = sorted(v for v in V if dot(v, B) == height)
    check(len(active) == 6 and height*height/dot(B, B) == F(1, 3), 'winning six originals')
    pairs = [(0, 5), (1, 3), (2, 4)]
    pair_rows = []
    for i, j in pairs:
        mean = tuple((a+b)/2 for a, b in zip(project(active[i], B), project(active[j], B)))
        check(dot(mean, mean) == F(5, 3), 'winning tangent pair mean')
        pair_rows.append({'indices': [i, j], 'mean': enc(mean)})
    nonactive = [dot(v, B)**2/dot(B, B) for v in V
                 if abs_field(dot(v, B)) != height]
    check(len(nonactive) == 48 and min(nonactive) == F(5, 3), 'all other winning originals')
    check(F(577, 1000)*F(499, 500)-F(3, 2)*D > F(1, 2), 'three pair means above candidate cutoff')
    check(F(5, 4)-F(9, 2)*D > 1, 'nonactive candidate exclusion')
    data = json.loads(Path(__file__).with_name('PROBES.json').read_text())
    probes = [(decode_phi(row['vertex']), decode_phi(row['edge'])) for row in data]
    check(len(probes) == len(set(probes)) == 10, 'ten proposed probe inputs')
    triangle = torque_triangle(V, probes)
    eta = F(23, 50)*DELTA+F(9, 4)*DELTA**2
    aW = F(13433, 300000)
    etaW = F(289, 500)*aW+F(9, 4)*aW*aW
    etaT = F(13, 10)*DELTA+F(9, 4)*DELTA**2
    E = (F(13, 15)*D+F(3, 2)*D**2+F(17, 16)*D**2)/(1-D**2/4)
    margin = F(1, 2)-F(9, 2)*F(27, 25)*F(64, 625)
    check(eta == F(577, 129600) and F(1, 100)+9*eta < F(9, 40)**2, 'radial candidate loss')
    check(F(1, 16)-etaW-etaT > F(1, 60), 'winning-to-threshold support margin')
    check(E == F(5191, 116100) and E < F(77, 1000), 'reduced roll error')
    check(F(101, 100)**2*((2*D)**2+E**2) < F(64, 625)**2, 'full winning spatial angle')
    check(margin == F(73, 31250) and margin > F(1, 500), 'winning rotation remainder margin')
    witnesses = [(Z, S(F(87, 250)), O), (S(F(7, 250)), O, -3-3*PHI)]
    witness_values = []
    for u in witnesses:
        value = min(dot(v, u)**2/dot(u, u) for v in V)
        check(BETA-F(1, 100) <= value < BETA-F(1, 150), 'strictly newly excluded band')
        witness_values.append(value.encoded())
    # Distinguish field and polynomial rejection checks from theorem premises.
    check((S(2)-S(0, 1)).sign() == -1 and (S(9)-S(0, 4)).sign() == 1, 'field adversarial signs')
    check(radical_upper(S(F(1, 4))) == F(1, 2), 'exact positive square root boundary')
    return {'agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'coefficient_field': 'Q(sqrt(5)), exact rational square signs',
            'vertex_count': len(V), 'moments': moments, 'receiving_envelopes': envelopes,
            'threshold_contacts': contacts,
            'winning_pairs': pair_rows, 'nonactive_winning_originals': len(nonactive),
            'triangle': triangle, 'source_support_margin': str(F(1, 16)-etaW-etaT),
            'winning_roll_error': str(E), 'winning_remainder_margin': str(margin),
            'new_band_squared_heights': witness_values,
            'author_code_imports': False, 'inherited_436_regions_rerun': False,
            'inherited_full_roll_cover_rerun_independently': False,
            'continuum_proof_in': 'REVIEW.md'}


def abs_field(x):
    return -x if x < 0 else x


if __name__ == '__main__':
    expected = Path(__file__).with_name('EXPECTED.json')
    check(expected.is_file(), 'required compact expected output is missing')
    result = main()
    canonical = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
    check(expected.read_bytes() == canonical, 'complete compact expected output')
    print(canonical.decode(), end='')
