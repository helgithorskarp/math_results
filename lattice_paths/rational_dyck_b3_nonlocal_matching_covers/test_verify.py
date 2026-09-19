from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VERIFY = load("verify")
INDEPENDENT = load("independent_check")


class NonlocalCoverTests(unittest.TestCase):
    def test_matrix_scores_equal_scalar_continuants(self) -> None:
        for a in range(4, 31):
            if a % 3 == 0:
                continue
            for part in VERIFY.partitions(a):
                for runs in VERIFY.valid_runs(part, a):
                    path = INDEPENDENT.from_runs(runs)
                    self.assertEqual(VERIFY.matching_score(runs), INDEPENDENT.matching_score(path))

    def test_closed_gap_formula(self) -> None:
        for a in range(4, 101):
            if a % 3 == 0:
                continue
            m = a // 3
            for z in range(m):
                x_path, y_path, _, epsilon, n = VERIFY.candidate_pair(a, z)
                self.assertEqual(
                    VERIFY.matching_score(y_path) - VERIFY.matching_score(x_path),
                    VERIFY.gap_formula(z, epsilon, n),
                )

    def test_every_fourth_fibonacci_sum(self) -> None:
        for even_r in range(2, 32, 2):
            for count in range(1, 15):
                left = sum(VERIFY.fibonacci(even_r + 4 * k) for k in range(count))
                right_numerator = (
                    VERIFY.lucas(even_r + 4 * count - 2) - VERIFY.lucas(even_r - 2)
                )
                self.assertEqual(5 * left, right_numerator)

    def test_first_nonadjacent_example(self) -> None:
        result = VERIFY.audit(13)
        self.assertEqual(result["max_fibre_distance"], 3)
        x_path, y_path, _, _, _ = VERIFY.candidate_pair(13, 0)
        self.assertEqual(x_path, (12, 1, 0))
        self.assertEqual(y_path, (9, 0, 4))
        self.assertEqual(VERIFY.matching_score(y_path) - VERIFY.matching_score(x_path), 39218)

    def test_small_definition_level_audit(self) -> None:
        result = INDEPENDENT.audit(20)
        self.assertEqual(result["endpoints"], 12)
        self.assertEqual(result["covers"], 42)
        self.assertEqual(result["max_fibre_distance"], 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
