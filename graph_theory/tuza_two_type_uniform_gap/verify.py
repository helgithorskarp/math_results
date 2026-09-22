"""Definition-level witness checks and exact scalar-identity regression.

This is not a graph census and does not prove the universal theorem by
testing. The parameter-uniform argument is in PROOF.md.
"""

from copy import deepcopy
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
from random import Random
import json

from construct import Parameters, arithmetic, digest, make_witness


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_witness(p, witness, full_graph=False):
    """Uses only graph definitions, not the construction's color choices."""
    a, b, c, d, original_s, original_t = p.as_tuple()
    k = a + b + c + d
    s_vertices = set(range(c + a))
    t_vertices = set(range(c)) | set(range(c + a, c + a + b))
    cap_s = min(original_s, max(0, len(s_vertices) - 1))
    cap_t = min(original_t, max(0, len(t_vertices) - 1))
    require(witness["parameters"] == list(p.as_tuple()), "wrong input")
    require(witness["caps"] == [cap_s, cap_t], "wrong caps")

    def is_edge(u, v):
        if type(u) is not int or type(v) is not int or u == v:
            return False
        u, v = min(u, v), max(u, v)
        if not 0 <= u < v < k + cap_s + cap_t:
            return False
        if v < k:
            return True
        if u >= k:
            return False
        return u in (s_vertices if v < k + cap_s else t_vertices)

    occupied = set()
    for triangle in witness["packing"]:
        require(len(triangle) == 3 and len(set(triangle)) == 3, "malformed triangle")
        edges = {tuple(sorted(pair)) for pair in combinations(triangle, 2)}
        require(all(is_edge(*edge) for edge in edges), "nonedge in packing")
        require(not edges & occupied, "packing repeats an edge")
        occupied.update(edges)
    require(witness["centered_size"] == sum(any(v >= k for v in tri)
                                              for tri in witness["packing"]),
            "incorrect centered packing count")

    deleted = set()
    for edge in witness["deleted_clique"]:
        require(len(edge) == 2, "malformed deleted edge")
        u, v = edge
        require(type(u) is int and type(v) is int and 0 <= u < v < k,
                "invalid deleted clique edge")
        require((u, v) not in deleted, "duplicate deleted edge")
        deleted.add((u, v))
    require(len(witness["retained"]) == 2, "wrong number of retained sets")
    kept = []
    for values, neigh, multiplicity in zip(witness["retained"],
                                          (s_vertices, t_vertices),
                                          (original_s, original_t)):
        require(all(type(v) is int for v in values), "noninteger retained vertex")
        subset = set(values)
        require(len(subset) == len(values) and subset <= neigh, "invalid retained set")
        if multiplicity:
            require(all(edge in deleted for edge in combinations(sorted(subset), 2)),
                    "uncovered centered triangle")
        kept.append(subset)
    for triple in combinations(range(k), 3):
        require(any(edge in deleted for edge in combinations(triple, 2)),
                "uncovered clique triangle")
    cost = (len(deleted) + original_s * (len(s_vertices) - len(kept[0]))
            + original_t * (len(t_vertices) - len(kept[1])))
    require(type(witness["cover_size"]) is int and cost == witness["cover_size"],
            "incorrect cover cost")

    if full_graph:
        # Expand the ORIGINAL multiplicities, with a separate vertex numbering,
        # and test all graph triangles against the actual deleted edge set.
        edges = set(combinations(range(k), 2))
        hitting = set(deleted)
        for start, count, neigh, retained in (
                (k, original_s, s_vertices, kept[0]),
                (k + original_s, original_t, t_vertices, kept[1])):
            for center in range(start, start + count):
                edges.update((v, center) for v in neigh)
                hitting.update((v, center) for v in neigh - retained)
        require(len(hitting) == cost, "expanded cover has wrong size")
        for triple in combinations(range(k + original_s + original_t), 3):
            triangle_edges = set(combinations(triple, 2))
            if triangle_edges <= edges:
                require(bool(triangle_edges & hitting), "expanded cover misses triangle")
        expanded_used = set()
        for triangle in witness["packing"]:
            mapped = [v if v < k + cap_s else v + original_s - cap_s for v in triangle]
            tri_edges = {tuple(sorted(pair)) for pair in combinations(mapped, 2)}
            require(tri_edges <= edges and not tri_edges & expanded_used,
                    "packing did not embed in original graph")
            expanded_used.update(tri_edges)
    return cost, len(witness["packing"])


def poly_add(a, b):
    return [((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0))
            for i in range(max(len(a), len(b)))]


