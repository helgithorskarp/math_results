"""Complete integral surrounds with full overlaps and necessary interior cuts."""
import json
from shared import BASE, PARENT, PRIOR, g, footprint, compact, masks, star, parent_build


def inventory(shape, fixed):
    occupied = set()
    for pose in fixed:
        f = footprint(shape, pose)
        assert len(f) == 214 and occupied.isdisjoint(f)
        occupied.update(f)
    vm = masks(occupied)
    boundary = {v: m for v, m in vm.items() if m != 63}
    assert all(sum(((m >> j) & 1) != ((m >> ((j + 1) % 6)) & 1)
                   for j in range(6)) == 2 for m in boundary.values())
    required = set()
    for v in boundary:
        required.update(star(v) - occupied)
    tried, good, feet = set(), {}, {}
    for matrix in g.matrices():
        rotation = {'matrix': list(matrix), 'translation': [0, 0]}
        rotated = sorted(compact(g.move(t, rotation)) for t in shape)
        for k, x, y in sorted(required):
            for q, a, b in rotated:
                if k != q:
                    continue
                tx, ty = x - a, y - b
                key = (matrix, (tx, ty))
                if key in tried:
                    continue
                tried.add(key)
                if any((r, u + tx, v + ty) in occupied for r, u, v in rotated):
                    continue
                f = frozenset((r, u + tx, v + ty) for r, u, v in rotated)
                assert len(f) == 214 and occupied.isdisjoint(f)
                good[key] = {'matrix': list(matrix), 'translation': [tx, ty]}
                feet[key] = f
                assert len(good) <= 10000, 'incomplete inventory guard; no exclusion'
    keys = sorted(good)
    poses, fs = [good[k] for k in keys], [feet[k] for k in keys]
    owners = {t: [] for t in sorted(required)}
    for j, f in enumerate(fs, 1):
        for t in f & owners.keys():
            owners[t].append(j)
    expected = json.loads((PRIOR / 'expected.json').read_text())
    raw = g.catalogues(shape)[3]
    negatives = [raw[row['attachment'] - 1] for row in expected['pair_negatives']]
    fixed_keys = {g.key(q) for q in fixed}
    assert all(g.key(g.compose(p, q)) not in fixed_keys for p in fixed for q in negatives)
    lookup = {g.key(q): j for j, q in enumerate(poses, 1)}
    pruned, pairs = set(), set()
    for p in fixed:
        for q in negatives:
            for r in (q, g.inverse(q)):
                j = lookup.get(g.key(g.compose(p, r)))
                if j is not None:
                    pruned.add(j)
    for i, p in enumerate(poses, 1):
        for q in negatives:
            j = lookup.get(g.key(g.compose(p, q)))
            if j is not None:
                assert i != j
                pairs.add(tuple(sorted((i, j))))
    report = {'fixed_copies': len(fixed), 'fixed_cells': len(occupied),
              'boundary_vertices': len(boundary), 'required_cells': len(required),
              'anchored_trials': len(tried), 'candidates': len(poses),
              'fixed_pair_pruned': len(pruned), 'candidate_pair_exclusions': len(pairs)}
    return poses, fs, owners, pruned, pairs, report


def seed_formula(fixed, inv):
    poses, fs, owners, pruned, pairs, report = inv
    clauses, conflicts = parent_build.formula(fs, owners, pruned, pairs)
    census, cuts = [], set()
    imported = json.loads((PARENT / 'patterns.json').read_text())
    local = json.loads((BASE / 'hole.json').read_text())
    for row in imported + [local]:
        instances = parent_build.instances(row, fixed, poses)
        census.append({'pattern_sha256': row['pattern_sha256'], 'instances': len(instances)})
        cuts.update(instances)
    clauses.extend(sorted(cuts))
    return clauses, {'inventory': report, 'binary_conflicts': conflicts,
                     'pattern_census': census, 'distinct_pattern_clauses': len(cuts)}


def inputs():
    shape, fixture = g.inputs()
    fixed = [q for q in fixture if q['level'] <= 3]
    assert len(fixed) == 40
    cases = json.loads((BASE / 'cases.json').read_text())
    assert [row['name'] for row in cases] == ['original', 'A', 'B', 'C']
    return shape, fixture, fixed, cases


def fourth(fixed, candidates, case):
    selected = case['selected_indices']
    assert selected == sorted(set(selected)) and len(selected) == 39
    assert all(type(j) is int and 1 <= j <= len(candidates) for j in selected)
    return fixed + [dict(candidates[j - 1], level=4) for j in selected]
