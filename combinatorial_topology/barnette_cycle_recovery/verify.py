"""Exact corroboration of the cycle-recovery theorem; Python 3.11+, stdlib."""
from collections import Counter, defaultdict
from itertools import combinations, permutations
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def edge(u, v):
    return tuple(sorted((u, v)))


def boundary(face):
    return [edge(face[i], face[(i + 1) % len(face)]) for i in range(len(face))]


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    adj = {v: set() for v in vertices}
    for u, v in edges:
        require(u in adj and v in adj, "edge endpoint outside vertex set")
        adj[u].add(v)
        adj[v].add(u)
    reached = {min(vertices)}
    todo = list(reached)
    while todo:
        for v in adj[todo.pop()] - reached:
            reached.add(v)
            todo.append(v)
    return reached == vertices


def tree(vertices, edges):
    return len(edges) == len(vertices) - 1 and connected(vertices, edges)


def audit_embedding(n, faces, colors):
    """Check sphere via orientable face gluing, vertex links, and Euler."""
    require(len(colors) == len(faces), "color count")
    incidence = defaultdict(list)
    for i, f in enumerate(faces):
        require(len(f) >= 4 and len(f) % 2 == 0, "face length")
        require(len(f) == len(set(f)), "nonsimple face")
        require(all(0 <= v < n for v in f), "bad vertex")
        for u, v in zip(f, f[1:] + f[:1]):
            incidence[edge(u, v)].append((i, 1 if u < v else -1))
    require(all(len(a) == 2 for a in incidence.values()), "edge incidence")
    edges = set(incidence)
    require(n - len(edges) + len(faces) == 2, "Euler characteristic")
    require(connected(range(n), edges), "disconnected graph")
    adj = {v: set() for v in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    require(all(len(a) == 3 for a in adj.values()), "not cubic")
    dual = set()
    ecolor = {}
    signs = {0: 1}
    while True:
        changed = False
        for e, ((i, a), (j, b)) in incidence.items():
            require(i != j and colors[i] != colors[j], "bad face coloring")
            dual.add(edge(i, j))
            ecolor[e] = 3 - colors[i] - colors[j]
            if i in signs and j not in signs:
                signs[j] = -a * b * signs[i]
                changed = True
            if j in signs and i not in signs:
                signs[i] = -a * b * signs[j]
                changed = True
            if i in signs and j in signs:
                require(a * signs[i] == -b * signs[j], "nonorientable gluing")
        if not changed:
            break
    require(len(signs) == len(faces), "disconnected dual")
    require(len(dual) == len(edges), "nonsimple dual")
    oriented = [f if signs[i] == 1 else list(reversed(f))
                for i, f in enumerate(faces)]
    for v in range(n):
        link = {}
        for f in oriented:
            if v in f:
                k = f.index(v)
                a, b = f[k - 1], f[(k + 1) % len(f)]
                require(a not in link, "duplicate link successor")
                link[a] = b
        start = min(adj[v])
        require(set(link) == adj[v] and set(link.values()) == adj[v], "link domain")
        x, seen = start, set()
        while x not in seen:
            seen.add(x)
            x = link[x]
        require(x == start and seen == adj[v], "vertex link is not a circle")
        require({ecolor[edge(v, u)] for u in adj[v]} == {0, 1, 2}, "edge colors")
    part = {0: 0}
    todo = [0]
    while todo:
        u = todo.pop()
        for v in adj[u]:
            if v not in part:
                part[v] = 1 - part[u]
                todo.append(v)
            require(part[v] != part[u], "not bipartite")
    deletions = 0
    for k in range(3):
        for deleted in combinations(range(n), k):
            live = set(range(n)) - set(deleted)
            require(connected(live, {e for e in edges if set(e) <= live}),
                    "not 3-connected")
            deletions += 1
    return edges, ecolor, dual, deletions


def hamiltonian_cycles(n, edges):
    """Definition-level DFS, independent of colors and dual trees."""
    adj = {v: [] for v in range(n)}
    for u, v in sorted(edges):
        adj[u].append(v)
        adj[v].append(u)
    found = set()

    def visit(path, used):
        if len(path) == n:
            if path[0] in adj[path[-1]] and path[1] < path[-1]:
                found.add(frozenset(boundary(path)))
            return
        for v in adj[path[-1]]:
            if v not in used:
                visit(path + [v], used | {v})
    visit([0], {0})
    return found


def cube():
    faces, colors = [], []
    for i, b in enumerate((1, 2, 4)):
        a, c = [x for x in (1, 2, 4) if x != b]
        for s in (0, b):
            faces.append([s, s ^ a, s ^ a ^ c, s ^ c])
            colors.append(i)
    return 8, faces, colors


def double_cube():
    def v(s, x):
        return 7 * s + x - 1
    faces, colors = [], []
    for i, b in enumerate((1, 2, 4)):
        a, c = [x for x in (1, 2, 4) if x != b]
        for s in range(2):
            faces.append([v(s, x) for x in (b, b ^ a, 7, b ^ c)])
            colors.append(i)
        faces.append([v(0, a), v(0, a ^ c), v(0, c),
                      v(1, c), v(1, a ^ c), v(1, a)])
        colors.append(i)
    return 14, faces, colors


def prism(k):
    require(k >= 4 and k % 2 == 0, "even prism")
    faces = [list(range(k)), list(range(k, 2 * k))]
    colors = [0, 0]
    for i in range(k):
        j = (i + 1) % k
        faces.append([i, j, j + k, i + k])
        colors.append(1 + i % 2)
    return 2 * k, faces, colors


def rudolph():
    # Published 16-vertex fixture, credited in SOURCES.md; not our construction.
    faces = [[0, 8, 9, 3, 5, 4], [0, 15, 14, 1, 11, 8],
             [0, 4, 12, 15], [1, 14, 13, 7], [1, 7, 6, 2, 10, 11],
             [2, 6, 5, 3], [2, 3, 9, 10], [4, 5, 6, 7, 13, 12],
             [8, 11, 10, 9], [12, 13, 14, 15]]
    return 16, faces, [0, 1, 2, 2, 0, 2, 1, 1, 2, 0]


def audit(name, fixture):
    n, faces, colors = fixture
    edges, ec, dual, deletions = audit_embedding(n, faces, colors)
    hcs = hamiltonian_cycles(n, edges)
    recovered = set()
    rows = []
    for red, blue, green in permutations(range(3)):
        B = {i for i, c in enumerate(colors) if c == blue}
        F = {i for i, c in enumerate(colors) if c == green}
        vertices = B | F
        H = {e for e in dual if set(e) <= vertices}
        neighbors = {f: {b for b in B if edge(b, f) in H} for f in F}
        Mg = {e for e in edges if ec[e] == green}
        eligible = {C for C in hcs if Mg <= C}
        require(connected(vertices, H), "bicolored dual disconnected")
        counts = Counter()
        unrooted = Counter()
        tree_count = full_count = rooted_count = rootless_count = 0
        for es in combinations(sorted(H), len(vertices) - 1):
            T = set(es)
            if not tree(vertices, T):
                continue
            tree_count += 1
            deg = Counter(x for e in T for x in e)
            if any(deg[f] not in (1, len(neighbors[f])) for f in F):
                continue
            full_count += 1
            C = set(Mg)
            for f in F:
                chosen = red if deg[f] == 1 else blue
                C.update(e for e in boundary(faces[f]) if ec[e] == chosen)
            C = frozenset(C)
            require(C in hcs, "full-star tree does not give Hamiltonian cycle")
            roots = sum(deg[b] == 1 for b in B)
            unrooted[C] += 1
            counts[C] += roots
            rooted_count += roots
            rootless_count += roots == 0
        require(set(counts) == eligible and all(counts[C] > 0 for C in eligible),
                "recovery image differs from eligible Hamiltonian cycles")
        for C in eligible:
            S = {f for f in F if
                 {e for e in boundary(faces[f]) if ec[e] == blue} <= C}
            Qv = B | S
            Q = {e for e in H if set(e) <= Qv}
            require(tree(Qv, Q), "cycle-side weak dual is not a tree")
            require(all(len(neighbors[f]) >= 2 for f in F), "small green degree")
            qdeg = Counter(x for e in Q for x in e)
            root_leaves = [b for b in B if qdeg[b] == 1]
            require(root_leaves, "no blue core leaf")
            expected_unrooted = 1
            for f in F - S:
                expected_unrooted *= len(neighbors[f])
            require(unrooted[C] == expected_unrooted, "unrooted certificate count")
            predicted = 0
            for b in root_leaves:
                term = 1
                for f in F - S:
                    term *= len(neighbors[f]) - (b in neighbors[f])
                predicted += term
            require(counts[C] == predicted, "rooted certificate count")
            # Explicit linear construction: retain every core edge and choose
            # one neighbor other than the fixed blue root for each other face.
            root = min(root_leaves)
            T = Q | {edge(f, min(neighbors[f] - {root})) for f in F - S}
            require(tree(vertices, T), "constructed tree invalid")
            require(sum(root in e for e in T) == 1, "root lost leaf property")
        recovered.update(eligible)
        rows.append({"red_blue_green": [red, blue, green],
                     "all_dual_trees": tree_count, "full_star_trees": full_count,
                     "full_star_trees_without_blue_leaf": rootless_count,
                     "rooted_full_star_trees": rooted_count,
                     "eligible_cycles": len(eligible)})
    missing_profiles = Counter(tuple(sum(ec[e] == c for e in edges - C)
                                     for c in range(3)) for C in hcs)
    return {"fixture": name, "vertices": n, "edges": len(edges),
            "faces": len(faces), "connectivity_deletions": deletions,
            "hamiltonian_cycles": len(hcs), "recoverable_under_relabeling": len(recovered),
            "unrecoverable": len(hcs - recovered),
            "omitted_edge_profiles": [[list(k), v] for k, v in sorted(missing_profiles.items())],
            "color_roles": rows}


def negative_controls():
    n, faces, colors = cube()
    rejected = 0
    for fs, cs in [(faces[:-1], colors[:-1]),
                   (faces, [0] * len(colors)),
                   ([[0, 1, 0, 2]] + faces[1:], colors)]:
        try:
            audit_embedding(n, fs, cs)
        except ValueError:
            rejected += 1
    require(rejected == 3, "malformed fixture escaped")
    return rejected


def main():
    fixtures = [("cube", cube()), ("hexagonal_prism", prism(6)),
                ("octagonal_prism", prism(8)), ("decagonal_prism", prism(10)),
                ("two_cube_sum", double_cube()), ("rudolph_2026", rudolph())]
    rows = [audit(name, fixture) for name, fixture in fixtures]
    n, faces, colors = double_cube()
    edges, ec, _, _ = audit_embedding(n, faces, colors)
    witness = [0, 2, 1, 5, 6, 4, 3, 10, 12, 8, 9, 13, 11, 7]
    C = set(boundary(witness))
    require(len(set(witness)) == n and C <= edges, "witness is not Hamiltonian")
    omitted = [sum(ec[e] == c for e in edges - C) for c in range(3)]
    require(omitted == [2, 3, 2], "witness matching profile")
    print(json.dumps({"schema": 1, "method": "exact DFS versus all dual spanning trees",
                      "fixtures": rows, "negative_controls": negative_controls(),
                      "two_cube_witness": witness, "witness_omitted_profile": omitted},
                     sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
