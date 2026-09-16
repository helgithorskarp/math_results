#!/usr/bin/env python3
"""Independent structural and positive-colouring review of the HN508 cohort.

This checker imports no target Python module.  It reconstructs the sixteen
supports using integer adjacency bitsets and a full eligible-vertex scan,
then checks both the target words and one reviewer-supplied word on their
952-vertex union.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_haugland508_nonlocal_cohort"
PARENT = ROOT / "hadwiger_nelson_haugland2131_exact_reproduction"

N = 2131
PINS = frozenset((0, 303, 435, 1368, 1500))
GRAPH_SHA256 = "201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d"
TARGET_CERT_SHA256 = "431a71049ad2cf95461857f873d9ec561f92207b2677b9f1df3bafec8437f046"
PARENT_CERT_SHA256 = "a00adc01f218922819318ef2ce982fa795b843e91a95c94cb9f36bea6a6c9111"
PARENT_EDGE_SHA256 = "980bdb02e133be0e4257bab1a204f2942f554e59822136fab632f45494a6c113"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_hashed(path: Path, digest: str):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == digest, f"hash mismatch: {path.name}")
    return json.loads(raw)


def digest_labels(labels: list[int]) -> str:
    return sha256("".join(f"{v}\n" for v in labels).encode()).hexdigest()


def digest_edges(edges: list[tuple[int, int]]) -> str:
    return sha256("".join(f"{u} {v}\n" for u, v in edges).encode()).hexdigest()


def iter_bits(bits: int):
    while bits:
        bit = bits & -bits
        yield bit.bit_length() - 1
        bits ^= bit


def load_parent():
    payload = read_hashed(PARENT / "graph.json", GRAPH_SHA256)
    edges = [tuple(edge) for edge in payload["G3_edges"]]
    require(len(edges) == 12530, "parent edge count")
    require(edges == sorted(set(edges)), "parent edge canonicality")
    require(digest_edges(edges) == PARENT_EDGE_SHA256, "parent edge digest")
    adjacency = [0] * N
    for u, v in edges:
        require(0 <= u < v < N, "parent edge range")
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return edges, adjacency


@lru_cache(maxsize=8)
def tie_keys(seed: int):
    return tuple(
        sha256(f"HN2131-nonlocal-cap508-v1:{seed}:{v}".encode("ascii")).digest()
        for v in range(N)
    )


def frozen_support(seed: int, orientation: int, adjacency: list[int]) -> list[int]:
    """Rebuild one support by full scans over an integer live-set bitmask."""
    require(seed in range(8) and orientation in (0, 1), "cohort parameter")
    quotas = (254, 253) if orientation == 0 else (253, 254)
    counts = [1065, 1065]
    keys = tie_keys(seed)
    live = (1 << N) - 1
    live_count = N
    left = tuple(v for v in range(1, 1066) if v not in PINS)
    right = tuple(v for v in range(1066, N) if v not in PINS)
    while live_count > 508:
        best = None
        if counts[0] > quotas[0]:
            for v in left:
                if live >> v & 1:
                    item = ((adjacency[v] & live).bit_count(), keys[v], v)
                    if best is None or item < best:
                        best = item
        if counts[1] > quotas[1]:
            for v in right:
                if live >> v & 1:
                    item = ((adjacency[v] & live).bit_count(), keys[v], v)
                    if best is None or item < best:
                        best = item
        require(best is not None, "eligible deletion exists")
        v = best[2]
        live ^= 1 << v
        counts[int(v >= 1066)] -= 1
        live_count -= 1
    result = list(iter_bits(live))
    require(tuple(counts) == quotas, "half quotas")
    require(PINS <= set(result), "pinned vertices")
    return result


def induced(labels: list[int], edges: list[tuple[int, int]]):
    selected = set(labels)
    return [(u, v) for u, v in edges if u in selected and v in selected]


def check_word(labels: list[int], edges: list[tuple[int, int]], word: str, colours: int):
    require(type(word) is str and len(word) == len(labels), "colour-word length")
    require(set(word) <= set(map(str, range(colours))), "colour-word alphabet")
    values = dict(zip(labels, map(int, word)))
    require(all(values[u] != values[v] for u, v in edges), "monochromatic edge")
    return values


def connected(labels: list[int], adjacency: list[int]) -> bool:
    allowed = sum(1 << v for v in labels)
    reached = 0
    frontier = 1 << labels[0]
    while frontier:
        reached |= frontier
        neighbours = 0
        for v in iter_bits(frontier):
            neighbours |= adjacency[v]
        frontier = neighbours & allowed & ~reached
    return reached == allowed


def max_capped_ball(adjacency: list[int]) -> int:
    maximum = 0
    for root in range(N):
        seen = 1 << root
        layer = seen
        last = 1
        while layer:
            neighbours = 0
            for v in iter_bits(layer):
                neighbours |= adjacency[v]
            layer = neighbours & ~seen
            seen |= layer
            order = seen.bit_count()
            if order > 508:
                break
            last = order
        maximum = max(maximum, last)
    return maximum


def verify(review_certificate: dict) -> dict:
    require(review_certificate["version"] == 1, "review certificate version")
    require(
        review_certificate["target_commit"] == "49b81225ca13eb0c4c4e184c25e61499da65dd2c",
        "target commit",
    )
    target = read_hashed(TARGET / "certificate.json", TARGET_CERT_SHA256)
    parent_cert = read_hashed(PARENT / "certificate.json", PARENT_CERT_SHA256)
    require(target["version"] == 1, "target certificate version")
    records = target["records"]
    require(
        [(r["seed"], r["orientation"]) for r in records]
        == [(seed, orientation) for seed in range(8) for orientation in (0, 1)],
        "frozen cohort index",
    )
    edges, adjacency = load_parent()

    parent_word = "".join(map(str, parent_cert["five_colouring"]))
    check_word(list(range(N)), edges, parent_word, 5)

    supports = []
    support_edges = []
    sizes = []
    minimum_degrees = []
    support_hash_stream = sha256()
    target_word_stream = sha256()
    for row in records:
        labels = frozen_support(row["seed"], row["orientation"], adjacency)
        actual_edges = induced(labels, edges)
        require(len(labels) == row["order"] == 508, "support order")
        require(digest_labels(labels) == row["vertex_sha256"], "support digest")
        require(len(actual_edges) == row["size"], "support edge count")
        require(digest_edges(actual_edges) == row["edge_sha256"], "support edge digest")
        require(connected(labels, adjacency), "support connectedness")
        require((303, 1368) in actual_edges and (435, 1500) in actual_edges, "cross edges")
        check_word(labels, actual_edges, row["four_word"], 4)
        check_word(labels, actual_edges, "".join(parent_word[v] for v in labels), 5)
        selected = sum(1 << v for v in labels)
        minimum_degrees.append(min((adjacency[v] & selected).bit_count() for v in labels))
        support_hash_stream.update((row["vertex_sha256"] + "\n").encode())
        target_word_stream.update((row["four_word"] + "\n").encode())
        supports.append(labels)
        support_edges.append(actual_edges)
        sizes.append(len(actual_edges))
    require(len({tuple(labels) for labels in supports}) == 16, "distinct labelled supports")

    union_labels = sorted(set().union(*map(set, supports)))
    union_edges = induced(union_labels, edges)
    require(len(union_labels) == review_certificate["union_vertices"] == 952, "union order")
    require(len(union_edges) == review_certificate["union_unit_edges"] == 4773, "union size")
    require(
        digest_edges(union_edges) == review_certificate["union_global_edge_sha256"],
        "union edge digest",
    )
    union_word = review_certificate["union_four_word"]
    union_colours = check_word(union_labels, union_edges, union_word, 4)
    union_selected = sum(1 << v for v in union_labels)
    require(connected(union_labels, adjacency), "union connectedness")
    for labels, actual_edges in zip(supports, support_edges):
        check_word(labels, actual_edges, "".join(str(union_colours[v]) for v in labels), 4)

    intersections = [len(set(a) & set(b)) for a, b in combinations(supports, 2)]
    common = set(supports[0]).intersection(*map(set, supports[1:]))
    # The two 1066-point halves share label 0.  "Cross-half" therefore means
    # an edge between their disjoint private parts, not an edge incident to 0.
    cross_edges = [(u, v) for u, v in edges if 0 < u < 1066 <= v]
    common_to_right = [(u, v) for u, v in edges if u == 0 and v >= 1066]
    capped_ball = max_capped_ball(adjacency)
    require(capped_ball == 507, "maximum metric ball of order at most 508")
    require(cross_edges == [(303, 1368), (435, 1500)], "parent cross-half edge census")

    return {
        "status": "ACCEPT_AND_STRENGTHEN_UNION_FOUR_COLOURABLE",
        "target_cases": 16,
        "target_vertices_each": 508,
        "target_edge_counts": sizes,
        "target_minimum_degrees": minimum_degrees,
        "target_words_checked": True,
        "target_support_hash_stream_sha256": support_hash_stream.hexdigest(),
        "target_word_stream_sha256": target_word_stream.hexdigest(),
        "all_supports_connected": True,
        "all_supports_retain_both_parent_cross_edges": True,
        "parent_cross_half_edges": [list(edge) for edge in cross_edges],
        "shared_vertex_to_right_edges": len(common_to_right),
        "parent_five_word_checked": True,
        "union_vertices": len(union_labels),
        "union_unit_edges": len(union_edges),
        "union_global_edge_sha256": digest_edges(union_edges),
        "union_four_word_sha256": sha256(union_word.encode()).hexdigest(),
        "union_four_word_checked": True,
        "union_colour_class_sizes": [union_word.count(str(c)) for c in range(4)],
        "union_connected": True,
        "union_minimum_degree": min(
            (adjacency[v] & union_selected).bit_count() for v in union_labels
        ),
        "union_word_restricts_properly_to_all_supports": True,
        "pairwise_support_intersection_min": min(intersections),
        "pairwise_support_intersection_max": max(intersections),
        "all_support_intersection": len(common),
        "maximum_parent_metric_ball_order_through_508": capped_ball,
        "exact_chromatic_number_claimed": False,
        "record_candidate": False,
    }


def main() -> None:
    cert = json.loads((HERE / "certificate.json").read_text())
    print(json.dumps(verify(cert), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
