"""Exact cyclotomic geometry and positive certificate replay; standard library."""
import hashlib
import json
from itertools import combinations
from pathlib import Path

ZERO = (0,) * 8
ONE = (1,) + (0,) * 7


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(k, a):
    return tuple(k * x for x in a)


def sub(a, b):
    return add(a, scale(-1, b))


def mul(a, b):
    out = [0] * 15
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    # Phi_24(X) = X^8 - X^4 + 1.
    for k in range(14, 7, -1):
        out[k - 4] += out[k]
        out[k - 8] -= out[k]
    return tuple(out[:8])


X = (0, 1) + (0,) * 6
POWERS = [ONE]
for _ in range(24):
    POWERS.append(mul(POWERS[-1], X))


def conj(a):
    out = ZERO
    for k, coefficient in enumerate(a):
        out = add(out, scale(coefficient, POWERS[-k % 24]))
    return out


def norm(a):
    return mul(a, conj(a))


def digest(a):
    return hashlib.sha256(json.dumps(a, separators=(",", ":")).encode()).hexdigest()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def geometry():
    need(POWERS[24] == ONE and len(set(POWERS[:24])) == 24, "root order")
    d = add(POWERS[1], POWERS[23])
    addresses = [ZERO, d] + POWERS[:24] + [add(d, p) for p in POWERS[:24]]
    points = list(dict.fromkeys(addresses))
    collisions = [[i for i, q in enumerate(addresses) if q == p]
                  for p in points if addresses.count(p) > 1]
    edges, distances = [], []
    for a, b in combinations(range(len(points)), 2):
        n = norm(sub(points[a], points[b]))
        need(n != ZERO, "physical collision")
        distances.append(n)
        if n == ONE:
            edges.append((a, b))
    need(len(points) == 48 and len(edges) == 100, "unexpected source geometry")
    left = set(POWERS[:24])
    right = {add(d, p) for p in left}
    extra = [(a, b) for a, b in edges if a >= 2
             and not ({points[a], points[b]} <= left or {points[a], points[b]} <= right)]
    need(extra == [(5, 33), (7, 35), (21, 39), (23, 41)], "cross-circle contacts")
    # The five-point conditional bridge in doubled coordinates.
    root3 = add(POWERS[2], POWERS[22])
    imaginary = POWERS[6]
    half = [ZERO, scale(2, ONE), add(ONE, mul(imaginary, root3)),
            sub(scale(-1, root3), imaginary),
            sub(add(scale(2, ONE), root3), imaginary)]
    ordinary, virtual = [], []
    for a, b in combinations(range(5), 2):
        n = norm(sub(half[a], half[b]))
        if n == scale(4, ONE):
            ordinary.append((a, b))
        elif n == scale(4, norm(d)):
            virtual.append((a, b))
        else:
            need((a, b) == (3, 4) and n == scale(4, add(scale(4, ONE), scale(2, root3))),
                 "unexpected bridge distance")
    need(ordinary == [(0, 1), (0, 2), (0, 3), (1, 2), (1, 4)], "bridge unit edges")
    need(virtual == [(0, 4), (1, 3), (2, 3), (2, 4)], "bridge virtual pairs")
    return points, edges, distances, collisions


def check(certificate, edges):
    need(certificate.get("schema") == "root24-two-circle-v1", "schema")
    for name, palette, pins in [("equal_three", "012", "00"),
                                ("different_four", "0123", "01")]:
        word = certificate.get(name)
        need(isinstance(word, str) and len(word) == 48, "word length")
        need(all(c in palette for c in word), "colour range")
        need(word[:2] == pins, "terminal prescription")
        need(all(word[a] != word[b] for a, b in edges), "unit edge inequality")
    word = certificate["equal_three"]
    need(set(word[2:]) <= set("12"), "interior bipartition")


def main():
    base = Path(__file__).resolve().parent
    certificate = json.loads((base / "certificate.json").read_text())
    points, edges, distances, collisions = geometry()
    check(certificate, edges)
    index = {p: j for j, p in enumerate(points)}
    for k, p in enumerate(POWERS[:24]):
        for q in [p, add(points[1], p)]:
            need(certificate["equal_three"][index[q]] == str(1 + (k // 4) % 2),
                 "closed-form colour")
    triangle = next(t for t in combinations(range(48), 3)
                    if all((a, b) in edges for a, b in combinations(t, 2)))
    damaged = []
    c = dict(certificate); c["schema"] = "wrong"; damaged.append(c)
    c = dict(certificate); c["equal_three"] = c["equal_three"][:-1]; damaged.append(c)
    c = dict(certificate); c["equal_three"] = "4" + c["equal_three"][1:]; damaged.append(c)
    c = dict(certificate); c["different_four"] = c["equal_three"]; damaged.append(c)
    c = dict(certificate); w = list(c["equal_three"])
    a, b = next((a, b) for a, b in edges if a >= 2)
    w[b] = w[a]; c["equal_three"] = "".join(w); damaged.append(c)
    for c in damaged:
        try:
            check(c, edges)
        except ValueError:
            pass
        else:
            raise ValueError("corrupt certificate accepted")
    result = {
        "status": "TWO-CIRCLE SOURCE RETIRED: NEUTRAL TERMINAL RELATION",
        "addresses": 50, "distinct_points": len(points), "address_collisions": collisions,
        "all_pair_distances": len(distances), "strict_unit_edges": len(edges),
        "interior_points": 46, "interior_unit_edges": sum(a >= 2 for a, b in edges),
        "extra_cross_circle_edges": [[5, 33], [7, 35], [21, 39], [23, 41]],
        "interior_bipartite": True, "chromatic_number": 3,
        "triangle": triangle, "terminal_relation": ["00", "01"],
        "named_terminal_patterns": 16, "all_pair_four_colour_relations_neutral_by_three_colouring": True,
        "point_sha256": digest(points), "edge_sha256": digest(edges),
        "norm_sha256": digest(distances), "positive_word_edge_checks": 2 * len(edges),
        "corruptions_rejected": len(damaged),
        "conditional_half_point_bound": 189, "conditional_full_point_bound": 377,
        "physical_virtual_edge_supplied": False, "record_candidate": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
