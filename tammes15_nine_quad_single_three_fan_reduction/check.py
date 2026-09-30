"""Exact Tammes-15 single-three fan checks; six-tammes-1, researcher.

CPython >=3.11, standard library. The certificate generator is untrusted:
all vector recurrences, norms, contacts and scalar identities are checked
in Z[c,t]. Exact tensor Bernstein coefficients prove the stated signs.
The original-face interpretation remains the written proof in PROOF.md.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
ONE = {(0, 0): 1}
C = {(1, 0): 1}
T = {(0, 1): 1}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add(p, q):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v}


def scale(a, p):
    return {k: a*v for k, v in p.items() if a*v}


def sub(p, q):
    return add(p, scale(-1, q))


def mul(p, q):
    out = {}
    for (i, j), a in p.items():
        for (k, l), b in q.items():
            key = i+k, j+l
            out[key] = out.get(key, 0) + a*b
    return {k: v for k, v in out.items() if v}


def psum(polynomials):
    out = {}
    for p in polynomials:
        out = add(out, p)
    return out


def decode(rows):
    need(isinstance(rows, list) and len(rows) <= 1000, 'polynomial row list')
    out = {}
    previous = None
    for row in rows:
        need(isinstance(row, list) and len(row) == 3, 'monomial triple')
        i, j, a = row
        need(all(type(v) is int for v in row), 'integer monomial entries')
        need(0 <= i <= 64 and 0 <= j <= 64 and a != 0,
             'bounded nonzero canonical monomial')
        key = i, j
        need(previous is None or previous < key, 'strict monomial order')
        previous = key
        out[key] = a
    return out


def degree(p):
    need(bool(p), 'nonzero polynomial required')
    return max(i for i, j in p), max(j for i, j in p)


def transformation(n, lo, hi):
    # Monomial x^i in the degree-n Bernstein basis on [lo,hi].
    return tuple(tuple(sum(F(comb(i, r)*comb(k, r), comb(n, r))
                           *lo**(i-r)*(hi-lo)**r
                           for r in range(min(i, k)+1))
                       for i in range(n+1)) for k in range(n+1))


def bernstein(p):
    n, m = degree(p)
    A = transformation(n, F(1, 2), F(3, 5))
    B = transformation(m, F(5, 11), F(15, 23))
    middle = [[sum(p.get((i, j), 0)*A[k][i] for i in range(n+1))
               for j in range(m+1)] for k in range(n+1)]
    return tuple(tuple(sum(middle[k][j]*B[l][j] for j in range(m+1))
                       for l in range(m+1)) for k in range(n+1))


def positive(name, p):
    rows = bernstein(p)
    entries = [v for row in rows for v in row]
    need(min(entries) > 0, 'strict positive Bernstein coefficients: '+name)
    digest = hashlib.sha256(json.dumps([[str(v) for v in row] for row in rows],
                                      separators=(',', ':')).encode()).hexdigest()
    return {'degree': list(degree(p)), 'coefficients': len(entries),
            'minimum': str(min(entries)), 'maximum': str(max(entries)),
            'sha256': digest}


def cross(a, b):
    return (sub(mul(a[1], b[2]), mul(a[2], b[1])),
            sub(mul(a[2], b[0]), mul(a[0], b[2])),
            sub(mul(a[0], b[1]), mul(a[1], b[0])))


def dot_numerator(a, b):
    x, dx = a
    y, dy = b
    return add(mul(sub(ONE, C), psum(mul(u, v) for u, v in zip(x, y))),
               mul(C, mul(psum(x), psum(y))))


def same_vector(a, b, message):
    x, dx = a
    y, dy = b
    need(all(not sub(mul(u, dy), mul(v, dx)) for u, v in zip(x, y)), message)


def reflection(a, b, old):
    x, dx = a
    y, dy = b
    z, dz = old
    base = mul(add(ONE, C), mul(dx, dy))
    nums = tuple(sub(mul(scale(2, C), mul(add(mul(u, dy), mul(v, dx)), dz)),
                     mul(w, base)) for u, v, w in zip(x, y, z))
    return nums, mul(base, dz)


def opposite(old, a, b):
    x, dx = a
    y, dy = b
    z, dz = old
    base = add(mul(dx, dy), dot_numerator(a, b))
    nums = tuple(sub(mul(scale(2, C), mul(add(mul(u, dy), mul(v, dx)), dz)),
                     mul(w, base)) for u, v, w in zip(x, y, z))
    return (nums, mul(base, dz)), base


def triangle(a, b, sign):
    x, dx = a
    y, dy = b
    n = cross(x, y)
    sn = psum(n)
    H = add(ONE, scale(2, C))
    nums = tuple(add(mul(C, add(mul(u, dy), mul(v, dx))),
                     scale(sign, sub(mul(H, w), mul(C, sn))))
                 for u, v, w in zip(x, y, n))
    return nums, mul(add(ONE, C), mul(dx, dy))


def verify(certificate):
    need(certificate['format'] == 'tammes15-five-three-collar-v1', 'format')
    need(certificate['coefficient_domain'] == 'Z[c,t]', 'coefficient domain')
    need(certificate['variable_order'] == ['c', 't'], 'variable order')
    need(certificate['rectangle'] == ['1/2', '3/5', '5/11', '15/23'], 'rectangle')
    names = ('F', 'X', 'R', 'S', 'Z', 'U', 'B', 'C', 'Y', 'J', 'M', 'N', 'O')
    need(set(certificate['points']) == set(names), 'exact point names')
    V = {}
    signs = {}
    for name in names:
        obj = certificate['points'][name]
        need(len(obj['numerators']) == 3, 'three vector coordinates')
        V[name] = tuple(decode(p) for p in obj['numerators']), decode(obj['denominator'])
        signs['point_denominator_'+name] = positive('point denominator '+name, V[name][1])
    for k, name in enumerate(('F', 'X', 'R')):
        seed = tuple(ONE if j == k else {} for j in range(3)), ONE
        same_vector(V[name], seed, 'equilateral basis '+name)
    same_vector(V['S'], reflection(V['F'], V['R'], V['X']), 'triangle reflection S')
    same_vector(V['Z'], reflection(V['F'], V['S'], V['R']), 'triangle reflection Z')
    H = add(ONE, scale(2, C))
    tt = mul(T, T)
    U = ((mul(scale(2, C), mul(T, add(mul(H, T), ONE))),
          add(sub(ONE, mul(H, tt)), mul(scale(2, C), T)),
          scale(-2, mul(add(ONE, C), T))), add(ONE, mul(H, tt)))
    same_vector(V['U'], U, 'half-angle parametrization U')
    for name, old, a, b in (('B', 'F', 'U', 'X'), ('C', 'F', 'U', 'Z'),
                            ('Y', 'U', 'B', 'C')):
        expected, divisor = opposite(V[old], V[a], V[b])
        same_vector(V[name], expected, 'original Q opposite '+name)
        signs['Q_divisor_'+name] = positive('Q divisor '+name, divisor)
    same_vector(V['J'], triangle(V['X'], V['B'], +1), 'positive triangle branch J')
    same_vector(V['M'], triangle(V['Z'], V['C'], -1), 'negative triangle branch M')
    for name, old, a, b in (('N', 'B', 'J', 'Y'), ('O', 'C', 'Y', 'M')):
        expected, divisor = opposite(V[old], V[a], V[b])
        same_vector(V[name], expected, 'original Q opposite '+name)
        signs['Q_divisor_'+name] = positive('Q divisor '+name, divisor)
    for name in names:
        need(not sub(dot_numerator(V[name], V[name]), mul(V[name][1], V[name][1])),
             'exact unit norm '+name)
    contacts = (('F', 'X'), ('F', 'R'), ('F', 'S'), ('F', 'Z'), ('F', 'U'),
                ('X', 'R'), ('R', 'S'), ('S', 'Z'), ('U', 'B'), ('U', 'C'),
                ('B', 'X'), ('B', 'Y'), ('C', 'Z'), ('C', 'Y'),
                ('X', 'J'), ('B', 'J'), ('Z', 'M'), ('C', 'M'),
                ('J', 'N'), ('Y', 'N'), ('Y', 'O'), ('M', 'O'))
    for a, b in contacts:
        need(not sub(dot_numerator(V[a], V[b]), mul(C, mul(V[a][1], V[b][1]))),
             'exact prescribed contact '+a+b)
    scalar = certificate['NO_inner_product']
    num, den = decode(scalar['numerator']), decode(scalar['denominator'])
    need(not sub(mul(num, mul(V['N'][1], V['O'][1])),
                 mul(den, dot_numerator(V['N'], V['O']))), 'exact N,O scalar identity')
    signs['NO_denominator'] = positive('NO denominator', den)
    signs['NO_cosine_excess_over_one_twentieth'] = positive(
        'NO cosine excess over 1/20', sub(scale(20, sub(num, mul(C, den))), den))
    signs['NO_distinctness_over_one_thousandth'] = positive(
        'NO distinctness over 1/1000', sub(scale(1000, sub(den, num)), den))
    return {'points': len(names), 'construction_identities': 10,
            'unit_norm_identities': len(names), 'prescribed_contacts': len(contacts),
            'scalar_identity': 'N dot O = certificate numerator / denominator',
            'strict_margins': {'N_dot_O_minus_c': '1/20', '1_minus_N_dot_O': '1/1000'},
            'closed_rectangle': ['1/2', '3/5', '5/11', '15/23'],
            'positive_tensor_Bernstein_tables': signs,
            'subdivisions': 0}


def bookkeeping():
    # The written incidence lemmas exclude (ordinary,0,3) and (deficit1,1,2).
    rows = []
    for delta in range(3):
        for b in range(4):
            a = 6-delta-2*b
            if a < 0 or a+b < delta+1:
                continue
            if (delta, a, b) in ((0, 0, 3), (1, 1, 2)):
                continue
            rows.append({'five_deficit': delta, 'one_T_fours': a,
                         'zero_T_fours': b, 'ordinary_fours': 13-a-b})
    need(len(rows) == 7, 'seven full-interval r1 necessary profiles')
    # Enumerate all cyclic five-stars, without assuming T blocks in advance.
    stars = []
    for delta in (1, 2):
        target = delta+1
        for mask in range(32):
            q = tuple(bool(mask >> k & 1) for k in range(5))
            if sum(q) != target:
                continue
            qq = sum(q[k] and q[(k+1) % 5] for k in range(5))
            need(qq in ((0, 1) if delta == 1 else (1, 2)), 'all cyclic Q-Q counts')
            stars.append({'five_deficit': delta, 'Q_mask': mask,
                          'forced_three_contacts': qq,
                          'allowed_with_unique_three': qq <= 1})
    labelled = []
    for zero in ('B', 'C', 'D'):
        for paired_xr in (False, True):
            for paired_sz in (False, True):
                if not paired_xr and (zero in ('B', 'D')):
                    continue
                if not paired_sz and (zero in ('C', 'D')):
                    continue
                if not (paired_xr or paired_sz):
                    continue
                labelled.append((zero, paired_xr, paired_sz))
    reflected = {'B': 'C', 'C': 'B', 'D': 'D'}
    canonical = sorted({min(x, (reflected[x[0]], x[2], x[1])) for x in labelled})
    need(len(labelled) == 5 and len(canonical) == 3, 'complete second-triangle prefix cover')
    return {'r1_necessary_profiles_on_open_half_three_fifths': rows,
            'profiles': 7, 'cyclic_five_stars': stars,
            'delta2_a2_b1_second_triangle_prefixes': {
                'labelled': labelled, 'up_to_reflection': canonical,
                'scope': 'Original-face prefixes; unknown third-point aliases and the remaining faces are retained.'},
            'two_excluded_previous_r1_rows': [[0, 0, 3], [1, 1, 2]],
            'beta_interval_previous_32_profiles_minus_two': 30,
            'cover_warning': 'Necessary count profiles, not embeddings or realizable packings.'}


def controls(certificate):
    from copy import deepcopy
    rejected = []
    for name, mutate in (
        ('zero_point_denominator', lambda x: x['points']['F'].update(denominator=[])),
        ('wrong_N_coordinate', lambda x: x['points']['N']['numerators'][0][0].__setitem__(2,
            x['points']['N']['numerators'][0][0][2]+1)),
        ('wrong_NO_scalar', lambda x: x['NO_inner_product']['numerator'][0].__setitem__(2,
            x['NO_inner_product']['numerator'][0][2]+1)),
        ('wrong_parameter_rectangle', lambda x: x.__setitem__('rectangle', ['1/2', '3/5', '0', '1'])),
    ):
        bad = deepcopy(certificate)
        mutate(bad)
        try:
            verify(bad)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('negative certificate control accepted: '+name)
    for name, operation in (
        ('duplicate_monomial', lambda: decode([[0, 0, 1], [0, 0, 2]])),
        ('negative_Bernstein_sign', lambda: positive('negative control', {(0, 0): -1})),
    ):
        try:
            operation()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('negative algebra control accepted: '+name)
    return {'negative_controls_rejected': rejected,
            'positive_control': positive('positive tensor example', {(0, 0): 1, (1, 1): 1})}


def main():
    data = (ROOT/'certificate.json').read_bytes()
    certificate = json.loads(data)
    result = {'agent': 'six-tammes-1', 'role': 'researcher',
              'status': 'AUTHOR_CHECKED_EXACT_CONDITIONAL_REDUCTION',
              'certificate_sha256': hashlib.sha256(data).hexdigest(),
              'collar': verify(certificate), 'bookkeeping': bookkeeping(),
              'controls': controls(certificate),
              'trust_boundary': 'Original-face forcing and geometric interpretation are written and unformalized. No independent review or global numerical bound is claimed.'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
