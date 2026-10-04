"""Independent original-equation controls of the ordinary written proof.

Normal and optimized modes must regenerate the same whole record. The
n28 seed theorem is an explicit external premise; this checker does NOT
replay, replace or independently review that seed or the real proof.
"""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from math import comb
from pathlib import Path
from linear import Rejected, encoded, identity, inverse, multiply, psd_rank, rank, require, rref, transpose, zeros
from model import build_T, counts, cycle, downset, literal, original, original_equations, parameters, path, validate_T


def direct_equations(data):
    """Build every equation from literal ORIGINAL M entries, not A/T."""
    members, n, N, s, h = data['members'], data['n'], data['N'], data['s'], data['h']
    qi = {members.index(a) for a in data['remaining']}
    unknown = [(i, j) for i in range(N) for j in range(i, N) if not (members[i] & members[j])]
    tail = {(members.index(a), members.index(b)) for a, b in data['edges']}
    unknown.sort(key=lambda pair: (pair in tail, pair))
    pos = {pair: i for i, pair in enumerate(unknown)}

    def index(i, j):
        return pos.get(tuple(sorted((i, j))))

    def equation(terms, rhs):
        row = [Q(0)]*len(unknown)+[Q(rhs)]
        for i, j, value in terms:
            at = index(i, j)
            if at is not None:
                row[at] += value
        return row

    rows = []
    for i, a in enumerate(members):
        rows.append(equation([(i, j, Q(1)) for j in range(N)], Q(1)))
        for p in data['maxpoints']:
            rows.append(equation([(i, j, Q(1)) for j, b in enumerate(members) if b & (1 << p)], Q(s, h)*(not bool(a & (1 << p)))))
        for a1, a2 in data['saturated']:
            x, y = members.index(a1), members.index(a2)
            rows.append(equation([(i, x, Q(1)), (i, y, Q(-1))], Q(s, h)*((i == y)-(i == x))))
    reduced, pivots = rref(rows, len(unknown))
    free = [i for i in range(len(unknown)) if i not in pivots]
    require({unknown[i] for i in free} == tail, 'ENTIRE independent original free coordinate set')
    require(len(free) == len(data['edges']), 'Independent original affine dimension')
    require(all(unknown[i][0] in qi and unknown[i][1] in qi for i in free), 'Only surviving residual coordinates')

    def recover(T):
        values = [Q(0)]*len(unknown)
        qpos = {a: i for i, a in enumerate(data['residual'])}
        for i in free:
            a, b = (members[j] for j in unknown[i])
            values[i] = (T[qpos[a]][qpos[b]]+1)/h
        for row, col in zip(reduced, pivots):
            values[col] = row[-1]-sum(row[i]*values[i] for i in free)
        M = zeros(N, N)
        for (i, j), value in zip(unknown, values):
            M[i][j] = M[j][i] = value
        return M

    record = dict(unknown_positions=unknown, original_equations=len(rows), original_rank=len(pivots),
                  free_positions=[unknown[i] for i in free],
                  complete_sparse_reduced_rows=[[(j, str(v)) for j, v in enumerate(row) if v] for row in reduced])
    return recover, record


