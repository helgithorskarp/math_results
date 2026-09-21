#!/usr/bin/env python3
"""Definition-level audit of linear-extension independence on poset modules."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from functools import cache
from itertools import combinations, permutations, product


Order = tuple[int, ...]
Word = tuple[int, ...]


def require(condition: bool, message: str = "exact check failed") -> None:
    if not condition:
        raise AssertionError(message)


def relation_from_pair_mask(n: int, mask: int) -> Order:
    """Strict relation with possible pairs i<j encoded lexicographically."""
    rows = [0] * n
    bit = 0
    for i in range(n):
        for j in range(i + 1, n):
            if mask >> bit & 1:
                rows[i] |= 1 << j
            bit += 1
    return tuple(rows)


def is_transitive(order: Order) -> bool:
    for i, successors in enumerate(order):
        bits = successors
        while bits:
            low = bits & -bits
            j = low.bit_length() - 1
            if order[j] & ~successors:
                return False
            bits ^= low
    return True


def naturally_labeled_posets(n: int):
    for mask in range(1 << (n * (n - 1) // 2)):
        order = relation_from_pair_mask(n, mask)
        if is_transitive(order):
            yield order


@cache
def extensions_on(order: Order, subset_mask: int) -> tuple[Word, ...]:
    """All linear extensions of the subposet induced by subset_mask."""
    elements = tuple(i for i in range(len(order)) if subset_mask >> i & 1)
    result = []
    for word in permutations(elements):
        position = {value: index for index, value in enumerate(word)}
        if all(
            position[i] < position[j]
            for i in elements
            for j in elements
            if order[i] >> j & 1
        ):
            result.append(word)
    return tuple(result)


def relation_type(order: Order, x: int, y: int) -> int:
    """Return -1 for x<y, +1 for y<x, and 0 for incomparability."""
    if order[x] >> y & 1:
        return -1
    if order[y] >> x & 1:
        return 1
    return 0


def is_module(order: Order, subset_mask: int) -> bool:
    inside = tuple(i for i in range(len(order)) if subset_mask >> i & 1)
    outside = tuple(i for i in range(len(order)) if not (subset_mask >> i & 1))
    if not inside:
        return False
    return all(
        len({relation_type(order, z, a) for a in inside}) == 1
        for z in outside
    )


def restrict_word(word: Word, subset_mask: int) -> Word:
    return tuple(value for value in word if subset_mask >> value & 1)


def audit_modules(max_n: int) -> dict[str, int]:
    posets = 0
    global_extensions = 0
    modules = 0
    proper_nontrivial_modules = 0
    restriction_fibres = 0

    for n in range(1, max_n + 1):
        whole = (1 << n) - 1
        for order in naturally_labeled_posets(n):
            posets += 1
            global_words = extensions_on(order, whole)
            global_extensions += len(global_words)
            for subset_mask in range(1, whole + 1):
                if not is_module(order, subset_mask):
                    continue
                modules += 1
                if subset_mask != whole and subset_mask.bit_count() >= 2:
                    proper_nontrivial_modules += 1
                internal_words = extensions_on(order, subset_mask)
                fibres = Counter(restrict_word(word, subset_mask) for word in global_words)
                require(set(fibres) == set(internal_words), "restriction is not onto")
                require(len(set(fibres.values())) == 1, "module fibres have unequal size")
                common = next(iter(fibres.values()))
                require(common * len(internal_words) == len(global_words))
                restriction_fibres += len(internal_words)

    return {
        "naturally_labeled_posets": posets,
        "global_linear_extensions": global_extensions,
        "autonomous_subsets": modules,
        "proper_nontrivial_autonomous_subsets": proper_nontrivial_modules,
        "restriction_fibres": restriction_fibres,
    }


def lexicographic_sum(skeleton: Order, blocks: tuple[Order, ...]) -> tuple[Order, tuple[tuple[int, ...], ...]]:
    require(len(skeleton) == len(blocks))
    offsets = []
    total = 0
    for block in blocks:
        offsets.append(total)
        total += len(block)
    block_vertices = tuple(
        tuple(offsets[s] + i for i in range(len(blocks[s])))
        for s in range(len(blocks))
    )
    rows = [0] * total
    for s, block in enumerate(blocks):
        offset = offsets[s]
        for i, successors in enumerate(block):
            bits = successors
            while bits:
                low = bits & -bits
                j = low.bit_length() - 1
                rows[offset + i] |= 1 << (offset + j)
                bits ^= low
    for s in range(len(blocks)):
        for t in range(len(blocks)):
            if skeleton[s] >> t & 1:
                target = sum(1 << vertex for vertex in block_vertices[t])
                for vertex in block_vertices[s]:
                    rows[vertex] |= target
    return tuple(rows), block_vertices


def admissible_block_words(skeleton: Order, sizes: tuple[int, ...]) -> tuple[Word, ...]:
    letters = tuple(s for s, size in enumerate(sizes) for _ in range(size))
    words = set(permutations(letters))
    result = []
    for word in words:
        positions = {
            s: tuple(i for i, letter in enumerate(word) if letter == s)
            for s in range(len(sizes))
        }
        if all(
            max(positions[s]) < min(positions[t])
            for s in range(len(sizes))
            for t in range(len(sizes))
            if skeleton[s] >> t & 1
        ):
            result.append(word)
    return tuple(sorted(result))


def block_coordinates(word: Word, block_vertices: tuple[tuple[int, ...], ...]) -> tuple[Word, tuple[Word, ...]]:
    owner = {}
    local = {}
    for block_index, vertices in enumerate(block_vertices):
        for local_index, vertex in enumerate(vertices):
            owner[vertex] = block_index
            local[vertex] = local_index
    block_word = tuple(owner[vertex] for vertex in word)
    internals = tuple(
        tuple(local[vertex] for vertex in word if owner[vertex] == block_index)
        for block_index in range(len(block_vertices))
    )
    return block_word, internals


def audit_joint_products() -> dict[str, int]:
    """Audit the simultaneous product bijection on a diverse exact family."""
    skeletons = tuple(
        order
        for n in range(1, 4)
        for order in naturally_labeled_posets(n)
    )
    small_blocks = {
        n: tuple(naturally_labeled_posets(n))
        for n in range(1, 4)
    }
    instances = 0
    global_words_checked = 0
    coordinate_tuples_checked = 0

    for skeleton in skeletons:
        k = len(skeleton)
        for sizes in product(range(1, 4), repeat=k):
            if sum(sizes) > 7:
                continue
            for blocks in product(*(small_blocks[size] for size in sizes)):
                summed, block_vertices = lexicographic_sum(skeleton, blocks)
                global_words = extensions_on(summed, (1 << len(summed)) - 1)
                coordinates = Counter(
                    block_coordinates(word, block_vertices) for word in global_words
                )
                block_words = admissible_block_words(skeleton, sizes)
                internal_products = tuple(
                    product(*(
                        extensions_on(block, (1 << len(block)) - 1)
                        for block in blocks
                    ))
                )
                expected = {
                    (block_word, internals)
                    for block_word in block_words
                    for internals in internal_products
                }
                require(set(coordinates) == expected, "product coordinates are not bijective")
                require(set(coordinates.values()) == {1}, "coordinate multiplicity is not one")
                instances += 1
                global_words_checked += len(global_words)
                coordinate_tuples_checked += len(expected)

    require(global_words_checked == coordinate_tuples_checked)
    return {
        "lexicographic_sum_instances": instances,
        "global_words_in_product_audit": global_words_checked,
        "coordinate_tuples": coordinate_tuples_checked,
    }


def audit_sharpness() -> dict[str, object]:
    # Three elements with the sole relation a<c; A={a,b} is not autonomous.
    order: Order = (1 << 2, 0, 0)
    subset_mask = 0b011
    require(not is_module(order, subset_mask))
    global_words = extensions_on(order, 0b111)
    internal_words = extensions_on(order, subset_mask)
    fibres = Counter(restrict_word(word, subset_mask) for word in global_words)
    require(set(internal_words) == {(0, 1), (1, 0)})
    require(fibres[(0, 1)] == 2 and fibres[(1, 0)] == 1)

    # No one- or two-element ambient poset can contain a nontrivial proper subset.
    return {
        "ambient_order": 3,
        "relation": "a<c",
        "subset": "{a,b}",
        "induced_extension_counts": [1, 1],
        "ambient_restriction_counts": [2, 1],
    }


def main() -> None:
    max_n = 6
    record = {
        "arithmetic": "exact Python integers and finite tuples",
        "module_audit": audit_modules(max_n),
        "joint_product_audit": audit_joint_products(),
        "sharp_nonmodule_witness": audit_sharpness(),
        "python": sys.version.split()[0],
        "scope": f"all naturally labeled posets through order {max_n}",
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    print(json.dumps(record, sort_keys=True, indent=2))
    print(f"record_sha256={hashlib.sha256(canonical.encode()).hexdigest()}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
