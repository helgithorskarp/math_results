"""Deterministic exact audit; stdout is the compact JSON certificate."""
import hashlib
import itertools
import json
import random
from fractions import Fraction as F

from cactus import (Graph, State, MODULE_EDGES, attach_cycle, attach_leaf,
                    attach_module, blocks, bridge_state, cycle_state, inertia,
                    need, prepare, response, rooted_state)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest_update(h, value):
    h.update(encode(value)+b'\n')


def characteristic_inertia(a):
    """Integer Faddeev--LeVerrier, then Descartes for a real-rooted polynomial.

    Independent of rational pivoting and the rooted-state recursion.
    """
    n = len(a)
    need(all(len(r) == n and all(type(x) is int for x in r) for r in a),
         'characteristic checker requires an integer square matrix')
    need(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)),
         'characteristic checker requires symmetry')
    nz = [[(j, x) for j, x in enumerate(row) if x] for row in a]
    b = [[int(i == j) for j in range(n)] for i in range(n)]
    coeff = [1]
    for k in range(1, n+1):
        product = [[sum(x*b[j][v] for j, x in nz[u]) for v in range(n)]
                   for u in range(n)]
        total = -sum(product[i][i] for i in range(n))
        c, remainder = divmod(total, k)
        need(remainder == 0, 'nonintegral characteristic coefficient')
        coeff.append(c)
        for i in range(n):
            product[i][i] += c
        b = product
    need(not any(x for row in b for x in row), 'Cayley--Hamilton failure')
    z = 0
    while len(coeff) > 1 and coeff[-1] == 0:
        z += 1
        coeff.pop()

    def changes(xs):
        signs = [1 if x > 0 else -1 for x in xs if x]
        return sum(u != v for u, v in zip(signs, signs[1:]))

    p = changes(coeff)
    m = changes([c*(-1)**i for i, c in enumerate(coeff)])
    need(p+z+m == n, 'real-rooted sign count mismatch')
    return p, z, m


def literal_matrix(g, root=None, line=False):
    if line:
        return [[int(i != j and any(u == v for u in e for v in f))
                 for j, f in enumerate(g.edges)] for i, e in enumerate(g.edges)]
    out = [[0]*g.n for _ in range(g.n)]
    for i in range(g.n):
        out[i][i] = sum(i in e for e in g.edges)-2+int(i == root)
        for j in range(i):
            out[i][j] = out[j][i] = int((j, i) in g.edges)
    return out


def brute_cactus(g):
    """Definition-level simple-cycle enumeration, independent of Tarjan blocks."""
    if not g.connected():
        return False
    adj = g.adjacency()
    cycles = set()
    for start in range(g.n):
        def walk(path):
            for v in adj[path[-1]]:
                if v == start and len(path) >= 3:
                    es = tuple(sorted(tuple(sorted(e)) for e in
                                      zip(path, path[1:]+[start])))
                    cycles.add(es)
                elif v > start and v not in path:
                    walk(path+[v])
        walk([start])
    counts = {e: 0 for e in g.edges}
    for cyc in cycles:
        for e in cyc:
            counts[e] += 1
    return max(counts.values(), default=0) <= 1


def trace_replay(original, trace, output):
    """Replay raw edge edits without calling either production constructor."""
    n, es = original.n, set(original.edges)
    for step in trace:
        if step['operation'] == 'split':
            v, group = step['vertex'], set(step['group'])
            ns = {next(iter(set(e)-{v})) for e in es if v in e}
            need(len(group) == 2 and group < ns, 'bad split trace')
            moved = ns-group
            es = {e for e in es if not (v in e and bool(set(e) & moved))}
            es.update(tuple(sorted((n, x))) for x in moved)
            es.update(tuple(sorted(e)) for e in
                      ((v, n+1), (n+1, n+2), (n+2, n+3), (n+3, n)))
            n += 4
        else:
            need(step['operation'] == 'four_subdivide', 'unknown trace operation')
            u, v = step['edge']
            es.remove(tuple(sorted((u, v))))
            path = [u]+list(range(n, n+4))+[v]
            es.update(tuple(sorted(e)) for e in zip(path, path[1:]))
            n += 4
    need(n == output.n and es == set(output.edges), 'edge-trace replay mismatch')


