"""q19 refined optimizer geometry, exact source-bound compact reader.

Reuses explicitly credited original-model formulas and two complete tables.
The parent's published spectral floor is a theorem premise. No old positive
checker, factor, EXPECTED value, solver, or peer artifact is mathematical input.
All newly claimed counting, rank-minor, zero-degree perturbation, entry/sign,
literal matrix differences and norm-bound arithmetic are checked here.
"""
import argparse
from collections import Counter, deque
from fractions import Fraction as F
import hashlib
import importlib
from itertools import combinations
import json
from math import lcm
from pathlib import Path
import resource
import sys
import time
from reader_binding import check_current
check_current()

ROOT = Path(__file__).resolve().parent
PARENT_COMMIT = '1af1d27b8a7b51e8a730d4496b1767c65ad52532'
PARENT_SEAL = 'c90b9d9ed0debb98d7a622e8457efe625006482898138f0a504769920a607625'
PARENT_FILES = {
    '.gitignore', 'BOUNDARY-CANDIDATE.json', 'COEFFICIENTS.json', 'DUAL.json',
    'ENTRY-PRIMAL.json', 'EXPECTED.json', 'POSTLINE-CANDIDATE.json', 'PROOF.md',
    'README.md', 'SOURCE.json', 'adverse.py', 'binding.py', 'check_boundary.py',
    'check_postline.py', 'check_structure.py', 'encoding.py', 'model.py',
    'physical.py', 'verify.py',
}
U, R, P0 = F(42901, 98304), F(1, 32768), F(8421443, 65536)
YY, BY, CY, BCY = (0, 0, 2), (2, 0, 1), (4, 0, 1), (6, 0, 1)
XY, X, Y = (0, 1, 1), (0, 1, 0), (0, 0, 1)
BAD = (YY, BY, CY, BCY)


def require(ok, why):
    if not ok:
        raise ValueError(why)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def pair(t, u):
    return tuple(sorted((t, u)))


def bind_parent(root):
    raw = (root / 'SHA256SUMS').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PARENT_SEAL,
            'entire published nineteen-file parent manifest before imports')
    names, records = set(), []
    for line in raw.decode().splitlines():
        pin, name = line.split('  ', 1)
        require(name == Path(name).name and name not in names and
                len(pin) == 64 and all(c in '0123456789abcdef' for c in pin),
                'distinct literal parent defining paths and hashes')
        names.add(name)
        blob = (root / name).read_bytes()
        require(hashlib.sha256(blob).hexdigest() == pin,
                'entire credited parent input before import: ' + name)
        records.append(dict(file=name, bytes=len(blob), sha256=pin))
    require(names == PARENT_FILES, 'all nineteen original defining parent files')
    return dict(commit=PARENT_COMMIT, manifest_sha256=PARENT_SEAL,
                entire_files=len(records), bytes=sum(a['bytes'] for a in records),
                records=records, bound_before_math_import=True)


def decode(root, name, expected_tau, base):
    data = json.loads((root / name).read_bytes())
    require(data['agent'] == 'six-downset-2' and data['role'] == 'researcher' and
            F(data['tau']) == expected_tau and
            data['exact_input_sha256'] ==
            '65f2b0a5170e0a7585d4892c33d72aca7e4479d0e3484dc98ee32b0ad27f1105',
            'whole exact credited table scope; historical status is not proof')
    table = {}
    for item in data['free_pair_values']:
        key = tuple(map(tuple, item['types']))
        require(key == tuple(sorted(key)) and key not in table and key in base,
                'each distinct original free table coordinate')
        require(type(item['value']) is str and type(item['delta']) is str,
                'exact rational strings required for complete table coefficients')
        val = F(item['value'])
        require(F(item['delta']) == val - base[key],
                'every table value versus explicitly fixed comparison')
        table[key] = val
    require(set(table) == set(base) and len(table) == 143,
            'entire 143-coordinate credited table, no omission')
    return table


