#!/usr/bin/env python3
"""Independently verify the corrected abelian degree-four obstruction."""

from __future__ import annotations

from collections import deque
from itertools import combinations
from itertools import product


RADIUS = 7
CENTER_COUNTS = (4, 6)
MAX_SPHERE_SIZE = 4 * RADIUS
MAX_GROUP_ORDER = max(CENTER_COUNTS) * MAX_SPHERE_SIZE


def add(element: int, generator: int, m: int, n: int, sign: int) -> int:
    x, y = divmod(element, n)
    gx, gy = divmod(generator, n)
    return ((x + sign * gx) % m) * n + (y + sign * gy) % n


def sphere_data(
    m: int, n: int, generators: tuple[int, ...]
) -> tuple[bool, list[int], int]:
    order = m * n
    distance = [-1] * order
    distance[0] = 0
    queue = deque([0])
    while queue:
        element = queue.popleft()
        for generator in generators:
            for sign in (-1, 1):
                neighbour = add(element, generator, m, n, sign)
                if distance[neighbour] == -1:
                    distance[neighbour] = distance[element] + 1
                    queue.append(neighbour)
    connected = all(value != -1 for value in distance)
    return (
        connected,
        [element for element, value in enumerate(distance) if value == RADIUS],
        max(distance),
    )


def rank2_translate_tiling(
    m: int, n: int, sphere: list[int], translate_count: int
) -> bool:
    order = m * n
    if len(sphere) * translate_count != order:
        return False
    covered = set(sphere)

    def search(remaining: int) -> bool:
        if remaining == 0:
            return len(covered) == order
        first_uncovered = next(
            (element for element in range(order) if element not in covered), None
        )
        if first_uncovered is None:
            return False
        tried_shifts = set()
        for sphere_element in sphere:
            shift = add(first_uncovered, sphere_element, m, n, -1)
            if shift in tried_shifts:
                continue
            tried_shifts.add(shift)
            translate = {add(element, shift, m, n, 1) for element in sphere}
            if covered.isdisjoint(translate):
                covered.update(translate)
                if search(remaining - 1):
                    return True
                covered.difference_update(translate)
        return False

    return search(translate_count - 1)


