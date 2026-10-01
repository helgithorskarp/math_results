"""Reviewer two: exact definition-level audit, no author imports by default.

CPython 3.11+, standard library. Optional --producer names the pinned author
affine_pendant_completion.py; this bridge compares entries AFTER own checks.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import ceil
from pathlib import Path
import argparse
import importlib.util
import json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def mv(A, v):
    return [dot(r, v) for r in A]


def digest(A):
    return sha256(json.dumps([[str(x) for x in row] for row in A],
                             separators=(',', ':')).encode()).hexdigest()


def psd(A):
    """Exact symmetric Schur elimination, including zero-pivot rows."""
    m = len(A)
    need(all(len(row) == m for row in A), 'square')
    need(all(A[i][j] == A[j][i] for i in range(m) for j in range(m)), 'symmetric')
    T = [list(map(F, row)) for row in A]
    rank = 0
    for k in range(m):
        q = T[k][k]
        need(q >= 0, 'negative Schur pivot')
        if q == 0:
            need(all(T[k][j] == 0 for j in range(k+1, m)), 'nonzero zero-pivot row')
            continue
        rank += 1
        for i in range(k+1, m):
            for j in range(i, m):
                T[i][j] -= T[k][i]*T[k][j]/q
                T[j][i] = T[i][j]
    return rank


def shifted(A, q, sign=1):
    return [[q*int(i == j)+sign*A[i][j] for j in range(len(A))]
            for i in range(len(A))]


def parts(D, c):
    bit = 1 << c
    old = D[1:]
    S = [i for i, a in enumerate(old) if a & bit]
    B = [i for i, a in enumerate(old) if not a & bit]
    return old, S, B


def affine(D, C, c):
    old, S, B = parts(D, c)
    n = len(S)
    need(n >= 3 and len(B) >= n-1, 'geometry')
    need(all(sum(row) == 0 for row in C), 'center')
    need(mv(C, [F(int(i in S)) for i in range(len(old))]) == [0]*len(old), 'star')
    for i, a in enumerate(old):
        need(C[i][i] == n-1, 'diagonal')
        for j, z in enumerate(old):
            need(C[i][j] == C[j][i], 'symmetry')
            if i != j and a & z:
                need(C[i][j] == -1, 'intersection')


def pendant(D, c):
    t = 1 << max(D).bit_length()
    return sorted(D+[t, t | (1 << c)]), t


def seed(D, c):
    old, S, B = parts(D, c)
    s, b = len(S), len(B)
    need(s >= 3, 'seed star')
    center = old.index(1 << c)
    A = [[F(s-1) if i == j else F(-bool(a & z))
          for j, z in enumerate(old)] for i, a in enumerate(old)]
    for j in B:
        A[center][j] = A[j][center] = F(sum(bool(old[i] & old[j]) for i in S))
    q, r = [j for j in B if old[j].bit_count() == 1][:2]
    tune = F(s-b-sum(map(sum, A)), 2)
    A[q][r] += tune
    A[r][q] += tune
    rows = list(map(sum, A))
    E, t = pendant(D, c)
    z = t | (1 << c)
    index = {a: i for i, a in enumerate(old)}
    T = [[F(0) for _ in E[1:]] for _ in E[1:]]
    for i, a in enumerate(E[1:]):
        for j, d in enumerate(E[1:]):
            if a == d:
                v = F(s)
            elif a & d:
                v = F(-1)
            elif t in (a, d):
                x = d if a == t else a
                v = -rows[index[x]]+int(x == (1 << c)) if index[x] in S else -rows[index[x]]-1
            elif z in (a, d):
                v = F(1, b)
            else:
                v = A[index[a]][index[d]]
                if (a == (1 << c) and index[d] in B) or (d == (1 << c) and index[a] in B):
                    v -= F(1, b)
            T[i][j] = v
    affine(E, T, c)
    return E, T


def step(D, C, c):
    """Iterative entry update; no closed history or author lift code."""
    old, S, B = parts(D, c)
    n, b = len(S), len(B)
    E, t = pendant(D, c)
    z = t | (1 << c)
    index = {a: i for i, a in enumerate(old)}
    a, beta = 1-F(1, n*b), 1-F(1, b)
    out = []
    for x in E[1:]:
        row = []
        for y in E[1:]:
            if x == y:
                v = F(n)
            elif x & y:
                v = F(-1)
            elif z in (x, y):
                v = F(1, b)
            elif t in (x, y):
                v = F(1, n) if (y if x == t else x) & (1 << c) else -F(n, b)
            else:
                i, j = index[x], index[y]
                if (i in S) != (j in S):
                    v = a*(C[i][j]+1)-1
                elif i in B:
                    v = beta*(C[i][j]+1)-1
                else:
                    v = F(-1)
            row.append(v)
        out.append(row)
    affine(E, out, c)
    return E, out


def norm_profile(D, C, c):
    old, S, B = parts(D, c)
    n, b = len(S), len(B)
    R = max(sum(abs(x) for x in row) for row in C)
    a = max(sum(abs(C[i][j]) for j in B) for i in S)
    d = max(sum(abs(C[i][j]) for i in S) for j in B)
    p = 0
    while F(p*p) < a*d:
        p += 1
    P = min(R, F(p))
    T = min(R+n, max(sum(abs(C[i][j]-n*int(i == j)+F(n, b)) for j in B) for i in B))
    return n, b, R, P, T


def counts(D, C, c):
    n, b, R, P, T = norm_profile(D, C, c)
    A = F(1)
    first = None
    for u in range(1, ceil(2*R+n)+1):
        A *= 1-F(1, (n+u-1)*(b+u-1))
        B = F(b-1, b+u-1)
        if u >= 2 and u >= B*T and u*(u-B*T) >= A*A*P*P:
            if first is None:
                first = u
            need(u >= first, 'monotonicity')
        elif first is not None:
            raise ValueError('scalar criterion lost at larger count')
    need(first is not None, 'termination')
    return dict(n=n, b=b, R=R, P=P, T=T, decay=first,
                improved_row=ceil(R+n), original_row=ceil(2*R+n))


def lift(D, C, c, eps):
    old, S, B = parts(D, c)
    n, N = len(S), len(D)
    newest = 1 << (max(D).bit_length()-1)
    other = next(a for a in old if not a & (1 << c) and a.bit_count() == 1)
    q, r = old.index(newest), old.index(other)
    T = [row[:] for row in C]
    T[q][r] += eps
    T[r][q] += eps
    rows, total = list(map(sum, T)), sum(map(sum, T))
    # Direct empty entries of the lift, followed by the definition of M.
    L = [[F(1)+total]+[F(1)-x for x in rows]]
    L += [[F(1)-rows[i]]+[F(1)+x for x in row] for i, row in enumerate(T)]
    M = [[(L[i][j]-n*int(i == j))/(N-n) for j in range(N)] for i in range(N)]
    need(all(sum(row) == 1 for row in M), 'H row sums')
    need(all(M[i][j] == 0 for i, a in enumerate(D) for j, z in enumerate(D) if a & z), 'H support')
    lower = [[(N-n)*M[i][j]+n*int(i == j) for j in range(N)] for i in range(N)]
    upper = [[F(int(i == j))-M[i][j] for j in range(N)] for i in range(N)]
    need(psd(lower) == N-1 and psd(upper) == N-1, 'whole endpoint ranks')
    star = [F(int(bool(a & (1 << c))))-F(n, N) for a in D]
    need(mv(lower, star) == [0]*N and mv(upper, [F(1)]*N) == [0]*N, 'exact endpoint kernels')
    need(min(M[0][1:]) >= F(1, 2*(N-n)), 'empty margin')
    return M


def complete_case(label, D, c, selector='decay', generic=None, producer=None):
    original = D[:]
    preprocess = 0
    if generic is None:
        while len(parts(D, c)[1]) < 3:
            D, _ = pendant(D, c)
            preprocess += 1
        initial, C = seed(D, c)
    else:
        initial, C = D[:], [r[:] for r in generic]
        affine(initial, C, c)
    initial_C = [r[:] for r in C]
    profile = counts(initial, C, c)
    u = profile[selector]
    E = initial[:]
    for _ in range(u):
        E, C = step(E, C, c)
    N, n = len(E), len(parts(E, c)[1])
    old, S, B = parts(E, c)
    Pz = [[F(int(i == j))-F(int(i in S and j in S), len(S))
           -F(int(i in B and j in B), len(B)) for j in range(N-1)] for i in range(N-1)]
    need(psd(C) == N-3, 'raw rank')
    psd([[C[i][j]-profile['n']*Pz[i][j] for j in range(N-1)] for i in range(N-1)])
    psd([[F(N*int(i == j)-1)-C[i][j]-int(i == j)
          for j in range(N-1)] for i in range(N-1)])
    eps = min(F(1, 2), F(profile['n'], 2*(len(B)+2)))
    M = lift(E, C, c, eps)
    eps2 = min(F(1, 2), F(profile['n'], len(B)+2))
    wider = lift(E, C, c, eps2)
    if producer is not None:
        if generic is None:
            aD, aC, _ = producer.centered_seed(D, c)
            need(aD == initial and aC == initial_C, 'all author seed entries')
        aE, entry, _ = producer.compile_history(initial, initial_C, c, u)
        need(aE == E and [[entry(a, z) for z in E[1:]] for a in E[1:]] == C, 'all author closed raw entries')
        if generic is None and selector == 'decay':
            aE, entry, _ = producer.completion(original, c, threshold='decay')
            need(aE == E and [[entry(a, z) for z in E] for a in E] == M, 'all author final entries')
    return dict(label=label, original=original, center=c, selector=selector,
                preprocessing=preprocess, seed_N=len(initial),
                profile={k: str(v) if isinstance(v, F) else v for k, v in profile.items()},
                further_pendants=u, N=N, s=n, raw_rank=N-3,
                lower_rank=N-1, upper_rank=N-1, epsilon=str(eps), wider_epsilon=str(eps2),
                matrix_sha256=digest(M), wider_matrix_sha256=digest(wider),
                complete_raw_entries=(N-1)**2, complete_final_entries=N*N)


def damping_controls():
    checked = 0
    for cross in product((-1, 0, 1), repeat=4):
        for y in ((1, 1, 1), (-1, -1, -1), (-1, 0, 1)):
            H = [[F(0), F(0), F(cross[0]), F(cross[1])],
                 [F(0), F(0), F(cross[2]), F(cross[3])],
                 [F(cross[0]), F(cross[2]), F(y[0]), F(y[1])],
                 [F(cross[1]), F(cross[3]), F(y[1]), F(y[2])]]
            q = F(0)
            while True:
                try:
                    psd(shifted(H, q)); psd(shifted(H, q, -1))
                    break
                except ValueError:
                    q += F(1, 2)
                    need(q <= 5, 'damping source bound guard')
            for A, B in ((F(1), F(0)), (F(0), F(1)), (F(1, 3), F(2, 3)), (F(2, 3), F(1, 3))):
                T = [[(B if i >= 2 and j >= 2 else A)*H[i][j] for j in range(4)] for i in range(4)]
                psd(shifted(T, q)); psd(shifted(T, q, -1)); checked += 2
    # With a nonzero first diagonal block, contraction need not hold.
    H = [[F(1), F(1)], [F(1), F(-1)]]
    psd(shifted(H, F(3, 2))); psd(shifted(H, F(3, 2), -1))
    try:
        psd(shifted([[F(1), F(1)], [F(1), F(0)]], F(3, 2), -1))
    except ValueError:
        rejected = True
    else:
        raise ValueError('missing zero-block control not rejected')
    return dict(zero_block_matrices=243, complete_scaled_slacks=checked,
                nonzero_first_block_counterexample_rejected=rejected)


def run(producer):
    records = []
    families = 0
    for mask in range(1 << 8):
        D = [a for a in range(8) if mask >> a & 1]
        if len(D) < 2 or D[0] != 0 or any(z not in D for a in D for z in range(8) if z & a == z):
            continue
        families += 1
        sizes = [sum(bool(a & (1 << c)) for a in D) for c in range(3)]
        for c in range(3):
            if sizes[c] == max(sizes):
                records.append(complete_case('three-point-'+str(mask), D, c, producer=producer))
    need(families == 18 and len(records) == 33, 'complete three-point input domain')
    records.append(complete_case('V-improved-row', [0, 1, 2, 3, 4, 5], 0,
                                 'improved_row', producer=producer))
    # Smallest permitted affine geometry: n=3, b=2, not a preliminary seed.
    D = [0, 1, 2, 3, 4, 5]
    old, S, B = parts(D, 0)
    cross = {(3, 2): -1, (3, 4): 1, (5, 2): 1, (5, 4): -1}
    C = []
    for i, a in enumerate(old):
        row = []
        for j, z in enumerate(old):
            if i == j:
                v = F(2)
            elif i in S and j in S:
                v = F(-1)
            elif i in B and j in B:
                v = F(-2)
            else:
                x, y = (a, z) if i in S else (z, a)
                v = F(cross.get((x, y), 0))
            row.append(v)
        C.append(row)
    records.append(complete_case('minimum-n3-b2', D, 0, generic=C, producer=producer))
    # Signed affine boundary cores outside the author's preliminary recipe.
    D = [0, 1, 2, 3, 4, 5, 8, 9]
    old, S, B = parts(D, 0)
    for t in (F(0), F(5), F(-5)):
        C = [[F(3) if i == j else F(-1) if i in S and j in S else
              F(-3, 2) if i in B and j in B else F(0)
              for j in range(7)] for i in range(7)]
        for i in S:
            if old[i] == 1:
                continue
            for j in B:
                C[i][j] = C[j][i] = F(-1) if old[i] & old[j] else F(1, 2)
        # Disjoint rectangle: old star {c},{c,2}, outside {4},{8}.
        for a, z, sign in ((1, 4, 1), (1, 8, -1), (3, 4, -1), (3, 8, 1)):
            i, j = old.index(a), old.index(z)
            C[i][j] += sign*t; C[j][i] += sign*t
        affine(D, C, 0)
        rec = complete_case('signed-boundary-'+str(t), D, 0, generic=C, producer=producer)
        if t:
            v = [F(int(a == 1)-int(a == 4)) for a in old]
            if t < 0:
                v = [F(int(a == 1)+int(a == 4)) for a in old]
            need(dot(v, mv(C, v)) == -4, 'indefinite generic seed control')
            rec['seed_negative_form'] = '-4'
        records.append(rec)
    return dict(agent='six-reviewer-2', role='independent mathematical reviewer',
                labeled_three_point_families=families, maximum_center_cases=33,
                records=records, damping_controls=damping_controls())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--producer', type=Path)
    ap.add_argument('--write-expected', action='store_true')
    args = ap.parse_args()
    producer = None
    if args.producer:
        pin = json.loads(Path(__file__).with_name('INPUT.json').read_text())
        expected_hash = pin['sources'][0]['files']['affine_pendant_completion.py']
        need(sha256(args.producer.read_bytes()).hexdigest() == expected_hash,
             'producer file does not match the reviewed source pin')
        spec = importlib.util.spec_from_file_location('pinned_author', args.producer)
        producer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(producer)
    result = run(producer)
    result['canonical_sha256'] = sha256(json.dumps(result, sort_keys=True,
                                       separators=(',', ':')).encode()).hexdigest()
    path = Path(__file__).with_name('expected.json')
    if args.write_expected:
        path.write_text(json.dumps(result, sort_keys=True, indent=1)+'\n')
    else:
        need(result == json.loads(path.read_text()), 'complete frozen evidence differs')
    print(json.dumps(dict(canonical_sha256=result['canonical_sha256'],
                         complete_cases=len(result['records']),
                         damping_controls=result['damping_controls']), sort_keys=True))


if __name__ == '__main__':
    main()
