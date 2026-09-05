"""Arithmetic isomorphism and small product/collision/extra-edge controls."""
from itertools import combinations
import json
import field as F
import audit as A

basis = [tuple(int(i == j) for i in range(24)) for j in range(24)]
for a in basis:
    assert A.decode(F.conjugate(a)) == A.conjugate(A.decode(a))
    for b in basis:
        assert A.decode(F.mul(a, b)) == A.mul(A.decode(a), A.decode(b))
omega = F.K.POW[7]+F.K.ZERO
root_minus3 = F.sub(F.scale(omega, 2), F.ONE)
gauss = F.ZERO
for j in range(1, 7):
    term = F.K.POW[(6*j) % 42]+F.K.ZERO
    gauss = F.add(gauss, F.scale(term, 1 if j in [1, 2, 4] else -1))
assert F.mul(root_minus3, root_minus3) == F.scale(F.ONE, -3)
assert F.mul(gauss, gauss) == F.scale(F.ONE, -7)
s = F.K.ZERO+F.K.ONE
assert F.mul(s, s) == F.scale(F.ONE, -11)
rho_numerator = F.add(F.scale(F.ONE, 5), s)
assert F.norm(rho_numerator) == F.scale(F.ONE, 36)


def tiny_sum(second, denominator):
    H = [F.ZERO, F.scale(F.ONE, denominator)]
    M = [F.ZERO, second]
    points = sorted({F.add(a, b) for a in H for b in M})
    index = {p: i for i, p in enumerate(points)}
    fibres = [[] for _ in points]
    for a in range(2):
        for b in range(2): fibres[index[F.add(H[a], M[b])]].append((a, b))
    edges = {(i, j) for i, j in combinations(range(len(points)), 2)
             if F.norm(F.sub(points[i], points[j])) == F.scale(F.ONE, denominator**2)}
    factor = {tuple(sorted((index[F.add(H[0], m)], index[F.add(H[1], m)]))) for m in M}
    factor |= {tuple(sorted((index[F.add(h, M[0])], index[F.add(h, M[1])])) ) for h in H}
    colours = []
    for fibre in fibres:
        vals = {a^b for a, b in fibre}
        assert len(vals) == 1
        colours.append(vals.pop())
    return len(points), len(edges), len(edges-factor), all(colours[a] != colours[b] for a, b in edges)


assert tiny_sum(rho_numerator, 6) == (4, 4, 0, True)
assert tiny_sum(F.ONE, 1) == (3, 2, 0, True)
assert tiny_sum(omega, 1) == (4, 5, 1, False)
print(json.dumps({'status': 'ALL ARITHMETIC AND PRODUCT CONTROLS PASSED',
                  'basis_products_compared': 576, 'basis_conjugates_compared': 24,
                  'quadratic_square_identities': [-3, -7, -11],
                  'generic_rotation_control': [4, 4, 0, True],
                  'compatible_collision_control': [3, 2, 0, True],
                  'extra_edge_XOR_failure_control': [4, 5, 1, False]}, indent=2))
