"""Independent small-set and malformed-certificate controls for the new bridge."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from check_splitting import blocked_colours, verify


class SplittingTests(unittest.TestCase):
    def test_blocking_against_definition(self):
        count = 0
        for mask in range(1 << 10):
            old_class = {v for v in range(1,11) if mask & (1 << (v-1))}
            if any(x+y in old_class for x in old_class for y in old_class):
                continue
            old = [0]+[1 if v in old_class else 0 for v in range(1,11)]
            blocked = blocked_colours(old)
            for v in set(range(1,11))-old_class:
                new_class = old_class | {v}
                invalid = any(x+y in new_class for x in new_class for y in new_class)
                self.assertEqual(1 in blocked[v],invalid)
            count += 1
        self.assertEqual(count,151)

    def test_doubling_both_directions_and_difference(self):
        a = blocked_colours([0,0,1])  # 1+1=2, only 2 is fixed
        self.assertIn(1,a[1])
        b = blocked_colours([0,1,0])  # 1+1=2, only 1 is fixed
        self.assertIn(1,b[2])
        c = blocked_colours([0,0,1,0,0,1])  # 2+3=5
        self.assertIn(1,c[3])

    def test_invalid_certificates(self):
        directory = Path(__file__).resolve().parent
        fixtures = json.loads((directory/'fixtures.json').read_text())
        certificate = json.loads((directory/'class_splitting.json').read_text())
        missing_pair = deepcopy(certificate)
        missing_pair['nonmerge']['baseline'].pop()
        with self.assertRaisesRegex(ValueError,'missing nonmerge pair'):
            verify(fixtures,missing_pair)
        missing_case = deepcopy(certificate)
        missing_case['cases'].pop()
        with self.assertRaisesRegex(ValueError,'kernel case coverage'):
            verify(fixtures,missing_case)
        unblocked = deepcopy(certificate)
        row = unblocked['cases'][0]
        old = [0]+list(map(int,fixtures[row['input']]['colours']))+[0]
        b = blocked_colours(old)
        frozen = set(range(1,7))-set(row['palette'])
        v = next(v for v in range(1,537) if old[v] in row['palette'] and not frozen <= b[v])
        row['vertices'] = [v]
        row['root'] = v
        with self.assertRaisesRegex(ValueError,'can enter a frozen colour'):
            verify(fixtures,unblocked)
        colourable = deepcopy(certificate)
        row = colourable['cases'][0]
        row['vertices'] = row['vertices'][:1]
        row['root'] = row['vertices'][0]
        with self.assertRaisesRegex(ValueError,'kernel is three-colourable'):
            verify(fixtures,colourable)


if __name__ == '__main__':
    unittest.main()
