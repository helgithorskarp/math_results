#!/usr/bin/env python3
"""Independent literal-set/exact-matrix audit by six-reviewer-5.

No imports from the reviewed implementation. Python standard library only.
Finite cases check the implementation bridge; identities.py and REVIEW.md
give the uniform proof. All failures use explicit exceptions, also under -O.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from math import lcm, factorial
import hashlib
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def psd_rank(matrix):
    """Integer Bareiss Schur elimination, including null-pivot row checks."""
    n = len(matrix)
    need(all(len(row) == n for row in matrix), 'square')
    need(all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(i)), 'symmetric')
    den = lcm(*(F(v).denominator for row in matrix for v in row))
    work = [[int(v*den) for v in row] for row in matrix]
    previous, rank = 1, 0
    for k in range(n):
        pivot = work[k][k]
        need(pivot >= 0, 'negative Schur pivot')
        if not pivot:
            need(all(work[k][j] == 0 for j in range(k, n)), 'nonzero null-pivot row')
            continue
        for i in range(k+1, n):
            for j in range(i, n):
                numerator = pivot*work[i][j]-work[i][k]*work[k][j]
                need(numerator % previous == 0, 'Bareiss divisibility')
                work[i][j] = work[j][i] = numerator//previous
        previous, rank = pivot, rank+1
    return rank


def rank(matrix):
    work = [[F(v) for v in row] for row in matrix]
    k = 0
    for j in range(len(work[0])):
        pivot = next((i for i in range(k, len(work)) if work[i][j]), None)
        if pivot is None:
            continue
        work[k], work[pivot] = work[pivot], work[k]
        for i in range(k+1, len(work)):
            if work[i][j]:
                ratio = work[i][j]/work[k][j]
                for col in range(j, len(work[0])):
                    work[i][col] -= ratio*work[k][col]
        k += 1
        if k == len(work):
            break
    return k


def mv(matrix, vector):
    nz = [(j, x) for j, x in enumerate(vector) if x]
    return [sum(row[j]*x for j, x in nz) for row in matrix]


def plus_vectors(vectors, coefficients):
    return [sum(c*v[i] for v, c in zip(vectors, coefficients)) for i in range(len(vectors[0]))]


def order(a):
    return len(a), tuple(sorted(a))


def clique(r, t):
    centers = set(range(r))
    members = [frozenset()] + [frozenset([i]) for i in range(r+t)]
    members += [frozenset(e) for e in combinations(range(r+t), 2) if set(e) & centers]
    return sorted(members, key=order)


def weights(r, t):
    if t >= r-1:
        return dict(AA=F(0), AE=F(0), EE=F(0), AC=-F(r-1, t),
                    CC=-1+F(r*(r-3)*(t-r+1), 2*t*(t-1)),
                    CE=F(t-r+3, t), AX=F(1, t), EX=F(2, t),
                    CX=F((r-2)*(r-1-t), t*(t-1)), XX=F(2*t-2*r+3, t*(t-1)))
    delta = F(t*(t-1), r-1+t*(t-1))
    q = F(2*(r-1-t), (r-1)*(r-2))
    return dict(AA=-1+delta, AE=q, EE=q, AC=F(-1), CC=F(-1),
                CE=F(2, r-1), AX=F(2, r-1)-delta/t,
                EX=F(2, r-1), CX=F(0), XX=delta/(t*(t-1)))


def kind(a, r):
    center_count = len(set(a) & set(range(r)))
    return ('A' if center_count else 'C') if len(a) == 1 else ('E' if center_count == 2 else 'X')


def clique_core(r, t, members):
    p = weights(r, t)
    return [[F(r+t-1) if a == b else F(-1) if a & b else
             p[''.join(sorted((kind(a, r), kind(b, r))))] for b in members] for a in members]


def partition(colors, s):
    return [[F(s*int(a == b)-1) for b in colors] for a in colors]


def proper(members, colors, s, eligible):
    need(all(0 <= c < s for c in colors), 'color range')
    need(all(not a & b or colors[i] != colors[j] for i, a in enumerate(members)
             for j, b in enumerate(members) if i != j), 'proper coloring')
    for point in eligible:
        need(sorted(c for a, c in zip(members, colors) if point in a) == list(range(s)), 'star saturates colors')


def mix(c, p, eps):
    need(0 < eps < 1, 'mixture coefficient')
    return [[(1-eps)*a+eps*b for a, b in zip(row, other)] for row, other in zip(c, p)]


def slack(c, buffer=0):
    n = len(c)+1
    return [[(n-buffer if i == j else 0)-1-c[i][j] for j in range(n-1)] for i in range(n-1)]


def lift(c, s):
    sums = [sum(row) for row in c]
    l = [[1+sum(sums)] + [1-v for v in sums]]
    l += [[1-v]+[1+a for a in row] for v, row in zip(sums, c)]
    n = len(l)
    m = [[(l[i][j]-(s if i == j else 0))/(n-s) for j in range(n)] for i in range(n)]
    return l, m


def digest(matrix):
    return hashlib.sha256(json.dumps([[str(v) for v in row] for row in matrix], separators=(',', ':')).encode()).hexdigest()


def check_lift(members, c, s, eligible, buffer):
    n = len(members)
    need(members[0] == frozenset(), 'empty first')
    need(all(frozenset(b) in members for a in members for size in range(len(a)+1)
             for b in combinations(a, size)), 'downward closure')
    stars = [[F(point in a) for a in members[1:]] for point in eligible]
    need(all(sum(x) == s and not any(mv(c, x)) for x in stars), 'star kernels')
    need(rank(stars) == len(eligible), 'independent stars')
    need(psd_rank(c) == n-1-len(eligible), 'repaired core rank')
    psd_rank(slack(c, buffer))
    l, m = lift(c, s)
    need(psd_rank(l) == n-len(eligible), 'lift rank')
    need(all(sum(row) == 1 for row in m), 'row normalization')
    need(all(m[i][j] == 0 for i, a in enumerate(members) for j, b in enumerate(members) if a & b), 'intersection support')
    need(all(m[i][j] >= 0 for i in range(n) for j in range(n) if i != j), 'off-diagonal sign')
    need(F(s, n-s) < 1, 'rho < 1')
    cap = [[(1 if i == j else 0)-m[i][j] for j in range(n)] for i in range(n)]
    need(psd_rank(cap) == n-1, 'simple upper endpoint')
    return {'N': n, 's': s, 'rank_L': n-len(eligible), 'lower_nullity': len(eligible),
            'buffer': str(buffer), 'empty_diagonal': str(m[0][0]), 'matrix_sha256': digest(m)}, m


def decomposition(r, t, members, c):
    """Full unnormalized rational incidence basis and every column image."""
    p = weights(r, t)
    a, q, e, b, u, v, w, h, z = [p[key] for key in ('AA', 'AE', 'EE', 'CC', 'CE', 'AX', 'EX', 'CX', 'XX')]
    d, ell = r+t-1, r*(r-1)//2
    basis = []

    def block(vectors, gram, metric):
        for j, vector in enumerate(vectors):
            expected = plus_vectors(vectors, [F(gram[i][j], metric[i]) for i in range(len(vectors))])
            need(mv(c, vector) == expected, 'incidence block image')
        basis.extend(vectors)

    # Leaf-standard summands.
    for j in range(1, t):
        y = [int(k == r)-int(k == r+j) for k in range(r, r+t)]
        vc = [sum(y[k-r] for k in member) if kind(member, r) == 'C' else 0 for member in members]
        vx = [sum(y[k-r] for k in member if k >= r) if kind(member, r) == 'X' else 0 for member in members]
        block([vc, vx], [[d-b, -r*(1+h)], [-r*(1+h), r*(t+1-(r-1)*z)]], [1, r])
    # Center-standard blocks; Gram is a connected weighted triangle Laplacian.
    aa, bb, cc = (r-2)*(1+q), t*(1+v), (r-2)*t*(1+w)
    lap = [[aa+bb, -aa, -bb], [-aa, aa+cc, -cc], [-bb, -cc, bb+cc]]
    for i in range(1, r):
        x = [int(k == 0)-int(k == i) for k in range(r)]
        vectors = [[sum(x[k] for k in member if k < r) if kind(member, r) == typ else 0
                    for member in members] for typ in ('A', 'E', 'X')]
        block(vectors, lap, [1, r-2, t])
        for j in range(1, t):
            y = [int(k == r)-int(k == r+j) for k in range(r, r+t)]
            vector = [sum(x[k] for k in member if k < r)*sum(y[k-r] for k in member if k >= r)
                      if kind(member, r) == 'X' else 0 for member in members]
            block([vector], [[d+2+z]], [1])
    # Edge-incidence kernel using rational elimination of B, independently.
    edges = [member for member in members if kind(member, r) == 'E']
    incidence = [[F(i in edge) for edge in edges] for i in range(r)]
    pivots, row = [], 0
    for j in range(ell):
        pivot = next((i for i in range(row, r) if incidence[i][j]), None)
        if pivot is None:
            continue
        incidence[row], incidence[pivot] = incidence[pivot], incidence[row]
        factor = incidence[row][j]
        incidence[row] = [value/factor for value in incidence[row]]
        for i in range(r):
            if i != row:
                factor = incidence[i][j]
                incidence[i] = [a-factor*b for a, b in zip(incidence[i], incidence[row])]
        pivots.append(j)
        row += 1
        if row == r:
            break
    need(len(pivots) == r, 'incidence rank')
    for free in set(range(ell))-set(pivots):
        coeff = {edges[free]: F(1)}
        coeff.update({edges[pivot]: -incidence[i][free] for i, pivot in enumerate(pivots)})
        vector = [coeff.get(member, F(0)) for member in members]
        block([vector], [[d+2+e]], [1])
    # Constant block, Gram=P K P^T in entirely rational coordinates.
    k = [[r*(d+(r-1)*a), r*t*p['AC']], [r*t*p['AC'], ell*t*u]]
    pp = [[1, 0], [0, 1], [0, 1], [-1, -2]]
    gram = [[sum(pp[i][ii]*k[ii][jj]*pp[j][jj] for ii in range(2) for jj in range(2))
             for j in range(4)] for i in range(4)]
    vectors = [[int(kind(member, r) == typ) for member in members] for typ in ('A', 'E', 'C', 'X')]
    block(vectors, gram, [r, ell, t, r*t])
    need(len(basis) == len(members) and rank(basis) == len(members), 'complete independent incidence basis')
    return len(basis)


def clique_case(r, t):
    members, s = clique(r, t), r+t
    c = clique_core(r, t, members[1:])
    need(not any(mv(c, [1]*(len(members)-1))), 'centered core')
    need(psd_rank(c) == len(members)-r-2, 'centered rank')
    psd_rank(slack(c, 1))
    count = decomposition(r, t, members[1:], c)
    colors = [(2*next(iter(a)) if len(a) == 1 else sum(a)) % s for a in members[1:]]
    balanced = len(set(colors.count(i) for i in range(s))) == 1
    if balanced:
        used = {color for a, color in zip(members[1:], colors) if r in a}
        colors[members[1:].index(frozenset([r]))] = next(i for i in range(s) if i not in used)
    proper(members[1:], colors, s, range(r))
    need(len(set(colors.count(i) for i in range(s))) > 1, 'unbalanced partition')
    bound = max(0, s*max(colors.count(i) for i in range(s))-len(members))
    eps = F(1, 2*(bound+1))
    repaired = mix(c, partition(colors, s), eps)
    result, matrix = check_lift(members, repaired, s, range(r), F(1, 2))
    result.update(r=r, t=t, regime=1 if t >= r-1 else 2, incidence_basis=count,
                  epsilon=str(eps), recolored=balanced)
    return result, matrix


def two_case(t):
    members, s = clique(2, t), t+2
    nonempty = members[1:]
    centers = frozenset([0, 1])
    def value(a, b):
        if a == b:
            return F(t+1)
        if a & b:
            return F(-1)
        if len(a) == len(b) == 1:
            x, y = bool(a & centers), bool(b & centers)
            return F(-1) if x and y else -F(1, t) if x or y else -F(t+1, t)
        if len(a) == len(b) == 2:
            return F(2, t)
        single, edge = (a, b) if len(a) == 1 else (b, a)
        return F(2, t) if single & centers else F(t+1, t) if edge == centers else F(0)
    c = [[value(a, b) for b in nonempty] for a in nonempty]
    def average(a, b):
        if a == b:
            return F(t+1)
        if a & b:
            return F(-1)
        big = lambda x: x == centers or len(x) == 1 and not x & centers
        if a <= centers and b <= centers or big(a) and big(b):
            return F(t+1)
        return F(3, t-1) if len(a) == len(b) == 2 else F(-1)
    part = [[average(a, b) for b in nonempty] for a in nonempty]
    if t <= 5:
        total = [[0]*len(nonempty) for _ in nonempty]
        for perm in permutations(range(2, t+2)):
            assign = {frozenset([0]): t+1, frozenset([1]): t+1, centers: t}
            for j, leaf in enumerate(perm):
                assign[frozenset([leaf])] = t
                assign[frozenset([0, leaf])] = j
                assign[frozenset([1, leaf])] = (j+1) % t
            colors = [assign[a] for a in nonempty]
            proper(nonempty, colors, s, range(2))
            pp = partition(colors, s)
            total = [[a+b for a, b in zip(row, other)] for row, other in zip(total, pp)]
        need([[v/factorial(t) for v in row] for row in total] == part, 'expanded leaf average')
    need(psd_rank(c) == len(members)-4 and not any(mv(c, [1]*len(c))), 'two-center baseline')
    psd_rank(slack(c, 1))
    eps = F(1, (t+1)**2)
    repaired = mix(c, part, eps)
    result, matrix = check_lift(members, repaired, s, range(2), F(2, t+1))
    need(matrix[0][0] == -F(2*t, (t+1)**2), 'two-center empty loop')
    need(sum(sum(row) for row in repaired) == F((t-1)**2, t+1) < 3*(t-1), 'partition-hull separation')
    result.update(t=t, averaged_permutations=factorial(t) if t <= 5 else None)
    return result, matrix


def friendship_case(k):
    center = 2*k
    members = [frozenset()]+[frozenset([i]) for i in range(2*k+1)]
    members += [frozenset([center, i]) for i in range(2*k)]
    members += [frozenset([2*i, 2*i+1]) for i in range(k)]
    members.sort(key=order)
    nonempty, s = members[1:], 2*k+1
    def typ(a):
        if a == frozenset([center]):
            return 'a', None
        leaf = min(a-set([center]))
        return ('c' if len(a) == 1 else 'b' if center in a else 'd'), leaf//2
    def value(a, b):
        if a == b:
            return F(2*k)
        if a & b:
            return F(-1)
        ta, ja = typ(a)
        tb, jb = typ(b)
        if 'a' in (ta, tb):
            return F(0)
        if 'b' in (ta, tb):
            return F(-1) if ja == jb else F(1, k-1)
        if ta == tb == 'c':
            return F(k-2) if ja == jb else F(-1)
        return F(0) if ta == tb == 'd' else F(-1)
    c = [[value(a, b) for b in nonempty] for a in nonempty]
    need(psd_rank(c) == len(members)-3 and not any(mv(c, [1]*len(c))), 'friendship baseline')
    psd_rank(slack(c, 1))
    assignment = {frozenset([center]): 2*k}
    for j in range(2*k):
        assignment[frozenset([center, j])] = j
        assignment[frozenset([j])] = j ^ 1
    for i in range(k):
        assignment[frozenset([2*i, 2*i+1])] = 2*k if i == 0 else (2*i+2) % (2*k)
    colors = [assignment[a] for a in nonempty]
    proper(nonempty, colors, s, [center])
    need(sorted(colors.count(i) for i in range(s)) == [2]*(k+2)+[3]*(k-1), 'friendship class sizes')
    eps = F(1, 2*(k+2))
    repaired = mix(c, partition(colors, s), eps)
    result, matrix = check_lift(members, repaired, s, [center], F(1, 2))
    need(matrix[0][0] == -F(1, 2), 'friendship empty loop')
    need(sum(sum(row) for row in repaired) == F(k-1, 2) < (k-1)*(k+2), 'friendship separation')
    result.update(k=k)
    return result, matrix


def tensor_case(a, b):
    ma, mb = a[1], b[1]
    na, nb = len(ma), len(mb)
    n = na*nb
    tensor = [[ma[i//nb][j//nb]*mb[i % nb][j % nb] for j in range(n)] for i in range(n)]
    p = max(F(a[0]['s'], na), F(b[0]['s'], nb))
    s = p*n
    nullity = sum(item[0]['lower_nullity'] for item in (a, b) if F(item[0]['s'], len(item[1])) == p)
    l = [[(n-s)*tensor[i][j]+(s if i == j else 0) for j in range(n)] for i in range(n)]
    cap = [[(1 if i == j else 0)-tensor[i][j] for j in range(n)] for i in range(n)]
    need(psd_rank(l) == n-nullity and psd_rank(cap) == n-1, 'full tensor endpoints')
    need(all(sum(row) == 1 for row in tensor), 'tensor row sums')
    return {'N': n, 's': str(s), 'rank_L': n-nullity, 'lower_nullity': nullity, 'matrix_sha256': digest(tensor)}


def checker_selftest():
    need(psd_rank([[F(1), F(1)], [F(1), F(1)]]) == 1, 'rank-one positive control')
    need(psd_rank([[0, 0, 0], [0, 1, 1], [0, 1, 1]]) == 1, 'skipped null pivot')
    rejected = 0
    for bad in ([[0, 1], [1, 0]], [[1, 2], [2, 1]], [[-1, 0], [0, 1]]):
        try:
            psd_rank(bad)
        except ValueError:
            rejected += 1
    need(rejected == 3, 'indefinite controls rejected')


def fractional_exception():
    """Replay only the credited D_* fixture, not the regular-six census."""
    triple_text = ('123', '124', '135', '245', '345', '236', '146', '346', '156', '256')
    triples = {frozenset(int(i)-1 for i in text) for text in triple_text}
    members = [frozenset(c) for size in range(3) for c in combinations(range(6), size)]
    members += sorted(triples, key=order)
    members.sort(key=order)
    autos = [p for p in permutations(range(6)) if
             {frozenset(p[i] for i in a) for a in triples} == triples]
    need(len(autos) == 60, 'exception automorphisms')
    # Orbit values q=21M, explicitly attributed to CAP_THEOREM.md.
    decode = lambda word: frozenset(i for i in range(6) if word >> i & 1)
    fixture = [(1, 2, F(0)), (1, 6, F(-1)), (1, 12, F(7, 2)),
               (1, 26, F(2)), (3, 12, F(0)), (3, 20, F(3, 2)), (3, 28, F(9, 2))]
    entries = {}
    for a, b, value in fixture:
        aa, bb = decode(a), decode(b)
        orbit = {frozenset([frozenset(p[i] for i in aa), frozenset(p[i] for i in bb)]) for p in autos}
        need(not entries.keys() & orbit, 'exception orbit overlap')
        entries.update({pair: value/21 for pair in orbit})
    required = {frozenset([a, b]) for a, b in combinations(members[1:], 2) if not a & b}
    need(entries.keys() == required, 'exception orbit coverage')
    m = [[F(0)]*32 for _ in range(32)]
    for i, a in enumerate(members[1:], 1):
        for j, b in enumerate(members[1:], 1):
            if a != b and not a & b:
                m[i][j] = entries[frozenset([a, b])]
    for i in range(1, 32):
        m[i][0] = m[0][i] = 1-sum(m[i][1:])
    m[0][0] = 1-sum(m[0][1:])
    need(all(sum(row) == 1 for row in m), 'exception row sums')
    need(all(not a & b or m[i][j] == 0 for i, a in enumerate(members) for j, b in enumerate(members)), 'exception support')
    l = [[21*m[i][j]+(11 if i == j else 0) for j in range(32)] for i in range(32)]
    upper = [[(1 if i == j else 0)-m[i][j] for j in range(32)] for i in range(32)]
    need(psd_rank(l) == 26 and psd_rank(upper) == 31, 'exception endpoint ranks')
    for point in range(6):
        star = [int(point in a) for a in members]
        need(sum(star) == 11 and not any(mv(l, [32*v-11 for v in star])), 'exception centered stars')
    dual = [F(max(0, len(a)-1), 3) for a in members[1:]]
    need(sum(dual) == F(35, 3), 'exception dual total')
    classes, maximum = 0, F(0)
    def disjoint(start, occupied, total):
        nonlocal classes, maximum
        classes += 1
        need(total <= 1, 'exception dual class inequality')
        maximum = max(maximum, total)
        for j in range(start, 31):
            a = members[j+1]
            if not a & occupied:
                disjoint(j+1, occupied | a, total+dual[j])
    disjoint(0, frozenset(), F(0))
    return {'N': 32, 's': 11, 'rank_L': 26, 'upper_slack_rank': 31,
            'automorphisms': 60, 'orbit_pairs': len(entries), 'matrix_sha256': digest(m),
            'dual_weight': '35/3', 'disjoint_classes_including_empty': classes,
            'maximum_class_weight': str(maximum), 'mixed_product_density_lower_bound': '35/96'}


def audit():
    checker_selftest()
    pairs = [(3, 2), (3, 4), (3, 9), (4, 2), (4, 3), (4, 6),
             (5, 2), (5, 3), (5, 4), (5, 7), (6, 2), (6, 4), (6, 5), (7, 3), (9, 2)]
    clique_results = [clique_case(r, t) for r, t in pairs]
    two_results = [two_case(t) for t in (2, 3, 4, 5, 8)]
    friendship_results = [friendship_case(k) for k in (2, 3, 5, 8)]
    tensors = [tensor_case(two_results[0], friendship_results[0]),
               tensor_case(two_results[0], clique_results[0]), tensor_case(two_results[0], two_results[0])]
    # A fresh positive witness for D_(3,3), found by 13-node capacity-limited
    # coloring and checked here directly. No coloring search is a proof input.
    balanced_members = clique(3, 3)
    colors = [0, 5, 5, 0, 2, 1, 1, 2, 3, 4, 5, 0, 2, 3, 4, 4, 1, 3]
    proper(balanced_members[1:], colors, 6, range(3))
    need([colors.count(i) for i in range(6)] == [3]*6, 'balanced proper fixture')
    used = {c for a, c in zip(balanced_members[1:], colors) if 3 in a}
    colors[balanced_members[1:].index(frozenset([3]))] = next(i for i in range(6) if i not in used)
    proper(balanced_members[1:], colors, 6, range(3))
    need(6*sum(colors.count(i)**2 for i in range(6))-18**2 == 12, 'balanced recoloring functional')
    bound = max(0, 6*max(colors.count(i) for i in range(6))-19)
    cc = clique_core(3, 3, balanced_members[1:])
    repaired = mix(cc, partition(colors, 6), F(1, 2*(bound+1)))
    balanced_result, _ = check_lift(balanced_members, repaired, 6, range(3), F(1, 2))
    return {'reviewer': 'six-reviewer-5', 'role': 'independent mathematical reviewer',
            'arithmetic': 'Fraction and integer Bareiss; no researcher imports',
            'clique_centers': [a[0] for a in clique_results], 'two_centers': [a[0] for a in two_results],
            'friendship': [a[0] for a in friendship_results], 'full_tensors': tensors,
            'negative_controls': 3, 'balanced_recoloring_control': balanced_result,
            'credited_fractional_exception': fractional_exception()}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
