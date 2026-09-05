#!/usr/bin/env python3
"""Independent exact audit of the dense506 one-low-point repair stratum.

This checker imports no module from the contribution under review.  It uses
the previously reviewed host/candidate arithmetic, but performs the new
52-million-row census with a third modular image, a fresh real-coordinate
quartic-field implementation, and direct brute-force list colouring.
"""

from argparse import ArgumentParser
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, product
from json import dump, dumps, load
from math import gcd, lcm
from pathlib import Path


D = 2592
PRIME, ROOT_Z, ROOT_R = 5051, 2194, 528
PRIOR_REVIEW_SHA = "9b7e9de99164784b1e7504800442bc1931ecdcaf5217cbae4382b026187e3b72"
HOST_COLOUR_SHA = "010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4"
CANDIDATE_PINS = {
    "points": "3bcfcab7e411f6adff3426ceb1cfff97718d634fe41a0e7a71982a57995c4c45",
    "positive_triples": "7f03bc7c1c61fc5d3ea5a0c0d8b512dd58c3bcdbd753716068e5bd83ab7ca2a2",
    "neighbors": "7c71b32a5807e4e9baab0c17953c9e2ba688e7e0d290caa9be6e23b752f564af",
    "candidate_edges": "7912eb1140ca9a570128233517073becd52380fe3840f7cc126bc85a7493f27e",
    "available_masks": "3521c2b5b0fa8942608728d88416688ca8b5a1d207aad59d2fd79d41be27bdb6",
}
SOURCE_POINT_SHA = "28b46f5eae9a537d8a189d03284e32d9012fbccde35f05bd72e19ee1f1699f43"
SOURCE_POSITIVE_SHA = "940266d1d44a967083fdaf371623bff7bf03fc2eca5e938c8de838a8b9891c96"
SOURCE_WITNESS_SHA = "5dce583891389a59cecc768c67db11e1b5afd4820fdb50bd4c6124faa5f7dcaf"


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def digest(value):
    return sha256(dumps(value, separators=(",", ":")).encode()).hexdigest()


def fadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def fsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def fscale(a, scalar):
    return tuple(scalar * x for x in a)


