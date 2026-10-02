"""Exact finite controls for ordinary root-fan proof; six-code-1 researcher."""
import itertools as it
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def certificate(n, roles, colors):
    # A=0 ineligible unit; V=1 eligible unit; C=2 ineligible nonunit;
    # B=3 eligible nonunit. These are abstract graph roles, not actual stars.
    need(type(n) is int and n >= 1 and len(roles) == n and
         all(type(r) is int and 0 <= r <= 3 for r in roles), 'physical role input')
    pairs = list(it.combinations(range(n), 2))
    need(len(colors) == len(pairs) and all(type(c) is int and c in (0, 1, 2)
                                         for c in colors), 'simple colored pair input')
    one, two, graph = [set() for _ in roles], [set() for _ in roles], [set() for _ in roles]
    for (a, b), color in zip(pairs, colors):
        if not color:
            continue
        unit_a, unit_b = roles[a] < 2, roles[b] < 2
        eligible_a, eligible_b = roles[a] in (1, 3), roles[b] in (1, 3)
        need(not ((unit_a and eligible_b) or (unit_b and eligible_a)),
             'unit has no eligible neighbor')
        need(color == 1 or not (unit_a or unit_b), 'unit has only color1')
        target = one if color == 1 else two
        target[a].add(b); target[b].add(a)
        graph[a].add(b); graph[b].add(a)
    A, V, C, B = ([i for i,r in enumerate(roles) if r == role] for role in range(4))
    roots = []
    for a in A:
        reached = {a} | graph[a]
        for v in graph[a]:
            reached |= graph[v]
        if len(reached) == n:
            roots.append(a)
    D_A, D_V = (sum(len(graph[i]) for i in side) for side in (A, V))
    I = sum(min(len(graph[i]), len(A)-1) for i in A)
    I_even = I - I % 2
    C1, C2 = (sum(len(layer[i]) for i in C) for layer in (one, two))
    capacities = sorted([len(graph[c])-1 for c in C if one[c]], reverse=True)
    target = len(V)+len(B)
    ell = next((j for j in range(len(capacities)+1)
                if sum(capacities[:j]) >= target), None)
    active = bool(roots and target)
    if active:
        need(ell is not None, 'every eligible point is reached through C')
        lower = D_V + max(len(roots)*ell, D_A-I_even)
        need(C1 >= lower, 'distinct root and eligible-unit color1 endpoints')
        need(C1+C2 >= lower+len(B), 'disjoint C-B crossing support endpoints')
    else:
        lower = None
    return dict(active=active, roots=roots, D_A=D_A, D_V=D_V, I_even=I_even,
                C1=C1, C2=C2, eligible_units=len(V), eligible_nonunits=len(B),
                residual_capacities=capacities, minimum_C_neighbors=ell,
                required_color1=lower,
                required_support=(lower+len(B) if active else None))


def records():
    begin, out = time.monotonic(), []
    for n in range(2, 6):
        for a, v, c in it.product(range(n+1), repeat=3):
            b = n-a-v-c
            if a < 1 or b < 0 or v+b < 1:
                continue
            roles = (0,)*a + (1,)*v + (2,)*c + (3,)*b
            options = []
            for i,j in it.combinations(range(n), 2):
                if ((roles[i] < 2 and roles[j] in (1,3)) or
                    (roles[j] < 2 and roles[i] in (1,3))):
                    options.append((0,))
                elif roles[i] >= 2 and roles[j] >= 2:
                    options.append((0,1,2))
                else:
                    options.append((0,1))
            for colors in it.product(*options):
                need(len(out) < 100000 and time.monotonic()-begin < 10,
                     'INCOMPLETE fixed100000-record/10s calibration guard')
                out.append(dict(n=n, roles=list(roles), colors=list(colors),
                                certificate=certificate(n, roles, colors)))
    return sorted(out, key=lambda r:(r['n'], r['roles'], r['colors']))