def path_matrix(weights, cycle=False):
    n = len(weights)
    a = [[int(i == j)*w for j in range(n)] for i, w in enumerate(weights)]
    for i in range(n-1):
        a[i][i+1] = a[i+1][i] = 1
    if cycle:
        need(n >= 3, 'short cycle')
        a[0][-1] = a[-1][0] = 1
    return a


def weighted_audit():
    h = hashlib.sha256()
    paths = cycles = 0
    for n in range(1, 9):
        for ws in itertools.product(range(3), repeat=n):
            ip = characteristic_inertia(path_matrix(ws))
            need(2*(ip[0]-ip[2]) <= sum(ws)+1, 'weighted path inequality')
            paths += 1
            ic = None
            if n >= 3:
                ic = characteristic_inertia(path_matrix(ws, True))
                need(2*(ic[0]-ic[2]) <= sum(ws)+2, 'weighted cycle inequality')
                cycles += 1
            digest_update(h, [ws, ip, ic])
    # Negative and unrestricted diagonals at the three-unit charge boundary.
    rng = random.Random(17001)
    charged = 0
    for _ in range(400):
        n = rng.randrange(3, 20)
        ks = [rng.randrange(5) for _ in range(n)]
        ds = [k-rng.randrange(6) if k <= 2 else rng.randrange(-30, 31)
              for k in ks]
        for iscycle in (False, True):
            ins = characteristic_inertia(path_matrix(ds, iscycle))
            need(2*(ins[0]-ins[2]) <= sum(ks)+(2 if iscycle else 1),
                 'charged path/cycle inequality')
            digest_update(h, [ks, ds, iscycle, ins])
            charged += 1
    return {'paths': paths, 'cycles': cycles, 'charged_cases': charged,
            'entrywise_sha256': h.hexdigest()}


def abstract_states():
    # Choose nonnegative inertias and cycle counts realizing each charge
    # algebraically; these are abstract transition inputs, not graph claims.
    specs = [(0, F(1)), (0, F(3)), (1, F(0)), (1, F(1, 3)),
             (2, F(-1)), (2, F(4)), (3, F(-100)), (4, F(-7)),
             (1, None), (2, None)]
    out = []
    for k, rho in specs:
        c = k % 2
        sigma = (3*c-k)//2
        inert = (max(sigma, 0)+1, int(rho is None), max(-sigma, 0)+1)
        state = State(c, inert, rho).validate()
        need(state.charge == k, 'abstract charge mismatch')
        out.append(state)
    return out


def state_row(s):
    return [s.cycles, s.inert, s.charge, None if s.rho is None else str(s.rho)]


def transition_audit():
    alphabet = abstract_states()
    h = hashlib.sha256()
    bc = cc = poles = 0
    for k in range(5):
        for ids in itertools.product(range(len(alphabet)), repeat=k):
            s = bridge_state([alphabet[i] for i in ids]).validate()
            poles += s.rho is None
            digest_update(h, ['bridge', ids, state_row(s)])
            bc += 1
    for length in range(3, 6):
        for ids in itertools.product(range(len(alphabet)), repeat=length-1):
            s = cycle_state([alphabet[i] for i in ids]).validate()
            poles += s.rho is None
            digest_update(h, ['cycle', ids, state_row(s)])
            cc += 1
    # No-child cycles, singular response regimes, long zero runs and holes.
    for length in range(3, 41):
        choices = ([None]*(length-1),
                   [alphabet[(3*i+length) % len(alphabet)] for i in range(length-1)])
        for children in choices:
            s = cycle_state(children).validate()
            digest_update(h, ['long_cycle', length, [None if x is None else state_row(x)
                                                    for x in children], state_row(s)])
            cc += 1
    return {'bridge_transitions': bc, 'cycle_transitions': cc,
            'pole_outputs_in_short_exhaustive_cases': poles,
            'entrywise_sha256': h.hexdigest()}


