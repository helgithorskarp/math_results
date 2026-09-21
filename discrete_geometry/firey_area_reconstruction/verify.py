"""Bounded exact checks for PROOF.md. Run from any working directory."""
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, factorial
from pathlib import Path
from random import Random

from reconstruct import decode, evaluate, gram, moments, multiply, require, rref


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def hull(points):
    points = sorted(set(tuple(map(F, p)) for p in points))
    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and cross(tuple(out[-1][i]-out[-2][i] for i in [0, 1]),
                                          tuple(p[i]-out[-1][i] for i in [0, 1])) <= 0:
                out.pop()
            out.append(p)
        return out
    return tuple(half(points)[:-1]+half(points[::-1])[:-1])


def atoms(vertices):
    out = []
    for a, b in zip(vertices, vertices[1:]+vertices[:1]):
        n = (b[1]-a[1], a[0]-b[0])
        c = sum(n[i]*a[i] for i in [0, 1])
        require(c > 0, 'origin not strictly interior or orientation incorrect')
        out.append((tuple(x/c for x in n), c))
    require(sum(c for _, c in out) == sum(cross(a, b) for a, b in
                    zip(vertices, vertices[1:]+vertices[:1])), 'cone-area mass mismatch')
    return out


def jet_from_vertices(vertices, maximum):
    data = atoms(vertices)
    jet = {0: [sum(c for _, c in data)]}
    # Polynomial multiplication, not the decoder's binomial extraction.
    for d in range(2, maximum+1, 2):
        result = [F(0)]*(d+1)
        for u, c in data:
            power = [F(1)]
            for _ in range(d):
                power = multiply(power, [u[1], u[0]])
            scale = c*F((-1)**(d//2-1), d-1)
            result = [a+scale*b for a, b in zip(result, power)]
        jet[d] = result
    return jet


def halfplane_vertices(polar):
    """Direct intersections; independent of the producer's convex-hull routine."""
    points = set()
    for u, v in combinations(polar, 2):
        det = cross(u, v)
        if det:
            x = ((v[1]-u[1])/det, (u[0]-v[0])/det)
            if all(sum(a*b for a, b in zip(x, w)) <= 1 for w in polar):
                points.add(x)
    return points


def transform(poly, matrix):
    a, b, c, d = map(F, matrix)
    return hull((a*x+b*y, c*x+d*y) for x, y in poly)


def substitute(form, matrix):
    """P(T x), using independent binomial products per monomial."""
    a, b, c, d = map(F, matrix)
    n = len(form)-1
    result = [F(0)]*(n+1)
    for j, q in enumerate(form):
        for i in range(j+1):
            left = comb(j, i)*a**i*b**(j-i)
            for k in range(n-j+1):
                right = comb(n-j, k)*c**k*d**(n-j-k)
                result[i+k] += q*left*right
    return result


def positive_definite(matrix):
    a = [row[:] for row in matrix]
    for i in range(len(a)):
        if a[i][i] <= 0:
            return False
        for j in range(i+1, len(a)):
            for k in range(i+1, len(a)):
                a[j][k] -= a[j][i]*a[i][k]/a[i][i]
    return True


def expected_failure(fn):
    try:
        fn()
    except ValueError:
        return
    raise RuntimeError('negative control was accepted')


def ellipse_jet(matrix, maximum):
    # F_(T disk)/pi = 2 |det T| sqrt(1+|T^-1 x|^2), independently of (3).
    a, b, c, d = map(F, matrix)
    det = a*d-b*c
    q = [(a*a+b*b)/det**2, -2*(a*c+b*d)/det**2,
         (c*c+d*d)/det**2]
    jet, power, coefficient = {0: [2*abs(det)]}, [F(1)], F(1)
    for m in range(1, maximum//2+1):
        coefficient *= (F(1, 2)-(m-1))/m
        power = multiply(power, q)
        jet[2*m] = [2*abs(det)*coefficient*x for x in power]
    return jet


def main():
    digest = hashlib.sha256()
    counts = {'polygons': 0, 'decoded_facets': 0, 'gram_ranks': 0,
              'affine_coefficient_checks': 0, 'kernel_atom_checks': 0,
              'ellipse_positive_grams': 0, 'disk_moments': 0,
              'sharpness_fourier_checks': 0, 'negative_controls': 0}
    matrices = [(1, 0, 0, 1), (1, 2, 0, 1), (2, -1, 1, 1),
                (F(3, 5), F(-4, 5), F(4, 5), F(3, 5)), (-1, 0, 0, 2)]
    bases = []
    for r in range(2, 8):
        generators = [(0, 1)]+[(1, t) for t in range(r-1)]
        bases.append(hull(tuple(sum(s*g[i] for s, g in zip(signs, generators))
                                for i in [0, 1])
                          for signs in product([-1, 1], repeat=r)))
    rng = Random(440921)
    for _ in range(12):
        points = [(rng.randint(-7, 7), rng.randint(-7, 7)) for _ in range(8)]
        points += [(-x, -y) for x, y in points]
        bases.append(hull(points))
    facet_counts, infinity_cases = set(), 0
    for base in bases:
        r = len(base)//2
        require(len(base) >= 4 and set(base) == {(-x, -y) for x, y in base},
                'invalid centrally symmetric fixture')
        base_jet = jet_from_vertices(base, 2*r+2)
        for matrix in matrices:
            poly = transform(base, matrix)
            jet = jet_from_vertices(poly, 2*r+2)
            supplied = {d: value for d, value in jet.items() if d <= 2*r}
            found, polar, kernel = decode(supplied)
            require(found == r and len(polar) == 2*r, 'wrong facet count')
            require(set(polar) == {u for u, _ in atoms(poly)}, 'wrong polar endpoints')
            require(halfplane_vertices(polar) == set(poly), 'halfplane reconstruction failed')
            infinity_cases += int(any(u[1] == 0 for u in polar))
            for u, _ in atoms(poly):
                require(evaluate(kernel, u) == 0, 'kernel missed an atom')
                counts['kernel_atom_checks'] += 1
            for k in range(1, r+2):
                g = gram(jet, k)
                require(len(rref(g)[1]) == min(k+1, r), 'wrong Gram rank')
                if k < r:
                    require(positive_definite(g), 'earlier Gram not positive definite')
                counts['gram_ranks'] += 1
            det = abs(F(matrix[0])*matrix[3]-F(matrix[1])*matrix[2])
            for d in jet:
                require(substitute(jet[d], matrix) == [det*x for x in base_jet[d]],
                        'affine covariance failed')
                counts['affine_coefficient_checks'] += len(jet[d])
            expected_failure(lambda: decode({d: v for d, v in jet.items() if d < 2*r}))
            counts['negative_controls'] += 1
            record = [list(map(str, p)) for p in polar]
            digest.update((json.dumps(record, separators=(',', ':'))+'\n').encode())
            counts['polygons'] += 1
            counts['decoded_facets'] += 2*r
            facet_counts.add(2*r)

    # The infinite-support disk moments have an independent beta-integral value.
    disk = ellipse_jet((1, 0, 0, 1), 16)
    for m in range(1, 9):
        for j, value in enumerate(moments(disk, 2*m)):
            if j % 2:
                target = F(0)
            else:
                a, b = j//2, m-j//2
                target = F(2*factorial(2*a)*factorial(2*b),
                           4**m*factorial(a)*factorial(b)*factorial(m))
            require(value == target, 'ellipse determinant disagrees with disk beta moment')
            counts['disk_moments'] += 1
    for matrix in matrices:
        ej = ellipse_jet(matrix, 16)
        for k in range(1, 9):
            require(positive_definite(gram(ej, k)), 'smooth ellipse has singular Gram')
            counts['ellipse_positive_grams'] += 1
        expected_failure(lambda ej=ej: decode(ej))
        counts['negative_controls'] += 1

    # Exact rational square rotation: same 3-jet, different 4-jet and body.
    square = hull([(-1, -1), (-1, 1), (1, -1), (1, 1)])
    rotated = transform(square, matrices[3])
    first, second = jet_from_vertices(square, 4), jet_from_vertices(rotated, 4)
    require(first[0] == second[0] and first[2] == second[2], 'square 3-jets differ')
    require(first[4] != second[4] and set(square) != set(rotated), 'sharpness pair collapsed')
    # Roots-of-unity filtering used in the all-r sharpness proof: modes in
    # (cos theta)^j (sin theta)^(d-j) are d-2i. Nonzero modes below 2r
    # are not multiples of 2r. This is an integer check, not trig rounding.
    for r in range(2, 17):
        for d in range(2, 2*r, 2):
            for i in range(d+1):
                mode = d-2*i
                require((mode % (2*r) == 0) == (mode == 0), 'Fourier alias below threshold')
                counts['sharpness_fourier_checks'] += 1

    # Deliberately corrupt the highest Taylor sign; the input is not positive data.
    corrupted = {d: value[:] for d, value in first.items()}
    corrupted[4] = [-x for x in corrupted[4]]
    expected_failure(lambda: decode(corrupted))
    counts['negative_controls'] += 1
    # A rank-one degenerate segment measure cannot pass as a 2D body.
    expected_failure(lambda: decode({0: [F(2)], 2: [F(0), F(0), F(2)]}))
    counts['negative_controls'] += 1
    result = {'status': 'pass', 'arithmetic': 'fractions.Fraction; no floating point',
              'seed': 440921, 'counts': counts, 'facet_counts': sorted(facet_counts),
              'projective_infinity_cases': infinity_cases,
              'decoded_polar_sha256': digest.hexdigest(),
              'square_second_term': [str(x) for x in first[2]],
              'square_fourth_term': [str(x) for x in first[4]],
              'rotated_square_fourth_term': [str(x) for x in second[4]]}
    expected_path = Path(__file__).with_name('expected.json')
    if expected_path.exists():
        require(result == json.loads(expected_path.read_text()), 'expected evidence mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