def metric_control(data, T):
    A, R, N, n, p = data['A'], data['R'], data['N'], data['n'], data['p']
    G = multiply(transpose(A), A)
    rr = multiply(R, transpose(R))
    qs = data['residual']
    r = [sum(bool(a & (1 << i)) for i in data['maxpoints']) for a in qs]
    b = [Q(1-count) for count in r]
    prescribed = [[Q(i == j)+rr[i][j]+b[i]*b[j] for j in range(len(qs))] for i in range(len(qs))]
    require(G == prescribed, 'Full ordinary Euclidean cap metric')
    inv = inverse(G)
    PA = multiply(multiply(A, inv), transpose(A))
    PU = [[Q(i == j)-Q(1, N)-PA[i][j] for j in range(N)] for i in range(N)]
    require(multiply(PU, PU) == PU and multiply(PU, PA) == zeros(N, N), 'Entire original orthogonal projector')
    require(rank(PU) == p and psd_rank(PU) == p, 'Full original maximum-star projector rank and PSD')
    L, M = original(data, T)
    B = [[N*inv[i][j]-T[i][j] for j in range(len(qs))] for i in range(len(qs))]
    reduced_cap = multiply(multiply(A, B), transpose(A))
    cap = [[N*Q(i == j)-L[i][j] for j in range(N)] for i in range(N)]
    require(cap == [[N*PU[i][j]+reduced_cap[i][j] for j in range(N)] for i in range(N)],
            'EVERY original cap-congruence entry')
    gamma = sum(count**2-count+2 for count in r)
    require(sum(G[i][i] for i in range(len(qs))) == gamma, 'Exact full metric trace formula')
    if data['name'] == 'near_cube':
        require(gamma == n*(n-1)*(2**(n-2)-n+1)+2*(N-n-1), 'Near-cube metric trace specialization')
    return dict(G=encoded(G), inverse_G=encoded(inv), full_original_projector=encoded(PU),
                original_cap=encoded(cap), reduced_cap=encoded(B), trace_G=gamma)


def affine_control(n, saturated, data=None):
    if data is None:
        data = literal(n, saturated)
    recover, record = direct_equations(data)
    dim = len(data['edges'])
    inputs = [[Q(0)]*dim]
    inputs += [[Q(i == j) for i in range(dim)] for j in range(dim)]
    if dim:
        inputs += [[Q((i % 7)-3, i+5) for i in range(dim)]]
    entire = []
    for values in inputs:
        T = build_T(data, values)
        L, M = original(data, T)
        full_direct = recover(T)
        require(M == full_direct, 'WHOLE original RREF/lift reconstruction equality')
        original_equations(data, M)
        recovered = [[L[data['members'].index(a)][data['members'].index(b)]-1 for b in data['residual']] for a in data['residual']]
        require(recovered == T, 'WHOLE T recovery including all complements')
        C = [[L[i][j]-1 for j in range(1, data['N'])] for i in range(1, data['N'])]
        W = identity(data['p'])+data['R']
        require(multiply(C, W) == zeros(data['N']-1, data['p']), 'Every original nonempty maximum-star kernel coordinate')
        entire.append(dict(parameters=[str(x) for x in values], original_M=encoded(M), T=encoded(T)))
    return dict(name=data['name'], n=n, p=data['p'], star_sizes=data['star_sizes'], saturated=[list(p) for p in saturated], affine_dimension=dim,
                original_member_count=data['N'], complete_original_matrices=len(inputs),
                independent_system=record, full_matrix_checks=entire,
                metric=metric_control(data, build_T(data, inputs[0])),
                affine_only_not_a_positive_seed=True)


def positive_and_wrong_metric():
    data = literal(4)
    T = build_T(data, [Q(3, 2)]*len(data['edges']))
    L, M = original(data, T)
    original_equations(data, M)
    G = multiply(transpose(data['A']), data['A'])
    inv = inverse(G)
    B = [[data['N']*inv[i][j]-T[i][j] for j in range(6)] for i in range(6)]
    cap = [[data['N']*Q(i == j)-L[i][j] for j in range(data['N'])] for i in range(data['N'])]
    require(psd_rank(T) == 6 and psd_rank(B) == 6, 'Both reduced positive cones')
    require(psd_rank(L) == 7 and psd_rank(cap) == 10, 'Original lower/upper ranks at positive control')

    wrong_T = build_T(data, [Q(2)]*len(data['edges']))
    wrong_L, wrong_M = original(data, wrong_T)
    original_equations(data, wrong_M)
    require(psd_rank(wrong_T) == 6, 'Wrong-metric example is ordinary H')
    naive = [[data['N']*Q(i == j)-wrong_T[i][j] for j in range(6)] for i in range(6)]
    require(psd_rank(naive) == 6, 'Wrong naive metric passes')
    x = [sum(row) for row in data['A']]
    false_cap = [[data['N']*Q(i == j)-wrong_L[i][j] for j in range(data['N'])] for i in range(data['N'])]
    energy = sum(x[i]*false_cap[i][j]*x[j] for i in range(data['N']) for j in range(data['N']))
    require(energy == -156, 'Literal original negative cap energy')
    return dict(positive_original_M=encoded(M), positive_T=encoded(T), positive_reduced_cap=encoded(B),
                lower_rank=7, cap_rank=10, wrong_metric_original_M=encoded(wrong_M),
                wrong_metric_original_test=[str(v) for v in x], wrong_metric_cap_energy=str(energy),
                wrong_metric_T_PSD=True, wrong_metric_NI_minus_T_PSD=True)


