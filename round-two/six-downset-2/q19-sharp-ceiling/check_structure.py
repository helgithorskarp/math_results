"""Exact new ceiling dual, individual-edge identity/rank and line checks.

Self-contained checker: explicitly reuses same-author defining modules.
No search, recovery, floating package or previously paid endpoint is run.
Ordinary real completeness, positivity and affine-hull bridges are in PROOF.md.
"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
from binding import check_current
check_current()
from encoding import F, comparison, scalar_rows, classify, model
from collections import Counter, deque
import argparse
import hashlib
import json
import resource
import time

U = F(42901, 98304)
RADIUS = F(1, 32768)
XY = (0, 1, 1)
X = (0, 1, 0)
Y = (0, 0, 1)
ZERO_TYPES = (XY, (0, 2, 0), (2, 0, 0), (2, 1, 0),
              (4, 0, 0), (4, 1, 0), (6, 0, 0))
ZERO_KEYS = {tuple(sorted((XY, t))) for t in ZERO_TYPES}
SELECTED_KEYS = {tuple(sorted((XY, t))) for t in (X, Y)}
BOUNDARY_PIN = '70b689016621c1bac532ccf043301865753462d96d968c19566f05a4e6187ff0'
POSTLINE_PIN = '3ed5f72aad412fd7d4c140b69bc7bfe31710e1328a4760c649a37da71940fd83'


def audit_inverse(A,inv):
    n=len(A)
    model.require(len(inv)==n and all(len(row)==n for row in inv)
                  and all(sum(A[i][k]*inv[k][j] for k in range(n))==int(i==j)
                          and sum(inv[i][k]*A[k][j] for k in range(n))==int(i==j)
                          for i in range(n) for j in range(n)),
                  'both whole NEW-domain inverse products')


def inverse_and_det(A):
    # Same elementary algorithm as the credited fe4 chart, with both products.
    n = len(A)
    work = [list(row) + [F(i == j) for j in range(n)]
            for i, row in enumerate(A)]
    det = F(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if work[i][j]), None)
        model.require(pivot is not None, 'new-boundary surviving exact rank minor')
        if pivot != j:
            work[pivot], work[j] = work[j], work[pivot]
            det = -det
        value = work[j][j]
        det *= value
        work[j] = [v / value for v in work[j]]
        for i in range(n):
            if i != j:
                value = work[i][j]
                work[i] = [v - value * w for v, w in zip(work[i], work[j])]
    inv = [row[n:] for row in work]
    audit_inverse(A,inv)
    return inv, det


def decode(path, pin, base, tau):
    raw = path.read_bytes()
    model.require(hashlib.sha256(raw).hexdigest() == pin, 'whole new witness bytes')
    data = json.loads(raw)
    model.require(F(data['tau']) == tau, 'actual new witness tau')
    table = {}
    for row in data['free_pair_values']:
        key = tuple(map(tuple, row['types']))
        model.require(key == tuple(sorted(key)) and key not in table and key in base,
                      'all distinct new original coordinate keys')
        table[key] = F(row['value'])
        model.require(table[key] - base[key] == F(row['delta']), 'new exact coordinate delta')
    model.require(set(table) == set(base), 'entire143 new endpoint coordinates')
    return table


def run():
    began = time.monotonic()
    base = comparison()
    parts, budgets = classify(base)
    keys = sorted(base)
    row0 = scalar_rows(base)
    rowkeys = list(row0)
    rowdir = {r: [] for r in rowkeys}
    for key in keys:
        table = base.copy()
        table[key] += 1
        rows = scalar_rows(table)
        model.require(list(rows) == rowkeys, 'all180 exact original scalar generators')
        for r in rowkeys:
            rowdir[r].append(rows[r] - row0[r])
    model.require([len(parts[t]) for t in ('KK', 'KG', 'GG', 'star')]
                  == [5, 25, 34, 79] and budgets['P0'] == F(8421443, 65536),
                  'fixed comparison and all143 coordinate census')

    # Fresh exact entry-relaxation instance; no discovery script is imported.
    A = [[-v for v in rowdir[r]] + [F(1)] for r in rowkeys]
    b = [row0[r] for r in rowkeys]
    labels = [['floor', list(r)] for r in rowkeys]
    for part, sign in (('KK', 1), ('GG', -1)):
        for key in parts[part]:
            row = [F(0)] * 144
            row[keys.index(key)] = F(sign)
            A.append(row)
            b.append(F(0))
            labels.append(['repair_sign', part, key])
    row = [F(0)] * 144
    row[-1] = -1
    A.append(row)
    b.append(F(0))
    labels.append(['tau_nonnegative'])
    eqkeys = [('empty', t) for t in budgets['bad_nn']] + [('loop',)]
    E = [rowdir[r] + [F(-1)] for r in eqkeys]
    f = [-row0[r] for r in eqkeys]
    elabels = [['sharp', list(r)] for r in eqkeys]
    for key in parts['KG']:
        row = [F(0)] * 144
        row[keys.index(key)] = 1
        E.append(row)
        f.append(F(0))
        elabels.append(['KG_zero', key])
    instance = dict(agent='six-downset-2', role='researcher',
        variables=['delta_' + str(p) for p in keys] + ['tau'], keys=keys,
        base=[str(base[p]) for p in keys],
        A=[[str(v) for v in r] for r in A], b=list(map(str, b)), labels=labels,
        E=[[str(v) for v in r] for r in E], f=list(map(str, f)), equality_labels=elabels,
        all_variables_unbounded_except_explicit_rows=True, original_floor_rows=180,
        KK_GG_tau_sign_rows=40, sharp_equations=5, KG_equations=25,
        lower_PSD_omitted_relaxation_only=True, source_binding_before_formula_import=True)
    instance_hash = model.digest(instance)
    model.require(instance_hash == 'c2e0f28b1029112c1d3e159673a96c46a3476382acf12a049cfef25ab5c31a16',
                  'whole regenerated new LP including conventions and labels')
    dual = json.loads((HERE / 'DUAL.json').read_text())
    y = list(map(F, dual['inequality_multipliers']))
    z = list(map(F, dual['equality_multipliers']))
    model.require(len(A) == len(y) == 220 and len(E) == len(z) == 30
                  and dual['instance_sha256'] == instance_hash and all(v >= 0 for v in y),
                  'all nonnegative new dual inequality weights')
    model.require(all(sum(y[i] * A[i][j] for i in range(220))
                      + sum(z[i] * E[i][j] for i in range(30)) == int(j == 143)
                      for j in range(144)), 'entire144 exact objective identity')
    model.require(sum(v * w for v, w in zip(y, b))
                  + sum(v * w for v, w in zip(z, f)) == U == F(dual['upper_tau']),
                  'exact new dual ceiling constant')
    entry = json.loads((HERE / 'ENTRY-PRIMAL.json').read_text())
    vertex = list(map(F, entry['deltas'])) + [F(entry['tau'])]
    slacks = [w - sum(v * x for v, x in zip(row, vertex)) for row, w in zip(A, b)]
    model.require(len(vertex) == 144 and vertex[-1] == U and min(slacks) >= 0
                  and all(sum(v * x for v, x in zip(row, vertex)) == w for row, w in zip(E, f)),
                  'whole220 inequalities and30 equalities of entry-only LP vertex')

    # Every ORIGINAL free edge, rather than only its orbit count.
    members = model.members(9, 10)
    masks = [sum(1 << p for p in v) for v in members]
    types = [model.type_of(v, 9) for v in members]
    Q = list(range(2, 303))
    NN = [i for i in Q if not masks[i] & 1]
    K = {i for i in NN if types[i] in budgets['bad_nn']}
    W = {i for i in NN if types[i] == XY}
    model.require((len(members), len(Q), len(NN), len(K), len(W)) == (303, 301, 241, 75, 90),
                  'entire original carrier and90 XY vertices')
    edges = []
    bytag = {t: [] for t in parts}
    counts = Counter()
    incident_remaining = Counter()
    selected = []
    forced_zero = []
    coefficients = Counter()
    for at, i in enumerate(Q):
        for j in Q[at + 1:]:
            if masks[i] & masks[j]:
                continue
            key = tuple(sorted((types[i], types[j])))
            tag = 'star' if masks[i] & 1 or masks[j] & 1 else 'KK' if i in K and j in K else 'KG' if i in K or j in K else 'GG'
            model.require(key in parts[tag], 'every original coordinate agrees with orbit partition')
            edges.append((i, j))
            bytag[tag].append((i, j))
            counts[key] += 1
            is_selected = key in SELECTED_KEYS
            r = (int(i in W) + int(j in W)) if tag != 'star' and not is_selected else 0
            model.require(r in ((0, 1) if tag == 'KG' else (0,) if tag in ('KK', 'star') else (0, 1, 2)),
                          'literal multiplicities make every dual summand nonnegative')
            if is_selected:
                model.require(tag == 'GG' and int(i in W) + int(j in W) == 1,
                              'all selected1530 proper floors are independent GG coordinates')
                selected.append((i, j))
            if tag == 'GG' and r:
                forced_zero.append((i, j))
                model.require(key in ZERO_KEYS, 'every new zero coordinate is in the seven stated orbits')
            if r:
                incident_remaining[(tag, key)] += r
            coefficients[key] -= r
            if tag != 'star':
                k = int(i in K) + int(j in K)
                # Coefficients on delta_+ and delta_- of the prior mass identity.
                pcoef = 2 - k + (2 if tag == 'KK' else 1 if tag == 'KG' else 0)
                ncoef = -(2 - k) + (1 if tag == 'KG' else 2 if tag == 'GG' else 0)
                model.require((pcoef, ncoef) == (2, 0), 'each23865 original-edge mass coefficient')
    edge_counts = {t: len(v) for t, v in bytag.items()}
    model.require(len(edges) == 35865 and edge_counts == dict(KK=1800, KG=10820, GG=11245, star=12000),
                  'all35865 original coordinates checked')
    model.require(len(selected) == 1530 and len(forced_zero) == 7470
                  and {tuple(sorted((types[i], types[j]))) for i, j in forced_zero} == ZERO_KEYS,
                  'all9000 additional independent GG coordinate equations')
    for i in W:
        neighbors = [j for j in NN if not masks[i] & masks[j] and types[j] in (X, Y)]
        model.require(Counter(types[j] for j in neighbors) == {Y: 9, X: 8},
                      'every XY vertex has exactly the17 selected singleton neighbors')
    eY = 1 + base[tuple(sorted((Y, XY)))]
    eX = 1 + base[tuple(sorted((X, XY)))]
    ellXY = budgets['ell'][XY]
    model.require((eY, eX, ellXY) == (F(13599, 32768), F(6785, 16384), F(26455, 32768))
                  and ellXY + 9 * eY + 8 * eX == 18 * U,
                  'exact original18-floor budget constant')
    model.require(75 * 1 + 1 == 76 and
                  sum(budgets['weights'][t] * budgets['ell'][t] for t in budgets['bad_nn'])
                  + budgets['loop'] == -2 * budgets['P0'], 'entire comparison constant in mass identity')
    for j, key in enumerate(keys):
        observed = 90 * rowdir[('empty', XY)][j]
        if key in SELECTED_KEYS:
            observed += counts[key]
        model.require(observed == coefficients[key], 'all143 aggregated budget coefficients including star cancellation')
        mass_linear = sum(budgets['weights'][t] * rowdir[('empty', t)][j]
                          for t in budgets['bad_nn']) + rowdir[('loop',)][j]
        if key in parts['star']:
            expected = 0
        else:
            k = sum(t in budgets['bad_nn'] for t in key)
            expected = counts[key] * (2 - k)
        model.require(mass_linear == expected, 'all original invariant mass generators agree with individual edge identity')

    # Fixed-coordinate deletions leave the old full bad-degree rank mechanism.
    adj = {i: [] for i in K}
    for i, j in bytag['KK']:
        adj[i].append(j)
        adj[j].append(i)
    root = members.index((12, 13))
    parent = {root: None}
    queue = deque([root])
    while queue:
        i = queue.popleft()
        for j in adj[i]:
            if j not in parent:
                parent[j] = i
                queue.append(j)
    triangle = [members.index(v) for v in ((12, 13), (14, 15), (16, 17))]
    model.require(len(parent) == 75 and all(j in adj[i] for i, j in zip(triangle, triangle[1:] + triangle[:1])),
                  'same original connected odd KK graph survives ALL9000 new deletions')
    free_loop_edge = next((i, j) for i, j in bytag['GG']
                          if types[i] == types[j] == Y)
    model.require(free_loop_edge not in selected and free_loop_edge not in forced_zero,
                  'loop coefficient2 survives while all bad-degree coefficients are0')
    fixed_keys = ZERO_KEYS | SELECTED_KEYS
    pivots = [(Y, Y), ((0, 0, 2), (0, 0, 2)),
              ((0, 0, 2), (2, 0, 1)), ((0, 0, 2), (4, 0, 1)),
              ((0, 0, 2), (6, 0, 1))]
    model.require(all(k not in fixed_keys and k not in parts['KG'] for k in pivots),
                  'all five invariant pivot columns survive the new affine face')
    minor = [[rowdir[r][keys.index(k)] for k in pivots] for r in eqkeys]
    inv, det = inverse_and_det(minor)
    model.require(abs(det) == 117573120, 'new boundary full five-equation rank')
    dimensions = (35865 - 10820 - 9000 - 75 - 1, 143 - 25 - 9 - 5)
    model.require(dimensions == (15969, 104), 'new full and invariant boundary dimensions')

    boundary = decode(HERE / 'BOUNDARY-CANDIDATE.json', BOUNDARY_PIN, base, U)
    post = decode(HERE / 'POSTLINE-CANDIDATE.json', POSTLINE_PIN, base, U + RADIUS)
    direction = {tuple(sorted(k)): v for k, v in [
        ((Y, XY), F(1)), ((X, XY), F(1)), ((XY, XY), -F(1, 4)),
        ((Y, Y), -F(682, 45)), (((0, 0, 2), (0, 0, 2)), -F(1, 84)),
        (((0, 0, 2), (2, 0, 1)), -F(1, 36)),
        (((0, 0, 2), (4, 0, 1)), -F(1, 36)),
        (((0, 0, 2), (6, 0, 1)), -F(1, 36))]}
    model.require(len(direction) == 8 and all(post[k] - boundary[k] == RADIUS * direction.get(k, 0) for k in keys),
                  'every143 original coordinate obeys the specified eight-coordinate affine line')
    rb = scalar_rows(boundary)
    rp = scalar_rows(post)
    forced = set(eqkeys) | {('empty', XY), ('proper', Y, XY), ('proper', X, XY)}
    model.require(all((rp[r] - rb[r]) / RADIUS == 1 and rb[r] == U for r in forced),
                  'every eight forced line-floor derivative is exactly1')
    model.require(sum(counts[k] * direction.get(k, 0) for k in keys if k not in parts['star']) == F(1, 2),
                  'exact half total NN direction gives original loop derivative1')
    negative_post = sum(counts[k] for k in parts['GG'] if post[k] - base[k] < 0)
    zero_post = sum(counts[k] for k in parts['GG'] if post[k] == base[k])
    model.require((negative_post, zero_post) == (3240, 4230),
                  'computed rather than declared original post-ceiling negative and zero GG counts')
    cost_boundary = sum(counts[k] * max(boundary[k] - base[k], F(0)) for k in keys if k not in parts['star'])
    cost_post = sum(counts[k] * max(post[k] - base[k], F(0)) for k in keys if k not in parts['star'])
    model.require(cost_boundary == budgets['P0'] + 38 * U
                  and (cost_post - cost_boundary) / RADIUS == 848,
                  'original individual cost slope848 from the literal full census')
    model.require(budgets['P0'] - 810 * U == -F(14745097, 65536),
                  'exact refined piecewise intercept')
    return dict(agent='six-downset-2', role='researcher', instance_sha256=instance_hash,
        original_LP_inequalities=220, original_LP_equalities=30,
        complete_dual_objective_coordinates=144, inequality_weights_nonnegative=True,
        upper_sharp_tau=str(U), upper_sharp_epsilon=str(U / 242),
        complete_entry_relaxation_primal_at_dual_ceiling=True,
        entry_relaxation_vertex_spectral_PSD_not_asserted=True,
        original_free_coordinate_count=len(edges), original_edge_counts=edge_counts,
        entire_original_edges_sha256=model.digest(edges),
        original_XY_vertex_count=90, selected_proper_floor_count=len(selected),
        additional_zero_GG_coordinates=len(forced_zero), additional_independent_GG_equations=9000,
        zero_GG_orbit_counts=[[k, counts[k]] for k in sorted(ZERO_KEYS)],
        selected_GG_orbit_counts=[[k, counts[k]] for k in sorted(SELECTED_KEYS)],
        every_original_dual_summand_multiplicity_checked=True,
        every_invariant_budget_generator_including_star_cancellation_checked=True,
        surviving_KK_degree_rank=75,
        surviving_KK_spanning_tree=[[members[i], None if p is None else members[p]] for i, p in sorted(parent.items())],
        surviving_KK_odd_cycle=[members[i] for i in triangle],
        surviving_loop_GG_column=[members[i] for i in free_loop_edge],
        entire_surviving_minor=[[str(v) for v in row] for row in minor],
        entire_surviving_minor_inverse=[[str(v) for v in row] for row in inv],
        surviving_minor_determinant=str(det), both_whole_inverse_products_checked=True,
        new_boundary_affine_dimension=dimensions[0], new_boundary_invariant_affine_dimension=dimensions[1],
        post_ceiling_tau=str(U + RADIUS), post_ceiling_epsilon=str((U + RADIUS) / 242),
        full143_exact_affine_line_coordinates=True,
        eight_nonzero_line_directions=[[k, str(v)] for k, v in sorted(direction.items())],
        all_eight_line_floor_derivatives='1', original_postline_negative_GG_count=negative_post,
        original_postline_zero_GG_count=zero_post, exact_original_cost_slope=848,
        refined_bound='P0+38*tau+810*max(tau-42901/98304,0)',
        no_search_recovery_or_floating_package_import=True,
        full_PSD_paid_by_separate_new_endpoint_checks=True,
        ordinary_real_reduction_identity_rank_and_interpolation_bridges_unformalized=True,
        independently_reviewed=False, source_commit=None, graph_ref=None,
        observed_seconds=time.monotonic() - began,
        peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    record = run()
    args.out.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items() if 'tree' not in k and 'minor' not in k}))
