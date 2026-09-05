#!/usr/bin/env python3
"""Independent list-colouring audit for the dense506 completion closure.

The earlier reviewer certificate establishes the complete candidate table.
This checker imports no submitted module.  It binds that table entrywise,
reconstructs host-available lists, runs synchronous fixed-point propagation,
proves the residue is a forest, constructs a colouring by reverse leaf order,
and directly checks both its colouring and the submitted colouring.
"""

from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from json import dump, dumps, load
from pathlib import Path


PINS = {
    "points": "3bcfcab7e411f6adff3426ceb1cfff97718d634fe41a0e7a71982a57995c4c45",
    "positive_triples": "7f03bc7c1c61fc5d3ea5a0c0d8b512dd58c3bcdbd753716068e5bd83ab7ca2a2",
    "neighbors": "7c71b32a5807e4e9baab0c17953c9e2ba688e7e0d290caa9be6e23b752f564af",
    "candidate_edges": "7912eb1140ca9a570128233517073becd52380fe3840f7cc126bc85a7493f27e",
    "available_masks": "3521c2b5b0fa8942608728d88416688ca8b5a1d207aad59d2fd79d41be27bdb6",
}
HOST_COLOUR_SHA = "010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4"
FULL_COLOUR_SHA = "1851be3b084aba56c0ec2910bdd4769b706d36c4ce8756b38d0c6726ca973a0b"
EXPECTED_RESIDUAL_EDGES = [
    [941, 1190], [949, 967], [1072, 1144], [1130, 1171],
    [1130, 1183], [1162, 1183], [1163, 1192],
]


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def digest(value):
    return sha256(dumps(value, separators=(",", ":")).encode()).hexdigest()


def read_colours(path, count, expected_sha):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == expected_sha, ("colour hash", path))
    require(len(raw) == count + 1 and raw[-1:] == b"\n", ("colour length", path))
    require(set(raw[:-1]) <= set(b"0123"), ("colour alphabet", path))
    return [item - ord("0") for item in raw[:-1]]


def validate_table(table):
    require(set(table) == set(PINS), "candidate table fields")
    for name, expected in PINS.items():
        require(digest(table[name]) == expected, ("candidate table digest", name))
    n = len(table["points"])
    require(n == 1420, "candidate count")
    require(all(isinstance(row, list) and len(row) == 9 for row in table["points"]),
            "point row width")
    require(len(table["neighbors"]) == len(table["available_masks"]) == n,
            "candidate row counts")
    for row in table["neighbors"]:
        require(row == sorted(set(row)) and len(row) >= 3 and
                all(type(v) is int and 0 <= v < 506 for v in row),
                ("host-neighbour row", row))
    edges = table["candidate_edges"]
    require(edges == sorted(edges) and len(edges) == len({tuple(edge) for edge in edges}),
            "candidate edge order or duplicates")
    require(all(type(i) is int and type(j) is int and 0 <= i < j < n for i, j in edges),
            "candidate edge range")


def available_lists(neighbors, host_colours):
    masks = []
    for row in neighbors:
        used = {host_colours[v] for v in row}
        masks.append(sum(1 << colour for colour in range(4) if colour not in used))
    require(all(masks), "empty initial list")
    return masks


def adjacency(n, edges):
    result = [set() for _ in range(n)]
    for i, j in edges:
        result[i].add(j)
        result[j].add(i)
    return result


def propagate(initial, graph):
    """Apply all singleton implications synchronously to the fixed point."""
    lists = [{colour for colour in range(4) if mask >> colour & 1}
             for mask in initial]
    rounds = []
    while True:
        before = [set(row) for row in lists]
        for i, row in enumerate(before):
            if len(row) == 1:
                for j in graph[i]:
                    lists[j] -= row
        require(all(lists), "singleton propagation contradiction")
        changed = sum(a != b for a, b in zip(before, lists))
        if not changed:
            break
        rounds.append({"changed_lists": changed,
                       "singletons": sum(len(row) == 1 for row in lists)})
    return lists, rounds


def forest_order(residual, graph):
    """Repeatedly remove one leaf; failure means the residue has a cycle."""
    remaining = set(residual)
    order = []
    while remaining:
        leaves = [v for v in sorted(remaining) if len(graph[v] & remaining) <= 1]
        require(leaves, "residual contains a cycle")
        vertex = leaves[0]
        remaining.remove(vertex)
        order.append(vertex)
    return order


