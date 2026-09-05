#!/usr/bin/env python3
"""Clean-room exact checker for the dense506 two-point extension theorem.

The checker imports no submitted Python module.  It rebuilds both hosts from
the pinned coordinate tables, uses generic quotient-ring multiplication and a
third modular image, rescans every host triple, checks the complete candidate
table entry by entry, and verifies the fixed-colouring list criterion.
"""

from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations
from json import dump, dumps, load
from math import comb, gcd
from pathlib import Path
import struct


D = 2592
ZERO = (0,) * 8
ONE = (1,) + (0,) * 7
PRIME, ROOT_Z, ROOT_R = 5051, 2194, 528
SOURCE_PINS = {
    159: "4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02",
    214: "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f",
}
EXPECTED = {
    "host_edges": (2389, "11af24079955c011d7ac15812b93f273044f94ce303281676abff341f33cf21a"),
    "positive_triples": (10517, "7f03bc7c1c61fc5d3ea5a0c0d8b512dd58c3bcdbd753716068e5bd83ab7ca2a2"),
    "candidate_points": (1420, "3bcfcab7e411f6adff3426ceb1cfff97718d634fe41a0e7a71982a57995c4c45"),
    "neighbors": (1420, "7c71b32a5807e4e9baab0c17953c9e2ba688e7e0d290caa9be6e23b752f564af"),
    "candidate_edges": (3975, "7912eb1140ca9a570128233517073becd52380fe3840f7cc126bc85a7493f27e"),
    "available_masks": (1420, "3521c2b5b0fa8942608728d88416688ca8b5a1d207aad59d2fd79d41be27bdb6"),
    "pair_witness": (1007490, "fd6e2b6a765b49c09f291f80711ea6534060b83390f49f92ea8e8d0e2585c2f5"),
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(a, n):
    return tuple(n * x for x in a)


def conjugate(a):
    return tuple(-x if index & 2 else x for index, x in enumerate(a))


def sigma(a):
    return tuple(-x if index & 4 else x for index, x in enumerate(a))


def reduce_monomial(ez, ea, er):
    """Reduce z^ez alpha^ea r^er using the three defining relations."""
    coefficient = 1
    if ea >= 2:
        coefficient *= -3
        ea -= 2
    terms = [(coefficient, ez, ea, er)]
    if er >= 2:
        terms = [(coefficient * -408, ez, ea, er - 2),
                 (coefficient * 72, ez + 1, ea, er - 2)]
    result = []
    for coefficient, ez, ea, er in terms:
        coefficient *= 33 ** (ez // 2)
        ez %= 2
        result.append((ez + 2 * ea + 4 * er, coefficient))
    return tuple(result)


PRODUCT = tuple(tuple(reduce_monomial((i & 1) + (j & 1),
                                      ((i >> 1) & 1) + ((j >> 1) & 1),
                                      ((i >> 2) & 1) + ((j >> 2) & 1))
                      for j in range(8)) for i in range(8))


def multiply(a, b):
    result = [0] * 8
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if not y:
                continue
            for k, coefficient in PRODUCT[i][j]:
                result[k] += coefficient * x * y
    return tuple(result)


def norm(a):
    return multiply(a, conjugate(a))


def digest(value):
    return sha256(dumps(value, separators=(",", ":")).encode()).hexdigest()


def file_digest(path):
    h = sha256()
    size = 0
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
            size += len(block)
    return {"bytes": size, "sha256": h.hexdigest()}


def read_source(path, n):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == SOURCE_PINS[n], f"source pin {n}")
    rows = []
    for line in raw.decode().splitlines():
        if not line or line.startswith("#"):
            continue
        source = tuple(map(int, line.split()))
        require(len(source) == 16, "source row width")
        require(not any(source[i] for i in range(16) if i not in (0, 5, 9, 12)),
                "unexpected source basis")
        rows.append((3 * source[0], 3 * source[5], 3 * source[9], source[12], 0, 0, 0, 0))
    require(len(rows) == len(set(rows)) == n, f"source cardinality {n}")
    return rows


def build_host(points159, points214, epsilon):
    translation = (15, 3, 15, -1, 0, 0, 0, 0)
    inner = list(dict.fromkeys(points159 + [add(conjugate(a), translation) for a in points159]))
    require(len(inner) == 293 and inner[0] == ZERO, "inner assembly")
    anchor = points214[10]
    require(anchor == (0, 0, 6, 0, 0, 0, 0, 0), "source anchor")
    shifted = [sub(v, anchor) for v in points214]
    rotation = (-18, -6, -30, 6, 3 * epsilon, 0, 6 * epsilon, epsilon)
    require(norm(rotation) == scale(ONE, 72 ** 2), "rotation norm")
    host = [scale(v, 72) for v in inner]
    host.extend(multiply(rotation, shifted[j]) for j in range(214) if j != 10)
    require(len(host) == len(set(host)) == 506, "host cardinality")
    return host


def normalize(numerator, denominator):
    require(denominator, "zero denominator")
    if denominator < 0:
        numerator, denominator = scale(numerator, -1), -denominator
    common = gcd(denominator, *numerator)
    return (denominator // common,) + tuple(x // common for x in numerator)


def decode_candidate(row):
    require(len(row) == 9 and row[0] > 0, "candidate encoding")
    numerator = (row[1], row[2], row[5], row[6], row[3], row[4], row[7], row[8])
    canonical = normalize(numerator, row[0])
    encoded = (canonical[0], canonical[1], canonical[2], canonical[5], canonical[6],
               canonical[3], canonical[4], canonical[7], canonical[8])
    require(encoded == tuple(row), "noncanonical candidate")
    return canonical[1:], canonical[0]


def rational_equal(a, b):
    x, d = a
    y, e = b
    return scale(x, e) == scale(y, d)


def unit_pair(a, b):
    x, d = a
    y, e = b
    delta = sub(scale(x, e), scale(y, d))
    return norm(delta) == scale(ONE, (d * e) ** 2)


def modular_point(point):
    numerator, denominator = point
    require(denominator % PRIME, "noninvertible denominator")
    inverse = pow(denominator, -1, PRIME)
    x = (numerator[0] + ROOT_Z * numerator[1] + ROOT_R * numerator[4] +
         ROOT_Z * ROOT_R * numerator[5]) * inverse % PRIME
    y = (numerator[2] + ROOT_Z * numerator[3] + ROOT_R * numerator[6] +
         ROOT_Z * ROOT_R * numerator[7]) * inverse % PRIME
    return x, y


def maybe_unit(a, b):
    dx, dy = (a[0] - b[0]) % PRIME, (a[1] - b[1]) % PRIME
    return (dx * dx + 3 * dy * dy - 1) % PRIME == 0


def graph_edges(points):
    modular = list(map(modular_point, points))
    edges = []
    exact_tests = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if maybe_unit(modular[i], modular[j]):
                exact_tests += 1
                if unit_pair(points[i], points[j]):
                    edges.append((i, j))
    return edges, exact_tests


def host_norms(host):
    matrix = [[None] * len(host) for _ in host]
    for i in range(len(host)):
        for j in range(i + 1, len(host)):
            value = norm(sub(host[j], host[i]))
            matrix[i][j] = matrix[j][i] = value
    return matrix


def exact_unit_circumradius(host, norms, i, j, k):
    d = sub(host[j], host[i])
    e = sub(host[k], host[i])
    determinant = sub(multiply(conjugate(d), e), multiply(conjugate(e), d))
    product = multiply(multiply(norms[i][j], norms[i][k]), norms[j][k])
    return add(product, scale(multiply(determinant, determinant), D * D)) == ZERO


def triple_census(host, norms, host_edges, expected_external):
    modular = [modular_point((point, D)) for point in host]
    squared = [[0] * len(host) for _ in host]
    for i in range(len(host)):
        for j in range(i + 1, len(host)):
            dx = (modular[j][0] - modular[i][0]) % PRIME
            dy = (modular[j][1] - modular[i][1]) % PRIME
            squared[i][j] = squared[j][i] = (dx * dx + 3 * dy * dy) % PRIME

    survivors = []
    for i in range(len(host)):
        xi, yi = modular[i]
        for j in range(i + 1, len(host)):
            dx, dy = (modular[j][0] - xi) % PRIME, (modular[j][1] - yi) % PRIME
            a = squared[i][j]
            for k in range(j + 1, len(host)):
                ex, ey = (modular[k][0] - xi) % PRIME, (modular[k][1] - yi) % PRIME
                determinant = (dx * ey - ex * dy) % PRIME
                if (a * squared[i][k] * squared[j][k] - 12 * determinant * determinant) % PRIME == 0:
                    survivors.append((i, j, k))

    exact = {triple for triple in survivors if exact_unit_circumradius(host, norms, *triple)}
    adjacency = [set() for _ in host]
    for a, b in host_edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    known_list = [triple for center in range(len(host))
                  for triple in combinations(sorted(adjacency[center]), 3)]
    known = set(known_list)
    require(len(known) == len(known_list) == 93131, "host-centred triple uniqueness")
    require(known <= exact, "known unit circles missing from exact census")
    external = sorted(exact - known)
    require(external == expected_external, "external unit-circle triples")
    return {"triples": comb(506, 3), "third_prime": PRIME, "root_z": ROOT_Z,
            "root_r": ROOT_R, "modular_survivors": len(survivors),
            "exact_unit_circumradius_triples": len(exact),
            "known_host_centres": len(known), "external_centre_triples": len(external),
            "external_triple_sha256": digest(external)}


def main():
    parser = ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--candidate-work", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    root = args.source.parent

    require(ROOT_Z * ROOT_Z % PRIME == 33, "third-prime z root")
    require(ROOT_R * ROOT_R % PRIME == (-408 + 72 * ROOT_Z) % PRIME, "third-prime r root")
    require(D % PRIME, "coordinate scale modulo prime")

    p159 = read_source(root / "hadwiger_nelson_nonmono159_214_lowden2/points159.tsv", 159)
    p214 = read_source(root / "hadwiger_nelson_nonmono159_214_lowden2/points214.tsv", 214)
    plus = build_host(p159, p214, 1)
    minus = build_host(p159, p214, -1)
    require(minus == [sigma(point) for point in plus], "root conjugation of host")
    basis = [tuple(int(i == j) for i in range(8)) for j in range(8)]
    require(all(sigma(multiply(a, b)) == multiply(sigma(a), sigma(b)) for a in basis for b in basis),
            "sigma is not a ring automorphism")
    require(all(sigma(conjugate(a)) == conjugate(sigma(a)) for a in basis),
            "sigma does not commute with conjugation")

    plus_rational = [(point, D) for point in plus]
    minus_rational = [(point, D) for point in minus]
    plus_edges, plus_edge_tests = graph_edges(plus_rational)
    minus_edges, minus_edge_tests = graph_edges(minus_rational)
    require(plus_edges == minus_edges, "two roots have different edge graphs")
    require((len(plus_edges), digest(plus_edges)) == EXPECTED["host_edges"], "host edge graph")

    with (args.candidate_work / "candidates.json").open() as stream:
        table = load(stream)
    raw_points = table["points"]
    candidates = [decode_candidate(row) for row in raw_points]
    require(len(candidates) == len({tuple(row) for row in raw_points}) == 1420, "candidate cardinality")
    canonical_host = {normalize(point, D) for point in plus}
    canonical_candidates = {(denominator,) + numerator for numerator, denominator in candidates}
    require(not canonical_host.intersection(canonical_candidates), "host point in candidate table")
    require((len(raw_points), digest(raw_points)) == EXPECTED["candidate_points"], "candidate digest")

    all_points = plus_rational + candidates
    all_modular = list(map(modular_point, all_points))
    rebuilt_neighbors = []
    host_candidate_exact = 0
    for i, candidate in enumerate(candidates):
        neighbors = []
        cm = all_modular[506 + i]
        for j, host_point in enumerate(plus_rational):
            if maybe_unit(cm, all_modular[j]):
                host_candidate_exact += 1
                if unit_pair(candidate, host_point):
                    neighbors.append(j)
        rebuilt_neighbors.append(neighbors)
    require(rebuilt_neighbors == table["neighbors"], "candidate-host adjacency")
    require((len(rebuilt_neighbors), digest(rebuilt_neighbors)) == EXPECTED["neighbors"], "neighbor digest")

    rebuilt_candidate_edges = []
    candidate_exact = 0
    candidate_modular = all_modular[506:]
    for i in range(len(candidates)):
        for j in range(i + 1, len(candidates)):
            if maybe_unit(candidate_modular[i], candidate_modular[j]):
                candidate_exact += 1
                if unit_pair(candidates[i], candidates[j]):
                    rebuilt_candidate_edges.append((i, j))
    require(rebuilt_candidate_edges == [tuple(edge) for edge in table["candidate_edges"]],
            "candidate-candidate adjacency")
    require((len(rebuilt_candidate_edges), digest(rebuilt_candidate_edges)) == EXPECTED["candidate_edges"],
            "candidate-edge digest")

    color_raw = (args.source / "host_colors.txt").read_bytes()
    require(file_digest(args.source / "host_colors.txt") ==
            {"bytes": 507, "sha256": "010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4"},
            "colour certificate identity")
    lines = color_raw.decode().splitlines()
    require(len(lines) == 1 and len(lines[0]) == 506, "colour row dimensions")
    colors = tuple(map(int, lines[0]))
    require(set(colors) <= set(range(4)), "colour domain")
    require(all(colors[a] != colors[b] for a, b in plus_edges), "improper host colouring")
    available = []
    for neighbors in rebuilt_neighbors:
        used = {colors[v] for v in neighbors}
        available.append(sum(1 << color for color in range(4) if color not in used))
    require(available == table["available_masks"] and all(available), "available colours")
    require((len(available), digest(available)) == EXPECTED["available_masks"], "available digest")

    edge_set = set(rebuilt_candidate_edges)
    witness_hash = sha256()
    uncovered = equal_singleton = singleton_edges = 0
    for i in range(len(candidates)):
        choices_i = [c for c in range(4) if available[i] & (1 << c)]
        for j in range(i + 1, len(candidates)):
            choices_j = [c for c in range(4) if available[j] & (1 << c)]
            edge = (i, j) in edge_set
            if edge and len(choices_i) == len(choices_j) == 1:
                singleton_edges += 1
                equal_singleton += choices_i == choices_j
            witness = next(((a, b) for a in choices_i for b in choices_j if not edge or a != b), None)
            if witness is None:
                uncovered += 1
            else:
                witness_hash.update(struct.pack("<HHBB", i, j, *witness))
    require(uncovered == equal_singleton == 0 and singleton_edges == 1880, "two-list obstruction")
    require((comb(1420, 2), witness_hash.hexdigest()) == EXPECTED["pair_witness"], "pair witnesses")

    expected_external = [tuple(row) for row in table["positive_triples"]]
    require((len(expected_external), digest(expected_external)) == EXPECTED["positive_triples"],
            "positive-triple table")
    cover_list = [triple for neighbors in rebuilt_neighbors for triple in combinations(neighbors, 3)]
    require(len(cover_list) == len(set(cover_list)) == 10517, "candidate triple cover uniqueness")
    require(sorted(cover_list) == expected_external, "candidate neighborhoods do not cover positive triples")
    norms = host_norms(plus)
    triple_report = triple_census(plus, norms, plus_edges, expected_external)

    report = {
        "format": "hn-dense506-two-point-review1-v1",
        "all_checks_passed": True,
        "hosts": {"vertices_each": 506, "edges_each": len(plus_edges),
                  "edge_sha256": digest(plus_edges), "two_roots_same_graph": True,
                  "sigma_ring_basis_products_checked": 64,
                  "plus_edge_exact_tests_after_third_screen": plus_edge_tests,
                  "minus_edge_exact_tests_after_third_screen": minus_edge_tests},
        "candidate_points": len(candidates),
        "candidate_point_sha256": digest(raw_points),
        "host_candidate_edges": sum(map(len, rebuilt_neighbors)),
        "neighbor_sha256": digest(rebuilt_neighbors),
        "candidate_edges": len(rebuilt_candidate_edges),
        "candidate_edge_sha256": digest(rebuilt_candidate_edges),
        "third_screen_exact_tests": {"host_candidate": host_candidate_exact,
                                     "candidate_candidate": candidate_exact},
        "triple_census": triple_report,
        "degree_histogram": dict(sorted(Counter(map(len, rebuilt_neighbors)).items())),
        "available_list_size_histogram": dict(sorted(Counter(mask.bit_count() for mask in available).items())),
        "available_mask_sha256": digest(available),
        "candidate_pairs_checked": comb(len(candidates), 2),
        "singleton_candidate_edges": singleton_edges,
        "equal_singleton_candidate_edges": equal_singleton,
        "uncovered_pairs": uncovered,
        "pair_witness_sha256": witness_hash.hexdigest(),
        "fixed_coloring": file_digest(args.source / "host_colors.txt"),
        "floating_point_decisions": 0,
        "target_graph_claimed": False,
    }
    require(report["host_candidate_edges"] == 5710, "host-candidate edge count")
    require(report["available_list_size_histogram"] == {1: 941, 2: 461, 3: 18},
            "available-list histogram")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    with args.report.open("w") as stream:
        dump(report, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print("PASS both hosts, third-prime triple census, all adjacencies, and all two-point lists")


if __name__ == "__main__":
    main()