def positive_regular_cycle():
    data = cycle(5)
    T = build_T(data, [Q(1, 5)]*len(data['edges']))
    L, M = original(data, T)
    original_equations(data, M)
    G = multiply(transpose(data['A']), data['A'])
    inv = inverse(G)
    B = [[data['N']*inv[i][j]-T[i][j] for j in range(len(T))] for i in range(len(T))]
    cap = [[data['N']*Q(i == j)-L[i][j] for j in range(data['N'])] for i in range(data['N'])]
    require(psd_rank(T) == 5 and psd_rank(B) == 5, 'Non-near-cube regular reduced positive cones')
    require(psd_rank(L) == 6 and psd_rank(cap) == 10, 'Non-near-cube original lower and cap ranks')
    return dict(original_members=data['members'], original_M=encoded(M), T=encoded(T),
                reduced_cap=encoded(B), lower_rank=6, cap_rank=10, common_star=data['s'])


def positive_nonregular_path():
    data = path()
    T = build_T(data, [Q(-1) if pair == (1, 4) else Q(1) for pair in data['edges']])
    L, M = original(data, T)
    original_equations(data, M)
    G = multiply(transpose(data['A']), data['A'])
    inv = inverse(G)
    B = [[data['N']*inv[i][j]-T[i][j] for j in range(len(T))] for i in range(len(T))]
    cap = [[data['N']*Q(i == j)-L[i][j] for j in range(data['N'])] for i in range(data['N'])]
    require(psd_rank(T) == 4 and psd_rank(B) == 4, 'Both nonregular residual positive cones')
    require(psd_rank(L) == 5 and psd_rank(cap) == 5, 'Original nonregular lower and upper ranks')
    row = data['members'].index(2)
    smaller_action = sum(M[row][j] for j, member in enumerate(data['members']) if member & 1)
    require(smaller_action == Q(1, 3) and smaller_action != Q(data['s'], data['h']),
            'Smaller-star direction is NOT forced as a maximum star')
    return dict(original_members=data['members'], original_M=encoded(M), T=encoded(T),
                reduced_cap=encoded(B), lower_rank=5, cap_rank=5, maxpoints=data['maxpoints'],
                star_sizes=data['star_sizes'], residual_includes_smaller_star_singletons=True,
                smaller_star_action=str(smaller_action), incorrect_maximum_star_action='1')


def positive_cap_boundary():
    data = downset(2, [0, 1, 2, 3])
    T = build_T(data, [])
    L, M = original(data, T)
    original_equations(data, M)
    G = multiply(transpose(data['A']), data['A'])
    B = [[data['N']*inverse(G)[0][0]-T[0][0]]]
    cap = [[data['N']*Q(i == j)-L[i][j] for j in range(data['N'])] for i in range(data['N'])]
    require(psd_rank(T) == 1 and psd_rank(B) == 0, 'Zero reduced cap cone is retained')
    require(psd_rank(L) == 2 and psd_rank(cap) == 2, 'Original cap boundary has two unit directions')
    return dict(original_M=encoded(M), T=encoded(T), reduced_cap=encoded(B),
                lower_rank=2, cap_rank=2, unit_multiplicity=2)


