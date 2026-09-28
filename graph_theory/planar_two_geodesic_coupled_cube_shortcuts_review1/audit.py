#!/usr/bin/env python3
"""Independent exact replay of the coupled-cube finite certificates."""

from collections import deque
from fractions import Fraction
from functools import reduce
from itertools import combinations
from math import gcd
from pathlib import Path
import hashlib
import json


SOURCE = Path(__file__).resolve().parents[1] / "planar_two_geodesic_coupled_cube_shortcuts"
PRICE_A = (14, 38, 7, 23, 20, 17, 8, 30, 11, 21, 14, 29,
           10, 28, 36, 4, 3, 7, 30, 6, 2, 4, 9, 5)
PRICE_B = (7, 10, 4, 8, 7, 11, 9, 6, 16, 14, 3, 23,
           3, 16, 15, 16, 3, 10, 22, 9, 12, 3, 12, 7)
SHORTCUTS = ((8, 15), (8, 16), (10, 14), (10, 16), (12, 14), (12, 15))
MARKS = tuple(range(17, 26))


def geometry():
    # Binary-coordinate construction, independent of an oriented face list.
    adj = [set() for _ in range(26)]
    triangles = []
    core = []
    def edge(u, v):
        adj[u].add(v)
        adj[v].add(u)
    for v in range(8):
        for axis in range(3):
            f = 8 + 2 * axis + (v >> axis & 1)
            edge(v, f)
            core.append((v, f))
    cube_edges = [(a, b) for a, b in combinations(range(8), 2)
                  if a ^ b in (1, 2, 4)]
    for z, (a, b) in enumerate(cube_edges, 14):
        axis = (a ^ b).bit_length() - 1
        edge(z, a)
        edge(z, b)
        for other in range(3):
            if other == axis:
                continue
            f = 8 + 2 * other + (a >> other & 1)
            edge(z, f)
            triangles.extend(((a, z, f), (b, z, f)))
    edges = {tuple(sorted((u, v))) for u, ns in enumerate(adj) for v in ns}
    assert len(core) == 24 and len(edges) == 72 and len(triangles) == 48
    assert set(SHORTCUTS) <= edges
    incidence = {e: 0 for e in edges}
    for t in triangles:
        for u, v in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            incidence[tuple(sorted((u, v)))] += 1
    assert set(incidence.values()) == {2} and 26 - 72 + 48 == 2
    for v in range(26):
        link = {u: set() for u in adj[v]}
        for t in triangles:
            if v in t:
                a, b = (u for u in t if u != v)
                link[a].add(b)
                link[b].add(a)
        assert all(len(ns) == 2 for ns in link.values())
        seen = {next(iter(link))}
        todo = list(seen)
        while todo:
            u = todo.pop()
            for w in link[u] - seen:
                seen.add(w)
                todo.append(w)
        assert seen == set(link)
    assert all(len(adj[z]) == 4 for z in MARKS)
    return adj, tuple(sorted(core))


ADJ, CORE = geometry()


def dijkstra_core(prices, shortcuts=()):
    adj = [[] for _ in range(17)]
    for (a, b), weight in list(prices.items()) + list(shortcuts):
        adj[a].append((b, weight))
        adj[b].append((a, weight))
    result = []
    for source in range(17):
        distances = [None] * 17
        distances[source] = 0
        queue = deque([source])
        # Exact Bellman--Ford relaxation on a tiny undirected nonnegative graph.
        while queue:
            u = queue.popleft()
            for v, weight in adj[u]:
                candidate = distances[u] + weight
                if distances[v] is None or candidate < distances[v]:
                    distances[v] = candidate
                    queue.append(v)
        result.append(distances)
    return result


def route_catalog(prices):
    d = dijkstra_core(prices)
    adj = [set() for _ in range(17)]
    for a, b in list(prices) + list(SHORTCUTS):
        adj[a].add(b)
        adj[b].add(a)
    routes = {(s, t): [] for s in range(17) for t in range(s, 17)}
    for s in range(17):
        def visit(path, anchor, spent):
            u = path[-1]
            if u >= s:
                routes[s, u].append(tuple(path))
            for v in sorted(adj[u]):
                if v in path:
                    continue
                if u < 14 and v < 14:
                    new_spent = spent + prices[tuple(sorted((u, v)))]
                    if new_spent == d[anchor][v]:
                        visit(path + [v], anchor, new_spent)
                elif v < 14:
                    visit(path + [v], v, 0)
                else:
                    visit(path + [v], None, 0)
        visit([s], s if s < 14 else None, 0)
    assert all(routes.values())
    return routes


