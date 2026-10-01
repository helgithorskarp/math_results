#!/usr/bin/env python3
"""Stdlib exact all-order root-layer cap certificate, six-downset-3 researcher."""
from fractions import Fraction as Q
from math import comb, lcm
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re


def require(ok, why):
    if not ok:
        raise ValueError(why)


def integer(s):
    require(type(s) is str and re.fullmatch(r'-?\d+', s), 'integer string required')
    return int(s)


# Sparse Laurent polynomial arithmetic in QQ[X,n,n^-1]. The final
# denominator-cleared object is required to belong to QQ[X,n].
def constant(v):
    return {(0, 0): Q(v)} if v else {}


def add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, Q(0))+v
    return {k: v for k, v in out.items() if v}


def scale(p, v):
    return {k: x*v for k, x in p.items() if x*v}


def multiply(p, q):
    out = {}
    for (a, b), x in p.items():
        for (c, d), y in q.items():
            k = (a+c, b+d)
            out[k] = out.get(k, Q(0))+x*y
    return {k: v for k, v in out.items() if v}


def power(p, k):
    out = constant(1)
    for _ in range(k):
        out = multiply(out, p)
    return out


def identity_polynomial():
    X, n, ni = {(1, 0): Q(1)}, {(0, 1): Q(1)}, {(0, -1): Q(1)}
    N = add(X, scale(n, -1), constant(-1))
    s = add(scale(X, Q(1, 2)), scale(n, -1))
    m = add(X, scale(n, -2), constant(-2))
    e = scale(multiply(n, add(n, constant(-1))), Q(1, 2))
    c = scale(multiply(n, add(power(n, 2), scale(n, -3), constant(4))), Q(1, 4))
    C2 = add(scale(multiply(n, X), Q(1, 4)), scale(c, -2))
    C4 = add(scale(multiply(add(scale(power(n, 2), 3), scale(n, -2)), X), Q(1, 16)),
             scale(add(power(n, 4), multiply(n, power(add(n, constant(-2)), 4))), Q(-1, 8)))
    V = add(multiply(N, add(C2, c)), scale(power(e, 2), -1))
    a = multiply(add(scale(n, 2), constant(5)), power(ni, 2))
    HL = add(m, scale(multiply(power(a, 2), C2), Q(1, 2)),
             scale(multiply(power(a, 4), C4), Q(-1, 8)))
    DL = add(multiply(e, HL), multiply(multiply(N, a), C2))
    HH = add(m, scale(multiply(power(a, 2), C2), 2))
    E = add(multiply(add(N, scale(s, -1)), HH), multiply(m, add(s, scale(m, -1))))
    P = scale(multiply(power(n, 12), add(power(DL, 2), scale(multiply(V, E), -1))), 65536)
    require(all(a >= 0 and b >= 0 and v.denominator == 1 for (a, b), v in P.items()),
            'cleared identity is an integer polynomial')
    return P


def shifted(row, offset):
    return [sum(row[k]*comb(k, j)*offset**(k-j) for k in range(j, len(row)))
            for j in range(len(row))]


def certificate_check(c):
    require(c['denominator_constant'] == '65536' and
            type(c['denominator_n_power']) is int and c['denominator_n_power'] == 12,
            'denominator convention')
    require(type(c['shift']) is int and c['shift'] == 8, 'tail starting point')
    arrays = c['coefficient_arrays']
    require(type(arrays) is list and [len(a) for a in arrays] == [19, 18, 16, 13],
            'all polynomial degrees')
    rows = [[integer(x) for x in row] for row in arrays]
    expected = {(a, b): Q(v) for a, row in enumerate(rows) for b, v in enumerate(row) if v}
    actual = identity_polynomial()
    require(actual == expected, 'complete independent coefficient identity')
    tests = {'c0': rows[0][:], 'c2': rows[2][:],
             'c3_lower': rows[3][:], 'c1_lower': rows[1][:]}
    tests['c3_lower'][12] -= 8192
    tests['c1_lower'][17] += 8192
    counts = {}
    for name, row in tests.items():
        while row and row[-1] == 0:
            row.pop()
        generated = shifted(row, 8)
        claimed = [integer(x) for x in c['positive_shifted_coefficients'][name]]
        require(generated == claimed and all(x > 0 for x in claimed),
                'full shifted positive-coefficient identity: '+name)
        counts[name] = len(claimed)
    require(4**8 > 8**5 and 4*8**5 > 9**5, 'exponential induction base and ratio')
    return {'domain': 'Exact QQ[X,n,n^-1] expansion; cleared result in ZZ[X,n].',
            'coefficient_monomials': len(actual), 'degrees_X_n': [3, 18],
            'positive_shift': 8, 'positive_coefficient_counts': counts,
            'tail_bound': 'P(n,2^n)>=8192*n^12*2^n*(4^n-n^5)>0 for every integern>=8',
            'induction_base': {'4^8': 4**8, '8^5': 8**5,
                               '4*8^5': 4*8**5, '9^5': 9**5}}


