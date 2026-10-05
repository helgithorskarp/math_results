"""Exact typed-flow construction, followed by ALL original entry checks.

Only the defining DATA and openly credited local original decoder are read.
No ancestor EXPECTED record, factor, solver, program or peer input is used.
The flow is an author construction, not independent mathematical review.
"""
from collections import deque
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json
from math import lcm


def require(ok, message):
    if not ok:
        raise ValueError(message)


def original():
    p = Path(__file__).with_name('census.py')
    spec = importlib.util.spec_from_file_location('new_transport_decoder', p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.original()


def flow(n, source, sink, edges):
    """Deterministic integer Dinic flow; only a complete lifted flow is evidence."""
    graph = [[] for _ in range(n)]
    handles = []
    for u, v, capacity in edges:
        require(capacity >= 0, 'nonnegative exact construction capacity')
        handles.append((u, len(graph[u]), capacity))
        graph[u].append([v, len(graph[v]), capacity])
        graph[v].append([u, len(graph[u])-1, 0])
    total = 0
    while True:
        level = [-1]*n; level[source] = 0; queue = deque([source])
        while queue:
            u = queue.popleft()
            for v, _, capacity in graph[u]:
                if capacity and level[v] < 0:
                    level[v] = level[u]+1; queue.append(v)
        if level[sink] < 0:
            break
        cursor = [0]*n

        def send(u, amount):
            if u == sink:
                return amount
            while cursor[u] < len(graph[u]):
                edge = graph[u][cursor[u]]
                v, rev, capacity = edge
                if capacity and level[v] == level[u]+1:
                    value = send(v, min(amount, capacity))
                    if value:
                        edge[2] -= value; graph[v][rev][2] += value
                        return value
                cursor[u] += 1
            return 0

        while True:
            amount = send(source, sum(c for _, _, c in graph[source]))
            if not amount:
                break
            total += amount
    return total, [cap-graph[u][k][2] for u, k, cap in handles]


def construct():
    S, B, label, A, nums, P, N, D = original()
    v = [F(x, D) for x in nums]
    abc = S.index(7); J = [i for i in P if i != abc]
    V, alpha = sum(v[i] for i in P), v[abc]
    row_types = sorted({label[s] for s in S})
    col_types = sorted({label[b] for b in B})
    rows = {t: [i for i, s in enumerate(S) if label[s] == t] for t in row_types}
    cols = {t: [j for j, b in enumerate(B) if label[b] == t] for t in col_types}
    cells = {}
    for r in row_types:
        for c in col_types:
            positions = [(i, j) for i in rows[r] for j in cols[c] if not S[i] & B[j]]
            if positions:
                require(len({A[i][j] for i, j in positions}) == 1,
                        'exact identical witness values on every typed allowed cell')
                cells[r, c] = positions
    require(len(row_types) == 10 and len(col_types) == 3 and len(cells) == 23 and
            sum(map(len, cells.values())) == 3906, 'full10 by3 type and3906 cell census')
    certificates = []
    tau = F(1, 256)
    for e in (F(1, 363), F(1, 362)):
        a = alpha-15840*e; b = V-alpha-269280*e; t = a+b
        q = [a if i == abc else b/19 if i in J else -t/38 for i in range(58)]
        row_target = {r: sum(q[i]-v[i] for i in rows[r]) for r in row_types}
        low, high = {}, {}
        for key, positions in cells.items():
            i, j = positions[0]
            low[key] = max(-220*e, tau-1-F(A[i][j], D))
            high[key] = 220*e
            require(low[key] <= high[key], 'exact lower/upper entry interval nonempty')
        supplies = {r: row_target[r]-sum(len(p)*low[r, c]
                                         for (rr, c), p in cells.items() if rr == r)
                    for r in row_types}
        demands = {c: -sum(len(p)*low[r, c]
                           for (r, cc), p in cells.items() if cc == c)
                   for c in col_types}
        require(all(x >= 0 for x in list(supplies.values())+list(demands.values())) and
                sum(supplies.values()) == sum(demands.values()),
                'exact balanced nonnegative typed-flow demands')
        fractional_edges = []
        source, sink = 13, 14
        for r in row_types:
            fractional_edges.append((source, row_types.index(r), supplies[r]))
        cell_edges = {}
        for key, positions in cells.items():
            r, c = key; cell_edges[key] = len(fractional_edges)
            fractional_edges.append((row_types.index(r), 10+col_types.index(c),
                                     len(positions)*(high[key]-low[key])))
        for c in col_types:
            fractional_edges.append((10+col_types.index(c), sink, demands[c]))
        scale = lcm(*(x.denominator for _, _, x in fractional_edges))
        integer_edges = [(u, w, int(x*scale)) for u, w, x in fractional_edges]
        total, values = flow(15, source, sink, integer_edges)
        require(total == sum(supplies.values())*scale,
                'construction completed exact typed transport (failure is not original nonexistence)')
        delta = [[F(0) for _ in B] for _ in S]
        recipe = []
        for key, positions in cells.items():
            change = low[key]+F(values[cell_edges[key]], scale*len(positions))
            for i, j in positions:
                delta[i][j] = change
            recipe.append({'star_type': list(key[0]), 'bad_type': list(key[1]),
                           'original_allowed_positions': len(positions),
                           'C_change': str(change)})
        # Construction is not trusted for its typed equations. Check the lift
        # on ALL original 58 by81 entries, ALL58 rows, and ALL81 columns.
        support_count = 0
        for i, s in enumerate(S):
            for j, bad in enumerate(B):
                change = delta[i][j]
                if s & bad:
                    require(change == 0 and A[i][j] == -D,
                            'ALL original intersecting transport cells fixed')
                else:
                    support_count += 1
                    require(abs(change) <= 220*e and F(A[i][j], D)+change >= tau-1,
                            'ALL3906 original transport displacement and floor bounds')
            require(v[i]+sum(delta[i]) == q[i], 'ALL58 original transported row targets')
        require(support_count == 3906 and sum(q) == 0,
                'full original transported support and aggregate kernel')
        require(all(sum(delta[i][j] for i in range(58)) == 0 for j in range(81)),
                'ALL81 original individual transported column kernels')
        require(q[abc] == a and sum(q[i] for i in J) == b,
                'new subset constraints attained by original transport')
        certificates.append({'e': str(e), 'tau': str(tau), 'q': list(map(str, q)),
                             'recipe_all23_types': recipe,
                             'literal_entry_checks': 4698, 'literal_allowed_floor_checks': 3906,
                             'literal_row_target_checks': 58, 'literal_column_checks': 81,
                             'exact_energy': str(sum(x*x for x in q))})
    return {'actual_agent': 'six-downset-3', 'role': 'researcher',
            'status': 'PRIVATE exact endpoint original transport; ordinary convex bridge required',
            'full_real_endpoint_bridge_interval': ['1/363', '1/362'],
            'largest_floor_tau': str(tau), 'endpoint_certificates': certificates,
            'independent_original_checker': 'check_transport.py (not yet paid by this producer)',
            'original_global_stochastic_PSD_matrix_or_best_distance_claimed': False,
            'independent_mathematical_review_claimed': False}


if __name__ == '__main__':
    print(json.dumps(construct(), indent=2))
