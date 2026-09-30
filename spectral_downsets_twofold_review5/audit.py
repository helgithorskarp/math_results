#!/usr/bin/env python3
"""six-reviewer-5: independent simple-twofold H audit and v>=9 refinement.

No author code or fixture input. Infinite proof is in REVIEW.md. Dense finite
checks are literal bitmask matrices with rational Schur congruence.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path
from exact import need, poly, add, sub, scale, mul, pmul, integer_record, matvec, rank, psd_rank, controls, determinant3


class Rat:
    """Unreduced rational functions: cross-multiplication, no polynomial gcd."""
    def __init__(self, n, d=(F(1),)):
        self.n = poly(n if isinstance(n, (list, tuple)) else [n])
        self.d = poly(d)
        need(self.d != (F(0),), 'zero symbolic denominator')
    @staticmethod
    def cast(x):
        return x if isinstance(x, Rat) else Rat(x)
    def __add__(self, other):
        z = self.cast(other)
        return Rat(add(mul(self.n, z.d), mul(z.n, self.d)), mul(self.d, z.d))
    __radd__ = __add__
    def __neg__(self):
        return Rat(scale(self.n, -1), self.d)
    def __sub__(self, other):
        return self+-self.cast(other)
    def __rsub__(self, other):
        return self.cast(other)+-self
    def __mul__(self, other):
        z = self.cast(other)
        return Rat(mul(self.n, z.n), mul(self.d, z.d))
    __rmul__ = __mul__
    def __truediv__(self, other):
        z = self.cast(other)
        return Rat(mul(self.n, z.d), mul(self.d, z.n))
    def __rtruediv__(self, other):
        return self.cast(other)/self
    def __pow__(self, k):
        need(isinstance(k, int) and k >= 0, 'polynomial power')
        return Rat(pmul(*[self.n]*k), pmul(*[self.d]*k))
    def equals(self, other):
        z = self.cast(other)
        return mul(self.n, z.d) == mul(z.n, self.d)


def symbolic():
    v = Rat([9, 1])
    s, m, b = 2*v-1, v*(v-1)/2, v*(v-1)/3
    N = 1+v+m+b
    a = Rat(-F(2, 3))
    w = 1+4*v*(2*v-5)/(3*(v-2)*(v-3)*(v-4))
    c = 1+4/(3*(v-2)*(v-3))
    d = (v*v-v-4)/((v-3)*(v-4))
    h = (v*v-7)/((v-3)*(v-4))
    t = (v-1)/(v-4)
    names = []
    def check(name, x, y):
        need(x.equals(y), 'symbolic identity: '+name)
        names.append(name)
    check('triple star', h+(v-4)*d+(v-7)*t, s)
    check('triple row', 1+s+(v-3)*h-3*t+(v-3)*(v-4)*d/2+(v-4)*(v-6)*t/3, N)
    check('pair star', w+(v-3)*c+(v-5)*d, s)
    check('pair row', 1+s+(v-2)*w-2*d+(v-2)*(v-3)*c/2+(v-3)*(v-4)*d/3, N)
    check('point star', a+(v-2)*w-2*d+(v-3)*h-3*t, s)
    check('point row', 1+s+(v-1)*a+(v-1)*(v-2)*w/2-(v-1)*d+(v-1)*(v-3)*h/3-(v-1)*t, N)
    check('pair constant', (s+c)-2*(v-1)*c+(c-1)*m, F(8, 3))
    check('cross constant', 2*d-2*(v-1)*d+(d-1)*b, -F(4, 3))
    check('triple constant', s-t+6*t-3*(v-1)*t+(t-1)*b, 1)
    alpha1, alpha2 = s-c*(v-3), s+c
    check('point-standard eigenvalue', alpha1, (3*v*v-16)/(3*(v-2)))
    beta = t-d*d/alpha2
    gamma = t-4*d*d/(alpha2*(v-2))+d*d*(v-4)**2/((v-2)*alpha1)
    mu = v*(3*v**3-13*v*v+32)/((v-3)*(v-2)*(3*v*v-16))
    check('Schur bound', s-t-(v-3)*(gamma-4*beta/(v-2)), mu)
    check('mu exceeds one', mu-1, 2*(v-4)*(v*v+3*v-12)/((v-3)*(v-2)*(3*v*v-16)))
    delta, k = N-7*v, (v-2)*(v-3)/2
    check('buffer delta', delta, (5*v*v-41*v+6)/6)
    eta = delta/(8*m*k)
    check('repair eta', eta, (5*v*v-41*v+6)/(12*v*(v-1)*(v-2)*(v-3)))
    ap = alpha1-eta*(v-3)
    A = (v-3)*d*d*(v-4)**2/(v-2)
    mup = s-t-(v-3)*(t*(v-6)/(v-2)+d*d*(v-4)**2/((v-2)*ap))
    check('perturbed Schur bound', mup, mu-A*(1/ap-1/alpha1))
    extra = v/3
    T = F(20, 3)*v
    wide_eta = (N-T)/(8*m*k)
    check('improved centered buffer', N-T, delta+extra)
    check('improved repaired buffer', N-T-delta/2, delta/2+extra)
    check('larger repair interval endpoint', wide_eta,
          (5*v*v-39*v+6)/(12*v*(v-1)*(v-2)*(v-3)))
    check('repair interval improvement', wide_eta-eta,
          1/(6*(v-1)*(v-2)*(v-3)))
    check('endpoint repaired buffer', N-T-4*m*k*wide_eta, (N-T)/2)
    np = v+1
    pn = 6*(2*v-1)/(5*v*v+v+6)
    pn1 = 6*(2*np-1)/(5*np*np+np+6)
    check('density strictly decreases', pn-pn1,
          12*(5*v*v-9)/((5*v*v+v+6)*(5*v*v+11*v+12)))
    # Positive coefficient certificates for every integer v>=9; zero constants
    # in sharp weight bounds indicate equality at nine, not strict positivity.
    def nonnegative(name, z):
        need(z.n[0] >= 0 and z.d[0] > 0 and all(x >= 0 for x in z.n+z.d),
             'nonnegative coefficient certificate '+name)
        den = 1
        from math import lcm
        den = lcm(*(x.denominator for x in z.n+z.d))
        return {'numerator_ascending': [int(x*den) for x in z.n],
                'denominator_ascending': [int(x*den) for x in z.d]}
    margins = {
        'w_at_most_61_over_35': Rat(F(61, 35))-w,
        'c_at_most_65_over_63': Rat(F(65, 63))-c,
        'd_at_most_34_over_15': Rat(F(34, 15))-d,
        'h_at_most_37_over_15': Rat(F(37, 15))-h,
        't_at_most_8_over_5': Rat(F(8, 5))-t,
        'alpha1_exceeds_v': alpha1-v,
        'alpha2_exceeds_2v': alpha2-2*v,
        'delta_positive': delta,
        'mu_exceeds_one': mu-1,
        'wide_eta_less_than_half_v_inverse_squared': 1/(2*v*v)-wide_eta,
        'Schur_R_lower_margin': 1-Rat(F(578, 225))/v,
        'repair_Schur_lower_margin': 1-Rat(F(1156, 225))/v,
        'constant_positive_gap': T-(v+10)/3}
    records = {name: nonnegative(name, z) for name, z in margins.items()}
    for name, z in margins.items():
        if not name.startswith(('w_', 'c_', 'd_', 'h_', 't_')):
            need(z.n[0] > 0, 'strict coefficient constant '+name)
    need(99**2-2*70**2 == 1 and 97**2-3*56**2 == 1 and 5**2-6*2**2 == 1,
         'rational square-root bounds')
    comparison = [[F(18, 5), F(866, 525), F(110, 63)],
                  [F(866, 525), F(1136, 567), F(34, 15)],
                  [F(110, 63), F(34, 15), F(25, 9)]]
    margin = [[F(20, 3)*(i == j)-comparison[i][j] for j in range(3)] for i in range(3)]
    minors = [margin[0][0], margin[0][0]*margin[1][1]-margin[0][1]**2, determinant3(margin)]
    need(minors == [F(46, 15), F(86172188, 7441875), F(563250652, 281302875)]
         and all(x > 0 for x in minors) and psd_rank(margin) == 3,
         'fixed rational comparison positive definiteness')
    return {'domain': 'Q[u], v=9+u', 'identity_count': len(names), 'identities': names,
            'nonnegative_coefficient_margins': records,
            'rational_sqrt2_upper': '99/70', 'rational_sqrt3_upper': '97/56',
            'rational_sqrt6_upper': '5/2', 'upper_T': '(20/3)v',
            'fixed_comparison_matrix': [[str(x) for x in row] for row in comparison],
            'comparison_margin_leading_principal_minors': [str(x) for x in minors]}


def mask(points):
    return sum(1 << i for i in points)


def affine_nine():
    return {mask([x+3*y, ((x+dx) % 3)+3*((y+dy) % 3),
                  ((x+2*dx) % 3)+3*((y+2*dy) % 3)])
            for x in range(3) for y in range(3) for dx, dy in [(1, 0), (0, 1), (1, 1), (1, 2)]}


def fixtures():
    A = affine_nine()
    need(len(A) == 12, 'affine nine STS')
    found = None
    for tail in permutations(range(1, 9)):
        perm = (0,)+tail
        B = {mask(perm[i] for i in range(9) if block >> i & 1) for block in A}
        if A.isdisjoint(B):
            found = (perm, B)
            break
    need(found is not None, 'no disjoint relabeling found in bounded construction')
    perm, B = found
    U = A | B
    parallel = {mask(range(3*j, 3*j+3)) for j in range(3)}
    need(parallel <= A, 'parallel class')
    ten = U-parallel
    for block in parallel:
        pts = [i for i in range(9) if block >> i & 1]
        ten.update(mask((9, x, y)) for x, y in combinations(pts, 2))
    # K8 minus the four matching edges through 0 in AG(2,3).
    matching = sorted(block ^ 1 for block in A if block & 1)
    labels = [None]*8
    for i, edge in enumerate(matching):
        pts = [j for j in range(1, 9) if edge >> j & 1]
        labels[i], labels[i+4] = pts
    twelve = U-{block for block in A if not block & 1}
    factors = []
    for new, difference in zip((9, 10, 11), (1, 2, 3)):
        edges = {mask((labels[i], labels[(i+difference) % 8])) for i in range(8)}
        need(len(edges) == 8 and all(sum(bool(e >> x & 1) for e in edges) == 2 for x in range(1, 9)),
             'two-factor')
        factors.append(edges)
        twelve.update(edge | (1 << new) for edge in edges)
    need(len(set.union(*factors)) == 24 and not set.union(*factors) & set(matching), 'factor cover')
    twelve.update(mask((0, x, y)) for x, y in combinations((9, 10, 11), 2))
    twelve.add(mask((9, 10, 11)))
    return [(9, U, 'two disjoint affine STS9'), (10, ten, 'parallel-class replacement'),
            (12, twelve, 'three-point extension through a K8-minus-matching factorization')], list(perm)


def field(v):
    if v == 13:
        plus = lambda x, y: (x+y) % 13
        times = lambda x, y: x*y % 13
    else:
        need(v == 16, 'field fixture order')
        plus = lambda x, y: x ^ y
        def times(x, y):
            r = 0
            while y:
                if y & 1:
                    r ^= x
                y >>= 1
                x <<= 1
                if x & 16:
                    x ^= 19
            return r
    roots = [x for x in range(v) if plus(plus(times(x, x), (v-x) % v if v == 13 else x), 1) == 0]
    need(len(roots) == 2, 'field rho roots')
    rho = roots[0]
    U = {mask((x, plus(x, d), plus(x, times(rho, d)))) for x in range(v) for d in range(1, v)}
    return U, roots


def data(v, blocks):
    need(len(set(blocks)) == len(blocks), 'duplicate block')
    need(all(isinstance(x, int) and 0 < x < 1 << v and x.bit_count() == 3 for x in blocks), 'invalid block')
    pairs = [mask(p) for p in combinations(range(v), 2)]
    containing = {p: [A for A in blocks if A & p == p] for p in pairs}
    need(all(len(A) == 2 and A[0] != A[1] for A in containing.values()), 'pair multiplicity')
    completion = {p: (A[0] ^ p) | (A[1] ^ p) for p, A in containing.items()}
    P = [[int(bool(pair >> i & 1)) for pair in pairs] for i in range(v)]
    B = [[int(bool(A >> i & 1)) for A in blocks] for i in range(v)]
    C = [[int(bool(completion[pair] >> i & 1)) for pair in pairs] for i in range(v)]
    R = [[int(pair & A == pair) for A in blocks] for pair in pairs]
    H = [[sum(1 for pair in pairs if pair & A == pair and not A >> i & 1
              and any(T ^ pair == 1 << i for T in containing[pair])) for A in blocks] for i in range(v)]
    counts = Counter(completion.values())
    Z = [[counts[(1 << i) | (1 << j)]-1 if i != j else 0 for j in range(v)] for i in range(v)]
    need(all(sum(row) == v-1 for mat in (P, B, C, H) for row in mat), 'incidence row sums')
    for mat, expected in [(P, 2), (C, 2), (B, 3), (H, 3), (R, 3)]:
        need(all(sum(row[k] for row in mat) == expected for k in range(len(mat[0]))), 'incidence column sums')
    need(all(sum(row) == 2 for row in R), 'pair block count')
    dot = lambda a, b: sum(x*y for x, y in zip(a, b))
    checks = 0
    for i in range(v):
        for j in range(v):
            need(dot(P[i], P[j]) == (v-2)*(i == j)+1, 'PPt')
            need(dot(B[i], B[j]) == (v-3)*(i == j)+2, 'BBt')
            need(dot(C[i], C[j]) == (v-2)*(i == j)+1+Z[i][j], 'CCt')
            need(dot(P[i], C[j]) == 2*(i != j), 'PCt')
            need(dot(B[i], H[j]) == 3*(i != j)+Z[i][j], 'BHt')
            checks += 5
        for j in range(len(blocks)):
            need(sum(P[i][k]*R[k][j] for k in range(len(pairs))) == 2*B[i][j], 'PR')
            need(sum(C[i][k]*R[k][j] for k in range(len(pairs))) == B[i][j]+H[i][j], 'CR')
            checks += 2
        for k, row in enumerate(R):
            need(dot(row, B[i]) == 2*P[i][k]+C[i][k], 'RBt')
            checks += 1
    need(all(sum(row) == 0 for row in Z), 'Z row sums')
    return pairs, completion, H, counts, checks


def matrices(v, blocks):
    blocks = sorted(blocks)
    pairs, completion, H, counts, checks = data(v, blocks)
    V = sorted({0} | {1 << i for i in range(v)} | set(pairs) | set(blocks))
    N, s = len(V), 2*v-1
    need(N == (5*v*v+v+6)//6, 'downset order')
    den = (v-3)*(v-4)
    weights = {(1, 1): -F(2, 3), (1, 2): 1+F(4*v*(2*v-5), 3*(v-2)*den),
               (1, 3): F(v*v-7, den), (2, 2): 1+F(4, 3*(v-2)*(v-3)),
               (2, 3): F(v*v-v-4, den), (3, 3): F(v-1, v-4)}
    m, k = v*(v-1)//2, (v-2)*(v-3)//2
    delta = F(N-7*v)
    eta = delta/(8*m*k)
    Q, E = [], []
    block_index = {A: i for i, A in enumerate(blocks)}
    for a in V:
        qr, er = [], []
        for b in V:
            if a & b:
                value, change = F(s if a == b else 0), 0
            elif not a or not b:
                value = F(1)
                size = (a | b).bit_count()
                change = m*k if size == 0 else (-(v-1)*k if size == 1 else (k if size == 2 else 0))
            else:
                x, y = (a, b) if a.bit_count() <= b.bit_count() else (b, a)
                sizes = (x.bit_count(), y.bit_count())
                value = weights[sizes]
                if sizes == (1, 1):
                    value += weights[(3, 3)]*(counts[x | y]-1)
                elif sizes == (1, 2):
                    value -= weights[(2, 3)]*int(x | y in block_index)
                elif sizes == (1, 3):
                    value -= weights[(3, 3)]*H[x.bit_length()-1][block_index[y]]
                change = {(1, 1): 2*k, (1, 2): -(v-3), (2, 2): 1}.get(sizes, 0)
            qr.append(value)
            er.append(F(change))
        Q.append(qr)
        E.append(er)
    stars = [[F(bool(A >> i & 1)) for A in V] for i in range(v)]
    need(all(sum(row) == N for row in Q) and all(sum(row) == 0 for row in E), 'Q/E row sums')
    need(all(matvec(Q, x) == [F(s)]*N and matvec(E, x) == [F(0)]*N for x in stars), 'star equations')
    need(max(sum(abs(x) for x in row) for row in E) == 4*m*k, 'full trade row norm')
    Qr = [[x+eta*y for x, y in zip(row, er)] for row, er in zip(Q, E)]
    forced = [[x-F(s, N) for x in row] for row in stars]
    empty = [F(int(A == 0))-F(1, N) for A in V]
    need(rank(forced+[empty]) == v+1, 'centered forced directions')
    need(matvec(Q, empty) == [F(0)]*N and matvec(Qr, empty) != [F(0)]*N, 'empty repair')
    for A in V:
        for B0 in V:
            if A & B0:
                i, j = V.index(A), V.index(B0)
                need(Q[i][j] == Qr[i][j] == (s if A == B0 else 0), 'prescribed diagonal/support')
    return V, Q, Qr, {'v': v, 'N': N, 's': s, 'blocks': len(blocks), 'eta': str(eta),
                      'distinct_completion_pairs': len(counts), 'pair_count': len(pairs),
                      'outside_completion_counts': sorted({x for row in H for x in row}),
                      'incidence_scalar_checks': checks}


def matrix_hash(A, V):
    order = sorted(range(len(V)), key=lambda i: (V[i].bit_count(), V[i]))
    body = json.dumps([[str(A[i][j]) for j in order] for i in order], separators=(',', ':'))
    return hashlib.sha256(body.encode()).hexdigest()


def buffered_slack(Q, gap):
    N = len(Q)
    return [[(N-gap)*(i == j)-Q[i][j]+gap/N for j in range(N)] for i in range(N)]


def finite(v, blocks, label, dense):
    V, Q, Qr, result = matrices(v, blocks)
    N = result['N']
    delta, extra = F(N-7*v), F(v, 3)
    gaps = [delta+extra, delta/2+extra]
    wide_eta = F(5*v*v-39*v+6, 12*v*(v-1)*(v-2)*(v-3))
    eta = F(result['eta'])
    Qwide = [[x+(wide_eta/eta)*(y-x) for x, y in zip(row, repaired)]
             for row, repaired in zip(Q, Qr)]
    result.update({'label': label, 'centered_sha256': matrix_hash(Q, V),
                   'repaired_sha256': matrix_hash(Qr, V), 'dense_PSD_checked': dense,
                   'centered_improved_buffer': str(gaps[0]), 'repaired_improved_buffer': str(gaps[1]),
                   'larger_repair_endpoint': str(wide_eta), 'endpoint_repaired_buffer': str(gaps[0]/2),
                   'endpoint_repaired_sha256': matrix_hash(Qwide, V),
                   'blocks_sha256': hashlib.sha256(json.dumps(sorted(blocks), separators=(',', ':')).encode()).hexdigest()})
    if dense:
        ranks = [psd_rank(Q), psd_rank(buffered_slack(Q, gaps[0])),
                 psd_rank(Qr), psd_rank(buffered_slack(Qr, gaps[1])),
                 psd_rank(Qwide), psd_rank(buffered_slack(Qwide, gaps[0]/2))]
        need(ranks == [N-v-1, N-1, N-v, N-1, N-v, N-1], 'full dense PSD/ranks')
        result['full_centered_upper_original_repair_upper_endpoint_repair_upper_ranks'] = ranks
    return result


def input_controls(blocks):
    bad = [list(blocks)+[next(iter(blocks))], list(blocks)[:-1], list(blocks)+[1], list(blocks)+[1 << 9]]
    rejected = 0
    for U in bad:
        try:
            data(9, U)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('bad design accepted')
    return rejected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', type=Path)
    ap.add_argument('--check', type=Path)
    args = ap.parse_args()
    small, perm = fixtures()
    result = {'agent': 'six-reviewer-5', 'role': 'independent mathematical reviewer',
              'symbolic': symbolic(), 'nine_disjoint_relabeling': perm,
              'finite': [finite(v, U, label, True) for v, U, label in small],
              'PSD_controls': controls(), 'design_inputs_rejected': input_controls(small[0][1])}
    for v in (13, 16):
        U, roots = field(v)
        r = finite(v, U, 'independent equilateral field fixture', v == 13)
        r['field_rho_roots'] = roots
        result['finite'].append(r)
    body = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.write:
        args.write.write_text(body)
    if args.check:
        need(args.check.read_text() == body, 'complete expected summary differs')
    print('Independent twofold audit and v>=9 refinement passed; summary SHA256 '+hashlib.sha256(body.encode()).hexdigest())


if __name__ == '__main__':
    main()
