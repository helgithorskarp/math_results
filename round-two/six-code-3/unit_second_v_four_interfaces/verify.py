"""Independent literal point-assignment checker; Python standard library only.

Imports neither domain.py nor produce.py. It enumerates each common-tail
point individually, rebuilds full words, and compares complete carrier and
positive-record hashes. Supplied groups are checked solely as subgroups.
"""
import argparse
import collections
import hashlib
import itertools
import json
import time
from pathlib import Path

PIN = 'c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7'

def need(test, message):
    if not test:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def inspect(data):
    need(len(data['stars']) == len(data['groups']) == 23, 'wrong fixture population')
    rows = []
    for index, (raw, permutations) in enumerate(zip(data['stars'], data['groups'])):
        blocks = tuple(sorted(tuple(sorted(q)) for q in raw))
        need(len(blocks) == len(set(blocks)) == 20, 'twenty distinct blocks')
        need(all(len(q) == len(set(q)) == 4 and set(q) <= set(range(17)) for q in blocks), 'invalid block')
        pairs = [tuple(sorted(pair)) for q in blocks for pair in itertools.combinations(q, 2)]
        need(len(pairs) == len(set(pairs)) == 120, 'repeated covered pair')
        covered = frozenset(pairs)
        replication = {p: sum(p in q for q in blocks) for p in range(17)}
        need(max(replication.values()) <= 5 and sum(replication.values()) == 80, 'invalid replications')
        high = frozenset(p for p in range(17) if replication[p] < 5)
        low = frozenset(range(17)) - high
        missing = {p: frozenset(q for q in range(17) if q != p and tuple(sorted((p, q))) not in covered)
                   for p in range(17)}
        need(all(len(missing[p]) == 1 and missing[p] <= high for p in low), 'bad low leave')
        maps = tuple(sorted(tuple(g) for g in (permutations or [list(range(17))])))
        need(len(set(maps)) == len(maps) and tuple(range(17)) in maps, 'bad subgroup identity or duplicate')
        for g in maps:
            need(len(g) == 17 and set(g) == set(range(17)), 'nonbijective subgroup map')
            need(tuple(sorted(tuple(sorted(g[p] for p in q)) for q in blocks)) == blocks, 'false automorphism')
        maps_set = set(maps)
        for g, h in itertools.product(maps, repeat=2):
            need(tuple(g[h[p]] for p in range(17)) in maps_set, 'subgroup not closed')
        first = []
        for u, v, y in itertools.product(sorted(high), sorted(low), sorted(high)):
            if len({u, v, y}) != 3 or replication[y] != 4:
                continue
            if missing[u] & high or missing[v] != {y}:
                continue
            if tuple(sorted((u, v))) in covered and tuple(sorted((u, y))) in covered:
                first.append((u, v, y))
        second = []
        if all(replication[p] == 4 for p in high):
            for u, v, x in itertools.product(sorted(low), sorted(high), sorted(high)):
                if v == x or tuple(sorted((v, x))) in covered:
                    continue
                b = next(iter(missing[u]))
                if tuple(sorted((u, x))) in covered:
                    second.append((u, v, x, b))
        def quotient(marks):
            classes = {}
            for mark in sorted(set(marks)):
                images = frozenset(tuple(g[p] for p in mark) for g in maps)
                need(images <= set(marks), 'automorphism leaves marking domain')
                representative = min(images)
                if representative in classes:
                    need(classes[representative] == images, 'orbit overlap disagreement')
                else:
                    classes[representative] = images
            need(set().union(*classes.values()) == set(marks) if classes else not marks, 'orbit coverage gap')
            return [dict(representative=list(rep), members=[list(t) for t in sorted(images)])
                    for rep, images in sorted(classes.items())]
        first_orbits, second_orbits = quotient(first), quotient(second)
        rows.append(dict(index=index, blocks=blocks, replication=replication, high=high, low=low,
                         missing=missing, maps=maps, first=sorted(first), second=sorted(second),
                         first_orbits=first_orbits, second_orbits=second_orbits))
    return rows

