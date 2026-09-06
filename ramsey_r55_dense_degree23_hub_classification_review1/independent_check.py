#!/usr/bin/env python3
"""Independent audit of the dense degree-23 hub classification and consumer.

No module from the reviewed package is imported.  The local tuple families
are enumerated afresh without affine normalization, in variable order
X2,X4,X3,X0,X1.  Optional replay checks consume regenerated CNFs/DRAT files.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import argparse
import json
from pathlib import Path
import subprocess


CORE_N = 17
GRAPH_N = 43
CORE_ALL = (1 << CORE_N) - 1
PAIRS_43 = list(combinations(range(GRAPH_N), 2))
S_RED = {
    62: {(0, 2), (0, 3), (0, 4), (1, 2), (1, 3)},
    126: {(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)},
}
EXPECTED_TYPES = [126] * 5 + [15] + [62] * 3 + [126] * 4
EXPECTED_TUPLE_SHA = {
    62: "b314d237f489f94600ccd90e0ef7c7ac3faaf98a9910ae09ce4adfc8e827651c",
    126: "6006ad0f7d35b0ffe64128a1702d06924e755e46b675b0eaca8e7798d65b69fa",
}
EXPECTED_MANIFEST_SHA = "e5d7b3b63e4508537c65cedeec9ef38c1ba39ca6e636349eb4f78227d15c214a"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return sha256(data).hexdigest()


def paley_rows():
    squares = {1, 2, 4, 8, 9, 13, 15, 16}
    return [sum(1 << v for v in range(CORE_N) if v != u and (v - u) % 17 in squares)
            for u in range(CORE_N)]


def complete_mask_tables(red_rows):
    independent = bytearray(CORE_ALL + 1)
    clique = bytearray(CORE_ALL + 1)
    red_triangle_free = bytearray(CORE_ALL + 1)
    blue_triangle_free = bytearray(CORE_ALL + 1)
    independent[0] = clique[0] = red_triangle_free[0] = blue_triangle_free[0] = 1
    blue_rows = [CORE_ALL ^ (1 << v) ^ red_rows[v] for v in range(CORE_N)]
    for mask in range(1, CORE_ALL + 1):
        bit = mask & -mask
        vertex = bit.bit_length() - 1
        rest = mask ^ bit
        independent[mask] = independent[rest] and not (red_rows[vertex] & rest)
        clique[mask] = clique[rest] and not (blue_rows[vertex] & rest)
        red_triangle_free[mask] = (
            red_triangle_free[rest] and independent[red_rows[vertex] & rest]
        )
        blue_triangle_free[mask] = (
            blue_triangle_free[rest] and clique[blue_rows[vertex] & rest]
        )
    return independent, clique, red_triangle_free, blue_triangle_free


def build_column_domain(red_rows):
    independent, clique, red_tf, blue_tf = complete_mask_tables(red_rows)
    require(max(mask.bit_count() for mask in range(CORE_ALL + 1) if red_tf[mask]) == 8,
            "triangle-free column maximum")
    columns = [mask for mask in range(CORE_ALL + 1)
               if 5 <= mask.bit_count() <= 8 and red_tf[mask]]
    histogram = Counter(mask.bit_count() for mask in columns)
    require(histogram == Counter({5: 2550, 6: 2176, 7: 816, 8: 51}), "column domain")
    bits = [1 << i for i in range(len(columns))]
    red_compatible = []
    blue_compatible = []
    for left in columns:
        red_bits = 0
        blue_bits = 0
        for index, right in enumerate(columns):
            if independent[left & right]:
                red_bits |= bits[index]
            if blue_tf[CORE_ALL ^ (left | right)]:
                blue_bits |= bits[index]
        red_compatible.append(red_bits)
        blue_compatible.append(blue_bits)
    at_least = []
    for size in range(9):
        at_least.append(sum(bits[i] for i, mask in enumerate(columns) if mask.bit_count() >= size))
    return columns, clique, red_compatible, blue_compatible, at_least


def enumerate_family(kind, tables):
    independent_triples = [q for q in combinations(range(5), 3)
                           if all(tuple(sorted(edge)) not in S_RED[kind]
                                  for edge in combinations(q, 2))]
    require(not any(all(tuple(sorted(edge)) in S_RED[kind] for edge in combinations(q, 2))
                    for q in combinations(range(5), 3)), "red triangle in S")
    require(not any(all(tuple(sorted(edge)) not in S_RED[kind] for edge in combinations(q, 2))
                    for q in combinations(range(5), 4)), "independent four-set in S")
    require(independent_triples == [(2, 3, 4)], "independent triples in S")
    columns, clique, red_compatible, blue_compatible, at_least = tables
    full = (1 << len(columns)) - 1
    order = [2, 4, 3, 0, 1]
    chosen = {}
    solutions = []
    visits = Counter()

    def dfs(depth, total, domains):
        visits[depth] += 1
        if depth == 5:
            solutions.append(tuple(columns[chosen[s]] for s in range(5)))
            return
        variable = order[depth]
        threshold = max(0, 37 - total - 8 * (4 - depth))
        if threshold > 8:
            return
        candidates = domains[variable] & at_least[threshold]
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            index = bit.bit_length() - 1
            chosen[variable] = index
            if all(s in chosen for s in (2, 3, 4)):
                missed = CORE_ALL ^ (columns[chosen[2]] | columns[chosen[3]] | columns[chosen[4]])
                if not clique[missed]:
                    del chosen[variable]
                    continue
            next_domains = list(domains)
            possible = True
            for future in order[depth + 1:]:
                pair = tuple(sorted((variable, future)))
                compatibility = red_compatible if pair in S_RED[kind] else blue_compatible
                next_domains[future] &= compatibility[index]
                if not next_domains[future]:
                    possible = False
                    break
            if possible:
                dfs(depth + 1, total + columns[index].bit_count(), next_domains)
            del chosen[variable]

    dfs(0, 0, [full] * 5)
    require(len(solutions) == len(set(solutions)), f"duplicate type-{kind} tuple")
    require({sum(mask.bit_count() for mask in row) for row in solutions} == {37}, "density boundary")
    solutions.sort()
    raw = "".join(" ".join(map(str, row)) + "\n" for row in solutions).encode()
    return solutions, raw, dict(sorted(visits.items()))


def s_automorphisms(kind):
    return [p for p in permutations(range(5))
            if {tuple(sorted((p[u], p[v]))) for u, v in S_RED[kind]} == S_RED[kind]]


def core_automorphisms(red_rows):
    neighbors = [v for v in range(1, 17) if red_rows[0] >> v & 1]
    outside = [v for v in range(1, 17) if not (red_rows[0] >> v & 1)]
    signature_to_vertex = {
        frozenset(v for v in neighbors if red_rows[u] >> v & 1): u for u in outside
    }
    require(len(signature_to_vertex) == 8, "nonunique outside signatures")
    local = 0
    stabilizer = set()
    for order in permutations(neighbors):
        mapping = {0: 0, **dict(zip(neighbors, order))}
        if any(bool(red_rows[u] >> v & 1) != bool(red_rows[mapping[u]] >> mapping[v] & 1)
               for u, v in combinations(neighbors, 2)):
            continue
        local += 1
        for vertex in outside:
            moved_signature = frozenset(mapping[v] for v in neighbors if red_rows[vertex] >> v & 1)
            if moved_signature not in signature_to_vertex:
                break
            mapping[vertex] = signature_to_vertex[moved_signature]
        else:
            image = tuple(mapping[v] for v in range(17))
            if sorted(image) == list(range(17)) and all(
                bool(red_rows[u] >> v & 1) == bool(red_rows[image[u]] >> image[v] & 1)
                for u, v in combinations(range(17), 2)
            ):
                stabilizer.add(image)
    require(local == 16 and len(stabilizer) == 8, "core stabilizer proof")
    actions = {tuple((image[v] + shift) % 17 for v in range(17))
               for image in stabilizer for shift in range(17)}
    require(len(actions) == 136, "core automorphism count")
    require(all(bool(red_rows[u] >> v & 1) == bool(red_rows[action[u]] >> action[v] & 1)
                for action in actions for u, v in combinations(range(17), 2)),
            "invalid core action")
    return sorted(actions)


def clique_exists(rows, size):
    def search(candidates, left):
        if left == 0:
            return True
        while candidates.bit_count() >= left:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            if search(candidates & rows[vertex], left - 1):
                return True
        return False
    return search((1 << len(rows)) - 1, size)


def representative_rows(kind, columns, red_rows):
    rows = [0] * 23
    for u in range(17):
        rows[u] |= red_rows[u]
    for u, v in S_RED[kind]:
        rows[17 + u] |= 1 << (17 + v)
        rows[17 + v] |= 1 << (17 + u)
    for s, mask in enumerate(columns):
        vertex = 17 + s
        rows[vertex] |= 1 << 22
        rows[22] |= 1 << vertex
        for core in range(17):
            if mask >> core & 1:
                rows[vertex] |= 1 << core
                rows[core] |= 1 << vertex
    return rows


def transformed_column(mask, action):
    return sum(1 << action[v] for v in range(17) if mask >> v & 1)


def verify_certificate(certificate, families, red_rows, actions):
    require(certificate.get("minimum_cross_edges") == 37, "certificate threshold")
    cert_by_kind = {family["type"]: family for family in certificate["families"]}
    result = []
    for kind in (62, 126):
        solutions, raw, visits = families[kind]
        expected_count = 6528 if kind == 62 else 47328
        expected_classes = 24 if kind == 62 else 29
        require(len(solutions) == expected_count and digest(raw) == EXPECTED_TUPLE_SHA[kind],
                f"independent type-{kind} enumeration")
        solution_set = set(solutions)
        family = cert_by_kind[kind]
        require(family["labeled_count"] == expected_count, "certificate labeled count")
        require(family["full_tuple_sha256"] == EXPECTED_TUPLE_SHA[kind], "certificate tuple digest")
        require(len(family["representatives"]) == expected_classes, "certificate class count")
        s_actions = s_automorphisms(kind)
        require(len(s_actions) == (2 if kind == 62 else 12), "S automorphism count")
        expanded = set()
        for entry in family["representatives"]:
            row = tuple(entry["columns"])
            physical = representative_rows(kind, row, red_rows)
            degrees = [neighbors.bit_count() for neighbors in physical]
            require([v for v, degree in enumerate(degrees) if degree == 5] == [22], "unique hub")
            require(sum(degrees) // 2 == (115 if kind == 62 else 116), "representative density")
            blue = [((1 << 23) - 1) ^ physical[u] ^ (1 << u) for u in range(23)]
            require(not clique_exists(physical, 4) and not clique_exists(blue, 5), "invalid representative")
            orbit = {
                tuple(transformed_column(row[p[s]], action) for s in range(5))
                for p in s_actions for action in actions
            }
            require(len(orbit) == entry["orbit_size"] == 136 * len(s_actions), "nonrigid representative")
            require(min(orbit) == row and not (expanded & orbit), "bad canonical orbit")
            expanded |= orbit
        require(expanded == solution_set, f"certificate does not partition type-{kind} family")
        result.append({
            "type": kind,
            "labeled_tuples": len(solutions),
            "isomorphism_classes": len(family["representatives"]),
            "maximum_edges": 115 if kind == 62 else 116,
            "all_rigid": True,
            "tuple_sha256": digest(raw),
            "search_visits_by_depth": visits,
        })
    return result


def parse_graph6(record):
    require(record and 63 <= ord(record[0]) < 126, "graph6 header")
    order = ord(record[0]) - 63
    bit_count = order * (order - 1) // 2
    require(order < 63 and len(record) == 1 + (bit_count + 5) // 6, "graph6 length")
    bits = "".join(f"{ord(char) - 63:06b}" for char in record[1:])[:bit_count]
    edges = set()
    position = 0
    for v in range(order):
        for u in range(v):
            if bits[position] == "1":
                edges.add((u, v))
            position += 1
    return order, edges


def graph_rows(order, edges):
    rows = [0] * order
    for u, v in edges:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return rows


def interface_data(record):
    order, edges = parse_graph6(record)
    require(order == 22 and len(edges) == 109, "interface order/density")
    rows = graph_rows(order, edges)
    blue = [((1 << order) - 1) ^ rows[u] ^ (1 << u) for u in range(order)]
    require(not clique_exists(rows, 4) and not clique_exists(blue, 5), "invalid interface")
    require([u for u in range(order) if rows[u].bit_count() == 5] == [21], "interface hub")
    S = sorted(v for v in range(21) if (v, 21) in edges)
    profile = sorted(sum((min(u, v), max(u, v)) in edges for v in S) for u in S)
    kind = 15 if profile == [1, 1, 1, 1, 4] else 62 if profile == [1, 2, 2, 2, 3] else 126 if profile == [2, 2, 2, 3, 3] else None
    require(kind is not None, "unknown interface type")
    return edges, rows, S, kind


def markings(edges, S, kind):
    return [p for p in permutations(S) if all(
        ((min(p[u], p[v]), max(p[u], p[v])) in edges) == ((u, v) in S_RED[kind])
        for u, v in combinations(range(5), 2)
    )]


def boundary_matrix(edges, mark, columns, red_rows):
    owner = {vertex: s for s, vertex in enumerate(mark)}
    symbols = []
    for u, v in PAIRS_43:
        value = None
        if v < 22:
            value = int((u, v) in edges)
        elif v == 22:
            value = int(u < 22)
        elif u == 22:
            value = 0
        elif u == 21:
            value = int(v < 40)
        elif 23 <= u < v < 40:
            value = int(red_rows[u - 23] >> (v - 23) & 1)
        elif u in owner and 23 <= v < 40:
            value = int(columns[owner[u]] >> (v - 23) & 1)
        symbols.append("2" if value is None else str(value))
    require(len(symbols) == 903 and symbols.count("2") == 389, "boundary fixed/free count")
    return "".join(symbols).encode()


def boundary_cover(inputs, certificate, red_rows):
    cert = {family["type"]: family for family in certificate["families"]}
    data = []
    kinds = []
    keys = {62: set(), 126: set()}
    matrices = {}
    for index, record in enumerate(inputs["interfaces"]):
        edges, rows, S, kind = interface_data(record)
        kinds.append(kind)
        data.append((edges, rows, S, kind))
        if kind == 15:
            require(index == 5, "star position")
            continue
        marks = markings(edges, S, kind)
        require(len(marks) == (2 if kind == 62 else 12), "relative marking count")
        for representative, entry in enumerate(cert[kind]["representatives"]):
            for mark_index, mark in enumerate(marks):
                key = (index, kind, representative, mark_index)
                matrix = boundary_matrix(edges, mark, entry["columns"], red_rows)
                require(key not in keys[kind], "duplicate boundary key")
                keys[kind].add(key)
                if kind == 62:
                    matrices[key] = matrix
    require(kinds == EXPECTED_TYPES, "thirteen-interface type split")
    require(len(keys[62]) == 144 and len(keys[126]) == 3132, "boundary cover size")
    return data, keys, matrices


def literal_cnf(matrix):
    require(len(matrix) == 903 and set(matrix) <= {48, 49, 50}, "matrix encoding")
    colors = dict(zip(PAIRS_43, (byte - 48 for byte in matrix)))
    variable = {edge: index + 1 for index, edge in enumerate(edge for edge in PAIRS_43 if colors[edge] == 2)}
    clauses = set()
    for vertices in combinations(range(43), 5):
        selected = list(combinations(vertices, 2))
        values = [colors[edge] for edge in selected]
        if 1 not in values:
            clauses.add(tuple(variable[edge] for edge, value in zip(selected, values) if value == 2))
        if 0 not in values:
            clauses.add(tuple(-variable[edge] for edge, value in zip(selected, values) if value == 2))
    raw = (f"p cnf {len(variable)} {len(clauses)}\n" +
           "".join(" ".join(map(str, clause)) + " 0\n" for clause in sorted(clauses))).encode()
    return raw


def verify_replay(source, replay, drat_trim, matrices, manifest):
    gluing = replay / "gluing"
    require((gluing / "manifest.json").read_bytes() == (source / "GLUING_MANIFEST.json").read_bytes(),
            "replayed manifest differs")
    runs = json.loads((gluing / "runs.json").read_text())
    require(len(runs) == 144, "replayed case count")
    run_by_key = {tuple(row["key"]): row for row in runs}
    require(set(run_by_key) == set(matrices), "replayed key coverage")
    proof_bytes = 0
    for item in manifest:
        key = tuple(item["key"])
        stem = "-".join(map(str, key))
        matrix_path = gluing / f"{stem}.matrix"
        cnf_path = gluing / f"{stem}.cnf"
        second_cnf = gluing / f"{stem}.independent.cnf"
        proof_path = gluing / f"{stem}.drat"
        require(matrix_path.read_bytes() == matrices[key], f"physical matrix mismatch at {key}")
        cnf = cnf_path.read_bytes()
        require(cnf == second_cnf.read_bytes(), f"two formula encoders differ at {key}")
        require(digest(cnf) == item["cnf_sha256"] == run_by_key[key]["cnf_sha256"], f"CNF digest at {key}")
        header = cnf.splitlines()[0].split()
        require(header[:3] == [b"p", b"cnf", b"389"] and int(header[3]) == item["clauses"], "DIMACS header")
        require(len(cnf.splitlines()) - 1 == item["clauses"], "DIMACS clause count")
        checked = subprocess.run([str(drat_trim), str(cnf_path), str(proof_path)],
                                 text=True, capture_output=True)
        require(checked.returncode == 0 and "s VERIFIED" in checked.stdout, f"DRAT failure at {key}")
        proof_bytes += proof_path.stat().st_size

    # A third literal five-set encoder is expensive, so rebuild one formula
    # for each original interface.  The author replay already compares two
    # independent encoders on all 144 cases.
    spot_keys = [(6, 62, 0, 0), (7, 62, 0, 0), (8, 62, 0, 0)]
    for key in spot_keys:
        stem = "-".join(map(str, key))
        require(literal_cnf(matrices[key]) == (gluing / f"{stem}.cnf").read_bytes(),
                f"literal CNF spot check at {key}")
    require(proof_bytes == 16851125, "proof byte total")
    return {
        "complete_cases": len(runs),
        "free_edges_per_case": 389,
        "all_Drat_proofs_reverified": True,
        "proof_bytes": proof_bytes,
        "third_encoder_spot_cases": [list(key) for key in spot_keys],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--replay", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    args = parser.parse_args()
    if bool(args.replay) != bool(args.drat_trim):
        raise ValueError("supply --replay and --drat-trim together")
    source = args.source.resolve()
    red_rows = paley_rows()
    tables = build_column_domain(red_rows)
    families = {}
    for kind in (62, 126):
        families[kind] = enumerate_family(kind, tables)
    actions = core_automorphisms(red_rows)
    certificate = json.loads((source / "certificate.json").read_text())
    local = verify_certificate(certificate, families, red_rows, actions)
    inputs = json.loads((source / "inputs.json").read_text())
    require(len(inputs.get("interfaces", [])) == 13, "input record count")
    _, keys, matrices = boundary_cover(inputs, certificate, red_rows)
    manifest_raw = (source / "GLUING_MANIFEST.json").read_bytes()
    require(digest(manifest_raw) == EXPECTED_MANIFEST_SHA, "manifest digest")
    manifest = json.loads(manifest_raw)
    manifest_keys = {tuple(item["key"]) for item in manifest}
    require(manifest_keys == keys[62] and len(manifest) == 144, "manifest boundary coverage")
    require(all(item["variables"] == 389 for item in manifest), "manifest variable count")
    replay = None
    if args.replay:
        replay = verify_replay(source, args.replay.resolve(), args.drat_trim.resolve(), matrices, manifest)

    report = {
        "status": "INDEPENDENTLY_VERIFIED_DENSE_HUB_CLASSIFICATION_AND_TYPE62_EXCLUSION",
        "local_classification": local,
        "core_automorphisms": len(actions),
        "column_domain_histogram": {str(k): v for k, v in sorted(Counter(mask.bit_count() for mask in tables[0]).items())},
        "boundary_cover": {
            "type62_keys": len(keys[62]),
            "type126_keys": len(keys[126]),
            "free_edges_per_key": 389,
            "type62_manifest_sha256": digest(manifest_raw),
            "type62_density115_excluded": replay is not None,
            "type62_new_deficiency_lower_bound": 8 if replay is not None else None,
            "type126_density116_excluded": False,
        },
        "proof_replay": replay,
        "scope": {
            "imports_R44_17_uniqueness": True,
            "imports_thirteen_interface_completeness": True,
            "entire_degree23_interface_excluded": False,
            "Ramsey_5_5_43_graph_constructed": False,
            "R_5_5_bound_improved": False,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
