"""Definition-level positive witnesses and deliberate certificate corruptions."""
from itertools import combinations
import json
from pathlib import Path

from finish import check_weights
from glue import joins

ROOT = Path(__file__).resolve().parent


def check_link(a, b):
    if len(a) != 5 or len(b) != 4 or len(set(a)) != 5 or len(set(b)) != 4:
        raise ValueError('block count or distinctness')
    if any(type(r) is not int or not 0 <= r < 2048 or r.bit_count() != 4 for r in a):
        raise ValueError('through-row domain')
    if any(type(r) is not int or not 0 <= r < 2048 or r.bit_count() != 5 for r in b):
        raise ValueError('away-row domain')
    full = [r | 2048 for r in a] + b
    for pair in combinations(range(12), 2):
        mask = sum(1 << p for p in pair)
        if not any(row & mask == mask for row in full):
            raise ValueError('uncovered link pair')
    if any(not 3 <= sum(r >> p & 1 for r in full) <= 5 for p in range(12)):
        raise ValueError('link degree')
    for pair in combinations(range(11), 2):
        mask = sum(1 << p for p in pair)
        if sum(row & mask == mask for row in a) > 2:
            raise ValueError('through-pair multiplicity')


def main():
    local = json.loads((ROOT / 'LOCAL.json').read_text())
    checked = 0
    for record in local:
        for cover in record['covers']:
            check_link(record['a'], cover)
            checked += 1
    links = json.loads((ROOT / 'LINKS.json').read_text())
    certificate = json.loads((ROOT / 'weights.json').read_text())[0]
    joined = joins(links[certificate['root']], links)
    configuration = joined['configurations'][certificate['index']]
    check_weights(joined, configuration, certificate)
    controls = []
    covered_pair = configuration['a'][0] & -configuration['a'][0]
    rest = configuration['a'][0] & ~covered_pair
    covered_pair |= rest & -rest
    corruptions = [
        ('weight_on_covered_pair', dict(weights=[[covered_pair, 1]], total=1, capacity=1)),
        ('insufficient_weight_gap', dict(weights=[[certificate['weights'][0][0], 1]],
                                        total=1, capacity=1)),
    ]
    for label, bad in corruptions:
        try:
            check_weights(joined, configuration, bad)
        except ValueError as error:
            controls.append(dict(control=label, rejected=True, reason=str(error)))
        else:
            raise ValueError('corrupt certificate accepted')
    record = local[0]
    cover = record['covers'][0]
    found = False
    for old in range(11):
        for new in range(11):
            if not cover[0] >> old & 1 or cover[0] >> new & 1:
                continue
            changed = cover.copy()
            changed[0] ^= (1 << old) | (1 << new)
            try:
                check_link(record['a'], changed)
            except ValueError as error:
                if str(error) == 'uncovered link pair':
                    controls.append(dict(control='size_preserving_block_corruption',
                                         rejected=True, reason=str(error)))
                    found = True
                    break
        if found:
            break
    if not found:
        raise ValueError('no missed-pair negative control found')
    print(json.dumps(dict(status='CONTROLS_PASSED', positive_links=checked,
                          negative_controls=controls), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
