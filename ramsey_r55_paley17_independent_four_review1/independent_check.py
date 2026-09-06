#!/usr/bin/env python3
"""Independent exact audit of the Paley-17 independent-four obstruction.

This checker imports no producer module or generated certificate.  It uses a
recursive enumeration of triangle-free subsets and a generic ordered clique
counter, then independently decodes and checks the finite consumer fixtures.
Only Python's standard library is required.
"""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_SHA256 = "f6c53a46d73bb6b6f00cdaaefe06f298ff8b125c003b565b874029ab36a47aab"
RESIDUES = frozenset((1, 2, 4, 8, 9, 13, 15, 16))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def graph6_rows(record):
    """Decode the small-n graph6 format into integer adjacency rows."""
    require(isinstance(record, str) and record, "empty graph6 record")
    values = [ord(char) - 63 for char in record]
    require(all(0 <= value < 64 for value in values), "invalid graph6 character")
    n = values[0]
    require(n < 63, "only the graph6 small-n form is accepted")
    edge_bits = n * (n - 1) // 2
    require(len(values) == 1 + (edge_bits + 5) // 6, "non-canonical graph6 length")

    bits = []
    for value in values[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    require(not any(bits[edge_bits:]), "nonzero graph6 padding")

    rows = [0] * n
    cursor = 0
    for high in range(n):
        for low in range(high):
            if bits[cursor]:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            cursor += 1
    return rows


def complement(rows):
    universe = (1 << len(rows)) - 1
    return [universe ^ (1 << vertex) ^ row for vertex, row in enumerate(rows)]


def edge_count(rows):
    return sum(row.bit_count() for row in rows) // 2


def clique_count(rows, order):
    """Count each clique once by extending vertices in increasing order."""
    if order == 0:
        return 1
    total = 0

    def extend(candidates, needed):
        nonlocal total
        if needed == 0:
            total += 1
            return
        while candidates.bit_count() >= needed:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            extend(candidates & rows[vertex], needed - 1)

    extend((1 << len(rows)) - 1, order)
    return total


def paley_rows():
    rows = [0] * 17
    for u in range(17):
        for v in range(u + 1, 17):
            if (v - u) % 17 in RESIDUES:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
    return rows


def recursively_enumerate_triangle_free(rows):
    """Generate the domain by include/exclude recursion, never scanning 2^17."""
    found = []
    n = len(rows)

    def visit(vertex, chosen):
        if vertex == n:
            found.append(chosen)
            return
        visit(vertex + 1, chosen)

        neighbours = chosen & rows[vertex]
        cursor = neighbours
        safe = True
        while cursor:
            bit = cursor & -cursor
            cursor ^= bit
            u = bit.bit_length() - 1
            if rows[u] & cursor:
                safe = False
                break
        if safe:
            visit(vertex + 1, chosen | (1 << vertex))

    visit(0, 0)
    return found


def has_independent_triple(rows, vertices):
    """Test the omitted-set condition directly, without a mask-domain table."""
    firsts = vertices
    while firsts:
        u_bit = firsts & -firsts
        firsts ^= u_bit
        u = u_bit.bit_length() - 1
        seconds = firsts & ~rows[u]
        while seconds:
            v_bit = seconds & -seconds
            seconds ^= v_bit
            v = v_bit.bit_length() - 1
            if seconds & ~rows[u] & ~rows[v]:
                return True
    return False


def compatibility_graph(rows, columns):
    universe = (1 << len(rows)) - 1
    omissions = [universe ^ column for column in columns]
    loops = [i for i, omitted in enumerate(omissions)
             if not has_independent_triple(rows, omitted)]
    adjacency = [0] * len(columns)
    encoded = bytearray()
    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            if not has_independent_triple(rows, omissions[i] & omissions[j]):
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
                encoded.extend(f"{i} {j}\n".encode("ascii"))
    return loops, adjacency, sha256(encoded).hexdigest()


def audit_local_obstruction():
    rows = paley_rows()
    require(clique_count(rows, 4) == 0, "Paley-17 contains a red K4")
    require(clique_count(complement(rows), 4) == 0, "Paley-17 contains an independent four-set")

    triangle_free = recursively_enumerate_triangle_free(rows)
    domain = set(triangle_free)
    maximal = sorted(
        mask for mask in triangle_free
        if all(mask & (1 << v) or (mask | (1 << v)) not in domain for v in range(17))
    )
    loops, pair_rows, pair_hash = compatibility_graph(rows, maximal)
    clique_counts = [clique_count(pair_rows, k) for k in range(5)]

    require(not loops, "a repeated maximal column is compatible with itself")
    require(clique_counts[4] == 0, "four compatible maximal columns exist")
    return {
        "triangle_free_subsets": len(triangle_free),
        "maximal_columns": len(maximal),
        "column_size_histogram": dict(sorted(Counter(mask.bit_count() for mask in maximal).items())),
        "compatibility_clique_counts": clique_counts,
        "compatible_self_pairs": len(loops),
        "pair_graph_sha256": pair_hash,
    }


def induced_profile(rows, vertices):
    vertex_mask = sum(1 << v for v in vertices)
    return tuple(sorted((rows[v] & vertex_mask).bit_count() for v in vertices))


def audit_interfaces(inputs):
    profiles = {
        (1, 1, 1, 1, 4): "K1,4",
        (1, 2, 2, 2, 3): "K2,3-e",
        (2, 2, 2, 3, 3): "K2,3",
    }
    labels = []
    records = inputs["interfaces"]
    require(len(records) == len(set(records)) == 13, "interfaces are not 13 distinct records")
    for record in records:
        rows = graph6_rows(record)
        require(len(rows) == 22 and edge_count(rows) == 109, "bad interface order or size")
        require(clique_count(rows, 4) == 0, "interface contains a red K4")
        require(clique_count(complement(rows), 5) == 0, "interface contains a blue K5")
        hubs = [v for v, row in enumerate(rows) if row.bit_count() == 5]
        require(len(hubs) == 1, "interface does not have one degree-five hub")
        hub = hubs[0]
        neighbours = [v for v in range(22) if rows[hub] & (1 << v)]
        profile = induced_profile(rows, neighbours)
        require(profile in profiles, f"unrecognized hub-neighbourhood profile {profile}")
        labels.append(profiles[profile])
    return labels


def audit_catalogue_transport(inputs):
    source = inputs["r44_17"]
    record = source["record"]
    require(sha256((record + "\n").encode()).hexdigest() == source["raw_sha256"],
            "order-17 primary-record hash mismatch")
    catalogue = graph6_rows(record)
    permutation = source["catalogue_to_paley"]
    require(len(catalogue) == 17 and sorted(permutation) == list(range(17)),
            "bad Paley transport permutation")
    paley = paley_rows()
    for u in range(17):
        for v in range(u + 1, 17):
            catalogue_edge = bool(catalogue[u] & (1 << v))
            paley_edge = bool(paley[permutation[u]] & (1 << permutation[v]))
            require(catalogue_edge == paley_edge, "displayed Paley transport is not an isomorphism")


def audit_local_survivors(inputs):
    local_type_edges = {
        62: ((0, 2), (0, 3), (0, 4), (1, 2), (1, 3)),
        126: ((0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)),
    }
    results = []
    require(sorted(item["type"] for item in inputs["local_survivors"]) == [62, 126],
            "missing local survivor type")
    for item in inputs["local_survivors"]:
        columns = item["columns"]
        require(len(columns) == 5, "a survivor must have five attachment columns")
        rows = paley_rows() + [0] * 6

        def add_edge(u, v):
            require(u != v, "loop in survivor")
            rows[u] |= 1 << v
            rows[v] |= 1 << u

        for u, v in local_type_edges[item["type"]]:
            add_edge(17 + u, 17 + v)
        for v in range(17, 22):
            add_edge(v, 22)
        for column_index, column in enumerate(columns):
            require(column == sorted(set(column)) and all(0 <= v < 17 for v in column),
                    "malformed survivor column")
            for core_vertex in column:
                add_edge(core_vertex, 17 + column_index)

        require(edge_count(rows) == item["red_edges"], "survivor edge count mismatch")
        require(clique_count(rows, 4) == 0, "local survivor contains a red K4")
        require(clique_count(complement(rows), 5) == 0, "local survivor contains a blue K5")
        results.append({"type": item["type"], "red_edges": edge_count(rows)})
    return results


def main():
    input_path = ROOT / "review_inputs.json"
    input_bytes = input_path.read_bytes()
    require(sha256(input_bytes).hexdigest() == INPUT_SHA256, "review input snapshot hash mismatch")
    inputs = json.loads(input_bytes)

    obstruction = audit_local_obstruction()
    labels = audit_interfaces(inputs)
    audit_catalogue_transport(inputs)
    survivors = audit_local_survivors(inputs)
    excluded = [i for i, label in enumerate(labels) if label == "K1,4"]

    result = {
        "status": "INDEPENDENTLY_VERIFIED_SCOPED_INTERMEDIATE_RESULT",
        "local_obstruction": obstruction,
        "consumer": {
            "interface_types": labels,
            "excluded_degree_23_indices": excluded,
            "retained_degree_23_indices": [i for i in range(13) if i not in excluded],
            "global_hub_upper_bounds": [22 if i in excluded else 23 for i in range(13)],
            "local_degree_23_survivors": survivors,
        },
    }
    expected = {
        "triangle_free_subsets": 7991,
        "maximal_columns": 459,
        "column_size_histogram": {7: 408, 8: 51},
        "compatibility_clique_counts": [1, 459, 13617, 21352, 0],
        "compatible_self_pairs": 0,
        "pair_graph_sha256": "409374628370bd3827317d5c59aff81650643965e529606fa2b622dcae1827b1",
    }
    require(obstruction == expected, "local obstruction differs from the claimed exact result")
    require(excluded == [5], "the star interface is not uniquely index 5")
    require(survivors == [{"type": 62, "red_edges": 112}, {"type": 126, "red_edges": 106}],
            "retained-type witnesses differ from the claim")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
