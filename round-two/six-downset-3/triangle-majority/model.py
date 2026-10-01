"""Exact disjoint weights and the proved S3 x Sq sector forms; see PROOF.md."""
from fractions import Fraction as F
from poly import R

TYPES = ((0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0))


def formula(q):
    if not isinstance(q, (F, R)):
        raise TypeError('formula parameter must be Fraction or an exact rational function')
    s, kappa = 3*q+4, F(1, 2)
    k = kappa/(3*q+5)
    alpha1, beta1 = 1-1/q, 1+1/q
    alpha2 = 1+2*k/(q*(q-1))
    beta2 = 1+2*(k+(q-1)**2/q)/((q-1)*(q-2))
    gamma1 = 1+6/q
    gamma2 = 1+6/q-6*k*(q+1)/(q*(q-1))
    outside11 = (kappa+(gamma1-1)+q-(s-q))/(q-1)
    outside12 = q/(q-2)-2*q/((q-1)*(q-2))
    outside22 = (kappa+(gamma2-1)+2*q/(q-1)-s+q*(q-1)/2)/((q-2)*(q-3)/2)
    result = {}
    def put(a, b, v):
        result[tuple(sorted((a, b)))] = v
    o, p, a, b, c, d, e = TYPES
    put(o, o, outside11); put(o, p, outside12); put(p, p, outside22)
    for out, alpha, beta, gamma in [(o, alpha1, beta1, gamma1), (p, alpha2, beta2, gamma2)]:
        put(out, a, alpha); put(out, c, alpha)
        put(out, b, beta); put(out, d, beta); put(out, e, gamma)
    r, w = 3+2/q, (s-(3+2/q))/(q-1)
    put(a, a, 0); put(a, b, 0); put(b, b, 0)
    put(a, c, 2); put(a, d, r); put(b, c, r); put(b, d, w)
    return result


def choose(n, k):
    if k < 0:
        return R(0)
    if isinstance(n, int) and (n < k or n < 0):
        return R(0)
    result = R(1)
    for j in range(k):
        result *= R(n-j)/(j+1)
    return result


def model(q, values):
    n, s = (q*q+13*q+16)/2, 3*q+4
    result = []
    for j, ell in [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)]:
        levels = [(a, b) for a, b in TYPES if j <= a <= 3-j and ell <= b]
        norms = [choose(3-2*j, a-j)*choose(q-2*ell, b-ell) for a, b in levels]
        g = []
        for i, (a, b) in enumerate(levels):
            row = []
            for k, (c, d) in enumerate(levels):
                coefficient = (-1)**(j+ell)*choose(3-a-j, c-j)*choose(q-b-ell, d-ell)
                key = tuple(sorted(((a, b), (c, d))))
                entry = norms[i]*values.get(key, 0)*coefficient
                row.append(s*norms[i]*int(i == k)+entry-
                           (norms[i]*norms[k] if j == ell == 0 else 0))
            g.append(row)
        if any(g[i][k] != g[k][i] for i in range(len(levels)) for k in range(len(levels))):
            raise ValueError('symbolic symmetry failed')
        kernel = [[a for a, b in levels], [int(a >= 2) for a, b in levels]] if j == ell == 0 else \
                 [[1]*len(levels)] if (j, ell) == (1, 0) else []
        if any(sum(g[i][k]*v[k] for k in range(len(levels))) != 0
               for i in range(len(levels)) for v in kernel):
            raise ValueError('symbolic forced kernel failed')
        result.append({'degree': (j, ell), 'levels': levels, 'norms': norms, 'lower': g, 'kernel': kernel})
    return result
