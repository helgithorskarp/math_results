#!/usr/bin/env python3
"""Complete exact H certificates for downsets on at most six elements.

Only the Python standard library is required. Family bit a represents the
subset whose element bits are set in a; element bits start at zero.
"""
import argparse
import hashlib
import json
from collections import Counter
from itertools import permutations, product
from math import comb, factorial, prod

from verify import EXCEPTION, check_partition, verify_exception


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask -= low


def labelled_downsets(n):
    """Split into lower/upper sections; upper is contained in lower."""
    result = [0, 1]
    for k in range(1, n + 1):
        shift = 1 << (k - 1)
        result = [lower | (upper << shift)
                  for lower in result for upper in result
                  if upper & ~lower == 0]
    return result


def subset_map(p):
    return [sum(1 << p[i] for i in range(len(p)) if a >> i & 1)
            for a in range(1 << len(p))]


def map_family(sets, transform):
    return sum(1 << transform[a] for a in sets)


def five_classes(n=5):
    """Full permutation orbits; this is also the small reference method."""
    transforms = [subset_map(p) for p in permutations(range(n))]
    unseen = set(labelled_downsets(n))
    classes = []
    while unseen:
        family = min(unseen)
        sets = list(bits(family))
        orbit = {map_family(sets, t) for t in transforms}
        if not orbit <= unseen:
            raise AssertionError("overlapping family orbits")
        unseen.difference_update(orbit)
        classes.append((family, len(orbit)))
    return classes


def profile_canonical(family, n):
    """Minimize after sorting the per-element rank-degree profiles.

    Equal-profile elements remain freely permutable. Every returned image
    is an actual relabeling; sorting profiles loses no isomorphism class.
    """
    sets = list(bits(family))
    groups = {}
    for i in range(n):
        signature = tuple(sum(a >> i & 1 for a in sets if a.bit_count() == k)
                          for k in range(1, n + 1))
        groups.setdefault(signature, []).append(i)
    blocks = [groups[k] for k in sorted(groups)]
    images = set()
    for choices in product(*(permutations(g) for g in blocks)):
        order = [i for block in choices for i in block]
        p = [order.index(i) for i in range(n)]
        images.add(map_family(sets, subset_map(p)))
    orbit = factorial(n) * len(images) // prod(factorial(len(g)) for g in blocks)
    return min(images), orbit


def six_classes():
    """All pairs (L,U) modulo S_5, then all their S_6 classes."""
    base = labelled_downsets(5)
    classes = {}
    pair_count = labelled_count = 0
    all_maps = [subset_map(p) for p in permutations(range(5))]
    for lower, lower_orbit in five_classes():
        lower_sets = list(bits(lower))
        automorphisms = [t for t in all_maps
                         if map_family(lower_sets, t) == lower]
        uppers = {upper for upper in base if upper & ~lower == 0}
        labelled_count += len(uppers) * lower_orbit
        while uppers:
            upper = min(uppers)
            upper_sets = list(bits(upper))
            upper_orbit = {map_family(upper_sets, t) for t in automorphisms}
            if not upper_orbit <= uppers:
                raise AssertionError("overlapping upper-section orbits")
            uppers.difference_update(upper_orbit)
            pair_count += 1
            family, orbit = profile_canonical(lower | (upper << 32), 6)
            if family in classes and classes[family] != orbit:
                raise AssertionError("inconsistent orbit multiplicity")
            classes[family] = orbit
    if sum(classes.values()) != labelled_count:
        raise AssertionError("labeled multiplicity reconstruction failed")
    return sorted(classes.items()), pair_count, labelled_count


