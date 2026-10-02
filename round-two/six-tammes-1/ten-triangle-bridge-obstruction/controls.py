"""Semantic damage controls and closed-endpoint/Bezout trust tests."""
from pathlib import Path
from fractions import Fraction as Q
from copy import deepcopy
import json
import audit


def rejected(function, label):
    try:
        function()
    except (ValueError, ZeroDivisionError):
        return label
    raise ValueError('invalid control accepted: ' + label)


def main():
    record = json.loads((Path(__file__).parent / 'CERTIFICATE.json').read_text())
    damages = []

    def damage(label, change):
        altered = deepcopy(record)
        change(altered)
        damages.append(rejected(lambda: audit.audit(altered), label))

    damage('unknown format', lambda r: r.update(format='wrong'))
    damage('extra silent hypothesis field', lambda r: r.update(unchecked_hypothesis=True))
    damage('open lower endpoint', lambda r: r.update(cosine_closed_band=['(14/25', '593/1000']))
    damage('different upper cosine', lambda r: r.update(cosine_closed_band=['14/25', '594/1000']))
    damage('incorrect transformed endpoint', lambda r: r.update(r_closed_band=['28/39', '3/4']))
    damage('wrong A contact triangle', lambda r: r['A_triangles'][0].__setitem__(0, 8))
    damage('wrong B contact triangle', lambda r: r['B_triangles'][0].__setitem__(0, 7))
    damage('missing first prescribed cross contact', lambda r: r['cross_contacts'].pop(0))
    damage('changed second prescribed cross contact', lambda r: r['cross_contacts'].__setitem__(1, [6, 8]))
    damage('changed row interpretation', lambda r: r['row_fields'].__setitem__(0, 'unknown'))
    damage('empty polynomial', lambda r: r['root_free_polynomials'][0].update(polynomial=[]))
    damage('nonmonic polynomial', lambda r: r['root_free_polynomials'][0].update(polynomial=['1', '2']))
    damage('trailing zero hides degree', lambda r: r['root_free_polynomials'][0]['polynomial'].append('0'))
    damage('altered Bernstein entry', lambda r: r['root_free_polynomials'][0]['Bernstein'].__setitem__(0, '0'))
    damage('removed polynomial', lambda r: r['root_free_polynomials'].pop())
    damage('duplicate polynomial', lambda r: r['root_free_polynomials'].__setitem__(1, r['root_free_polynomials'][0]))
    damage('omitted last literal placement', lambda r: r['rows'].pop())
    damage('duplicated placement', lambda r: r['rows'].__setitem__(1, r['rows'][0]))
    damage('unknown A label', lambda r: r['rows'][0].__setitem__(0, 8))
    damage('equal A boundary labels', lambda r: r['rows'][0].__setitem__(1, r['rows'][0][0]))
    damage('internal A edge', lambda r: r['rows'][0].__setitem__(slice(0, 2), [0, 5]))
    damage('internal B edge', lambda r: r['rows'][0].__setitem__(slice(2, 4), [1, 2]))
    damage('negative index', lambda r: r['rows'][0].__setitem__(4, -1))
    damage('boolean label', lambda r: r['rows'][0].__setitem__(0, True))
    damage('out of range index', lambda r: r['rows'][0].__setitem__(4, 23))
    damage('wrong case root-free binding', lambda r: r['rows'][0].__setitem__(4, (r['rows'][0][4] + 1) % 23))
    # The final two degree fields are checked after all cases: targeted direct
    # witness tests below cover their mathematical role without repeated full runs.
    damages.append(rejected(lambda: audit.witness({}, {}), 'both zero gaps do not yield gcd1'))
    damages.append(rejected(lambda: audit.certify_nonzero({0: -audit.LOW, 1: Q(1)}), 'root at closed lower endpoint'))
    damages.append(rejected(lambda: audit.certify_nonzero({0: -audit.HIGH, 1: Q(1)}), 'root at closed upper endpoint'))
    damages.append(rejected(lambda: audit.certify_nonzero({0: -(audit.LOW + audit.HIGH) / 2, 1: Q(1)}), 'interior root'))
    damages.append(rejected(lambda: audit.division({0: Q(1)}, {}), 'zero divisor'))
    # 1 divides (r-r0) twice, but it cannot be a Bezout witness for that pair.
    f = {0: -audit.LOW, 1: Q(1)}
    h, _, _ = audit.witness(f, f)
    audit.need(h != {0: Q(1)}, 'common-divisor-only false proof control')
    damages.append(rejected(lambda: audit.certify_nonzero(h), 'common divisor1 cannot certify shared root'))
    # A single zero gap remains sound when the other gap is root-free.
    h, u, v = audit.witness({}, {0: Q(2), 1: Q(1)})
    audit.certify_nonzero(h)
    audit.need(audit.plus(audit.times(u, {}), audit.times(v, {0: Q(2), 1: Q(1)})) == h,
               'one zero gap positive control')
    accepted = ['one zero gap with root-free other gap']
    reverse = deepcopy(record)
    reverse['rows'].reverse()
    audit.audit(reverse)
    accepted.append('all rows in reversed order')
    permuted = deepcopy(record)
    permuted['root_free_polynomials'].reverse()
    for row in permuted['rows']:
        row[4] = 22 - row[4]
    audit.audit(permuted)
    accepted.append('all root-free indices consistently reversed')
    print(json.dumps({'status': 'complete', 'damages_rejected': len(damages),
                      'damage_labels': damages, 'valid_representations_accepted': len(accepted),
                      'valid_labels': accepted}, sort_keys=True))


if __name__ == '__main__':
    main()
