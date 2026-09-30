"""Independent integer-grid/Newton reconstruction of the real-root certificates.

No author implementation is imported. Only compact public summaries are read.
Python >=3.11, standard library, arbitrary-precision integers and Fraction.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb, factorial, lcm, prod
from pathlib import Path
import argparse
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def convolution(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c


def profile_value(pairs, k, point):
    """Return 2520*m**m * P, using only integer t-coefficients.

    The integrand has t-degree 8; 2520 is lcm(1,...,9).
    Each of the m free factors is scaled by m to clear C's denominator.
    """
    a, u, *vs = point
    m = 8 - 2*pairs - k
    D = 1+a
    residual = 1
    radii = []
    for v in vs:
        radii.append(1 + 4*a*v*residual)
        residual *= 1-v
    Cnum = m + 8*a*residual*u
    factors = [[D, -a]] * k + [[m*D, -a*Cnum]] * m
    for R in radii:
        factors.append([D*D, (1-a*a)*R*R-D*D, a*a*R*R])
    integrand = [1]
    for factor in factors:
        integrand = convolution(integrand, factor)
    require(len(integrand) == 9, 'integrand degree bound')
    integral = sum(9*(2520//(i+1))*c for i, c in enumerate(integrand))
    return integral - 2520*Cnum**m*prod(R*R for R in radii)


def natural_degrees(pairs, k):
    """Factorwise degree bound, proved in REVIEW.md, not inferred from data."""
    m = 8-2*pairs-k
    return (16-k, m, *(m+2*(pairs-j) for j in range(pairs)))


def grid_values(pairs, k):
    degrees = natural_degrees(pairs, k)
    shape = tuple(n+1 for n in degrees)
    return shape, [profile_value(pairs, k, x)
                   for x in product(*(range(n) for n in shape))]


def fibers(shape, axis):
    stride = prod(shape[axis+1:])
    width = shape[axis]
    for block in range(prod(shape[:axis])):
        base = block*width*stride
        for tail in range(stride):
            yield base+tail, stride, width


def differences(values, shape):
    """Tensor forward differences: coefficient of prod binom(x_j,alpha_j)."""
    result = list(values)
    for axis in range(len(shape)):
        for start, stride, width in fibers(shape, axis):
            row = [result[start+i*stride] for i in range(width)]
            for j in range(width):
                result[start+j*stride] = row[0]
                row = [y-x for x, y in zip(row, row[1:])]
    return result


def inverse_differences(values, shape):
    result = list(values)
    for axis in range(len(shape)):
        for start, stride, width in fibers(shape, axis):
            row = [result[start+j*stride] for j in range(width)]
            for i in range(width):
                result[start+i*stride] = sum(comb(i, j)*row[j] for j in range(i+1))
    return result


def newton_value(coefficients, shape, point):
    def falling(x, n):
        return prod(x-i for i in range(n))/Q(factorial(n))
    weights = [[falling(x, j) for j in range(n)] for x, n in zip(point, shape)]
    return sum(c*prod(w[j] for w, j in zip(weights, index))
               for c, index in zip(coefficients, product(*(range(n) for n in shape))))


def local_matrix(natural, degree, left, right):
    """Local Bernstein coefficients of binom(x,j), all scaled to integers.

    Build falling factorials by univariate recurrence, substitute the box,
    then use x**h = sum_i binom(i,h)/binom(degree,h) B_i**degree.
    """
    require(degree >= natural and left < right, 'basis bounds')
    columns = []
    falling = [Q(1)]
    width = right-left
    for j in range(natural+1):
        if j:
            falling = convolution(falling, [Q(-(j-1), j), Q(1, j)])
        local = [sum(falling[h]*comb(h, t)*left**(h-t)*width**t
                     for h in range(t, j+1)) for t in range(j+1)]
        columns.append([sum(local[t]*Q(comb(i, t), comb(degree, t))
                            for t in range(min(i, j)+1)) for i in range(degree+1)])
    scale = lcm(*(v.denominator for column in columns for v in column))
    matrix = [[int(columns[j][i]*scale) for j in range(natural+1)]
              for i in range(degree+1)]
    return matrix, scale


def transform(values, shape, axis, matrix):
    width = shape[axis]
    require(all(len(row) == width for row in matrix), 'matrix width')
    stride = prod(shape[axis+1:])
    newshape = shape[:axis] + (len(matrix),) + shape[axis+1:]
    result = [0]*prod(newshape)
    for block in range(prod(shape[:axis])):
        for tail in range(stride):
            row = [values[(block*width+j)*stride+tail] for j in range(width)]
            for i, weights in enumerate(matrix):
                result[(block*len(matrix)+i)*stride+tail] = sum(x*w for x, w in zip(row, weights))
    return result, newshape


def reconstruct(pairs, k, cell, newton, shape):
    result = newton
    denominator = 2520*(8-2*pairs-k)**(8-2*pairs-k)
    intervals = [(Q(0), Q(1))]*2 + [(Q(a), Q(b)) for a, b in cell['radial_box']]
    for axis, (degree, (left, right)) in enumerate(zip(cell['degree'], intervals)):
        matrix, scale = local_matrix(shape[axis]-1, degree, left, right)
        result, shape = transform(result, shape, axis, matrix)
        denominator *= scale
    return [Q(x, denominator) for x in result], shape


def digest(coefficients, shape):
    h = hashlib.sha256()
    for x, index in zip(coefficients, product(*(range(n) for n in shape))):
        h.update((','.join(map(str, index))+':'+str(x.numerator)+'/'+str(x.denominator)+'\n').encode('ascii'))
    return h.hexdigest()


def summary(coefficients, shape, include_zeros=True):
    require(len(coefficients) == prod(shape), 'incomplete enumeration')
    require(all(x >= 0 for x in coefficients), 'negative coefficient')
    zeros = [list(i) for x, i in zip(coefficients, product(*(range(n) for n in shape))) if not x]
    out = {'coefficients': len(coefficients), 'minimum_positive': str(min(x for x in coefficients if x)),
           'sha256': digest(coefficients, shape)}
    if include_zeros:
        out['zero_indices'] = zeros
    else:
        out['zero_coefficients'] = len(zeros)
        out['all_coefficients_nonnegative'] = True
    return out


def cover(boxes):
    """Exact containment of all atomic open boxes; closures cover faces."""
    cuts = [sorted({Q(0), Q(1)} | {Q(endpoint) for box in boxes for endpoint in box[j]}) for j in range(3)]
    require(all(c[0] == 0 and c[-1] == 1 for c in cuts), 'outer box boundary')
    atoms = list(product(*[list(zip(c, c[1:])) for c in cuts]))
    for atom in atoms:
        count = sum(all(Q(L) <= l < r <= Q(R) for (L, R), (l, r) in zip(box, atom)) for box in boxes)
        require(count == 1, 'coverage hole or overlap')
    return len(atoms)


def scope_controls():
    """Definition-level derivative factorizations with 2, 3 and 4 pairs."""
    def power(poly, n):
        out = [1]
        for _ in range(n):
            out = convolution(out, poly)
        return out
    def derivative(poly):
        return [i*x for i, x in enumerate(poly)][1:]
    plus, minus = [1, 0, 1], [-1, 0, 1]
    examples = [
        (convolution([0, 1], power([-1, 0, 0, 0, 1], 2)),
         convolution([-1, 0, 0, 0, 1], [-1, 0, 0, 0, 9])),
        (convolution(convolution([0, 1], power(plus, 3)), minus),
         convolution(power(plus, 2), [-1, 0, -4, 0, 9])),
        (convolution([0, 1], power(plus, 4)),
         convolution(power(plus, 3), [1, 0, 9]))]
    for poly, factored in examples:
        require(derivative(poly) == factored, 'critical pair count control')
    # Exact offset-line collapsed equality: h=3/5, R=4/5, S1=10.
    h, R = Q(3, 5), Q(4, 5)
    require(h*h+R*R == 1, 'affine endpoint circle')
    require(7/(2*R) + 9/(2*R) == 8/R == 10, 'affine equality sum')
    return 5


def bernstein_check(coefficients, shape, p, k, cell):
    """One exact off-grid identity per full local expansion, x_j=1/3."""
    degrees = tuple(n-1 for n in shape)
    common = lcm(*(x.denominator for x in coefficients))
    weights = [[comb(n, i)*2**(n-i) for i in range(n+1)] for n in degrees]
    numerator = sum(x.numerator*(common//x.denominator)*prod(w[j] for w, j in zip(weights, index))
                    for x, index in zip(coefficients, product(*(range(n) for n in shape))))
    value = Q(numerator, common*3**sum(degrees))
    point = (Q(1, 3), Q(1, 3), *(Q(L)+(Q(R)-Q(L))/3 for L, R in cell['radial_box']))
    m = 8-2*p-k
    require(value == profile_value(p, k, point)/Q(2520*m**m), 'full local Bernstein identity')


def controls():
    # Full entry-level inversion for a generic degree-(2,2) integer polynomial.
    shape = (3, 3)
    values = [7+2*x-3*y+5*x*y+11*x*x*y*y for x, y in product(range(3), repeat=2)]
    newton = differences(values, shape)
    for x, y in product(range(3), repeat=2):
        require(newton_value(newton, shape, (Q(x), Q(y))) == values[3*x+y], 'Newton inverse')
    require(newton_value(newton, shape, (Q(2, 7), Q(-3, 5))) ==
            7+2*Q(2, 7)-3*Q(-3, 5)+5*Q(2, 7)*Q(-3, 5)+11*Q(2, 7)**2*Q(-3, 5)**2, 'off-grid identity')
    # Partition of unity and falling-factorial evaluation for local bases.
    for degree in (3, 8):
        for L, R in ((Q(0), Q(1)), (Q(1, 2), Q(1)), (Q(0), Q(1, 2))):
            matrix, scale = local_matrix(3, degree, L, R)
            for x in (Q(0), Q(2, 5), Q(1)):
                weights = [comb(degree, i)*x**i*(1-x)**(degree-i) for i in range(degree+1)]
                for j in range(4):
                    actual = sum(Q(matrix[i][j], scale)*weights[i] for i in range(degree+1))
                    require(actual == prod(L+(R-L)*x-h for h in range(j))/Q(factorial(j)), 'local basis identity')
    return 82


def run(expected):
    require(expected['total_coefficients'] == 186577, 'target size')
    require(len(expected['profiles']) == 10, 'target cell count')
    checks = controls()
    scope_checks = scope_controls()
    U, L, H = ['0', '1'], ['0', '1/2'], ['1/2', '1']
    manifest = [(2, k, degree, [U, U]) for k, degree in enumerate(
        [[16, 4, 10, 8], [15, 3, 7, 5], [14, 2, 6, 4], [13, 1, 8, 8]])]
    manifest += [(3, 0, [16, 2, 10, 8, 6], [U, U, U])]
    manifest += [(3, 1, [15, 1, 8, 8, 8], box) for box in
                 [[U, L, H], [U, H, L], [U, H, H], [H, L, L]]]
    manifest += [(3, 1, [15, 1, 10, 10, 10], [L, L, L])]
    require([(c['pair_count'], c['k'], c['degree'], c['radial_box']) for c in expected['profiles']] == manifest,
            'independently fixed ten-cell manifest')
    profile_cache = {}
    rows = []
    offgrid = 0
    for cell in expected['profiles']:
        p, k = cell['pair_count'], cell['k']
        if (p, k) not in profile_cache:
            shape, values = grid_values(p, k)
            newton = differences(values, shape)
            require(inverse_differences(newton, shape) == values, 'complete integer-grid inverse')
            # Independent exact evaluation outside the interpolation grid.
            point = tuple(Q((-1)**j*(j+1), j+3) for j in range(len(shape)))
            require(newton_value(newton, shape, point) == profile_value(p, k, point), 'profile off-grid reconstruction')
            offgrid += 1
            profile_cache[p, k] = newton, shape
        newton, shape = profile_cache[p, k]
        coefficients, bshape = reconstruct(p, k, cell, newton, shape)
        bernstein_check(coefficients, bshape, p, k, cell)
        original = summary(coefficients, bshape)
        require(all(original[field] == cell[field] for field in original), 'original full-coefficient hash/summary mismatch')
        require(min(x for x in coefficients if x) >= 4, 'positive coefficient bound')
        require(all(x == 8 for x, index in zip(coefficients, product(*(range(n) for n in bshape))) if index[0] == 0), 'a=0 face')
        da = bshape[0]-1
        gap = [x - 8*(1-Q(comb(index[0], 9), comb(da, 9)))
               for x, index in zip(coefficients, product(*(range(n) for n in bshape)))]
        gap_summary = summary(gap, bshape, False)
        require(all(gap_summary[field] == cell['gap8_certificate'][field] for field in gap_summary if field != 'coefficients'), 'gap full-coefficient hash/summary mismatch')
        rows.append({'pair_count': p, 'k': k, 'cell': cell['cell'], 'natural_degrees': list(natural_degrees(p, k)),
                     'degree': cell['degree'], 'radial_box': cell['radial_box'], **original,
                     'gap8_certificate': gap_summary})
    boxes = [cell['radial_box'] for cell in expected['profiles'] if (cell['pair_count'], cell['k']) == (3, 1)]
    atoms = cover(boxes)
    rejects = 0
    def reject(call):
        nonlocal rejects
        try:
            call()
        except ValueError:
            rejects += 1
        else:
            raise ValueError('mutation accepted')
    reject(lambda: cover(boxes[:-1]))
    reject(lambda: cover(boxes + [boxes[0]]))
    changed = coefficients[:]
    changed[-1] += 1
    reject(lambda: require(digest(changed, bshape) == rows[-1]['sha256'], 'changed actual coefficient'))
    negative = coefficients[:]
    negative[0] = Q(-1)
    reject(lambda: summary(negative, bshape))
    reject(lambda: summary(coefficients[:-1], bshape))
    total = sum(row['coefficients'] for row in rows)
    require(total == 186577, 'complete certificate count')
    require(set(profile_cache) == {(2, k) for k in range(4)} | {(3, k) for k in range(2)}, 'profile coverage')
    return {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer',
            'method': 'integer t-coefficient evaluation on complete integer grid; tensor forward differences; local Newton-to-Bernstein conversion with common-denominator integer transforms',
            'arithmetic': 'arbitrary-precision integers and Fraction; standard library only',
            'profiles': rows, 'original_coefficients': total, 'gap_coefficients': total,
            'full_coefficient_hash_matches': 20, 'complete_interpolation_grid_points': sum(prod(shape) for _, shape in profile_cache.values()),
            'off_grid_exact_identities': offgrid, 'small_basis_control_checks': checks,
            'complete_integer_grid_inverses': len(profile_cache),
            'local_bernstein_definition_identities': len(rows), 'scope_control_checks': scope_checks,
            'atomic_subboxes': atoms, 'mutation_rejections': rejects}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('author_summary', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(json.loads(args.author_summary.read_text()))
    output = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end='')