def main() -> None:
    assert sphere_data(1, 18, (1,)) == (True, [7, 11], 9)
    examined = {1: 0, 2: 0}
    connected_count = {1: 0, 2: 0}
    connected_over_radius = {1: 0, 2: 0}
    counting_candidates = {count: [] for count in CENTER_COUNTS}
    translate_tilings = {count: 0 for count in CENTER_COUNTS}
    best_error = MAX_GROUP_ORDER
    best_rows: list[tuple[int, int, tuple[int, ...], int]] = []

    for m in range(1, MAX_GROUP_ORDER + 1):
        for n in range(m, MAX_GROUP_ORDER + 1):
            order = m * n
            if order > MAX_GROUP_ORDER or n % m != 0:
                continue
            if order % 4 != 0 and order % 6 != 0:
                continue
            nonidentity = range(1, order)
            for generator_count in (1, 2):
                for generators in combinations(nonidentity, generator_count):
                    examined[generator_count] += 1
                    connected, sphere, eccentricity = sphere_data(m, n, generators)
                    if not connected:
                        continue
                    size = len(sphere)
                    connected_count[generator_count] += 1
                    connected_over_radius[generator_count] += eccentricity > RADIUS
                    error = abs(4 * size - order)
                    row = (m, n, generators, size)
                    if error < best_error:
                        best_error = error
                        best_rows = [row]
                    elif error == best_error:
                        best_rows.append(row)
                    for center_count in CENTER_COUNTS:
                        if center_count * size == order:
                            counting_candidates[center_count].append(row)
                            translate_tilings[center_count] += rank2_translate_tiling(
                                m, n, sphere, center_count
                            )

    assert not counting_candidates[4]
    assert not translate_tilings[4]
    assert not translate_tilings[6]

    # The only degree-at-most-four abelian Cayley connection sets not covered
    # by two signed generators have one non-involutory pair {+g,-g} and up to
    # two involutions.  Their free-model radius-7 sphere has size at most 8,
    # so a four- or six-center example has group order at most 48.
    mixed_examined = 0
    mixed_connected = 0
    mixed_connected_over_radius = 0
    mixed_counting_candidates = {count: [] for count in CENTER_COUNTS}
    mixed_translate_tilings = {count: 0 for count in CENTER_COUNTS}

    def invariant_factor_types(
        limit: int, prefix: tuple[int, ...] = ()
    ) -> list[tuple[int, ...]]:
        result = []
        product_so_far = 1
        for factor in prefix:
            product_so_far *= factor
        start = 2 if not prefix else prefix[-1]
        for factor in range(start, limit + 1):
            if prefix and factor % prefix[-1] != 0:
                continue
            if product_so_far * factor > limit:
                break
            factors = prefix + (factor,)
            result.append(factors)
            result.extend(invariant_factor_types(limit, factors))
        return result

    def tuple_add(
        left: tuple[int, ...],
        right: tuple[int, ...],
        factors: tuple[int, ...],
        sign: int = 1,
    ) -> tuple[int, ...]:
        return tuple(
            (a + sign * b) % factor
            for a, b, factor in zip(left, right, factors)
        )

    def tuple_translate_tiling(
        elements: list[tuple[int, ...]],
        sphere: set[tuple[int, ...]],
        factors: tuple[int, ...],
        translate_count: int,
    ) -> bool:
        if len(sphere) * translate_count != len(elements):
            return False
        covered = set(sphere)

        def search(remaining: int) -> bool:
            if remaining == 0:
                return len(covered) == len(elements)
            first_uncovered = next(
                (element for element in elements if element not in covered), None
            )
            if first_uncovered is None:
                return False
            tried_shifts = set()
            for sphere_element in sphere:
                shift = tuple_add(first_uncovered, sphere_element, factors, -1)
                if shift in tried_shifts:
                    continue
                tried_shifts.add(shift)
                translate = {
                    tuple_add(element, shift, factors) for element in sphere
                }
                if covered.isdisjoint(translate):
                    covered.update(translate)
                    if search(remaining - 1):
                        return True
                    covered.difference_update(translate)
            return False

        return search(translate_count - 1)

    for factors in invariant_factor_types(48):
        elements = list(product(*(range(factor) for factor in factors)))
        if len(elements) % 4 != 0 and len(elements) % 6 != 0:
            continue
        zero = tuple(0 for _ in factors)
        indices = {element: index for index, element in enumerate(elements)}
        involutions = []
        noninvolutory_pair_representatives = []
        for element in elements[1:]:
            inverse = tuple((-value) % factor for value, factor in zip(element, factors))
            if element == inverse:
                involutions.append(element)
            elif indices[element] < indices[inverse]:
                noninvolutory_pair_representatives.append(element)

        for generator in noninvolutory_pair_representatives:
            for involution_count in (0, 1, 2):
                for selected_involutions in combinations(involutions, involution_count):
                    mixed_examined += 1
                    distance = {zero: 0}
                    queue = deque([zero])
                    while queue:
                        element = queue.popleft()
                        for sign in (-1, 1):
                            neighbour = tuple_add(element, generator, factors, sign)
                            if neighbour not in distance:
                                distance[neighbour] = distance[element] + 1
                                queue.append(neighbour)
                        for involution in selected_involutions:
                            neighbour = tuple_add(element, involution, factors)
                            if neighbour not in distance:
                                distance[neighbour] = distance[element] + 1
                                queue.append(neighbour)
                    if len(distance) != len(elements):
                        continue
                    mixed_connected += 1
                    mixed_connected_over_radius += max(distance.values()) > RADIUS
                    sphere = {
                        element
                        for element, value in distance.items()
                        if value == RADIUS
                    }
                    size = len(sphere)
                    for center_count in CENTER_COUNTS:
                        if center_count * size == len(elements):
                            mixed_counting_candidates[center_count].append(
                                (factors, generator, selected_involutions, size)
                            )
                            mixed_translate_tilings[center_count] += (
                                tuple_translate_tiling(
                                    elements, sphere, factors, center_count
                                )
                            )

    assert not mixed_counting_candidates[4]
    assert not mixed_translate_tilings[4]
    assert not mixed_translate_tilings[6]
    assert examined == {1: 11170, 2: 628183}
    assert connected_count == {1: 1810, 2: 323010}
    assert connected_over_radius == {1: 1798, 2: 301643}
    assert len(counting_candidates[6]) == 9032
    assert mixed_examined == 6748
    assert mixed_connected == 1082
    assert mixed_connected_over_radius == 341
    assert not mixed_counting_candidates[6]
    print(f"radius={RADIUS}")
    print(f"maximum_possible_sphere_size={MAX_SPHERE_SIZE}")
    print(f"maximum_group_order={MAX_GROUP_ORDER}")
    print(f"examined_one_generator_sets={examined[1]}")
    print(f"examined_two_generator_sets={examined[2]}")
    print(f"connected_one_generator_sets={connected_count[1]}")
    print(f"connected_two_generator_sets={connected_count[2]}")
    print(
        "connected_one_generator_sets_over_radius="
        f"{connected_over_radius[1]}"
    )
    print(
        "connected_two_generator_sets_over_radius="
        f"{connected_over_radius[2]}"
    )
    print(f"four_center_counting_candidates={len(counting_candidates[4])}")
    print(f"six_center_counting_candidates={len(counting_candidates[6])}")
    print(f"four_center_translate_tilings={translate_tilings[4]}")
    print(f"six_center_translate_tilings={translate_tilings[6]}")
    print(f"smallest_counting_error={best_error}")
    print(f"number_attaining_smallest_error={len(best_rows)}")
    print(f"mixed_connection_sets_examined={mixed_examined}")
    print(f"mixed_connected_connection_sets={mixed_connected}")
    print(
        "mixed_connected_sets_over_radius=" f"{mixed_connected_over_radius}"
    )
    print(
        f"mixed_four_center_counting_candidates="
        f"{len(mixed_counting_candidates[4])}"
    )
    print(
        f"mixed_six_center_counting_candidates="
        f"{len(mixed_counting_candidates[6])}"
    )
    print(f"mixed_four_center_translate_tilings={mixed_translate_tilings[4]}")
    print(f"mixed_six_center_translate_tilings={mixed_translate_tilings[6]}")


if __name__ == "__main__":
    main()