def partition(family, n=6, node_limit=2_000_000):
    """Exact finite coloring with a maximum star anchored to all colors.

    A limit raises an exception and invalidates the run; it is never UNSAT.
    Only positive partitions enter the proof, except the analytic exception.
    """
    sets = [a for a in bits(family) if a]
    if not sets:
        return [], 0
    stars = [[j for j, a in enumerate(sets) if a >> i & 1] for i in range(n)]
    star = max(stars, key=lambda x: (len(x), tuple(x)))
    s = len(star)
    adjacency = [sum(1 << j for j, b in enumerate(sets) if i != j and a & b)
                 for i, a in enumerate(sets)]
    colors = [-1] * len(sets)
    allowed = [(1 << s) - 1] * len(sets)
    todo = (1 << len(sets)) - 1
    for color, i in enumerate(star):
        colors[i] = color
        todo ^= 1 << i
        for j in bits(adjacency[i]):
            allowed[j] &= ~(1 << color)
    nodes = 0

    def visit(remaining):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit:
            raise RuntimeError("INCOMPLETE: coloring node limit exceeded")
        if not remaining:
            return True
        i = min(bits(remaining),
                key=lambda j: (allowed[j].bit_count(),
                               -(adjacency[j] & remaining).bit_count(), j))
        for color in bits(allowed[i]):
            changed = []
            possible = True
            for j in bits(adjacency[i] & remaining):
                old = allowed[j]
                new = old & ~(1 << color)
                if new != old:
                    changed.append((j, old))
                    allowed[j] = new
                    if not new:
                        possible = False
            colors[i] = color
            if possible and visit(remaining ^ (1 << i)):
                return True
            for j, old in changed:
                allowed[j] = old
        colors[i] = -1
        return False

    if not visit(todo):
        return None, nodes
    bins = [[] for _ in range(s)]
    for a, color in zip(sets, colors):
        bins[color].append(a)
    return bins, nodes


def run():
    baseline = {str(n): {"classes": len(c), "labelled": sum(o for _, o in c)}
                for n in range(6) for c in [five_classes(n)]}
    expected = [(2, 2), (3, 3), (5, 6), (10, 20), (30, 168), (210, 7581)]
    if [(v["classes"], v["labelled"]) for v in baseline.values()] != expected:
        raise AssertionError("small census differs from primary baseline")
    classes, pairs, labelled = six_classes()
    if len(classes) != 16353 or labelled != 7828354:
        raise AssertionError("six-element census differs from primary baseline")
    census_hash = hashlib.sha256()
    witness_hash = hashlib.sha256()
    exceptions = []
    nontrivial_partition_count = trivial_count = max_nodes = 0
    histogram = Counter()
    size_histogram = Counter()
    labeled_family_sum = 0
    rank_bit_sums = [sum(1 << a for a in range(64) if a.bit_count() == k)
                     for k in range(7)]
    for family, orbit in classes:
        histogram[orbit] += 1
        size_histogram[family.bit_count()] += orbit
        for k in range(7):
            frequency_numerator = orbit * sum(a.bit_count() == k for a in bits(family))
            if frequency_numerator % comb(6, k):
                raise AssertionError("rank orbit frequency is nonintegral")
            labeled_family_sum += frequency_numerator // comb(6, k) * rank_bit_sums[k]
        census_hash.update(f"{family}:{orbit}\n".encode())
        if family == EXCEPTION:
            exceptions.append(family)
            continue
        bins, nodes = partition(family)
        max_nodes = max(max_nodes, nodes)
        if bins is None:
            raise AssertionError(f"unhandled exception: {family}")
        check_partition(family, bins, 6)
        if bins:
            nontrivial_partition_count += 1
        else:
            trivial_count += 1
        record = [family, bins]
        witness_hash.update((json.dumps(record, separators=(",", ":")) + "\n").encode())
    if exceptions != [EXCEPTION] or trivial_count != 2:
        raise AssertionError("exception or boundary coverage failed")
    exception_result = verify_exception()
    return {
        "agent": "six-downset-3", "role": "researcher",
        "claim_status": "exact computer-assisted finite theorem",
        "baseline": baseline, "ground_set_size": 6,
        "classes_including_trivial": len(classes),
        "labelled_downsets": labelled, "section_pair_orbits": pairs,
        "nontrivial_classes": len(classes) - trivial_count,
        "partition_certified_nontrivial_classes": nontrivial_partition_count,
        "partition_exception_family_masks": exceptions,
        "census_sha256": census_hash.hexdigest(),
        "partition_witness_stream_sha256": witness_hash.hexdigest(),
        "orbit_size_histogram": {str(k): v for k, v in sorted(histogram.items())},
        "labeled_size_histogram": {str(k): v for k, v in sorted(size_histogram.items())},
        "labeled_family_mask_sum": labeled_family_sum,
        "maximum_coloring_search_nodes": max_nodes,
        "exception": exception_result,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", help="compare every output field to compact expected JSON")
    args = parser.parse_args()
    result = run()
    if args.check:
        with open(args.check, encoding="utf-8") as handle:
            if result != json.load(handle):
                raise SystemExit("FAIL: expected result mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
