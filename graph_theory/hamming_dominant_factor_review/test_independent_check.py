#!/usr/bin/env python3
import unittest

from independent_check import (
    boundary_extension_audit,
    dimension_two_nonunique_witness,
    direct_class_census,
    endpoint_audit,
)


class DominantFactorReviewTests(unittest.TestCase):
    def test_endpoint_gaps(self) -> None:
        self.assertEqual(endpoint_audit(20)[1], 2)

    def test_boundary_extension(self) -> None:
        self.assertEqual(boundary_extension_audit(20), 38)

    def test_strict_small_graph(self) -> None:
        self.assertEqual(direct_class_census((5, 2, 2))[1], 4)

    def test_dimension_two_exception(self) -> None:
        self.assertEqual(dimension_two_nonunique_witness(), 2)


if __name__ == "__main__":
    unittest.main()
