"""Small complete compatibility audit and actual witness rejection controls."""
from itertools import combinations, product
from pathlib import Path
import json
import tempfile

from geometry import classical_design, mask, require
from generate import no_edges
from verify import check_witness


def compatible(left, right):
    b, qs = left
    c, rs = right
    return (b & c).bit_count() <= 2 and all(
        q == r or (q & r).bit_count() <= 1 for q in qs for r in rs)


def main():
    old = [mask(p) for p in ((0, 1, 2, 3, 4), (0, 1, 2, 3, 5),
                             (0, 1, 2, 5, 6), (0, 1, 5, 6, 7),
                             (0, 5, 6, 7, 8), (5, 6, 7, 8, 9))]
    qs = [mask(p) for p in ((0, 1, 2, 3), (0, 1, 2, 4), (0, 1, 4, 5),
                            (0, 4, 5, 6), (4, 5, 6, 7))]
    records = [(b, q) for b, q in product(old, [()] + [(q,) for q in qs])]
    checked = 0
    for a, b in combinations(records, 2):
        direct = compatible(a, b)
        try:
            no_edges([a, b])
            computed = False
        except ValueError as e:
            require(str(e) == 'a compatible pair exists', 'unexpected audit failure')
            computed = True
        require(computed == direct, 'incidence compatibility mismatch')
        checked += 1
    # Empty and singleton universes include the diagonal/self exclusion.
    no_edges([])
    for r in records:
        no_edges([r])
    # In particular, sharing an identical four-set must be permitted.
    require(compatible((old[0], (qs[0],)), (old[-1], (qs[0],))),
            'shared-old-part positive control failed')
    circles, _ = classical_design()
    folder = Path(__file__).resolve().parent
    original = json.loads((folder / 'witness69.json').read_text())
    corruptions = {}
    duplicate = json.loads(json.dumps(original))
    duplicate['old_parts'][1] = duplicate['old_parts'][0]
    corruptions['duplicate_replacement'] = duplicate
    incompatible = json.loads(json.dumps(original))
    c = next(c for c in circles if c & original['old_parts'][0] == original['old_parts'][0])
    outside_point = next(p for p in range(17) if c >> p & 1 and not original['outsider'] >> p & 1)
    incompatible['old_parts'][0] = c ^ (1 << outside_point)
    corruptions['retained_outsider_triple'] = incompatible
    rejected = {}
    with tempfile.TemporaryDirectory(prefix='steiner-audit-') as d:
        for name, data in corruptions.items():
            path = Path(d) / (name + '.json')
            path.write_text(json.dumps(data))
            try:
                check_witness(circles, path)
            except ValueError as e:
                rejected[name] = str(e)
            else:
                raise ValueError('corrupted witness was accepted: ' + name)
    print(json.dumps({'two_record_cases': checked, 'singleton_cases': len(records),
                      'empty_case': True, 'shared_four_set_allowed': True,
                      'rejected_corruptions': rejected}, sort_keys=True))


if __name__ == '__main__':
    main()
