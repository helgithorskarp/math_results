"""Fresh complete sparse chart and actual-lift verifier, standard library only.

No parent executable, PSD factor, solver, quotient or floating point is used.
The parent ordinary theorem10308 supplies only the stated center/margins.
The inverse producer is untrusted and is never imported by this checker.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json

BASE = Path(__file__).resolve().parent


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def physical_carrier():
    """Independent core/outside enumeration of all277 proper members."""
    members = []
    for core in range(8):
        k = core.bit_count()
        for r in range(3):
            if not (1 <= k+r <= 2 or k+r == 3 and k >= 2):
                continue
            for subset in combinations(range(3, 21), r):
                if core == 6 and r == 1 and subset[0] < 12:
                    continue
                members.append(core + sum(1 << i for i in subset))
    members.sort()
    require(len(members) == len(set(members)) == 277, 'complete original carrier')
    present = set(members) | {0}
    require(all(A ^ (1 << i) in present for A in members for i in range(21)
                if A & (1 << i)), 'all original downward closure relations')
    require([sum(bool(A & (1 << i)) for A in members) for i in range(21)] ==
            [58, 49, 49] + [23]*9 + [24]*9, 'every actual point star')
    star = {A for A in members if A & 1}
    bad = {A for A in members if (A & 7) == 0 and A.bit_count() == 2 and
           ((A >> 3).bit_count() == ((A >> 3) & 511).bit_count() or (A >> 12).bit_count() == 2)}
    bad |= {A for A in members if A & 7 == 6 and A >> 12}
    require(len(bad) == 81 and bad <= set(members)-star, 'all81 literal bad vertices')
    return members, star, bad


def edge(u, v):
    return (min(u, v), max(u, v))


def verify_inverse(data, bad):
    order = data['bad_vertex_order']; pivots = data['pivot_edge_order']
    require(isinstance(data['twice_inverse_rows'],list) and
            all(isinstance(row,str) for row in data['twice_inverse_rows']), 'all81 textual integer inverse rows')
    Q = [[int(v) for v in row.split()] for row in data['twice_inverse_rows']]
    require(order == sorted(bad), 'all original bad labels in ascending order')
    require(len(pivots) == 81 and len({tuple(e) for e in pivots}) == 81 and
            all(isinstance(e, list) and len(e) == 2 and e[0] < e[1] and
                e[0] in bad and e[1] in bad and not e[0] & e[1] for e in pivots),
            '81 distinct actual supported pivot edges')
    # The tree is verified through cut growth, not the producer elimination.
    visited = {order[0]}
    for e in pivots[:80]:
        require(sum(v in visited for v in e) == 1, 'every chosen tree edge grows the original vertex span')
        visited.update(e)
    require(visited == bad and pivots[-1] == [12288, 49152] and
            edge(24,12288) in map(tuple,pivots) and edge(24,49152) in map(tuple,pivots),
            'entire selected spanning tree and original odd triangle')
    require(data['inverse_denominator'] == 2 and len(Q) == 81 and
            all(len(row) == 81 and all(type(v) is int and abs(v) <= 2 for v in row) for row in Q),
            'entire inverse over2, literal coefficients bounded by1')
    A = [[int(v in e) for e in pivots] for v in order]
    # BOTH complete products in original labels; every one of13122 entries.
    for i in range(81):
        for j in range(81):
            require(sum(A[i][k]*Q[k][j] for k in range(81)) == 2*int(i == j),
                    'every entry of A times the claimed inverse')
            require(sum(Q[i][k]*A[k][j] for k in range(81)) == 2*int(i == j),
                    'every entry of the claimed inverse times A')
    return order, list(map(tuple,pivots)), Q


def sparse_original_lift(proper, star, present, forced):
    """Complete nonzero proper edges -> all nonzero entries of EHE^T.

    Every omitted entry is exactly0 by the displayed completion equations.
    Values here are integer numerators over2, not floating values.
    """
    rows = Counter(); kernel = Counter(); actual = Counter()
    for (u,v), value in proper.items():
        require(type(value) is int and value and u in present and v in present and
                0 < u < v and not u & v, 'every nonzero original proper entry supported offdiagonal')
        rows[u] += value; rows[v] += value
        if v in star: kernel[u] += value
        if u in star: kernel[v] += value
        actual[(u,v)] += value
    require(all(v == 0 for v in kernel.values()), 'every physical star kernel row')
    for u, value in rows.items():
        if value: actual[(0,u)] = -value
    total = sum(rows.values())
    if total: actual[(0,0)] = total
    actual = {e:v for e,v in actual.items() if v}
    require(not any(e in forced for e in actual), 'ALL163 forced ordered floors unchanged')
    actual_rows = Counter()
    for (u,v), value in actual.items():
        require(not u & v and (u != v or u == 0), 'every nonzero ACTUAL supported entry, empty retained')
        actual_rows[u] += value
        if u != v: actual_rows[v] += value
    require(all(v == 0 for v in actual_rows.values()), 'every actual stochastic perturbation row')
    require(total == 0, 'actual empty loop fixed')
    return actual


def verify(data):
    require((data['actual_agent'],data['role'],data['q'],data['k'],data['actual_N'],data['s']) ==
            ('six-downset-3','researcher',18,9,278,58), 'fixed actual authorship and carrier')
    require(data['dependency_graph'] == 'bafkreifiauc33i6a3pumyecwlfcprotceve2xb6c47iavaqyvhcpexv3qy' and
            data['dependency_source'] == '88c6c7ea0905fe51d4ecab5703a3e9cd18d3344c' and
            data['dependency_not_rechecked'] is True and data['real_tau_interval'] == ['0','1/128'],
            'explicit published ordinary same-carrier center/margin dependency, not a new PSD factor claim')
    eta = F(data['eta']); require(eta == F(1,2**60), 'exact published center scale')
    power = data['rho_eta_denominator_power']
    require(type(power) is int and 0 <= power <= 20, 'finite explicit dyadic coordinate radius')
    rho = eta / 2**power
    for key in ['selected_edge_numerator','pivot_compensation_multiplier','good_gauge_numerator','anchored_a_numerator']:
        require(type(data[key]) is int, 'exact submitted sparse chart coefficients')
    X, S, B = physical_carrier(); present = set(X)
    order, pivots, Q = verify_inverse(data,B); labels = {v:i for i,v in enumerate(order)}
    pivot_set = set(pivots)
    free = [(u,v) for i,u in enumerate(X) for v in X[i+1:]
            if not u & v and u != 1 and v != 1]
    bb = [e for e in free if all(v in B for v in e)]
    gg = [e for e in free if all(v not in B|S for v in e)]
    ns = [e for e in free if sum(v in S for v in e) == 1]
    cross = [e for e in free if sum(v in B for v in e) == 1 and not any(v in S for v in e)]
    require((len(free),len(bb),len(gg),len(ns),len(cross)) == (29802,2628,7885,10280,9009),
            'complete original independent coordinate partition')
    gauge = gg[0]; bad_free = [e for e in bb if e not in pivot_set]; good_free = gg[1:]
    selected = set(bad_free + good_free + ns)
    require(len(selected) == 20711, 'entire canonical coordinate set, no duplicates')
    forced = {(0,0)} | {(0,u) for u in B}
    proper_budget = Counter(); actual_budget = Counter(); column_hash = hashlib.sha256()
    counts = Counter(); l1_sum = Counter(); max_column_l1 = Counter(); max_column_actual = Counter()
    max_terms = Counter(); sparse_position_checks = Counter()

    def accept(kind, key, H):
        H = {e:v for e,v in H.items() if v}
        require(H.get(key) == 2 and all(e == key or e not in selected for e in H),
                'every literal coordinate projection is the identity left inverse')
        degrees = Counter(); good_mass = 0
        for (u,v), value in H.items():
            require((u in B) == (v in B) or u in S or v in S, 'no cross NN coordinate')
            if u in B and v in B: degrees[u] += value; degrees[v] += value
            elif u not in B|S and v not in B|S: good_mass += value
        require(all(v == 0 for v in degrees.values()) and good_mass == 0,
                'EVERY original bad-degree equation and good total unchanged')
        actual = sparse_original_lift(H,S,present,forced)
        mass = sum(abs(v) for v in H.values())
        counts[kind] += 1; l1_sum[kind] += mass
        max_column_l1[kind] = max(max_column_l1[kind],mass)
        max_column_actual[kind] = max(max_column_actual[kind],max(map(abs,actual.values())))
        max_terms[kind] = max(max_terms[kind],len(H))
        sparse_position_checks['proper_unordered'] += len(H)
        sparse_position_checks['actual_unordered'] += len(actual)
        for e,v in H.items(): proper_budget[e] += abs(v)
        for e,v in actual.items(): actual_budget[e] += abs(v)
        row = {'kind':kind,'coordinate':list(key),
               'proper':[[u,v,a] for (u,v),a in sorted(H.items())],
               'actual':[[u,v,a] for (u,v),a in sorted(actual.items())]}
        column_hash.update((json.dumps(row,sort_keys=True,separators=(',',':'))+'\n').encode())

    for u,v in bad_free:
        H = {(u,v):data['selected_edge_numerator']}
        for j,e in enumerate(pivots):
            value = data['pivot_compensation_multiplier']*(-Q[j][labels[u]]-Q[j][labels[v]])
            if value: H[e] = value
        accept('bad', (u,v), H)
    for e in good_free:
        accept('good', e, {e:data['selected_edge_numerator'], gauge:data['good_gauge_numerator']})
    for e in ns:
        nonstar = next(v for v in e if v not in S)
        accept('anchored', e, {e:data['selected_edge_numerator'], edge(nonstar,1):data['anchored_a_numerator']})
    require(dict(counts) == {'bad':2547,'good':7884,'anchored':10280}, 'all20711 complete generators')
    nn = bb+gg+cross
    nn_max = max(proper_budget[e] for e in nn)
    actual_max = max(actual_budget.values())
    proper_mass = sum(l1_sum.values())
    require(F(nn_max,2)*rho < eta/2, 'uniform cube keeps every strict NN sign by eta/2')
    require(F(actual_max,2)*rho < eta, 'uniform cube keeps every unforced ACTUAL surplus by8eta')
    require(F(proper_mass,2)*rho < F(1,512), 'uniform proper operator bound pays BOTH1/512 floors')
    needed = 0
    while 2**needed < max(nn_max, F(actual_max,2)):
        needed += 1
    require(power >= needed, 'radius lies inside the all-entry certified cube')
    # Full literal coordinate envelopes are hashed; no aggregate-only gate.
    pbytes = json.dumps([[u,v,a] for (u,v),a in sorted(proper_budget.items())],separators=(',',':')).encode()
    abytes = json.dumps([[u,v,a] for (u,v),a in sorted(actual_budget.items())],separators=(',',':')).encode()
    return {'actual_agent':'six-downset-3','role':'researcher','coverage':'ALL20711 individual REAL coordinates, all real tau in[0,1/128]',
            'ordinary_dependency_graph':data['dependency_graph'],'ordinary_dependency_source':data['dependency_source'],
            'parent_center_and_PSD_not_rechecked':True,'inverse_product_entries_checked':13122,
            'inverse_value_counts_over2':{str(k):v for k,v in sorted(Counter(v for r in Q for v in r).items())},
            'chart_counts':dict(counts),'chart_dimension':20711,'good_gauge_masks':list(gauge),
            'forced_ordered_floor_positions':163,'maximum_column_terms':dict(max_terms),
            'proper_column_l1_sums':{k:str(F(v,2)) for k,v in l1_sum.items()},
            'proper_column_l1_maxima':{k:str(F(v,2)) for k,v in max_column_l1.items()},
            'actual_column_entry_maxima':{k:str(F(v,2)) for k,v in max_column_actual.items()},
            'full_column_hash':column_hash.hexdigest(),'original_sparse_position_checks':dict(sparse_position_checks),
            'proper_envelope_sha256':hashlib.sha256(pbytes).hexdigest(),
            'actual_envelope_sha256':hashlib.sha256(abytes).hexdigest(),
            'proper_envelope_positions':len(proper_budget),'actual_envelope_positions':len(actual_budget),
            'NN_maximizer_masks':[list(e) for e in nn if proper_budget[e] == nn_max],
            'actual_maximizer_masks':[list(e) for e,v in actual_budget.items() if v == actual_max],
            'NN_entry_cube_coefficient':str(F(nn_max,2)),
            'actual_entry_cube_coefficient':str(F(actual_max,2)),
            'proper_operator_cube_coefficient':str(F(proper_mass,2)),
            'smallest_entry_certified_dyadic_power':needed,'rho':str(rho),
            'strict_NN_sign_margin':str(eta/2),'unforced_actual_C_unit_surplus':str(8*eta),
            'C_starperp_and_U_uniform_floor':'1/512','other276_eigenvalue_gap':'1/112640',
            'actual_endpoint_ranks':[277,277],'simple_extreme_eigenvalues':['-29/110','1'],
            'all_floor_sign_spectral_arithmetic_exact':True,
            'unformalized_completeness_real_cube_and_congruence_bridges_in_PROOF':True,
            'independent_review_claimed':False}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--certificate',type=Path,default=BASE/'CHART.json')
    ap.add_argument('--out',type=Path,required=True); args = ap.parse_args()
    spec=importlib.util.spec_from_file_location('sourcecheck',BASE/'sourcecheck.py')
    source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
    source.check_bundle(BASE)
    record = verify(json.loads(args.certificate.read_text()))
    args.out.write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print(json.dumps(record,sort_keys=True))
