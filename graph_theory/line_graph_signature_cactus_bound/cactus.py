"""Exact rooted states and cactus reduction; Python 3.11+, standard library."""
from dataclasses import dataclass
from fractions import Fraction as F


def need(condition, message):
    if not condition:
        raise ValueError(message)


def inertia(matrix):
    """Symmetric rational elimination with 1x1 and hyperbolic 2x2 pivots."""
    a = [list(map(F, row)) for row in matrix]
    n = len(a)
    need(all(len(row) == n for row in a), 'matrix is not square')
    need(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)),
         'matrix is not symmetric')
    p = z = m = 0
    while a:
        n = len(a)
        i = next((i for i in range(n) if a[i][i]), None)
        if i is not None:
            order = [i] + [j for j in range(n) if j != i]
            a = [[a[u][v] for v in order] for u in order]
            d = a[0][0]
            p += d > 0
            m += d < 0
            a = [[a[u][v] - a[u][0]*a[0][v]/d
                  for v in range(1, n)] for u in range(1, n)]
            continue
        pair = next(((i, j) for i in range(n) for j in range(i+1, n)
                     if a[i][j]), None)
        if pair is None:
            z += n
            break
        i, j = pair
        order = [i, j] + [k for k in range(n) if k not in (i, j)]
        a = [[a[u][v] for v in order] for u in order]
        d = a[0][1]
        a = [[a[u][v] - (a[u][0]*a[1][v]+a[u][1]*a[0][v])/d
              for v in range(2, n)] for u in range(2, n)]
        p += 1
        m += 1
    return p, z, m


def response(matrix, root=0):
    """None means e_root not in range; otherwise return the exact response."""
    n = len(matrix)
    need(0 <= root < n, 'invalid root')
    a = [list(map(F, row)) + [F(i == root)]
         for i, row in enumerate(matrix)]
    pivots = []
    row = 0
    for col in range(n):
        i = next((i for i in range(row, n) if a[i][col]), None)
        if i is None:
            continue
        a[row], a[i] = a[i], a[row]
        d = a[row][col]
        a[row] = [x/d for x in a[row]]
        for j in range(n):
            if j != row and a[j][col]:
                q = a[j][col]
                a[j] = [x-q*y for x, y in zip(a[j], a[row])]
        pivots.append(col)
        row += 1
    if any(not any(r[:n]) and r[n] for r in a):
        return None
    x = [F(0)]*n
    for i, col in enumerate(pivots):
        x[col] = a[i][n]
    need(all(sum(F(matrix[i][j])*x[j] for j in range(n)) == (i == root)
             for i in range(n)), 'range solve failed')
    return x[root]


@dataclass(frozen=True)
class Graph:
    n: int
    edges: tuple

    def __post_init__(self):
        need(isinstance(self.n, int) and self.n >= 1, 'invalid graph order')
        out = []
        for edge in self.edges:
            need(len(edge) == 2, 'malformed edge')
            u, v = edge
            need(isinstance(u, int) and isinstance(v, int)
                 and 0 <= u < self.n and 0 <= v < self.n and u != v,
                 'invalid simple edge')
            out.append(tuple(sorted((u, v))))
        need(len(set(out)) == len(out), 'duplicate edge')
        object.__setattr__(self, 'edges', tuple(sorted(out)))

    def adjacency(self):
        a = [set() for _ in range(self.n)]
        for u, v in self.edges:
            a[u].add(v)
            a[v].add(u)
        return a

    def connected(self):
        a = self.adjacency()
        seen, todo = {0}, [0]
        while todo:
            for v in a[todo.pop()]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        return len(seen) == self.n

    def c(self):
        need(self.connected(), 'cyclomatic number requires connectivity')
        return len(self.edges)-self.n+1

    def matrix(self, root=None):
        a = [[0]*self.n for _ in range(self.n)]
        for i in range(self.n):
            a[i][i] = -2
        for u, v in self.edges:
            a[u][u] += 1
            a[v][v] += 1
            a[u][v] = a[v][u] = 1
        if root is not None:
            need(0 <= root < self.n, 'invalid root')
            a[root][root] += 1
        return a

    def line_matrix(self):
        return [[int(i != j and bool(set(e) & set(f)))
                 for j, f in enumerate(self.edges)]
                for i, e in enumerate(self.edges)]


