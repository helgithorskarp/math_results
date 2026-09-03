import unittest
from itertools import combinations, product

from verify import (
    direct_majority_check,
    star_partition,
    theorem_parameters,
    validate_star_partition,
    verify_shell_bound,
)


class StarPartitionTests(unittest.TestCase):
    def test_all_small_rectangles(self) -> None:
        for n in range(1, 13):
            for m in range(n, 13):
                for s in range(1, n + 1):
                    pieces = star_partition(m, n, s)
                    validate_star_partition(m, n, s, pieces)

    def test_nondivisible_examples(self) -> None:
        for m, n, s in ((5, 4, 3), (8, 7, 3), (11, 8, 5), (12, 11, 7)):
            pieces = star_partition(m, n, s)
            self.assertEqual(len(pieces), (m * n) // s)
            self.assertEqual(sum(map(len, pieces)), m * n)


class HammingTheoremTests(unittest.TestCase):
    def test_balanced_specialization(self) -> None:
        for n in range(2, 21):
            _, s, value = theorem_parameters(n, n, n)
            self.assertEqual(s, (n + 2) // 2)
            self.assertEqual(value, (n * n) // s)

    def test_direct_definition_and_shell_bound(self) -> None:
        tested = 0
        for n3 in range(2, 9):
            for n2 in range(n3, 9):
                for n1 in range(n2, 9):
                    degree = n1 + n2 + n3 - 3
                    threshold = (degree + 1) // 2
                    if threshold < n1 - 1:
                        continue
                    _, s, _ = theorem_parameters(n1, n2, n3)
                    pieces = star_partition(n2, n3, s)
                    validate_star_partition(n2, n3, s, pieces)
                    direct_majority_check(n1, n2, n3, pieces)
                    checked, equality = verify_shell_bound(n1, n2, n3)
                    self.assertGreater(checked, 0)
                    self.assertGreater(equality, 0)
                    tested += 1
        self.assertEqual(tested, 71)

    def test_boundary_and_rejection(self) -> None:
        self.assertEqual(theorem_parameters(5, 3, 2), (4, 1, 6))
        with self.assertRaises(ValueError):
            theorem_parameters(6, 3, 2)

    def test_exhaustive_small_minimum_sets_and_classification(self) -> None:
        for dimensions in ((2, 2, 2), (3, 2, 2), (3, 3, 2), (4, 2, 2), (4, 3, 2)):
            n1, n2, n3 = dimensions
            threshold, s, _ = theorem_parameters(*dimensions)
            target = n1 * s
            vertices = list(product(*(range(n) for n in dimensions)))

            def is_majority_set(candidate: frozenset[tuple[int, int, int]]) -> bool:
                for vertex in candidate:
                    internal = sum(
                        sum(
                            tuple(
                                value if index == coordinate else vertex[index]
                                for index in range(3)
                            )
                            in candidate
                            for value in range(dimensions[coordinate])
                            if value != vertex[coordinate]
                        )
                        for coordinate in range(3)
                    )
                    if internal < threshold:
                        return False
                return True

            rectangles: set[frozenset[tuple[int, int, int]]] = set()
            for full_coordinate in range(3):
                if dimensions[full_coordinate] != n1:
                    continue
                for selected_coordinate in range(3):
                    if selected_coordinate == full_coordinate:
                        continue
                    if dimensions[selected_coordinate] < s:
                        continue
                    fixed_coordinate = 3 - full_coordinate - selected_coordinate
                    for selected in combinations(range(dimensions[selected_coordinate]), s):
                        for fixed in range(dimensions[fixed_coordinate]):
                            rectangle = set()
                            for full in range(n1):
                                for chosen in selected:
                                    point = [0, 0, 0]
                                    point[full_coordinate] = full
                                    point[selected_coordinate] = chosen
                                    point[fixed_coordinate] = fixed
                                    rectangle.add(tuple(point))
                            rectangles.add(frozenset(rectangle))

            found_at_target: set[frozenset[tuple[int, int, int]]] = set()
            for size in range(threshold + 1, target + 1):
                for raw_candidate in combinations(vertices, size):
                    candidate = frozenset(raw_candidate)
                    if not is_majority_set(candidate):
                        continue
                    self.assertEqual(size, target)
                    found_at_target.add(candidate)
            self.assertEqual(found_at_target, rectangles)


if __name__ == "__main__":
    unittest.main()
