"""Exact bilinear blocks for complements, disjoint2/2 and multiple2/r orbits.

Complete ordinary reduction is in PROOF.md. Exact positivity is a verifier
obligation; block generation alone makes no cap verdict. Author six-downset-3, role researcher.
"""
from fractions import Fraction as F
from math import comb
from matrices import parameters, require, rational


def inverse(a):
    d = len(a)
    rows = [[rational(x) for x in row]+[F(i == j) for j in range(d)]
            for i, row in enumerate(a)]
    require(d and all(len(row) == 2*d for row in rows), 'Inverse shape')
    for j in range(d):
        pivot = next((i for i in range(j, d) if rows[i][j]), None)
        require(pivot is not None, 'Singular inverse')
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [x/scale for x in rows[j]]
        for i in range(d):
            if i != j:
                scale = rows[i][j]
                rows[i] = [x-scale*y for x, y in zip(rows[i], rows[j])]
    result = [row[d:] for row in rows]
    require(all(sum(a[i][k]*result[k][j] for k in range(d)) == (i == j)
                for i in range(d) for j in range(d)), 'Inverse residual')
    return result


def blocks(n, z, epsilon, delta):
    z, epsilon, delta = parameters(n, z, epsilon, delta)
    selected = sorted(delta)
    layers = list(range(2, n-1)); d = len(layers)
    N, s = 2**n-n-1, 2**(n-1)-n
    b = [comb(n, k) for k in layers]
    alpha = [comb(n-2, k-1) for k in layers]
    G0 = [[F(b[i] if i == j else 0)+F(k*l*b[i]*b[j], n)
           +(k-1)*(l-1)*b[i]*b[j] for j, l in enumerate(layers)]
          for i, k in enumerate(layers)]
    G1 = [[F(alpha[i] if i == j else 0)+alpha[i]*alpha[j]
           for j in range(d)] for i in range(d)]
    Q0 = [[F(s*b[i] if i == j else 0)-b[i]*b[j]
           for j in range(d)] for i in range(d)]
    Q1 = [[F(s*alpha[i] if i == j else 0) for j in range(d)]
           for i in range(d)]
    for i, k in enumerate(layers):
        j = layers.index(n-k)
        Q0[i][j] += b[i]*(s-z[k])
        Q1[i][j] -= alpha[i]*(s-z[k])
    Q0[0][0] += comb(n-2, 2)*b[0]*epsilon
    Q1[0][0] -= (n-3)*alpha[0]*epsilon
    for r in selected:
        j = layers.index(r)
        c0 = b[0]*comb(n-2, r)*delta[r]
        c1 = -alpha[0]*comb(n-3, r-1)*delta[r]
        Q0[0][j] += c0; Q0[j][0] += c0
        Q1[0][j] += c1; Q1[j][0] += c1
    inv0, inv1 = inverse(G0), inverse(G1)
    U0 = [[N*b[i]*b[j]*inv0[i][j]-Q0[i][j]
           for j in range(d)] for i in range(d)]
    U1 = [[N*alpha[i]*alpha[j]*inv1[i][j]-Q1[i][j]
           for j in range(d)] for i in range(d)]
    coupled_layers = [2]+selected+[n-r for r in reversed(selected)]+[n-2]
    q = {r: comb(n-4, r-2) for r in selected}
    norms = [1]+[q[r] for r in selected]+[q[r] for r in reversed(selected)]+[1]
    size = len(norms)
    C = [[F(s*norms[i] if i == j else 0) for j in range(size)]
         for i in range(size)]
    C[0][0] += epsilon
    for i, k in enumerate(coupled_layers):
        C[i][size-1-i] += norms[i]*(s-z[k])
    for i, r in enumerate(selected, 1):
        C[0][i] += q[r]*delta[r]
        C[i][0] += q[r]*delta[r]
    U = [[F(N*norms[i] if i == j else 0)-C[i][j] for j in range(size)]
         for i in range(size)]
    return {'Q0': Q0, 'Q1': Q1, 'U0': U0, 'U1': U1, 'C': C, 'U': U}, {
        'n': n, 'N': N, 's': s, 'layers': layers, 'b': b, 'alpha': alpha,
        'G0': G0, 'G1': G1, 'coupled_layers': coupled_layers,
        'coupled_norms': norms,
        'dimensions': {'constants': d, 'point_standard': (n-1)*d,
                       'coupled': size*(comb(n, 2)-n),
                       'selected_remainders': 2*sum(comb(n, r)-comb(n, 2) for r in selected),
                       'other_residuals': sum(comb(n, k)-n for k in layers if k not in coupled_layers)},
    }