def moments(n):
    require(type(n) is int and n >= 4, 'order domain')
    N, s, m = 2**n-n-1, 2**(n-1)-n, 2**n-2*n-2
    e = Q(n*(n-1), 2)
    c = Q(n*(n*n-3*n+4), 4)
    C2 = Q(n*2**(n-2))-2*c
    C4 = Q((3*n*n-2*n)*2**(n-4))-Q(n**4+n*(n-2)**4, 8)
    V = N*(C2+c)-e*e
    a = Q(2*n+5, n*n)
    HL = m+a*a*C2/2-a**4*C4/8
    DL = e*HL+N*a*C2
    HH = m+2*a*a*C2
    E = (N-s)*HH+m*(s-m)
    upper = E-DL*DL/V
    require(V > 0 and C2 >= 0 and HL >= m > 0 and DL > 0, 'moment domain')
    return {'n': n, 'N': N, 's': s, 'm': m, 'e': e, 'c': c, 'C2': C2,
            'C4': C4, 'V': V, 'a': a, 'H_lower': HL, 'D_lower': DL,
            'HH': HH, 'E': E, 'Phi_upper': upper, 'beta': -upper/(2*(N-s))}


def evaluate_polynomial(rows, n, X):
    return sum(X**a*sum(integer(v)*n**b for b, v in enumerate(row))
               for a, row in enumerate(rows))


def finite_moment_controls(c):
    # These controls are supplementary, not the proof of the tail sign.
    records = []
    for n in range(4, 81):
        info = moments(n)
        counts = [comb(n, k) for k in range(n-1)]
        N = sum(counts)
        A = sum(k*counts[k] for k in range(n-1))
        B = sum(k*k*counts[k] for k in range(n-1))
        C2 = sum(comb(n, k)*Q(2*k-n, 2)**2 for k in range(2, n-1))
        C4 = sum(comb(n, k)*Q(2*k-n, 2)**4 for k in range(2, n-1))
        require(N == info['N'] and A == n*info['s'] and N*B-A*A == info['V'],
                'literal full cardinality moments')
        require((C2, C4) == (info['C2'], info['C4']), 'literal middle central moments')
        P = evaluate_polynomial(c['coefficient_arrays'], n, 2**n)
        require(Q(P, 65536*n**12) == info['D_lower']**2-info['V']*info['E'],
                'literal specialization of symbolic identity')
        if n >= 6:
            require(info['Phi_upper'] < 0 < info['beta'], 'finite rational negative constants')
        for k in range(2, n-1):
            z = info['a']*Q(2*k-n, 2)
            radicand = 1+z*z
            require(abs(z) < 1 and radicand-z*z == 1, 'positive reciprocal root domain')
            # In QQ[sqrt(radicand)], h=z+sqrt(radicand) and its
            # complement are a conjugate pair with product one.
            require((2*radicand+2*z*z) == 2+4*z*z, 'exact pair square norm')
            x = z*z
            lower = 1+x/2-x*x/8
            require(lower >= 1 and 1+x-lower*lower == x**3*(8-x)/64 >= 0,
                    'exact Taylor square certificate')
        if n in (6, 7, 8, 11, 14, 16, 32, 80):
            records.append({k: str(info[k]) for k in
                            ('n', 'a', 'V', 'H_lower', 'Phi_upper', 'beta')})
    return {'orders': [4, 80], 'cases': 77,
            'scope': 'Finite moment and radical-domain controls; all-order sign uses the polynomial/induction proof.',
            'selected_rational_constants': records}


def psd_rank(a):
    N = len(a)
    require(N > 0 and all(len(row) == N for row in a), 'PSD shape')
    require(all(a[i][j] == a[j][i] for i in range(N) for j in range(N)), 'PSD symmetry')
    den = lcm(*(Q(x).denominator for row in a for x in row))
    z = [[int(Q(x)*den) for x in row] for row in a]
    previous, rank = 1, 0
    for k in range(N):
        require(all(z[i][i] >= 0 for i in range(k, N)), 'negative Schur diagonal')
        p = next((i for i in range(k, N) if z[i][i] > 0), None)
        if p is None:
            require(all(z[i][j] == 0 for i in range(k, N) for j in range(k, N)),
                    'indefinite zero diagonal')
            break
        if p != k:
            z[k], z[p] = z[p], z[k]
            for row in z:
                row[k], row[p] = row[p], row[k]
        pivot = z[k][k]
        for i in range(k+1, N):
            for j in range(i, N):
                value = pivot*z[i][j]-z[i][k]*z[k][j]
                require(value % previous == 0, 'fraction-free exact division')
                z[i][j] = z[j][i] = value//previous
        for i in range(k+1, N):
            z[i][k] = z[k][i] = 0
        previous, rank = pivot, rank+1
    return rank