def components_after(deleted):
    remaining = set(range(26)) - deleted
    pieces = []
    while remaining:
        seed = remaining.pop()
        piece = {seed}
        queue = [seed]
        while queue:
            u = queue.pop()
            new = ADJ[u] & remaining
            remaining.difference_update(new)
            piece.update(new)
            queue.extend(new)
        pieces.append(piece)
    return pieces


def parent_variables():
    return {(z, p): 1 + 4 * (z - 17) + j
            for z in MARKS for j, p in enumerate(sorted(ADJ[z]))}


PARENTS = parent_variables()


def four_residue(pair):
    assert len(pair) == 2
    deleted = set(pair[0]) | set(pair[1])
    return max((len(piece & set(MARKS)) for piece in components_after(deleted)), default=0) <= 4


def extract_core_path(path):
    assert path and len(path) == len(set(path))
    assert all(0 <= v < 26 for v in path)
    assert all(v in ADJ[u] for u, v in zip(path, path[1:]))
    assert all(v < 17 for v in path[1:-1])
    conditions = set()
    if len(path) > 1 and path[0] in MARKS:
        conditions.add((path[0], path[1]))
    if len(path) > 1 and path[-1] in MARKS:
        conditions.add((path[-1], path[-2]))
    middle = tuple(v for v in path if v < 17)
    if middle and middle[0] > middle[-1]:
        middle = tuple(reversed(middle))
    return middle, conditions


def affine(path, prices):
    result = [0] * 7
    lookup = {e: j for j, e in enumerate(SHORTCUTS)}
    for u, v in zip(path, path[1:]):
        edge = tuple(sorted((u, v)))
        if edge in prices:
            result[6] += prices[edge]
        else:
            result[lookup[edge]] += 1
    return tuple(result)


