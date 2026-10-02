"""Search-free certificate replay with separate source and axial geometry."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import resource
import signal
import time

import deps
import model as M
import reader as V
import supplier_trees as T
import strip_contact_reader as R
import strip_parametric_geometry as G
from strip_columns import require
from strip_point_suppliers import IDENTITY

HERE = Path(__file__).absolute().parent
FIXED = (IDENTITY, ((1, 0, 0, 1), (0, 6), (-1, 4)),
         ((-1, 0, 0, -1), (0, 5), (0, 3)), ((2, -3, 1, -2), (3, 6), (2, 5)))
POINTS = (((0, 4), (0, 6)), ((0, 5), (0, 6)))


def exclusion(record, entry, guard, material=True):
    require(record['case'] == entry['name'] and record['method'] == entry['method']
            and R.freeze(record['fixed']) == (IDENTITY, R.freeze(entry['pose']))
            and R.freeze(record['points']) == R.freeze(entry['points']), 'Changed literal exclusion')
    V.universal([G.neg(G.intersection(G.relative(*R.freeze(record['fixed'])))),
                 G.touching(G.relative(*R.freeze(record['fixed'])))], guard)
    if entry['method'] == 'tree': return T.check(record, entry, guard, material)
    result = R.local_check(record, guard, material)
    result.update(case=entry['name'], record_sha256=R.sha(record))
    return result


def direct_bad(first, second, feet_first, feet_second, excluded, k):
    # Actual axial set contact and independent axial matrix composition.
    if not R.E.touching(feet_first, feet_second): return False
    relative = R.E.compose(R.E.inverse(first), second)
    inverse = R.E.inverse(relative)
    angle = R.axial(((2, -3, 1, -2), (0, 5), (0, 3)), k)
    literals = {R.axial(pose, k) for pose in excluded}
    if relative in literals or inverse in literals or relative == angle or inverse == angle:
        return True
    for a, b, c, d, x, y in (relative, inverse):
        if (a, b, c, d) == (1, 0, 0, 1) and x+2*y == 6 and y not in (3-k, 4-k):
            return True
    return False


def material_matrix(atlas, entries, k, guard):
    tile = R.literal(k)
    fixed_poses = [R.axial(f, k) for f in FIXED]
    poses = [R.axial(g, k) for g in atlas]
    fixed_feet = [set(R.E.affine(tile, p)) for p in fixed_poses]
    feet = [set(R.E.affine(tile, p)) for p in poses]
    occupied = set().union(*fixed_feet)
    points = [(G.value(u, k)-2*G.value(v, k), G.value(v, k)) for u, v in POINTS]
    original = fixed_feet[0] | fixed_feet[1]
    require(set(points) <= R.E.halo(original)-occupied, 'Material demands leave the original pair halo')
    require(all(not fixed_feet[i] & fixed_feet[j]
                for j in range(len(FIXED)) for i in range(j)), 'Material fixed prefix overlaps')
    excluded = M.models(entries)
    cover = [sum(1 << j for j, p in enumerate(points) if p in footprint) for footprint in feet]
    available = 0; conflicts = []
    for i, footprint in enumerate(feet):
        guard()
        if cover[i] and not footprint & occupied and not any(
            direct_bad(p, poses[i], ff, footprint, excluded, k)
            for p, ff in zip(fixed_poses, fixed_feet)):
            available |= 1 << i
        conflict = 1 << i
        for j in range(len(feet)):
            if j != i and footprint & feet[j]:
                conflict |= 1 << j
        conflicts.append(conflict)
    return {'cover': cover, 'conflicts': conflicts, 'available': available}


def check_cut(record, entries, guard, material=True):
    require(record['complete'] is True and R.freeze(record['fixed']) == FIXED
            and R.freeze(record['points']) == POINTS, 'Changed literal P prefix or original demands')
    geometry = V.universal([
        *[G.neg(G.intersection(G.relative(f, h))) for i, h in enumerate(FIXED) for f in FIXED[:i]],
        *[V.in_halo(p, FIXED[:2]) for p in POINTS],
        *[G.neg(G.point_membership(f, p)) for p in POINTS for f in FIXED]], guard)
    require(len(record['supplier_records']) == len(POINTS), 'Missing original demand supplier record')
    atlas = set(); per_point = []
    for point, saved in zip(POINTS, record['supplier_records']):
        fresh = R.supplier_atlas(point, FIXED, guard)
        require(R.freeze(saved) == R.freeze(fresh), 'Changed complete original-halo height reduction')
        if material: V.material(point, FIXED, fresh, guard)
        atlas.update(fresh['atlas']); per_point.append(len(fresh['atlas']))
    atlas = sorted(atlas)
    require(R.freeze(record['atlas']) == R.freeze(atlas), 'Incomplete original-halo supplier atlas')
    rows = M.predicates(atlas, entries)
    coverage, eligibility, clashes, demanded = rows
    partition = R.splitter(M.flat(rows))
    require(partition == G.partition(M.flat(rows)) and partition == record['partition'],
            'Changed exact two-demand parameter partition')
    n = len(atlas); samples = []
    universal = {'cover': [0]*n, 'conflicts': [(1 << n)-1]*n, 'available': 0}
    for k in partition['representatives']:
        guard(); require(all(G.evaluate(p, k) for p in demanded), 'Invalid original demanded cell')
        cover = [sum(1 << j for j, p in enumerate(row) if G.evaluate(p, k)) for row in coverage]
        con = [1 << i for i in range(n)]
        for (i, j), predicate in clashes.items():
            if G.evaluate(predicate, k): con[i] |= 1 << j; con[j] |= 1 << i
        av = sum(1 << i for i, predicate in enumerate(eligibility) if cover[i] and G.evaluate(predicate, k))
        matrix = {'cover': cover, 'conflicts': con, 'available': av}
        if material: require(material_matrix(atlas, entries, k, guard) == matrix,
                             'Independent axial geometry or literal contact cuts differ')
        samples.append({'k': k, 'matrix': matrix})
        universal['available'] |= av
        for i in range(n):
            universal['cover'][i] |= cover[i]; universal['conflicts'][i] &= con[i]
    require(samples == record['samples'] and universal == record['universal'],
            'Changed exact sample or conservative matrix')
    nodes = R.dag_check(record['proof'], universal, len(POINTS))
    require(per_point == [12, 13] and len(atlas) == 19, 'Unexpected complete supplier inventory')
    left = [i for i, c in enumerate(universal['cover']) if universal['available'] >> i & 1 and c & 1]
    right = [i for i, c in enumerate(universal['cover']) if universal['available'] >> i & 1 and c & 2]
    require(len(left) == 6 and len(right) == 4 and not set(left) & set(right),
            'Unexpected eligible first/second supplier inventory')
    require(all(universal['conflicts'][i] >> j & 1 for i in left for j in right),
            'Compatible physical first/second supplier pair remains')
    return {'original_demands': 2, 'per_point_suppliers': per_point, 'atlas_suppliers': n,
            'eligible_suppliers_per_demand': [len(left), len(right)], 'physical_cross_clashes': len(left)*len(right),
            'cuts': partition['cuts'], 'geometry_cuts': geometry['cuts'], 'DAG_nodes': nodes,
            'record_sha256': R.sha(record),
            'conclusion': 'Registered shifted contact (I;6,4-k) is outside E2 for every k>=6',
            'premises': '9404 forced R;9474 S-or-P;9542 excludes S; six newly checked E1 cuts'}


def main():
    start = time.monotonic(); calls = 0
    def guard():
        nonlocal calls
        calls += 1
        if deps.paused() or time.monotonic()-start >= 43 or calls > 100000:
            raise RuntimeError('Operational/43s/100000 guard; incomplete check inconclusive')
    def alarm(a, b): raise RuntimeError('45s signal guard; incomplete check inconclusive')
    signal.signal(signal.SIGALRM, alarm); signal.alarm(45)
    entries = json.loads((HERE/'inputs.json').read_text())['cases']
    require([e['name'] for e in entries] == [f'B{i:02d}' for i in range(1, 7)]
            and [e['method'] for e in entries] == ['finite', 'tree', 'finite', 'finite', 'finite', 'tree'],
            'Changed six-case literal inventory')
    folder = HERE/'generated/normal'
    records = {e['name']: json.loads((folder/f"{e['name']}.json").read_text()) for e in entries}
    exclusions = [exclusion(records[e['name']], e, guard) for e in entries]
    cut = json.loads((folder/'shift-cut.json').read_text())
    result = check_cut(cut, entries, guard)
    damages = []
    def negative(label, operation):
        try: operation()
        except ValueError: damages.append(label)
        else: raise ValueError('Damaged certificate accepted: '+label)
    finite = entries[2]; tree = entries[1]
    for label in ('changed_case_pose', 'missing_supplier', 'changed_partition', 'missing_DAG_node', 'changed_conflict'):
        d = deepcopy(records[finite['name']])
        if label == 'changed_case_pose': d['fixed'][1][1][1] += 1
        elif label == 'missing_supplier': d['supplier_records'][0]['atlas'].append(IDENTITY)
        elif label == 'changed_partition': d['partition']['cuts'].append(999)
        elif label == 'missing_DAG_node': d['proof']['nodes'].pop()
        else: d['universal']['conflicts'][0] ^= 1
        negative(label, lambda damaged=d: exclusion(damaged, finite, guard, False))
    for label in ('missing_cap_branch', 'new_halo_demand', 'false_empty_leaf'):
        d = deepcopy(records[tree['name']])
        if label == 'missing_cap_branch': d['tree']['children'].pop()
        elif label == 'new_halo_demand': d['tree']['children'][0]['node']['point'] = ((0, 100), (0, 100))
        else: d['tree']['children'][0]['node']['suppliers']['atlas'].append(IDENTITY)
        negative(label, lambda damaged=d: exclusion(damaged, tree, guard, False))
    for label in ('changed_P_prefix', 'changed_original_demand', 'missing_original_demand', 'missing_atlas_pose',
                  'changed_cover', 'changed_cut_conflict', 'changed_available', 'changed_cut_partition', 'missing_cut_DAG'):
        d = deepcopy(cut)
        if label == 'changed_P_prefix': d['fixed'][3][1][1] += 1
        elif label == 'changed_original_demand': d['points'][1][0][1] += 1
        elif label == 'missing_original_demand': d['supplier_records'].pop()
        elif label == 'missing_atlas_pose': d['atlas'].pop()
        elif label == 'changed_cover': d['universal']['cover'][0] ^= 1
        elif label == 'changed_cut_conflict': d['universal']['conflicts'][0] ^= 1
        elif label == 'changed_available': d['universal']['available'] ^= 1
        elif label == 'changed_cut_partition': d['partition']['cuts'].append(999)
        else: d['proof']['nodes'].pop()
        negative(label, lambda damaged=d: check_cut(damaged, entries, guard, False))
    math = {'exclusions': exclusions, 'shift_cut': result, 'damaged_controls': damages}
    signal.alarm(0)
    out = {'agent': 'six-heesch-2', 'role': 'researcher', 'complete': True, 'evidence': math,
           'mathematics_sha256': R.sha(math), 'seconds': round(time.monotonic()-start, 3),
           'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
           'checked_utc': datetime.now(timezone.utc).isoformat()}
    mode = 'normal' if __debug__ else 'optimized'
    (HERE/'generated'/f'reader-{mode}.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'evidence'}), flush=True)


if __name__ == '__main__': main()
