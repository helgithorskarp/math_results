#!/usr/bin/env python3
"""Independent exact checks for the even-uniform AHT arithmetic gap.

CPython 3.11+, standard library only.  This file imports no target code or
output.  It audits the folded-cube character calculation, Catalan residues,
integer core-count alternatives, Steiner divisibility obstruction, the odd
rank boundary case, and the complete 23-edge r=4 endpoint.

The universal theorem remains the human counting proof reviewed separately.
"""

from hashlib import sha256
from itertools import combinations
from math import comb
import argparse
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_power_of_two(value):
    return value > 0 and value & (value - 1) == 0


def catalan(index):
    return comb(2 * index, index) // (index + 1)


def explicit_independent_set(rank):
    middle = rank // 2
    return frozenset(
        word for word in range(1 << rank)
        if ((word.bit_count() < middle and word.bit_count() % 2 == 0)
            or (word.bit_count() > middle and word.bit_count() % 2 == 1))
    )


def folded_neighbors(word, rank):
    for coordinate in range(rank):
        yield word ^ (1 << coordinate)
    yield word ^ ((1 << rank) - 1)


def audit_explicit_independent_set(rank):
    independent = explicit_independent_set(rank)
    for word in independent:
        require(all(neighbor not in independent
                    for neighbor in folded_neighbors(word, rank)),
                ("claimed folded-cube set is not independent", rank, word))
    expected = (1 << (rank - 1)) - comb(rank, rank // 2) // 2
    require(len(independent) == expected,
            ("folded-cube independent-set size mismatch", rank))
    return len(independent)


def brute_independence_number(rank):
    """Definition-level exhaustive check, used only for F_4 (16 vertices)."""
    order = 1 << rank
    adjacency = []
    for vertex in range(order):
        mask = 0
        for neighbor in folded_neighbors(vertex, rank):
            mask |= 1 << neighbor
        adjacency.append(mask)
    maximum = 0
    witnesses = 0
    for subset in range(1 << order):
        size = subset.bit_count()
        if size < maximum:
            continue
        remaining = subset
        valid = True
        while remaining:
            bit = remaining & -remaining
            vertex = bit.bit_length() - 1
            remaining ^= bit
            if adjacency[vertex] & remaining:
                valid = False
                break
        if valid and size > maximum:
            maximum = size
            witnesses = 1
        elif valid and size == maximum:
            witnesses += 1
    return maximum, witnesses


def folded_spectrum(rank):
    positive = negative = zero = 0
    eigenvalues = []
    for weight in range(rank + 1):
        eigenvalue = rank - 2 * weight + (-1) ** weight
        multiplicity = comb(rank, weight)
        eigenvalues.append((weight, eigenvalue, multiplicity))
        if eigenvalue > 0:
            positive += multiplicity
        elif eigenvalue < 0:
            negative += multiplicity
        else:
            zero += multiplicity
    return positive, negative, zero, tuple(eigenvalues)


def pair_inequality_profile(rank, total_sets):
    """Audit the target's minimum-coordinate dichotomy and equality profile."""
    quotient, remainder = divmod(total_sets, rank)
    if remainder:
        require(remainder == rank // 2 and is_power_of_two(rank),
                "unexpected Catalan residue")
        constant = quotient + 1
        require(rank * constant == total_sets + rank // 2,
                "power-of-two profile total")
        require(constant + (rank - 1) * constant >= total_sets,
                "constant profile violates pair inequalities")
        low_minimum_bound = (quotient + (rank - 1)
                             * (total_sets - (rank - 1) * quotient))
        require(low_minimum_bound >= total_sets + rank * (rank - 2) // 2,
                "minimum-coordinate lower bound mismatch")
        return total_sets + rank // 2, tuple([constant] * rank)

    require(rank * quotient == total_sets, "divisible profile total")
    require(quotient + (rank - 1) * quotient == total_sets,
            "constant equality profile violates pair inequalities")
    # If the forbidden equality is increased by exactly one, a minimum below
    # q would force a jump of at least r(r-2), so the only possible profile is
    # one q+1 and r-1 copies of q.
    low_minimum_bound = ((quotient - 1) + (rank - 1)
                         * (total_sets - (rank - 1) * (quotient - 1)))
    require(low_minimum_bound >= total_sets + rank * (rank - 2),
            "non-power minimum-coordinate lower bound mismatch")
    near_profile = tuple(sorted([quotient + 1] + [quotient] * (rank - 1)))
    require(sum(near_profile) == total_sets + 1, "near-equality profile total")
    require(all(near_profile[i] + (rank - 1) * near_profile[j] >= total_sets
                for i in range(rank) for j in range(rank) if i != j),
            "near-equality profile violates pair inequalities")
    return total_sets + 1, near_profile


def audit_rank(rank, explicit_limit):
    require(rank >= 4 and rank % 2 == 0, "rank must be even and at least four")
    core_size = comb(2 * rank - 3, rank - 2)
    cat = catalan(rank - 1)
    require(core_size == rank * cat // 2, "Catalan identity failed")
    expected_remainder = rank // 2 if is_power_of_two(rank) else 0
    require(core_size % rank == expected_remainder, "Catalan residue failed")
    require((cat % 2 == 1) == is_power_of_two(rank), "Catalan parity failed")

    positive, negative, zero, eigenvalues = folded_spectrum(rank)
    require(zero == 0 and positive + negative == 1 << rank,
            "folded-cube inertia partition failed")
    smaller = min(positive, negative)
    alpha = (1 << (rank - 1)) - comb(rank, rank // 2) // 2
    cover = (1 << rank) - alpha
    require(smaller == alpha, "inertia count does not match construction")
    require(cover == ((1 << (rank - 1))
                      + comb(rank, rank // 2) // 2),
            "folded-cube cover formula failed")
    require(all(value != 0 for _, value, _ in eigenvalues),
            "unexpected zero eigenvalue")

    explicit_size = None
    if rank <= explicit_limit:
        explicit_size = audit_explicit_independent_set(rank)
        require(explicit_size == alpha, "explicit independent-set mismatch")

    core_bound, equality_profile = pair_inequality_profile(rank, core_size)
    if is_power_of_two(rank):
        epsilon = rank // 2
        replication = None
    else:
        epsilon = 1
        k = rank - 2
        replication = (k + 3, 2)
        require(replication[0] % replication[1] != 0,
                "Steiner replication unexpectedly integral")
    require(core_bound == core_size + epsilon, "core gap mismatch")

    return {
        "rank": rank,
        "M": core_size,
        "Catalan": cat,
        "M_mod_r": core_size % rank,
        "inertia": [positive, negative, zero],
        "alpha": alpha,
        "tau": cover,
        "epsilon": epsilon,
        "core_bound": core_bound,
        "equality_profile": list(equality_profile),
        "Steiner_replication_numerator_denominator": (
            list(replication) if replication else None),
        "explicit_independent_size": explicit_size,
    }


def fano_odd_boundary_control():
    blocks = (
        (0, 1, 3), (0, 2, 5), (0, 4, 6), (1, 2, 4),
        (1, 5, 6), (2, 3, 6), (3, 4, 5),
    )
    pair_counts = {pair: 0 for pair in combinations(range(7), 2)}
    for block in blocks:
        for pair in combinations(block, 2):
            pair_counts[tuple(sorted(pair))] += 1
    require(set(pair_counts.values()) == {1}, "Fano pair coverage failed")
    require(all(set(left) & set(right) for left, right in combinations(blocks, 2)),
            "Fano blocks are not intersecting")
    require(5 * len(blocks) == comb(7, 3), "odd-rank equality count failed")
    return {"rank": 5, "blocks": len(blocks), "core_sum": 5 * len(blocks)}


def endpoint_r4():
    rank = 4
    core_vertices = tuple(range(5))
    pairs = tuple((5 + 2 * index, 6 + 2 * index) for index in range(rank))
    triangle = ((0, 1), (0, 2), (1, 2))
    core_edges = [tuple(sorted(core + pairs[index]))
                  for index in range(rank) for core in triangle]

    independent = explicit_independent_set(rank)
    transversal_words = [word for word in range(1 << rank)
                          if word not in independent]
    transversal_edges = []
    for word in transversal_words:
        edge = tuple(pairs[index][(word >> index) & 1] for index in range(rank))
        transversal_edges.append(tuple(sorted(edge)))
    edges = tuple(core_edges + transversal_edges)
    require(len(edges) == len(set(edges)) == 23, "r=4 edge count or uniqueness")
    require(all(len(edge) == rank for edge in edges), "r=4 nonuniform edge")
    require(set(core_vertices).isdisjoint(set().union(*map(set, pairs))),
            "core and outer vertices overlap")

    vertex_count = 5 + 2 * rank
    proper = []
    for coloring in range(1 << vertex_count):
        if all(not (all((coloring >> vertex) & 1 for vertex in edge)
                       or all(not ((coloring >> vertex) & 1) for vertex in edge))
               for edge in edges):
            proper.append(coloring)
    require(not proper, "23-edge endpoint has a proper coloring")

    maximum, maximum_witnesses = brute_independence_number(rank)
    require(maximum == 5 and (1 << rank) - maximum == 11,
            "definition-level F4 cover check failed")
    return {
        "vertices": vertex_count,
        "edges": len(edges),
        "colorings_checked": 1 << vertex_count,
        "proper_colorings": len(proper),
        "F4_alpha": maximum,
        "F4_maximum_independent_sets": maximum_witnesses,
        "F4_tau": (1 << rank) - maximum,
    }


def run(max_rank, explicit_limit):
    require(max_rank >= 4 and max_rank % 2 == 0, "invalid maximum rank")
    require(explicit_limit >= 4 and explicit_limit % 2 == 0,
            "invalid explicit limit")
    records = [audit_rank(rank, explicit_limit)
               for rank in range(4, max_rank + 1, 2)]
    digest = sha256()
    for record in records:
        digest.update((json.dumps(record, sort_keys=True) + "\n").encode())
    return {
        "schema": 1,
        "max_rank": max_rank,
        "explicit_limit": explicit_limit,
        "even_ranks_checked": len(records),
        "explicit_folded_cube_vertices_checked": sum(
            1 << rank for rank in range(4, min(max_rank, explicit_limit) + 1, 2)),
        "rank_record_sha256": digest.hexdigest(),
        "selected_rank_records": records[:4],
        "last_rank_summary": {
            key: records[-1][key]
            for key in ("rank", "M", "M_mod_r", "alpha", "tau",
                        "epsilon", "core_bound")
        },
        "odd_boundary_control": fano_odd_boundary_control(),
        "endpoint_r4": endpoint_r4(),
        "trust_boundary": (
            "Finite exact corroboration; the all-even-rank theorem is the "
            "human counting, inertia, Catalan, and design-divisibility proof."),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-rank", type=int, default=64)
    parser.add_argument("--explicit-limit", type=int, default=14)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    require((args.max_rank, args.explicit_limit) == (64, 14),
            "frozen audit requires default limits")
    result = run(args.max_rank, args.explicit_limit)
    if args.emit:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    expected_path = Path(__file__).with_name("expected.json")
    expected = json.loads(expected_path.read_text())
    require(result == expected, "frozen expected output mismatch")
    print(json.dumps({
        "status": "PASS",
        "even_ranks_checked": result["even_ranks_checked"],
        "rank_record_sha256": result["rank_record_sha256"],
        "expected_sha256": sha256(expected_path.read_bytes()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
