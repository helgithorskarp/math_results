#!/usr/bin/env python3
"""Exact audits for the remote-resolver theorem (standard library only)."""

from __future__ import annotations

from collections import defaultdict, deque
from itertools import product


Graph = tuple[frozenset[int], ...]


def validate_graph(graph: Graph) -> None:
    n = len(graph)
    if n < 2:
        raise ValueError("the base graph must have at least two vertices")
    for v, nbrs in enumerate(graph):
        if v in nbrs or any(w < 0 or w >= n for w in nbrs):
            raise ValueError("graph must be simple")
        if any(v not in graph[w] for w in nbrs):
            raise ValueError("adjacency must be symmetric")
    seen = {0}
    queue = deque([0])
    while queue:
        v = queue.popleft()
        for w in graph[v] - seen:
            seen.add(w)
            queue.append(w)
    if len(seen) != n:
        raise ValueError("graph must be connected")


def distances(graph: Graph, source: int) -> tuple[int, ...]:
    dist = [-1] * len(graph)
    dist[source] = 0
    queue = deque([source])
    while queue:
        v = queue.popleft()
        for w in graph[v]:
            if dist[w] == -1:
                dist[w] = dist[v] + 1
                queue.append(w)
    if -1 in dist:
        raise ValueError("graph must be connected")
    return tuple(dist)


def full_response(graph: Graph, probe: int, target: int) -> frozenset[int]:
    if probe == target:
        return frozenset({probe})
    distance_to_target = distances(graph, target)
    wanted = distance_to_target[probe] - 1
    return frozenset(w for w in graph[probe] if distance_to_target[w] == wanted)


def remote_signatures(graph: Graph, p: int) -> dict[int, frozenset[int]]:
    validate_graph(graph)
    domain = [p] + [
        q for q in range(len(graph)) if q != p and q not in graph[p]
    ]
    return {
        q: graph[p] if q == p else full_response(graph, p, q)
        for q in domain
    }


def remote_resolvers(graph: Graph) -> tuple[int, ...]:
    result = []
    for p in range(len(graph)):
        values = list(remote_signatures(graph, p).values())
        if len(values) == len(set(values)):
            result.append(p)
    return tuple(result)


def cycle(n: int) -> Graph:
    if n < 3:
        raise ValueError("a simple cycle needs at least three vertices")
    return tuple(frozenset({(v - 1) % n, (v + 1) % n}) for v in range(n))


def graph_from_mask(n: int, mask: int) -> Graph:
    nbrs = [set() for _ in range(n)]
    bit = 0
    for u in range(n):
        for v in range(u + 1, n):
            if mask & (1 << bit):
                nbrs[u].add(v)
                nbrs[v].add(u)
            bit += 1
    return tuple(frozenset(s) for s in nbrs)


def is_connected(graph: Graph) -> bool:
    if not graph:
        return False
    seen = {0}
    queue = deque([0])
    while queue:
        v = queue.popleft()
        for w in graph[v] - seen:
            seen.add(w)
            queue.append(w)
    return len(seen) == len(graph)


def independent_blowup(
    base: Graph, sizes: tuple[int, ...]
) -> tuple[Graph, tuple[int, ...], tuple[tuple[int, ...], ...]]:
    validate_graph(base)
    if len(sizes) != len(base) or any(size < 2 for size in sizes):
        raise ValueError("one module size >= 2 is required for each base vertex")
    modules: list[tuple[int, ...]] = []
    owner: list[int] = []
    cursor = 0
    for q, size in enumerate(sizes):
        module = tuple(range(cursor, cursor + size))
        modules.append(module)
        owner.extend([q] * size)
        cursor += size
    nbrs = [set() for _ in owner]
    for q, module in enumerate(modules):
        for r in base[q]:
            for x in module:
                nbrs[x].update(modules[r])
    return (
        tuple(frozenset(s) for s in nbrs),
        tuple(owner),
        tuple(modules),
    )


def recontaminate(graph: Graph, territory: frozenset[int]) -> frozenset[int]:
    expanded = set(territory)
    for v in territory:
        expanded.update(graph[v])
    return frozenset(expanded)


def response_classes(
    graph: Graph, probe: int, territory: frozenset[int]
) -> tuple[frozenset[int], ...]:
    classes: dict[frozenset[int], set[int]] = defaultdict(set)
    for target in territory:
        classes[full_response(graph, probe, target)].add(target)
    return tuple(frozenset(cls) for cls in classes.values())


