"""Independent literal checker of every physical covering-DAG node and branch."""
from itertools import combinations


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dense(n, word):
    require(type(n) is int and n >= 2, "order")
    require(type(word) is int and 0 <= word < 2**(n * (n - 1) // 2), "graph word")
    g = [[0] * n for _ in range(n)]
    bit = 0
    for u in range(n):
        for v in range(u + 1, n):
            g[u][v] = g[v][u] = (word // 2**bit) % 2
            bit += 1
    return g


def bad_sets(g, k):
    answer = []
    for q in combinations(range(len(g)), k):
        values = {g[u][v] for u, v in combinations(q, 2)}
        if len(values) == 1:
            answer.append((q, next(iter(values))))
    return answer


def check(n, word, proof, k=5):
    g = dense(n, word)
    require(type(k) is int and 2 <= k <= n, "clique order")
    require(type(proof) is dict and proof.get("n") == n and proof.get("k") == k, "certificate dimensions")
    pairs = list(combinations(range(n), 2))
    index = {pair: i for i, pair in enumerate(pairs)}
    if proof.get("status") == "SAT":
        m = proof.get("matching")
        require(type(m) is list and m == sorted(set(m)) and
                all(type(i) is int and 0 <= i < len(pairs) for i in m), "matching syntax")
        used = set()
        for i in m:
            u, v = pairs[i]
            require(u not in used and v not in used, "matching has repeated endpoint")
            used.update((u, v))
            g[u][v] ^= 1
            g[v][u] ^= 1
        require(not bad_sets(g, k), "false physical SAT witness")
        return {"status": "VERIFIED_PHYSICAL_TARGET", "matching_size": len(m)}
    require(proof.get("status") == "UNSAT", "unproved status")
    nodes = proof.get("nodes")
    require(type(nodes) is list and nodes and proof.get("root") == 0, "root/node syntax")
    states = {}
    visited = set()
    counts = {"nodes": 0, "leaves": 0, "branches": 0, "shared_references": 0, "max_depth": 0,
              "literal_pair_checks": 0}

    def walk(i, selected, used):
        require(type(i) is int and 0 <= i < len(nodes), "node reference")
        require(i not in visited or states[i] == selected, "shared node has different matching")
        if i in visited:
            counts["shared_references"] += 1
            return
        # Every reference adds an edge; revisiting a pending node cannot have
        # the same state. Record before children to reject cycles as well.
        require(i not in states or states[i] == selected, "cyclic or inconsistent node")
        states[i] = selected
        node = nodes[i]
        require(type(node) is list and len(node) == 2, "node syntax")
        mask, children = node
        require(type(mask) is int and 0 < mask < 2**n and mask.bit_count() == k, "obstruction mask")
        require(type(children) is list, "children syntax")
        q = [v for v in range(n) if (mask // 2**v) % 2]
        values = [g[u][v] for u, v in combinations(q, 2)]
        require(all(c == values[0] for c in values), "node five-set is not monochromatic")
        counts["literal_pair_checks"] += len(values)
        available = [(u, v) for u, v in combinations(q, 2) if u not in used and v not in used]
        require(len(children) == len(available), "branch coverage failure")
        counts["nodes"] += 1
        counts["max_depth"] = max(counts["max_depth"], len(selected))
        if not available:
            counts["leaves"] += 1
        for (u, v), child in zip(available, children):
            counts["branches"] += 1
            e = index[u, v]
            g[u][v] ^= 1
            g[v][u] ^= 1
            walk(child, tuple(sorted(selected + (e,))), used | {u, v})
            g[u][v] ^= 1
            g[v][u] ^= 1
        visited.add(i)

    walk(0, (), set())
    require(visited == set(range(len(nodes))), "unreachable or unfinished proof node")
    return dict(counts, status="VERIFIED_COMPLETE_MATCHING_FAMILY_EXCLUSION")
