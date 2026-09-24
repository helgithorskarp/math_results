"""Constructive exact reduction; standard-library Python 3.11.

Vertices are consecutive integers, edges are distinct sorted pairs.
No spectral calculation is used to select a transformation.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Graph:
    order: int
    edges: tuple[tuple[int, int], ...]

    def __post_init__(self):
        if type(self.order) is not int or self.order < 1:
            raise ValueError("positive integer order required")
        if tuple(sorted(set(self.edges))) != self.edges:
            raise ValueError("edges must be sorted and distinct")
        if any(type(u) is not int or type(v) is not int or
               not 0 <= u < v < self.order for u, v in self.edges):
            raise ValueError("invalid simple edge")

    def neighbors(self):
        result = [set() for _ in range(self.order)]
        for u, v in self.edges:
            result[u].add(v)
            result[v].add(u)
        return result

    def connected(self):
        adj = self.neighbors()
        seen = {0}
        todo = [0]
        while todo:
            for v in adj[todo.pop()]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        return len(seen) == self.order

    def cyclomatic(self):
        if not self.connected():
            raise ValueError("connected graph required")
        return len(self.edges) - self.order + 1


def make_graph(order, edges):
    normalized = [tuple(sorted(e)) for e in edges]
    # Deliberately do not silently remove repeated edges.
    return Graph(order, tuple(sorted(normalized)))


# Vertex 9 is the root leaf, edge (1,9) is the root edge.
MODULE = make_graph(10, [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 8), (8, 4),
    (0, 4), (1, 9),
])


def split_vertex(graph, vertex, left):
    """Split one vertex into two, linked by a path of length four.

The old vertex retains the neighbors in left. Its other neighbors move to
new vertex n. Internal path vertices are n+1,n+2,n+3.
"""
    if not 0 <= vertex < graph.order:
        raise ValueError("invalid split vertex")
    neighbors = graph.neighbors()[vertex]
    left = set(left)
    if not left or not left < neighbors:
        raise ValueError("nonempty proper neighbor partition required")
    n = graph.order
    edges = []
    for u, v in graph.edges:
        if vertex not in (u, v):
            edges.append((u, v))
        else:
            w = v if u == vertex else u
            edges.append((vertex if w in left else n, w))
    edges.extend([(vertex, n+1), (n+1, n+2), (n+2, n+3), (n+3, n)])
    return make_graph(n+4, edges)


def attach_module(graph, vertex):
    """Identify the module root leaf with vertex; add nine vertices."""
    if not 0 <= vertex < graph.order:
        raise ValueError("invalid attachment vertex")
    labels = list(range(graph.order, graph.order+9)) + [vertex]
    return make_graph(graph.order+9, list(graph.edges) +
                      [(labels[u], labels[v]) for u, v in MODULE.edges])


def four_subdivide(graph, edge):
    """Replace one edge by a path of length five."""
    edge = tuple(sorted(edge))
    if edge not in graph.edges:
        raise ValueError("missing subdivision edge")
    u, v = edge
    n = graph.order
    path = [u, n, n+1, n+2, n+3, v]
    return make_graph(n+4, [e for e in graph.edges if e != edge] +
                      list(zip(path, path[1:])))


def to_core(graph):
    """Return subcubic 2-core plus a complete deterministic move trace.

A connected nontrivial cycle is returned unchanged. A singleton is outside
this construction. Other inputs give cyclomatic number at least two.
"""
    if not graph.connected() or graph.order < 2:
        raise ValueError("connected graph of order at least two required")
    trace = []
    current = graph
    while True:
        adj = current.neighbors()
        high = next((v for v, row in enumerate(adj) if len(row) >= 4), None)
        if high is None:
            break
        left = sorted(adj[high])[:2]
        trace.append({"move": "split", "vertex": high, "left": left})
        current = split_vertex(current, high, left)
    leaves = [v for v, row in enumerate(current.neighbors()) if len(row) == 1]
    for vertex in leaves:
        trace.append({"move": "cap", "vertex": vertex})
        current = attach_module(current, vertex)
    degrees = [len(row) for row in current.neighbors()]
    if not current.connected() or min(degrees) < 2 or max(degrees) > 3:
        raise RuntimeError("construction failed to produce a subcubic core")
    return current, trace


def branch_paths(graph):
    """Extract all maximal degree-two paths, including returning loops."""
    adj = graph.neighbors()
    if not graph.connected() or any(len(row) not in (2, 3) for row in adj):
        raise ValueError("connected subcubic 2-core required")
    branch = [v for v, row in enumerate(adj) if len(row) == 3]
    if not branch:
        raise ValueError("a cycle has no cubic kernel")
    index = {v: i for i, v in enumerate(branch)}
    unused = set(graph.edges)
    paths = []
    for u in branch:
        for start in sorted(adj[u]):
            if tuple(sorted((u, start))) not in unused:
                continue
            route = [u, start]
            unused.remove(tuple(sorted((u, start))))
            previous, current = u, start
            while current not in index:
                onward = adj[current] - {previous}
                if len(onward) != 1:
                    raise RuntimeError("invalid internal path vertex")
                following = next(iter(onward))
                unused.remove(tuple(sorted((current, following))))
                route.append(following)
                previous, current = current, following
            paths.append((index[u], index[current], len(route)-1))
    if unused:
        raise RuntimeError("uncovered edges in path extraction")
    return tuple(branch), tuple(paths)


def realize(branch_count, paths):
    """Expand a pseudokernel with explicitly supplied positive path lengths."""
    if type(branch_count) is not int or branch_count < 2:
        raise ValueError("at least two branch vertices required")
    degrees = [0]*branch_count
    edges = []
    n = branch_count
    for u, v, length in paths:
        if (type(u) is not int or type(v) is not int or
            not 0 <= u < branch_count or not 0 <= v < branch_count or
            type(length) is not int or length < (3 if u == v else 1)):
            raise ValueError("invalid kernel path")
        degrees[u] += 1
        degrees[v] += 1
        route = [u] + list(range(n, n+length-1)) + [v]
        n += length-1
        edges.extend(zip(route, route[1:]))
    if any(d != 3 for d in degrees):
        raise ValueError("kernel must be cubic, loops counting twice")
    result = make_graph(n, edges)
    if not result.connected():
        raise ValueError("kernel must be connected")
    return result


def residue_representative(graph):
    branch, paths = branch_paths(graph)
    reps = []
    for u, v, length in paths:
        residue = length % 4
        # Distinct paths have private interiors. Never use a direct edge.
        representative = {0: 4, 1: 5, 2: 6 if u == v else 2, 3: 3}[residue]
        reps.append((u, v, representative))
    result = realize(len(branch), reps)
    c = result.cyclomatic()
    if result.order > 15*c-14:
        raise RuntimeError("representative order bound failed")
    return result, tuple(reps)
