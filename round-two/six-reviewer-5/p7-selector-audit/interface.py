"""New five-role filter on the explicitly imported complete9141 carrier.

The old34-core completeness and actual18-point transports are mathematical
premises. We rebuild each physical core, check EVERY extra point marking,
and reconstruct all physical residuals of the THREE admitted mixed roots.
The reviewed old numerical61 readout is not a proof input to new maxima.
"""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
from clique import maximum
from star_primitives import require, digest

HERE = Path(__file__).resolve().parent


def literal(masks):
    require(len(masks) == len(set(masks)) and all(type(m) is int and
            0 < m < 1 << 18 and m.bit_count() == 5 for m in masks), 'literal packing domain')
    words = [frozenset(p for p in range(18) if m >> p & 1) for m in masks]
    require(all(len(a&b) <= 2 for a, b in combinations(words, 2)), 'actual word intersection')
    return words


def opposite_hypotheses(masks, roles):
    words = literal(masks)
    x, y, u, w, v = roles
    require(len(set(roles)) == 5 and all(type(p) is int and 0 <= p < 18 for p in roles), 'five distinct physical roles')
    lam = lambda p, q: sum({p, q} <= f for f in words)
    covered = lambda p, q, r: any({p, q, r} <= f for f in words)
    require(sum(x in f for f in words) == sum(y in f for f in words) == 20, 'complete saturated centers')
    require(lam(x, y) == 4 and lam(x, v) == lam(y, v) == 5 and not covered(x, y, v), 'common low leave friend')
    require(lam(x, u) == 4 and lam(x, w) == lam(y, u) == 5 and
            all(lam(x, p) in (4, 5) for p in range(18) if p != x), 'unit first center and cross-low hubs')
    require(lam(y, w) in (3, 4) and all(lam(y, p) in (4, 5) for p in range(18) if p not in (y, w)), 'unit-or-isolated-heavy second center')
    for center, hub in [(x, u), (y, w)]:
        highs = {p for p in range(18) if p != center and lam(center, p) < 5}
        require(hub in highs and all(covered(center, hub, p) for p in highs-{hub}), 'actual induced-high isolation')
    return lam(y, w)


def decode_all(stars=None, inputs=None):
    if stars is None:
        stars = json.loads((HERE/'fixtures.json').read_text())['stars']
    if inputs is None:
        inputs = json.loads((HERE/'BRIDGE34.json').read_text())['raw_positive_maps']
    require(len(inputs) == 34, 'imported complete normalized carrier population')
    records = []; marked = []; seen = set()
    for index, row in enumerate(inputs):
        i, (hub, low, other) = row['first']; j, (su, sv, sx, sb) = row['second']; phi = row['point_map']
        require(len(phi) == len(set(phi)) == 17 and set(phi) == set(range(18))-{other}, 'actual relative point bijection')
        require((phi[su], phi[sv], phi[sx]) == (hub, low, 17), 'transported distinguished old roles')
        masks = sorted({(1 << 17)+sum(1 << p for p in q) for q in stars[i]} |
                       {(1 << other)+sum(1 << phi[p] for p in q) for q in stars[j]})
        require(masks == row['word_masks'] and len(masks) == 36, 'complete actual two-star core')
        words = literal(masks)
        lam = lambda p, q: sum({p, q} <= f for f in words)
        covered = lambda p, q, r: any({p, q, r} <= f for f in words)
        first, second = 17, other; alpha = 5-lam(first, hub)
        require(alpha in (1, 2), 'old first-hub branch')
        require(len({first, second, hub, low}) == 4 and
                sum(first in f for f in words) == sum(second in f for f in words) == 20,
                'imported distinct complete saturated old roles')
        require(lam(first, second) == 4 and lam(first, low) == lam(second, low) ==
                lam(second, hub) == 5 and not covered(first, second, low),
                'old carrier simultaneous physical hypotheses')
        require(all(lam(second, p) in (4, 5) for p in range(18) if p != second) and
                all(lam(first, p) in (4, 5) for p in range(18) if p not in (first, hub)),
                'old carrier unit second and isolated-heavy first domain')
        require(all(covered(first, hub, p) for p in range(18)
                    if p not in (first, hub) and lam(first, p) < 5), 'old carrier isolated marked hub')
        key = (tuple(masks), first, second, hub, low)
        require(key not in seen, 'duplicate normalized marked carrier'); seen.add(key)
        candidates = []
        for extra in range(18):
            if extra in {first, second, hub, low}:
                continue
            # Unit branch: old first is x; extra is second's isolated w.
            # Mixed branch: old first is y; extra is unit second's isolated u.
            roles = ((first, second, hub, extra, low) if alpha == 1 else
                     (second, first, extra, hub, low))
            x, y, u, w, v = roles
            if not (lam(x, u) == 4 and lam(x, w) == lam(y, u) == 5):
                continue
            isolated = all(covered(center, H, p) for center, H in [(x, u), (y, w)]
                           for p in range(18) if p not in (center, H) and lam(center, p) < 5)
            if not isolated:
                continue
            deficit = opposite_hypotheses(masks, roles)
            candidates.append({'roles': roles, 'second_hub_multiplicity': deficit})
            marked.append({'index': index, 'roles': roles, 'words': masks, 'unit': alpha == 1})
        records.append({'index': index, 'old_hub_deficit': alpha, 'extra_marks': candidates})
    require(sum(r['old_hub_deficit'] == 1 for r in records) == 8, 'complete eight unit-first roots')
    require(not any(r['unit'] for r in marked), 'unit opposite-hub core exists')
    require([(r['index'], r['roles']) for r in marked] ==
            [(22, (11, 17, 16, 13, 2)), (23, (11, 17, 5, 13, 2)), (24, (11, 17, 8, 13, 2))],
            'complete three mixed marked cores')
    return records, marked


