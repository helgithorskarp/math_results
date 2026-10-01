"""six-reviewer-2: exact independent linear-pendant audit and boundary repair.

Default: no producer imports. Build from a Schur-factorized Gram matrix,
compare a separate edge assembly, check complete rational slacks and buffers.
The all-order proofs are in REVIEW.md, not consequences of finite sampling.
Exact Schur arithmetic is reused from this reviewer's published pass38 and
is again checked against all principal minors on 729 ternary 3x3 matrices.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product, permutations
from pathlib import Path
import argparse
import importlib.util
import json
import sys


def need(ok, message):
    if not ok:
        raise ValueError(message)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def mv(A, v):
    return [dot(row, v) for row in A]


def digest(obj):
    return sha256(json.dumps(obj, sort_keys=True, separators=(',', ':'),
                             default=str).encode()).hexdigest()


def psd(A):
    n = len(A)
    need(all(len(row) == n for row in A), 'square')
    need(all(A[i][j] == A[j][i] for i in range(n) for j in range(n)), 'symmetric')
    T = [list(map(F, row)) for row in A]
    rank = 0
    for k in range(n):
        pivot = T[k][k]
        need(pivot >= 0, 'negative Schur pivot')
        if not pivot:
            need(all(T[k][j] == 0 for j in range(k+1, n)), 'nonzero zero-pivot row')
            continue
        rank += 1
        for i in range(k+1, n):
            for j in range(i, n):
                T[i][j] -= T[k][i]*T[k][j]/pivot
                T[j][i] = T[i][j]
    return rank


def geometry(D, c):
    need(isinstance(D, (list, tuple)) and len(D) >= 2, 'nontrivial input')
    need(all(type(a) is int and a >= 0 for a in D), 'integer masks')
    need(list(D) == sorted(set(D)) and D[0] == 0, 'sorted distinct with empty')
    present = set(D)
    for a in D:
        bit = a
        while bit:
            low = bit & -bit
            need(a ^ low in present, 'immediate downset deletion')
            bit ^= low
    d = max(D).bit_length()
    need(type(c) is int and 0 <= c < d, 'active integer center')
    S = [a for a in D if a >> c & 1]
    E = [a for a in D if not a >> c & 1]
    need(len(S) == max(sum(a >> j & 1 for a in D) for j in range(d)),
         'maximum coordinate')
    need(1 <= len(S) <= len(E), 'deletion injection bound')
    return S, E, d


def construct(D, c, r=None, boundary=False):
    S, E, d = geometry(D, c)
    s, t = len(S), len(E)
    r = t if boundary and r is None else t+1 if r is None else r
    need(type(r) is int, 'integer pendant count')
    need((t > s and r == t) if boundary else r > t, 'recipe domain')
    need(r >= 2, 'two fresh indices')
    P = [1 << (d+i) for i in range(r)]
    Z = [p | (1 << c) for p in P]
    groups = S+Z+E+P
    family = sorted(groups)
    k, b, n, delta = s+r, t+r, len(groups), t-s
    need(n <= 64, 'explicit finite dense-check order limit')
    u, v = F(1, r), F(k, b*r)
    # Row balance independently defines w, rather than its expanded formula.
    w = (1-t*v)/(r-1)
    y, mu = F(r-t, r*(r-1)), F(delta, b)
    need(w == F(r*r-s*t, b*r*(r-1)) and min(u, v, w) > 0, 'cross weight')
    X = [[F(0)]*t+[u]*r for _ in S]
    X += [[v]*t+[w*int(i != j) for j in range(r)] for i in range(r)]
    need(all(sum(row) == 1 for row in X), 'cross row balance')
    need(all(sum(X[i][j] for i in range(k)) == F(k, b) for j in range(b)),
         'cross column balance')
    psi = k-delta*y-(b*w)**2/k
    coefficient = F(k*t*(r-t), r)
    z = [F(1, t)]*t+[-F(1, r)]*r
    PE = [[F(int(i == j and i < t))-F(int(i < t and j < t), t)
           for j in range(b)] for i in range(b)]
    PP = [[F(int(i == j and i >= t))-F(int(i >= t and j >= t), r)
           for j in range(b)] for i in range(b)]
    Q = [[k*PE[i][j]+psi*PP[i][j]+coefficient*z[i]*z[j]
          for j in range(b)] for i in range(b)]
    XX = [[sum(X[h][i]*X[h][j] for h in range(k)) for j in range(b)]
          for i in range(b)]
    # The base is reconstructed from its complete Schur Gram factorization.
    L = [[F(k*int(i == j)) if i < k and j < k else
          b*X[i][j-k] if i < k else b*X[j][i-k] if j < k else
          Q[i-k][j-k]+F(b*b, k)*XX[i-k][j-k]
          for j in range(n)] for i in range(n)]
    grouped_M0 = [[(L[i][j]-k*int(i == j))/b for j in range(n)] for i in range(n)]
    loc = {a: i for i, a in enumerate(groups)}
    M0 = [[grouped_M0[loc[a]][loc[e]] for e in family] for a in family]
    index = {a: i for i, a in enumerate(family)}
    literal = [[F(0)]*n for _ in family]
    def edge(a, e, weight):
        literal[index[a]][index[e]] = literal[index[e]][index[a]] = weight
    for a in S:
        for p in P:
            edge(a, p, u)
    for i, spoke in enumerate(Z):
        for a in E:
            edge(spoke, a, v)
        for j, p in enumerate(P):
            if i != j:
                edge(spoke, p, w)
    for a in E:
        for p in P:
            edge(a, p, mu/r)
    for i in range(r):
        for j in range(i):
            edge(P[i], P[j], mu*y)
    need(M0 == literal, 'complete Gram versus edge assembly')
    need(all(M0[i][j] >= 0 for i in range(n) for j in range(n)), 'raw nonnegative')
    h = 2*min(u, v, w)/(n-1)**2
    B = 2*s+4*(t-1 if boundary else b-2)
    R = [[F(0)]*n for _ in family]
    def change(a, e, amount):
        R[index[a]][index[e]] += amount
        if a != e:
            R[index[e]][index[a]] += amount
    for a in S:
        for x, e, amount in [(0, a, 1), (Z[0], P[1], 1),
                              (a, P[1], -1), (Z[0], 0, -1)]:
            change(x, e, amount)
    # The boundary repair deliberately omits all P/P triangular trades.
    for a in E[1:]+([] if boundary else P[1:]):
        for x, e, amount in [(0, a, 1), (0, P[0], 1), (P[0], a, -1), (0, 0, -2)]:
            change(x, e, amount)
    if boundary:
        lam, tau = F(8, 15), F(4*s*k, t*(3*s+t))
        epsilon = min(tau*lam/(4*b*B*B), v/(2*s), u/2, mu/(2*t))
    else:
        epsilon = min(F(1, 15*b*B), h/(2*B), v/(2*s), u/2)
        if delta:
            epsilon = min(epsilon, mu/(2*r), mu*y/2)
    M = [[M0[i][j]+epsilon*R[i][j] for j in range(n)] for i in range(n)]
    meta = dict(original_N=len(D), original_s=s, t=t, r=r, k=k, b=b, N=n,
                delta=delta, u=u, v=v, w=w, y=y, mu=mu, upper_gap=h,
                repair_bound=B, epsilon=epsilon, psi=psi)
    return family, S+Z, E, P, M0, R, M, Q, meta


def census(D, S):
    if len(D) > 20:
        return None
    values = D[1:]
    maximum, maximizers, count = 0, [], 0
    def visit(start, chosen):
        nonlocal maximum, maximizers, count
        count += 1
        if len(chosen) > maximum:
            maximum, maximizers = len(chosen), [chosen]
        elif len(chosen) == maximum:
            maximizers.append(chosen)
        for j in range(start, len(values)):
            if all(values[j] & a for a in chosen):
                visit(j+1, chosen+(values[j],))
    visit(0, ())
    need(maximum == len(S) and maximizers == [tuple(sorted(S))], 'maximum equality census')
    return dict(intersecting_subfamilies=count, maximum=maximum, maximizers=1)


def audit(D, c, r=None, boundary=False, producer=None, boundary_producer=None):
    family, S, E, P, M0, R, M, Q, m = construct(D, c, r, boundary)
    n, k, b, s, t = (m[key] for key in ['N', 'k', 'b', 'original_s', 't'])
    one = [F(1)]*n
    q = [F(b if a in S else -k) for a in family]
    qnorm = dot(q, q)
    Pone = [[F(int(i == j))-F(1, n) for j in range(n)] for i in range(n)]
    PZ = [[Pone[i][j]-q[i]*q[j]/qnorm for j in range(n)] for i in range(n)]
    need(sum(q) == 0, 'orthogonal constants')
    for A in [M0, M]:
        need(mv(A, one) == one and mv(A, q) == [-F(k, b)*x for x in q], 'endpoints')
        need(all(A[i][j] == A[j][i] for i in range(n) for j in range(n)), 'symmetry')
        need(all(A[i][j] == 0 for i, a in enumerate(family)
                 for j, e in enumerate(family) if a & e), 'actual set support')
    need(mv(R, one) == mv(R, q) == [0]*n, 'repair constants')
    need(max(sum(map(abs, row)) for row in R) <= m['repair_bound'], 'repair norm')
    need(min(M[0][1:]) >= m['epsilon'] > 0, 'positive empty margin')
    negative = sum(M[i][j] < 0 for i in range(1, n) for j in range(i+1, n))
    if m['delta']:
        need(negative == 0, 'nonempty nonnegative')
    lower0 = [[b*M0[i][j]+k*int(i == j) for j in range(n)] for i in range(n)]
    lower = [[b*M[i][j]+k*int(i == j) for j in range(n)] for i in range(n)]
    need(psd(lower) == n-1, 'final whole lower rank')
    for A, upper_gap in [(M0, m['upper_gap']),
                         (M, m['epsilon'] if boundary else m['upper_gap']/2)]:
        cap = [[F(int(i == j))-A[i][j] for j in range(n)] for i in range(n)]
        need(psd(cap) == n-1, 'whole cap rank')
        need(psd([[cap[i][j]-upper_gap*Pone[i][j] for j in range(n)]
                  for i in range(n)]) == n-1, 'whole constant-orthogonal cap buffer')
    if boundary:
        need(psd(Q) == b-2 and psd(lower0) == n-2, 'boundary extra kernel rank')
        original_star = set(a for a in D if a >> c & 1)
        vextra = [F(2, k) if a in original_star else -F(2*s, k*t) if a in S else
                  F(1, t) if a in E else -F(1, t) for a in family]
        vn = dot(vextra, vextra)
        need(vn == F(2*(3*s+t), k*t) and dot(vextra, q) == sum(vextra) == 0,
             'extra kernel norm and orthogonality')
        need(mv(lower0, vextra) == [0]*n, 'exact extra kernel')
        lam, tau = F(8, 15), F(4*s*k, t*(3*s+t))
        need(dot(vextra, mv(R, vextra)) == F(8*s, t*t) == tau*vn, 'lift quadratic')
        oldR = [row[:] for row in R]
        ix = {a: i for i, a in enumerate(family)}
        for a in P[1:]:
            for x, e, amount in [(0, a, 1), (0, P[0], 1), (P[0], a, -1), (0, 0, -2)]:
                oldR[ix[x]][ix[e]] += amount
                if x != e:
                    oldR[ix[e]][ix[x]] += amount
        old_mass = dot(vextra, mv(oldR, vextra))
        need(old_mass == F(8*(1-m['delta']), t*t) and
             (old_mass < 0 or (old_mass == 0 and any(mv(oldR, vextra)))),
             'old all-outside repair obstruction')
        Ppositive = [[PZ[i][j]-vextra[i]*vextra[j]/vn for j in range(n)]
                     for i in range(n)]
        need(psd([[lower0[i][j]-lam*Ppositive[i][j] for j in range(n)]
                  for i in range(n)]) == n-2, 'complete boundary positive gap')
        need(b*m['epsilon']*m['repair_bound'] <= lam/2, 'boundary positive block')
        need(2*(b*m['epsilon']*m['repair_bound'])**2/lam <=
             b*m['epsilon']*tau/2, 'boundary coupled Schur bound')
        need(b*m['epsilon']*m['repair_bound'] <= lam/4 and
             2*b*m['epsilon']*m['repair_bound']**2/tau <= lam/2,
             'improved complete Young bounds')
        lower_gap = b*m['epsilon']*tau/2
        need(psd([[lower[i][j]-lower_gap*PZ[i][j] for j in range(n)]
                  for i in range(n)]) == n-1, 'whole improved boundary lower buffer')
        old_epsilon = min(tau*lam/(8*b*m['repair_bound']**2), m['v']/(2*s),
                          m['u']/2, m['mu']/(2*t))
        need(m['epsilon'] == 2*old_epsilon, 'all-input doubled boundary repair')
        author_M = [[M0[i][j]+old_epsilon*R[i][j] for j in range(n)] for i in range(n)]
        author_lower = [[b*author_M[i][j]+k*int(i == j) for j in range(n)] for i in range(n)]
        author_cap = [[F(int(i == j))-author_M[i][j] for j in range(n)] for i in range(n)]
        need(psd(author_lower) == psd(author_cap) == n-1, 'whole author boundary ranks')
        need(psd([[author_lower[i][j]-b*old_epsilon*tau/2*PZ[i][j] for j in range(n)]
                  for i in range(n)]) == n-1, 'whole author boundary lower buffer')
        need(psd([[author_cap[i][j]-old_epsilon*Pone[i][j] for j in range(n)]
                  for i in range(n)]) == n-1, 'whole author boundary upper buffer')
        need(min(author_M[0][1:]) >= old_epsilon > 0 and
             all(author_M[i][j] >= 0 for i in range(n) for j in range(i+1, n)),
             'author boundary sign/margin')
        if boundary_producer:
            z = boundary_producer.completion(D, c)
            need(z['family'] == family and boundary_producer.dense_entries(z, 'raw') == M0 and
                 boundary_producer.dense_entries(z, 'repair') == R and
                 boundary_producer.dense_entries(z) == author_M,
                 'complete independent boundary producer bridge')
            need(z['epsilon'] == old_epsilon and z['lower_gap'] == b*old_epsilon*tau/2,
                 'boundary producer scalar bridge')
        m.update(extra_kernel_norm2=vn, extra_kernel_lift=tau, raw_positive_gap=lam,
                 improved_lower_gap=lower_gap, author_epsilon=old_epsilon,
                 author_final_sha256=digest(author_M), author_lower_gap=lower_gap/2,
                 old_repair_extra_quadratic=old_mass)
    else:
        need(m['psi'] > 1 and k*(1-F(t*t, m['r']**2)) > 1, 'sharper contrasts')
        need(psd(Q) == b-1, 'whole Schur rank')
        need(psd([[Q[i][j]-(F(int(i == j))-F(1, b)) for j in range(b)]
                  for i in range(b)]) == b-1, 'whole sharper Schur buffer')
        for A, gap in [(lower0, F(1, 3)), (lower, F(4, 15))]:
            need(psd([[A[i][j]-gap*PZ[i][j] for j in range(n)]
                      for i in range(n)]) == n-1, 'complete sharper lower gap')
        if producer:
            z = producer.completion(D, c, m['r'])
            need(z['family'] == family and producer.dense_entries(z, 'raw') == M0 and
                 producer.dense_entries(z, 'repair') == R and producer.dense_entries(z) == M,
                 'complete independent producer bridge')
            for key in ['u', 'v', 'w', 'y', 'mu', 'epsilon']:
                need(z[key] == m[key], 'producer scalar bridge')
    result = {key: str(value) if isinstance(value, F) else value for key, value in m.items()}
    result.update(original_family=list(D), center=c, boundary=boundary,
                  lower_rank=n-1, upper_rank=n-1, raw_lower_rank=n-2 if boundary else n-1,
                  empty_margin=str(min(M[0][1:])), negative_nonempty_edges=negative,
                  schur_sha256=digest(Q), raw_sha256=digest(M0),
                  repair_sha256=digest(R), final_sha256=digest(M),
                  intersecting_census=census(family, S))
    return result


def fixtures():
    inputs, records = [], []
    for mask in range(1 << 8):
        D = [a for a in range(8) if mask >> a & 1]
        if len(D) < 2 or 0 not in D:
            continue
        if any(a ^ (1 << j) not in D for a in D for j in range(3) if a >> j & 1):
            continue
        inputs.append(D)
        maximum = max(sum(a >> c & 1 for a in D) for c in range(3))
        records += [(D, c, None) for c in range(3) if sum(a >> c & 1 for a in D) == maximum]
    need(len(inputs) == 18 and len(records) == 33, 'complete labeled three-bit census')
    for E0, E1 in [([0, 1, 2, 4, 5], [0, 2, 4]),
                   ([a for a in range(16) if a.bit_count() <= 2], [0, 1, 2, 4, 8])]:
        records.append((sorted([a << 1 for a in E0]+[(a << 1) | 1 for a in E1]), 0, None))
    records += [([0, 1, 2, 3, 4, 5], 0, 5), ([0, 1, 8, 16, 17, 24], 4, 6)]
    boundary = [(D, c, None) for D, c, _ in records[:35]
                if len(D) > 2*sum(a >> c & 1 for a in D)]
    need(len(boundary) == 20, 'strict boundary fixture count')
    boundary += [(list(range(15)), 0, None), ([0, 1, 8, 16], 4, None)]
    return records, boundary


def backend_audit():
    def determinant(A):
        n, answer = len(A), 0
        for p in permutations(range(n)):
            term = (-1)**sum(p[i] > p[j] for i in range(n) for j in range(i+1, n))
            for i in range(n):
                term *= A[i][p[i]]
            answer += term
        return answer
    passed = 0
    for entries in product((-1, 0, 1), repeat=6):
        a, b, c, d, e, f = entries
        A = [[a, b, c], [b, d, e], [c, e, f]]
        exact = all(determinant([[A[i][j] for j in range(3) if mask >> j & 1]
                                 for i in range(3) if mask >> i & 1]) >= 0
                    for mask in range(1, 8))
        try:
            psd(A)
            checked = True
        except ValueError:
            checked = False
        need(exact == checked, 'principal-minor backend disagreement')
        passed += checked
    need(passed == 24, 'PSD backend census')
    return dict(matrices=729, psd=passed, criterion='all seven principal minors')


def reject_controls():
    controls = [lambda: construct([0], 0), lambda: construct([0, True], 0),
                lambda: construct([0, 1, 3, 4], 0), lambda: construct([0, 1, 1], 0),
                lambda: construct([0, 1, 2], True), lambda: construct([0, 1, 2], 2),
                lambda: construct([0, 1, 2, 3, 4], 2), lambda: construct([0, 1], 0, True),
                lambda: construct([0, 1], 0, 1), lambda: construct([0, 1], 0, 2.0),
                lambda: construct([0, 1], 0, boundary=True),
                lambda: construct([0, 1, 2], 0, 1, boundary=True),
                lambda: psd([[0, 1], [1, 0]]), lambda: psd([[1, 1], [0, 1]]),
                lambda: psd([[-1]])]
    for control in controls:
        try:
            control()
        except ValueError:
            pass
        else:
            raise ValueError('domain/corruption control accepted')
    # D={empty,c} plus one pendant has two independent maximum stars.
    a, b = [F(-1), F(1), F(-1), F(1)], [F(-1), F(-1), F(1), F(1)]
    need(dot(a, a)*dot(b, b)-dot(a, b)**2 > 0, 'one-pendant exceptional obstruction')
    return len(controls)


def load_producer(directory, boundary=False):
    directory = Path(directory).resolve()
    manifest = json.loads(Path(__file__).with_name('PROVENANCE.json').read_text())
    for record in manifest['boundary_target_pins' if boundary else 'target_pins']:
        raw = (directory/record['name']).read_bytes()
        need(len(raw) == record['bytes'] and sha256(raw).hexdigest() == record['sha256'],
             'pinned target bytes')
    sys.path.insert(0, str(directory))
    spec = importlib.util.spec_from_file_location('review2_boundary_producer' if boundary else
                                                'review2_pinned_producer', directory/
                                                ('boundary_pendant_completion.py' if boundary else
                                                 'linear_pendant_completion.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--producer', metavar='PINNED_DIRECTORY')
    parser.add_argument('--boundary-producer', metavar='PINNED_DIRECTORY')
    args = parser.parse_args()
    producer = load_producer(args.producer) if args.producer else None
    boundary_producer = load_producer(args.boundary_producer, boundary=True) if args.boundary_producer else None
    main_cases, boundary_cases = fixtures()
    original = [audit(D, c, r, producer=producer) for D, c, r in main_cases]
    boundary = [audit(D, c, r, boundary=True, boundary_producer=boundary_producer)
                for D, c, r in boundary_cases]
    columns = sorted(set().union(*(row.keys() for row in original+boundary)))
    result = dict(agent='six-reviewer-2', role='independent mathematical reviewer',
                  scope='finite implementation evidence; all-order proofs are separate',
                  independent_representation='Schur-factorized Gram plus literal edge/trade assembly',
                  main_cases=len(original), boundary_cases=len(boundary),
                  final_matrix_checks=len(original)+2*len(boundary),
                  backend=backend_audit(), rejected_controls=reject_controls(),
                  record_columns=columns,
                  original=[[row.get(key) for key in columns] for row in original],
                  boundary=[[row.get(key) for key in columns] for row in boundary])
    result['canonical_sha256'] = digest(result)
    if args.check:
        expected = json.loads(Path(__file__).with_name('RESULTS.json').read_text())
        need(result == expected, 'whole frozen output differs')
    if producer:
        print('Hash-pinned producer bridge: all 37 raw/repair/final matrices and scalars agree.',
              file=sys.stderr)
    if boundary_producer:
        print('Hash-pinned boundary producer bridge: all 22 raw/repair/author-final matrices agree.',
              file=sys.stderr)
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
