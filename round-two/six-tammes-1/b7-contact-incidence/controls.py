"""Semantic damage and arithmetic controls, using once-regenerated references."""
from copy import deepcopy
from pathlib import Path
from fractions import Fraction as F
import json
import check
import audit


def require(ok, why):
    if not ok:
        raise ValueError(why)


def damages(reference):
    mutations = []
    def add_case(name, change):
        copy = deepcopy(reference)
        change(copy)
        mutations.append((name, copy))
    add_case('widen-closed-cosine-band', lambda c: c['cosine_closed_band'].__setitem__(0, '1/2'))
    add_case('open-r-band-endpoint', lambda c: c['r_closed_band'].__setitem__(1, '749/1000'))
    add_case('omit-complete-contact-hypothesis', lambda c: c.__setitem__('physical_interface', 'chosen edge subgraph'))
    add_case('alias-two-core-corners', lambda c: c['B'][0].__setitem__(2, 2))
    add_case('omit-a-rooted-shape', lambda c: c['all_shapes'].pop())
    add_case('omit-a-parent-order', lambda c: c['history_multiplicities'].__setitem__(0, c['history_multiplicities'][0]-1))
    add_case('erase-first-reuse-probe', lambda c: c['freshness'].__setitem__('normalized_collision_tests', 1529))
    add_case('alter-first-reuse-polynomial-binding', lambda c: c['freshness'].__setitem__('whole_normalized_polynomial_digest', '0'*64))
    add_case('erase-packing-rejection', lambda c: next(r for r in c['packing'] if r['rejecting_pair']).__setitem__('rejecting_pair', None))
    add_case('allow-triangle-across-actual-P', lambda c: c['actual_P_shapes'].append(next(i for i in c['packing_compatible_shapes'] if i not in c['actual_P_shapes'])))
    add_case('drop-one-shared-ear-assignment', lambda c: c['overlap_rows'].pop())
    add_case('allow-two-shared-ears', lambda c: c['overlap_rows'][0].__setitem__(1, 6) or c['overlap_rows'][0].__setitem__(2, 7))
    add_case('omit-grid-path', lambda c: c.__setitem__('raw_increment_paths', 529))
    add_case('delete-extra-contact-edge', lambda c: c['geometric_maps'][0]['cross'].pop())
    add_case('alias-nontriangle-corner', lambda c: c['geometric_maps'][0]['faces'][0].__setitem__(1, c['geometric_maps'][0]['faces'][0][0]))
    add_case('erase-degree-or-convexity-screen', lambda c: c.__setitem__('whole_annulus_filter_digest', '1'*64))
    add_case('reverse-root-free-equation-sign', lambda c: next(r for r in c['algebra'] if r['status'] == 'excluded-equation')['witness'][1].__setitem__(1, '999'))
    add_case('replace-gcd-with-zero', lambda c: next(r for r in c['algebra'] if r['status'] == 'excluded-gcd').__setitem__('witness', []))
    add_case('change-four-vector-Gram-binding', lambda c: c.__setitem__('whole_necessary_equations_digest', '2'*64))
    add_case('change-incumbent-polynomial', lambda c: c['critical_r_polynomial'].__setitem__(0, '-3'))
    add_case('admit-critical-map-as-strict-improvement', lambda c: c['strict_improvement_maps'].append(next(r['map'] for r in c['algebra'] if r['status'] == 'critical-only')))
    add_case('omit-full-band-map', lambda c: c['full_band_maps'].pop())
    add_case('boolean-for-corner-integer', lambda c: c['B'][0].__setitem__(0, True))
    add_case('float-for-count-integer', lambda c: c.__setitem__('raw_increment_paths', 530.0))
    add_case('unknown-certificate-field', lambda c: c.__setitem__('unproved-realizability', True))
    return mutations


def arithmetic_controls():
    # A rank-three Gram matrix of four literal reflected unit vectors.
    dp = check.core('B')
    sp = audit.points(tuple(sorted(tuple(sorted(t)) for t in audit.B)))
    names = (1, 2, 4, 10)
    dense = [[check.inner(dp[i], dp[j]) for j in names] for i in names]
    sparse = [[audit.gram(sp[i], sp[j]) for j in names] for i in names]
    require(not check.determinant(dense) and not audit.bareiss(sparse), 'actual rank-three Gram determinant')
    # Rank four is not silently admitted. This also exercises exact Bareiss divisions.
    dd = [[check.D if i == j else [] for j in range(4)] for i in range(4)]
    ss = [[audit.D if i == j else {} for j in range(4)] for i in range(4)]
    dvalue, svalue = check.determinant(dd), audit.bareiss(ss)
    require(check.sign(dvalue) == audit.bernstein_sign(svalue) == 1, 'false rank-four matrix has strict positive determinant')
    dd[0], dd[1] = dd[1], dd[0]
    ss[0], ss[1] = ss[1], ss[0]
    require(check.sign(check.determinant(dd)) == audit.bernstein_sign(audit.bareiss(ss)) == -1, 'row exchange reverses determinant sign')
    # A root IN the band must never be called root-free.
    crossing = [F(-29, 40), F(1)]
    require(check.sign(crossing) == audit.bernstein_sign(audit.P(*crossing)) == 0, 'mixed Bernstein signs stay unresolved')
    # Common root is outside the band; both exact Euclidean kernels retain it.
    from poly import mul, bezout, add
    p = mul([F(-4, 5), F(1)], [F(-1, 3), F(1)])
    q = mul([F(-4, 5), F(1)], [F(1), F(1)])
    h, u, v = bezout(p, q)
    sh = audit.common_divisor(audit.P(*p), audit.P(*q))
    require(check.encode(h) == audit.serial_poly(sh), 'entire common divisor')
    require(add(mul(u, p), mul(v, q)) == h and check.sign(h) == audit.bernstein_sign(sh) == -1, 'Bezout and root-free common divisor')
    # Exact change of variable of the KNOWN table polynomial; no new construction.
    def power(p, n):
        result = [F(1)]
        for _ in range(n):
            result = mul(result, p)
        return result
    transformed = []
    for i, coefficient in enumerate((-1, -3, 2, 6, -1, 13)):
        transformed = add(transformed, [coefficient*x for x in mul(power(check.R, i), power(check.D, 5-i))])
    require(transformed == [16*x for x in check.G], 'entire incumbent polynomial identity')
    return ['rank-three-actual-Gram', 'rank-four-rejected', 'Bareiss-row-exchange',
            'in-band-root-unresolved', 'root-free-common-divisor', 'known-incumbent-change-of-variable']


def main():
    record = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    truth = check.build()
    separate = audit.build()
    require(check.canonical(truth) == audit.serialize(separate), 'all separately regenerated certificate bytes')
    controls = damages(record)
    for name, altered in controls:
        for module, expected in ((check, truth), (audit, separate)):
            try:
                module.verify(altered, expected)
            except ValueError:
                continue
            raise ValueError('accepted semantic damage: ' + name)
    valid = [deepcopy(record), json.loads(json.dumps(record, indent=7)), dict(reversed(list(record.items())))]
    for representation in valid:
        check.verify(representation, truth)
        audit.verify(representation, separate)
    print(check.canonical({'status': 'complete', 'semantic_damages_rejected_by_both': len(controls),
                           'damages': [name for name, _ in controls],
                           'valid_representations_accepted_by_both': len(valid),
                           'arithmetic_controls': arithmetic_controls()}), end='')


if __name__ == '__main__':
    main()