def complete(work):
    record, marked = decode_all(); roots = []; witnesses = []
    for row in marked:
        x, y, u, w, v = row['roles']; core = row['words']
        candidates = []
        # Entire physical universe of words avoiding the two already-full stars.
        for points in combinations([p for p in range(18) if p not in (x, y)], 5):
            mask = sum(1 << p for p in points)
            if all(len(set(points)&{p for p in range(18) if f >> p & 1}) <= 2 for f in core):
                candidates.append(mask)
        adj = [0]*len(candidates); physical = [set(p for p in range(18) if m >> p & 1) for m in candidates]
        for a, b in combinations(range(len(candidates)), 2):
            if len(physical[a]&physical[b]) <= 2:
                adj[a] |= 1 << b; adj[b] |= 1 << a
        # Different oracle: each core owns its ten actual triples. An
        # extra word is legal iff it owns none; residual words are
        # adjacent iff their owned-triple sets are disjoint.
        occupied = {q for f in literal(core) for q in combinations(sorted(f), 3)}
        oracle = []
        for points in combinations([p for p in range(18) if p not in (x, y)], 5):
            if occupied.isdisjoint(combinations(points, 3)):
                oracle.append(sum(1 << p for p in points))
        require(candidates == oracle, 'whole physical residual/triple-ownership oracle differs')
        triples = [set(combinations(sorted(f), 3)) for f in physical]
        oracle_adj = [sum(1 << b for b in range(len(candidates)) if a != b and
                          triples[a].isdisjoint(triples[b])) for a in range(len(candidates))]
        require(adj == oracle_adj, 'whole physical residual adjacency oracle differs')
        chosen, nodes = maximum(adj)
        full = sorted(core+[candidates[a] for a in chosen])
        require(opposite_hypotheses(full, row['roles']) == 3, 'attaining completion lost exact hypotheses')
        roots.append({'index': row['index'], 'roles': row['roles'], 'candidates': len(candidates),
                      'edges': sum(a.bit_count() for a in adj)//2, 'candidate_sha256': digest(candidates),
                      'adjacency_sha256': digest(adj), 'residual_maximum': len(chosen),
                      'exact_total': len(full), 'nodes': nodes, 'completion_sha256': digest(full)})
        witnesses.append({'roles': row['roles'], 'word_masks': full, 'size': len(full)})
    require([r['exact_total'] for r in roots] == [59, 61, 56], 'three complete maximum values')
    require(max(r['exact_total'] for r in roots) == 61, 'sharp mixed interface maximum')
    work = Path(work); work.mkdir(parents=True, exist_ok=True)
    (work/'LOCAL_WITNESSES.json').write_text(json.dumps(witnesses, sort_keys=True)+'\n')
    expected = json.loads((HERE/'WITNESS61.json').read_text()) if (HERE/'WITNESS61.json').exists() else None
    if expected is not None:
        require(expected == json.loads(json.dumps(witnesses[1])), 'frozen literal sharp61 witness differs')
    return {'status': 'COMPLETE_OPPOSITE_ISOLATED_HUB_INTERFACE', 'all34_markings': record,
            'unit_branch_incompatible': True, 'mixed_roots': roots, 'mixed_sharp_upper': 61,
            'covered_triangle_hypothesis': False, 'global_profile_hypothesis': False,
            'all_residuals_and_adjacency_match_owned_triple_oracle': True}
