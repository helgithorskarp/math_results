#!/usr/bin/env python3
"""Exact checks of PROOF.md. Python 3.11+, standard library, no inputs."""
import hashlib
import itertools as it
import json
import math
from collections import Counter


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(row):
    row = tuple(row)
    k = row.index(min(row))
    return row[k:] + row[:k]


def face_cycles(rows):
    """Direct definition: phi(u,v)=(v,rho_v(u))."""
    rho = [{u: row[(j + 1) % len(row)] for j, u in enumerate(row)}
           for row in rows]
    unseen = {(v, w) for v, row in enumerate(rows) for w in row}
    faces = []
    while unseen:
        first = min(unseen)
        dart = first
        face = []
        while True:
            require(dart in unseen, 'invalid face permutation')
            unseen.remove(dart)
            face.append(dart[0])
            u, v = dart
            dart = (v, rho[v][u])
            if dart == first:
                break
        faces.append(tuple(face))
    return faces


def genus(rows, faces):
    twice = 2 - len(rows) + sum(map(len, rows)) // 2 - len(faces)
    require(twice >= 0 and twice % 2 == 0, 'invalid orientable Euler genus')
    return twice // 2


def orient_facets(facets):
    """Orient an initially unoriented connected triangulation by dual BFS."""
    facets = sorted(set(tuple(sorted(f)) for f in facets))
    edges = {}
    for i, f in enumerate(facets):
        for j in range(3):
            a, b = f[j], f[(j + 1) % 3]
            edges.setdefault(tuple(sorted((a, b))), []).append((i, 1 if a < b else -1))
    require(all(len(x) == 2 for x in edges.values()), 'not a closed triangulation')
    signs = {0: 1}
    todo = [0]
    while todo:
        i = todo.pop()
        for edge in it.combinations(facets[i], 2):
            entries = edges[tuple(sorted(edge))]
            (a, sa), (b, sb) = entries
            j = b if a == i else a
            s = -signs[i] * sa * sb
            if j in signs:
                require(signs[j] == s, 'nonorientable facets')
            else:
                signs[j] = s
                todo.append(j)
    require(len(signs) == len(facets), 'disconnected dual')
    return [f if signs[i] == 1 else f[::-1] for i, f in enumerate(facets)]


class Triangulation:
    def __init__(self, facets):
        self.faces = orient_facets(facets)
        self.keys = [tuple(sorted(f)) for f in self.faces]
        self.n = 1 + max(max(f) for f in self.faces)
        adj = [set() for _ in range(self.n)]
        succ = [{} for _ in range(self.n)]
        edge_faces = {}
        for i, f in enumerate(self.faces):
            for j in range(3):
                u, v, w = f[j], f[(j + 1) % 3], f[(j + 2) % 3]
                adj[v].update((u, w))
                require(u not in succ[v], 'duplicate successor')
                succ[v][u] = w
                edge_faces.setdefault(tuple(sorted((u, v))), []).append(i)
        self.adj = [tuple(sorted(a)) for a in adj]
        self.reference = []
        for v, a in enumerate(self.adj):
            require(len(a) >= 3, 'degree below three')
            row = [a[0]]
            while succ[v][row[-1]] != row[0]:
                row.append(succ[v][row[-1]])
                require(len(row) <= len(a), 'broken vertex link')
            require(set(row) == set(a), 'vertex link not a cycle')
            self.reference.append(tuple(row))
        self.reference = tuple(self.reference)
        self.dual = [set() for _ in self.faces]
        for fs in edge_faces.values():
            require(len(fs) == 2, 'edge incidence not two')
            a, b = fs
            self.dual[a].add(b)
            self.dual[b].add(a)
        triangles = {t for t in it.combinations(range(self.n), 3)
                     if all(v in adj[u] for u, v in it.combinations(t, 2))}
        require(triangles == set(self.keys), 'nonfacial graph triangle')
        require({tuple(sorted(f)) for f in face_cycles(self.reference)} == triangles,
                'reference reconstruction failed')
        self.h = genus(self.reference, face_cycles(self.reference))

    def components(self, removed):
        remaining = set(range(len(self.faces))) - set(removed)
        components = []
        while remaining:
            root = min(remaining)
            remaining.remove(root)
            comp, todo = [root], [root]
            while todo:
                i = todo.pop()
                for j in sorted(self.dual[i] & remaining):
                    remaining.remove(j)
                    comp.append(j)
                    todo.append(j)
            components.append(tuple(sorted(comp)))
        if removed:
            require(len(components) <= len(removed), 'dual component bound')
        return components

    def constraints(self, removed, bits):
        comps = self.components(removed)
        require(len(bits) == len(comps), 'wrong orientation bit count')
        successors = [{} for _ in self.adj]
        predecessors = [{} for _ in self.adj]
        for comp, bit in zip(comps, bits):
            for i in comp:
                f = self.faces[i] if bit == 0 else self.faces[i][::-1]
                for j in range(3):
                    u, v, w = f[j], f[(j + 1) % 3], f[(j + 2) % 3]
                    if (u in successors[v] and successors[v][u] != w
                            or w in predecessors[v] and predecessors[v][w] != u):
                        return None
                    successors[v][u] = w
                    predecessors[v][w] = u
        return successors