def marked_domain(rows):
    output = dict(rows=[], first=[], second=[])
    for row in rows:
        i = row['index']
        output['rows'].append(dict(fixture=i, first_raw=len(row['first']), second_raw=len(row['second']),
                                   first_orbits=row['first_orbits'], second_orbits=row['second_orbits'],
                                   subgroup_order=len(row['maps'])))
        for name in ('first', 'second'):
            output[name].extend([i, orbit['representative']] for orbit in row[name+'_orbits'])
    return output

def point_maps(first, second, first_mark, second_mark):
    """Assign individual tail points; no permutations of block tails are used."""
    u, v, y = first_mark
    su, sv, sx, sb = second_mark
    source = [set(q) - {sx} for q in second['blocks'] if sx in q]
    target = [set(q) - {y} for q in first['blocks'] if y in q]
    need(len(source) == len(target) == 4 and all(len(t) == 3 for t in source + target), 'bad common tails')
    need(len(set().union(*source)) == len(set().union(*target)) == 12, 'common tails repeat point')
    source_group = {p: i for i, t in enumerate(source) for p in t}
    target_group = {p: i for i, t in enumerate(target) for p in t}
    need(su in source_group and u in target_group and sv not in source_group and v not in target_group,
         'special tail marking')
    phi = [-1] * 17
    phi[su], phi[sv], phi[sx] = u, v, 17
    association = [-1] * 4
    association[source_group[su]] = target_group[u]
    used_points = {u, v, 17}
    used_tails = {target_group[u]}
    order = sorted(set(source_group) - {su})
    states = 0
    def dfs(depth):
        nonlocal states
        states += 1
        need(states <= 200000, 'INCOMPLETE point-DFS state guard')
        if depth == len(order):
            yield tuple(phi)
            return
        p = order[depth]
        group = source_group[p]
        previous = association[group]
        for image in sorted(target_group):
            if image in used_points:
                continue
            tail = target_group[image]
            if previous >= 0 and tail != previous:
                continue
            if previous < 0 and tail in used_tails:
                continue
            phi[p] = image
            used_points.add(image)
            if previous < 0:
                association[group] = tail
                used_tails.add(tail)
            yield from dfs(depth+1)
            if previous < 0:
                used_tails.remove(tail)
                association[group] = -1
            used_points.remove(image)
            phi[p] = -1
    maps = list(dfs(0))
    need(len(maps) == len(set(maps)) == 2592, 'partial map universe incomplete or duplicated')
    return sorted(maps), states