def primitive(vector):
    values = tuple(int(v) for v in vector)
    factor = reduce(gcd, (abs(v) for v in values), 0)
    return tuple(v // factor for v in values) if factor else values


class Clauses:
    def __init__(self):
        self.next_id = 1
        self.atoms = {}
        self.vectors = {}
        self.clauses = []

    def variable(self):
        answer = self.next_id
        self.next_id += 1
        return answer

    def nonnegative(self, vector):
        v = primitive(vector)
        if not any(v[:6]):
            return v[6] >= 0
        if v not in self.atoms:
            number = self.variable()
            self.atoms[v] = number
            self.vectors[number] = v
        return self.atoms[v]

    def positive(self, vector):
        value = self.nonnegative(tuple(-v for v in vector))
        return (not value) if type(value) is bool else -value

    def add(self, literals):
        if any(v is True for v in literals):
            return
        clause = set(v for v in literals if v is not False)
        if any(-v in clause for v in clause):
            return
        self.clauses.append(tuple(sorted(clause)))


def exactly_one(enc):
    parents = {(z, p): enc.variable() for z in MARKS for p in sorted(ADJ[z])}
    assert parents == PARENTS
    for z in MARKS:
        group = [parents[z, p] for p in sorted(ADJ[z])]
        enc.add(group)
        for a, b in combinations(group, 2):
            enc.add((-a, -b))


def rup_check(base, proof):
    database = list(base)
    for proposed in proof:
        assert len(proposed) == len(set(proposed))
        assigned = {}
        queue = deque(-lit for lit in proposed)
        conflict = False
        while True:
            while queue:
                lit = queue.popleft()
                v, value = abs(lit), lit > 0
                if v in assigned and assigned[v] != value:
                    conflict = True
                    break
                assigned[v] = value
            if conflict:
                break
            progress = False
            for clause in database:
                unknown = []
                true = False
                for lit in clause:
                    if abs(lit) not in assigned:
                        unknown.append(lit)
                    elif assigned[abs(lit)] == (lit > 0):
                        true = True
                        break
                if true:
                    continue
                if not unknown:
                    conflict = True
                    break
                if len(unknown) == 1:
                    queue.append(unknown[0])
                    progress = True
            if conflict or not progress:
                break
        assert conflict, ("invalid RUP", proposed)
        database.append(tuple(proposed))
    assert proof and proof[-1] == []
    return len(proof)


def verify_A(data):
    prices = {(a, b): w for a, b, w in data["prices"]}
    assert sorted(prices) == list(CORE)
    assert tuple(prices[e] for e in CORE) == PRICE_A
    assert data["variable_edges"] == [list(e) for e in SHORTCUTS]
    routes = route_catalog(prices)
    assert sum(map(len, routes.values())) == 1066
    route_sets = {pair: set(paths) for pair, paths in routes.items()}
    enc = Clauses()
    exactly_one(enc)
    for i in range(6):
        vector = [0] * 7
        vector[i] = 1
        enc.add((enc.positive(vector),))
    assert len(data["pairs"]) == 48
    for pair in data["pairs"]:
        assert four_residue(pair)
        forced = set()
        cores = []
        for path in pair:
            middle, conditions = extract_core_path(path)
            forced.update(conditions)
            if middle:
                assert middle in route_sets[middle[0], middle[-1]]
                cores.append(middle)
        clause = [-PARENTS[z, p] for z, p in sorted(forced)]
        for path in cores:
            left = affine(path, prices)
            for rival in routes[path[0], path[-1]]:
                right = affine(rival, prices)
                clause.append(enc.positive(tuple(a - b for a, b in zip(left, right))))
        enc.add(clause)
    assert len(enc.clauses) == 117
    for number, vector in data["extra_linear_atoms"]:
        assert number == enc.next_id
        assert primitive(vector) == tuple(vector)
        assert enc.nonnegative(vector) == number
    assert len(enc.vectors) == 177
    assert len(data["farkas"]) == 217
    strict_count = 0
    for row in data["farkas"]:
        total = [Fraction(0) for _ in range(7)]
        strict = False
        for literal, weight_text in row:
            weight = Fraction(weight_text)
            assert weight > 0 and abs(literal) in enc.vectors
            vector = enc.vectors[abs(literal)]
            sign = 1 if literal > 0 else -1
            total = [a + sign * weight * b for a, b in zip(total, vector)]
            strict |= literal < 0
        assert all(v == 0 for v in total[:6])
        assert total[6] < 0 or (total[6] == 0 and strict)
        strict_count += total[6] == 0
        enc.add([-lit for lit, _ in row])
    assert rup_check(enc.clauses, data["rup"]) == 28
    return strict_count


def verify_static(data):
    assert {row["metric"] for row in data} == {"B", "symmetric"}
    template_count = additions = 0
    for row in data:
        prices = {(a, b): w for a, b, w in row["prices"]}
        assert sorted(prices) == list(CORE)
        expected = PRICE_B if row["metric"] == "B" else (1,) * 24
        assert tuple(prices[e] for e in CORE) == expected
        assert len(row["templates"]) == (44 if row["metric"] == "B" else 4)
        d0 = dijkstra_core(prices, tuple((e, 0) for e in SHORTCUTS))
        enc = Clauses()
        exactly_one(enc)
        for template in row["templates"]:
            assert len(template["paths"]) == 2
            assert four_residue(template["paths"])
            marked_counts = sorted(len(piece & set(MARKS)) for piece in
                                   components_after(set(template["paths"][0]) |
                                                    set(template["paths"][1])) if piece & set(MARKS))
            assert marked_counts == sorted(template["component_masses"])
            conditions = dict(template["conditions"])
            assert len(conditions) == len(template["conditions"])
            assert all(z in MARKS and p in ADJ[z] for z, p in conditions.items())
            for path in template["paths"]:
                middle, forced = extract_core_path(path)
                assert all(conditions[z] == p for z, p in forced)
                assert middle and all(v < 14 for v in middle)
                cost = sum(prices[tuple(sorted((a, b)))]
                           for a, b in zip(middle, middle[1:]))
                assert cost == d0[middle[0]][middle[-1]]
            enc.add([-PARENTS[z, p] for z, p in template["conditions"]])
            template_count += 1
        additions += rup_check(enc.clauses, row["rup"])
    assert template_count == 48 and additions == 4
    return template_count


def main():
    a_file = SOURCE / "certificate_A.json"
    static_file = SOURCE / "certificate_static.json"
    assert hashlib.sha256(a_file.read_bytes()).hexdigest() == \
        "440d6ee5330a11034d9fe585b4bcc472cba182221bc99d2060ed0f84ff47f604"
    assert hashlib.sha256(static_file.read_bytes()).hexdigest() == \
        "957998ff4ead354c36ec283a44f2fd4a3d1b5ed08ab8b751299fa0126a8e921f"
    strict = verify_A(json.loads(a_file.read_text()))
    static = verify_static(json.loads(static_file.read_text()))
    print(f"A_routes=1066 A_templates=48 A_atoms=177 Farkas=217 "
          f"strict_zero_sum={strict} RUP=28 static_templates={static} static_RUP=4 PASS")


if __name__ == "__main__":
    main()
