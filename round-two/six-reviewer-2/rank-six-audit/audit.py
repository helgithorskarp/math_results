"""Independent exact rank-six audit; six-reviewer-2, mathematical reviewer.

No author modules, solver, floating arithmetic, or assert statements. PSD is
checked by ALL principal minors, not the author's two Schur/Bareiss engines.
Ordinary harmonic exhaustion and the infinite moment argument are in REVIEW.md.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from math import comb, prod, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TABLE_HASH = '39f4fa1c28fadac421ac395a03090c407e0fa9053f08a3041aa4954aab0d6757'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def determinant(A):
    """Row-pivoted rational Gaussian determinant, including empty minor."""
    Z = [list(map(Q, row)) for row in A]
    answer = Q(1)
    for c in range(len(Z)):
        p = next((i for i in range(c, len(Z)) if Z[i][c]), None)
        if p is None:
            return Q(0)
        if p != c:
            Z[p], Z[c] = Z[c], Z[p]
            answer = -answer
        pivot = Z[c][c]
        answer *= pivot
        for i in range(c+1, len(Z)):
            z = Z[i][c]/pivot
            for k in range(c+1, len(Z)):
                Z[i][k] -= z*Z[c][k]
    return answer


def rank(A):
    Z = [list(map(Q, row)) for row in A]
    r = 0
    for c in range(len(Z[0]) if Z else 0):
        p = next((i for i in range(r, len(Z)) if Z[i][c]), None)
        if p is None:
            continue
        Z[p], Z[r] = Z[r], Z[p]
        pivot = Z[r][c]
        for i in range(r+1, len(Z)):
            z = Z[i][c]/pivot
            for k in range(c+1, len(Z[0])):
                Z[i][k] -= z*Z[r][k]
            Z[i][c] = 0
        r += 1
        if r == len(Z):
            break
    return r


MINORS = []


def psd(A, label, expected=None):
    d = len(A)
    need(all(len(row) == d for row in A), 'square '+label)
    need(all(A[i][k] == A[k][i] for i in range(d) for k in range(d)), 'symmetric '+label)
    values = []
    for size in range(1, d+1):
        for ix in combinations(range(d), size):
            value = determinant([[A[i][k] for k in ix] for i in ix])
            need(value >= 0, 'negative principal minor '+label+' '+str(ix))
            values.append(str(value))
    r = rank(A)
    need(expected is None or r == expected, 'rank '+label)
    MINORS.append({'label': label, 'order': d, 'rank': r,
                   'principal_minors': len(values), 'zeros': values.count('0'),
                   'minor_sha256': sha256(json.dumps(values, separators=(',', ':')).encode()).hexdigest()})
    return r


def add(A, B, factor=Q(1)):
    return [[a+factor*b for a, b in zip(row, other)] for row, other in zip(A, B)]


def mul(A, B):
    return [[sum(a*b for a, b in zip(row, col)) for col in zip(*B)] for row in A]


def diag(g):
    return [[Q(g[i] if i == k else 0) for k in range(len(g))] for i in range(len(g))]


def metric(g, A):
    return [[g[i]*v for v in row] for i, row in enumerate(A)]


def inverse_action(A, v):
    n = len(A)
    Z = [list(map(Q, row))+[Q(x)] for row, x in zip(A, v)]
    for i in range(n):
        p = next(k for k in range(i, n) if Z[k][i])
        Z[p], Z[i] = Z[i], Z[p]
        pivot = Z[i][i]
        Z[i] = [x/pivot for x in Z[i]]
        for k in range(n):
            if k != i:
                z = Z[k][i]
                Z[k] = [x-z*y for x, y in zip(Z[k], Z[i])]
    return [row[-1] for row in Z]


def quadratic(A, v):
    return sum(v[i]*a*v[k] for i, row in enumerate(A) for k, a in enumerate(row))


def endpoint(B, T, label):
    """Certify a positive rank-one update and its exact generalized endpoint."""
    psd(B, label+' baseline', len(B))
    psd(T, label+' trade', 1)
    i = next(k for k in range(len(T)) if T[k][k])
    v = [row[i] for row in T]
    q = T[i][i]
    need(T == [[x*y/q for y in v] for x in v], 'rank-one identity '+label)
    w = inverse_action(B, v)
    need([sum(a*x for a, x in zip(row, w)) for row in B] == v, 'inverse witness '+label)
    tau = q/sum(a*b for a, b in zip(v, w))
    psd(add(B, T, -tau), label+' endpoint', len(B)-1)
    need(quadratic(add(B, T, -tau), w) == 0, 'endpoint witness '+label)
    need(quadratic(add(B, T, -2*tau), w) < 0, 'outside witness '+label)
    return tau, {'threshold': str(tau), 'trade_pivot': i, 'trade_diagonal': str(q),
                 'trade_column': list(map(str, v)), 'inverse_witness': list(map(str, w))}


def trade(n, a, b):
    if a == b == 1:
        return (n-2)*(n-3)
    if {a, b} == {1, 2}:
        return -(n-3)
    return int(a == b == 2)


def parameters(n, tables):
    N = sum(comb(n, a) for a in range(7))
    s = sum(comb(n-1, a) for a in range(6))
    if n < 12:
        raw = tables[str(n)]
        need((N, s) == (raw['N'], raw['s']), 'table parameters')
        beta = [[Q(0)]*7]+[[Q(0)]+list(map(Q, row)) for row in raw['weights']]
    else:
        m, h, z = N-1, n*s, sum(a*a*comb(n, a) for a in range(1, 7))
        det = m*z-h*h
        need(det > 0, 'positive moment determinant')
        beta = [[Q(0)]*7]
        for a in range(1, 7):
            beta.append([Q(0)]+[Q(comb(n, b), comb(n-a, b))*(1-Q(s*(z-h*(a+b)+m*a*b), det))
                                     for b in range(1, 7)])
    need(all(beta[a][b] == beta[b][a] for a in range(1, 7) for b in range(1, 7)), 'weight symmetry')
    for a in range(1, 7):
        need(sum(beta[a][b]*choose(n-a, b) for b in range(1, 7)) == N-1-s, 'row affine moment')
        need(sum(b*beta[a][b]*choose(n-a, b) for b in range(1, 7)) == (n-a)*s, 'star affine moment')
        need(all(not beta[a][b] for b in range(1, 7) if a+b > n), 'absent disjoint weights')
    return N, s, Q((n-2)*(n-3)*(2*n-1), 2), beta


def blocks(n, tables):
    N, s, alpha, beta = parameters(n, tables)
    result = []
    for j in range(min(6, n//2)+1):
        aa = list(range(max(1, j), min(6, n-j)+1))
        g = [choose(n-2*j, a-j) for a in aa]
        K = [[Q(s*int(a == b)-choose(n, b)*int(j == 0))
              +(-1)**j*beta[a][b]*choose(n-a-j, b-j) for b in aa] for a in aa]
        U = [[Q(N*int(a == b)-choose(n, b)*int(j == 0))-K[i][k]
              for k, b in enumerate(aa)] for i, a in enumerate(aa)]
        T = [[Q((-1)**j*trade(n, a, b)*choose(n-a-j, b-j)) for b in aa] for a in aa]
        result.append((j, aa, g, K, U, T))
    return result


def projection(g, aa, j):
    G = diag(g)
    if j >= 2:
        return G
    if j == 1:
        return [[G[i][k]-Q(g[i]*g[k], sum(g)) for k in range(len(g))] for i in range(len(g))]
    M = [[sum(ga*a**(u+v) for ga, a in zip(g, aa)) for v in range(2)] for u in range(2)]
    inv = [inverse_action(M, [1, 0]), inverse_action(M, [0, 1])]
    return [[G[i][k]-g[i]*g[k]*sum(Q(aa[i]**u)*inv[v][u]*aa[k]**v for u in range(2) for v in range(2))
             for k in range(len(g))] for i in range(len(g))]


def check_case(n, tables):
    N, s, alpha, beta = parameters(n, tables)
    sectors = blocks(n, tables)
    records, thresholds, witnesses = [], {}, {}
    for j, aa, g, K, U, T in sectors:
        name = str(n)+'/'+str(j)
        d = len(aa)
        need(all(x > 0 for x in g), 'positive metric')
        mult = comb(n, j)-choose(n, j-1)
        rk = d-(2 if j == 0 else 1 if j == 1 else 0)
        psd(metric(g, K), name+' seed lower', rk)
        psd(metric(g, U), name+' seed upper', d)
        P = projection(g, aa, j)
        if n < 12:
            psd(add(metric(g, K), P, -1), name+' projected floor')
            psd(add(metric(g, U), diag(g), -Q(1, 4)), name+' cap floor')
        else:
            psd(add(diag(g), metric(g, K), -Q(1, 2*s)), name+' stable upper')
            if j <= 1:
                psd(add(metric(g, K), P, -s), name+' stable lower')
        ev = alpha if j == 0 else -(n-1)*(n-3) if j == 1 else int(j == 2)
        need(mul(T, T) == [[ev*x for x in row] for row in T], 'trade polynomial')
        if j <= 2:
            psd(metric(g, T), name+' positive trade', 1) if j != 1 else psd(metric(g, [[-v for v in row] for row in T]), name+' negative trade', 1)
        else:
            need(all(not x for row in T for x in row), 'higher trade vanishes')
        forced = ([1]*d, aa) if j == 0 else ([1]*d,) if j == 1 else ()
        need(all(all(sum(x*y for x, y in zip(row, v)) == 0 for row in K) for v in forced), 'forced kernel')
        if j <= 1:
            v = aa if j == 0 else [1]*d
            need(all(sum(x*y for x, y in zip(row, v)) == 0 for row in T), 'trade preserves stars')
        if n < 12 and j <= 2:
            B, R = metric(g, U), metric(g, T)
            if j == 1:
                B = [row[:-1] for row in metric(g, K)[:-1]]
                R = [[-x for x in row[:-1]] for row in metric(g, T)[:-1]]
            tau, witness = endpoint(B, R, name+' exact threshold')
            thresholds[str(j)], witnesses[str(j)] = tau, witness
        records.append({'degree': j, 'layers': aa, 'metric': g, 'multiplicity': mult, 'seed_rank': rk})
    need(sum(len(r['layers'])*r['multiplicity'] for r in records) == N-1, 'complete dimension')
    need(sum(r['seed_rank']*r['multiplicity'] for r in records) == N-n-2, 'seed whole rank')
    if n < 12:
        tau = thresholds['0']
        need(tau < thresholds['1'] and tau < thresholds['2'] and tau > 1/alpha, 'active threshold')
        gap = (1-1/(alpha*tau))/4
    else:
        tau, gap = None, Q(4, 7)
    for t in (1/(16*alpha), 1/(8*alpha), 1/alpha):
        for j, aa, g, K, U, T in sectors:
            name = str(n)+'/'+str(j)+' t='+str(t)
            psd(metric(g, add(K, T, t)), name+' repaired lower', len(aa)-int(j <= 1))
            psd(add(metric(g, add(U, T, -t)), diag(g), -gap), name+' repaired cap gap')
    if tau is not None:
        for j, aa, g, K, U, T in sectors:
            psd(metric(g, add(K, T, tau)), str(n)+'/'+str(j)+' active lower', len(aa)-int(j <= 1))
            psd(metric(g, add(U, T, -tau)), str(n)+'/'+str(j)+' active cap', len(aa)-int(j == 0))
    return {'n': n, 'N': N, 's': s, 'alpha': str(alpha), 'blocks': records,
            'thresholds': {k: str(v) for k, v in thresholds.items()}, 'endpoint_witnesses': witnesses,
            'extended_closed_t': str(1/alpha), 'extended_core_gap': str(gap),
            'whole_lower_rank': N-n, 'whole_upper_rank': N-1,
            'upper_rank_at_active_endpoint': N-2 if tau is not None else None}


def prime_rank(A, p):
    need(all(p % d for d in range(2, isqrt(p)+1)), 'modulus is prime')
    Z = [[v % p for v in row] for row in A]
    r = 0
    for c in range(len(Z[0])):
        pivot = next((i for i in range(r, len(Z)) if Z[i][c]), None)
        if pivot is None:
            continue
        Z[pivot], Z[r] = Z[r], Z[pivot]
        inv = pow(Z[r][c], p-2, p)
        for i in range(r+1, len(Z)):
            f = Z[i][c]*inv % p
            if f:
                for k in range(c+1, len(Z[0])):
                    Z[i][k] = (Z[i][k]-f*Z[r][k]) % p
            Z[i][c] = 0
        r += 1
    return r


def literal_audit(tables):
    n = 8
    N, s, alpha, beta = parameters(n, tables)
    masks = [sum(1 << x for x in ix) for a in range(1, 7) for ix in combinations(range(n), a)]
    sizes = [a.bit_count() for a in masks]
    need(len(masks) == N-1, 'literal vertex count')
    C = [[Q(s*int(i == k)-1)+(beta[a][b] if not (A & B) else 0)
          for k, (B, b) in enumerate(zip(masks, sizes))] for i, (A, a) in enumerate(zip(masks, sizes))]
    D = [[trade(n, a, b) if not (A & B) else 0 for B, b in zip(masks, sizes)] for A, a in zip(masks, sizes)]
    sector = {j: (aa, K, T) for j, aa, g, K, U, T in blocks(n, tables)}
    columns, labels, action_count, vanished = [], [], 0, 0
    for j in range(n//2+1):
        count = 0
        for top in combinations(range(n), j):
            if any(b+1 < 2*(i+1) for i, b in enumerate(top)):
                continue
            used = set(top)
            bottom = []
            for b in top:
                a = next(x for x in range(b) if x not in used)
                bottom.append(a)
                used.add(a)
            count += 1
            h = [prod(int(bool(A & (1 << a)))-int(bool(A & (1 << b))) for a, b in zip(bottom, top)) for A in masks]
            aa, K, T = sector[j]
            for a in range(1, 7):
                if a not in aa:
                    need(not any(v for v, size in zip(h, sizes) if size == a), 'absent lift')
                    vanished += 1
            for k, b in enumerate(aa):
                col = [v if a == b else 0 for v, a in zip(h, sizes)]
                columns.append(col)
                labels.append((j, top, b))
                for i, a in enumerate(sizes):
                    act = sum(v*x for v, x in zip(C[i], col) if x)
                    act_d = sum(v*x for v, x in zip(D[i], col) if x)
                    expected = K[aa.index(a)][k]*h[i] if a in aa else 0
                    expected_d = T[aa.index(a)][k]*h[i] if a in aa else 0
                    need(act == expected and act_d == expected_d, 'literal complete action')
                    action_count += 2
                need(sum(v*v for v in col) == (2**j)*choose(n-2*j, b-j), 'literal lift norm')
        need(count == comb(n, j)-choose(n, j-1), 'complete harmonic top-set count')
    need(len(columns) == N-1, 'square full basis')
    basis = [list(row) for row in zip(*columns)]
    need(prime_rank(basis, 1000003) == N-1, 'exact full-basis independence')
    orthogonality = 0
    for i, (j, top, a) in enumerate(labels):
        for k in range(i):
            l, other, b = labels[k]
            if j != l or a != b:
                need(sum(x*y for x, y in zip(columns[i], columns[k])) == 0, 'orthogonal sectors')
                orthogonality += 1
    whole = []
    for t in (1/(8*alpha), 1/alpha):
        core = add(C, D, t)
        # Definition ECE^T is assembled from the independently built core.
        row_sums = [sum(row) for row in core]
        L = [[1+sum(row_sums)]+[1-v for v in row_sums]]
        L.extend([[1-row_sums[i]]+[1+x for x in row] for i, row in enumerate(core)])
        need(all(sum(row) == N for row in L), 'whole row normalization')
        need(all(L[i][k] == L[k][i] for i in range(N) for k in range(N)), 'whole symmetry')
        for i, A in enumerate([0]+masks):
            for k, B in enumerate([0]+masks):
                a, b = A.bit_count(), B.bit_count()
                if i == k == 0:
                    expected = 1+t*n*(n-1)*(n-2)*(n-3)/4
                elif i == 0 or k == 0:
                    size = a or b
                    expected = 1-t*(n-1)*(n-2)*(n-3)/2 if size == 1 else 1+t*(n-2)*(n-3)/2 if size == 2 else 1
                else:
                    expected = s*int(i == k)+(beta[a][b]+t*trade(n, a, b) if not A & B else 0)
                need(L[i][k] == expected, 'full original-entry formula')
                need(not (A & B) or L[i][k] == s*int(i == k), 'whole H support')
        for point in range(n):
            z = [Q(int(bool(A & (1 << point))))-Q(s, N) for A in [0]+masks]
            need(all(sum(a*b for a, b in zip(row, z)) == 0 for row in L), 'whole centered star')
        digest = sha256(json.dumps([[str(v) for v in row] for row in L], separators=(',', ':')).encode()).hexdigest()
        whole.append({'t': str(t), 'matrix_sha256': digest, 'entries_checked': N*N,
                      'empty_diagonal': str(L[0][0]), 'centered_stars': n})
    return {'n': n, 'basis_columns': len(columns), 'basis_mod_prime': 1000003,
            'basis_rank': N-1, 'operator_action_scalars': action_count,
            'orthogonality_pairs': orthogonality, 'absent_lifts': vanished,
            'whole_matrices': whole}


def run(path=ROOT/'TABLES.json', literal=True):
    MINORS.clear()
    raw = path.read_bytes()
    need(sha256(raw).hexdigest() == TABLE_HASH, 'source table hash')
    obj = json.loads(raw)
    need(set(obj['cases']) == {'8', '9', '10', '11'}, 'complete boundary inputs')
    cases = [check_case(n, obj['cases']) for n in (8, 9, 10, 11, 12, 16, 32)]
    result = {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer',
              'table_sha256': TABLE_HASH, 'cases': cases,
              'literal_audit': literal_audit(obj['cases']) if literal else None,
              'psd_forms': len(MINORS), 'principal_minors': sum(x['principal_minors'] for x in MINORS),
              'principal_minor_transcript_sha256': sha256(json.dumps(MINORS, sort_keys=True,
                                               separators=(',', ':')).encode()).hexdigest()}
    result['uniform_extended_gap'] = str(min(Q(x['extended_core_gap']) for x in cases))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tables', type=Path, default=ROOT/'TABLES.json')
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--blocks-only', action='store_true')
    args = ap.parse_args()
    result = run(args.tables, not args.blocks_only)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: result[k] for k in ('psd_forms', 'principal_minors', 'uniform_extended_gap')}))


if __name__ == '__main__':
    main()
