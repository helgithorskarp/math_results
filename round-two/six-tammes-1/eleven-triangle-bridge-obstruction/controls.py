"""Semantic certificate, branch, range and full-field comparison controls."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as Q
import json
import audit


def reject(function, label):
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
        damages.append(reject(lambda: audit.audit(altered, 0, 1), label))

    damage('unknown format', lambda r: r.update(format='wrong'))
    damage('extra silent assumption', lambda r: r.update(unchecked_assumption=True))
    damage('open lower endpoint', lambda r: r.update(cosine_closed_band=['(14/25', '593/1000']))
    damage('different upper cosine', lambda r: r.update(cosine_closed_band=['14/25', '594/1000']))
    damage('wrong transformed endpoint', lambda r: r.update(r_closed_band=['28/39', '3/4']))
    damage('altered A triangle', lambda r: r['A_triangles'][0].__setitem__(0, 8))
    damage('altered B triangle', lambda r: r['B_triangles'][0].__setitem__(0, 7))
    damage('missing prescribed cross contact', lambda r: r['cross_contacts'].pop())
    damage('altered prescribed cross contact', lambda r: r['cross_contacts'].__setitem__(0, [6, 8]))
    damage('changed fresh label', lambda r: r.update(fresh_corner_label=3))
    damage('boolean fresh label', lambda r: r.update(fresh_corner_label=True))
    damage('omitted long branch', lambda r: r['types'].pop())
    damage('wrong row semantics', lambda r: r['row_fields'].__setitem__(0, 'unknown'))
    damage('omitted last literal case', lambda r: r['rows'].pop())
    damage('duplicate literal case', lambda r: r['rows'].__setitem__(1, r['rows'][0]))
    damage('unknown path type', lambda r: r['rows'][0].__setitem__(0, 'other'))
    damage('bad A label', lambda r: r['rows'][0].__setitem__(1, 8))
    damage('bad B label', lambda r: r['rows'][0].__setitem__(3, 7))
    damage('boolean corner', lambda r: r['rows'][0].__setitem__(1, True))
    damage('internal A attachment edge', lambda r: r['rows'][0].__setitem__(slice(1, 3), [0, 5]))
    damage('internal B attachment edge', lambda r: r['rows'][0].__setitem__(slice(3, 5), [1, 2]))
    damage('negative root-free index', lambda r: r['rows'][0].__setitem__(5, -1))
    damage('out of range root-free index', lambda r: r['rows'][0].__setitem__(5, len(r['root_free_polynomials'])))
    damage('wrong case-polynomial binding', lambda r: r['rows'][0].__setitem__(5, (r['rows'][0][5] + 1) % len(r['root_free_polynomials'])))
    damage('empty root-free polynomial', lambda r: r['root_free_polynomials'][0].update(polynomial=[]))
    damage('nonmonic polynomial', lambda r: r['root_free_polynomials'][0].update(polynomial=['1', '2']))
    damage('trailing zero hides degree', lambda r: r['root_free_polynomials'][0]['polynomial'].append('0'))
    damage('altered root-free Bernstein entry', lambda r: r['root_free_polynomials'][0]['Bernstein'].__setitem__(0, '0'))
    damage('duplicate root-free polynomial', lambda r: r['root_free_polynomials'].__setitem__(1, r['root_free_polynomials'][0]))
    damage('omitted core noncontact', lambda r: r['core_noncontacts'].pop())
    damage('wrong core noncontact pair', lambda r: r['core_noncontacts'][0].update(pair=[0, 5]))
    damage('wrong core gap polynomial', lambda r: r['core_noncontacts'][0]['gap'].__setitem__(0, '0'))
    damage('wrong core Bernstein entry', lambda r: r['core_noncontacts'][0]['Bernstein'].__setitem__(0, '0'))
    damage('negative gap degree', lambda r: r.update(maximum_gap_degree=-1))
    damage('negative witness degree', lambda r: r.update(maximum_Bezout_witness_degree=-1))
    damage('insufficient gap-degree bound', lambda r: r.update(maximum_gap_degree=0))
    for start, stop, label in [(-1, 1, 'negative ordinal'), (0, 577, 'out of range stop'),
                               (1, 1, 'empty range'), (2, 1, 'reversed range')]:
        damages.append(reject(lambda start=start, stop=stop: audit.audit(record, start, stop), label))
    damages.append(reject(lambda: audit.witness({}, {}), 'both zero gaps do not become gcd1'))
    for point, label in [(audit.LOW, 'closed lower root'), (audit.HIGH, 'closed upper root'),
                         ((audit.LOW + audit.HIGH) / 2, 'interior root')]:
        damages.append(reject(lambda point=point: audit.certify_nonzero({0: -point, 1: Q(1)}), label))
    f = {0: -audit.LOW, 1: Q(1)}
    h, _, _ = audit.witness(f, f)
    audit.need(h != {0: Q(1)}, 'merely common divisor1 is not a Bezout witness')
    damages.append(reject(lambda: audit.certify_nonzero(h), 'merely common divisor trap'))
    from check import construct

    def bad_gram(case):
        gram, f, g = construct(case, True)
        gram[0][0][0] += 1
        return gram, f, g

    def bad_gap(case):
        gram, f, g = construct(case, True)
        if f:
            f[0] += 1
        else:
            f = [Q(1)]
        return gram, f, g

    damages.append(reject(lambda: audit.audit(record, 0, 1, bad_gram), 'changed full Gram entry'))
    damages.append(reject(lambda: audit.audit(record, 0, 1, bad_gap), 'changed cross-gap field'))
    accepted = []
    reverse = deepcopy(record)
    reverse['rows'].reverse()
    audit.audit(reverse, 0, 1)
    accepted.append('literal row order reversed')
    permuted = deepcopy(record)
    count = len(permuted['root_free_polynomials'])
    permuted['root_free_polynomials'].reverse()
    for row in permuted['rows']:
        row[5] = count - 1 - row[5]
    audit.audit(permuted, 0, 1)
    accepted.append('root-free basis consistently permuted')
    h, u, v = audit.witness({}, {0: Q(2), 1: Q(1)})
    audit.certify_nonzero(h)
    audit.need(audit.plus(audit.times(u, {}), audit.times(v, {0: Q(2), 1: Q(1)})) == h,
               'one zero gap valid identity')
    accepted.append('one zero gap and root-free other gap')
    print(json.dumps({'status': 'complete', 'damages_rejected': len(damages), 'damage_labels': damages,
                      'valid_controls_accepted': len(accepted), 'valid_labels': accepted,
                      'control_arithmetic_ranges_are_deliberately_small': True,
                      'whole_theorem_coverage_requires_all_four_audit_ranges': True}, sort_keys=True))


if __name__ == '__main__':
    main()