def audit_scan_strategy(
    graph: Graph,
    owner: tuple[int, ...],
    module: tuple[int, ...],
    territory: frozenset[int],
    scan_index: int = 0,
) -> None:
    """Audit every response branch of the fixed scan of one known module."""
    if scan_index == len(module):
        raise AssertionError("scan ended with unresolved territory")
    probe = module[scan_index]
    for cls in response_classes(graph, probe, territory):
        if len(cls) == 1:
            continue
        if {owner[v] for v in cls} != {owner[module[0]]}:
            raise AssertionError("a continuing response escaped the known module")
        audit_scan_strategy(
            graph,
            owner,
            module,
            recontaminate(graph, cls),
            scan_index + 1,
        )


def audit_remote_resolver_strategy(
    base: Graph, sizes: tuple[int, ...], p: int
) -> None:
    if p not in remote_resolvers(base):
        raise ValueError("the chosen base vertex is not a remote resolver")
    graph, owner, modules = independent_blowup(base, sizes)
    first_probe = modules[p][0]
    all_vertices = frozenset(range(len(graph)))
    for cls in response_classes(graph, first_probe, all_vertices):
        if len(cls) == 1:
            continue
        module_indices = {owner[v] for v in cls}
        if len(module_indices) != 1:
            raise AssertionError("first probe did not identify a unique module")
        q = next(iter(module_indices))
        audit_scan_strategy(
            graph, owner, modules[q], recontaminate(graph, cls)
        )


def first_probe_identifies_modules(
    base: Graph, sizes: tuple[int, ...], p: int
) -> bool:
    """Whether one clone in M_p locates or identifies the target module."""
    graph, owner, modules = independent_blowup(base, sizes)
    classes = response_classes(
        graph, modules[p][0], frozenset(range(len(graph)))
    )
    return all(
        len(cls) == 1 or len({owner[v] for v in cls}) == 1
        for cls in classes
    )


def audit_c5_base() -> None:
    graph = cycle(5)
    pairs = {
        target: (full_response(graph, 0, target), full_response(graph, 1, target))
        for target in range(5)
    }
    if len(set(pairs.values())) != 5:
        raise AssertionError("two consecutive probes do not resolve C5")

    block = frozenset({0, 1, 2, 3})
    for probe in range(5):
        classes = response_classes(graph, probe, block)
        if not any(
            len(cls) == 2
            and any((v + 1) % 5 in cls for v in cls)
            and len(recontaminate(graph, cls)) == 4
            for cls in classes
        ):
            raise AssertionError("the four-vertex robber invariant failed")


def exhaustive_small_graph_audit() -> tuple[int, int, int]:
    connected_count = 0
    resolver_graph_count = 0
    resolver_instance_count = 0
    for n in range(2, 6):
        edge_count = n * (n - 1) // 2
        for mask in range(1 << edge_count):
            graph = graph_from_mask(n, mask)
            if not is_connected(graph):
                continue
            connected_count += 1
            resolvers = remote_resolvers(graph)
            if resolvers:
                resolver_graph_count += 1
            for p in range(n):
                criterion = first_probe_identifies_modules(graph, (2,) * n, p)
                if criterion != (p in resolvers):
                    raise AssertionError("exact first-probe criterion failed")
                if p in resolvers:
                    resolver_instance_count += 1
                    audit_remote_resolver_strategy(graph, (2,) * n, p)
    return connected_count, resolver_graph_count, resolver_instance_count


def main() -> None:
    cycle_orders = tuple(
        n for n in range(3, 51) if remote_resolvers(cycle(n))
    )
    if cycle_orders != (3, 5):
        raise AssertionError("cycle classification audit failed")

    audit_c5_base()
    connected, with_resolver, instances = exhaustive_small_graph_audit()

    c5 = cycle(5)
    size_vectors = 0
    for sizes in product(range(2, 5), repeat=5):
        size_vectors += 1
        for p in remote_resolvers(c5):
            audit_remote_resolver_strategy(c5, sizes, p)

    print("remote-resolver audit: PASS")
    print("cycle orders 3..50 with a remote resolver: 3, 5")
    print(f"connected labelled graphs of orders 2..5 checked: {connected}")
    print(f"graphs with at least one remote resolver: {with_resolver}")
    print(f"remote-resolver vertex instances checked at size 2: {instances}")
    print(f"C5 size vectors in {{2,3,4}}^5 checked: {size_vectors}")
    print("C5 base lower/upper response audits: PASS")


if __name__ == "__main__":
    main()
