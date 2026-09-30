#!/usr/bin/env python3
"""six-reviewer-2: independent saturated double-star audit, exact integers only."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import time


def insist(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask -= low


def mask(points):
    return sum(1 << x for x in points)


def pairs(word):
    return frozenset(combinations(bits(word), 2))


def words_json(words):
    return sorted([list(bits(w)) for w in words])


def packing(words, center=None, size=None):
    insist(len(words) == len(set(words)), 'duplicate word')
    insist(all(0 <= w < 1 << 18 and w.bit_count() == 5 for w in words), 'word domain')
    insist(all((a & b).bit_count() <= 2 for a, b in combinations(words, 2)), 'repeated triple')
    if center is not None:
        insist(all(w >> center & 1 for w in words), 'wrong center')
    if size is not None:
        insist(len(words) == size, 'wrong star size')


def mul(a, b):
    # Multiply the two degree-one binary polynomials, then reduce z^2=z+1.
    lo = (a & 1) * (b & 1)
    mid = ((a & 1) * (b >> 1)) ^ ((a >> 1) * (b & 1))
    hi = (a >> 1) * (b >> 1)
    return (lo ^ hi) | ((mid ^ hi) << 1)


def plane():
    # Generate translates of one-dimensional subspaces, with no line equations.
    directions = [(1, t) for t in range(4)] + [(0, 1)]
    lines = {mask(4 * (x ^ mul(s, dx)) + (y ^ mul(s, dy)) for s in range(4))
             for dx, dy in directions for x in range(4) for y in range(4)}
    counts = Counter(p for w in lines for p in pairs(w))
    insist(len(lines) == 20 and len(counts) == 120 and set(counts.values()) == {1}, 'plane')
    return tuple(sorted(lines))


AXES = {mask(range(4)), mask((0, 4, 8, 12))}


def first_star(replacement):
    result = tuple(sorted((line ^ 1 | 1 << replacement | 1 << 17)
                          if line & 1 and line not in AXES else line | 1 << 17
                          for line in plane()))
    packing(result, 17, 20)
    return result


def valid_extension(word, star):
    return all((word & old).bit_count() <= 2 for old in star if old != word)


def saturated_row(words, center, expected):
    insist(sum(w >> center & 1 for w in words) == 20, 'saturated replication changed')
    actual = {x: 5 - sum((w >> center & 1) and (w >> x & 1) for w in words)
              for x in range(18) if x != center}
    insist({x: d for x, d in actual.items() if d} == expected, 'saturated deficit pattern changed')


def compatibility(columns):
    supports = list(map(pairs, columns))
    adjacency = [0] * len(columns)
    for i, j in combinations(range(len(columns)), 2):
        if not supports[i] & supports[j]:
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    return adjacency


def colored_order(active, adjacency):
    """Greedy independent color classes: their count bounds every clique."""
    order, bounds, color = [], [], 0
    while active:
        color += 1
        eligible = active
        while eligible:
            v = (eligible & -eligible).bit_length() - 1
            bit = 1 << v
            order.append(v)
            bounds.append(color)
            active ^= bit
            eligible &= ~bit & ~adjacency[v]
    return order, bounds


def clique_census(adjacency, target, cap=200000, seconds=10):
    """All target cliques, each once; no reliance on a cover-search routine."""
    insist(target >= 0 and cap >= 0, 'invalid clique parameters')
    n = len(adjacency)
    insist(all(a >= 0 and a < 1 << n and not (a >> i & 1)
               for i, a in enumerate(adjacency)), 'bad graph mask or loop')
    insist(all(bool(adjacency[i] >> j & 1) == bool(adjacency[j] >> i & 1)
               for i, j in combinations(range(n), 2)), 'asymmetric graph')
    answers, states = [], 0
    started = time.monotonic()

    def walk(active, chosen):
        nonlocal states
        states += 1
        if states > cap or time.monotonic() - started > seconds:
            raise RuntimeError('INCOMPLETE: clique census guard')
        need = target - len(chosen)
        if not need:
            answers.append(tuple(sorted(chosen)))
            return
        if active.bit_count() < need:
            return
        order, bounds = colored_order(active, adjacency)
        for k in range(len(order) - 1, -1, -1):
            if bounds[k] < need:
                return
            v = order[k]
            walk(active & adjacency[v], chosen + (v,))
            active &= ~(1 << v)

    walk((1 << n) - 1, ())
    insist(len(answers) == len(set(answers)), 'repeated clique')
    insist(all(len(q) == target and all(adjacency[i] >> j & 1 for i, j in combinations(q, 2))
               for q in answers), 'false clique witness')
    return sorted(answers), states


def complete_links(required, columns, fixed, center):
    insist(len(required) % 6 == 0, 'nonintegral pair cover')
    insist(all(pairs(q) <= required for q in columns), 'column outside pair universe')
    cliques, states = clique_census(compatibility(columns), len(required) // 6)
    stars = []
    for ids in cliques:
        chosen = tuple(columns[i] for i in ids)
        covered = Counter(p for q in chosen for p in pairs(q))
        insist(set(covered) == required and set(covered.values()) == {1}, 'not a pair cover')
        star = tuple(sorted(set(fixed) | {q | 1 << center for q in chosen}))
        packing(star, center, 20)
        stars.append(star)
    insist(len(stars) == len(set(stars)), 'duplicated link')
    return sorted(stars), states


def point_capacity(columns, vertices):
    union = set().union(*(pairs(q) for q in columns)) if columns else set()
    degrees = [sum(x in p for p in union) for x in vertices]
    return sum(d // 3 for d in degrees) // 4, degrees


def tail_partitions(points):
    if not points:
        yield ()
    else:
        p = points[0]
        for a, b in combinations(points[1:], 2):
            tail = (p, a, b)
            for rest in tail_partitions(tuple(x for x in points if x not in tail)):
                yield (tail,) + rest


def source_projection(path, mode):
    raw = path.read_bytes()
    expected_sha = {'shared': '91a3969e36e598149f10dfbc22fe5d73f0c13a7c57ed43e63591f89f56f40aba',
                    'adjacent': 'c8b902a7c0a0f6250bffeadeb40109ad8f6829cd3274147145bf1feec52790e4'}[mode]
    insist(sha256(raw).hexdigest() == expected_sha, 'reference input hash mismatch')
    d = json.loads(raw)
    if mode == 'shared':
        stars = {case['c']: {tuple(tuple(w) for w in item['vstar']): item
                            for item in case['stars']} for case in d['cases']}
    else:
        stars = {}
        for case in d['primary']['cases']:
            part = tuple(tuple(t) for t in case['partition'])
            stars[part] = {tuple(tuple(q) for q in item['nonorigin_quads']): item
                           for item in case['compatible_second_stars']}
    return sha256(raw).hexdigest(), d, stars


def shared_audit(source):
    source_sha, manifest, expected = source_projection(source, 'shared')
    u, v, b = 17, 1, 16
    root = first_star(b)
    fixed = tuple(w for w in root if w >> v & 1)
    h = tuple(x for x in range(18) if x not in (u, v, b))
    groups = [w ^ 1 << u ^ 1 << v for w in fixed]
    insist(len(fixed) == 5 and mask(h) == sum(groups), 'shared pencil')
    maps = []
    for s in (1, 2, 3):
        for conjugate in (False, True):
            f = lambda z: mul(z, z) if conjugate else z
            p = tuple(4 * mul(s, f(x)) + f(y) for x in range(4) for y in range(4)) + (b, u)
            insist(len(set(p)) == 18 and all(p[x] == x for x in (0, v, b, u)), 'flag map')
            insist({mask(p[x] for x in bits(w)) for w in root} == set(root), 'flag transport')
            maps.append(p)
    insist(len(set(maps)) == 6 and all(tuple(p[q[x]] for x in range(18)) in maps
                                      for p in maps for q in maps), 'flag group')
    orbits = [sorted({p[c] for p in maps}) for c in (2, 4, 5, 6)]
    insist(sorted(x for orbit in orbits for x in orbit) == list(range(2, 16)), 'flag orbit cover')
    results, nodes_total, leaves_total, missing_total = [], 0, 0, 0
    for c in (2, 4, 5, 6):
        cg = next(g for g in groups if g >> c & 1)
        available = tuple(x for x in h if not cg >> x & 1)
        tails = list(combinations(available, 3))
        insist(len(tails) == 220, 'tail universe')
        rows, found = [], {}
        for tail in tails:
            special = mask((v, c) + tail)
            if not valid_extension(special, root):
                continue
            known = fixed + (special,)
            cwords = [w for w in known if w >> c & 1]
            insist(len(cwords) == 2, 'c pencil')
            # Ordinary double-star structure determines every leave edge.
            cthirds = set(x for w in cwords for x in bits(w) if x not in (v, c))
            leave = {tuple(sorted((c, b)))}
            for x in range(18):
                if x not in (v, c, b):
                    leave.add(tuple(sorted((b if x in cthirds else c, x))))
            used = set(p for w in known for p in pairs(w ^ 1 << v))
            insist(not used & leave, 'fixed word hits double-star leave')
            required = set(combinations(tuple(x for x in range(18) if x != v), 2)) - leave - used
            insist(len(required) == 84, 'shared pair universe')
            columns = tuple(mask(q) for q in combinations(tuple(x for x in range(18) if x not in (u, v)), 4)
                            if pairs(mask(q)) <= required and valid_extension(mask(q) | 1 << v, root))
            stars, states = complete_links(required, columns, known, v)
            nodes_total += states
            row_digest = sha256(encoded(sorted(required))).hexdigest()
            col_digest = sha256(encoded([list(q) for q in sorted(tuple(bits(q)) for q in columns)])).hexdigest()
            old = next(r for case in manifest['cases'] if case['c'] == c
                       for r in case['second_star_searches'] if r['tail'] == list(tail))
            insist((len(columns), len(stars), row_digest, col_digest) ==
                   (old['columns'], old['second_stars'], old['rows_sha256'], old['columns_sha256']), 'shared instance differs')
            rows.append({'tail': list(tail), 'columns': len(columns), 'stars': len(stars),
                         'clique_states': states, 'rows_sha256': row_digest, 'columns_sha256': col_digest})
            for star in stars:
                key = tuple(tuple(bits(w)) for w in sorted(star, key=lambda w: tuple(bits(w))))
                insist(key not in found, 'shared star repeated across tails')
                union = tuple(sorted(set(root) | set(star)))
                packing(union)
                insist(len(union) == 35, 'shared union size')
                saturated_row(union, u, {0: 3, b: 2})
                saturated_row(union, v, {c: 3, b: 2})
                details = anchor_audit(union, b, h, expected[c][key])
                found[key] = details
                leaves_total += details.get('leave_cases', 0)
                missing_total += details.get('missing_pair_cases', 0)
        insist(set(found) == set(expected[c]), 'shared star-list differs')
        insist(len(rows) == next(case['compatible_other_origin_lines'] for case in manifest['cases'] if case['c'] == c), 'shared tail-list differs')
        results.append({'c': c, 'tail_cases': len(rows), 'stars': len(found), 'instances': rows,
                        'anchor_results': [{'vstar': [list(w) for w in key], **value} for key, value in sorted(found.items())]})
    return {'manifest_sha256': source_sha, 'flag_orbits': orbits, 'clique_states': nodes_total,
            'leave_cases': leaves_total, 'missing_pair_cases': missing_total, 'cases': results}


def anchor_audit(union, b, h, old):
    fixed = [w for w in union if w >> b & 1]
    insist(len(fixed) == 6, 'fixed b incidence')
    tails = [w & mask(h) for w in fixed]
    freq = Counter(x for t in tails for x in bits(t))
    q = sum(freq[x] == 2 for x in h)
    insist(q == old['overlap'], 'anchor overlap differs')
    raw_bound = sum((14 - 2 * freq[x]) // 3 for x in h) // 4
    insist(raw_bound == (60 - q) // 4, 'ordinary frequency bound')
    columns = tuple(mask(t) for t in combinations(h, 4)
                    if valid_extension(mask(t) | 1 << b, union))
    # This extra necessary capacity bound does not presume saturation or its leave.
    candidate_bound, degrees = point_capacity(columns, h)
    answer = {'overlap': q, 'ordinary_extra_bound': raw_bound,
              'all_anchor_candidates': len(columns), 'candidate_capacity_bound': candidate_bound,
              'candidate_pair_degrees': degrees}
    if q >= 5:
        insist(raw_bound <= 13 and old['status'] == 'POINT_CAPACITY', 'capacity exclusion')
        return answer
    used = set(p for t in tails for p in pairs(t))
    insist(len(used) == 18, 'fixed anchor pair count')
    free = set(combinations(h, 2)) - used
    trials = []
    for e in h:
        degree = {x: freq[x] - 1 + 3 * (x == e) for x in h}
        if any(d < 0 or d > 3 for d in degree.values()):
            continue
        possible = [(x, y) for x, y in combinations(h, 2) if degree[x] and degree[y]]
        for leave in combinations(possible, 3):
            realized = Counter(x for p in leave for x in p)
            if any(realized[x] != degree[x] for x in h):
                continue
            if not set(leave) <= free:
                trials.append({'e': e, 'leave': [list(p) for p in leave], 'status': 'FIXED_PAIR_CONFLICT'})
                continue
            required = free - set(leave)
            legal = tuple(qword for qword in columns if pairs(qword) <= required)
            covered = set(p for qword in legal for p in pairs(qword))
            missing = sorted(required - covered)
            insist(len(required) == 84 and missing, 'missing-pair obstruction fails')
            trials.append({'e': e, 'leave': [list(p) for p in leave], 'status': 'UNCOVERABLE_PAIR',
                           'columns': len(legal), 'rows_sha256': sha256(encoded(sorted(required))).hexdigest(),
                           'columns_sha256': sha256(encoded(sorted(list(bits(w)) for w in legal))).hexdigest(),
                           'uncoverable_pair': list(missing[0]), 'uncoverable_pairs': len(missing)})
    trials.sort(key=lambda r: (r['e'], r['leave']))
    insist(trials == old['trials'], 'anchor leave/certificate entry differs')
    answer.update(leave_cases=len(trials), missing_pair_cases=sum(r['status'] == 'UNCOVERABLE_PAIR' for r in trials), trials=trials)
    return answer


def adjacent_audit(source):
    source_sha, manifest, expected = source_projection(source, 'adjacent')
    u, v, b = 17, 0, 5
    root = first_star(16)
    fixed = tuple(w for w in root if w >> v & 1)
    h = tuple(x for x in range(18) if x not in (u, v, b))
    unavailable = {u, v, b} | set(x for w in fixed for x in bits(w))
    covered = tuple(x for x in range(18) if x not in unavailable)
    insist(len(covered) == 9, 'adjacent nine-point universe')
    all_parts = list(tail_partitions(covered))
    insist(len(all_parts) == len(set(all_parts)) == 280, 'partition cover')
    results, nodes_total = [], 0
    for part in all_parts:
        extra = tuple(mask((v, b) + t) for t in part)
        if not all(valid_extension(w, root) for w in extra):
            continue
        known = fixed + extra
        groups = [w & mask(h) for w in known]
        insist(len(groups) == 5 and sum(groups) == mask(h), 'adjacent pencil')
        required = set(combinations(h, 2)) - set(p for g in groups for p in pairs(g))
        insist(len(required) == 90, 'adjacent pair universe')
        columns = tuple(mask(t) for t in combinations(h, 4)
                        if pairs(mask(t)) <= required and valid_extension(mask(t) | 1 << v, root))
        stars, states = complete_links(required, columns, known, v)
        nodes_total += states
        got = {}
        for star in stars:
            remaining = tuple(w ^ 1 << v for w in star if w not in known)
            key = tuple(sorted(tuple(bits(w)) for w in remaining))
            union = tuple(sorted(set(root) | set(star)))
            packing(union)
            insist(len(union) == 38 and sum(w >> b & 1 for w in union) == 8, 'adjacent anchor incidence')
            candidates = tuple(mask(t) for t in combinations(h, 4)
                               if valid_extension(mask(t) | 1 << b, union))
            bound, degrees = point_capacity(candidates, h)
            old = expected[part][key]
            insist(bound == old['upper_bound'] and degrees == old['pair_union_degrees'] and
                   len(candidates) == old['anchor_candidates'], 'adjacent capacity entry differs')
            insist(bound <= 11, 'adjacent anchor bound fails')
            # Complete optimization of this small packing graph strengthens the source.
            graph = compatibility(candidates)
            optimization_states = 0
            for maximum in range(bound, -1, -1):
                optima, count = clique_census(graph, maximum)
                optimization_states += count
                if optima:
                    break
            witness = union + tuple(candidates[i] | 1 << b for i in optima[0])
            packing(witness)
            saturated_row(witness, u, {v: 3, 16: 2})
            saturated_row(witness, v, {u: 3, b: 2})
            insist(sum(w >> b & 1 for w in witness) == 8 + maximum, 'false sharp anchor witness')
            got[key] = {'candidate_quadruples': len(candidates), 'pair_degrees': degrees,
                        'source_extra_bound': bound, 'maximum_extra': maximum,
                        'sharp_replication_bound': 8 + maximum,
                        'number_of_optimal_extensions': len(optima),
                        'optimization_states': optimization_states, 'witness': words_json(witness)}
        insist(set(got) == set(expected[part]), 'adjacent star list differs')
        results.append({'partition': [list(t) for t in part], 'stars': len(got), 'columns': len(columns),
                        'clique_states': states, 'anchor_results': [{'nonorigin_quads': [list(q) for q in key], **item}
                                                                   for key, item in sorted(got.items())]})
    insist({tuple(tuple(t) for t in r['partition']) for r in results} == set(expected), 'adjacent partition list differs')
    return {'manifest_sha256': source_sha, 'all_partitions': len(all_parts), 'compatible_partitions': len(results),
            'stars': sum(r['stars'] for r in results), 'clique_states': nodes_total, 'cases': results}


def controls():
    graphs, calls = 0, 0
    for n in range(6):
        edges = tuple(combinations(range(n), 2))
        for code in range(1 << len(edges)):
            graph = [0] * n
            for k, (i, j) in enumerate(edges):
                if code >> k & 1:
                    graph[i] |= 1 << j
                    graph[j] |= 1 << i
            for size in range(n + 1):
                brute = [q for q in combinations(range(n), size)
                         if all(graph[i] >> j & 1 for i, j in combinations(q, 2))]
                actual, _ = clique_census(graph, size)
                insist(actual == brute, 'small clique census')
                calls += 1
            graphs += 1
    lines = plane()
    answers, _ = clique_census(compatibility(lines), 20)
    insist(answers == [tuple(range(20))], 'positive plane clique fixture')
    root = first_star(16)
    rejected = 0
    for operation in [lambda: packing(root[:-1] + (root[0],)),
                      lambda: packing(root[:-1] + (mask((0, 1, 2, 4, 17)),)),
                      lambda: clique_census([1], 1),
                      lambda: clique_census([2, 0], 1),
                      lambda: clique_census([], 0, cap=0),
                      lambda: clique_census([], 0, seconds=-1)]:
        try:
            operation()
        except (ValueError, RuntimeError):
            rejected += 1
    insist(rejected == 6, 'semantic controls accepted')
    # Check the small model in the ordinary uniqueness proof, independently of source.
    perms = list(permutations(range(4)))
    edges = [(i, j) for i, j in combinations(range(24), 2)
             if sum(x != y for x, y in zip(perms[i], perms[j])) == 2]
    visited = {0}
    while True:
        following = visited | {j if i in visited else i for i, j in edges if i in visited or j in visited}
        if following == visited:
            break
        visited = following
    even = [p for p in perms if sum(p[i] > p[j] for i, j in combinations(range(4), 2)) % 2 == 0]
    model = {mask(4 * x + p[x] for x in range(4)) for p in even}
    model |= {mask(4 * x + y for x in range(4)) for y in range(4)}
    model |= {mask(4 * x + y for y in range(4)) for x in range(4)}
    insist(len(edges) == 72 and len(visited) == 24 and model == set(lines), 'affine uniqueness model')
    # Every nonempty proper origin split has a directly checked inverse merge.
    through = [line for line in lines if line & 1]
    for selection in range(1, 31):
        split = [line ^ 1 | 1 << 16 if line in through and selection >> through.index(line) & 1
                 else line for line in lines]
        count = Counter(p for line in split for p in pairs(line))
        insist(len(split) == len(set(split)) == 20 and set(count.values()) == {1}, 'bad split pair packing')
        merged = {line ^ 1 << 16 | 1 if line >> 16 & 1 else line for line in split}
        insist(merged == set(lines), 'bad inverse merge')
    # All 100 choices in the ordinary adjacent deficit-two contradiction.
    count = 0
    universe = set(range(5))
    for part in combinations(range(5), 2):
        for other in combinations(range(5), 2):
            insist(set(part) & set(other) or len((universe - set(part)) & set(other)) == 2,
                   'deficit-two conflict failed')
            count += 1
    return {'small_graphs': graphs, 'all_target_clique_checks': calls,
            'negative_controls': rejected, 'positive_affine_fixture': True,
            'ordinary_weight_two_checks': count, 'affine_uniqueness_graph': [24, 72],
            'inverse_merge_splits': 30}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=Path, default=Path(__file__).resolve().parents[1] / 'constant_weight_18_6_5_equality_structure')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--generate', action='store_true', help='Explicitly regenerate reviewer expected.json')
    args = parser.parse_args()
    result = {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer', 'status': 'COMPLETE',
              'shared': shared_audit(args.target / 'two_isolates_expected.json'),
              'adjacent': adjacent_audit(args.target / 'adjacent_low_expected.json'), 'controls': controls()}
    data = encoded(result)
    expected_path = Path(__file__).resolve().parent / 'expected.json'
    if args.generate:
        expected_path.write_bytes(data)
    else:
        insist(data == expected_path.read_bytes(), 'reviewer summary differs')
    if args.output:
        args.output.write_bytes(data)
    print(json.dumps({'status': 'COMPLETE', 'shared_stars': [r['stars'] for r in result['shared']['cases']],
                      'shared_clique_states': result['shared']['clique_states'],
                      'shared_leave_cases': result['shared']['leave_cases'],
                      'adjacent_stars': result['adjacent']['stars'],
                      'adjacent_clique_states': result['adjacent']['clique_states'],
                      'result_sha256': sha256(data).hexdigest()}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
