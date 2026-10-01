#!/usr/bin/env python3
"""Exact author controls of EIGHTEEN.md; Python3.11+, standard library.

Actual author six-books-2, role researcher. Written identities provide
universal sign/inside coverage. These controls are validation, not a new
enumeration premise or independent peer review. No campaign imports.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path
from random import Random

PAIRS = tuple(combinations(range(11), 2))
ALL_VERTICES = (1 << 22) - 1


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def neighbors(edges):
    return tuple(frozenset(j if i == v else i for i, j in edges if v in (i, j))
                 for v in range(11))


def lift(red, blue, inside=0, sign_word=0):
    """Literal22-vertex graph. Bit1 on a matching block means crossed red."""
    require(not (red & blue), "red and blue uniform blocks must be disjoint")
    rows = [0] * 22
    for index, (i, j) in enumerate(PAIRS):
        crossed = (sign_word >> index) & 1
        for x, y in product(range(2), repeat=2):
            if (i, j) in red or ((i, j) not in blue and (x ^ y) == crossed):
                rows[2 * i + x] |= 1 << (2 * j + y)
                rows[2 * j + y] |= 1 << (2 * i + x)
    for i in range(11):
        if (inside >> i) & 1:
            rows[2 * i] |= 1 << (2 * i + 1)
            rows[2 * i + 1] |= 1 << (2 * i)
    opposite = [ALL_VERTICES ^ (1 << v) ^ row for v, row in enumerate(rows)]
    return rows, opposite


def matching_combined(rows, opposite, i, j):
    red_bit = 0 if (rows[2 * i] >> (2 * j)) & 1 else 1
    return ((rows[2 * i] & rows[2 * j + red_bit]).bit_count()
            + (opposite[2 * i] & opposite[2 * j + 1 - red_bit]).bit_count())


def uniform_sum(rows, i, j):
    return sum((rows[2 * i] & rows[2 * j + bit]).bit_count() for bit in range(2))


def leaf_parts(remaining):
    """Every partial matching, with the unpaired vertices listed separately."""
    if not remaining:
        yield (), ()
        return
    first, tail = remaining[0], remaining[1:]
    for edges, singles in leaf_parts(tail):
        yield edges, (first,) + singles
    for index, partner in enumerate(tail):
        for edges, singles in leaf_parts(tail[:index] + tail[index + 1:]):
            yield ((first, partner),) + edges, singles


def path_blue_graphs(red, forced):
    """All degree2 on0..4/degree1 on5..10 D graphs disjoint from fixed R.

    Forced D edges occupy whole leaf degrees. Every unused blue leaf is
    either paired with another unused leaf or attached to exactly one core
    vertex. Every remaining core graph is a binary word on its free edges.
    """
    free_core = [e for e in combinations(range(5), 2) if e not in red]
    cores = {}
    for bits in product(range(2), repeat=len(free_core)):
        edges = tuple(e for e, bit in zip(free_core, bits) if bit)
        degrees = tuple(sum(i in e for e in edges) for i in range(5))
        cores.setdefault(degrees, []).append(edges)
    occupied = {v for e in forced for v in e}
    leaves = tuple(v for v in range(5, 11) if v not in occupied)
    for leaf_edges, singles in leaf_parts(leaves):
        for parents in product(range(5), repeat=len(singles)):
            attached = [(parent, leaf) for leaf, parent in zip(singles, parents)]
            if any(e in red for e in attached):
                continue
            needed = tuple(2 - parents.count(i) for i in range(5))
            for core_edges in cores.get(needed, []):
                yield frozenset(forced | set(leaf_edges) | set(attached) | set(core_edges))


def path_rejection(red, blue):
    blue_neighbors = neighbors(blue)
    if any(len(row & set(range(5, 11))) > 1 for row in blue_neighbors):
        return "shared_blue_leaves", None
    rows, opposite = lift(red, blue)
    require(all(row.bit_count() == 10 for row in rows), "path lift must be ten-regular")
    for i, j in PAIRS:
        if (i, j) not in red and (i, j) not in blue:
            actual = matching_combined(rows, opposite, i, j)
            if actual > 9:
                return "matching_square", [i, j, actual - 9]
    for i, j in sorted(red):
        actual = uniform_sum(rows, i, j)
        if actual > 6:
            return "red_uniform", [i, j, actual]
    for i, j in sorted(blue):
        actual = uniform_sum(opposite, i, j)
        if actual > 12:
            return "blue_uniform", [i, j, actual]
    return "surviving_necessary_quotient", None


def path_controls():
    cases = [
        ("P5_2P3", {(0, 1), (1, 2), (0, 5), (2, 6), (3, 7), (3, 8), (4, 9), (4, 10)},
         {(7, 8), (9, 10)}),
        ("2P4_P3", {(0, 1), (2, 3), (0, 5), (1, 6), (2, 7), (3, 8), (4, 9), (4, 10)},
         {(9, 10)})]
    output = []
    for name, red, forced in cases:
        records = []
        for blue in path_blue_graphs(red, forced):
            require(not (red & blue) and forced <= blue, "D block constraints")
            require([len(n) for n in neighbors(blue)] == [2] * 5 + [1] * 6, "D degrees")
            why, obstruction = path_rejection(red, blue)
            require(why != "surviving_necessary_quotient", "path unsigned survivor")
            records.append({"blue_mask": sum(1 << i for i, e in enumerate(PAIRS) if e in blue),
                            "rejection": why, "obstruction": obstruction})
        records.sort(key=lambda row: row["blue_mask"])
        require(len({r["blue_mask"] for r in records}) == len(records), "duplicate D graph")
        output.append({"name": name, "domain": len(records),
                       "literal_first_failure_counts": dict(Counter(r["rejection"] for r in records)),
                       "record_sha256": digest(records)})
    return output


def degree_profiles(total_degree):
    return [p for p in combinations_with_replacement(range(1, 4), 11) if sum(p) == total_degree]


def red_core_graphs(profile):
    """Whole nonleaf core words; attach indistinguishable leaves in order.

    Every R leaf has a nonleaf parent by the proved transfer lemma. For a
    fixed core its labeled attachments differ only by a leaf permutation.
    Controls use one attachment representative, not all labeled hosts.
    """
    core_degrees = tuple(sorted((d for d in profile if d > 1), reverse=True))
    m = len(core_degrees)
    edge_count = sum(profile) // 2 - profile.count(1)
    for core_edges in combinations(tuple(combinations(range(m), 2)), edge_count):
        current = [sum(i in e for e in core_edges) for i in range(m)]
        if any(current[i] > core_degrees[i] for i in range(m)):
            continue
        red = set(core_edges)
        leaf = m
        for i in range(m):
            for _ in range(core_degrees[i] - current[i]):
                red.add((i, leaf))
                leaf += 1
        require(leaf == 11 and len(red) == 8, "red core/leaf reconstruction")
        actual = sorted(len(n) for n in neighbors(red))
        require(actual == list(profile), "R profile reconstruction")
        yield frozenset(red), m


def red_type(red, m):
    nr = neighbors(red)
    trivalent = [i for i in range(m) if len(nr[i]) == 3]
    if len(trivalent) == 2:
        return "two_trivalent_stars"
    if len(trivalent) == 1:
        return ("one_trivalent_incident" if nr[trivalent[0]] & set(range(m))
                else "one_trivalent_nonincident")
    core_degree = [len(nr[i] & set(range(m))) for i in range(m)]
    return "P5_2P3" if max(core_degree) == 2 else "2P4_P3"


def blue_completions(red, nr, inside):
    """Every D with regular degrees and necessary leaf/sibling constraints.

    Edges are enumerated by whole remaining degree stars, independently
    of the partial-matching/core-bit generator used for the path census.
    """
    degree = [len(nr[i]) + ((inside >> i) & 1) for i in range(11)]
    allowed_leaf = {}
    forced = set()
    for i in range(11):
        leaves = sorted(j for j in nr[i] if len(nr[j]) == 1)
        forced.update(combinations(leaves, 2))
        if len(nr[i]) == 1:
            parent = next(iter(nr[i]))
            allowed_leaf[i] = nr[parent] - {i}
    allowed = set()
    for i, j in PAIRS:
        if (i, j) in red:
            continue
        if i in allowed_leaf and j not in allowed_leaf[i]:
            continue
        if j in allowed_leaf and i not in allowed_leaf[j]:
            continue
        allowed.add((i, j))
    if not forced <= allowed:
        return
    residual = [degree[i] - sum(i in e for e in forced) for i in range(11)]
    if any(d < 0 for d in residual):
        return
    free = allowed - forced

    def visit(i, remaining, edges):
        while i < 11 and not remaining[i]:
            i += 1
        if i == 11:
            yield frozenset(forced | edges)
            return
        candidates = [j for j in range(i + 1, 11)
                      if remaining[j] > 0 and (i, j) in free]
        for selected in combinations(candidates, remaining[i]):
            after = remaining[:]
            after[i] = 0
            for j in selected:
                after[j] -= 1
            # At this boundary all labels<=i are saturated. Count all
            # still-active neighbors, both earlier/later than each j.
            possible = all(after[j] <= sum(after[k] > 0 and
                           (min(j, k), max(j, k)) in free
                           for k in range(i + 1, 11) if k != j)
                           for j in range(i + 1, 11))
            if possible:
                yield from visit(i + 1, after, edges | {(i, j) for j in selected})

    yield from visit(0, residual, set())


def red_core_controls():
    profiles = degree_profiles(16)
    cores = Counter()
    eligible = Counter()
    completions = Counter()
    records = []
    inside_words = 0
    literal_lifts = 0
    rng = Random(2026100118)
    signs = [0, (1 << 55) - 1] + [rng.getrandbits(55) for _ in range(6)]
    for profile in profiles:
        for red, m in red_core_graphs(profile):
            name = red_type(red, m)
            cores[name] += 1
            nr = neighbors(red)
            permitted = {i for i in range(m, 11)
                         if len(nr[next(iter(nr[i]))]) == 3}
            for inside in range(1 << 11):
                inside_words += 1
                flagged = {i for i in range(11) if (inside >> i) & 1}
                if len(flagged) % 2 or not flagged <= permitted:
                    continue
                eligible[name] += 1
                seen = set()
                for blue in blue_completions(red, nr, inside):
                    mask = sum(1 << i for i, e in enumerate(PAIRS) if e in blue)
                    require(mask not in seen, "duplicate transfer-constrained D")
                    seen.add(mask)
                    completions[name] += 1
                    wanted = [len(nr[i]) + ((inside >> i) & 1) for i in range(11)]
                    require([len(n) for n in neighbors(blue)] == wanted, "regular D degrees")
                    require(not (red & blue), "uniform blocks disjoint")
                    base_pair = None
                    base_count = None
                    for sign_word in signs:
                        rows, opposite = lift(red, blue, inside, sign_word)
                        literal_lifts += 1
                        require(all(row.bit_count() == 10 for row in rows), "regular degree literal")
                        if base_pair is None:
                            for i, j in PAIRS:
                                if (i, j) in red or (i, j) in blue:
                                    continue
                                actual = matching_combined(rows, opposite, i, j)
                                if actual > 9:
                                    base_pair, base_count = (i, j), actual
                                    break
                        require(base_pair is not None, "remaining unsigned R8 quotient")
                        require(matching_combined(rows, opposite, *base_pair) == base_count,
                                "matching obstruction must be sign independent")
                    records.append({"type": name, "red": sorted(red), "inside": inside,
                                    "blue_mask": mask, "matching_pair": base_pair,
                                    "combined_pages": base_count})
    records.sort(key=lambda r: (r["red"], r["inside"], r["blue_mask"]))
    return {"R8_profiles": [list(p) for p in profiles], "normalized_core_words": dict(cores),
            "literal_inside_words": inside_words, "eligible_inside_words": dict(eligible),
            "transfer_constrained_D_completions": dict(completions),
            "every_D_completion_has_literal_matching_obstruction": True,
            "literal_lifts": literal_lifts, "sign_words_per_completion": len(signs),
            "obstruction_record_sha256": digest(records),
            "R9_equality_profiles": [list(p) for p in degree_profiles(18)]}


def local_transfer_controls():
    total = 0
    survivors = []
    for leaf_flag, parent_flag in product(range(2), repeat=2):
        for terms in product((-1, 0, 1), repeat=1 + leaf_flag):
            total += 1
            if sum(terms) >= 1 + leaf_flag + parent_flag:
                require(parent_flag == 0 and all(t == 1 for t in terms), "leaf transfer algebra")
                survivors.append({"leaf_flag": leaf_flag, "parent_flag": parent_flag,
                                  "terms": list(terms)})
    return {"all_term_and_flag_words": total, "surviving_words": survivors}


def identities_controls():
    rng = Random(220418)
    cases = []
    # Disjoint Hamilton cycles have r_i=b_i=2 and all-blue inside gives
    # an actually regular lift. Its signs are still arbitrary.
    red = {tuple(sorted((i, (i + 1) % 11))) for i in range(11)}
    blue = {tuple(sorted((i, (i + 2) % 11))) for i in range(11)}
    for inside in (0, (1 << 11) - 1, 0b10101010101):
        for _ in range(8):
            cases.append((red, blue, inside, rng.getrandbits(55)))
    for _ in range(48):
        codes = [rng.randrange(3) for _ in PAIRS]
        cases.append(({e for e, code in zip(PAIRS, codes) if code == 1},
                      {e for e, code in zip(PAIRS, codes) if code == 2},
                      rng.getrandbits(11), rng.getrandbits(55)))
    counts = Counter()
    for red, blue, inside, sign_word in cases:
        rows, opposite = lift(red, blue, inside, sign_word)
        nr, nd = neighbors(red), neighbors(blue)
        w = [[int(j in nr[i]) - int(j in nd[i]) for j in range(11)] for i in range(11)]
        u = [sum(row) for row in w]
        flags = [(inside >> i) & 1 for i in range(11)]
        regular = all(rows[2 * i].bit_count() == 10 for i in range(11))
        counts["literal_lifts"] += 1
        counts["regular_lifts"] += regular
        for i in range(11):
            for x in range(2):
                require(rows[2 * i + x].bit_count() == 10 + u[i] + flags[i], "degree identity")
                counts["literal_degrees"] += 1
            page_rows = rows if flags[i] else opposite
            actual = (page_rows[2 * i] & page_rows[2 * i + 1]).bit_count()
            require(actual == 2 * len(nr[i] if flags[i] else nd[i]), "inside pages")
            counts["inside_page_identities"] += 1
        for i, j in PAIRS:
            square = sum(w[i][k] * w[k][j] for k in range(11))
            if (i, j) in red:
                actual = uniform_sum(rows, i, j)
                require(actual == 7 + u[i] + u[j] + square + 2 * (flags[i] + flags[j]),
                        "general uniform red sum")
                counts["uniform_red_sums"] += 1
                if regular:
                    require(actual == 7 + square + flags[i] + flags[j], "regular uniform red sum")
                    counts["regular_uniform_red_sums"] += 1
            elif (i, j) in blue:
                actual = uniform_sum(opposite, i, j)
                require(actual == 11 - u[i] - u[j] + square - 2 * (flags[i] + flags[j]),
                        "general uniform blue sum")
                counts["uniform_blue_sums"] += 1
            else:
                require(matching_combined(rows, opposite, i, j) == 9 + square, "matching sum")
                counts["matching_page_identities"] += 1
    return dict(counts)


def run():
    return {"agent": "six-books-2", "role": "researcher", "complete": True,
            "proof_is_written_not_new_enumeration_premise": True,
            "imported_regular_positive_codegree_computation_not_replayed": True,
            "threads": 1, "local_jobs": 1,
            "local_leaf_transfer": local_transfer_controls(),
            "regular_R8_core_and_inside_audit": red_core_controls(),
            "unsigned_path_census_literal": path_controls(),
            "literal_identities": identities_controls()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("eighteen_expected.json"))
    parser.add_argument("--emit", action="store_true", help="print author output without fixture comparison")
    args = parser.parse_args()
    result = run()
    if not args.emit:
        expected = json.loads(args.expected.read_text())
        require(result == expected, "computed controls differ from the expected fixture")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