def original_sets():
    """Direct named-core construction independent of imported enumeration."""
    collection = {()}
    collection.update((i,) for i in range(22))
    collection.update(combinations(range(22), 2))
    collection.add((0, 1, 2))
    for i in range(3, 22):
        collection.add((0, 1, i))
        collection.add((0, 2, i))
        if i >= 12:
            collection.add((1, 2, i))
    members = sorted(collection, key=lambda a: sum(1 << v for v in a))
    masks = [sum(1 << v for v in a) for a in members]
    types = [(m & 7, ((m >> 3) & 511).bit_count(),
              (m >> 12).bit_count()) for m in masks]
    require(len(members) == 303 and members[:2] == [(), (0,)] and
            sum(bool(m & 1) for m in masks) == 61,
            'independent entire original carrier and star')
    require(all(tuple(u for u in v if u != i) in collection
                for v in members for i in v), 'each original downward deletion')
    return members, masks, types


def bucket(types, i, j):
    t, u = types[i], types[j]
    if t[0] & 1 or u[0] & 1:
        return 'star', 0, False
    tag = 'KK' if t in BAD and u in BAD else 'KG' if t in BAD or u in BAD else 'GG'
    selected = (t == XY and u in (X, Y)) or (u == XY and t in (X, Y))
    m = 0 if selected else int(t == XY) + int(u == XY)
    return tag, m, selected


def invert(A):
    n = len(A)
    aug = [[F(a) for a in row] + [F(int(i == j)) for j in range(n)]
           for i, row in enumerate(A)]
    det = F(1)
    for j in range(n):
        p = next((i for i in range(j, n) if aug[i][j]), None)
        require(p is not None, 'new exact surviving six-floor minor is nonsingular')
        if p != j:
            aug[p], aug[j] = aug[j], aug[p]
            det = -det
        d = aug[j][j]
        det *= d
        aug[j] = [v / d for v in aug[j]]
        for i in range(n):
            if i != j:
                a = aug[i][j]
                aug[i] = [v - a * w for v, w in zip(aug[i], aug[j])]
    inv = [row[n:] for row in aug]
    require(all(sum(A[i][k] * inv[k][j] for k in range(n)) == int(i == j) and
                sum(inv[i][k] * A[k][j] for k in range(n)) == int(i == j)
                for i in range(n) for j in range(n)),
            'both entire new six-by-six rational inverse products')
    return det, inv