def components(residual, graph):
    remaining = set(residual)
    result = []
    while remaining:
        root = min(remaining)
        stack = [root]
        component = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend((graph[vertex] & residual) - component)
        remaining -= component
        result.append(sorted(component))
    return result


def alternate_colouring(lists, graph, order):
    colours = [-1] * len(lists)
    for vertex, row in enumerate(lists):
        if len(row) == 1:
            colours[vertex] = next(iter(row))
    for vertex in reversed(order):
        forbidden = {colours[other] for other in graph[vertex] if colours[other] >= 0}
        choices = sorted(lists[vertex] - forbidden)
        require(choices, ("no reverse-leaf colour", vertex))
        colours[vertex] = choices[0]
    require(all(colour >= 0 for colour in colours), "uncoloured candidate")
    return colours


def check_candidate_colouring(colours, masks, edges):
    require(len(colours) == len(masks), "candidate colour length")
    require(all(type(colour) is int and 0 <= colour < 4 and mask >> colour & 1
                for colour, mask in zip(colours, masks)), "colour outside host list")
    require(all(colours[i] != colours[j] for i, j in edges),
            "monochromatic candidate edge")


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path,
                        default=Path(__file__).resolve().parents[1])
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo.resolve()
    with args.candidates.open() as stream:
        table = load(stream)
    validate_table(table)
    host = read_colours(root / "hadwiger_nelson_dense506_two_point_extension/host_colors.txt",
                        506, HOST_COLOUR_SHA)
    published = read_colours(root / "hadwiger_nelson_dense506_completion_closure/colors.txt",
                             1926, FULL_COLOUR_SHA)
    require(published[:506] == host, "host colouring not preserved")

    masks = available_lists(table["neighbors"], host)
    require(masks == table["available_masks"], "available-list table mismatch")
    graph = adjacency(1420, table["candidate_edges"])
    lists, rounds = propagate(masks, graph)
    residual = {i for i, row in enumerate(lists) if len(row) > 1}
    residual_edges = [[i, j] for i, j in table["candidate_edges"]
                      if i in residual and j in residual]
    require(residual_edges == EXPECTED_RESIDUAL_EDGES, "residual edge list")
    order = forest_order(residual, graph)
    pieces = components(residual, graph)
    require(len(order) == len(residual) == 53, "residual order")
    require(Counter(map(len, pieces)) == {1: 41, 2: 4, 4: 1},
            "residual component orders")

    alternate = alternate_colouring(lists, graph, order)
    check_candidate_colouring(alternate, masks, table["candidate_edges"])
    check_candidate_colouring(published[506:], masks, table["candidate_edges"])
    alternate_full = host + alternate
    alternate_raw = ("".join(map(str, alternate_full)) + "\n").encode()
    host_candidate_edges = sum(map(len, table["neighbors"]))
    full_edges = 2389 + host_candidate_edges + len(table["candidate_edges"])
    require(host_candidate_edges == 5710 and full_edges == 12074, "edge totals")
    report = {
        "status": "accepted at complete first triple-neighbour support scope",
        "imported_complete_candidate_census": True,
        "candidate_table_digests": PINS,
        "host_vertices": 506,
        "candidate_vertices": 1420,
        "full_vertices": 1926,
        "host_edges_imported": 2389,
        "host_candidate_edges": host_candidate_edges,
        "candidate_edges": len(table["candidate_edges"]),
        "full_edges": full_edges,
        "initial_list_histogram": dict(sorted(Counter(mask.bit_count() for mask in masks).items())),
        "synchronous_propagation_rounds": rounds,
        "final_list_histogram": dict(sorted(Counter(map(len, lists)).items())),
        "residual_vertices": len(residual),
        "residual_edges": residual_edges,
        "residual_component_order_histogram": dict(sorted(Counter(map(len, pieces)).items())),
        "reverse_leaf_order_verified": True,
        "published_colour_sha256": FULL_COLOUR_SHA,
        "published_colour_class_sizes": dict(sorted(Counter(published).items())),
        "published_colouring_verified": True,
        "alternate_colour_sha256": sha256(alternate_raw).hexdigest(),
        "alternate_colour_class_sizes": dict(sorted(Counter(alternate_full).items())),
        "alternate_colouring_verified": True,
    }
    with args.report.open("w") as stream:
        dump(report, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(args.report)


if __name__ == "__main__":
    main()
