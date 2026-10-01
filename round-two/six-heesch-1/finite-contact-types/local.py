"""Complete finite mesh surround compiler. Solvers are optional callers.

Scale 4 is complete for an unrestricted surround of a half-grid fixed pair.
For a restricted contact domain use the proved anchored mesh, not scale 4.
"""
from collections import defaultdict
from fractions import Fraction as Q
from contact import halo, require


def candidates(tile, fixed, scale):
    old = set().union(*(tile.pixels(p, scale) for p in fixed))
    target = halo(old)
    result = []
    for o in range(len(tile.orientations)):
        op = tile.pixels((o, 0, 0), scale)
        shifts = {(x-a, y-b) for x, y in target for a, b in op}
        for x, y in sorted(shifts):
            physical = frozenset((a+x, b+y) for a, b in op)
            if old.isdisjoint(physical):
                result.append(((o, Q(x, scale), Q(y, scale)), physical))
    return target, result


def compile_cnf(tile, fixed, scale, domain=None):
    if domain is not None:
        for i, A in enumerate(fixed):
            for B in fixed[:i]:
                rel = tile.relation(A, B)
                require(rel != 'overlap', 'fixed overlap')
                require(rel != 'contact' or tile.relative_type(A, B) in domain,
                        'fixed forbidden contact')
    target, pool = candidates(tile, fixed, scale)
    if domain is not None:
        pool = [(p, pixels) for p, pixels in pool
                if all(tile.relation(p, A) != 'contact' or
                       tile.relative_type(p, A) in domain for A in fixed)]
    owners = defaultdict(list)
    for i, (pose, pixels) in enumerate(pool, 1):
        for p in pixels:
            owners[p].append(i)
    clauses = []
    nv = len(pool)
    for p in sorted(owners):
        xs = owners[p]
        if len(xs) < 2:
            continue
        if len(xs) == 2:
            clauses.append([-xs[0], -xs[1]])
            continue
        ss = list(range(nv+1, nv+len(xs)))
        nv += len(xs)-1
        clauses.append([-xs[0], ss[0]])
        for i in range(1, len(xs)-1):
            clauses.extend(([-xs[i], ss[i]], [-ss[i-1], ss[i]], [-xs[i], -ss[i-1]]))
        clauses.append([-xs[-1], -ss[-1]])
    clauses.extend(owners[p] for p in sorted(target))
    if domain is not None:
        # All contact constraints, including outside the demanded halo.
        halos = [halo(pixels) for p, pixels in pool]
        for i, (A, pa) in enumerate(pool):
            for j in range(i):
                B, pb = pool[j]
                if pa.isdisjoint(pb) and not halos[i].isdisjoint(pb) and \
                        tile.relative_type(A, B) not in domain:
                    clauses.append([-i-1, -j-1])
    return pool, clauses, nv


def dimacs(clauses, nv):
    return ('p cnf %d %d\n' % (nv, len(clauses))+''.join(
        ' '.join(map(str, c))+' 0\n' for c in clauses)).encode()