def geometry(members, masks, types, base, scalar_rows):
    edges = [(i, j) for i in range(2, 303) for j in range(i + 1, 303)
             if not masks[i] & masks[j]]
    require(len(edges) == 35865, 'each original independent unordered free edge')
    K = {i for i in range(2, 303) if types[i] in BAD}
    W = {i for i in range(2, 303) if types[i] == XY}
    H = K | W
    require(len(K) == 75 and len(W) == 90 and len(H) == 165,
            'all original bad and XY floor vertices')
    counts, orbit_counts, fixed = Counter(), Counter(), set()
    fixed_orbits = set()
    for i, j in edges:
        tag, m, selected = bucket(types, i, j)
        key = pair(types[i], types[j])
        counts[tag] += 1
        counts[f'{tag}:m{m}:selected{int(selected)}'] += 1
        orbit_counts[(tag, m, selected, key)] += 1
        if (tag == 'KG' and m == 0) or (tag == 'GG' and m == 1) or selected:
            fixed.add((i, j))
            fixed_orbits.add(key)
    expected = {
        'star': 12000, 'KK': 1800, 'KG': 10820, 'GG': 11245,
        'KG:m0:selected0': 5150, 'KG:m1:selected0': 5670,
        'GG:m0:selected0': 2245, 'GG:m0:selected1': 1530,
        'GG:m1:selected0': 4230, 'GG:m2:selected0': 3240,
    }
    require(all(counts[k] == n for k, n in expected.items()) and
            len(fixed) == 10910 and len(fixed_orbits) == 29,
            'complete newly refined fixed-row and remaining-edge census')
    require({pair(types[i], types[j]) for i, j in edges} == set(base),
            'all 143 invariant coordinates occur in literal free edges')
    adjacency = {i: [] for i in H}
    for i, j in edges:
        if (i, j) in fixed or bucket(types, i, j)[0] == 'star':
            continue
        require((i in H) == (j in H),
                'every surviving column has either two or zero degree-row endpoints')
        if i in H:
            adjacency[i].append(j)
            adjacency[j].append(i)
    require(sum(map(len, adjacency.values())) == 2 * 10710,
            'all surviving unsigned HH incidence columns')
    start, tree, seen = min(H), [], {min(H)}
    todo = deque([start])
    while todo:
        i = todo.popleft()
        for j in sorted(adjacency[i]):
            if j not in seen:
                seen.add(j)
                todo.append(j)
                tree.append((i, j))
    require(seen == H and len(tree) == 164,
            'entire new 165-vertex connected surviving incidence graph')
    index = {v: i for i, v in enumerate(members)}
    triangle = [index[(12, 13)], index[(14, 15)], index[(16, 17)]]
    require(all(triangle[(i + 1) % 3] in adjacency[triangle[i]] for i in range(3)),
            'literal surviving odd cycle closes full degree rank')
    loop_column = tuple(sorted((index[(12,)], index[(13,)])))
    require(loop_column in edges and loop_column not in fixed and
            not any(v in H for v in loop_column),
            'remaining Y/Y column has loop coefficient2 and all165 degree coefficients0')
    eqkeys = [('empty', t) for t in BAD] + [('empty', XY), ('loop',)]
    pivots = [pair(Y, Y), pair(YY, YY), pair(YY, BY), pair(YY, CY),
              pair(YY, BCY), pair(XY, XY)]
    require(all(p in base and p not in fixed_orbits for p in pivots),
            'all six invariant pivots survive original coordinate deletions')
    row0 = scalar_rows(base)
    directions = []
    for p in pivots:
        tab = base.copy()
        tab[p] += 1
        rows = scalar_rows(tab)
        directions.append([rows[k] - row0[k] for k in eqkeys])
    A = [[directions[j][i] for j in range(6)] for i in range(6)]
    det, inv = invert(A)
    return edges, dict(
        all_free_edges=35865, edge_census=dict(sorted(counts.items())),
        orbit_census=[dict(tag=a, m=b, selected=c, types=d, count=n)
                      for (a, b, c, d), n in sorted(orbit_counts.items())],
        fixed_coordinate_rows=10910, bad_degree_rows=75, XY_degree_rows=90,
        surviving_degree_rank=165, independent_loop_rank=1,
        connected_HH_columns=10710, spanning_tree=tree, odd_cycle=triangle,
        loop_independence_column=loop_column,
        rank_bridge='ordinary left-null alternation, connectivity and odd cycle',
        full_affine_dimension=35865 - len(fixed) - len(H) - 1,
        invariant_fixed_rows=29, invariant_remaining_coordinate_count=114,
        invariant_floor_rank=6, invariant_affine_dimension=143 - 29 - 6,
        invariant_minor_rows=[repr(k) for k in eqkeys],
        invariant_minor_columns=pivots, invariant_minor_determinant=str(det),
        invariant_minor_matrix=[[str(a) for a in row] for row in A],
        invariant_minor_inverse=[[str(a) for a in row] for row in inv],
        both_entire_inverse_products=True,
    )