def small_capped_baselines():
    result = []
    for n in (4, 5):
        full = (1 << n)-1
        F = [1 << i for i in range(n)]+[A for A in range(1 << n) if 2 <= A.bit_count() <= n-2]
        index = {A: i for i, A in enumerate(F)}
        pairs = [(A, full ^ A) for A in F[n:] if A < (full ^ A)]
        s, N = 2**(n-1)-n, 2**n-n-1
        K = [[Q(s*int(i == j)) for j in range(len(F))] for i in range(len(F))]
        for i in range(n):
            for j in range(i):
                K[i][j] = K[j][i] = s
        for A, B in pairs:
            a, b = index[A], index[B]
            K[a][b] = K[b][a] = s-2
            for i in range(n):
                target = b if A & (1 << i) else a
                K[i][target] = K[target][i] = 2
                for j in range(i):
                    if bool(A & (1 << i)) != bool(A & (1 << j)):
                        K[i][j] -= 2
                        K[j][i] -= 2
        C = [[v-1 for v in row] for row in K]
        totals = [sum(row) for row in C]
        L = [[1+sum(totals)]+[1-x for x in totals]]+[
            [1-totals[i]]+[1+x for x in row] for i, row in enumerate(C)]
        members = [0]+F
        require(all(sum(row) == N for row in L), 'baseline full row sums')
        require(all(L[i][j] == s*int(i == j) for i, A in enumerate(members)
                    for j, B in enumerate(members) if A & B), 'baseline support')
        require(all(not K[i][j] for i, A in enumerate(F) for j, B in enumerate(F)
                    if i != j and i >= n and j >= n and A ^ B != full),
                'complement-only baseline support')
        for point in range(n):
            y = [int(bool(A & (1 << point))) for A in members]
            require(sum(y) == s and all(sum(v*y[j] for j, v in enumerate(row)) == s for row in L),
                    'baseline literal star equations')
        upper = [[N*int(i == j)-v for j, v in enumerate(row)] for i, row in enumerate(L)]
        ranks = [psd_rank(C), psd_rank(L), psd_rank(upper)]
        require(ranks == [N-n-2, N-n-1, N-1], 'baseline exact two-slack PSD ranks')
        result.append({'n': n, 'N': N, 's': s, 'common_pair_weight': '2',
                       'core_lower_rank': ranks[0], 'full_lower_rank': ranks[1], 'upper_rank': ranks[2]})
    return {'attribution': 'Existing complement-only feasibility8154, independently confirmed8196; positive controls only.',
            'cases': result}


def sparse_direction(n, A, B):
    require(min(A.bit_count(), B.bit_count()) >= 2 and not A & B, 'free middle pair')
    K = {}

    def edge(i, j, v):
        K[i, j] = K.get((i, j), 0)+v
        K[j, i] = K.get((j, i), 0)+v

    edge(A, B, 1)
    for i in range(n):
        bit = 1 << i
        if B & bit:
            edge(bit, A, -1)
        if A & bit:
            edge(bit, B, -1)
            for j in range(n):
                if B & (1 << j):
                    edge(bit, 1 << j, 1)
    sums = {}
    for (i, j), v in K.items():
        sums[i] = sums.get(i, 0)+v
    L = dict(K)
    L[0, 0] = sum(sums.values())
    for i, v in sums.items():
        L[0, i] = L[i, 0] = -v
    return {key: value for key, value in L.items() if value}


