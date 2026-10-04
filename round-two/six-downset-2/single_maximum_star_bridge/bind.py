"""Private original-coordinate binding; parent PSD/gaps are explicit premises.

No peer native code or positivity factors are imported or replayed. All
point entries and every sparse affine basis are reconstructed exactly.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from math import lcm
from pathlib import Path

INPUT_SHA = '132c164b1e453d93d8d8e2df4d75789b0211cb605e0b80247bc8ec31e7de4feb'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def members():
    values = {0, 7}
    values.update(1 << i for i in range(19))
    values.update((1 << i) | (1 << j) for i in range(19) for j in range(i + 1, 19))
    for i in range(3, 19):
        values.add(3 | (1 << i))
        values.add(5 | (1 << i))
        if i >= 11:
            values.add(6 | (1 << i))
    # Separate complete literal membership predicate on the entire finite ground.
    literal = {v for v in range(1 << 19) if v.bit_count() <= 2 or
        (v.bit_count() == 3 and (v & 7).bit_count() >= 2 and
         not ((v & 6) == 6 and (v & ((1 << 11) - 8))))}
    require(values == literal and len(values) == 232, 'entire original carrier binding')
    require(all(v ^ (1 << i) in values for v in values for i in range(19) if v & (1 << i)),
            'original downward closure')
    return sorted(values)


def orbit(v):
    return v & 7, ((v >> 3) & 255).bit_count(), (v >> 11).bit_count()


def maximum_pivot(actual, pivot):
    sizes = [sum(bool(v & (1 << i)) for v in actual) for i in range(19)]
    require(pivot.bit_count() == 1 and pivot in actual and
            sizes[pivot.bit_length() - 1] == max(sizes) and
            sizes.count(max(sizes)) == 1, 'unique ACTUAL maximum-star singleton pivot')
    return sizes


def require_residual(actual, pivot, residual):
    require(residual == [v for v in actual if v not in (0, pivot)],
            'retain EVERY smaller-star singleton and residual member')


def original_core(actual, certificate):
    proper = actual[1:]
    residual = [v for v in proper if v != 1]
    denom = certificate['free_original_entry_denominator']
    require(type(denom) is int and denom == 1024, 'original common integer denominator')
    require((certificate['q'], certificate['k'], certificate['actual_empty_N'],
             certificate['maximum_star_s']) == (16, 8, 232, 52), 'exact parent carrier')
    keys = sorted({tuple(sorted((orbit(v), orbit(w)))) for i, v in enumerate(residual)
                   for w in residual[i + 1:] if not v & w})
    require([[list(x) for x in key] for key in keys] == certificate['free_original_entry_orbit_keys']
            and len(keys) == 143, 'entire original orbit key census')
    values = certificate['free_original_entry_numerators']
    require(len(values) == len(keys) and all(type(x) is int for x in values), 'all exact orbit values')
    table = dict(zip(keys, values))
    point = []
    for v in proper:
        point.append([51 * denom if v == w else -denom if v & w else
                      0 if 1 in (v, w) else table[tuple(sorted((orbit(v), orbit(w))))]
                      for w in proper])
    anchor = proper.index(1)
    star = [i for i, v in enumerate(proper) if v & 1]
    for i, v in enumerate(proper):
        if not v & 1:
            point[i][anchor] = point[anchor][i] = -sum(point[i][j] for j in star if j != anchor)
    require(all(sum(point[i][j] for j in star) == 0 for i in range(len(proper))),
            'complete original core maximum-star action')
    return point, denom


def lift_proper(core, denom):
    sums = [sum(row) for row in core]
    return [[denom + sum(sums)] + [denom - x for x in sums]] + [
        [denom - sums[i]] + [denom + x for x in row] for i, row in enumerate(core)]


def residual_congruence(matrix, r):
    """A K A^T, with Q identity rows, pivot -r and actual empty -(1-r)."""
    b = [1 - x for x in r]
    rs = [sum(matrix[i][j] for i in range(len(r)) if r[i]) for j in range(len(r))]
    bs = [sum(matrix[i][j] for i in range(len(r)) if b[i]) for j in range(len(r))]
    rr = sum(rs[j] for j in range(len(r)) if r[j])
    rb = sum(rs[j] for j in range(len(r)) if b[j])
    bb = sum(bs[j] for j in range(len(r)) if b[j])
    return [[bb, rb] + [-x for x in bs], [rb, rr] + [-x for x in rs]] + [
        [-bs[i], -rs[i]] + row[:] for i, row in enumerate(matrix)]


def outer(v, w):
    result = {}
    for i, x in v.items():
        for j, y in w.items():
            result[i, j] = result.get((i, j), 0) + x * y
            result[j, i] = result.get((j, i), 0) + x * y
    return {key: value for key, value in result.items() if value}


def original_anchor_basis(i, j, r, pivot):
    result = {(i, j): 1, (j, i): 1}
    for row, other in [(i, j), (j, i)]:
        if r[other]:
            result[row, pivot] = result[pivot, row] = -1
    return result


def expected_failure(name, work):
    try:
        work()
    except ValueError:
        return name
    raise ValueError('Damaged mathematical condition escaped: ' + name)


def bind(certificate):
    actual = members()
    sizes = maximum_pivot(actual, 1)
    require(sizes == [52, 44, 44] + [21] * 8 + [22] * 8, 'every original point-star size')
    q = [v for v in actual if v not in (0, 1)]
    require_residual(actual, 1, q)
    require(len(q) == 230 and 2 in q and 4 in q, 'all smaller-star singleton coordinates present')
    core, denom = original_core(actual, certificate)
    # An independently decoded principal block and residual-first completion.
    pi = {v: i for i, v in enumerate(actual[1:])}
    t = [[core[pi[v]][pi[w]] for w in q] for v in q]
    require(all(t[i][j] == (51 * denom if i == j else -denom)
                for i, v in enumerate(q) for j, w in enumerate(q) if i == j or v & w),
            'complete fixed residual profile, parent deletion k8 is NOT diagonal k0=51')
    r = [int(bool(v & 1)) for v in q]
    b = [1 - x for x in r]
    require(sum(r) == 51 and sum(b) == 179, 'complete incidence groups')
    lift = lift_proper(core, denom)
    lift_from_t = [[x + denom for x in row] for row in residual_congruence(t, r)]
    require(actual == [0, 1] + q and lift == lift_from_t, 'EVERY original entry including actual empty')
    require(all(sum(row) == 232 * denom for row in lift), 'every original row')
    require(all(lift[i][j] == lift[j][i] and
                (not v & w or lift[i][j] == 52 * denom * int(i == j))
                for i, v in enumerate(actual) for j, w in enumerate(actual)), 'entire original M support')
    star_energies = []
    for mark, size in enumerate(sizes):
        w = [int(bool(v & (1 << mark))) for v in actual]
        action = [sum(x * y for x, y in zip(row, w)) for row in lift]
        energy = sum(wi * x for wi, x in zip(w, action)) * 232**2 - denom * 232**2 * size**2
        require(energy == denom * 232**2 * size * (52 - size), 'actual centered point-star energies')
        if mark == 0:
            require(action == [52 * denom] * 232, 'entire original maximum-star action')
        else:
            require(energy > 0, 'smaller stars are NOT forced kernels')
        star_energies.append(energy)

    columns = [{i + 2: 1, 1 if r[i] else 0: -1} for i in range(len(q))]
    g = [[sum(x * columns[j].get(k, 0) for k, x in columns[i].items())
          for j in range(len(q))] for i in range(len(q))]
    require(g == [[int(i == j) + r[i] * r[j] + b[i] * b[j]
                   for j in range(len(q))] for i in range(len(q))], 'EVERY actual metric entry')
    clear = lcm(52, 180)
    gi = [[clear * int(i == j) - (clear // 52) * r[i] * r[j] - (clear // 180) * b[i] * b[j]
           for j in range(len(q))] for i in range(len(q))]
    groupcols = [[sum(gi[k][j] for k in range(len(q)) if r[k] == group)
                  for j in range(len(q))] for group in (0, 1)]
    require(all(gi[i][j] + groupcols[r[i]][j] == clear * int(i == j)
                and gi[i][j] + groupcols[r[j]][i] == clear * int(i == j)
                for i in range(len(q)) for j in range(len(q))), 'ALL entries of BOTH exact metric inverse products')
    reduced_cap = [[232 * denom * gi[i][j] - clear * t[i][j]
                    for j in range(len(q))] for i in range(len(q))]
    cap_lift = residual_congruence(reduced_cap, r)
    centered = [232 * int(bool(v & 1)) - 52 for v in actual]
    require(sum(x*x for x in centered) == 232 * 52 * 180 and clear * denom % (52 * 180) == 0,
            'exact original centered-star projector')
    pay = clear * denom // (52 * 180)
    require(all(clear * (232 * denom * int(i == j) - lift[i][j]) ==
                cap_lift[i][j] + pay * centered[i] * centered[j]
                for i in range(232) for j in range(232)), 'EVERY original cap identity entry')

    free = [(i, j) for i, v in enumerate(q) for j in range(i + 1, len(q)) if not v & q[j]]
    degrees = [sum(not v & w for w in q if w != v) for v in q]
    require(len(free) == 20103 and max(degrees) == 209, 'entire finite coordinate dimension and maximum degree')
    all_proper_free = sum(not v & w for i, v in enumerate(actual[1:]) for w in actual[i + 2:])
    require(all_proper_free == 20282 and all_proper_free - len(free) == 179,
            'distinct complete original anchored-variable count')
    basis = []
    for i, j in free:
        f_i = {i: 1, -1: -r[i]} if r[i] else {i: 1}
        f_j = {j: 1, -1: -r[j]} if r[j] else {j: 1}
        proper_delta = outer(f_i, f_j)
        original_delta = original_anchor_basis(i, j, r, -1)
        require(proper_delta == original_delta and not (r[i] and r[j]), 'ALL original anchored basis coefficients')
        full_delta = outer(columns[i], columns[j])
        require(all(sum(x for (a, _), x in full_delta.items() if a == row) == 0
                    for row in {a for a, _ in full_delta}), 'every sparse original basis row')
        require(all(not actual[a] & actual[c] for a, c in full_delta), 'every sparse original basis support')
        require(all(sum(x for (a, c), x in full_delta.items() if a == row and actual[c] & 1) == 0
                    for row in {a for a, _ in full_delta}), 'every sparse original basis maximum-star action')
        basis.append([q[i], q[j], [[a, c, x] for (a, c), x in sorted(full_delta.items())]])

    def wrong_anchor():
        damaged = [row[:] for row in core]
        damaged[actual[1:].index(2)][0] += 1
        star = [i for i, v in enumerate(actual[1:]) if v & 1]
        require(all(sum(row[j] for j in star) == 0 for row in damaged), 'original anchor action')

    failures = [
        expected_failure('smaller_star_pivot', lambda: maximum_pivot(actual, 2)),
        expected_failure('removed_smaller_singleton', lambda: require_residual(actual, 1, [v for v in q if v != 2])),
        expected_failure('wrong_original_anchor', wrong_anchor),
        expected_failure('omitted_actual_empty_metric', lambda: require(g == [[int(i == j) + r[i]*r[j]
            for j in range(len(q))] for i in range(len(q))], 'actual empty metric term')),
        expected_failure('full_lift_norm_paid_as_proper_lift', lambda: require(max(52, 180) == 52, 'distinct actual lift norm')),
        expected_failure('imported_whole_ground_saturation', lambda: require(any(v ^ ((1 << 19) - 1) in q for v in q), 'no complementary residual endpoints'))
    ]
    require(core[pi[8]][pi[48]] == -583, 'credited original outside-five-face baseline')
    rho = Fraction(1, 256 * 52 * max(degrees))
    record = dict(agent='six-downset-2', role='researcher', actual=actual, q=q, core_denominator=denom,
        original_C_numerators=core, original_L_numerators=lift, residual_T_numerators=t,
        actual_G=g, actual_G_inverse_denominator=clear, actual_G_inverse_numerators=gi,
        reduced_cap_denominator=clear*denom, reduced_cap_numerators=reduced_cap,
        complete_original_sparse_basis=basis, residual_degrees=degrees, original_star_energies=star_energies)
    summary = dict(agent='six-downset-2', role='researcher', source_parent='10242/0',
        parent_source_commit='52ce9643a4eb700056e37c0df6e3ed3736f71808',
        carrier=dict(N=232,s=52,h=180,p=1,m=230,all19_star_sizes=sizes,selected_whole_ground_pairs=0),
        complete_original_core_entries=231**2, complete_original_lift_entries=232**2,
        complete_original_cap_identity_entries=232**2, entire_metric_inverse_product_entries=2*230**2,
        complete_original_basis_count=len(basis), sparse_basis_positions=sum(len(x[2]) for x in basis),
        proper_lift_squared_norm=52, actual_empty_lift_squared_norm=180,
        G_spectrum={'52':1,'180':1,'1':228}, trace_G=460, maximum_residual_disjoint_degree=max(degrees),
        radius_if_parent_core_margins_hold=str(rho), original_L_gap_if_parent_margins_hold='1/256',
        M_endpoint_gap_if_parent_margins_hold='1/46080',
        prior_parent_cube_radius='1/10292736', radius_factor=str(rho/Fraction(1,10292736)),
        rejected_mathematical_damages=failures, parent_PSD_and_gaps_reaudited=False,
        parent_core_margin_premise='C on proper a-star perpendicular >=1/128 and U>=1/128',
        current_new_result='Private entire original q16 point/basis binding to the one-maximum-star incidence cone',
        generic_degree_box_superseded_by_independent_Frobenius_source='c393814322f69f914bedef7ad1a327e07241634c',
        independently_reviewed=False, ordinary_real_bridges_unformalized=True)
    return record, summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate', type=Path, required=True)
    ap.add_argument('--record', type=Path, required=True)
    args = ap.parse_args()
    raw = args.certificate.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == INPUT_SHA, 'entire pinned published peer coefficient input')
    record, summary = bind(json.loads(raw))
    out = (json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n').encode()
    args.record.write_bytes(out)
    summary.update(complete_record_bytes=len(out), complete_record_sha256=hashlib.sha256(out).hexdigest())
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
