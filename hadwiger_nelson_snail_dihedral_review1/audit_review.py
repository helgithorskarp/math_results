#!/usr/bin/env python3
"""Independent audit of the complete Snail D9 classification.

This checker imports no target code.  It uses a fresh finite-field
specialization for the upper colour certificates, direct monomial reduction
for exact Q(a,b,c,e) arithmetic, and a bitset DSATUR search for the lower
three-colour obstructions.
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


P = 1_000_010_251
ROOTS = (863_024_046, 726_668_820, 504_977_047, 548_931_751)
D = 768
ZERO = (0,) * 16
ONE = (1,) + (0,) * 15
A = (0, 1) + (0,) * 14
B = (0, 0, 1) + (0,) * 13
C = (0, 0, 0, 0, 1) + (0,) * 11
E = (0,) * 8 + (1,) + (0,) * 7
EXPECTED_CERTIFICATE_SHA256 = (
    "c217efc0649faf986475dac157e7f2ac4bb992e4f4ac88a108e3217808d20dc3"
)
EXPECTED_SEED_SHA256 = (
    "9d03aaf2233e7b96109484a1fe3c8d311025bb95186b6927d517d716e774f614"
)
EXPECTED_CENSUS_SHA256 = (
    "cafc136a70b10e3b4b97537cdd319eb573e16307a2396a6730ee032da98728b5"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def add(x: tuple[int, ...], y: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(x, y))


def sub(x: tuple[int, ...], y: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a - b for a, b in zip(x, y))


def scale(n: int, x: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(n * a for a in x)


def base_monomial_product(i: int, j: int) -> tuple[int, int]:
    """Multiply a^i0 b^i1 c^i2 and a^j0 b^j1 c^j2."""
    common = i & j
    coefficient = 1
    if common & 1:
        coefficient *= -3
    if common & 2:
        coefficient *= -11
    if common & 4:
        coefficient *= 5
    return coefficient, i ^ j


def monomial_product(i: int, j: int) -> tuple[tuple[int, int], ...]:
    """Directly reduce one product using e^2=-3320+632ab."""
    coefficient, mask = base_monomial_product(i & 7, j & 7)
    if not (i & 8 and j & 8):
        return ((mask | ((i ^ j) & 8), coefficient),)
    extra_coefficient, extra_mask = base_monomial_product(mask, 3)
    return (
        (mask, -3320 * coefficient),
        (extra_mask, 632 * coefficient * extra_coefficient),
    )


PRODUCTS = tuple(
    tuple(monomial_product(i, j) for j in range(16)) for i in range(16)
)


def mul(x: tuple[int, ...], y: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * 16
    for i, xi in enumerate(x):
        if not xi:
            continue
        for j, yj in enumerate(y):
            if not yj:
                continue
            for mask, coefficient in PRODUCTS[i][j]:
                out[mask] += xi * yj * coefficient
    return tuple(out)


def bar(x: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        -coefficient if ((mask & 1) + ((mask >> 1) & 1) + ((mask >> 3) & 1)) & 1
        else coefficient
        for mask, coefficient in enumerate(x)
    )


def norm(x: tuple[int, ...]) -> tuple[int, ...]:
    return mul(x, bar(x))


def linear(*terms: tuple[int, tuple[int, ...]]) -> tuple[int, ...]:
    out = ZERO
    for coefficient, value in terms:
        out = add(out, scale(coefficient, value))
    return out


def exact_seed(rows: list[list[int]]) -> list[tuple[int, ...]]:
    """Return 768 times the 29 source coordinates in the a,b,c,e basis."""
    w2 = add(ONE, A)
    v6 = add(scale(5, ONE), B)
    wv12 = mul(w2, v6)
    p = add(
        linear((2304, ONE), (816, w2), (-112, v6), (128, wv12)),
        mul(C, linear((-192, ONE), (48, w2), (-16, v6), (16, wv12))),
    )
    q = add(
        linear((2112, ONE), (624, w2), (-16, v6), (128, wv12)),
        mul(E, linear((-6, w2), (2, v6), (1, wv12))),
    )
    result = [p, q]
    result.extend(
        linear((768 * x, ONE), (384 * y, w2), (128 * z, v6), (64 * t, wv12))
        for x, y, z, t in rows
    )
    require(len(result) == len(set(result)) == 29, "exact seed shape")
    return result


def exact_addresses(
    seed: list[tuple[int, ...]], centre: int, axis: int
) -> tuple[list[tuple[int, ...]], tuple[int, ...], tuple[int, ...]]:
    delta = sub(seed[axis], seed[centre])
    n = norm(delta)
    require(delta != ZERO and n != ZERO, "exact axis")
    relative = [sub(point, seed[centre]) for point in seed]
    direct = [mul(n, point) for point in relative]
    delta_squared = mul(delta, delta)
    reflected = [mul(delta_squared, bar(point)) for point in relative]
    rotations_twice = (scale(2, ONE), sub(A, ONE), scale(-1, add(ONE, A)))
    formal = [
        mul(turn, point)
        for turn in rotations_twice
        for cloud in (direct, reflected)
        for point in cloud
    ]
    target = scale(4 * D * D, mul(n, n))
    return formal, target, n


def is_prime_by_trial_division(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def evaluate(x: tuple[int, ...]) -> int:
    powers = [1] * 16
    for mask in range(16):
        for bit, root in enumerate(ROOTS):
            if mask & (1 << bit):
                powers[mask] = powers[mask] * root % P
    return sum(coefficient * powers[mask] for mask, coefficient in enumerate(x)) % P


RESIDUE_BASIS = tuple(evaluate(tuple(int(i == j) for i in range(16))) for j in range(16))


def residue(x: tuple[int, ...]) -> int:
    return sum(coefficient * image for coefficient, image in zip(x, RESIDUE_BASIS)) % P


def modular_seed(rows: list[list[int]]) -> tuple[list[int], list[int]]:
    inv = lambda n: pow(n, -1, P)

    def values(roots: tuple[int, int, int, int]) -> list[int]:
        a, b, c, e = roots
        w = (1 + a) * inv(2) % P
        v = (5 + b) * inv(6) % P
        p = (
            3 + 17 * inv(8) * w - 7 * inv(8) * v + 2 * w * v
            + c * (-inv(4) + inv(8) * w - inv(8) * v + inv(4) * w * v)
        ) % P
        q = (
            11 * inv(4) + 13 * inv(8) * w - inv(8) * v + 2 * w * v
            + e * inv(64) * (-w + v + w * v)
        ) % P
        return [p, q] + [(x + y * w + z * v + t * w * v) % P for x, y, z, t in rows]

    a, b, c, e = ROOTS
    return values(ROOTS), values((-a % P, -b % P, c, -e % P))


def modular_addresses(
    seed: list[int], barred_seed: list[int], centre: int, axis: int
) -> tuple[list[int], list[int]]:
    delta = (seed[axis] - seed[centre]) % P
    barred_delta = (barred_seed[axis] - barred_seed[centre]) % P
    require(delta and barred_delta, "modular axis denominator")
    u = delta * pow(barred_delta, -1, P) % P
    barred_u = barred_delta * pow(delta, -1, P) % P
    a = ROOTS[0]
    turn = (a - 1) * pow(2, -1, P) % P
    barred_turn = (-a - 1) * pow(2, -1, P) % P
    require(turn * barred_turn % P == 1 and pow(turn, 3, P) == 1 and turn != 1,
            "modular third root")
    values: list[int] = []
    barred_values: list[int] = []
    for k in range(3):
        t, bt = pow(turn, k, P), pow(barred_turn, k, P)
        for reflected in range(2):
            for x, bx in zip(seed, barred_seed):
                relative = (x - seed[centre]) % P
                barred_relative = (bx - barred_seed[centre]) % P
                if reflected:
                    values.append(t * u * barred_relative % P)
                    barred_values.append(bt * barred_u * relative % P)
                else:
                    values.append(t * relative % P)
                    barred_values.append(bt * barred_relative % P)
    require(len(values) == len(barred_values) == 174, "formal address count")
    return values, barred_values


def unpack(word: object, length: int) -> list[int]:
    require(type(word) is str, "packed word type")
    data = base64.b64decode(word, validate=True)
    require(len(data) == (length + 3) // 4, "packed word length")
    require(base64.b64encode(data).decode() == word, "canonical base64")
    result = [(data[i // 4] >> (2 * (i % 4))) & 3 for i in range(length)]
    if length % 4:
        require(data[-1] >> (2 * (length % 4)) == 0, "nonzero padding")
    return result


def check_upper(values: list[int], barred: list[int], colours: list[int]) -> int:
    comparisons = 0
    for colour in range(4):
        addresses = [i for i, value in enumerate(colours) if value == colour]
        for i, j in combinations(addresses, 2):
            require(
                (values[i] - values[j]) * (barred[i] - barred[j]) % P != 1,
                "same-colour modular unit",
            )
            comparisons += 1
    return comparisons


def three_colourable_bitset(n: int, edges: list[tuple[int, int]]) -> tuple[bool, int]:
    """Independent bitset DSATUR decision procedure, with colour symmetry fixed."""
    adjacency = [0] * n
    for x, y in edges:
        require(type(x) is int and type(y) is int and 0 <= x < y < n, "edge shape")
        adjacency[x] |= 1 << y
        adjacency[y] |= 1 << x
    colours = [-1] * n
    triangle = None
    for x in range(n):
        neighbours = adjacency[x]
        while neighbours:
            ybit = neighbours & -neighbours
            y = ybit.bit_length() - 1
            common = adjacency[x] & adjacency[y]
            if common:
                triangle = (x, y, (common & -common).bit_length() - 1)
                break
            neighbours ^= ybit
        if triangle is not None:
            break
    assigned = 0
    if triangle is not None:
        for colour, vertex in enumerate(triangle):
            colours[vertex] = colour
            assigned |= 1 << vertex
    elif n:
        colours[0] = 0
        assigned = 1
    nodes = 0
    full = (1 << n) - 1

    def search(used_vertices: int) -> bool:
        nonlocal nodes
        nodes += 1
        if used_vertices == full:
            return True
        best_vertex = -1
        best_key = None
        best_available = 0
        for vertex in range(n):
            if used_vertices >> vertex & 1:
                continue
            used_colours = 0
            neighbours = adjacency[vertex] & used_vertices
            while neighbours:
                bit = neighbours & -neighbours
                neighbour = bit.bit_length() - 1
                used_colours |= 1 << colours[neighbour]
                neighbours ^= bit
            available = 7 & ~used_colours
            if not available:
                return False
            # Deliberately break DSATUR ties in the opposite vertex order from
            # the target checker, so the lower search tree is independently
            # traversed rather than replayed node-for-node.
            key = (used_colours.bit_count(), adjacency[vertex].bit_count(), vertex)
            if best_key is None or key > best_key:
                best_key = key
                best_vertex = vertex
                best_available = available
        choice = best_available
        while choice:
            colour_bit = 1 << (choice.bit_length() - 1)
            colours[best_vertex] = colour_bit.bit_length() - 1
            if search(used_vertices | (1 << best_vertex)):
                return True
            choice ^= colour_bit
        colours[best_vertex] = -1
        return False

    return search(assigned), nodes


def chromatic_count_three(n: int, edges: list[tuple[int, int]]) -> int:
    """Evaluate the chromatic polynomial at 3 by inclusion--exclusion."""
    total = 0
    for mask in range(1 << len(edges)):
        parent = list(range(n))

        def find(vertex: int) -> int:
            while parent[vertex] != vertex:
                parent[vertex] = parent[parent[vertex]]
                vertex = parent[vertex]
            return vertex

        for edge_index, (x, y) in enumerate(edges):
            if mask >> edge_index & 1:
                xroot, yroot = find(x), find(y)
                if xroot != yroot:
                    parent[xroot] = yroot
        components = len({find(vertex) for vertex in range(n)})
        total += (-1 if mask.bit_count() & 1 else 1) * 3**components
    return total


def internal_controls() -> tuple[int, int, int]:
    """Check the two reviewer-owned proof engines on exhaustive small inputs."""
    graphs = 0
    for n in range(6):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            edges = [edge for index, edge in enumerate(possible) if mask >> index & 1]
            colourable, _ = three_colourable_bitset(n, edges)
            require(colourable == (chromatic_count_three(n, edges) > 0),
                    "reviewer small-graph control")
            graphs += 1

    basis = [tuple(int(i == j) for i in range(16)) for j in range(16)]
    products = 0
    for i in range(16):
        for j in range(16):
            product = mul(basis[i], basis[j])
            require(product == mul(basis[j], basis[i]), "reviewer commutativity")
            require(residue(product) == residue(basis[i]) * residue(basis[j]) % P,
                    "reviewer residue homomorphism")
            products += 1
    associativity = 0
    for i in range(16):
        for j in range(16):
            left_pair = mul(basis[i], basis[j])
            for k in range(16):
                require(mul(left_pair, basis[k]) == mul(basis[i], mul(basis[j], basis[k])),
                        "reviewer associativity")
                associativity += 1
    return graphs, products, associativity


def audit(target: Path) -> dict[str, object]:
    seed_bytes = (target / "seed.json").read_bytes()
    certificate_bytes = (target / "certificate.json").read_bytes()
    require(sha256(seed_bytes).hexdigest() == EXPECTED_SEED_SHA256, "seed digest")
    require(
        sha256(certificate_bytes).hexdigest() == EXPECTED_CERTIFICATE_SHA256,
        "certificate digest",
    )
    seed_data = json.loads(seed_bytes)
    rows = seed_data["moser_rows"]
    require(
        len(rows) == 27
        and all(type(row) is list and len(row) == 4 for row in rows)
        and all(type(value) is int for row in rows for value in row),
        "seed rows",
    )
    certificate = json.loads(certificate_bytes)
    require(certificate.get("version") == 2 and type(certificate.get("version")) is int,
            "certificate version")
    require(certificate.get("complete") is True, "certificate completeness")
    cases = certificate.get("cases")
    expected_cases = [(c, a) for c in range(29) for a in range(29) if c != a]
    require(type(cases) is list and len(cases) == len(expected_cases) == 812,
            "case count")

    require(is_prime_by_trial_division(P), "reviewer modulus is not prime")
    a, b, c, e = ROOTS
    require(
        (a * a + 3) % P == 0
        and (b * b + 11) % P == 0
        and (c * c - 5) % P == 0
        and (e * e + 3320 - 632 * a * b) % P == 0,
        "reviewer residue roots",
    )
    small_graphs, basis_products, associativity_triples = internal_controls()
    modular, barred_modular = modular_seed(rows)
    require(len(set(modular)) == len(set(barred_modular)) == 29,
            "reviewer residue seed collisions")
    exact = exact_seed(rows)
    seed_edges = [
        pair for pair in combinations(range(29), 2)
        if norm(sub(exact[pair[0]], exact[pair[1]])) == scale(D * D, ONE)
    ]
    require(len(seed_edges) == 51, "seed edge count")
    triangle = certificate.get("seed_triangle")
    require(
        type(triangle) is list
        and len(triangle) == len(set(triangle)) == 3
        and all(type(vertex) is int and 0 <= vertex < 29 for vertex in triangle)
        and all(tuple(sorted(pair)) in seed_edges for pair in combinations(triangle, 2)),
        "seed triangle",
    )
    base_word = unpack(certificate.get("base_word"), 29)
    require(all(colour < 3 for colour in base_word), "seed colour range")
    seed_upper_pairs = check_upper(modular, barred_modular, base_word)

    census: list[dict[str, int]] = []
    classifications = Counter()
    upper_pairs = 0
    exact_pair_tests = 0
    exact_norm_candidates = 0
    formal_positions = 0
    lower_nodes = 0
    max_lower_nodes = 0
    max_lower_vertices = 0

    for row, (centre, axis) in zip(cases, expected_cases):
        require(type(row) is list and len(row) == 5, "case row")
        require(
            type(row[0]) is int and type(row[1]) is int
            and row[0] == centre and row[1] == axis,
            "ordered case coverage",
        )
        chi, core = row[3], row[4]
        require(type(chi) is int and chi in (3, 4), "chromatic label")
        word = unpack(row[2], 174)
        require(all(colour < chi for colour in word), "upper colour range")

        values, barred_values = modular_addresses(modular, barred_modular, centre, axis)
        upper_pairs += check_upper(values, barred_values, word)
        formal, target_norm, axis_norm = exact_addresses(exact, centre, axis)
        denominator = 2 * D * residue(axis_norm) % P
        require(denominator != 0, "reviewer exact denominator")
        inverse = pow(denominator, -1, P)
        require(
            [residue(point) * inverse % P for point in formal] == values,
            "direct/exact residue disagreement",
        )
        require(
            [residue(bar(point)) * inverse % P for point in formal] == barred_values,
            "direct/exact barred residue disagreement",
        )

        first: dict[tuple[int, ...], int] = {}
        for index, point in enumerate(formal):
            first.setdefault(point, index)
        representatives = sorted(first.values())
        edge_count = 0
        target_residue = residue(target_norm)
        formal_residues = [residue(point) for point in formal]
        formal_barred = [residue(bar(point)) for point in formal]
        for i, j in combinations(representatives, 2):
            exact_pair_tests += 1
            if (
                (formal_residues[i] - formal_residues[j])
                * (formal_barred[i] - formal_barred[j])
                % P
                == target_residue
            ):
                exact_norm_candidates += 1
                if norm(sub(formal[i], formal[j])) == target_norm:
                    edge_count += 1
        vertices = len(representatives)
        census.append(
            {
                "centre": centre,
                "axis": axis,
                "D3_vertices": vertices,
                "D3_edges": edge_count,
                "D9_vertices": 3 * vertices - 2,
                "D9_edges": 3 * edge_count,
            }
        )
        formal_positions += len(formal)

        if chi == 3:
            require(core == [], "three-colour case has lower core")
        else:
            require(
                type(core) is list
                and 4 <= len(core) <= 174
                and len(core) == len(set(core))
                and all(type(index) is int and 0 <= index < 174 for index in core),
                "lower core indices",
            )
            selected = [formal[index] for index in core]
            require(len(selected) == len(set(selected)), "coincident lower-core points")
            selected_residues = [formal_residues[index] for index in core]
            selected_barred = [formal_barred[index] for index in core]
            edges: list[tuple[int, int]] = []
            for i, j in combinations(range(len(core)), 2):
                if (
                    (selected_residues[i] - selected_residues[j])
                    * (selected_barred[i] - selected_barred[j])
                    % P
                    == target_residue
                    and norm(sub(selected[i], selected[j])) == target_norm
                ):
                    edges.append((i, j))
            colourable, nodes = three_colourable_bitset(len(core), edges)
            require(not colourable, "lower core is three-colourable")
            lower_nodes += nodes
            max_lower_nodes = max(max_lower_nodes, nodes)
            max_lower_vertices = max(max_lower_vertices, len(core))
        classifications[chi] += 1

    census_bytes = json.dumps(census, separators=(",", ":")).encode()
    census_hash = sha256(census_bytes).hexdigest()
    require(census_hash == EXPECTED_CENSUS_SHA256, "complete census digest")
    require(classifications == Counter({4: 655, 3: 157}), "classification counts")
    return {
        "verified": True,
        "target_cases": 812,
        "target_certificate_sha256": EXPECTED_CERTIFICATE_SHA256,
        "reviewer_modulus": P,
        "reviewer_roots": list(ROOTS),
        "reviewer_modulus_prime": True,
        "reviewer_small_graph_controls": small_graphs,
        "reviewer_basis_products": basis_products,
        "reviewer_associativity_triples": associativity_triples,
        "seed_vertices": 29,
        "seed_edges": len(seed_edges),
        "seed_upper_pairs": seed_upper_pairs,
        "formal_positions": formal_positions,
        "upper_same_colour_pairs": upper_pairs,
        "exact_census_pair_tests": exact_pair_tests,
        "exact_norm_candidates": exact_norm_candidates,
        "census_sha256": census_hash,
        "D3_vertices_range": [
            min(row["D3_vertices"] for row in census),
            max(row["D3_vertices"] for row in census),
        ],
        "D3_edges_range": [
            min(row["D3_edges"] for row in census),
            max(row["D3_edges"] for row in census),
        ],
        "D9_vertices_range": [
            min(row["D9_vertices"] for row in census),
            max(row["D9_vertices"] for row in census),
        ],
        "D9_edges_range": [
            min(row["D9_edges"] for row in census),
            max(row["D9_edges"] for row in census),
        ],
        "exactly_three_chromatic": classifications[3],
        "exactly_four_chromatic": classifications[4],
        "lower_bitset_search_nodes": lower_nodes,
        "max_lower_bitset_search_nodes": max_lower_nodes,
        "max_lower_core_vertices": max_lower_vertices,
        "all_D9_graphs_four_colourable": True,
        "record_improvement": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target",
        type=Path,
        nargs="?",
        default=Path(__file__).resolve().parent.parent / "hadwiger_nelson_snail_dihedral",
    )
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = audit(args.target)
    if args.check_expected:
        expected = json.loads((Path(__file__).resolve().parent / "EXPECTED.json").read_text())
        require(result == expected, "expected result disagreement")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