def path_blocks(nodes, succ):
    """Return paths, or one forced full cycle, or invalid proper cycle."""
    if len(set(succ.values())) != len(succ):
        return None
    pred = set(succ.values())
    if len(succ) == len(nodes):
        row, current = [], min(nodes)
        while current not in row:
            row.append(current)
            current = succ[current]
        if len(row) == len(nodes) and current == row[0]:
            return 'cycle', [tuple(row)]
        return None
    blocks, seen = [], set()
    for start in sorted(set(nodes) - pred):
        block, current = [], start
        while True:
            if current in seen:
                return None
            seen.add(current)
            block.append(current)
            if current not in succ:
                break
            current = succ[current]
        blocks.append(tuple(block))
    if seen != set(nodes):
        return None
    return 'paths', blocks


def completions(nodes, succ):
    result = path_blocks(nodes, succ)
    if result is None:
        return []
    mode, blocks = result
    if mode == 'cycle':
        return [canonical(blocks[0])]
    return [canonical(sum((blocks[0],) + p, ())) for p in it.permutations(blocks[1:])]


def missing(T, faces):
    triangles = {tuple(sorted(f)) for f in faces if len(f) == 3}
    require(triangles <= set(T.keys), 'new graph triangle')
    return tuple(i for i, key in enumerate(T.keys) if key not in triangles)


def enumerate_decoder(T):
    """All genera for small fixtures; fixed-r version restricts |S|<=8r."""
    accepted = {}
    trials = 0
    for t in range(len(T.faces) + 1):
        for removed in it.combinations(range(len(T.faces)), t):
            comps = T.components(removed)
            for bits in it.product((0, 1), repeat=len(comps)):
                constraints = T.constraints(removed, bits)
                if constraints is None:
                    continue
                options = [completions(a, s) for a, s in zip(T.adj, constraints)]
                kvals = [sum(v in T.faces[i] for i in removed) for v in range(T.n)]
                require(sum(kvals) == 3 * t, 'corner budget')
                if all(options):
                    for k, option in zip(kvals, options):
                        require(len(option) == (math.factorial(k - 1) if k else 1),
                                'local completion count')
                for rows in it.product(*options):
                    trials += 1
                    faces = face_cycles(rows)
                    if missing(T, faces) != removed:
                        continue
                    g = genus(rows, faces)
                    r = g - T.h
                    require(t <= 8 * r, 'lost triangle bound')
                    require(rows not in accepted, 'decoder duplicate')
                    accepted[rows] = (g, t)
    return accepted, trials


def direct_enumeration(T):
    """No defect assumptions: enumerate all cyclic vertex orders directly."""
    choices = [[(a[0],) + p for p in it.permutations(a[1:])] for a in T.adj]
    data = {}
    for rows in it.product(*choices):
        faces = face_cycles(rows)
        g = genus(rows, faces)
        t = len(missing(T, faces))
        require(sum(len(f) - 3 for f in faces) == 6 * (g - T.h), 'Euler defect')
        data[rows] = (g, t)
    require(len(data) == math.prod(math.factorial(len(a) - 1) for a in T.adj),
            'direct enumeration total')
    return data


def encode_and_check(T, rows):
    """Extract the unique bounded certificate of one supplied embedding."""
    rows = tuple(canonical(row) for row in rows)
    faces = face_cycles(rows)
    removed = missing(T, faces)
    r = genus(rows, faces) - T.h
    require(len(removed) <= 8 * r, 'sample defect bound')
    oriented = {canonical(f) for f in faces if len(f) == 3}
    bits = []
    for comp in T.components(removed):
        vals = {0 if canonical(T.faces[i]) in oriented else 1 for i in comp}
        require(len(vals) == 1, 'orientation propagation')
        bits.append(vals.pop())
    constraints = T.constraints(removed, bits)
    require(constraints is not None, 'inconsistent extracted constraints')
    reconstructed, orders, total_blocks = [], [], 0
    for v, (nodes, succ) in enumerate(zip(T.adj, constraints)):
        partial = path_blocks(nodes, succ)
        require(partial is not None, 'extracted proper cycle')
        mode, blocks = partial
        if mode == 'cycle':
            order, rebuilt = (), canonical(blocks[0])
        else:
            total_blocks += len(blocks)
            row = rows[v]
            positions = {u: j for j, u in enumerate(row)}
            order = tuple(sorted(range(len(blocks)), key=lambda k: positions[blocks[k][0]]))
            p = order.index(0)
            order = order[p:] + order[:p]
            rebuilt = canonical(sum((blocks[k] for k in order), ()))
        require(rebuilt == rows[v], 'certificate round trip')
        reconstructed.append(rebuilt)
        orders.append(order)
    require(total_blocks == 3 * len(removed), 'certificate block budget')
    return {'vertices': T.n, 'edges': sum(map(len, T.adj)) // 2,
            'base_genus': T.h, 'excess_genus': r, 'lost_triangles': len(removed),
            'components': len(bits), 'path_blocks': total_blocks,
            'maximum_degree': max(map(len, T.adj))}


