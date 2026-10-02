"""Separate bitmask/recursive controls; imports no producer or expected data."""
import itertools as it
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def certificate(n, roles, colors):
    need(type(n) is int and n > 0 and len(roles) == n and
         all(type(r) is int and r in range(4) for r in roles), 'role domain')
    need(len(colors) == n*(n-1)//2 and
         all(type(c) is int and c in range(3) for c in colors), 'pair color domain')
    masks = [[0]*n for _ in range(2)]
    cursor = 0
    for i in range(n):
        for j in range(i+1, n):
            color = colors[cursor]; cursor += 1
            if color:
                need(not (roles[i] <= 1 and roles[j] % 2) and
                     not (roles[j] <= 1 and roles[i] % 2), 'eligible endpoint prohibition')
                need(color != 2 or (roles[i] > 1 and roles[j] > 1), 'heavy endpoint prohibition')
                masks[color-1][i] |= 1 << j
                masks[color-1][j] |= 1 << i
    adjacency = [x|y for x,y in zip(*masks)]
    side = [[i for i in range(n) if roles[i] == r] for r in range(4)]
    roots = []
    for i in side[0]:
        reach = (1 << i) | adjacency[i]
        for j in range(n):
            if adjacency[i] >> j & 1:
                reach |= adjacency[j]
        if reach == (1 << n)-1:
            roots.append(i)
    dA = sum(adjacency[i].bit_count() for i in side[0])
    dV = sum(masks[0][i].bit_count() for i in side[1])
    bound = 0
    for i in side[0]:
        d = adjacency[i].bit_count()
        bound += d if d < len(side[0]) else len(side[0])-1
    bound = (bound//2)*2
    first = sum(masks[0][i].bit_count() for i in side[2])
    second = sum(masks[1][i].bit_count() for i in side[2])
    residual = [(adjacency[i].bit_count()-1) for i in side[2] if masks[0][i]]
    target = len(side[1])+len(side[3])
    ell = None
    # Complete subset/cardinality minimization, not the sorted-prefix formula.
    for size in range(len(residual)+1):
        if any(sum(subset) >= target for subset in it.combinations(residual, size)):
            ell = size
            break
    active = bool(roots) and target > 0
    lower = None
    if active:
        need(ell is not None, 'radius-root capacity exists')
        need(first-dV >= len(roots)*ell and first-dV >= dA-bound,
             'all distinct unit-C edges use color1 capacity')
        need(first+second-dV-len(side[3]) >= max(len(roots)*ell, dA-bound),
             'eligible nonunit edges are disjoint from unit-C edges')
        lower = dV+max(len(roots)*ell,dA-bound)
    return dict(active=active, roots=roots, D_A=dA, D_V=dV, I_even=bound,
                C1=first, C2=second, eligible_units=len(side[1]), eligible_nonunits=len(side[3]),
                residual_capacities=sorted(residual,reverse=True), minimum_C_neighbors=ell,
                required_color1=lower,
                required_support=(lower+len(side[3]) if active else None))


def records():
    begin, out = time.monotonic(), []
    for n in range(2,6):
        for roles in it.combinations_with_replacement(range(4),n):
            if 0 not in roles or not any(r in (1,3) for r in roles):
                continue
            pairs = [(i,j) for i in range(n) for j in range(i+1,n)]
            def visit(position, colors):
                need(len(out) < 100000 and time.monotonic()-begin < 10,
                     'INCOMPLETE fixed100000-record/10s oracle guard')
                if position == len(pairs):
                    out.append(dict(n=n, roles=list(roles), colors=list(colors),
                                    certificate=certificate(n,roles,colors)))
                    return
                i,j = pairs[position]
                visit(position+1,colors+(0,))
                if ((roles[i] <= 1 and roles[j] % 2) or
                    (roles[j] <= 1 and roles[i] % 2)):
                    return
                visit(position+1,colors+(1,))
                if roles[i] > 1 and roles[j] > 1:
                    visit(position+1,colors+(2,))
            visit(0,())
    return sorted(out,key=lambda r:(r['n'],r['roles'],r['colors']))
