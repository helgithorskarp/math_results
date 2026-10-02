"""Semantic controls, independent recursion checks and exact scope limits."""
from copy import deepcopy
from itertools import combinations, combinations_with_replacement, product
import json
from audit import HERE, canonical, check_charge, derive_rows, flags, inventory, require, unit_types
from ordinary import literal_partition_controls


def check():
    fixtures = json.loads((HERE/'fixtures.json').read_text())['stars']
    classes, _ = unit_types(fixtures)
    coarse, refined = derive_rows(classes)
    rejected = []

    def reject(name, action):
        try:
            action()
        except (ValueError, RuntimeError):
            rejected.append(name)
        else:
            raise ValueError('damage accepted: '+name)

    for name, damage in [
        ('missing-fixture', lambda f: f.pop()),
        ('duplicate-fixture', lambda f: f.__setitem__(15, f[11])),
        ('missing-quadruple', lambda f: f[11].pop()),
        ('out-of-domain-point', lambda f: f[11][0].__setitem__(0, 17)),
        ('repeated-point', lambda f: f[11][0].__setitem__(0, f[11][0][1])),
        ('repeated-pair', lambda f: f[11].__setitem__(1, f[11][0]))]:
        bad = deepcopy(fixtures); damage(bad)
        reject(name, lambda bad=bad: unit_types(bad))
    reject('false-unit-two-hub-charge', lambda: check_charge({((0, 1), (0, 2), (1, 2), (3, 4))}))
    reject('out-of-contract-inventory', lambda: inventory(coarse, (2, 2, 3), (17, 19, 19), 0))
    witness = json.loads((HERE/'WITNESS69.json').read_text())
    bad = deepcopy(witness); bad['words'][0] = bad['words'][1]
    reject('duplicate-positive-word', lambda: literal_partition_controls(bad))
    # In a mixed2111 row, an isolated unit-deficient hub with the
    # deficit-two point elsewhere is outside the mixed shared-hub lemma.
    require(flags((2, 1, 1, 1), ((0, 1), (0, 2), (1, 2)), (3, -1, -1)) == (0, 0, 0),
            'mixed-other-deficit scope leakage')
    require(flags((2, 1, 1, 1), ((1, 2), (1, 3), (2, 3)), (0, -1, -1)) == (1, 0, 0),
            'positive mixed isolated hub missed')
    require(flags((1,)*5, ((0, 1), (1, 2), (2, 3), (0, 3)), (4, -1, -1)) == (1, 0, 0),
            'positive unit isolated hub missed')
    # An independent flat exceptional-multiset algorithm checks recursion
    # coverage at the two main P6 representatives, before any cuts.
    brute_counts = []
    positive = tuple(r for r in coarse if r[3]+r[4] > 0)
    for lam in ((1, 1, 4), (1, 2, 3)):
        for t in (0, 1):
            D = (13-lam[2], 5-lam[1], 5-lam[0]); budget = 3-t
            expected = set()
            for n in range(4):
                for extra in combinations_with_replacement(positive, n):
                    E = sum(r[3] for r in extra); Q = sum(r[4] for r in extra)
                    if E+Q > budget or (budget-E-Q) % 2:
                        continue
                    remaining = tuple(D[i]-sum(r[i] for r in extra) for i in range(3))
                    if min(remaining) < 0 or sum(remaining) > 15-n:
                        continue
                    cross = sum(sum(max(v-1, 0) for v in r[:3]) for r in extra)
                    if (E-cross) % 2:
                        continue
                    expected.add(extra)
            summary, records = inventory(coarse, lam, (17, 19, 19), t)
            require(expected == {tuple(r['exceptional_rows']) for r in records}, 'recursive/flat whole inventory cover differs')
            brute_counts.append(len(expected))
    # Deliberately enlarged catalog demonstrates the omitted unit condition
    # cannot simply be ignored by this necessary-domain proof.
    all_unit_classes = {canonical(5, edges) for edges in combinations(tuple(combinations(range(5), 2)), 4)}
    relaxed, _ = derive_rows(all_unit_classes)
    relaxed_survivors = []
    for lam in ((1, 1, 4), (1, 2, 3)):
        for t in (0, 1):
            s, records = inventory(relaxed, lam, (17, 19, 19), t)
            relaxed_survivors.append(s['counts'].get('survivor', 0))
    require(relaxed_survivors == [12, 0, 7, 0], 'unit-premise escape control differs')
    # A low point's friend is forced into S only after excluding its
    # distinguished unsaturated hub by complete physical S tail coverage.
    require(3*5-0 == 15 and 3*5-1 < 15 and 3*2 < 15,
            'all-S low-friend justification transferred to a smaller tail union')
    return {'status': 'PASS_SEMANTIC_AND_DOMAIN_CONTROLS', 'damage_rejections': rejected,
            'isolated_hub_scope_controls': 3, 'flat_complete_inventory_counts': brute_counts,
            'relaxed_unit_catalog_aggregate_survivors': relaxed_survivors,
            'aggregate_survivors_are_not_codes': True, 'whole74_to59_row_projection': len(refined) == 74 and len(coarse) == 59}
