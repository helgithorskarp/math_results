"""Exact graph statistics, Mycielski lifts and Stirling wedge counts.

CPython 3.11+, standard library. The universal homotopy proof is in PROOF.md.
"""
from itertools import combinations


def require(ok, message):
    if not ok:
        raise ValueError(message)


def adjacency(n, edges):
    out = [set() for _ in range(n)]
    for a, b in edges:
        out[a].add(b)
        out[b].add(a)
    return out


def components(vertices, adj):
    unseen = set(vertices)
    answer = []
    while unseen:
        seed = min(unseen)
        unseen.remove(seed)
        part, stack = {seed}, [seed]
        while stack:
            v = stack.pop()
            fresh = unseen & adj[v]
            unseen -= fresh
            part |= fresh
            stack.extend(sorted(fresh))
        answer.append(part)
    return answer


def validate(n, edges):
    require(type(n) is int and n >= 2, 'at least two labelled vertices required')
    answer = set()
    for edge in edges:
        require(len(edge) == 2, 'edge must have two endpoints')
        a, b = edge
        require(type(a) is int and type(b) is int and 0 <= a < b < n,
                'canonical nonloop edge required')
        require((a, b) not in answer, 'duplicate edge')
        answer.add((a, b))
    adj = adjacency(n, answer)
    require(len(components(range(n), adj)) == 1, 'connected graph required')
    for a, b in answer:
        common = adj[a] & adj[b]
        require(not any(y in adj[x] for x, y in combinations(common, 2)),
                'K4-free graph required')
    return answer


def triangles(n, edges):
    adj = adjacency(n, edges)
    return sorted((a, b, c) for a, b in edges for c in adj[a] & adj[b] if b < c)


def statistics(n, edges):
    edges = validate(n, edges)
    adj = adjacency(n, edges)
    link_components = [len(components(adj[v], adj)) for v in range(n)]
    multiplicities = {e: len(adj[e[0]] & adj[e[1]]) for e in edges}
    t = sum(multiplicities.values()) // 3
    e0 = sum(value == 0 for value in multiplicities.values())
    c = sum(link_components)
    d = 3*t - 2*len(edges) + c
    y = 3*t - len(edges) + e0
    require(d >= 0 and y >= 0, 'negative structural defect')
    return {'n': n, 'm': len(edges), 't': t, 'e0': e0, 'C': c, 'D': d, 'Y': y,
            'link_components': link_components}


def mycielski(n, edges):
    edges = validate(n, edges)
    out = set(edges)
    for a, b in edges:
        out.add((a, n+b))
        out.add((b, n+a))
    out.update((n+v, 2*n) for v in range(n))
    return 2*n+1, out


def stirling(n, r):
    require(type(n) is int and n >= 0 and type(r) is int and r >= 0,
            'nonnegative integer Stirling indices required')
    row = [1] + [0]*r
    for _ in range(n):
        row = [0] + [j*row[j] + row[j-1] for j in range(1, r+1)]
    return row[r]


def wedge_counts(stats, k):
    require(type(k) is int and k >= 0, 'nonnegative integer iterate required')
    s2, s3, s4 = (stirling(k+1, r) for r in (2, 3, 4))
    circles = (stats['C']-1)*s2 + (2*stats['e0']+2*stats['n']+1)*s3
    spheres = stats['D']*s2 + 2*stats['Y']*s3 + 6*stats['t']*s4
    return {'circles': circles, 'two_spheres': spheres}


def first_failure(stats):
    """First nonaspherical positive iterate; None means every iterate passes."""
    if stats['D']:
        return 1
    if stats['Y']:
        return 2
    if stats['t']:
        return 3
    return None


def collapse_trace(n, edges):
    """Triangle/free-edge removals; None means this peeling process got stuck.

    Failure is not a general asphericity decision. Positive cases of our
    theorem always admit such a trace. Vertices and unpaired edges are kept.
    """
    edges = validate(n, edges)
    cells = set(triangles(n, edges))
    trace = []
    while cells:
        incident = {}
        for face in sorted(cells):
            for edge in combinations(face, 2):
                incident.setdefault(edge, []).append(face)
        free = next((edge for edge in sorted(incident) if len(incident[edge]) == 1), None)
        if free is None:
            return None
        face = incident[free][0]
        trace.append([list(free), list(face)])
        cells.remove(face)
    return trace