def blocks(g):
    """Tarjan edge blocks, rejecting every non-cactus or disconnected graph."""
    need(g.connected(), 'disconnected graph')
    adj = g.adjacency()
    disc = [-1]*g.n
    low = [0]*g.n
    stack, out = [], []
    clock = 0

    def visit(u, parent):
        nonlocal clock
        disc[u] = low[u] = clock
        clock += 1
        for v in sorted(adj[u]):
            if v == parent:
                continue
            e = tuple(sorted((u, v)))
            if disc[v] == -1:
                stack.append(e)
                visit(v, u)
                low[u] = min(low[u], low[v])
                if low[v] >= disc[u]:
                    block = []
                    while True:
                        f = stack.pop()
                        block.append(f)
                        if f == e:
                            break
                    out.append(tuple(sorted(block)))
            elif disc[v] < disc[u]:
                stack.append(e)
                low[u] = min(low[u], disc[v])

    visit(0, -1)
    need(not stack, 'unfinished block stack')
    for block in out:
        if len(block) == 1:
            continue
        degrees = {}
        for u, v in block:
            degrees[u] = degrees.get(u, 0)+1
            degrees[v] = degrees.get(v, 0)+1
        need(len(block) == len(degrees) and all(d == 2 for d in degrees.values()),
             'graph is not a cactus')
    return tuple(sorted(out))


def split(g, v, group):
    group = set(group)
    adj = g.adjacency()
    need(0 <= v < g.n and group and group < adj[v], 'invalid split')
    # v is the first endpoint, n is the second, then n+1,n+2,n+3.
    w, p, q, r = range(g.n, g.n+4)
    es = []
    for u, z in g.edges:
        if v not in (u, z):
            es.append((u, z))
        else:
            x = z if u == v else u
            es.append((v if x in group else w, x))
    es.extend(((v, p), (p, q), (q, r), (r, w)))
    return Graph(g.n+4, tuple(es))


def prepare(g):
    """Return a subcubic cactus and an off-cycle root, or None for a cycle."""
    blocks(g)
    trace = []
    while True:
        adj = g.adjacency()
        v = next((v for v in range(g.n) if len(adj[v]) >= 4), None)
        if v is None:
            break
        cyc = next((b for b in blocks(g) if len(b) > 1
                    and any(v in e for e in b)), None)
        group = sorted(next(iter(set(e)-{v})) for e in cyc if v in e) if cyc else sorted(adj[v])[:2]
        trace.append({'operation': 'split', 'vertex': v, 'group': group})
        g = split(g, v, group)
    bs = blocks(g)
    oncycle = {v for b in bs if len(b) > 1 for e in b for v in e}
    root = next((v for v in range(g.n) if v not in oncycle), None)
    if root is None:
        bridge = next((b[0] for b in bs if len(b) == 1), None)
        if bridge is None:
            return g, None, trace
        u, v = bridge
        path = [u]+list(range(g.n, g.n+4))+[v]
        es = [e for e in g.edges if e != bridge]
        es.extend(zip(path, path[1:]))
        root = g.n
        trace.append({'operation': 'four_subdivide', 'edge': [u, v]})
        g = Graph(g.n+4, tuple(es))
    return g, root, trace


@dataclass(frozen=True)
class State:
    cycles: int
    inert: tuple
    rho: object  # Fraction, or None for an active root pole

    @property
    def sigma(self):
        return self.inert[0]-self.inert[2]

    @property
    def charge(self):
        return 3*self.cycles-2*self.sigma

    def validate(self):
        k = self.charge
        need(k >= 0 and min(self.inert) >= 0, 'negative charge or inertia')
        if self.rho is None:
            need(k >= 1, 'zero-charge pole')
        elif k <= 2:
            need(self.rho >= 1-k, 'root-response bound failed')
        return self


def add_inertias(states):
    return [sum(s.inert[i] for s in states) for i in range(3)]