def fmul(a, b):
    """Multiply in Q[z,r]/(z^2-33, r^2+408-72z)."""
    answer = [0, 0, 0, 0]
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if not y:
                continue
            ez = (i & 1) + (j & 1)
            er = (i >> 1) + (j >> 1)
            terms = [(x * y, ez, er)]
            if er == 2:
                terms = [(-408 * x * y, ez, 0), (72 * x * y, ez + 1, 0)]
            for coefficient, z_power, r_power in terms:
                coefficient *= 33 ** (z_power // 2)
                answer[(z_power % 2) + 2 * r_power] += coefficient
    return tuple(answer)


@lru_cache(None)
def finverse(a):
    """Invert a quartic-field element by exact Gaussian elimination."""
    basis = [tuple(Fraction(i == j) for i in range(4)) for j in range(4)]
    columns = [fmul(a, vector) for vector in basis]
    matrix = [[columns[column][row] for column in range(4)]
              + [Fraction(row == 0)] for row in range(4)]
    for column in range(4):
        pivot = next((row for row in range(column, 4) if matrix[row][column]), None)
        require(pivot is not None, "singular quartic element")
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        divisor = matrix[column][column]
        matrix[column] = [value / divisor for value in matrix[column]]
        for row in range(4):
            if row == column:
                continue
            multiple = matrix[row][column]
            if multiple:
                matrix[row] = [x - multiple * y
                               for x, y in zip(matrix[row], matrix[column])]
    result = tuple(matrix[row][4] for row in range(4))
    require(fmul(a, result) == (1, 0, 0, 0), "quartic inverse check")
    return result


def split_point(point):
    return ((point[0], point[1], point[4], point[5]),
            (point[2], point[3], point[6], point[7]))


def squared_distance(a, b):
    ax, ay = split_point(a)
    bx, by = split_point(b)
    dx, dy = fsub(bx, ax), fsub(by, ay)
    return fadd(fmul(dx, dx), fscale(fmul(dy, dy), 3))


def circle_identity(points, i, j, k):
    a = squared_distance(points[i], points[j])
    b = squared_distance(points[i], points[k])
    c = squared_distance(points[j], points[k])
    heron = fsub(fscale(fadd(fadd(fmul(a, b), fmul(a, c)), fmul(b, c)), 2),
                 fadd(fadd(fmul(a, a), fmul(b, b)), fmul(c, c)))
    return fmul(fmul(a, b), c) == fscale(heron, D * D)


def canonical_key(x, y):
    values = [Fraction(value, D) for value in (*x, *y)]
    denominator = lcm(*(value.denominator for value in values))
    integers = [int(value * denominator) for value in values]
    common = gcd(denominator, *integers)
    return (denominator // common,) + tuple(value // common for value in integers)


def point_key(point):
    return canonical_key(*split_point(point))


def circle_centre(points, i, j, k):
    px, py = split_point(points[i])
    qx, qy = split_point(points[j])
    sx, sy = split_point(points[k])
    dx, dy = fsub(qx, px), fsub(qy, py)
    ex, ey = fsub(sx, px), fsub(sy, py)
    a = fadd(fmul(dx, dx), fscale(fmul(dy, dy), 3))
    b = fadd(fmul(ex, ex), fscale(fmul(ey, ey), 3))
    determinant = fsub(fmul(dx, ey), fmul(ex, dy))
    require(any(determinant), "collinear positive triple")
    inverse = finverse(determinant)
    cx = fscale(fmul(fsub(fmul(a, ey), fmul(b, dy)), inverse), Fraction(1, 2))
    cy = fscale(fmul(fsub(fmul(dx, b), fmul(ex, a)), inverse), Fraction(1, 6))
    return canonical_key(fadd(px, cx), fadd(py, cy))


def possible_colouring(mask, first, second, xp, xq, pq, reverse=False):
    order = range(3, -1, -1) if reverse else range(4)
    return next(((x, p, q) for x in order for p in order for q in order
                 if mask >> x & 1 and first >> p & 1 and second >> q & 1
                 and (not xp or x != p) and (not xq or x != q)
                 and (not pq or p != q)), None)


def list_criterion_audit():
    cases = obstructions = 0
    for mask in range(1, 16):
        if mask.bit_count() != 2:
            continue
        for first, second in product(range(1, 16), repeat=2):
            for xp, xq, pq in product((False, True), repeat=3):
                if pq and first == second and first.bit_count() == 1:
                    continue
                colourable = possible_colouring(mask, first, second, xp, xq, pq)
                predicted_bad = (xp and xq and not (first & ~mask)
                                 and not (second & ~mask)
                                 and (pq or (first != second
                                             and first.bit_count() == 1
                                             and second.bit_count() == 1)))
                require((colourable is None) == predicted_bad,
                        ("list criterion", mask, first, second, xp, xq, pq))
                cases += 1
                obstructions += colourable is None
    require((cases, obstructions) == (10704, 54), "list audit totals")
    return cases, obstructions


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--candidate-work", type=Path, required=True)
    parser.add_argument("--repair-work", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo.resolve()

    prior_path = root / "hadwiger_nelson_dense506_two_point_extension_review1/independent_check.py"
    require(sha256(prior_path.read_bytes()).hexdigest() == PRIOR_REVIEW_SHA,
            "prior independent checker pin")
    spec = spec_from_file_location("dense506_prior_review", prior_path)
    prior = module_from_spec(spec)
    spec.loader.exec_module(prior)

    require(PRIME > 3 and D % PRIME, "third-prime scale")
    require(ROOT_Z * ROOT_Z % PRIME == 33, "third-prime z root")
    require(ROOT_R * ROOT_R % PRIME == (-408 + 72 * ROOT_Z) % PRIME,
            "third-prime r root")
    field_basis = [tuple(Fraction(i == j) for i in range(4)) for j in range(4)]
    one, z_element, r_element = field_basis[0], field_basis[1], field_basis[2]
    require(fmul(z_element, z_element) == (33, 0, 0, 0), "quartic z relation")
    require(fmul(r_element, r_element) == (-408, 72, 0, 0), "quartic r relation")
    require(all(fmul(fmul(a, b), c) == fmul(a, fmul(b, c))
                for a, b, c in product(field_basis, repeat=3)),
            "quartic basis associativity")
    require(all(fmul(one, a) == a for a in field_basis), "quartic identity")

    source = root / "hadwiger_nelson_nonmono159_214_lowden2"
    points159 = prior.read_source(source / "points159.tsv", 159)
    points214 = prior.read_source(source / "points214.tsv", 214)
    host = prior.build_host(points159, points214, 1)
    minus_host = prior.build_host(points159, points214, -1)
    require(minus_host == [prior.sigma(point) for point in host], "host conjugation")

    with (args.candidate_work / "candidates.json").open() as stream:
        candidate_table = load(stream)
    require(set(candidate_table) == set(CANDIDATE_PINS), "candidate table fields")
    for name, expected in CANDIDATE_PINS.items():
        require(digest(candidate_table[name]) == expected, ("candidate pin", name))

    candidates = []
    for row in candidate_table["points"]:
        numerator, denominator = prior.decode_candidate(row)
        require(D % denominator == 0, "candidate common denominator")
        candidates.append(prior.scale(numerator, D // denominator))
    points = host + candidates
    require(len(points) == len(set(points)) == 1926, "known support cardinality")

    colour_path = root / "hadwiger_nelson_dense506_two_point_extension/host_colors.txt"
    raw_colours = colour_path.read_bytes()
    require(sha256(raw_colours).hexdigest() == HOST_COLOUR_SHA, "host colour pin")
    require(len(raw_colours) == 507 and raw_colours[-1:] == b"\n", "host colour shape")
    colours = [value - ord("0") for value in raw_colours[:-1]]
    require(set(colours) <= set(range(4)), "host colour alphabet")

    host_edges, host_exact_tests = prior.graph_edges([(point, D) for point in host])
    require(len(host_edges) == 2389 and digest(host_edges) == prior.EXPECTED["host_edges"][1],
            "host graph")
    require(all(colours[i] != colours[j] for i, j in host_edges), "host colouring")
    rebuilt_masks = []
    for neighbours in candidate_table["neighbors"]:
        used = {colours[vertex] for vertex in neighbours}
        rebuilt_masks.append(sum(1 << colour for colour in range(4) if colour not in used))
    require(rebuilt_masks == candidate_table["available_masks"] and all(rebuilt_masks),
            "candidate lists")
    candidate_edges = {tuple(edge) for edge in candidate_table["candidate_edges"]}
    require(all(not (rebuilt_masks[i] == rebuilt_masks[j]
                     and rebuilt_masks[i].bit_count() == 1)
                for i, j in candidate_edges), "candidate pair hypothesis")

    adjacency = [0] * len(points)
    all_edges = list(host_edges)
    all_edges.extend((host_vertex, 506 + candidate)
                     for candidate, neighbours in enumerate(candidate_table["neighbors"])
                     for host_vertex in neighbours)
    all_edges.extend((506 + i, 506 + j) for i, j in candidate_edges)
    require(len(all_edges) == 12074, "known support edge count")
    for i, j in all_edges:
        adjacency[i] |= 1 << j
        adjacency[j] |= 1 << i

    inverse_d = pow(D, -1, PRIME)
    modular = [((point[0] + ROOT_Z * point[1] + ROOT_R * point[4]
                 + ROOT_Z * ROOT_R * point[5]) * inverse_d % PRIME,
                (point[2] + ROOT_Z * point[3] + ROOT_R * point[6]
                 + ROOT_Z * ROOT_R * point[7]) * inverse_d % PRIME)
               for point in points]
    modular_distances = [[((x - X) ** 2 + 3 * (y - Y) ** 2) % PRIME
                          for X, Y in modular] for x, y in modular[:506]]
    eligible = {mask: [candidate for candidate, available in enumerate(rebuilt_masks)
                       if not (available & ~mask)]
                for mask in range(1, 16) if mask.bit_count() == 2}

    survivors = []
    differently_coloured_pairs = eligible_rows = 0
    for i in range(506):
        xi, yi = modular[i]
        for j in range(i + 1, 506):
            if colours[i] == colours[j]:
                continue
            differently_coloured_pairs += 1
            mask = 15 ^ (1 << colours[i]) ^ (1 << colours[j])
            choices = eligible[mask]
            eligible_rows += len(choices)
            dx, dy = modular[j][0] - xi, modular[j][1] - yi
            a = modular_distances[i][j]
            for candidate in choices:
                k = 506 + candidate
                ex, ey = modular[k][0] - xi, modular[k][1] - yi
                determinant = (dx * ey - ex * dy) % PRIME
                if (a * modular_distances[i][k] * modular_distances[j][k]
                        - 12 * determinant * determinant) % PRIME == 0:
                    survivors.append((i, j, candidate))
    require((differently_coloured_pairs, eligible_rows) == (96003, 52550758),
            "complete eligible domain")

    known_centres = 0
    centres = defaultdict(list)
    positive = []
    known_points = {point_key(point) for point in points}
    for i, j, candidate in survivors:
        k = 506 + candidate
        if not circle_identity(points, i, j, k):
            continue
        common = adjacency[i] & adjacency[j] & adjacency[k]
        if common:
            require(common.bit_count() == 1, "nonunique known centre")
            known_centres += 1
            continue
        centre = circle_centre(points, i, j, k)
        require(centre not in known_points, "unremoved known centre")
        centres[centre].append((i, j, candidate))
        positive.append((i, j, candidate))

    with (args.repair_work / "centres.json").open() as stream:
        source_table = load(stream)
    require(set(source_table) == {"points", "host_pairs", "eligible_candidate_neighbors",
                                  "positive_triples", "obstructions"},
            "source centre table fields")
    require(source_table["obstructions"] == [], "source reports obstruction")
    ordered_centres = sorted(centres)
    require(ordered_centres == [tuple(row) for row in source_table["points"]],
            "external centres entrywise")
    require(positive == [tuple(row) for row in source_table["positive_triples"]],
            "positive triples entrywise")
    require(digest(ordered_centres) == SOURCE_POINT_SHA, "external centre digest")
    require(digest(positive) == SOURCE_POSITIVE_SHA, "positive triple digest")

    host_pairs = []
    eligible_neighbours = []
    source_witness = sha256()
    alternate_witness = sha256()
    pair_count = 0
    for outside_index, centre in enumerate(ordered_centres):
        triples = centres[centre]
        pairs = {row[:2] for row in triples}
        require(len(pairs) == 1, "external point has other host pair")
        host_pair = next(iter(pairs))
        host_pairs.append(host_pair)
        neighbours = sorted(row[2] for row in triples)
        require(len(neighbours) == len(set(neighbours)), "duplicate eligible incidence")
        eligible_neighbours.append(neighbours)
        mask = 15 ^ (1 << colours[host_pair[0]]) ^ (1 << colours[host_pair[1]])
        for first, second in combinations(neighbours, 2):
            adjacent = (first, second) in candidate_edges
            witness = possible_colouring(mask, rebuilt_masks[first], rebuilt_masks[second],
                                         True, True, adjacent)
            alternate = possible_colouring(mask, rebuilt_masks[first], rebuilt_masks[second],
                                           True, True, adjacent, reverse=True)
            require(witness is not None and alternate is not None,
                    ("actual list obstruction", outside_index, first, second))
            source_witness.update((dumps([outside_index, first, second, *witness],
                                         separators=(",", ":")) + "\n").encode())
            alternate_witness.update((dumps([outside_index, first, second, *alternate],
                                            separators=(",", ":")) + "\n").encode())
            pair_count += 1
    require(host_pairs == [tuple(row) for row in source_table["host_pairs"]],
            "host pairs entrywise")
    require(eligible_neighbours == source_table["eligible_candidate_neighbors"],
            "eligible neighbours entrywise")
    require(source_witness.hexdigest() == SOURCE_WITNESS_SHA, "source witness stream")
    require(pair_count == 1262, "actual pair count")

    list_cases, abstract_obstructions = list_criterion_audit()
    basis = [tuple(int(i == j) for i in range(8)) for j in range(8)]
    require(all(prior.sigma(prior.multiply(a, b))
                == prior.multiply(prior.sigma(a), prior.sigma(b))
                for a, b in product(basis, repeat=2)), "sigma multiplication")
    require(all(prior.sigma(prior.conjugate(a))
                == prior.conjugate(prior.sigma(a)) for a in basis), "sigma conjugation")
    minus_points = [prior.sigma(point) for point in points]
    require(all(circle_identity(minus_points, i, j, 506 + candidate)
                for i, j, candidate in positive), "minus-root positive triples")

    report = {
        "status": "accepted at one arbitrary plus two completion points scope",
        "imported_candidate_census": True,
        "third_prime": PRIME,
        "third_root_z": ROOT_Z,
        "third_root_r": ROOT_R,
        "host_graph_exact_tests": host_exact_tests,
        "differently_coloured_host_pairs": differently_coloured_pairs,
        "eligible_triples": eligible_rows,
        "third_prime_survivors": len(survivors),
        "third_prime_survivor_sha256": digest(survivors),
        "exact_circumradius_triples": known_centres + len(positive),
        "third_prime_false_positives": len(survivors) - known_centres - len(positive),
        "known_support_centre_triples": known_centres,
        "external_centre_triples": len(positive),
        "external_centres": len(ordered_centres),
        "external_centre_sha256": digest(ordered_centres),
        "positive_triple_sha256": digest(positive),
        "source_table_entrywise_match": True,
        "eligible_neighbour_histogram": dict(sorted(Counter(map(len, eligible_neighbours)).items())),
        "centres_with_at_least_two_eligible": sum(len(row) >= 2 for row in eligible_neighbours),
        "actual_candidate_pairs_brute_coloured": pair_count,
        "source_witness_sha256": source_witness.hexdigest(),
        "alternate_reverse_witness_sha256": alternate_witness.hexdigest(),
        "abstract_list_cases": list_cases,
        "abstract_obstructions": abstract_obstructions,
        "all_abstract_predictions_match_brute_force": True,
        "quartic_basis_relations_checked": True,
        "minus_root_transport_checked": True,
        "uncovered_actual_cases": 0,
    }
    with args.report.open("w") as stream:
        dump(report, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(args.report)


if __name__ == "__main__":
    main()
