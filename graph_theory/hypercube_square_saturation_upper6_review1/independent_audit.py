#!/usr/bin/env python3
"""Independent exact audit of the shortened-template upper-six construction.

No module from the reviewed contribution is imported.  The three templates
are reconstructed from the proof, their finite conditions are checked by a
separate affine-plane enumeration, and scale-32 quotients are built directly.
The theorem-selected dimension-19 cube is then constructed and checked by
enumerating all of its two-dimensional faces.
"""

from array import array
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import sys


TEMPLATES = [
    {
        "name": "H", "k": 2, "C": [0], "D": [1, 2],
        "T": [0, 1, 2, 3],
        "core_edges": [[0, 1], [0, 2], [0, 3], [1, 3]],
        "outside_neighbors": [[0, 1], [0, 2], [0, 2], [0, 1]],
    },
    {
        "name": "S", "k": 2, "C": [0, 1], "D": [2, 3],
        "T": [0, 2, 3],
        "core_edges": [[0, 3], [1, 2], [1, 3]],
        "outside_neighbors": [[0, 2], [1, 3], [1, 2], [0, 3]],
    },
    {
        "name": "F", "k": 4, "C": [0, 1], "D": [2, 4, 8],
        "T": [0, 1, 2, 5, 7, 8, 11, 12, 14, 15],
        "core_edges": [
            [0, 2], [0, 5], [0, 7], [0, 8], [0, 11], [0, 12],
            [1, 3], [1, 4], [1, 6], [1, 9], [1, 10], [1, 13],
            [1, 14], [1, 15], [2, 3], [2, 7], [2, 10], [2, 12],
            [2, 14], [3, 8], [4, 5], [4, 6], [4, 11], [4, 12],
            [4, 15], [6, 8], [7, 8], [8, 9], [8, 13],
        ],
        "outside_neighbors": [
            [1, 8], [1, 4], [0, 2], [1, 2], [1, 8], [0, 4],
            [1, 4, 8], [0, 2], [0, 8], [1, 2], [1, 8], [0, 4],
            [0, 4], [1, 2], [0, 2], [0, 8],
        ],
    },
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def affine_path_exists(adjacency, u, v):
    """Return whether u--w--(u xor v xor w)--v is present."""
    for w in adjacency[u]:
        if w == v:
            continue
        x = u ^ v ^ w
        if x in (u, v, w):
            continue
        if x in adjacency[w] and v in adjacency[x]:
            return True
    return False


def audit_template(template):
    q = 1 << template["k"]
    C, D, T = map(set, (template["C"], template["D"], template["T"]))
    A = C | D
    core = {edge(*row) for row in template["core_edges"]}
    rows = [set(row) for row in template["outside_neighbors"]]
    require(C and D and not C & D, "bad center classes")
    require(len(rows) == q and 0 in T, "bad row count or zero residue")
    require(all(row <= A and row & C and row & D for row in rows),
            "outside domination failed")

    span = {0}
    for vector in T:
        span |= {old ^ vector for old in list(span)}
    require(len(span) == q, "residues do not span")

    adjacency = [set() for _ in range(q)]
    for u, v in core:
        require((u ^ v) in T and ({u, v} & A), "invalid core edge")
        adjacency[u].add(v)
        adjacency[v].add(u)
    for cls in (C, D):
        require(all(not (adjacency[u] & cls) for u in cls), "class not independent")
        require(all(u in cls or adjacency[u] & cls for u in range(q)),
                "core domination failed")

    affine_sets = [quad for quad in combinations(range(q), 4)
                   if quad[0] ^ quad[1] ^ quad[2] ^ quad[3] == 0]
    cycle_orderings = 0
    for a, b, c, d in affine_sets:
        for order in ((a, b, c, d), (a, b, d, c), (a, c, b, d)):
            cycle_orderings += 1
            cycle = [edge(order[i], order[(i + 1) % 4]) for i in range(4)]
            require(not all(item in core for item in cycle), "core affine square")

    missing_core = 0
    for u, v in combinations(range(q), 2):
        if ({u, v} & A) and (u ^ v) in T and edge(u, v) not in core:
            missing_core += 1
            require(affine_path_exists(adjacency, u, v),
                    "missing core boundary witness")

    rectangle_tests = 0
    for a, b in combinations(sorted(A), 2):
        for x in range(q):
            rectangle_tests += 1
            require(not ({a, b} <= rows[x] and
                         {a, b} <= rows[x ^ a ^ b]), "outside affine square")

    missing_outside = 0
    for x, row in enumerate(rows):
        require(all((x ^ a) in T for a in row), "outside edge not allowed")
        for a in A:
            if (x ^ a) in T and a not in row:
                missing_outside += 1
                require(any({a, b} <= rows[x ^ a ^ b] for b in row),
                        "missing outside boundary witness")

    return {
        "affine_cycle_orderings": cycle_orderings,
        "class_sizes": [len(C), len(D)],
        "core_edges": len(core),
        "missing_core_boundary_edges": missing_core,
        "missing_outside_incidences": missing_outside,
        "name": template["name"],
        "outside_edges_per_nonzero_layer": sum(map(len, rows)),
        "outside_rectangle_tests": rectangle_tests,
    }


def audit_quotient(template, scale):
    q = 1 << template["k"]
    order = q * scale
    C, D, T = map(set, (template["C"], template["D"], template["T"]))
    A = C | D
    centers = A
    edges = {edge(*row) for row in template["core_edges"]}
    for z in range(1, scale):
        for x, row in enumerate(template["outside_neighbors"]):
            vertex = z * q + x
            edges.update(edge(a, vertex) for a in row)
    adjacency = [set() for _ in range(order)]
    for u, v in edges:
        require(((u ^ v) & (q - 1)) in T and ({u, v} & centers),
                "quotient edge violates support or center cover")
        adjacency[u].add(v)
        adjacency[v].add(u)
    for cls in (C, D):
        require(all(u in cls or adjacency[u] & cls for u in range(order)),
                "replicated domination failed")
        require(all(not (adjacency[u] & cls) for u in cls),
                "replicated independence failed")
    require(all(not affine_path_exists(adjacency, u, v) for u, v in edges),
            "replicated affine square")

    boundary_checked = 0
    for center in centers:
        for vertex in range(order):
            if vertex == center or ((center ^ vertex) & (q - 1)) not in T:
                continue
            if edge(center, vertex) not in edges:
                boundary_checked += 1
                require(affine_path_exists(adjacency, center, vertex),
                        "replicated missing boundary edge")
    expected_edges = len(template["core_edges"]) + (scale - 1) * sum(
        map(len, template["outside_neighbors"])
    )
    require(len(edges) == expected_edges, "replicated edge count")
    return {
        "boundary_edges_checked": boundary_checked,
        "edges": len(edges),
        "name": template["name"],
        "order": order,
        "scale": scale,
    }


class Block:
    def __init__(self, template, scale):
        self.template = template
        self.scale = scale
        self.q = 1 << template["k"]
        self.C, self.D = set(template["C"]), set(template["D"])
        self.A = self.C | self.D
        self.T = list(template["T"])
        self.core = {edge(*row) for row in template["core_edges"]}
        self.rows = [set(row) for row in template["outside_neighbors"]]
        self.length = len(self.T) * scale - 1
        self.delta = Fraction(len(self.A), self.q * scale)
        self.h = Fraction(len(self.core) + (scale - 1) * sum(map(len, self.rows)),
                          self.q * scale)
        self.labels = [z * self.q + residue for z in range(scale)
                       for residue in self.T if z or residue]
        require(len(self.labels) == self.length, "block label count")
        self.syndromes = [0] * (1 << self.length)
        for vertex in range(1, len(self.syndromes)):
            bit = vertex & -vertex
            self.syndromes[vertex] = (
                self.syndromes[vertex ^ bit] ^ self.labels[bit.bit_length() - 1]
            )

    def selected(self, left, right):
        if left < self.q and right < self.q:
            return edge(left, right) in self.core
        if left in self.A and right >= self.q:
            return left in self.rows[right % self.q]
        if right in self.A and left >= self.q:
            return right in self.rows[left % self.q]
        return False


def make_initial_cube():
    by_name = {template["name"]: template for template in TEMPLATES}
    first = Block(by_name["H"], 2)
    second = Block(by_name["S"], 4)
    padding = 1
    n = first.length + second.length + padding
    require(n == 19, "unexpected extension-test dimension")
    count = 1 << n
    first_mask = (1 << first.length) - 1
    second_mask = ((1 << second.length) - 1) << first.length
    outside_first = (count - 1) ^ first_mask
    outside_second = (count - 1) ^ second_mask
    adjacency = array("I", [0]) * count
    exceptional = bytearray(count)

    for vertex in range(count):
        s = first.syndromes[vertex & first_mask]
        t = second.syndromes[(vertex & second_mask) >> first.length]
        exceptional[vertex] = s in first.A and t in second.A

    selected_edges = 0
    for vertex in range(count):
        s = first.syndromes[vertex & first_mask]
        t = second.syndromes[(vertex & second_mask) >> first.length]
        for direction in range(n):
            bit = 1 << direction
            if vertex & bit:
                continue
            other = vertex ^ bit
            if exceptional[vertex] or exceptional[other]:
                continue
            chosen = False
            if direction < first.length:
                chosen = first.selected(s, s ^ first.labels[direction])
            elif direction < first.length + second.length:
                local = direction - first.length
                chosen = second.selected(t, t ^ second.labels[local])
            if direction >= first.length and s in first.A:
                parity = (vertex & outside_first).bit_count() & 1
                chosen |= parity == (0 if s in first.C else 1)
            if not first.length <= direction < first.length + second.length and t in second.A:
                parity = (vertex & outside_second).bit_count() & 1
                chosen |= parity == (0 if t in second.C else 1)
            if chosen:
                adjacency[vertex] |= bit
                adjacency[other] |= bit
                selected_edges += 1
    return n, first, second, adjacency, exceptional, selected_edges


def insert_two_zero_bits(value, first, second):
    lower = value & ((1 << first) - 1)
    value = lower | ((value >> first) << (first + 1))
    lower = value & ((1 << second) - 1)
    return lower | ((value >> second) << (second + 1))


def face_audit(n, adjacency, exceptional, require_every_missing):
    count = 1 << n
    witnesses = array("I", [0]) * count
    faces = three_edge_faces = 0
    for first in range(n):
        bit_first = 1 << first
        for second in range(first + 1, n):
            bit_second = 1 << second
            for compressed in range(1 << (n - 2)):
                base = insert_two_zero_bits(compressed, first, second)
                flags = (
                    bool(adjacency[base] & bit_first),
                    bool(adjacency[base] & bit_second),
                    bool(adjacency[base ^ bit_first] & bit_second),
                    bool(adjacency[base ^ bit_second] & bit_first),
                )
                total = sum(flags)
                require(total < 4, "cube contains a square")
                if total == 3:
                    three_edge_faces += 1
                    if not flags[0]:
                        witnesses[base] |= bit_first
                    elif not flags[1]:
                        witnesses[base] |= bit_second
                    elif not flags[2]:
                        witnesses[base ^ bit_first] |= bit_second
                    else:
                        witnesses[base ^ bit_second] |= bit_first
                faces += 1

    selected = missing = unwitnessed = 0
    for vertex in range(count):
        for direction in range(n):
            bit = 1 << direction
            if vertex & bit:
                continue
            other = vertex ^ bit
            if adjacency[vertex] & bit:
                selected += 1
            else:
                missing += 1
                if not witnesses[vertex] & bit:
                    unwitnessed += 1
                    require(not require_every_missing and
                            (exceptional[vertex] or exceptional[other]),
                            "unwitnessed edge outside permitted exceptional set")
    return {
        "faces": faces,
        "missing_edges": missing,
        "selected_edges": selected,
        "three_edge_faces": three_edge_faces,
        "unwitnessed_edges": unwitnessed,
    }


def currently_witnessed(adjacency, vertex, direction):
    bit = 1 << direction
    other = vertex ^ bit
    candidates = adjacency[vertex] & adjacency[other] & ~bit
    while candidates:
        transverse = candidates & -candidates
        if adjacency[vertex ^ transverse] & bit:
            return True
        candidates ^= transverse
    return False


def complete_cube(n, adjacency, exceptional):
    added = 0
    for vertex in range(1 << n):
        for direction in range(n):
            bit = 1 << direction
            if vertex & bit or adjacency[vertex] & bit:
                continue
            other = vertex ^ bit
            if not (exceptional[vertex] or exceptional[other]):
                continue
            if not currently_witnessed(adjacency, vertex, direction):
                adjacency[vertex] |= bit
                adjacency[other] |= bit
                added += 1
    return added


def audit_arithmetic():
    parameters = {
        "H": (4, 4, 3, 4, 8),
        "S": (4, 3, 4, 3, 8),
        "F": (16, 10, 5, 29, 33),
    }

    def block(name, scale):
        q, t, a, r0, r1 = parameters[name]
        return {
            "length": t * scale - 1,
            "h": Fraction(r0 + (scale - 1) * r1, q * scale),
            "delta": Fraction(a, q * scale),
        }

    def select(n):
        x = n + 2
        scale = 1 << ((x // 16).bit_length() - 1)
        if x < 18 * scale:
            names = (("H", 2 * scale), ("H", 2 * scale))
        elif x < 20 * scale:
            names = (("H", 2 * scale), ("F", scale))
        elif x < 22 * scale:
            names = (("H", 2 * scale), ("S", 4 * scale))
        elif x < 24 * scale:
            names = (("F", scale), ("S", 4 * scale))
        elif x < 28 * scale:
            names = (("S", 4 * scale), ("S", 4 * scale))
        else:
            names = (("S", 4 * scale), ("H", 4 * scale))
        return block(*names[0]), block(*names[1])

    consecutive = 0
    for n in range(14, 100001):
        first, second = select(n)
        require(first["length"] + second["length"] <= n, "negative padding")
        coefficient = (
            first["h"] + second["h"]
            + ((n - first["length"]) * first["delta"]
               + (n - second["length"]) * second["delta"]) / 4
            + n * first["delta"] * second["delta"]
        )
        require(coefficient < 6 + Fraction(49, n + 2), "uniform inequality")
        consecutive += 1
    return {"consecutive_dimensions_checked": consecutive, "last_dimension": 100000}


def main():
    require(len(sys.argv) == 2, "usage: independent_audit.py TARGET_TEMPLATES_JSON")
    published = json.loads(Path(sys.argv[1]).read_text())
    require(published == TEMPLATES, "published templates differ from proof reconstruction")
    finite = [audit_template(template) for template in TEMPLATES]
    quotients = [audit_quotient(template, 32) for template in TEMPLATES]
    arithmetic = audit_arithmetic()

    n, first, second, adjacency, exceptional, initial_edges = make_initial_cube()
    initial = face_audit(n, adjacency, exceptional, False)
    require(initial["selected_edges"] == initial_edges, "initial edge-count mismatch")
    require(initial["unwitnessed_edges"] > 0, "extension test did not exercise completion")
    added = complete_cube(n, adjacency, exceptional)
    final = face_audit(n, adjacency, exceptional, True)
    require(final["unwitnessed_edges"] == 0, "completed cube is not saturated")
    bound = (
        first.h + second.h
        + ((n - first.length) * first.delta + (n - second.length) * second.delta) / 4
        + n * first.delta * second.delta
    )
    require(final["selected_edges"] == initial_edges + added, "completion edge count")
    require(final["selected_edges"] <= bound * (1 << n), "finite bound failure")

    print(json.dumps({
        "arithmetic": arithmetic,
        "dimension_19_extension": {
            "blocks": [["H", 2], ["S", 4]],
            "bound_coefficient": str(bound),
            "completion_edges": added,
            "exceptional_vertices": sum(exceptional),
            "final": final,
            "initial": initial,
            "initial_edges": initial_edges,
            "padding": 1,
        },
        "finite_templates": finite,
        "new_scale_32_quotients": quotients,
        "status": "PASS",
        "trust_boundary": (
            "Exact finite corroboration. The universal replication, composition, "
            "greedy completion, and interval arguments remain human-audited proofs."
        ),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
