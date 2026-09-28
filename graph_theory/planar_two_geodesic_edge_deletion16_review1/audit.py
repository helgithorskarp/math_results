"""Independent sample checker for the order-16 witness-edge induction.

Input: graph6 records of hard order-16 triangulations. Standard Python only.
The routines here do not import the researcher's graph or search code.
"""
import argparse
import hashlib
import itertools
import json
from collections import deque
from pathlib import Path


def decode(line):
    if line.startswith(b">>graph6<<"):
        line = line[10:]
    assert len(line) == 21 and line[0] == 79
    bits = []
    for char in line[1:]:
        assert 63 <= char <= 126
        bits.extend((char - 63 >> shift) & 1 for shift in range(5, -1, -1))
    assert len(bits) == 120
    adj = [0] * 16
    k = 0
    for v in range(1, 16):
        for u in range(v):
            if bits[k]:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
            k += 1
    assert sum(x.bit_count() for x in adj) == 84
    return tuple(adj)


def vertices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


def distances(adj):
    result = []
    for start in range(16):
        d = [-1] * 16
        d[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in vertices(adj[u]):
                if d[v] < 0:
                    d[v] = d[u] + 1
                    queue.append(v)
        result.append(d)
    return result


def balanced(adj, removed):
    unseen = ((1 << 16) - 1) & ~removed
    while unseen:
        seed = unseen & -unseen
        unseen -= seed
        queue = seed
        count = 0
        while queue:
            bit = queue & -queue
            queue -= bit
            count += 1
            if count > 8:
                return False
            u = bit.bit_length() - 1
            fresh = adj[u] & unseen
            queue |= fresh
            unseen &= ~fresh
    return True


FOUR_SETS = [sum(1 << v for v in combo)
             for combo in itertools.combinations(range(16), 4)]


def terminal(adj):
    if any(balanced(adj, cut) for cut in FOUR_SETS):
        return "four_cut", None
    d = distances(adj)
    if any(x < 0 or x >= 4 for row in d for x in row):
        return "diameter", None
    return "hard", d


def geodesics(adj, d):
    paths = [(1 << u, frozenset()) for u in range(16)]
    for s in range(16):
        for t in range(s + 1, 16):
            stack = [(s, (s,))]
            while stack:
                u, path = stack.pop()
                if u == t:
                    edges = frozenset((min(a, b), max(a, b))
                                      for a, b in zip(path, path[1:]))
                    paths.append((sum(1 << v for v in path), edges))
                    continue
                for v in vertices(adj[u]):
                    if d[s][v] == d[s][u] + 1 and d[s][v] + d[v][t] == d[s][t]:
                        stack.append((v, path + (v,)))
    return paths


def remove_edge(adj, edge):
    u, v = edge
    child = list(adj)
    child[u] &= ~(1 << v)
    child[v] &= ~(1 << u)
    return tuple(child)


def audit_roots(lines, selected):
    proven = set()
    counts = {"sampled_roots": len(selected), "states": 0,
              "max_depth": 0, "terminal_children": 0,
              "pairs_tested": 0}

    def prove(adj, depth):
        if adj in proven:
            return
        counts["states"] += 1
        counts["max_depth"] = max(counts["max_depth"], depth)
        status, d = terminal(adj)
        if status != "hard":
            counts["terminal_children"] += 1
            proven.add(adj)
            return
        easy = set()
        for u in range(16):
            for v in vertices(adj[u] & ~((1 << (u + 1)) - 1)):
                edge = (u, v)
                child = remove_edge(adj, edge)
                if child in proven or terminal(child)[0] != "hard":
                    easy.add(edge)
        paths = geodesics(adj, d)
        best = None
        best_score = (7, 7)
        for i, (m1, e1) in enumerate(paths):
            for m2, e2 in paths[i:]:
                edges = e1 | e2
                score = (len(edges - easy), len(edges))
                if score >= best_score:
                    continue
                counts["pairs_tested"] += 1
                if balanced(adj, m1 | m2):
                    best, best_score = edges, score
                    if score[0] == 0:
                        break
            if best_score[0] == 0:
                break
        assert best is not None, "no geodesic-pair witness"
        for edge in sorted(best - easy):
            prove(remove_edge(adj, edge), depth + 1)
        proven.add(adj)

    for index in selected:
        adj = decode(lines[index])
        assert terminal(adj)[0] == "hard"
        prove(adj, 0)
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("hard_graph6", type=Path)
    args = parser.parse_args()
    raw = args.hard_graph6.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    assert sha == "a1ee18fc00018b938e76cf40925df78f5b69d86f41788babceb04af139e69c92"
    lines = raw.splitlines()
    assert len(lines) == 399
    selected = sorted(set(range(8)) | set(range(17, len(lines), 37)))
    counts = audit_roots(lines, selected)
    print(json.dumps({"input_sha256": sha, **counts}, sort_keys=True))


if __name__ == "__main__":
    main()
