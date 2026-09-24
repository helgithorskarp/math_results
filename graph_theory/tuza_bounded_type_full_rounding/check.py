"""Exact finite audits of the full-rounding proof; Python standard library only.

This checks finite identities and implementations, not the universal theorem.
The analytic concentration and iteration proofs are in NIBBLE.md.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations, product
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prod(values):
    result = Q(1)
    for value in values:
        result *= value
    return result


def validate(n, edges, weights):
    require(len(edges) == len(weights), 'weight count')
    require(len(set(edges)) == len(edges), 'duplicate edge')
    require(all(len(e) == 3 and len(set(e)) == 3 and tuple(sorted(e)) == e
                and all(type(v) is int and 0 <= v < n for v in e)
                for e in edges), 'edge domain')
    require(all(len(set(e) & set(f)) <= 1 for e, f in combinations(edges, 2)),
            'hypergraph not linear')
    require(all(isinstance(x, Q) and x >= 0 for x in weights), 'weight domain')
    loads = [sum((x for e, x in zip(edges, weights) if v in e), Q(0))
             for v in range(n)]
    require(all(x <= 1 for x in loads), 'infeasible weights')
    return loads


def one_round(n, edges, weights, alpha):
    """Enumerate marks and relevant retention coins, integrating other coins."""
    validate(n, edges, weights)
    q, eta = 1-alpha, alpha*alpha
    marks = [alpha*x for x in weights]
    r = [prod(1-marks[j] for j, e in enumerate(edges) if v in e)
         for v in range(n)]
    keep = [q/z for z in r]
    require(all(q <= z <= 1 for z in keep), 'coin probability')
    total = matching = raw_mean = next_mean = bad_probability = Q(0)
    vertex_survival = [Q(0)]*n
    edge_survival = [Q(0)]*len(edges)
    conditional_numerator = [Q(0)]*n
    outcomes = 0
    digest = sha256()
    for marked_bits in product((0, 1), repeat=len(edges)):
        pm = prod(p if bit else 1-p for p, bit in zip(marks, marked_bits))
        marked = [j for j, bit in enumerate(marked_bits) if bit]
        occupied = set().union(*(set(edges[j]) for j in marked))
        free = [v for v in range(n) if v not in occupied]
        accepted = [j for j in marked
                    if all(j == h or not set(edges[j]) & set(edges[h])
                           for h in marked)]
        used = [v for j in accepted for v in edges[j]]
        require(len(used) == len(set(used)), 'accepted edges overlap')
        for coin_bits in product((0, 1), repeat=len(free)):
            probability = pm*prod(keep[v] if bit else 1-keep[v]
                                  for v, bit in zip(free, coin_bits))
            surviving = {v for v, bit in zip(free, coin_bits) if bit}
            require(not surviving & set(used), 'matching intersects future')
            old_loads = [Q(0)]*n
            remaining = []
            for j, e in enumerate(edges):
                if set(e) <= surviving:
                    remaining.append(j)
                    edge_survival[j] += probability
                    for v in e:
                        old_loads[v] += weights[j]
            scale = q*q*(1+eta)
            raw = sum((weights[j] for j in remaining), Q(0))/scale
            good = all(z <= scale for z in old_loads)
            if good:
                validate(n, tuple(edges[j] for j in remaining),
                         tuple(weights[j]/scale for j in remaining))
                next_mean += probability*raw
            else:
                bad_probability += probability
            total += probability
            matching += probability*len(accepted)
            raw_mean += probability*raw
            for v in surviving:
                vertex_survival[v] += probability
                conditional_numerator[v] += probability*old_loads[v]
            record = [marked_bits, sorted(surviving), str(probability), accepted, good]
            digest.update((json.dumps(record, separators=(',', ':'))+'\n').encode())
            outcomes += 1
    require(total == 1, 'total probability')
    require(all(z == q for z in vertex_survival), 'vertex marginal')
    for j, x in enumerate(weights):
        require(edge_survival[j] == q**3/(1-alpha*x)**2,
                'dependent edge survival')
    for v in range(n):
        expected = q*q*sum((x/(1-alpha*x)**2 for e, x in zip(edges, weights)
                           if v in e), Q(0))
        require(conditional_numerator[v]/q == expected, 'conditional load mean')
    expected_matching = sum((alpha*x*prod(1-alpha*weights[h]
                            for h, f in enumerate(edges)
                            if j != h and set(e) & set(f))
                            for j, (e, x) in enumerate(zip(edges, weights))), Q(0))
    require(matching == expected_matching, 'matching mean')
    w = sum(weights, Q(0))
    require(matching >= alpha*(1-3*alpha)*w, 'matching lower bound')
    require(raw_mean == q/(1+eta)*sum((x/(1-alpha*x)**2 for x in weights), Q(0)),
            'raw objective identity')
    require(next_mean >= raw_mean-bad_probability*w/(q*q*(1+eta)),
            'abort correction')
    return dict(vertices=n, hyperedges=len(edges), alpha=str(alpha), outcomes=outcomes,
                fractional_value=str(w), expected_matching=str(matching),
                expected_raw_value=str(raw_mean), expected_next_value=str(next_mean),
                abort_probability=str(bad_probability), outcome_sha256=digest.hexdigest())


def influence_audit(n, edges, weights, alpha):
    """Evaluate every conditional Boolean state and every coordinate toggle."""
    validate(n, edges, weights)
    q = 1-alpha
    delta = max(weights, default=Q(0))
    total_states = total_toggles = 0
    for v in range(n):
        adjacent = {a: x for e, x in zip(edges, weights) if v in e
                    for a in e if a != v}
        variables = []
        for e, x in zip(edges, weights):
            if v not in e:
                bound = sum((adjacent.get(a, Q(0)) for a in e), Q(0))
                if bound:
                    variables.append((set(e), alpha*x, bound))
        for a, x in adjacent.items():
            r = prod(1-alpha*y for e, y in zip(edges, weights) if a in e)
            variables.append(({a}, 1-q/r, x))
        variance_bound = sum((p*c*c for _, p, c in variables), Q(0))
        require(variance_bound <= 8*alpha*delta, 'variance proxy')
        require(all(c <= 3*delta for _, _, c in variables), 'maximum influence')
        values = []
        for bits in product((0, 1), repeat=len(variables)):
            removed = set().union(*(affected for (affected, _, _), bit
                                    in zip(variables, bits) if bit))
            values.append(sum((x for e, x in zip(edges, weights)
                               if v in e and not (set(e)-{v}) & removed), Q(0)))
        # Product order makes its first coordinate the highest binary bit.
        for state, value in enumerate(values):
            for j, (_, _, bound) in enumerate(variables):
                other = state ^ (1 << (len(variables)-1-j))
                require(abs(value-values[other]) <= bound, 'coordinate influence')
                total_toggles += 1
        total_states += len(values)
    return dict(conditional_states=total_states, coordinate_toggles=total_toggles)


def triangle_hypergraph(k):
    graph_edges = list(combinations(range(k), 2))
    ids = {e: j for j, e in enumerate(graph_edges)}
    edges = tuple(tuple(sorted(ids[e] for e in combinations(t, 2)))
                  for t in combinations(range(k), 3))
    return len(graph_edges), edges


def symmetry_audit(sizes, cliques, cross):
    classes = []
    before = 0
    for s in sizes:
        classes.append(tuple(range(before, before+s)))
        before += s
    owner = {v: i for i, group in enumerate(classes) for v in group}
    graph_edges = {e for e in combinations(range(before), 2)
                   if (owner[e[0]] == owner[e[1]] and cliques[owner[e[0]]])
                   or tuple(sorted((owner[e[0]], owner[e[1]]))) in cross}
    triangles = [t for t in combinations(range(before), 3)
                 if all(e in graph_edges for e in combinations(t, 2))]
    used, packing = set(), []
    for t in triangles:
        es = set(combinations(t, 2))
        if not es & used:
            used.update(es)
            packing.append(t)
    key = lambda t: tuple(sorted(owner[v] for v in t))
    orbits = Counter(map(key, triangles))
    chosen = Counter(map(key, packing))
    average = {t: Q(chosen[key(t)], orbits[key(t)]) for t in triangles}
    direct = Counter()
    group_order = 0
    for maps in product(*(tuple(permutations(group)) for group in classes)):
        mapping = {v: w for group, perm in zip(classes, maps) for v, w in zip(group, perm)}
        direct.update(tuple(sorted(mapping[v] for v in t)) for t in packing)
        group_order += 1
    require(all(average[t] == Q(direct[t], group_order) for t in triangles),
            'orbit average differs from permutation average')
    loads = Counter()
    for t, x in average.items():
        for e in combinations(t, 2):
            loads[e] += x
        for a, b in combinations(t, 2):
            third = next(v for v in t if v not in (a, b))
            count = len(classes[owner[third]])-sum(owner[z] == owner[third] for z in (a, b))
            require(count*x <= 1, 'stabilizer weight bound')
    require(all(z <= 1 for z in loads.values()), 'averaged packing overload')
    require(sum(average.values(), Q(0)) == len(packing), 'average value changed')
    deletion_checks = 0
    for threshold in range(2, max(sizes)+2):
        removed = {v for group in classes if len(group) < threshold for v in group}
        loss = sum((x for t, x in average.items() if set(t) & removed), Q(0))
        require(loss <= Q(len(removed)*(before-1), 2), 'vertex deletion loss')
        remaining = [x for t, x in average.items() if not set(t) & removed]
        if threshold >= 3:
            require(all(x <= Q(1, threshold-2) for x in remaining), 'small weight reduction')
        deletion_checks += 1
    return dict(sizes=sizes, vertices=before, graph_edges=len(graph_edges),
                triangles=len(triangles), seed_packing=len(packing),
                permutations=group_order, deletion_checks=deletion_checks)


def parameters():
    rows = []
    for epsilon in [Q(1, 2), Q(1, 5), Q(1, 10), Q(1, 20)]:
        alpha = epsilon/10
        q, eta = 1-alpha, alpha*alpha
        b, a = 1-alpha-2*eta, alpha*(1-3*alpha)
        power, rounds = Q(1), 0
        while power > epsilon/2:
            power *= q
            rounds += 1
        require(q*epsilon/2 < power <= epsilon/2, 'minimal round count')
        require(4/(q*q) <= 5, 'maximum weight growth')
        require((q-eta/(4*q*q))/(1+eta) >= b, 'objective recurrence')
        require(a/(1-b) >= 1-epsilon/2 and 0 < b <= q, 'iteration ratio')
        require((1-epsilon/2)**2 >= 1-epsilon, 'final approximation')
        require(q*q*eta/2 >= eta/3, 'load margin')
        require((eta/3)**2/(2*(8*alpha+eta/3)) >= eta*eta/180,
                'concentration exponent')
        require(5*epsilon**4/10**8 == alpha**4/2000, 'constant conversion')
        require(alpha**4/2000 <= alpha/8, 'small weight range')
        rows.append(dict(epsilon=str(epsilon), rounds=rounds,
                         alpha=str(alpha), eta=str(eta)))
    return rows


def cutoffs():
    rows = []
    for r in [1, 2, 3, 4, 9, 20]:
        a, d, c = 8*r+11, 2**r+r, 400*(r+1)
        b = 10**10*d*(64*a)**7*(r+1)**13
        ell = (4*b*c).bit_length()
        k = max(16*(r+1), 4*b*ell)
        require(2**(ell-1) <= 4*b*c < 2**ell, 'bit length')
        require(k >= 2*b and 4*(2*k+32*(r+1)) <= k*k, 'cutoff conditions')
        require(b == (64*a)**7*10**10*d*(r+1)**13, 'seventh-power comparison')
        rows.append(dict(r=r, A=a, d=d, C=c, B=str(b), ell=ell,
                         K=str(k), digits=len(str(k))))
    return rows


def rejected(operation):
    try:
        operation()
    except ValueError:
        return True
    raise AssertionError('malformed object accepted')


def audit():
    nk4, ek4 = triangle_hypergraph(4)
    fano = tuple(sorted({tuple(sorted((a-1, b-1, (a^b)-1)))
                         for a in range(1, 8) for b in range(a+1, 8)}))
    fixtures = [
        ('empty', 1, (), ()),
        ('single', 3, ((0, 1, 2),), (Q(1),)),
        ('unequal_bowtie', 5, ((0, 1, 2), (0, 3, 4)), (Q(1, 3), Q(2, 3))),
        ('graph_K4', nk4, ek4, (Q(1, 2),)*4),
        ('Fano', 7, fano, (Q(1, 3),)*7),
        ('linear_cycle', 8, ((0, 1, 2), (2, 3, 4), (4, 5, 6), (0, 6, 7)),
         (Q(1, 2),)*4),
    ]
    rounds, influences = [], []
    for name, n, edges, weights in fixtures:
        for alpha in (Q(1, 20), Q(1, 100)):
            rounds.append(dict(name=name, **one_round(n, edges, weights, alpha)))
        influences.append(dict(name=name, **influence_audit(n, edges, weights, Q(1, 20))))
    controls = [
        rejected(lambda: validate(4, ((0, 1, 2), (0, 1, 3)), (Q(1, 2), Q(1, 2)))),
        rejected(lambda: validate(3, ((0, 1, 2),), (Q(2),))),
        rejected(lambda: validate(3, ((0, 1, 2), (0, 1, 2)), (Q(1, 4), Q(1, 4)))),
        rejected(lambda: require(Q(19, 20)**3 == Q(19, 20)**3/(1-Q(1, 40))**2,
                                 'false independent survival')),
        rejected(lambda: require((1-Q(1, 60))*(1-Q(1, 30)) == Q(19, 20),
                                 'missing equalizing coin')),
    ]
    symmetry = [
        symmetry_audit((3, 3, 3), (True, True, True), {(0, 1), (0, 2), (1, 2)}),
        symmetry_audit((3, 3, 3), (False, False, False), {(0, 1), (0, 2), (1, 2)}),
        symmetry_audit((2, 3, 4), (True, True, False), {(0, 1), (0, 2), (1, 2)}),
    ]
    return dict(status='all exact finite audits passed', one_round=rounds,
                influences=influences, symmetry=symmetry, parameters=parameters(),
                cutoffs=cutoffs(), negative_controls=len(controls),
                boundary='Finite audits do not prove concentration or the universal theorem; see NIBBLE.md and PROOF.md.')


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
