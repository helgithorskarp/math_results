#!/usr/bin/env python3
"""Exact finite controls for the written finite-atomic low-noise theorem.

Python 3.11+, standard library. No numerical Gaussian integration, solver,
floating point, or unrecorded external input. The universal proof is PROOF.md.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import factorial, lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(value, message):
    if not value:
        raise ValueError(message)


def dot(a, b):
    return sum((u*v for u, v in zip(a, b)), F(0))


def difference(a, b):
    return [u-v for u, v in zip(a, b)]


def distances(points):
    return [[dot(difference(a, b), difference(a, b)) for b in points]
            for a in points]


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    r = 0
    for j in range(len(a[0])):
        k = next((k for k in range(r, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        c = a[r][j]
        a[r] = [v/c for v in a[r]]
        for k in range(r+1, len(a)):
            c = a[k][j]
            a[k] = [v-c*w for v, w in zip(a[k], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def ceil_log2(q):
    q = F(q)
    require(q > 0, 'nonpositive logarithm input')
    k = max(0, q.numerator.bit_length()-q.denominator.bit_length())
    while F(2)**k < q:
        k += 1
    while k and F(2)**(k-1) >= q:
        k -= 1
    return k


def parameters(D, b):
    require(type(D) is int and D >= 1, 'D must be a positive integer')
    require(type(b) is int and b >= 1, 'b must be a positive integer')
    M = 2*D+2
    K = 8*D*(D+1)*(2*D+1)
    L = M*b+ceil_log2(2*D)
    return M, K, L


def inspect(x, y, weights, b):
    require(len(x) == len(y) == len(weights) >= 2, 'bad lengths')
    require(all(len(v) == 3 for v in x+y), 'points must be in R3')
    require(all(isinstance(q, F) for v in x+y for q in v), 'exact coordinates required')
    require(all(isinstance(w, F) and w > 0 for w in weights), 'exact positive weights required')
    require(sum(weights) == 1, 'mass is not one')
    require(min(weights) >= F(1, 2**b), 'mass floor fails')
    dx, dy = distances(x), distances(y)
    pairs = list(combinations(range(len(x)), 2))
    require(all(dx[i][j] > 0 for i, j in pairs), 'combine repeated source sites first')
    require(all(dx[i][j] >= dy[i][j] for i, j in pairs), 'not a contraction')
    active = [(i, j) for i, j in pairs if dx[i][j] > dy[i][j]]
    require(active, 'all pair distances are preserved')
    return dx, dy, pairs, active


def certificate(x, y, weights, s, D, b):
    M, K, L = parameters(D, b)
    require(isinstance(s, F) and s > 0, 'exact positive variance required')
    dx, dy, pairs, active = inspect(x, y, weights, b)
    common = {'D': D, 'energy_degree': 2*D+2, 'b': b, 'variance': str(s),
              'active_pairs': len(active), 'tight_pairs': len(pairs)-len(active)}
    if all(dy[i][j] > 0 for i, j in pairs):
        beta = min(min(dy[i][j], dx[i][j]-dy[i][j]) for i, j in active)
        bound = beta/(K*L)
        require(s <= bound, 'distinct-target low-noise condition fails')
        return dict(common, branch='DISTINCT_TARGETS', beta=str(beta),
                    M=M, K=K, L=L, variance_upper_bound=str(bound),
                    conclusion='H_D >= diag(H_D)/2 > 0')
    positive = [d[i][j] for d in [dx, dy] for i, j in pairs if d[i][j] > 0]
    delta = min(positive)
    bound = delta/(108*b*D)
    require(s <= bound, 'collision low-noise condition fails')
    p = F(1, 2**b)
    margin = p**(2*D+2)/(512*(D+1)*(2*D+1)*20**(2*D))
    return dict(common, branch='TARGET_COLLISION', delta=str(delta),
                variance_upper_bound=str(bound), identity_matrix_margin=str(margin),
                conclusion='H_D >= identity_matrix_margin * I > 0')


def compositions(m, n):
    if n == 1:
        yield (m,)
    else:
        for k in range(m+1):
            for rest in compositions(m-k, n-1):
                yield (k,)+rest


def branches(dx, dy, active):
    """Return (A,B,i,j,k), with exponent A/2-B/(2m)."""
    out = []
    for i, j in active:
        c = dy[i][j]
        out.append((c, c, i, j, i))
        for k in range(len(dx)):
            if k in (i, j):
                continue
            a, d = dy[i][k], dy[j][k]
            if a+d < c and dx[i][k] == a and dx[j][k] == d:
                out.append((a+d, 2*(a+d)-c, i, j, k))
    return out


def exponent_controls(x, y, max_m):
    dx, dy = distances(x), distances(y)
    pairs = list(combinations(range(len(x)), 2))
    active = [(i, j) for i, j in pairs if dx[i][j] > dy[i][j]]
    require(active and all(dx[i][j] >= dy[i][j] > 0 for i, j in pairs), 'bad exponent fixture')
    beta = min(min(dy[i][j], dx[i][j]-dy[i][j]) for i, j in active)
    reduced = branches(dx, dy, active)
    require(all(B >= beta for A, B, i, j, k in reduced), 'curvature floor fails')
    for A, B, i, j, k in reduced:
        if k not in (i, j):
            xs = [x[i][r]+x[j][r]-2*x[k][r] for r in range(3)]
            ys = [y[i][r]+y[j][r]-2*y[k][r] for r in range(3)]
            require(B == dot(ys, ys), 'target parallelogram identity fails')
            require(B-dot(xs, xs) == dx[i][j]-dy[i][j], 'loss identity fails')
    den = lcm(*(q.denominator for row in dy for q in row))
    di = [int(dy[i][j]*den) for i, j in pairs]
    li = [dx[i][j]-dy[i][j] for i, j in pairs]
    digest, checked, geometry_checks, rows = sha256(), 0, 0, []
    for m in range(2, max_m+1):
        minimum = None
        for counts in compositions(m, len(x)):
            products = [counts[i]*counts[j] for i, j in pairs]
            if not any(a and loss for a, loss in zip(products, li)):
                continue
            scatter = sum(a*d for a, d in zip(products, di))
            minimum = scatter if minimum is None else min(minimum, scatter)
            checked += 1
            if checked % 113 == 0:
                bary = [sum(counts[i]*y[i][r] for i in range(len(x))) for r in range(3)]
                direct = m*sum(counts[i]*dot(y[i], y[i]) for i in range(len(x)))-dot(bary, bary)
                require(F(scatter, den) == direct, 'direct scatter check fails')
                geometry_checks += 1
        exhaustive = F(minimum, 2*m*den)
        unrestricted = min((dy[i][j]+(m-2)*(dy[i][k]+dy[j][k]))/(2*m)
                           for i, j in active for k in range(len(x)))
        pruned = min(A/2-B/(2*m) for A, B, i, j, k in reduced)
        require(exhaustive == unrestricted == pruned, 'minimum-scatter reduction fails')
        minimizers = [(A, B, i, j, k) for A, B, i, j, k in reduced if A/2-B/(2*m) == pruned]
        for A, B, i, j, k in minimizers:
            n = [0]*len(x); n[i] += 1; n[j] += 1; n[k] += m-2
            mult = factorial(m)
            for v in n:
                mult //= factorial(v)
            require(mult >= m, 'multinomial lower bound fails')
            loss = sum(n[u]*n[v]*(dx[u][v]-dy[u][v]) for u, v in pairs)
            require(loss >= beta, 'scatter-loss floor fails')
        rows.append({'m': m, 'E_m': str(exhaustive),
                     'has_third_site_minimizer': any(k not in (i, j) for A, B, i, j, k in minimizers)})
        digest.update(f'{m}:{exhaustive}\n'.encode())
    return {'active_count_vectors_checked': checked, 'direct_scatter_controls': geometry_checks,
            'surviving_branches': len(reduced), 'beta': str(beta), 'orders': rows,
            'minimum_digest': digest.hexdigest()}


def poly_add(a, b):
    return [(a[i] if i < len(a) else F(0))+(b[i] if i < len(b) else F(0))
            for i in range(max(len(a), len(b)))]


def poly_mul(a, b):
    c = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c


def integrate(poly, a, b):
    return sum(c*(b**(j+1)-a**(j+1))/(j+1) for j, c in enumerate(poly))


def inverse(a):
    n = len(a)
    q = [list(row)+[F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        k = next((k for k in range(j, n) if q[k][j]), None)
        require(k is not None, 'singular matrix')
        q[j], q[k] = q[k], q[j]
        pivot = q[j][j]; q[j] = [v/pivot for v in q[j]]
        for k in range(n):
            if k != j:
                pivot = q[k][j]
                q[k] = [v-pivot*w for v, w in zip(q[k], q[j])]
    return [row[n:] for row in q]


def legendre_controls():
    digest, orthogonality, inverse_entries = sha256(), 0, 0
    for b in [1, 3, 7]:
        p = F(1, 2**b)
        z = [-F(3), 8/p]
        polys = [[F(1)], z]
        for n in range(1, 10):
            part = [F(2*n+1, n+1)*v for v in poly_mul(z, polys[-1])]
            part2 = [-F(n, n+1)*v for v in polys[-2]]
            polys.append(poly_add(part, part2))
        for j, q in enumerate(polys):
            require(sum(map(abs, q)) <= (20/p)**j, 'Legendre coefficient bound fails')
        for i in range(9):
            for j in range(9):
                value = integrate(poly_mul(polys[i], polys[j]), p/4, p/2)
                target = p/(4*(2*i+1)) if i == j else F(0)
                require(value == target, 'Legendre orthogonality fails')
                orthogonality += 1
        for D in range(1, 7):
            Q = [[((p/2)**(i+j+1)-(p/4)**(i+j+1))/(i+j+1)
                  for j in range(D+1)] for i in range(D+1)]
            Qinv = inverse(Q)
            for i in range(D+1):
                for j in range(D+1):
                    value = sum(4*(2*k+1)/p*
                                (polys[k][i] if i <= k else 0)*
                                (polys[k][j] if j <= k else 0)
                                for k in range(D+1))
                    require(value == Qinv[i][j], 'independent inverse identity fails')
                    inverse_entries += 1
            trace = sum(Qinv[i][i] for i in range(D+1))
            bound = 4/p*(D+1)*(2*D+1)*(20/p)**(2*D)
            require(trace <= bound, 'inverse trace bound fails')
            digest.update(f'{b},{D}:{trace}\n'.encode())
    return {'orthogonality_entries': orthogonality, 'inverse_entries': inverse_entries,
            'inverse_trace_digest': digest.hexdigest()}


def scalar_controls():
    count, digest = 0, sha256()
    for i in range(61):
        for j in range(i+1, 61):
            A, B, m = 2*i+2, 2*j+2, i+j+2
            gamma = F(m-1, 2*m)-(F(A-1, 2*A)+F(B-1, 2*B))/2
            formula = F((i-j)**2, 8*(i+1)*(j+1)*(i+j+2))
            require(gamma == formula, 'curvature identity fails')
            require(gamma >= F(1, 8*j*(j+1)*(2*j+1)), 'curvature floor fails')
            # Squaring removes every radical from c_m <= sqrt(c_A*c_B).
            require(m**10*(m-1)**4 >= A**5*B**5*(A-1)**2*(B-1)**2, 'prefactor bound fails')
            count += 1; digest.update(f'{i},{j}:{gamma}\n'.encode())
    budgets = 0
    for D in range(1, 201):
        for b in [1, 2, 3, 7, 8]:
            M, K, L = parameters(D, b)
            require(K*L >= 2*M and K*L <= 288*b*D**4, 'distinct-target budget fails')
            Lc = 9+10*D+(2*D+2)*b+ceil_log2((D+1)**2*(2*D+1))
            require(Lc <= 27*b*D, 'collision budget fails')
            p = F(1, 2**b)
            ratio = 512*(D+1)**2*(2*D+1)*(20/p)**(2*D)/p**2
            require(2**Lc >= ratio, 'collision exponential budget fails')
            budgets += 1
    require(F(44, 7)**3 < 256, 'Gaussian normalization bound fails')
    require(F(1)/(1-F(3, 8)) < 2, 'cube exponential bound fails')
    return {'curvature_prefactor_controls': count, 'budget_controls': budgets,
            'scalar_digest': digest.hexdigest()}


def collision_controls(x, y, weights):
    dx, dy = distances(x), distances(y)
    pairs = list(combinations(range(len(x)), 2))
    delta = min(d[i][j] for d in [dx, dy] for i, j in pairs if d[i][j])
    groups = {}
    for point, weight in zip(y, weights):
        key = tuple(point)
        groups[key] = groups.get(key, F(0))+weight
    checked, digest = 0, sha256()
    for m in range(2, 7):
        zero = [F(0), F(0)]; total = F(0)
        for n in compositions(m, len(x)):
            mult = factorial(m)
            for k in n:
                mult //= factorial(k)
            probability = F(mult)
            for w, k in zip(weights, n):
                probability *= w**k
            total += probability
            for r, d in enumerate([dx, dy]):
                scatter = sum(n[i]*n[j]*d[i][j] for i, j in pairs)
                if scatter == 0:
                    zero[r] += probability
                else:
                    require(scatter >= (m-1)*delta, 'collision residual scatter bound fails')
            checked += 1
        require(total == 1, 'replica probabilities do not sum to one')
        require(zero[0] == sum(w**m for w in weights), 'source zero-scatter grouping fails')
        require(zero[1] == sum(w**m for w in groups.values()), 'target zero-scatter grouping fails')
        require(zero[1] > zero[0], 'merger power gain is not positive')
        digest.update(f'{m}:{zero[0]},{zero[1]}\n'.encode())
    # Direct merger hinges, without Gaussian integration; the cube bound
    # and the universal inequality are proved in the text.
    hinge_checks = 0
    for q in [F(1, 2), F(3, 5), F(1)]:
        for t in [F(1, 512), F(3, 1024), F(1, 256)]:
            gap = sum(max(W*q-t, 0) for W in groups.values())
            gap -= sum(max(w*q-t, 0) for w in weights)
            require(gap >= t, 'merger hinge margin fails')
            hinge_checks += 1
    return {'count_vectors_checked': checked, 'target_groups': len(groups),
            'zero_scatter_digest': digest.hexdigest(), 'hinge_controls': hinge_checks}


def fixtures():
    core = [[F(0), F(0), F(0)], [F(2), F(0), F(0)],
            [F(1), F(2), F(0)], [F(1, 2), F(1, 3), F(3)]]
    centers = [[F(7, 6), F(7, 9), F(1)], [F(1, 2), F(7, 9), F(1)],
               [F(5, 6), F(1, 9), F(1)]]
    normals = [[F(1), F(1, 2), F(4, 9)], [-F(1), F(1, 2), F(1, 9)],
               [F(0), -F(1), F(1, 9)]]
    x, y = [v[:] for v in core], [v[:] for v in core]
    for p, n, r in zip(centers, normals, [20, 30, 40]):
        x.append([u+r*v for u, v in zip(p, n)])
        y.append([u-r*v for u, v in zip(p, n)])
    oblique = (x, y, [F(1, 8)]*4+[F(1, 4), F(1, 8), F(1, 8)], 3)
    vs = [[F(v) for v in row] for row in [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]]
    tetra = (vs+[[-20*u for u in v] for v in vs],
             vs+[[F(58, 3)*u for u in v] for v in vs],
             [F(2**i, 255) for i in range(8)], 8)
    triangle = ([[F(-1),F(0),F(0)],[F(1),F(0),F(0)],[F(0),F(0),F(0)]],
                [[-F(4,5),F(3,5),F(0)],[F(4,5),F(3,5),F(0)],[F(0),F(0),F(0)]],
                [F(1,3)]*3, 2)
    collision_x = [[F(0)]*3]
    for j, r in enumerate([1,2,3]):
        for sign in [-1,1]:
            v = [F(0)]*3; v[j] = F(sign*r); collision_x.append(v)
    collision = (collision_x, [[abs(v) for v in a] for a in collision_x],
                 [F(2**i,127) for i in range(7)], 7)
    return {'oblique_rank_six': oblique, 'eight_site_benchmark': tetra,
            'third_site_dominant': triangle, 'collision_rank_six': collision}


def rejected_controls(data, bound):
    x, y, w, b = data
    expanded = [v[:] for v in y]; expanded[0] = [F(10**6),F(0),F(0)]
    tests = [lambda: certificate(x,y,w,bound*F(1000001,1000000),5,b),
             lambda: certificate(x,y,w,bound,5,b-1),
             lambda: certificate(x,expanded,w,bound,5,b),
             lambda: certificate(x,x,w,bound,5,b),
             lambda: certificate(x,y,w,F(0),5,b),
             lambda: certificate(x,y,w,-bound,5,b),
             lambda: certificate(x,y,w,bound,0,b),
             lambda: certificate(x,y,w,bound,5,0),
             lambda: certificate(x,y,w[:-1]+[F(0)],bound,5,b),
             lambda: certificate(x,y,[F(1,7)]*6+[F(2,7)],bound,5,b),
             lambda: certificate([x[0]]*len(x),y,w,bound,5,b)]
    for test in tests:
        try:
            test()
        except ValueError:
            continue
        raise RuntimeError('A damaged input passed')
    return len(tests)


def reproduce():
    data = fixtures(); records = {}; counts = 0
    for name, (x, y, w, b) in data.items():
        dx, dy, pairs, active = inspect(x, y, w, b)
        collided = any(dy[i][j] == 0 for i,j in pairs)
        if collided:
            delta = min(d[i][j] for d in [dx,dy] for i,j in pairs if d[i][j])
            bound = delta/(108*b*5)
        else:
            beta = min(min(dy[i][j],dx[i][j]-dy[i][j]) for i,j in active)
            M,K,L = parameters(5,b); bound = beta/(K*L)
        joined = [a+c for a,c in zip(x,y)]
        joined_rank = rank([difference(v, joined[0]) for v in joined[1:]])
        record = {'source': [[str(q) for q in v] for v in x],
                  'target': [[str(q) for q in v] for v in y],
                  'weights': list(map(str,w)), 'paired_affine_rank': joined_rank,
                  'boundary_certificate': certificate(x,y,w,bound,5,b)}
        if not collided:
            minimum = min(dy[i][j] for i,j in pairs)
            record['all_nearest_target_pairs_tight'] = all(dx[i][j] == minimum for i,j in pairs if dy[i][j] == minimum)
            record['exponent_controls'] = exponent_controls(x,y,8 if len(x)>3 else 12)
            counts += record['exponent_controls']['active_count_vectors_checked']
        else:
            record['collision_controls'] = collision_controls(x, y, w)
        records[name] = record
    require(records['oblique_rank_six']['all_nearest_target_pairs_tight'], 'oblique nearest pair is shortened')
    require(records['eight_site_benchmark']['all_nearest_target_pairs_tight'], 'benchmark nearest pair is shortened')
    require(records['oblique_rank_six']['paired_affine_rank'] == 6, 'oblique rank fails')
    require(records['collision_rank_six']['paired_affine_rank'] == 6, 'collision rank fails')
    require(dot(difference(data['oblique_rank_six'][0][1], data['oblique_rank_six'][0][0]),
                difference(data['oblique_rank_six'][0][3], data['oblique_rank_six'][0][2])) != 0,
            'tetrahedron unexpectedly orthocentric')
    third = records['third_site_dominant']['exponent_controls']['orders']
    require(all(row['has_third_site_minimizer'] for row in third), 'third-site control fails')
    require(all(F(row['E_m']) == 1-F(18,25*row['m']) for row in third), 'third-site exponent formula fails')
    return {'status': 'FINITE_ATOMIC_LOW_NOISE_EXCLUSION_EXACT_PASS',
            'headline_status': 'OPEN: no full Gaussian majorisation or KP consequence',
            'fixtures': records, 'active_count_vectors_checked': counts,
            'legendre_controls': legendre_controls(), 'scalar_controls': scalar_controls(),
            'damaged_controls_rejected': rejected_controls(data['oblique_rank_six'], F(records['oblique_rank_six']['boundary_certificate']['variance_upper_bound'])),
            'trust_boundary': 'Finite exact controls supplement the universal written proof. No finite control is an exhaustive check of all measures, contractions, variances, or polynomial orders.'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--write-expected', action='store_true')
    args = ap.parse_args()
    text = json.dumps(reproduce(), indent=2)+'\n'
    if args.write_expected:
        (ROOT/'EXPECTED.json').write_text(text)
    if args.check:
        require(text == (ROOT/'EXPECTED.json').read_text(), 'expected output mismatch')
    print(text, end='')


if __name__ == '__main__':
    main()
