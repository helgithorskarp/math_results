"""Definition-level check of the frozen-edge erasure collision; Python 3.11+."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(",", ":")).encode()).hexdigest()


def decode_graph6(word):
    """Strict one-byte-order graph6 decoder, independent of discovery code."""
    require(isinstance(word, str) and len(word) > 1, "invalid graph6 word")
    values = [ord(c) - 63 for c in word]
    require(all(0 <= x <= 63 for x in values), "invalid graph6 alphabet")
    n = values[0]
    require(1 <= n <= 62, "extended graph6 order not supported")
    m = n * (n - 1) // 2
    require(len(values) == 1 + (m + 5) // 6, "invalid graph6 length")
    bits = "".join(format(x, "06b") for x in values[1:])
    require(set(bits[m:]) <= {"0"}, "nonzero graph6 padding")
    adjacency = [[0] * n for _ in range(n)]
    k = 0
    for v in range(1, n):
        for u in range(v):
            adjacency[u][v] = adjacency[v][u] = int(bits[k])
            k += 1
    return adjacency


def audit(adjacency):
    """Inspect every five-set, not common-neighborhood triangle searches."""
    n = len(adjacency)
    frozen = set()
    witness = {}
    five_sets = 0
    near_cliques = [0, 0]
    for vertices in combinations(range(n), 5):
        pairs = list(combinations(vertices, 2))
        colors = [adjacency[u][v] for u, v in pairs]
        total = sum(colors)
        require(total not in (0, 10), "monochromatic five-set: " + str(vertices))
        five_sets += 1
        if total in (1, 9):
            minority = int(total == 1)
            edge = pairs[colors.index(minority)]
            frozen.add(edge)
            witness.setdefault(edge, list(vertices))
            near_cliques[1 - minority] += 1
    free = [[u, v, adjacency[u][v]]
            for u, v in combinations(range(n), 2) if (u, v) not in frozen]
    triangles = [0, 0]
    for u, v, w in combinations(range(n), 3):
        if adjacency[u][v] == adjacency[u][w] == adjacency[v][w]:
            triangles[adjacency[u][v]] += 1
    return {
        "vertices": n,
        "edges": sum(map(sum, adjacency)) // 2,
        "degrees": list(map(sum, adjacency)),
        "checked_five_sets": five_sets,
        "monochromatic_five_sets": 0,
        "frozen_count": len(frozen),
        "free_edges": free,
        "frozen_pairs_sha256": digest(sorted(frozen)),
        "first_witnesses_sha256": digest([[*e, witness[e]] for e in sorted(witness)]),
        "blue_red_triangles": triangles,
        "blue_red_near_cliques": near_cliques,
    }


def verify(fixture):
    a = decode_graph6(fixture["first_graph6"])
    original_b = decode_graph6(fixture["second_graph6"])
    require(len(a) == len(original_b) == 42, "wrong order")
    permutation = fixture["second_to_first_permutation"]
    require(sorted(permutation) == list(range(42)), "not a vertex permutation")
    b = [[0] * 42 for _ in range(42)]
    for u, v in combinations(range(42), 2):
        i, j = permutation[u], permutation[v]
        b[i][j] = b[j][i] = original_b[u][v]
    x, y = audit(a), audit(b)
    require(x["free_edges"] == y["free_edges"] == fixture["nonfrozen_edges_in_first_labels"],
            "erasure records differ")
    require(x["degrees"] == y["degrees"] == fixture["common_degree_vector"],
            "degree vectors differ")
    require(x["frozen_pairs_sha256"] == y["frozen_pairs_sha256"], "frozen masks differ")
    require(x["edges"] == y["edges"], "edge counts differ")
    require(x["blue_red_triangles"] != y["blue_red_triangles"],
            "triangle counts do not certify nonisomorphism")
    require(x["edges"] + y["edges"] != 861, "color-complement ambiguity not excluded")
    changed = [(u, v) for u, v in combinations(range(42), 2) if a[u][v] != b[u][v]]
    require(changed, "graphs are identical")
    return {
        "status": "VERIFIED_NONINJECTIVE_FROZEN_ERASURE_WITH_DEGREES",
        "scope": "two explicit good42 graphs; no assertion about good43 existence",
        "first": x,
        "second_in_first_labels": y,
        "changed_pairs": len(changed),
        "changed_pairs_sha256": digest(changed),
        "same_full_degree_vector": True,
        "same_ternary_erasure": True,
        "nonisomorphic_by_triangle_counts": True,
    }


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    fixture = json.loads((root / "COUNTEREXAMPLE.json").read_text())
    print(json.dumps(verify(fixture), sort_keys=True, indent=2))