def graph_audit():
    h = hashlib.sha256()
    counts = {}
    totals = {'graphs': 0, 'splits': 0, 'bridge_subdivisions': 0,
              'recursive_states': 0, 'pole_states': 0,
              'singular_rooted_inputs': 0, 'literal_line_checks': 0}
    max_order = 0

    def check_graph(g, label, literal_line=False):
        nonlocal max_order
        original = characteristic_inertia(literal_matrix(g))
        need(g.matrix() == literal_matrix(g), 'vertex matrix definition')
        c = g.c()
        need(2*(original[0]-original[2]-c+1) <= c+1 if g.edges else True,
             'literal graph violates cactus bound')
        out, root, trace = prepare(g)
        trace_replay(g, trace, out)
        blocks(out)
        need(max(map(len, out.adjacency())) <= 3, 'degree reduction failed')
        need(out.c() == c, 'cycle count changed')
        exact = characteristic_inertia(literal_matrix(out))
        increments = 2*len(trace)
        need(exact == (original[0]+increments, original[1], original[2]+increments),
             'reduction inertia changed incorrectly')
        totals['splits'] += sum(x['operation'] == 'split' for x in trace)
        totals['bridge_subdivisions'] += sum(x['operation'] == 'four_subdivide' for x in trace)
        rows = []
        if root is not None:
            s = rooted_state(out, root, rows)
            direct = characteristic_inertia(literal_matrix(out, root))
            need(s.inert == direct, 'recursive/characteristic inertia mismatch')
            need(s.rho == response(literal_matrix(out, root), root),
                 'recursive/direct range response mismatch')
            totals['singular_rooted_inputs'] += bool(direct[1])
            totals['recursive_states'] += len(rows)
            totals['pole_states'] += sum(x['response'] is None for x in rows)
        else:
            need(c == 1 and all(len(x) == 2 for x in out.adjacency()),
                 'missing root outside the pure-cycle case')
            s = rooted_state(out, 0, rows)
            need(s.inert == characteristic_inertia(literal_matrix(out, 0)),
                 'pure-cycle rooted state')
        if literal_line:
            li = characteristic_inertia(literal_matrix(out, line=True))
            need(li == (exact[0], exact[1], exact[2]+c-1) if out.edges else li == (0, 0, 0),
                 'literal incidence/line inertia mismatch')
            totals['literal_line_checks'] += 1
        totals['graphs'] += 1
        max_order = max(max_order, out.n)
        digest_update(h, [label, g.n, g.edges, trace, out.n, exact, rows])

    # Entire labelled graph universe, with independent cycle-definition filter.
    for n in range(1, 7):
        edges = list(itertools.combinations(range(n), 2))
        count = 0
        for mask in range(1 << len(edges)):
            g = Graph(n, tuple(e for j, e in enumerate(edges) if mask >> j & 1))
            is_cactus = brute_cactus(g)
            try:
                blocks(g)
                accepted = True
            except ValueError:
                accepted = False
            need(accepted == is_cactus, 'Tarjan/definition cactus mismatch')
            if not is_cactus:
                continue
            check_graph(g, ['labelled', n, mask], n <= 4 or mask % 97 == 0)
            count += 1
        counts[str(n)] = count

    # Reproducible varied articulation, bridge, leaf and cycle-length fixtures.
    rng = random.Random(2026092417)
    for index in range(120):
        g = Graph(1, ())
        for step in range(rng.randrange(3, 10)):
            root = rng.randrange(g.n)
            if rng.randrange(3) == 0:
                g = attach_leaf(g, root)
            else:
                g = attach_cycle(g, root, rng.randrange(3, 9))
        check_graph(g, ['seeded', index], index % 10 == 0)

    sharp = []
    for parity in (0, 1):
        g = Graph(1, ()) if parity == 0 else attach_cycle(Graph(1, ()), 0, 5)
        for k in range(7):
            ins = characteristic_inertia(literal_matrix(g, line=True))
            need(ins[0]-ins[2] == (g.c()+1)//2, 'sharpness witness failed')
            sharp.append([g.c(), g.n, len(g.edges), ins])
            check_graph(g, ['sharp', parity, k], True)
            g = attach_module(g, (3*k) % g.n)
    return {'all_labelled_cactus_counts': counts, 'totals': totals,
            'maximum_reduced_order': max_order, 'sharp_witnesses': sharp,
            'entrywise_sha256': h.hexdigest()}


def rejection_audit():
    cases = {
        'simple_loop': lambda: Graph(2, ((0, 0),)),
        'duplicate_edge': lambda: Graph(2, ((0, 1), (1, 0))),
        'bad_endpoint': lambda: Graph(2, ((0, 2),)),
        'disconnected': lambda: blocks(Graph(2, ())),
        'theta_is_not_cactus': lambda: blocks(Graph(4, ((0, 1), (0, 2), (1, 2), (0, 3), (1, 3)))),
        'k4_is_not_cactus': lambda: blocks(Graph(4, tuple(itertools.combinations(range(4), 2)))),
        'short_cycle': lambda: cycle_state([None]),
        'negative_charge': lambda: State(0, (1, 0, 0), F(1)).validate(),
        'zero_charge_pole': lambda: State(0, (0, 1, 0), None).validate(),
        'zero_charge_bad_response': lambda: State(0, (0, 0, 0), F(1, 2)).validate(),
        'charge_one_bad_response': lambda: State(1, (1, 0, 0), F(-1)).validate(),
        'charge_two_bad_response': lambda: State(0, (0, 0, 1), F(-2)).validate(),
        'extra_cycle_root_child': lambda: rooted_state(attach_leaf(attach_cycle(Graph(1, ()), 0, 3), 0), 0),
        'nonsymmetric_matrix': lambda: inertia([[0, 1], [0, 0]]),
    }
    for name, run in cases.items():
        try:
            run()
        except ValueError:
            pass
        else:
            raise RuntimeError('negative control accepted: '+name)
    # A charge-two allowance for an arbitrary diagonal would be false:
    # diag(1,3,1)+A(P3) is positive definite and has signature three.
    need(characteristic_inertia(path_matrix([1, 3, 1])) == (3, 0, 0),
         'three-unit charge boundary witness')
    # Explicit singular root cases distinguish poles from zero response.
    singular_cases = [([[0]], None), ([[0, 1], [1, 0]], F(0)),
                      ([[1, 0], [0, 0]], F(1)),
                      ([[1, 1], [1, 1]], None)]
    for a, expected in singular_cases:
        need(response(a) == expected, 'singular range boundary')
        need(inertia(a) == characteristic_inertia(a), 'singular inertia boundary')
    module = Graph(10, MODULE_EDGES)
    need(characteristic_inertia(module.line_matrix()) == (6, 0, 5), 'module inertia')
    edge = module.edges.index((1, 9))
    need(response(module.line_matrix(), edge) == 0, 'module zero response')
    return {'rejected_inputs': sorted(cases), 'singular_range_cases': len(singular_cases),
            'charge_two_unrestricted_counterexample': [1, 3, 1],
            'known_module_inertia': [6, 0, 5], 'known_module_root_response': '0'}


def main():
    result = {'weighted_lemmas': weighted_audit(),
              'abstract_transitions': transition_audit(),
              'literal_graphs': graph_audit(), 'boundary_controls': rejection_audit()}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
