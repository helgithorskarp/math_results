#!/usr/bin/env python3
"""Clean-room incidence-graph and exact-dual audit for C(13,7,5)=78."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path

import networkx as nx


POINTS12 = tuple(range(1, 13))
R = tuple(range(2, 13))
GENERATORS = (
    (2, 3, 4, 6, 5, 9, 8, 7, 10, 11, 12),
    (3, 4, 7, 9, 11, 2, 6, 5, 10, 12, 8),
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_blocks(path, size, allowed):
    blocks = []
    for raw in path.read_text(encoding="ascii").splitlines():
        text = raw.partition("#")[0].strip()
        if text:
            block = tuple(sorted(map(int, text.split())))
            require(len(block) == len(set(block)) == size, "malformed block")
            require(set(block) <= allowed, "out-of-range block")
            blocks.append(block)
    require(len(blocks) == len(set(blocks)), "duplicate block")
    return tuple(blocks)


def incidence_group(blocks):
    graph = nx.Graph()
    for point in R:
        graph.add_node(("p", point), color="point")
    for index, block in enumerate(blocks):
        node = ("b", index)
        graph.add_node(node, color="block")
        graph.add_edges_from((node, ("p", point)) for point in block)
    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph,
        graph,
        node_match=nx.algorithms.isomorphism.categorical_node_match("color", None),
    )
    return {
        tuple(mapping[("p", point)][1] for point in R)
        for mapping in matcher.isomorphisms_iter()
    }


def compose(left, right):
    return tuple(left[right[point - 2] - 2] for point in R)


def generated_group(blocks):
    block_sets = set(map(frozenset, blocks))
    for generator in GENERATORS:
        require(
            {frozenset(generator[p - 2] for p in block) for block in blocks}
            == block_sets,
            "generator does not preserve second link",
        )
    group = {R}
    boundary = deque([R])
    while boundary:
        current = boundary.popleft()
        for generator in GENERATORS:
            product = compose(generator, current)
            if product not in group:
                group.add(product)
                boundary.append(product)
    return group


def weak_compositions(total, length, prefix=()):
    if length == 1:
        yield prefix + (total,)
    else:
        for value in range(total + 1):
            yield from weak_compositions(total - value, length - 1, prefix + (value,))


def image_profile(profile, permutation):
    result = [None] * 11
    for old, value in enumerate(profile):
        result[permutation[old] - 2] = value
    return tuple(result)


def profile_orbits(group):
    unseen = set(weak_compositions(6, 11))
    result = []
    while unseen:
        representative = min(unseen)
        orbit = {image_profile(representative, permutation) for permutation in group}
        require(orbit <= unseen, "overlapping profile orbits")
        result.append((representative, len(orbit)))
        unseen -= orbit
    require(len(result) == 143, "wrong profile-orbit count")
    require(sum(size for _, size in result) == 8008, "incomplete profile cover")
    return result


def link_rows(second, profile, candidates, blocker=None):
    second_sets = tuple(map(frozenset, second))
    candidate_sets = tuple(map(frozenset, candidates))
    rows = []
    for target in combinations(R, 4):
        target = frozenset(target)
        if not any(target <= block for block in second_sets):
            rows.append((tuple(i for i, block in enumerate(candidate_sets) if target <= block), 1, None))
    require(len(rows) == 230, "wrong residual-quadruple count")
    rows.append((tuple(range(462)), 21, 21))
    fixed_degrees = Counter(point for block in second for point in block)
    for point, excess in zip(R, profile):
        target = 20 + excess - fixed_degrees[point]
        rows.append((tuple(i for i, block in enumerate(candidate_sets) if point in block), target, target))
    fixed_full = tuple(frozenset((1, *block)) for block in second)
    for size, lower in ((2, 9), (3, 3)):
        for target in combinations(POINTS12, size):
            target = frozenset(target)
            need = lower - sum(target <= block for block in fixed_full)
            if need > 0:
                columns = tuple(i for i, block in enumerate(candidate_sets) if target <= block)
                require(columns, "empty positive shadow row")
                rows.append((columns, need, None))
    if blocker is not None:
        rows.append((tuple(blocker), None, 20))
    require(len(rows) == (458 if blocker is not None else 457), "wrong link-row count")
    return rows


def completion_rows(second, left, right, candidates):
    known = tuple(map(frozenset, second + left + right))
    candidate_sets = tuple(map(frozenset, candidates))
    rows = []
    for target in combinations(R, 5):
        target = frozenset(target)
        if not any(target <= block for block in known):
            rows.append((tuple(i for i, block in enumerate(candidate_sets) if target <= block), 1, None))
    residual = len(rows)
    rows.append((tuple(range(330)), 15, 15))
    return rows, residual


def check_dual(case, variable_count, rows):
    require(case["row_count"] == len(rows), "dual row-count mismatch")
    require(case["matrix_nonzeros"] == sum(len(row[0]) for row in rows), "dual nonzero mismatch")
    multipliers = [0] * len(rows)
    previous = -1
    for index, value in case["multipliers"]:
        require(previous < index < len(rows), "bad sparse dual index")
        require(isinstance(value, int) and value != 0, "bad sparse dual value")
        multipliers[index] = value
        previous = index
    coefficients = [0] * variable_count
    rhs = 0
    for multiplier, (columns, lower, upper) in zip(multipliers, rows):
        if multiplier > 0:
            require(lower is not None, "positive dual multiplier without lower bound")
            rhs += multiplier * lower
        elif multiplier < 0:
            require(upper is not None, "negative dual multiplier without upper bound")
            rhs += multiplier * upper
        for column in columns:
            coefficients[column] += multiplier
    metrics = {
        "support": sum(value != 0 for value in multipliers),
        "max_abs_multiplier": max(map(abs, multipliers), default=0),
        "rhs": rhs,
        "max_box_lhs": sum(max(value, 0) for value in coefficients),
    }
    metrics["gap"] = metrics["rhs"] - metrics["max_box_lhs"]
    require(all(case[key] == value for key, value in metrics.items()), "dual metrics mismatch")
    require(metrics["gap"] > 0, "nonpositive dual gap")
    return metrics


def verify_extension(second, extension):
    require(len(extension) == len(set(extension)) == 21, "bad extension size")
    full = tuple(frozenset((1, *block)) for block in second) + tuple(map(frozenset, extension))
    require(
        all(any(frozenset(target) <= block for block in full) for target in combinations(POINTS12, 4)),
        "extension misses a quadruple",
    )
    degrees = Counter(point for block in full for point in block)
    profile = tuple(degrees[point] - 20 for point in R)
    require(degrees[1] == 20 and min(profile) >= 0 and sum(profile) == 6, "bad extension profile")
    return profile


def image_family(family, permutation):
    return frozenset(
        frozenset(permutation[point - 2] for point in block) for block in family
    )


def upper_cover():
    def shift(block, amount):
        return frozenset(((point - 1 + amount) % 13) + 1 for point in block)

    lines = {shift((1, 2, 4, 10), amount) for amount in range(13)}
    pair_counts = Counter(pair for line in lines for pair in combinations(line, 2))
    require(len(lines) == 13 and len(pair_counts) == 78, "bad plane development")
    require(set(pair_counts.values()) == {1}, "not a projective plane")
    cover = {left | right for left, right in combinations(lines, 2)}
    require(len(cover) == 78 and all(len(block) == 7 for block in cover), "bad line-union cover")
    histogram = Counter(
        sum(frozenset(target) <= block for block in cover)
        for target in combinations(range(1, 14), 5)
    )
    require(histogram == Counter({1: 1170, 4: 117}), "upper cover misses a five-set")
    return histogram


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("witness", type=Path)
    parser.add_argument("prior", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()

    source = read_blocks(args.source, 6, set(POINTS12))
    require(len(source) == 41, "wrong source-cover size")
    require(
        all(any(frozenset(target) <= frozenset(block) for block in source) for target in combinations(POINTS12, 4)),
        "source cover misses a quadruple",
    )
    second = tuple(tuple(point for point in block if point != 1) for block in source if 1 in block)
    require(len(second) == 20, "wrong second-link size")
    require(
        all(any(frozenset(target) <= frozenset(block) for block in second) for target in combinations(R, 3)),
        "second link misses a triple",
    )
    full_group = incidence_group(second)
    generated = generated_group(second)
    require(full_group == generated and len(full_group) == 240, "group mismatch")

    profiles = profile_orbits(full_group)
    certificate = json.loads(args.certificate.read_text(encoding="ascii"))
    require(certificate["format"] == "C1375-exact-78-farkas-v1", "bad certificate format")
    require(certificate["source_link_sha256"] == digest(args.source), "source hash mismatch")
    require(certificate["prior_witness_sha256"] == digest(args.witness), "witness hash mismatch")
    require(certificate["prior_certificate_sha256"] == digest(args.prior), "prior hash mismatch")
    candidates = tuple(combinations(R, 6))
    profile_metrics = []
    for orbit, case in enumerate(certificate["profile_cases"]):
        representative, orbit_size = profiles[orbit]
        require(case["orbit"] == orbit, "profile orbit index mismatch")
        require(case["representative"] == list(representative), "profile representative mismatch")
        require(case["orbit_size"] == orbit_size, "profile orbit size mismatch")
        profile_metrics.append(check_dual(case, 462, link_rows(second, representative, candidates)))
    require(len(profile_metrics) == 142, "wrong profile certificate count")
    survivor, survivor_size = profiles[142]
    require(survivor_size == 2 and sorted(survivor) == [0] * 5 + [1] * 6, "bad survivor")
    excluded_labeled = sum(size for _, size in profiles[:142])
    require(excluded_labeled == 8006, "wrong excluded labeled count")

    witness = read_blocks(args.witness, 6, set(R))
    witness_profile = verify_extension(second, witness)
    prior = json.loads(args.prior.read_text(encoding="ascii"))
    require(prior["format"] == "C1375-hard-e1-link-farkas-v1", "bad prior format")
    require(prior["source_link_sha256"] == digest(args.source), "prior source hash mismatch")
    require(prior["witness_sha256"] == digest(args.witness), "prior witness hash mismatch")
    candidate_index = {block: index for index, block in enumerate(candidates)}
    blocker = tuple(sorted(candidate_index[block] for block in witness))
    high_seen = set()
    prior_metrics = []
    for orbit, case in enumerate(prior["cases"]):
        high = tuple(case["high"])
        images = {
            frozenset(permutation[point - 2] for point in high)
            for permutation in full_group
        }
        require(not high_seen & images, "prior high-set orbit overlap")
        high_seen |= images
        require(case["orbit"] == orbit and case["high_orbit_size"] == len(images), "prior orbit metadata")
        blocked = orbit == 11
        require(case["known_blocker"] == blocked, "prior blocker metadata")
        profile = tuple(int(point in high) for point in R)
        prior_metrics.append(
            check_dual(case, 462, link_rows(second, profile, candidates, blocker if blocked else None))
        )
    require(len(prior_metrics) == 12 and len(high_seen) == 462, "incomplete prior orbit cover")
    require(tuple(point for point, value in zip(R, witness_profile) if value) == tuple(prior["cases"][11]["high"]), "witness high set mismatch")
    survivor_profiles = {image_profile(survivor, permutation) for permutation in full_group}
    require(witness_profile in survivor_profiles, "survivor does not transport to witness")

    source_extension = tuple(block for block in source if 1 not in block)
    verify_extension(second, source_extension)
    extension_orbit = {image_family(witness, permutation) for permutation in full_group}
    expected_extensions = {frozenset(map(frozenset, source_extension)), frozenset(map(frozenset, witness))}
    require(extension_orbit == expected_extensions, "extension orbit mismatch")
    stabilizers = sorted(
        sum(image_family(extension, permutation) == extension for permutation in full_group)
        for extension in expected_extensions
    )
    require(stabilizers == [120, 120], "extension stabilizer mismatch")

    canonical = (source_extension, witness)
    terminal_metrics = []
    residual_counts = []
    d_candidates = tuple(combinations(R, 7))
    require(len(certificate["completion_cases"]) == 2, "wrong terminal case count")
    for pair, case in zip(((0, 0), (0, 1)), certificate["completion_cases"]):
        require(tuple(case["pair"]) == pair, "terminal pair mismatch")
        rows, residual = completion_rows(second, canonical[pair[0]], canonical[pair[1]], d_candidates)
        require(case["residual_five_sets"] == residual, "terminal residual mismatch")
        residual_counts.append(residual)
        terminal_metrics.append(check_dual(case, 330, rows))
    histogram = upper_cover()

    print("cleanroom_incidence_and_dual_audit=PASS")
    print("source_blocks=41 second_link_blocks=20 quadruple_and_triple_coverage=PASS")
    print("full_automorphism_group=240 generated_group=240 groups_equal=true")
    print("profile_compositions=8008 profile_orbits=143 excluded_orbits=142 excluded_labeled=8006 survivor_orbit_size=2")
    print(
        f"profile_certificate_min_gap={min(row['gap'] for row in profile_metrics)} "
        f"support_range={min(row['support'] for row in profile_metrics)}:{max(row['support'] for row in profile_metrics)}"
    )
    print("prior_high_set_orbits=12 prior_certificates=12 extension_orbit=2 stabilizers=120,120")
    print(
        "terminal_residuals=" + ",".join(map(str, residual_counts))
        + " terminal_gaps=" + ",".join(str(row["gap"]) for row in terminal_metrics)
    )
    print("upper_cover_blocks=78 five_set_histogram=1:1170,4:117")
    print(f"certificate_sha256={digest(args.certificate)}")
    print("conclusion=C(13,7,5)=78")


if __name__ == "__main__":
    main()