def perturbation(members, masks, types, edges, base, scalar_rows, candidate=None):
    V = {
        pair(YY, XY): F(-1), pair(BY, XY): F(-1),
        pair(CY, XY): F(-1), pair(BCY, XY): F(-1),
        pair(YY, YY): F(9, 14), pair(YY, BY): F(9, 4),
        pair(YY, CY): F(9, 4), pair(YY, BCY): F(9, 4),
        pair(XY, XY): F(7, 8),
    }
    if candidate is not None:
        V = candidate
    require(type(V) is dict and all(type(v) is F for v in V.values()),
            'complete exact rational direction coefficients')
    require(len(V) == 9 and set(V) <= set(base), 'nine actual perturbation orbits')
    den = lcm(*(v.denominator for v in V.values()))
    literal = [[0] * 303 for _ in range(303)]
    count = Counter()
    total = F(0)
    for i, j in edges:
        key = pair(types[i], types[j])
        if key in V:
            require(not(masks[i] & 1 or masks[j] & 1),
                    'perturbation is supported on original nonstar proper edges')
            f = V[key] * den
            require(f.denominator == 1, 'complete integer perturbation clearing')
            literal[i][j] = literal[j][i] = f.numerator
            count[key] += 1
            total += V[key]
    degrees = [F(sum(row), den) for row in literal]
    require(total == 0 and all(a == 0 for a in degrees),
            'every original vertex degree and actual loop direction cancel exactly')
    norm_rows = [F(sum(map(abs, row)), den) for row in literal]
    require(max(norm_rows) == 162 and max(abs(v) for v in V.values()) == F(9, 4),
            'new full original row-absolute norm and entry-change bounds')
    expected = {YY: F(144), BY: F(162), CY: F(162), BCY: F(162), XY: F(126)}
    require(all(a == expected.get(t, 0) for a, t in zip(norm_rows, types)),
            'each of303 original row-absolute sums agrees with named compensation')
    unit = base.copy()
    for key, value in V.items():
        unit[key] += value
    rows, rows0 = scalar_rows(unit), scalar_rows(base)
    require(all(rows[k] - rows0[k] ==
                (V.get((k[1], k[2]), 0) if k[0] == 'proper' else 0)
                for k in rows0),
            'all180 original invariant scalar derivatives, including all empty/anchor/loop')
    floor = F(1, 1024) - 162 * R / 64
    require(floor == F(943, 1048576) and floor > F(1, 2048),
            'exact sufficient transferred lower/upper physical floor')
    coarse_margin = F(1, 256) - F(9, 4) * R / 64
    require(coarse_margin >= F(1, 512), 'all-real coarse untouched-entry/sign bound')
    return V, literal, den, dict(
        direction=[dict(types=k, value=str(V[k]), individual_edges=count[k])
                   for k in sorted(V)],
        affected_unordered_edges=sum(count.values()),
        all303_original_degrees_zero=True, all_empty_anchor_and_loop_derivatives_zero=True,
        total_unordered_NN_direction=str(total),
        original_row_abs_sums=[dict(type=t, count=types.count(t), value=str(a))
                               for t, a in sorted(expected.items())],
        other_zero_rows=303 - sum(types.count(t) for t in expected),
        entire_cleared_original_direction_sha256=sha(literal),
        original_clear_denominator=den, max_operator_norm_bound=162,
        max_entry_change_per_unit=str(F(9, 4)), amplitude='t/64',
        released_KG_repair='-t/64', XY_XY_repair='-121*t/512',
        baseline_T_and_Bcap_floor='1/1024',
        baseline_spectral_premise='published parent PROOF.md, all-real postline [U,U+R]',
        new_spectral_verification='symmetric original row-absolute norm, not replayed LDL',
        new_T_and_Bcap_floor=str(floor), sufficient_coarse_floor='1/2048',
        other301_lower_and_upper_eigenvalue_gap=str(F(1, 2048 * 242)),
        coarse_unforced_entry_and_retained_sign_margin=str(coarse_margin),
        coarse_margin_exceeds='1/512',
    )


