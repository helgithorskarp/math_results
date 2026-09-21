#!/usr/bin/env python3
"""Exact p=3,4 checks of PROOF.md; Python 3.11+, standard library."""
import hashlib
import itertools as it
import json
import math
from collections import Counter


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical_row(row):
    row = tuple(row)
    i = row.index(min(row))
    return row[i:] + row[:i]


def canonical_cycle(cycle):
    cycle = tuple(cycle)
    choices = []
    for row in (cycle, cycle[::-1]):
        choices.extend(row[i:] + row[:i] for i in range(len(row)))
    return min(choices)


def face_cycles(rows):
    rho = [{u: row[(i + 1) % len(row)] for i, u in enumerate(row)}
           for row in rows]
    unseen = {(v, w) for v, row in enumerate(rows) for w in row}
    faces = []
    while unseen:
        first = min(unseen)
        dart = first
        face = []
        while True:
            require(dart in unseen, "invalid face permutation")
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
    require(twice >= 0 and twice % 2 == 0, "invalid orientable genus")
    return twice // 2


def orient_faces(faces):
    faces = [tuple(f) for f in faces]
    edge_uses = {}
    for i, face in enumerate(faces):
        require(len(set(face)) == len(face), "non-simple reference face")
        for a, b in zip(face, face[1:] + face[:1]):
            key = tuple(sorted((a, b)))
            edge_uses.setdefault(key, []).append((i, 1 if a < b else -1))
    require(all(len(uses) == 2 for uses in edge_uses.values()),
            "not a closed cellulation")
    signs = {0: 1}
    todo = [0]
    while todo:
        i = todo.pop()
        for a, b in zip(faces[i], faces[i][1:] + faces[i][:1]):
            uses = edge_uses[tuple(sorted((a, b)))]
            (x, sx), (y, sy) = uses
            j = y if x == i else x
            sign = -signs[i] * sx * sy
            if j in signs:
                require(signs[j] == sign, "nonorientable reference faces")
            else:
                signs[j] = sign
                todo.append(j)
    require(len(signs) == len(faces), "disconnected face dual")
    return [face if signs[i] == 1 else face[::-1]
            for i, face in enumerate(faces)]


def simple_cycles(adj, length):
    found = set()
    n = len(adj)
    for start in range(n):
        def visit(path):
            if len(path) == length:
                if start in adj[path[-1]]:
                    found.add(canonical_cycle(path))
                return
            for w in adj[path[-1]]:
                if w > start and w not in path:
                    visit(path + (w,))
        visit((start,))
    return found


class PAngulation:
    def __init__(self, faces):
        lengths = {len(face) for face in faces}
        require(len(lengths) == 1, "not a p-angulation")
        self.p = lengths.pop()
        require(self.p >= 3, "p below three")
        self.faces = orient_faces(faces)
        self.keys = tuple(canonical_cycle(face) for face in self.faces)
        self.n = 1 + max(max(face) for face in self.faces)
        adj = [set() for _ in range(self.n)]
        succ = [{} for _ in range(self.n)]
        edge_faces = {}
        for i, face in enumerate(self.faces):
            for j, v in enumerate(face):
                u, w = face[j - 1], face[(j + 1) % self.p]
                adj[v].update((u, w))
                require(u not in succ[v], "duplicate reference corner")
                succ[v][u] = w
                edge_faces.setdefault(tuple(sorted((v, w))), []).append(i)
        self.adj = tuple(tuple(sorted(a)) for a in adj)
        require(all(len(a) >= 3 for a in self.adj), "degree below three")
        require(len(set(self.keys)) == len(self.keys), "duplicate reference face")
        self.reference = []
        for v, nodes in enumerate(self.adj):
            row = [nodes[0]]
            while succ[v][row[-1]] != row[0]:
                row.append(succ[v][row[-1]])
                require(len(row) <= len(nodes), "broken vertex link")
            require(set(row) == set(nodes), "vertex link not a cycle")
            self.reference.append(tuple(row))
        self.reference = tuple(self.reference)
        for q in range(3, self.p):
            require(not simple_cycles(self.adj, q), "girth below p")
        require(simple_cycles(self.adj, self.p) == set(self.keys),
                "nonfacial p-cycle")
        require({canonical_cycle(f) for f in face_cycles(self.reference)}
                == set(self.keys), "reference reconstruction failed")
        self.dual = [set() for _ in self.faces]
        for uses in edge_faces.values():
            require(len(uses) == 2, "edge incidence not two")
            a, b = uses
            self.dual[a].add(b)
            self.dual[b].add(a)
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
            require(len(components) <= len(removed), "dual component bound")
        return components

    def constraints(self, removed, bits):
        components = self.components(removed)
        require(len(bits) == len(components), "wrong bit count")
        successors = [{} for _ in self.adj]
        predecessors = [{} for _ in self.adj]
        for comp, bit in zip(components, bits):
            for i in comp:
                face = self.faces[i] if bit == 0 else self.faces[i][::-1]
                for j, v in enumerate(face):
                    u, w = face[j - 1], face[(j + 1) % self.p]
                    if (u in successors[v] and successors[v][u] != w
                            or w in predecessors[v] and predecessors[v][w] != u):
                        return None
                    successors[v][u] = w
                    predecessors[v][w] = u
        return successors


