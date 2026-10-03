"""Exact congruences of the complete harmonic cones to original coordinates.

Actual author six-downset-2, researcher. Target n24. This changes
coordinates only; it neither drops the degree-zero mean nor relaxes a cone.
The lift/star/harmonic input is credited7578/9365/9639 and model10008.
"""
from fractions import Fraction as Q
from math import comb
from model import require, choose, lower_keep


def mean_congruence(matrix, populations):
    """P' matrix P, P=I+1 b', with exact quadratic-cost assembly."""
    r = len(populations)
    require(len(matrix) == r and all(len(row) == r for row in matrix),
            'Complete mean matrix shape')
    rows = [sum(row, Q(0)) for row in matrix]
    total = sum(rows, Q(0))
    return [[matrix[i][k]+populations[i]*rows[k]+rows[i]*populations[k]
             +populations[i]*populations[k]*total for k in range(r)]
            for i in range(r)]


def principal_keep(kernels, dimension):
    """RREF pivot deletion is reversible modulo the verified kernel span."""
    rows = [v[:] for v in kernels]
    require(all(len(v) == dimension and all(type(x) is Q for x in v) for v in rows),
            'Exact full kernel vectors')
    position, pivots = 0, []
    for c in range(dimension):
        hit = next((i for i in range(position, len(rows)) if rows[i][c]), None)
        if hit is None:
            continue
        rows[position], rows[hit] = rows[hit], rows[position]
        pivot = rows[position][c]
        rows[position] = [v/pivot for v in rows[position]]
        for i in range(len(rows)):
            if i != position:
                factor = rows[i][c]
                rows[i] = [v-factor*w for v, w in zip(rows[i], rows[position])]
        pivots.append(c)
        position += 1
    require(len(pivots) == len(kernels), 'Independent complete named kernels')
    return [i for i in range(dimension) if i not in pivots]


def original_form(spec, block):
    """Both full physical forms, original metric and exact lower kernels.

    At degree zero the coefficient plane consists of layer constants z and
    actual empty coefficient -b'z. Its metric is diag(b)+bb'. At all other
    degrees the layer vectors are mean zero and the physical metric stays
    diagonal. A restricted lower floor is on the kept coordinate plane only.
    """
    j, g, aa = block['j'], block['gram'], block['layers']
    r = len(aa)
    old_keep, old_kernels = lower_keep(spec, block)
    if j == 0:
        require(aa == list(range(1, spec['r']+1)), 'Full degree-zero layer plane')
        require(g == [comb(spec['n'], a) for a in aa], 'Actual layer populations')
        lower = mean_congruence(block['lower'], g)
        upper = mean_congruence(block['upper'], g)
        gram = [[Q(g[i]*int(i == k)+g[i]*g[k]) for k in range(r)]
                for i in range(r)]
        kernels = []
        for vector in old_kernels:
            shift = sum(g[i]*vector[i] for i in range(r))/spec['N']
            kernels.append([v-shift for v in vector])
        star_shift = Q(spec['n']*spec['s'], spec['N'])
        require(kernels[0] == [Q(a)-star_shift for a in aa],
                'Original centered cardinality-star kernel')
        require(kernels[1:] == old_kernels[1:],
                'Equal-population saturated kernels stay unchanged')
        keep = principal_keep(kernels, r)
    else:
        lower, upper = block['lower'], block['upper']
        gram = [[Q(g[i]*int(i == k)) for k in range(r)] for i in range(r)]
        kernels, keep = old_kernels, old_keep
    for matrix in (lower, upper, gram):
        require(all(matrix[i][k] == matrix[k][i] for i in range(r) for k in range(r)),
                'Symmetric original physical form')
    require(all(lower[i][k]+upper[i][k] == spec['N']*gram[i][k]
                for i in range(r) for k in range(r)), 'Both full original endpoints sum to N metric')
    for v in kernels:
        require(all(sum(lower[i][k]*v[k] for k in range(r)) == 0 for i in range(r)),
                'Entire exact original lower kernel')
    return dict(j=j, layers=aa, diagonal_scaling=g, gram=gram,
                lower=lower, upper=upper, lower_keep=keep,
                kernels=kernels, multiplicity=block['multiplicity'])


def coordinate_scales(spec):
    """Invertible rational scaling of EVERY affine coefficient, no extra bound."""
    scales = [Q(spec['n'])]*(len(spec['active'])+1)
    gammas = []
    for a, b in spec['proper']:
        ga = choose(spec['n']-a-1, b-1)
        gb = choose(spec['n']-b-1, a-1)
        require(ga > 0 and gb > 0, 'Positive proper star-incidence multipliers')
        scales.append(Q(spec['n'], max(ga, gb)))
        gammas.append([ga, gb])
    require(len(scales) == len(spec['names']) and all(s > 0 for s in scales),
            'Every coordinate has an invertible positive rational scale')
    return scales, gammas