def damage_controls():
    names = []

    def reject(name, fn):
        try:
            fn()
        except Rejected:
            names.append(name)
            return
        raise Rejected('Semantic damage accepted: '+name)

    d = literal(4)
    T = build_T(d, [Q(3, 2)]*3)
    L, M = original(d, T)
    reject('noninteger_order', lambda: literal(Q(4)))
    reject('proper_pair_is_not_whole_ground_complement', lambda: literal(5, [(3, 12)]))
    reject('duplicate_saturated_pair', lambda: literal(4, [(3, 12), (12, 3)]))
    reject('omitted_complement_parameter', lambda: build_T(d, [Q(0)]*2))
    reject('floating_parameter', lambda: build_T(d, [0.0]*3))
    bad = [row[:] for row in T]; bad[0][0] += 1
    reject('wrong_fixed_diagonal', lambda: validate_T(d, bad))
    bad_intersection = [row[:] for row in T]
    i, j = next((i, j) for i, a in enumerate(d['residual']) for j, b in enumerate(d['residual']) if i != j and a & b)
    bad_intersection[i][j] = bad_intersection[j][i] = Q(0)
    reject('intersecting_higher_entry', lambda: validate_T(d, bad_intersection))
    no_empty = [row[:] for row in M]; no_empty[0] = [Q(0)]*d['N']
    for row in no_empty: row[0] = Q(0)
    reject('deleted_actual_empty_row', lambda: original_equations(d, no_empty))
    bad_star = [row[:] for row in M]
    a, b = d['edges'][0]; i, j = d['members'].index(a), d['members'].index(b)
    bad_star[i][j] += 1; bad_star[j][i] += 1
    bad_star[0][i] -= 1; bad_star[i][0] -= 1
    bad_star[0][j] -= 1; bad_star[j][0] -= 1; bad_star[0][0] += 2
    require(all(sum(row) == 1 for row in bad_star), 'Star damage preserves whole row sums')
    reject('supported_row_one_without_star_equations', lambda: original_equations(d, bad_star))
    return names


def finish_damage_controls(names):
    def reject(name, fn):
        try:
            fn()
        except Rejected:
            names.append(name); return
        raise Rejected('Semantic damage accepted: '+name)
    ds = literal(5, [(3, 28)])
    bad_sat = build_T(ds, [Q(0)]*len(ds['edges']))
    frozen = ds['residual'].index(3)
    other = next(z for z, a in enumerate(ds['residual']) if not (a & 3) and a != 28)
    bad_sat[frozen][other] = bad_sat[other][frozen] = Q(0)
    reject('saturated_value_without_entire_column_equality', lambda: validate_T(ds, bad_sat))
    d = literal(4)
    G = multiply(transpose(d['A']), d['A'])
    omitted = [[Q(i == j)+v for j, v in enumerate(row)] for i, row in enumerate(multiply(d['R'], transpose(d['R'])))]
    reject('empty_term_omitted_from_metric', lambda: require(omitted == G, 'Actual empty term required'))
    wrong_inverse = inverse(G); wrong_inverse[0][0] += 1
    reject('wrong_exact_metric_inverse', lambda: require(multiply(G, wrong_inverse) == identity(6), 'Metric inverse product'))
    proper = [(a, b) for a, b in d['edges'] if (a | b) != 15]
    reject('whole_ground_complements_removed_from_count', lambda: require(proper == d['edges'], 'Every complement is a free coordinate'))
    wrong_T = build_T(d, [Q(2)]*3)
    wrong_L, _ = original(d, wrong_T)
    wrong_cap = [[d['N']*Q(i == j)-wrong_L[i][j] for j in range(d['N'])] for i in range(d['N'])]
    reject('naive_metric_misses_original_cap_failure', lambda: psd_rank(wrong_cap))
    pn = path()
    Tn = build_T(pn, [Q(-1) if pair == (1,4) else Q(1) for pair in pn['edges']])
    _, Mn = original(pn, Tn)
    wrong_stars = dict(pn, maxpoints=list(range(3)))
    reject('incorrectly_forcing_smaller_point_stars', lambda: original_equations(wrong_stars, Mn))
    return names