def poly_mul(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def check_identities():
    q = [Q(1), Q(-1, 2), Q(-1, 8)]
    require(poly_add(poly_mul(q, q), [Q(-1), Q(1)])
            == [0, 0, 0, Q(1, 8), Q(1, 64)], "square-root majorant identity")
    square = poly_mul([Q(-6, 19), Q(1)], [Q(-6, 19), Q(1)])
    completed = poly_add([Q(19, 24) * z for z in square], [Q(1, 228)])
    require(completed == [Q(1, 12), Q(-1, 2), Q(19, 24)], "positive-gap identity")
    require(Q(17, 24) ** 2 > Q(1, 2), "middle interval comparison")
    gap = lambda k: Q(k * k, 228) - Q(k, 2) - Q(1, 4)
    require(gap(113) == Q(-85, 114) and gap(113) > -1 and gap(112) <= -1,
            "integer cutoff")
    require(3 * 112 - 2 == 334, "kernel vertex bound")


def check_arithmetic(p):
    values = arithmetic(p)
    alpha, r, delta = values["alpha"], values["r"], values["delta"]
    require(0 <= delta <= alpha * alpha <= 1, "delta domain")
    require(0 <= r <= 2 * alpha, "effective multiplicity domain")
    require(delta >= alpha * r - r * r / 4, "overlap inequality")
    require(values["density_gap"] >= Q(1, 228), "uniform density gap")
    require(2 * values["packing_lower"] - values["cover_upper"]
            >= values["uniform_gap"], "finite-order error accounting")
    return values


def main():
    check_identities()
    rng = Random(2026092250)
    small = []
    for _ in range(96):
        k = rng.randrange(3, 9)
        cuts = sorted(rng.randrange(k + 1) for _ in range(3))
        a, b, c, d = cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], k - cuts[2]
        small.append(Parameters(a, b, c, d, rng.randrange(7), rng.randrange(7)))
    # Boundary fixtures include absent types, inactive vertices, identical
    # neighborhoods, nonnested types, and lifting at the cap.
    small += [Parameters(*v) for v in (
        (0, 0, 0, 3, 0, 0), (1, 1, 0, 2, 6, 6),
        (0, 0, 3, 0, 6, 6), (1, 1, 1, 0, 3, 3),
        (2, 2, 1, 0, 0, 4), (1, 2, 2, 1, 5, 1),
        (0, 3, 2, 0, 1, 6), (3, 0, 2, 0, 6, 1),
    )]
    records = []
    for p in small:
        witness = make_witness(p)
        cost, pack = check_witness(p, witness, full_graph=True)
        values = check_arithmetic(p)
        require(witness["centered_size"] >= values["H"] - Q(p.k, 2),
                "centered construction misses averaging bound")
        require(cost <= values["cover_upper"] and pack >= values["packing_lower"],
                "constructed witness misses its bound")
        records.append([list(p.as_tuple()), cost, pack, digest(witness)])

    # These are four named algorithm fixtures, not a cutoff census.
    tail = [Parameters(*v) for v in (
        (0, 0, 0, 113, 0, 0),
        (0, 0, 113, 0, 20, 20),
        (35, 31, 29, 18, 10 ** 9, 17),
        (20, 32, 61, 14, 29, 10 ** 30),
    )]
    tail_summary = []
    for p in tail:
        witness = make_witness(p)
        cost, pack = check_witness(p, witness)
        values = check_arithmetic(p)
        require(witness["centered_size"] >= values["H"] - Q(p.k, 2),
                "tail centered construction misses averaging bound")
        require(cost <= values["cover_upper"] and pack >= values["packing_lower"],
                "tail fixture misses its bound")
        require(cost <= 2 * pack, "tail fixture violates proved comparison")
        tail_summary.append({"parameters": list(p.as_tuple()), "cover": cost, "packing": pack})
        records.append([list(p.as_tuple()), cost, pack, digest(witness)])

    # Binary-sized arithmetic only: no graph with these sizes is expanded.
    for _ in range(128):
        cells = [rng.randrange(10 ** 12) for _ in range(4)]
        m, n = rng.randrange(10 ** 15), rng.randrange(10 ** 15)
        p = Parameters(*cells, m, n)
        values = check_arithmetic(p)
        records.append([list(p.as_tuple()), {key: str(value) for key, value in values.items()}])

    p = Parameters(1, 1, 1, 1, 5, 5)
    good = make_witness(p)
    damaged = []
    w = deepcopy(good)
    w["packing"].append(w["packing"][0])
    damaged.append(w)
    w = deepcopy(good)
    w["packing"][0] = [0, 1, -1]
    damaged.append(w)
    w = deepcopy(good)
    w["retained"][0].append(p.k)
    damaged.append(w)
    w = deepcopy(good)
    w["cover_size"] += 1
    damaged.append(w)
    rejected = 0
    for w in damaged:
        try:
            check_witness(p, w)
        except ValueError:
            rejected += 1
    require(rejected == len(damaged), "malformed certificate was accepted")

    invalid_inputs = [(1, 1, 1, -1, 0, 0), (1, 1, True, 0, 0, 0), (1, 0, 0, 0, 0, 0)]
    input_rejections = 0
    for args in invalid_inputs:
        try:
            Parameters(*args)
        except ValueError:
            input_rejections += 1
    require(input_rejections == 3, "malformed input was accepted")

    summary = {
        "status": "ok",
        "small_full_graph_witness_checks": len(small),
        "tail_witness_fixtures": tail_summary,
        "large_binary_arithmetic_checks": 128,
        "rejected_malformed_witnesses": rejected,
        "rejected_malformed_inputs": input_rejections,
        "cutoff_from_proof": 113,
        "counterexample_vertex_cap": 334,
        "record_sha256": digest(records),
    }
    expected_path = Path(__file__).with_name("EXPECTED.json")
    require(summary == json.loads(expected_path.read_text()), "expected output changed")
    print(json.dumps(summary, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