def bridge_state(children):
    c = sum(s.cycles for s in children)
    p, z, m = add_inertias(children)
    if any(s.rho is None for s in children):
        return State(c, (p+1, z-1, m+1), F(0))
    a = len(children)-1-sum((s.rho for s in children), F(0))
    return State(c, (p+(a > 0), z+(a == 0), m+(a < 0)),
                 1/a if a else None)


def cycle_state(children):
    """children[i] attaches at cycle vertex i+1; root is cycle vertex 0."""
    n = len(children)+1
    need(n >= 3, 'cycle is too short')
    a = [[F(0)]*n for _ in range(n)]
    a[0][0] = F(1)
    for i in range(n):
        a[i][(i+1) % n] = a[(i+1) % n][i] = F(1)
    poles = set()
    states = [s for s in children if s is not None]
    for i, s in enumerate(children, 1):
        if s is None:
            continue
        if s.rho is None:
            poles.add(i)
        else:
            a[i][i] += 1-s.rho
    keep = [i for i in range(n) if i not in poles]
    b = [[a[i][j] for j in keep] for i in keep]
    p, z, m = add_inertias(states)
    ip, iz, im = inertia(b)
    return State(1+sum(s.cycles for s in states),
                 (p+len(poles)+ip, z-len(poles)+iz, m+len(poles)+im),
                 response(b))


def rooted_state(g, root, trace=None):
    """Exact recursion. Whole root must be off cycles unless g is one cycle."""
    bs = blocks(g)
    adj = g.adjacency()
    need(max(map(len, adj)) <= 3, 'rooted recursion requires subcubic input')
    cycle_at = {}
    for block in bs:
        if len(block) <= 1:
            continue
        ca = {}
        for u, v in block:
            ca.setdefault(u, []).append(v)
            ca.setdefault(v, []).append(u)
        for u in ca:
            need(u not in cycle_at, 'cycles are not vertex disjoint')
            cycle_at[u] = ca
    visited = set()

    def visit(u, parent):
        need(u not in visited, 'repeated recursive vertex')
        ca = cycle_at.get(u)
        if ca is None:
            visited.add(u)
            children = [visit(v, u) for v in sorted(adj[u]) if v != parent]
            state = bridge_state(children)
            kind = 'bridge'
        else:
            need(adj[u]-set(ca[u]) <= ({parent} if parent is not None else set()),
                 'cycle root has an extra child')
            order = [u]
            prev, cur = u, min(ca[u])
            while cur != u:
                order.append(cur)
                prev, cur = cur, next(v for v in ca[cur] if v != prev)
            need(not (set(order) & visited), 'repeated cycle')
            visited.update(order)
            children = []
            for v in order[1:]:
                off = adj[v]-set(ca[v])
                need(len(off) <= 1, 'multiple cycle children')
                children.append(visit(next(iter(off)), v) if off else None)
            state = cycle_state(children)
            kind = 'cycle'
        state.validate()
        if trace is not None:
            trace.append({'root': u, 'kind': kind, 'cycles': state.cycles,
                          'inertia': state.inert, 'charge': state.charge,
                          'response': None if state.rho is None else str(state.rho)})
        return state

    need(0 <= root < g.n, 'invalid root')
    state = visit(root, None)
    need(len(visited) == g.n, 'incomplete recursion')
    need(sum(state.inert) == g.n and state.cycles == g.c(), 'recursive size mismatch')
    return state


def attach_cycle(g, root, length):
    need(0 <= root < g.n and length >= 3, 'invalid cycle attachment')
    path = [root]+list(range(g.n, g.n+length-1))+[root]
    return Graph(g.n+length-1, g.edges+tuple(zip(path, path[1:])))


def attach_leaf(g, root):
    need(0 <= root < g.n, 'invalid leaf attachment')
    return Graph(g.n+1, g.edges+((root, g.n),))


MODULE_EDGES = ((0, 1), (1, 2), (2, 3), (3, 0),
                (4, 5), (5, 6), (6, 7), (7, 8), (8, 4), (0, 4), (1, 9))


def attach_module(g, root):
    need(0 <= root < g.n, 'invalid module attachment')
    mapping = list(range(g.n, g.n+9))+[root]
    return Graph(g.n+9, g.edges+tuple((mapping[u], mapping[v]) for u, v in MODULE_EDGES))
