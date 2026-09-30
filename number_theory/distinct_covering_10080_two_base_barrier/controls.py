"""Exhaustive small physical projection controls and decoder rejection tests."""
import copy
import json
import math
from pathlib import Path
import shutil
import tempfile

import check


def main():
    cases = phases = 0
    for B in (2,3,4,5,6,8,9,10):
        assert math.gcd(7,B) == 1
        for H in range(1 << B):
            indicator = [(H >> z) & 1 for z in range(B)]
            cases += 1
            for d in range(1,B+1):
                if B % d:
                    continue
                projected = [sum(indicator[z] for z in range(a,B,d)) for a in range(d)]
                physical = [sum(indicator[x % B] for x in range(a,7*B,7*d)) for a in range(7*d)]
                if physical != [projected[a % d] for a in range(7*d)]:
                    raise ValueError('Full small physical phase projection differs')
                phases += len(physical)
    original_root = check.ROOT
    supplied = json.loads((original_root/'weights.json').read_text())
    rejections = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        shutil.copyfile(original_root/'near_cover.tsv',root/'near_cover.tsv')
        check.ROOT = root
        try:
            for index in range(8):
                obj = copy.deepcopy(supplied)
                sparse = obj['vectors'][0]['nonzero_weights']
                if index == 0: sparse[0][1] = -1
                if index == 1: sparse[0][1] = 0
                if index == 2: sparse[0][1] = 1.5
                if index == 3: sparse[0][0] = -1
                if index == 4: sparse[0][0] = 1440
                if index == 5: sparse.insert(1,sparse[0][:])
                if index == 6: obj['vectors'].pop()
                if index == 7: obj['fixture_sha256'] = 'wrong'
                (root/'weights.json').write_text(json.dumps(obj))
                try:
                    check.load()
                except ValueError:
                    rejections += 1
                else:
                    raise ValueError('Malformed certificate was accepted')
        finally:
            check.ROOT = original_root
    if cases != 1916 or phases != 210308 or rejections != 8:
        raise ValueError('Control domain or rejection count changed')
    print(json.dumps(dict(status='ALL_CONTROLS_PASSED',small_indicator_cases=cases,
                          full_physical_phase_values=phases,malformed_rejections=rejections)))


if __name__ == '__main__':
    main()
