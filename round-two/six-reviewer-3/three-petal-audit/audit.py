#!/usr/bin/env python3
"""six-reviewer-3: independent projector, interpolation and integer audit.

No author Python imports; two explicitly hash-pinned public JSON comparisons.
The unbounded proofs and degree bounds are in REVIEW.md, not finite sampling.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
from math import lcm
from pathlib import Path
import json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def transpose(a):
    return list(map(list, zip(*a)))


def psd(a):
    """Denominator clearing; symmetric pivoted integer Bareiss elimination."""
    n = len(a)
    need(n and all(len(row) == n for row in a), 'square PSD input')
    need(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)), 'PSD symmetry')
    den = lcm(*(F(x).denominator for row in a for x in row))
    a = [[int(F(x)*den) for x in row] for row in a]
    previous, rank = 1, 0
    while a:
        n = len(a)
        need(all(a[i][i] >= 0 for i in range(n)), 'negative diagonal')
        pivot = max(range(n), key=lambda i: a[i][i])
        if a[pivot][pivot] == 0:
            need(all(x == 0 for row in a for x in row), 'illegal zero residual')
            break
        ids = [i for i in range(n) if i != pivot]
        p = a[pivot][pivot]
        out = []
        for i in ids:
            row = []
            for j in ids:
                num = p*a[i][j]-a[i][pivot]*a[pivot][j]
                need(num % previous == 0, 'nonintegral Bareiss division')
                row.append(num//previous)
            out.append(row)
        a, previous, rank = out, p, rank+1
    return rank


def inverse(a):
    n = len(a)
    a = [[F(x) for x in row]+[F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for k in range(n):
        p = next(i for i in range(k, n) if a[i][k])
        a[k], a[p] = a[p], a[k]
        d = a[k][k]
        a[k] = [x/d for x in a[k]]
        for i in range(n):
            if i != k:
                d = a[i][k]
                a[i] = [x-d*y for x, y in zip(a[i], a[k])]
    return [row[n:] for row in a]


def fingerprint(a):
    return sha256(json.dumps([[str(x) for x in row] for row in a], separators=(',', ':')).encode()).hexdigest()


def balanced(stars):
    t, u, v = stars
    a, b = F(t-2*u+1, t-1), F(t-2*v+1, t-1)
    need(a+b > 1 and abs(a-b) < 1 and a > 0 and b > 0, 'triangle hypotheses')
    g = [[F(1), (1+a*a-b*b)/(2*a), (1+b*b-a*a)/(2*b)],
         [(1+a*a-b*b)/(2*a), F(1), (1-a*a-b*b)/(2*a*b)],
         [(1+b*b-a*a)/(2*b), (1-a*a-b*b)/(2*a*b), F(1)]]
    g = [[(t-1)*x for x in row] for row in g]
    need(mm(g, [[-1], [a], [b]]) == [[0], [0], [0]], 'balanced null vector')
    need(psd(g) == 2, 'balanced rank')
    return g


def frame_invariants(stars):
    """Compute cleared invariants from actual Gram minors, not source (7)."""
    t, u, v = map(F, stars)
    n, A = 2*(t+u+v)-2, t-1
    d, e = t-2*u+1, t-2*v+1
    g = balanced(stars)
    diagonal = [1+(2*w-2)/(A*A) for w in stars]
    trace = sum(diagonal[i]*g[i][i] for i in range(3))
    second = sum(diagonal[i]*diagonal[j]*(g[i][i]*g[j][j]-g[i][j]**2)
                 for i, j in combinations(range(3), 2))
    denominator = 4*d*d*e*e*A**3
    h = 4*d*d*e*e-(A*A-d*d-e*e)**2
    cap = denominator*(n*n-n*trace+second)
    w = A*(2*n-trace)
    return h, cap, w


def interpolate_grid(fn, degree):
    """Tensor Newton interpolation on 0..degree, then binomial -> powers."""
    count = degree+1
    values = {e: F(fn(e)) for e in product(range(count), repeat=3)}
    basis = [[F(1)]]
    for k in range(1, count):
        b = [F(0)]*(k+1)
        for i, c in enumerate(basis[-1]):
            b[i] -= F(k-1, k)*c
            b[i+1] += c/k
        basis.append(b)
    for axis in range(3):
        out = {}
        others = [i for i in range(3) if i != axis]
        for pair in product(range(count), repeat=2):
            ids = []
            for k in range(count):
                e = [0, 0, 0]
                e[axis] = k
                for j, value in zip(others, pair):
                    e[j] = value
                ids.append(tuple(e))
            row = [values[e] for e in ids]
            differences = []
            while row:
                differences.append(row[0])
                row = [b-a for a, b in zip(row, row[1:])]
            coefficients = [sum(differences[k]*basis[k][j] for k in range(j, count))
                            for j in range(count)]
            for e, c in zip(ids, coefficients):
                out[e] = c
        values = out
    return {e: c for e, c in values.items() if c}


def signs(published):
    names = ['heron_numerator', 'cap_quadratic_numerator', 'twice_N_minus_trace_numerator']
    output = {}
    for index, degree, count, constant in zip(range(3), [4, 9, 2], [34, 219, 10], [243, 168399, 27]):
        def fn(e):
            x, y, z = e
            v, u = 1+x, 1+x+y
            return frame_invariants((4*u+z, u, v))[index]
        terms = interpolate_grid(fn, degree)
        need(len(terms) == count and terms[(0, 0, 0)] == constant, 'coefficient census')
        need(all(c > 0 and c.denominator == 1 for c in terms.values()), 'polynomial sign')
        need(max(map(sum, terms)) == degree, 'total degree')
        certificate = [[list(e), str(c)] for e, c in sorted(terms.items())]
        need(certificate == published[names[index]], 'published coefficient comparison')
        output[names[index]] = {'terms': count, 'constant': constant, 'degree': degree,
                                'grid_points': (degree+1)**3,
                                'sha256': sha256(json.dumps(certificate, separators=(',', ':')).encode()).hexdigest()}
    return output


def parameters(stars):
    t, u, v = stars
    n = 2*sum(stars)-2
    if t == u == v:
        return [[F((t-1)*(i == j)) for j in range(3)] for i in range(3)], F(2*t)
    if t == u:
        return [[F(t-1), F(1-t), F(0)], [F(1-t), F(t-1), F(0)], [F(0), F(0), F(t-1)]], F(n-2*(t+1))
    if u == v == 1:
        return balanced(stars), F(2)
    if t == 2*u and v == 1:
        return balanced(stars), F(1, t-1)
    if t == 2*u:
        return [[F(t-1)]*3 for _ in range(3)], F(2*(v-1)*(t-2*v+2), t-1)
    need(t >= 4*u, 'complete dyadic split')
    h, f, w = frame_invariants(stars)
    need(min(h, f, w) > 0, 'wide-gap signs')
    return balanced(stars), min(F(n-2*t), f/(4*(t-2*u+1)**2*(t-2*v+1)**2*(t-1)**3*n))


def vertices(orders):
    need(len(orders) >= 2 and list(orders) == sorted(orders, reverse=True)
         and all(type(x) is int and x >= 1 for x in orders), 'sorted positive orders')
    need(sum(2**a for a in orders)-len(orders)+1 <= 80, 'literal size guard')
    result, offset = [], 0
    for j, order in enumerate(orders):
        full = (1 << order)-1
        result += [(j, a, full, a << offset) for a in range(1, full+1)]
        offset += order
    return result


def projected_core(orders, g):
    """Construct Z using complementary +/- projectors, then Gram coefficient map."""
    data = vertices(orders)
    stars = [1 << (a-1) for a in orders]
    t, A = stars[0], stars[0]-1
    c = []
    for i, a, full, _ in data:
        row = []
        for j, b, full_b, _ in data:
            ca = F(1) if a == full else F(-1, A)
            cb = F(1) if b == full_b else F(-1, A)
            value = ca*cb*g[i][j]
            if i == j and a != full and b != full:
                u, ell = stars[i], 2*stars[i]-2
                plus = F(int(a == b)+int(a ^ b == full), 2)
                minus = F(int(a == b)-int(a ^ b == full), 2)
                z = ell*(plus-F(1, ell))+2*(t-u)*minus
                value += F(t, A)*z
            row.append(value)
        c.append(row)
    return c


def shifted_core(orders):
    data = vertices(orders)
    stars = [1 << (a-1) for a in orders]
    t = stars[0]
    return [[F(t*(i == j and a == b) + stars[i]*(i == j and a ^ b == full)-int(i == j))
             for j, b, _, _ in data] for i, a, full, _ in data]


def lift_q(c):
    """Literal E multiplication; no row-sum constructor."""
    m = len(c)
    e = [[F(-1)]*m]+[[F(i == j) for j in range(m)] for i in range(m)]
    return mm(mm(e, c), transpose(e))


def matrix_from_q(q, t):
    n = len(q)
    return [[(1+q[i][j]-t*(i == j))/(n-t) for j in range(n)] for i in range(n)]


def checks(family, matrix, s, forced, upper_nullity=1):
    n = len(family)
    need(len(matrix) == n and family[0] == 0 and len(set(family)) == n, 'vertex dimension')
    star = max(sum(bool(a & (1 << i)) for a in family) for i in range(max(family).bit_length()))
    need(star == s, 'literal largest star')
    present = set(family)
    for a in family:
        b = a
        while b:
            need(b in present, 'downset closure')
            b = (b-1) & a
    need(all(sum(row) == 1 for row in matrix), 'row sums')
    need(all(not (a & b) or matrix[i][j] == 0 for i, a in enumerate(family) for j, b in enumerate(family)), 'intersection support')
    lower = [[(n-s)*matrix[i][j]+s*(i == j) for j in range(n)] for i in range(n)]
    upper = [[F(i == j)-matrix[i][j] for j in range(n)] for i in range(n)]
    need(psd(lower) == n-forced, 'lower rank')
    need(psd(upper) == n-upper_nullity, 'upper rank')
    return {'N': n, 's': s, 'lower_rank': n-forced, 'upper_rank': n-upper_nullity,
            'matrix_sha256': fingerprint(matrix)}


def gap(matrix, t, beta):
    n = len(matrix)
    test = [[(n-t)*(F(i == j)-matrix[i][j])-beta*(F(i == j)-F(1, n))
             for j in range(n)] for i in range(n)]
    return psd(test)


def build(orders, improved=False):
    data = vertices(orders)
    family = [0]+[x[3] for x in data]
    stars = [1 << (a-1) for a in orders]
    t, n = stars[0], len(family)
    cshift = shifted_core(orders)
    qshift = lift_q(cshift)
    if t == 1:
        return (family, matrix_from_q(qshift, t), t), {'epsilon': '0'}
    if len(orders) == 2:
        need(stars[0] > stars[1], 'two-branch inherited constructor')
        u = stars[1]
        g = [[F(t-1)]*2 for _ in range(2)]
        beta = F((2*u-1)*(t-2*u+1), t-1)
    else:
        need(len(orders) == 3, 'three branches')
        g, beta = parameters(stars)
    c = projected_core(orders, g)
    q = lift_q(c)
    B = sum(w-1+(t-w)*(2*w-1) for w in stars)
    qtrace = (n-1)*(t-1)+B
    need(sum(qshift[i][i] for i in range(n)) == qtrace, 'trace identity')
    h, cap = t+1, t+1+B
    K = 2*sum(w*w*(t-w) for w in stars)
    need(h*B-sum(sum(row)**2 for row in cshift) == K, 'constant/full deficit identity')
    eta = min(F(cap-2*t), F(K, cap)) if K else F(0)
    need(psd([[cap*(F(i == j)-F(1, n))-qshift[i][j] for j in range(n)] for i in range(n)]) == n-1-int(K == 0), 'new shifted norm rank')
    psd([[(cap-eta)*(F(i == j)-F(1, n))-qshift[i][j] for j in range(n)] for i in range(n)])
    epsilon = beta/(beta+max(F(cap-n), F(0))) if improved else beta/(2*(beta+qtrace))
    mixed = matrix_from_q([[(1-epsilon)*q[i][j]+epsilon*qshift[i][j] for j in range(n)] for i in range(n)], t)
    seed = matrix_from_q(q, t)
    forced = t*stars.count(t)
    p = sum(1 < w < t for w in stars)
    seed_nullity = forced+len(stars)+p-psd(g)
    checks(family, seed, t, seed_nullity)
    gap(seed, t, beta)
    gbound = (1-epsilon)*beta+epsilon*(n-cap+eta) if improved else beta/2
    need(gbound > 0, 'positive endpoint gap')
    gap(mixed, t, gbound)
    if len(stars) == 3:
        diagonal = [1+F(2*w-2, (t-1)**2) for w in stars]
        alpha = [F(t-2*w+1, t-1) for w in stars]
        R = [[diagonal[i]*(i == j)+alpha[i]*alpha[j] for j in range(3)] for i in range(3)]
        inv = inverse(R)
        psd([[(n-beta)*inv[i][j]-g[i][j] for j in range(3)] for i in range(3)])
    return (family, mixed, t), {'beta': str(beta), 'epsilon': str(epsilon), 'q': qtrace,
                               'B': B, 'new_shifted_norm_bound': cap, 'eta': str(eta),
                               'scaled_upper_gap_bound': str(gbound), 'seed_lower_rank': n-seed_nullity,
                               'seed_matrix_sha256': fingerprint(seed)}


def cube(order):
    family = list(range(1 << order))
    full = family[-1]
    return family, [[F(a ^ b == full) for b in family] for a in family], 1 << (order-1)


def union(parts):
    need(len(parts) >= 2 and len({p[2] for p in parts}) == 1, 'equal-star packets')
    s = parts[0][2]
    family, blocks, offset = [0], [], 0
    for f, matrix, _ in parts:
        family += [a << offset for a in f[1:]]
        offset += max(f).bit_length()
        n = len(f)
        blocks.append([[(n-s)*matrix[i][j]+s*(i == j)-1 for j in range(1, n)] for i in range(1, n)])
    c = [[F(0)]*(len(family)-1) for _ in family[1:]]
    start = 0
    for b in blocks:
        for i in range(len(b)):
            for j in range(len(b)):
                c[start+i][start+j] = b[i][j]
        start += len(b)
    return family, matrix_from_q(lift_q(c), s), s


def packets(orders):
    k = orders.count(orders[0])
    need(len(orders) <= 3*k, 'packet allocation bound')
    ps = [[orders[0]] for _ in range(k)]
    for i, order in enumerate(orders[k:]):
        ps[i % k].append(order)
    parts = [cube(p[0]) if len(p) == 1 else build(p)[0] for p in ps]
    return union(parts) if k > 1 else parts[0]


def tensor(parts):
    ids = list(product(*(range(len(p[0])) for p in parts)))
    need(len(ids) <= 80, 'tensor size guard')
    offsets, offset = [], 0
    for f, _, _ in parts:
        offsets.append(offset)
        offset += max(f).bit_length()
    family = [sum(parts[j][0][row[j]] << offsets[j] for j in range(len(parts))) for row in ids]
    a = []
    for x in ids:
        row = []
        for y in ids:
            v = F(1)
            for j, p in enumerate(parts):
                v *= p[1][x[j]][y[j]]
            row.append(v)
        a.append(row)
    s = max(p[2]*(len(ids)//len(p[0])) for p in parts)
    return family, a, s


def census(part):
    family, matrix, s = part
    need(len(family) <= 24 and s <= 8, 'census guard')
    maximal = [f for f in combinations(range(1, len(family)), s)
               if all(family[i] & family[j] for i, j in combinations(f, 2))]
    need(maximal, 'empty maximum census')
    gram = [[F(sum(i in f and j in f for f in maximal)) for j in range(1, len(family))]
            for i in range(1, len(family))]
    return {'N': len(family), 's': s, 'maximum_family_count': len(maximal),
            'forced_core_dimension': psd(gram)}


def reject(fn):
    try:
        fn()
    except (ValueError, StopIteration):
        return
    raise ValueError('corruption accepted')


def run(author, coefficients):
    polynomial_results = signs(coefficients)
    triples = [tuple(reversed(x)) for x in combinations_with_replacement(range(1, 5), 3)]
    triples += [(5, 4, 3), (5, 4, 4), (6, 2, 1), (6, 3, 2)]
    rows, built, entry_count = [], {}, 0
    for orders, old in zip(triples, author['three_cubes']):
        part, meta = build(orders)
        forced = part[2]*orders.count(orders[0])
        observed = checks(*part, forced)
        need(list(orders) == old['orders'] and all(observed[k] == old[k] for k in observed), 'original entry/rank/hash comparison')
        if part[2] > 1:
            need(meta['seed_lower_rank'] == old['seed_lower_rank'] and meta['seed_matrix_sha256'] == old['seed_matrix_sha256'], 'seed comparison')
            need(meta['beta'] == old['beta'] and meta['epsilon'] == old['epsilon'], 'original parameter comparison')
            improved, newmeta = build(orders, True)
            newobs = checks(*improved, forced)
            need(F(newmeta['epsilon']) > F(meta['epsilon']), 'strict repair enlargement')
            newobs.update(newmeta)
        else:
            newobs = None
        rows.append({'orders': list(orders), 'original': observed, 'improved': newobs})
        built[orders] = part
        entry_count += len(part[0])**2
    assemblies = []
    for old in author['many_cube_assemblies']:
        orders = old['orders']
        part = packets(orders)
        obs = checks(*part, part[2]*orders.count(orders[0]))
        need(all(obs[k] == old[k] for k in obs), 'assembly comparison')
        assemblies.append(obs)
        entry_count += len(part[0])**2
    products = []
    fixture_parts = [[built[(2, 1, 1)], built[(2, 1, 1)]],
                     [built[(2, 1, 1)], built[(1, 1, 1)]],
                     [built[(2, 2, 1)], built[(1, 1, 1)]],
                     [built[(2, 1, 1)], build((2, 1))[0]]]
    for parts, old in zip(fixture_parts, author['products']):
        part = tensor(parts)
        obs = checks(*part, old['forced_nullity'])
        need(all(obs[k] == old[k] for k in obs), 'product comparison')
        products.append(obs)
        entry_count += len(part[0])**2
    sunflowers = []
    for old in author['common_core_sunflowers']:
        c, orders = old['common_core_order'], tuple(old['petal_orders'])
        part = tensor([cube(c), built[orders]])
        obs = checks(*part, 1 << (c-1), 1 << (c-1))
        need(all(obs[k] == old[k] for k in obs), 'common-core comparison')
        sunflowers.append(obs)
        entry_count += len(part[0])**2
    censuses = []
    for orders in [tuple(reversed(x)) for x in combinations_with_replacement(range(1, 4), 3)]:
        obs = census(built[orders])
        need(obs['forced_core_dimension'] == built[orders][2]*orders.count(orders[0]), 'finite universal forced span')
        censuses.append({'orders': list(orders), **obs})
    for c, orders in [(1, (1, 1, 1)), (1, (2, 1, 1)), (2, (1, 1, 1))]:
        part = tensor([cube(c), built[orders]])
        obs = census(part)
        need(obs['forced_core_dimension'] == 1 << (c-1), 'common-core census span')
        need(obs['maximum_family_count'] == census(cube(c))['maximum_family_count'], 'cylinder count')
        censuses.append({'common_core_order': c, 'orders': list(orders), **obs})
    controls = [lambda: psd([[-1]]), lambda: psd([[0, 1], [1, 0]]),
                lambda: psd([[1, 0], [1, 1]]), lambda: vertices((1, 2, 1)),
                lambda: vertices((2, 1, 0)), lambda: vertices((6, 6, 1)),
                lambda: balanced((8, 4, 2)), lambda: packets([4, 2, 1, 1])]
    for f in controls:
        reject(f)
    family, matrix, s = built[(2, 1, 1)]
    bad = [row[:] for row in matrix]
    bad[1][1] = 1
    reject(lambda: checks(family, bad, s, s))
    reject(lambda: gap(matrix, s, 100))
    return {'reviewer': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
            'polynomial_interpolation': polynomial_results, 'three_cubes': rows,
            'many_cube_assemblies': assemblies, 'products': products, 'common_core_sunflowers': sunflowers,
            'complete_maximum_family_censuses': censuses, 'original_matrix_entries_compared': entry_count,
            'rejection_controls': len(controls)+2,
            'scope': 'ordinary unformalized proof; exact independent finite evidence; general H/I unresolved'}


def read_pinned(path, digest):
    raw = path.read_bytes()
    need(sha256(raw).hexdigest() == digest, 'public input SHA256')
    return json.loads(raw)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--author-results', type=Path, required=True)
    p.add_argument('--coefficients', type=Path, required=True)
    p.add_argument('--write', type=Path)
    p.add_argument('--check', type=Path)
    args = p.parse_args()
    author = read_pinned(args.author_results, 'e2bffb13274445cded7b3b808cd0e9ec6389613d4de88d71664bdfc4dc808d0d')
    coefficients = read_pinned(args.coefficients, '892ff3f9611aa4632fd67936d630eff35c52960098016c404323c9446dc5ddbb')
    result = run(author, coefficients)
    raw = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
    if args.write:
        args.write.write_bytes(raw)
    if args.check:
        need(json.loads(args.check.read_bytes()) == result, 'independent expected receipt')
    print(json.dumps({'ok': True, 'original_matrix_entries_compared': result['original_matrix_entries_compared'],
                      'triple_cases': len(result['three_cubes']), 'coefficient_terms': 263,
                      'rejection_controls': result['rejection_controls'], 'expected_sha256': sha256(raw).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