def bipyramid(m):
    return Triangulation([(a, 2 + i, 2 + (i + 1) % m)
                          for a in (0, 1) for i in range(m)])


def torus(m, n):
    def v(i, j):
        return (i % m) * n + j % n
    return Triangulation([f for i in range(m) for j in range(n)
                          for f in [(v(i, j), v(i + 1, j), v(i + 1, j + 1)),
                                    (v(i, j), v(i + 1, j + 1), v(i, j + 1))]])


def k7_control():
    """Relabel one triangular K7 map: different faces at the same genus."""
    base = (1, 3, 2, 6, 4, 5)
    rows1 = tuple(canonical(tuple((v + d) % 7 for d in base)) for v in range(7))
    relabel = [1, 0, 2, 3, 4, 5, 6]
    rows2 = [None] * 7
    for v, row in enumerate(rows1):
        rows2[relabel[v]] = canonical(tuple(relabel[u] for u in row))
    rows2 = tuple(rows2)
    faces1, faces2 = face_cycles(rows1), face_cycles(rows2)
    require(all(len(f) == 3 for f in faces1 + faces2), 'K7 triangularity')
    require(genus(rows1, faces1) == genus(rows2, faces2) == 1, 'K7 genus')
    keys1 = {tuple(sorted(f)) for f in faces1}
    keys2 = {tuple(sorted(f)) for f in faces2}
    require(keys1 != keys2, 'K7 face trade')
    rejected = False
    try:
        Triangulation(faces1)
    except ValueError as e:
        rejected = str(e) == 'nonfacial graph triangle'
    require(rejected, 'K7 hypothesis rejection')
    return {'first_rotations': rows1, 'second_rotations': rows2,
            'excess_genus': 0, 'lost_reference_triangles': len(keys1 - keys2),
            'hypothesis_rejected': rejected}


def main():
    report = {'claim': 'bounded triangulation genus-defect reconstruction', 'exhaustive': []}
    tetra = Triangulation(it.combinations(range(4), 3))
    octa = Triangulation(it.product((0, 1), (2, 3), (4, 5)))
    for name, T in [('tetrahedron', tetra), ('octahedron', octa)]:
        direct = direct_enumeration(T)
        decoded, trials = enumerate_decoder(T)
        require(direct == decoded, 'entry-level decoder disagreement')
        table = Counter(direct.values())
        sha = hashlib.sha256()
        for rows, pair in sorted(direct.items()):
            sha.update((json.dumps([rows, pair], separators=(',', ':')) + '\n').encode())
        report['exhaustive'].append({'name': name, 'rotations': len(direct),
                                    'decoder_candidates': trials, 'sha256': sha.hexdigest(),
                                    'genus_lost_counts': [[g, t, c] for (g, t), c in sorted(table.items())]})
    sharp_rows = ((2, 3, 4, 5), (2, 5, 4, 3), (0, 1, 4, 5),
                  (0, 5, 4, 1), (0, 1, 2, 3), (0, 3, 2, 1))
    sharp_faces = face_cycles(sharp_rows)
    require(genus(sharp_rows, sharp_faces) == 1 and all(len(f) == 4 for f in sharp_faces),
            'sharp octahedral quadrangulation')
    report['sharp_witness'] = {'rotations': sharp_rows, 'faces': sharp_faces,
                               'certificate': encode_and_check(octa, sharp_rows)}
    samples = []
    for T in [bipyramid(5), bipyramid(12), bipyramid(64), torus(4, 4), torus(5, 7)]:
        samples.append(encode_and_check(T, T.reference))
        samples.append(encode_and_check(T, [row[::-1] for row in T.reference]))
        for vertices in [(0,), (0, 1), (0, 2, 4)]:
            rows = [list(row) for row in T.reference]
            for v in vertices:
                rows[v][0], rows[v][1] = rows[v][1], rows[v][0]
            samples.append(encode_and_check(T, rows))
    report['certificate_roundtrips'] = samples
    report['nonfacial_triangle_control'] = k7_control()
    local = [
        (range(4), {0: 1, 1: 0}),
        (range(4), {0: 1, 2: 1}),
        (range(4), {0: 1, 1: 2, 2: 0}),
    ]
    require(all(path_blocks(nodes, succ) is None for nodes, succ in local), 'malformed controls')
    report['invalid_local_controls'] = len(local)
    require(len(completions(range(5), {0: 1, 1: 2, 3: 4})) == 1, 'two path blocks')
    require(len(completions(range(5), {})) == math.factorial(4), 'no constraints')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
