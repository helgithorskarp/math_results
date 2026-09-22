"""Exact binary certificate for the exponent-four local Ehrhart jump.

A coordinate class is (a,x) in Z/4 x F_2^s. Allowed classes are
(2,0), or (1,x)/(3,x); together they must generate the full group.
No face enumeration or geometric hypothesis recognition is performed.
"""
from fractions import Fraction


def dot(u, v):
    return (u & v).bit_count() & 1


def dependencies(columns):
    """Kernel basis of a binary column matrix, as masks on columns."""
    pivots = {}
    kernel = []
    for j, column in enumerate(columns):
        v, mask = column, 1 << j
        while v:
            k = v.bit_length() - 1
            if k not in pivots:
                pivots[k] = (v, mask)
                break
            w, c = pivots[k]
            v ^= w
            mask ^= c
        if not v:
            kernel.append(mask)
    return kernel, len(pivots)


def quadratic(z, negative):
    if z.bit_count() & 1:
        raise ValueError('quadratic form requires an even-weight word')
    return ((z.bit_count() // 2) + dot(z, negative)) & 1


def analyze(s, classes):
    if type(s) is not int or s < 0:
        raise ValueError('s must be a nonnegative integer')
    if not isinstance(classes, (tuple, list)) or not classes:
        raise ValueError('nonempty coordinate profile required')
    odd = []
    for item in classes:
        if not isinstance(item, (tuple, list)) or len(item) != 2:
            raise ValueError('each class is a pair')
        a, x = item
        if type(a) is not int or type(x) is not int or not 0 <= x < (1 << s):
            raise ValueError('invalid coordinate class')
        if (a, x) == (2, 0):
            continue
        if a not in (1, 3):
            raise ValueError('coordinate cyclic subgroup does not contain b')
        odd.append((a, x))
    if not odd:
        raise ValueError('profile generates no element of order four')
    basis, rank = dependencies([1 | (x << 1) for a, x in odd])
    if rank != s + 1:
        raise ValueError('coordinate profile does not generate the stated group')
    negative = sum((a == 3) << i for i, (a, x) in enumerate(odd))
    q = lambda z: quadratic(z, negative)
    remaining = basis.copy()
    pairs = []
    while True:
        pair = next(((i, j) for i in range(len(remaining))
                     for j in range(i + 1, len(remaining))
                     if dot(remaining[i], remaining[j])), None)
        if pair is None:
            break
        i, j = pair
        u, v = remaining[i], remaining[j]
        pairs.append([u, v])
        remaining = [w ^ (u if dot(w, v) else 0) ^ (v if dot(w, u) else 0)
                     for k, w in enumerate(remaining) if k not in (i, j)]
    radical = remaining
    witness = next((z for z in radical if q(z)), None)
    phase = sum(q(u) * q(v) for u, v in pairs) & 1
    gauss = 0 if witness is not None else (-1)**phase * (1 << (len(pairs) + len(radical)))
    delta = Fraction(gauss, 1 << len(classes))
    return {'s': s, 'codimension': len(classes), 'order_two_columns': len(classes)-len(odd),
            'odd_columns': len(odd), 'code_dimension': len(basis),
            'code_basis': basis, 'symplectic_pairs': pairs, 'radical_basis': radical,
            'bilinear_rank': 2 * len(pairs), 'radical_dimension': len(radical),
            'cancellation_witness': witness, 'arf': None if witness is not None else phase,
            'gauss_sum': gauss, 'delta': [delta.numerator, delta.denominator]}