def path_blocks(nodes, succ):
    if len(set(succ.values())) != len(succ):
        return None
    pred = set(succ.values())
    if len(succ) == len(nodes):
        row, current = [], min(nodes)
        while current not in row:
            row.append(current)
            current = succ[current]
        if len(row) == len(nodes) and current == row[0]:
            return "cycle", [tuple(row)]
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
    return "paths", blocks


def completions(nodes, succ):
    result = path_blocks(nodes, succ)
    if result is None:
        return []
    mode, blocks = result
    if mode == "cycle":
        return [canonical_row(blocks[0])]
    return [canonical_row(sum((blocks[0],) + order, ()))
            for order in it.permutations(blocks[1:])]


def missing(T, faces):
    short = set()
    for face in faces:
        if len(face) == T.p:
            require(len(set(face)) == T.p, "repeated vertex in p-face")
            short.add(canonical_cycle(face))
    require(short <= set(T.keys), "new p-cycle face")
    return tuple(i for i, key in enumerate(T.keys) if key not in short)


def check_defect(T, rows, faces, removed):
    r = genus(rows, faces) - T.h
    t = len(removed)
    other = [face for face in faces if len(face) != T.p]
    require(len(other) == t - 2 * r, "face-count identity")
    require(sum(map(len, other)) == T.p * t, "dart-count identity")
    require(sum(len(face) - (T.p + 1) for face in other)
            == 2 * (T.p + 1) * r - t, "excess-length identity")
    if r == 0:
        require(t == 0, "zero-excess face loss")
    else:
        require(2 * r + 1 <= t <= 2 * (T.p + 1) * r,
                "face-defect bound")
    return r, t


def direct_enumeration(T):
    choices = [[(nodes[0],) + order for order in it.permutations(nodes[1:])]
               for nodes in T.adj]
    data = {}
    for rows in it.product(*choices):
        faces = face_cycles(rows)
        removed = missing(T, faces)
        data[rows] = check_defect(T, rows, faces, removed)
    require(len(data) == math.prod(math.factorial(len(a) - 1) for a in T.adj),
            "direct enumeration total")
    return data


def decoder_enumeration(T):
    accepted = {}
    candidates = 0
    for t in range(len(T.faces) + 1):
        for removed in it.combinations(range(len(T.faces)), t):
            components = T.components(removed)
            for bits in it.product((0, 1), repeat=len(components)):
                constraints = T.constraints(removed, bits)
                if constraints is None:
                    continue
                options = [completions(nodes, succ)
                           for nodes, succ in zip(T.adj, constraints)]
                kvals = [sum(v in T.faces[i] for i in removed)
                         for v in range(T.n)]
                require(sum(kvals) == T.p * t, "block budget")
                if all(options):
                    for k, option in zip(kvals, options):
                        require(len(option) == (math.factorial(k - 1) if k else 1),
                                "local completion count")
                for rows in it.product(*options):
                    candidates += 1
                    faces = face_cycles(rows)
                    if missing(T, faces) != removed:
                        continue
                    pair = check_defect(T, rows, faces, removed)
                    require(rows not in accepted, "decoder duplicate")
                    accepted[rows] = pair
    return accepted, candidates


def tetrahedron():
    return PAngulation(list(it.combinations(range(4), 3)))


def cube():
    return PAngulation([
        (0, 1, 3, 2), (4, 6, 7, 5),
        (0, 4, 5, 1), (2, 3, 7, 6),
        (0, 2, 6, 4), (1, 5, 7, 3),
    ])


def main():
    report = {
        "claim": "uniform clean-p-angulation face-defect reconstruction",
        "fixtures": [],
    }
    for name, T in (("tetrahedron", tetrahedron()), ("cube", cube())):
        direct = direct_enumeration(T)
        decoded, candidates = decoder_enumeration(T)
        require(direct == decoded, "entry-level decoder disagreement")
        digest = hashlib.sha256()
        for rows, pair in sorted(direct.items()):
            digest.update((json.dumps([rows, pair], separators=(",", ":")) + "\n").encode())
        counts = Counter(direct.values())
        report["fixtures"].append({
            "name": name,
            "p": T.p,
            "vertices": T.n,
            "reference_faces": len(T.faces),
            "rotations": len(direct),
            "decoder_candidates": candidates,
            "genus_lost_counts": [[g, t, n] for (g, t), n in sorted(counts.items())],
            "rotation_map_sha256": digest.hexdigest(),
        })
    rejected = False
    rejection_reason = None
    try:
        PAngulation([(0, 1, 2, 3), (0, 3, 2, 1)])
    except ValueError as error:
        rejected = True
        rejection_reason = str(error)
    require(rejected, "degree-two control not rejected")
    report["degree_two_control_rejected"] = rejected
    report["degree_two_control_reason"] = rejection_reason
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
