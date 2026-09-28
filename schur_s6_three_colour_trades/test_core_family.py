"""Controls for fixed-core support and the Cartesian product argument."""
from copy import deepcopy
from itertools import product
import json
from pathlib import Path
import unittest

from check import violations
from check_core_family import verify,verify_product
from check_splitting import blocked_colours


class CoreFamilyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=Path(__file__).resolve().parent
        cls.cert=json.loads((p/'core_family.json').read_text())
        cls.kernels=json.loads((p/'class_splitting.json').read_text())
        cls.fixtures=json.loads((p/'fixtures.json').read_text())
        cls.partial=[0]*538
        for d,B in cls.cert['cores'].items():
            for v in B:cls.partial[v]=int(d)

    def test_product_criterion_against_all_assignments(self):
        choices=[{1},{2},{1,2}]
        cases=positive=0
        for n in (3,4,5):
            for domains in product(choices,repeat=n):
                direct=all(not violations(list(c)) for c in product(*(sorted(D) for D in domains)))
                local=all(not(domains[x-1]&domains[z-x-1]&domains[z-1])
                          for z in range(2,n+1) for x in range(1,z//2+1))
                self.assertEqual(local,direct)
                cases+=1
                positive+=direct
        self.assertEqual(cases,351)
        self.assertGreater(positive,0)
        self.assertLess(positive,cases)

    def test_product_rejects_bad_switch_and_core_change(self):
        bad=deepcopy(self.cert)
        old=self.fixtures['baseline']['colours']
        # Since 1+1=2, allowing the old colour of 2 at 1 is invalid.
        bad['product_switches']=[{'vertex':1,'old':int(old[0]),'alternative':int(old[1])}]
        no_fixed=[0]*538
        with self.assertRaisesRegex(ValueError,'monochromatic triple'):
            verify_product(bad,self.fixtures,no_fixed)
        bad=deepcopy(self.cert)
        v=next(v for v in range(1,537) if self.partial[v])
        d=int(old[v-1])
        bad['product_switches']=[{'vertex':v,'old':d,'alternative':d%6+1}]
        with self.assertRaisesRegex(ValueError,'changes a core'):
            verify_product(bad,self.fixtures,self.partial)

    def test_partial_support_and_nonmerge_guards(self):
        # Forgotten vertices must supply no premise to a blocking triple.
        b=blocked_colours([0,0,1,0])
        self.assertNotIn(1,b[3])
        self.assertIn(1,b[1])  # repeated summand 1+1=2 still blocks 1
        bad=deepcopy(self.cert)
        bad['nonmerge'].pop()
        with self.assertRaisesRegex(ValueError,'missing pair witness'):
            verify(bad,self.kernels,self.fixtures)
        bad=deepcopy(self.cert)
        bad['cores']['2'].append(bad['cores']['1'][0]);bad['cores']['2'].sort()
        with self.assertRaisesRegex(ValueError,'overlapping cores'):
            verify(bad,self.kernels,self.fixtures)


if __name__=='__main__':unittest.main()