def endpoint(parent, model, physical, scalar_rows, base, members, masks, types,
             edges, V, literal, vden):
    low = decode(parent, 'BOUNDARY-CANDIDATE.json', U, base)
    high = decode(parent, 'POSTLINE-CANDIDATE.json', U + R, base)
    D = {pair(Y, XY): F(1), pair(X, XY): F(1), pair(XY, XY): F(-1, 4),
         pair(Y, Y): F(-682, 45), pair(YY, YY): F(-1, 84),
         pair(YY, BY): F(-1, 36), pair(YY, CY): F(-1, 36),
         pair(YY, BCY): F(-1, 36)}
    require(all(high[k] - low[k] == R * D.get(k, 0) for k in base),
            'entire credited postline data versus stated eight-coordinate formula')
    new = {k: high[k] + R * V.get(k, 0) / 64 for k in base}
    forced = {('empty', t) for t in BAD + (XY,)} | {('loop',)} | {
        ('proper',) + pair(X, XY), ('proper',) + pair(Y, XY)}
    scalar_margins = []
    for tau, tab in [(U, low), (U + R, new)]:
        rows = scalar_rows(tab)
        require(set(rows) == set(scalar_rows(base)), 'whole180 scalar entry types')
        for k, value in rows.items():
            slack = value - tau
            if k in forced:
                require(slack == 0, 'each refined forced scalar floor at both endpoints')
            else:
                require(slack >= F(1, 512), 'every unforced scalar endpoint margin')
                scalar_margins.append(slack)
        for i, j in edges:
            tag, m, selected = bucket(types, i, j)
            if tag == 'star':
                continue
            delta = tab[pair(types[i], types[j])] - base[pair(types[i], types[j])]
            if tag == 'KK':
                require(delta <= -F(1, 512), 'each strict KK repair throughout affine endpoints')
            elif tag == 'KG':
                require(delta == (-F(tau - U, 64) if m == 1 else 0),
                        'each released or fixed KG coordinate')
            elif m == 1:
                require(delta == 0, 'each fixed GG:m1 coordinate')
            elif m == 2:
                require(delta == -F(121, 512) * (tau - U),
                        'every strict-open-branch WW repair')
            elif not selected:
                require(delta >= F(1, 512), 'each unforced GG:m0 retained strict repair')
            else:
                require(delta == tau - (1 + base[pair(types[i], types[j])]) and delta > 0,
                        'each selected original proper floor and positive repair')
    pold = physical.original(high, 9, 10)
    pnew = physical.original(new, 9, 10)
    independent = model.literal_point(new, 9, 10)
    require(pnew['members'] == members == independent['members'] and
            pnew['masks'] == masks, 'both whole original representations and independent census')
    Ln = [[F(a, pnew['den']) for a in row] for row in pnew['L']]
    Lo = [[F(a, pold['den']) for a in row] for row in pold['L']]
    alpha = R / 64
    require(all(Ln[i][j] == independent['L'][i][j] and
                Ln[i][j] - Lo[i][j] == alpha * F(literal[i][j], vden)
                for i in range(303) for j in range(303)),
            'ENTIRE new original L agreement and exact physical perturbation')
    require(all(F(pnew['T'][i][j], pnew['den']) == independent['T'][i][j] and
                F(pnew['T'][i][j], pnew['den']) - F(pold['T'][i][j], pold['den']) ==
                alpha * F(literal[i + 2][j + 2], vden) and
                F(pnew['cap'][i][j], pnew['den'] * pnew['clear']) -
                F(pold['cap'][i][j], pold['den'] * pold['clear']) ==
                -alpha * F(literal[i + 2][j + 2], vden)
                for i in range(301) for j in range(301)),
            'BOTH entire new T and physical Bcap matrix differences')
    allowed, tight, loose = 0, 0, []
    tau = U + R
    for i in range(303):
        for j in range(303):
            if masks[i] & masks[j]:
                require(Ln[i][j] == 61 * int(i == j), 'every original forbidden support entry')
                continue
            allowed += 1
            value = Ln[i][j] - 61 * int(i == j)
            if i == j == 0:
                isforced = True
            elif i == 0 or j == 0:
                isforced = types[max(i, j)] in BAD + (XY,)
            elif i < 2 or j < 2:
                isforced = False
            else:
                isforced = bucket(types, i, j)[2]
            if isforced:
                require(value == tau, 'every actual forced original floor')
                tight += 1
            else:
                require(value - tau >= F(1, 512), 'every actual unforced original entry is strict')
                loose.append(value - tau)
    require(allowed == 72817 and tight == 3391, 'entire original allowed/floor position census')
    cost = F(0)
    nn_signs = Counter()
    for i, j in edges:
        tag, m, selected = bucket(types, i, j)
        if tag == 'star':
            continue
        delta = Ln[i][j] - 1 - base[pair(types[i], types[j])]
        cost += max(delta, 0)
        nn_signs[(tag, m, selected, 'positive' if delta > 0 else 'negative' if delta < 0 else 'zero')] += 1
    require(cost == P0 + 38 * tau + 810 * R == F(28529893, 196608),
            'entire original unrestricted positive-part cost equality')
    return dict(
        tau=str(tau), t=str(R), original_positions=303 * 303,
        all_original_L_positions_equal=True, all_original_T_positions_equal=True,
        all_lower_and_upper_physical_differences_equal=True,
        all303_original_rows_support_and_centered_star_equations=True,
        allowed_ordered_positions=allowed, forced_ordered_positions=tight,
        other_ordered_positions=len(loose), actual_min_unforced_entry_surplus=str(min(loose)),
        both_scalar_endpoint_min_unforced_surplus=str(min(scalar_margins)),
        original_NN_sign_census=[dict(tag=a, m=b, selected=c, sign=d, count=n)
                                for (a, b, c, d), n in sorted(nn_signs.items())],
        cost=str(cost), complete_new_endpoint_L_sha256=sha([[str(a) for a in row] for row in Ln]),
        complete_new_endpoint_table=[dict(types=k, value=str(new[k]), delta=str(new[k] - base[k]))
                                     for k in sorted(new)],
        existing_endpoint_factors_or_positive_checkers_not_rerun=True,
        new_LDL_claim=False,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--parent', type=Path, default=ROOT.parent / 'q19-sharp-ceiling')
    args = ap.parse_args()
    started = time.monotonic()
    parent = args.parent.resolve()
    binding = bind_parent(parent)
    sys.path.insert(0, str(parent))
    encoding = importlib.import_module('encoding')
    model, physical = encoding.model, encoding.physical
    base = encoding.comparison()
    members, masks, types = original_sets()
    b = model.type_budgets(base, 9, 10)
    require(tuple(b['bad_nn']) == BAD and b['P0'] == P0,
            'exact original fixed comparison and four bad types')
    edges, geom = geometry(members, masks, types, base, encoding.scalar_rows)
    V, literal, den, pert = perturbation(members, masks, types, edges, base, encoding.scalar_rows)
    ep = endpoint(parent, model, physical, encoding.scalar_rows, base, members,
                  masks, types, edges, V, literal, den)
    out = dict(
        agent='six-downset-2', role='researcher', status='private exact author checks',
        scope=dict(N=303, s=61, h=242, X=9, Y=10,
                   real_tau_interval_open_left_closed_right=[str(U), str(U + R)],
                   real_epsilon_interval_open_left_closed_right=[str(U / 242), str((U + R) / 242)],
                   unrestricted_individual_real=True, original_empty_loop_retained=True,
                   comparison='fixed 143-entry 29u/32768 source65580698'),
        credited_source_binding=binding, refined_geometry=geom,
        new_zero_degree_direction=pert, new_strict_endpoint=ep,
        all_real_bridge='affine scalars/signs and symmetric row-norm spectral perturbation',
        actual_affine_hull_and_relative_interior_bridge='ordinary finite continuity, PD openness and supporting faces',
        proof_assistant_formalization=False, independent_review=False,
        new_source_commit=None, new_graph_ref=None,
        runtime=dict(observed_seconds=time.monotonic() - started,
                     peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
    )
    print(json.dumps(out, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
