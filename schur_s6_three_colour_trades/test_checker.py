"""Definition-level controls and malformed-certificate checks."""
from copy import deepcopy
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path
import random
import unittest

from check import colourable, verify, violations


def brute(vertices, k):
    for labels in product(range(k), repeat=len(vertices)):
        colour = dict(zip(vertices, labels))
        if all(x+y not in colour or colour[x] != colour[y] or colour[x] != colour[x+y]
               for x, y in combinations_with_replacement(vertices, 2)):
            return True
    return False


class CheckerTests(unittest.TestCase):
    def test_classical_boundaries(self):
        for k, n, expected in [(1,1,True),(1,2,False),(2,4,True),
                                (2,5,False),(3,13,True),(3,14,False)]:
            with self.subTest(k=k, n=n):
                answer, _, _ = colourable(list(range(1,n+1)), k, 1)
                self.assertEqual(answer is not None, expected)

    def test_direct_exhaustive_controls(self):
        count = 0
        for size in range(10):
            for vertices in combinations(range(1,10), size):
                vertices = list(vertices)
                for k in [1, 2]:
                    result = colourable(vertices, k, vertices[-1] if vertices else None)[0]
                    self.assertEqual(result is not None, brute(vertices, k))
                    count += 1
        self.assertEqual(count, 1024)
        rng = random.Random(537)
        for _ in range(60):
            vertices = sorted(rng.sample(range(1,25), rng.randrange(1,10)))
            expected = brute(vertices, 3)
            for root in [vertices[0], vertices[-1]]:
                self.assertEqual(colourable(vertices,3,root)[0] is not None, expected)

    def test_doubling(self):
        self.assertEqual(violations([1,1]), [[1,1,2,1]])
        self.assertFalse(violations([1,2]))
        self.assertEqual(violations([1,2,1,2]), [[2,2,4,2]])

    def test_certificate_guards(self):
        directory = Path(__file__).resolve().parent
        fixtures = json.loads((directory/'fixtures.json').read_text())
        certificate = json.loads((directory/'certificate.json').read_text())
        missing = deepcopy(certificate)
        missing['cases'] = []
        with self.assertRaisesRegex(ValueError, 'missing palette'):
            verify(fixtures, missing)
        bad_vertex = deepcopy(certificate)
        bad_vertex['cases'][0]['vertices'] = [538]
        with self.assertRaisesRegex(ValueError, 'outside palette'):
            verify(fixtures, bad_vertex)
        colourable_claim = deepcopy(certificate)
        colourable_claim['cases'][0]['vertices'] = [colourable_claim['cases'][0]['vertices'][0]]
        colourable_claim['cases'][0]['root'] = colourable_claim['cases'][0]['vertices'][0]
        with self.assertRaisesRegex(ValueError, 'three-colourable'):
            verify(fixtures, colourable_claim)


if __name__ == '__main__':
    unittest.main()
