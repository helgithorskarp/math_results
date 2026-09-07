"""Complete matching-edit search; compact covering DAG, not a SAT verdict."""
import json
from itertools import combinations


class BudgetExceeded(RuntimeError):
    pass


class TargetFound(RuntimeError):
    def __init__(self, matching):
        self.matching = list(matching)


def cliques(adj, available, k, prefix=0):
    if k == 0:
        yield prefix
        return
    while available.bit_count() >= k:
        bit = available & -available
        available ^= bit
        v = bit.bit_length() - 1
        yield from cliques(adj, available & adj[v], k - 1, prefix | bit)


class State:
    def __init__(self, n, word, k=5):
        self.n, self.k = n, k
        self.full = (1 << n) - 1
        self.pairs = list(combinations(range(n), 2))
        self.adj = [0] * n
        for i, (u, v) in enumerate(self.pairs):
            if word & (1 << i):
                self.adj[u] |= 1 << v
                self.adj[v] |= 1 << u
        self.bad = set()
        for color in (0, 1):
            self.bad.update(cliques(self.colored(color), self.full, k))

    def colored(self, color):
        if color:
            return self.adj
        return [self.full ^ row ^ (1 << v) for v, row in enumerate(self.adj)]

    def flip(self, e):
        u, v = self.pairs[e]
        old = (self.adj[u] >> v) & 1
        colored = self.colored(old)
        ends = (1 << u) | (1 << v)
        remove = [ends | q for q in cliques(colored, colored[u] & colored[v], self.k - 2)]
        for q in remove:
            if q not in self.bad:
                raise RuntimeError("incremental deletion mismatch")
            self.bad.remove(q)
        self.adj[u] ^= 1 << v
        self.adj[v] ^= 1 << u
        colored = self.colored(1 - old)
        for q in cliques(colored, colored[u] & colored[v], self.k - 2):
            q |= ends
            if q in self.bad:
                raise RuntimeError("incremental insertion mismatch")
            self.bad.add(q)


def decide(n, word, k=5, budget=None):
    """budget is a shared one-element list, decremented for each new DAG node."""
    if not (2 <= k <= n and 0 <= word < (1 << (n * (n - 1) // 2))):
        raise ValueError("invalid graph dimensions/word")
    if budget is None:
        budget = [2_000_000]
    state = State(n, word, k)
    lookup = {e: i for i, e in enumerate(state.pairs)}
    nodes, cache = [], {}
    counts = {"cache_hits": 0, "leaves": 0, "max_depth": 0, "branches": 0}

    def visit(matching, free):
        key = tuple(sorted(matching))
        if key in cache:
            counts["cache_hits"] += 1
            return cache[key]
        if budget[0] == 0:
            raise BudgetExceeded("declared global proof-node budget exhausted")
        budget[0] -= 1
        node_id = len(nodes)
        cache[key] = node_id
        nodes.append(None)
        counts["max_depth"] = max(counts["max_depth"], len(key))
        if not state.bad:
            raise TargetFound(key)
        q = min(state.bad, key=lambda q: ((q & free).bit_count(), q))
        available = [v for v in range(n) if (q & free) & (1 << v)]
        children = []
        for u, v in combinations(available, 2):
            edge = lookup[u, v]
            state.flip(edge)
            try:
                child = visit(key + (edge,), free ^ (1 << u) ^ (1 << v))
            finally:
                state.flip(edge)
            children.append(child)
            counts["branches"] += 1
        if not children:
            counts["leaves"] += 1
        nodes[node_id] = [q, children]
        return node_id

    try:
        root = visit((), state.full)
    except TargetFound as found:
        return {"status": "SAT", "n": n, "k": k, "matching": found.matching, "stats": counts,
                "discovery_nodes": len(nodes)}
    except BudgetExceeded:
        return {"status": "UNKNOWN", "n": n, "k": k, "partial_nodes": nodes,
                "stats": counts, "discovery_nodes": len(nodes)}
    return {"status": "UNSAT", "n": n, "k": k, "root": root, "nodes": nodes,
            "stats": counts, "discovery_nodes": len(nodes)}


def encode(data):
    return (json.dumps(data, separators=(",", ":"), sort_keys=True) + "\n").encode()
