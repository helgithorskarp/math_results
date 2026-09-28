#!/usr/bin/env python3
"""Independent simple-path audit of the three-port trace reduction."""

from itertools import combinations


C = (0, 1, 2, 3)
PORTS = (0, 1, 2)
EDGES = (
    (0, 3), (3, 1), (3, 2),
    (0, 4), (4, 1), (1, 5), (5, 2), (4, 5),
    (0, 6), (6, 2), (4, 2),
)


def graph(mask):
    adj = [set() for _ in range(7)]
    for j, (a, b) in enumerate(EDGES):
        if mask >> j & 1:
            adj[a].add(b)
            adj[b].add(a)
    return adj


def simple_paths(adj, source, target, permitted):
    """Enumerate paths directly; no shortest-path routine is shared with source."""
    stack = [(source, (source,), 1 << source)]
    while stack:
        here, path, seen = stack.pop()
        if here == target:
            yield path
            continue
        for nxt in adj[here]:
            if nxt in permitted and not (seen >> nxt & 1):
                stack.append((nxt, path + (nxt,), seen | (1 << nxt)))


def exterior_lengths(adj):
    result = {}
    for a, b in combinations(PORTS, 2):
        paths = simple_paths(adj, a, b, set(range(4, 7)) | {a, b})
        lengths = [len(p) - 1 for p in paths if len(p) >= 3]
        result[a, b] = min(lengths) if lengths else None
    return result


def closure(adj, lengths):
    out = [set(adj[v] & set(C)) for v in C]
    for (a, b), length in lengths.items():
        if length is None:
            continue
        path = [a]
        for _ in range(length - 1):
            path.append(len(out))
            out.append(set())
        path.append(b)
        for u, v in zip(path, path[1:]):
            out[u].add(v)
            out[v].add(u)
    return out


def signatures(adj):
    """For every ordered C pair, return distance and every shortest C trace."""
    answer = {}
    for a in C:
        for b in C:
            paths = list(simple_paths(adj, a, b, set(range(len(adj)))))
            if not paths:
                answer[a, b] = (None, frozenset())
                continue
            minimum = min(len(p) - 1 for p in paths)
            traces = frozenset(frozenset(v for v in p if v in C)
                               for p in paths if len(p) - 1 == minimum)
            answer[a, b] = (minimum, traces)
    return answer


def main():
    nonmetric = 0
    comparisons = 0
    for mask in range(1 << len(EDGES)):
        host = graph(mask)
        lengths = exterior_lengths(host)
        ab, ac, bc = (lengths[0, 1], lengths[0, 2], lengths[1, 2])
        if ab is not None and bc is not None and (ac is None or ac > ab + bc):
            nonmetric += 1
        left = signatures(host)
        right = signatures(closure(host, lengths))
        assert left == right, (mask, lengths, left, right)
        comparisons += len(left)
    assert nonmetric > 0
    print(f"states={1 << len(EDGES)} ordered_C_pairs={comparisons} "
          f"nonmetric_states={nonmetric} PASS")


if __name__ == "__main__":
    main()