def check_product(rows, first_ref, second_ref):
    fi, (u, v, y) = first_ref
    si, (su, sv, sx, sb) = second_ref
    first, second = rows[fi], rows[si]
    start = time.monotonic()
    partials, states = point_maps(first, second, (u, v, y), (su, sv, sx, sb))
    first_words = [frozenset(q) | {17} for q in first['blocks']]
    private_second = [q for q in second['blocks'] if sx not in q]
    def reject(phi):
        # Direct intersections include every first word and the actual second center.
        for q in private_second:
            known_word = {y} | {phi[p] for p in q if phi[p] >= 0}
            if any(len(known_word & word) >= 3 for word in first_words):
                return True
        return False
    positives = []
    represented = 0
    full_checked = 0
    for partial in partials:
        represented += 6
        if represented % 768 == 0:
            need(time.monotonic()-start <= 10, 'INCOMPLETE literal product time guard')
        if reject(partial):
            continue
        remaining_source = sorted(p for p in range(17) if partial[p] < 0)
        remaining_target = sorted((set(range(18)) - {y}) - set(partial))
        need(len(remaining_source) == len(remaining_target) == 3, 'residual bijection has wrong size')
        for images in itertools.permutations(remaining_target):
            full_checked += 1
            phi = list(partial)
            for p, image in zip(remaining_source, images):
                phi[p] = image
            if reject(phi):
                continue
            need(set(phi) == set(range(18))-{y} and len(set(phi)) == 17, 'nonbijective full map')
            second_words = [frozenset(phi[p] for p in q) | {y} for q in second['blocks']]
            words = sorted(set(first_words + second_words), key=lambda w: sum(1 << p for p in w))
            need(len(words) == 36, 'wrong complete union size')
            need(all(len(a & b) <= 2 for a, b in itertools.combinations(words, 2)), 'full-word collision')
            need(sum(17 in w for w in words) == sum(y in w for w in words) == 20, 'star degrees changed')
            source_uv = sum(su in q and sv in q for q in second['blocks'])
            need(source_uv in (0, 1) and sum({u, v} <= w for w in words) == 1 + source_uv,
                 'observed hub multiplicity differs from actual source pair coverage')
            masks = [sum(1 << p for p in w) for w in words]
            need(sum({17, y} <= w for w in words) == 4, 'center pair multiplicity')
            triangle_points = []
            for t in sorted(set(range(18)) - {17, y, u, v}):
                xt = sum({17, t} <= w for w in words)
                yt = sum({y, t} <= w for w in words)
                if xt == yt == 4 and not any({17, y, t} <= w for w in words):
                    triangle_points.append(t)
            positives.append(dict(point_map=phi, word_masks=masks, triangle_points=triangle_points))
    need(represented == 15552, 'full map universe accounting gap')
    positives.sort(key=lambda row: row['point_map'])
    return dict(partial_maps_sha256=sha([list(phi) for phi in partials]),
                positives_sha256=sha(positives), positives=positives, dfs_states=states,
                full_maps_tested=full_checked, represented_full_maps=represented,
                seconds=time.monotonic()-start)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixtures', required=True)
    parser.add_argument('--primary-work', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--first', type=int, default=0)
    parser.add_argument('--finish', type=int)
    args = parser.parse_args()
    raw = Path(args.fixtures).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'fixture source pin mismatch')
    rows = inspect(json.loads(raw))
    ds = marked_domain(rows)
    work = Path(args.primary_work)
    need(json.loads((work/'domains.json').read_text()) == ds, 'literal mark/orbit domains disagree')
    products = list(itertools.product(ds['first'], ds['second']))
    finish = len(products) if args.finish is None else args.finish
    need(0 <= args.first <= finish <= len(products), 'invalid product interval')
    if args.first == 0 and finish == len(products):
        expected_files = {f'product-{i:03d}.json' for i in range(len(products))}
        need({p.name for p in work.glob('product-*.json')} == expected_files, 'primary product population gap')
    records = []
    start = time.monotonic()
    for i in range(args.first, finish):
        first_ref, second_ref = products[i]
        primary = json.loads((work/f'product-{i:03d}.json').read_text())
        need(primary['status'] == 'COMPLETE_MARKED_PRODUCT' and primary['product_index'] == i, 'incomplete primary product')
        need(primary['first'] == first_ref and primary['second'] == second_ref, 'primary product marking differs')
        need(primary['counts']['partial_maps'] == 2592 and
             sum(primary['rejected_full_maps'].values()) + len(primary['positives']) == 15552,
             'primary full-map accounting differs')
        result = check_product(rows, first_ref, second_ref)
        need(primary['counts']['full_maps_tested'] == result['full_maps_tested'], 'explicit full-map count differs')
        need(primary['partial_maps_sha256'] == result['partial_maps_sha256'], 'complete partial-map universe differs')
        need(primary['positives_sha256'] == result['positives_sha256'], 'complete positive maps differ')
        need(sorted(primary['positives'], key=lambda row: row['point_map']) == result['positives'], 'literal positive records differ')
        record = {k:v for k,v in result.items() if k!='seconds'}
        record.update(product_index=i, first=first_ref, second=second_ref)
        records.append(record)
        if i % 30 == 0 or result['positives']:
            print(json.dumps(dict(index=i, positives=len(result['positives']), dfs_states=result['dfs_states'])), flush=True)
    output = dict(status='COMPLETE_INDEPENDENT_POINT_DFS' if args.first == 0 and finish == len(products) else 'COMPLETE_SELECTED_PRODUCTS_ONLY',
                  first=args.first, finish=finish, total_products=len(products), domain_sha256=sha(ds),
                  records_sha256=sha(records), records=records, seconds=time.monotonic()-start)
    Path(args.output).write_text(json.dumps(output, sort_keys=True, indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='records'}), flush=True)

if __name__ == '__main__':
    main()
