#!/usr/bin/env python3
"""Independent matching/enumeration check of the h=20 split closure."""

from hashlib import sha256
from itertools import combinations


CASES = (
    ("D20", 20, 7, (7, 8, 9, 10), 7, 87, 13),
    ("D19", 19, 8, (8,), 8, 75, 14),
)


def maximum_matching(lists, palette_size=26):
    """Return a maximum system of distinct representatives by augmenting paths."""
    owner = [-1] * palette_size

    def augment(vertex, seen):
        for colour in lists[vertex]:
            if colour in seen:
                continue
            seen.add(colour)
            if owner[colour] == -1 or augment(owner[colour], seen):
                owner[colour] = vertex
                return True
        return False

    return sum(augment(vertex, set()) for vertex in range(len(lists)))


def split_list_matching(block_order, active, chromatic):
    """Build both list types and solve the SDR problem for every split weight."""
    old_colour = 0
    fresh_colour = chromatic
    active_colours = set(range(active))
    palette = set(range(26))
    records = []
    for weight in range(1, block_order):
        lists = []
        for vertex in range(block_order):
            if vertex < weight:
                forbidden = (active_colours - {old_colour}) | {fresh_colour}
            else:
                forbidden = active_colours
            available = tuple(sorted(palette - forbidden))
            assert len(available) == block_order - 1
            lists.append(available)
        matching = maximum_matching(lists)
        assert matching == block_order
        records.append((weight, matching))
    return tuple(records)


def endpoint_enumeration(block_order, active, outside, high_edges):
    """Enumerate every labelled 0/full incidence vector with the fixed total."""
    target = block_order * active
    vectors = 0
    minimum_degree_sum = None
    digest_terms = []
    for full_vertices in combinations(range(20), active):
        full_set = set(full_vertices)
        weights = tuple(block_order if vertex in full_set else 0 for vertex in range(20))
        assert sum(weights) == target
        degree_sum = sum(active - 1 if weight else 27 - outside for weight in weights)
        minimum_degree_sum = (
            degree_sum if minimum_degree_sum is None else min(minimum_degree_sum, degree_sum)
        )
        digest_terms.append((full_vertices, degree_sum))
        vectors += 1
    assert minimum_degree_sum is not None
    assert minimum_degree_sum > 2 * high_edges
    return vectors, minimum_degree_sum, sha256(repr(digest_terms).encode()).hexdigest()


def main():
    records = []
    for name, b, active, chromatic_values, small_chi, high_edges, outside in CASES:
        matchings = []
        for chromatic in chromatic_values:
            assert 26 - (chromatic + 1) >= small_chi
            matchings.append((chromatic, split_list_matching(b, active, chromatic)))
        vectors, degree_floor, vector_hash = endpoint_enumeration(
            b, active, outside, high_edges
        )
        records.append(
            (name, b, active, tuple(matchings), vectors, degree_floor, 2 * high_edges, vector_hash)
        )

    records = tuple(records)
    assert tuple((row[0], row[4], row[5], row[6]) for row in records) == (
        ("D20", 77520, 224, 174),
        ("D19", 125970, 212, 150),
    )
    print("PASS independent Albertson r=27 h=20 split-colour check")
    for row in records:
        print(
            f"{row[0]}: matching_instances={sum(len(x[1]) for x in row[3])}; "
            f"endpoint_vectors={row[4]}; degree_floor={row[5]}; handshake={row[6]}; "
            f"vectors_sha256={row[7]}"
        )
    print(f"certificate_sha256={sha256(repr(records).encode()).hexdigest()}")


if __name__ == "__main__":
    main()