def derivative_controls():
    output = []
    for n in (6, 7, 11, 16):
        info = moments(n)
        N, s, m = info['N'], info['s'], info['m']
        h = {k: Q(k+1, n-k+1) for k in range(2, n-1)}
        counts = [comb(n, k) for k in range(n-1)]
        A = n*s
        H = sum(counts[k]*h[k] for k in h)
        FH = sum(k*counts[k]*h[k] for k in h)
        tau = (N*FH-A*H)/info['V']
        w = [Q(0), tau]+[k*tau-h[k] for k in range(2, n-1)]
        u = [Q(2 <= k <= n-2)-Q(m, N) for k in range(n-1)]
        HH = sum(counts[k]*h[k]*h[k] for k in h)
        old = (N-s)*HH+m*(s-m)-(N*FH-A*H)**2/info['V']
        total = sum(counts[k]*w[k] for k in range(n-1))
        literal = N*sum(counts[k]*w[k]*w[k] for k in range(n-1))-total*total
        literal += m*(s-m)-s*HH+H*H
        require(literal == old, 'literal full constant for arbitrary reciprocal layers')
        pairs = []
        if n <= 7:
            middle = [A for A in range(1 << n) if 2 <= A.bit_count() <= n-2]
            pairs = [(A, B) for i, A in enumerate(middle) for B in middle[i+1:] if not A & B]
        else:
            pairs = [((1 << a)-1, ((1 << b)-1) << a) for a in range(2, n-1)
                     for b in range(a, n-1) if a+b <= n]
        coefficients = []
        for A, B in pairs:
            direction = sparse_direction(n, A, B)
            vertices = set(i for i, j in direction) | set(j for i, j in direction)
            require(all(i == j == 0 or (i != j and not i & j) for i, j in direction),
                    'literal full derivative support')
            for i in vertices:
                require(sum(v for (a, b), v in direction.items() if a == i) == 0,
                        'literal full derivative row')
                for point in range(n):
                    require(sum(v for (a, b), v in direction.items()
                                if a == i and b & (1 << point)) == 0,
                            'literal full derivative forced stars')
            value = sum(v*(-w[i.bit_count()]*w[j.bit_count()]+u[i.bit_count()]*u[j.bit_count()])
                        for (i, j), v in direction.items())
            expected = 2*(1-h[A.bit_count()]*h[B.bit_count()])
            require(value == expected, 'literal arbitrary-layer dual coefficient')
            coefficients.append([A, B, str(value)])
        output.append({'n': n, 'scope': 'all free coefficients' if n <= 7 else 'all orbit representatives',
                       'derivatives': len(pairs), 'coefficient_sha256': hashlib.sha256(
                           json.dumps(coefficients, separators=(',', ':')).encode()).hexdigest()})
    return output


def pair_count_controls():
    output = []
    for n in range(4, 12):
        full = (1 << n)-1
        seen = {}
        for A in range(1 << n):
            if A.bit_count() < 2:
                continue
            remaining = full ^ A
            B = remaining
            while B:
                if A < B and B.bit_count() >= 2:
                    a, b = sorted((A.bit_count(), B.bit_count()))
                    key = (a, b)
                    seen[key] = seen.get(key, 0)+1
                B = (B-1) & remaining
        expected = {(a, b): comb(n, a)*comb(n-a, b)//(1+int(a == b))
                    for a in range(2, n-1) for b in range(a, n-1) if a+b <= n}
        require(seen == expected, 'complete pair-type multiplicities')
        total = (3**n-(n+2)*2**n+n*n+n+1)//2
        require(sum(seen.values()) == total, 'independent ternary-state total')
        output.append({'n': n, 'free_middle_pairs': total, 'orbits': len(seen)})
    return output


def negative_controls(c):
    names = []

    def reject(name, work):
        try:
            work()
        except (ValueError, ZeroDivisionError):
            names.append(name)
            return
        raise ValueError('corrupt control accepted: '+name)

    for name, field, value in [('wrong_shift', 'shift', 7),
                               ('wrong_denominator_constant', 'denominator_constant', '65535'),
                               ('wrong_denominator_power', 'denominator_n_power', 11)]:
        bad = copy.deepcopy(c)
        bad[field] = value
        reject(name, lambda b=bad: certificate_check(b))
    bad = copy.deepcopy(c)
    bad['coefficient_arrays'][3][12] = '24575'
    reject('changed_symbolic_coefficient', lambda: certificate_check(bad))
    bad = copy.deepcopy(c)
    bad['positive_shifted_coefficients']['c0'][0] = '-1'
    reject('false_positive_tail_certificate', lambda: certificate_check(bad))
    reject('float_coefficient', lambda: integer(0.5))
    reject('decimal_coefficient', lambda: integer('0.5'))
    reject('indefinite_zero_diagonal', lambda: psd_rank([[0, 1], [1, 0]]))
    reject('invalid_order', lambda: moments(3))
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    c = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    result = {'agent': 'six-downset-3', 'role': 'researcher',
              'status': 'Written author-checked unformalized proof, not independently reviewed.',
              'classification': 'For integersn>=4, a capped complement-only H certificate exists iff n=4or5.',
              'polynomial_certificate': certificate_check(c),
              'finite_moment_controls': finite_moment_controls(c),
              'small_capped_baselines': small_capped_baselines(),
              'literal_generic_dual_derivatives': derivative_controls(),
              'complete_pair_count_controls': pair_count_controls(),
              'negative_controls': negative_controls(c)}
    raw = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(raw)
    print(raw, end='')


if __name__ == '__main__':
    main()