def run():
    controls = [affine_control(4, []), affine_control(5, []),
                affine_control(4, [(3, 12)]), affine_control(5, [(3, 28), (5, 26)]),
                affine_control(4, [(3, 12), (5, 10), (6, 9)]), affine_control(5, [], cycle(5)),
                affine_control(3, [], path()), affine_control(3, [(1, 6)], path([(1, 6)])),
                affine_control(2, [], downset(2, [0, 1, 2, 3]))]
    small_counts = []
    for n in (4, 5, 6):
        d = literal(n); c = counts(n, 2, n-2)
        require(c['dimension'] == len(d['edges']), 'Literal independent full higher-edge count')
        small_counts.append(c)
    c28 = counts(28, 9, 19)
    cube = Q(1, 10**8)/(4*c28['trace_G']*c28['maximum_degree'])
    q = sum(comb(28, a) for a in range(2, 9))
    N, s, h, k = parameters(28)
    large = dict(c28, seed='10208/0 explicit theorem premise, not re-audited here',
                 seed_source_commit='8dd0fd663b047d525540a285901461388e696323',
                 lower_seed_floor='1/100000000', cube_radius=str(cube),
                 saturated_pair_count=q, lower_rank=N-28-q, cap_rank=N-1,
                 noninvariant_slice_dimension=c28['dimension']-c28['invariant_dimension'],
                 L_two_endpoint_gap='3/400000000', M_two_endpoint_gap=str(Q(3, 400000000*h)),
                 changes_actual_empty_and_unsaturated_complements=True,
                 entire_original_matrix_generated=False)
    rejected = finish_damage_controls(damage_controls())
    return dict(agent='six-downset-2', role='researcher', ordinary_real_proof_unformalized=True,
                independently_reviewed=False, affine_controls=controls, small_counts=small_counts,
                positive_and_wrong_metric=positive_and_wrong_metric(), positive_regular_cycle=positive_regular_cycle(),
                positive_nonregular_path=positive_nonregular_path(), positive_cap_boundary=positive_cap_boundary(), n28_conditional_face=large,
                semantic_rejections=rejected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    record = run()
    raw = (json.dumps(record, sort_keys=True, separators=(',', ':'))+'\n').encode()
    if args.record:
        args.record.write_bytes(raw)
    summary = dict(agent=record['agent'], role=record['role'], standard_library_only=True,
                   ordinary_real_proof_unformalized=True, independently_reviewed=False,
                   seed10208_is_explicit_premise=True, full_record_bytes=len(raw),
                   full_record_sha256=hashlib.sha256(raw).hexdigest(),
                   affine_controls=[{k:c[k] for k in ['name','n','p','star_sizes','saturated','affine_dimension','original_member_count','complete_original_matrices']} |
                                    {k:c['independent_system'][k] for k in ['original_equations','original_rank']} for c in record['affine_controls']],
                   complete_original_entry_comparisons=sum(c['original_member_count']**2*c['complete_original_matrices'] for c in record['affine_controls']),
                   original_star_actions=sum(c['p']*c['original_member_count']*c['complete_original_matrices'] for c in record['affine_controls']),
                   reduced_and_original_positive_ranks=[6,6,7,10], positive_regular_cycle_ranks=[5,5,6,10],
                   positive_nonregular_path_ranks=[4,4,5,5], positive_cap_boundary_ranks=[1,0,2,2], wrong_metric_cap_energy='-156',
                   n28_conditional_face=record['n28_conditional_face'], semantic_rejections=record['semantic_rejections'])
    if args.check:
        require(summary == json.loads(args.check.read_text()), 'ENTIRE compact expected record')
    print(json.dumps(summary, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
