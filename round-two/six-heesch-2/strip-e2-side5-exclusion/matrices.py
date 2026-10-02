"""Exact Boolean matrices and a conservative all-parameter relaxation."""
import deps
import strip_parametric_geometry as G
from strip_point_suppliers import finite_suppliers,IDENTITY
from strip_local_pair_certificate import cover_certificate
from known_e1 import known_bad
FIXED=()
POINTS=()
def matrices(atlas, guard, known):
    coverage = []; eligibility = []; clashes = {}; demands = []
    for h in atlas:
        guard()
        coverage.append([G.point_membership(h, p) for p in POINTS])
        eligibility.append(G.both(*(
            G.both(G.neg(G.intersection(G.relative(f, h))),
                   G.neg(known_bad(G.relative(f, h))) if known else True)
            for f in FIXED)))
    for j, h in enumerate(atlas):
        for i, g in enumerate(atlas[:j]):
            guard(); rel = G.relative(g, h)
            clashes[i, j] = G.either(G.intersection(rel), known_bad(rel) if known else False)
    for p in POINTS:
        occupied = G.either(*(G.point_membership(f, p) for f in FIXED))
        adjacent = G.either(*(
            G.point_membership(f, (G.sub(p[0], (0, du)), G.sub(p[1], (0, dv))))
            for f in FIXED[:2] for du, dv in G.UV_DIRS))
        demands.append(G.both(G.neg(occupied), adjacent))
    part = G.partition([x for row in coverage for x in row] + eligibility + list(clashes.values()) + demands)
    n = len(atlas)
    universal = {'cover': [0]*n, 'conflicts': [(1 << n)-1]*n, 'available': 0}
    samples = []
    for k in part['representatives']:
        guard()
        if not all(G.evaluate(x, k) for x in demands):
            raise ValueError('Demand outside the fixed-pair open halo')
        cov = [sum(1 << j for j, f in enumerate(row) if G.evaluate(f, k)) for row in coverage]
        con = [1 << j for j in range(n)]
        for (i, j), f in clashes.items():
            if G.evaluate(f, k):
                con[i] |= 1 << j; con[j] |= 1 << i
        av = sum(1 << j for j, f in enumerate(eligibility) if cov[j] and G.evaluate(f, k))
        matrix = {'cover': cov, 'conflicts': con, 'available': av}
        for j in range(n):
            universal['cover'][j] |= cov[j]
            universal['conflicts'][j] &= con[j]
        universal['available'] |= av
        proof = cover_certificate(matrix, len(POINTS), guard)
        samples.append({'k': k, 'matrix': matrix, 'proof': proof})
    proof = cover_certificate(universal, len(POINTS), guard)
    return {'partition': part, 'samples': samples, 'universal': universal, 'proof': proof,
            'complete_rejection': proof['rejected'] or all(x['proof']['rejected'] for x in samples)}
