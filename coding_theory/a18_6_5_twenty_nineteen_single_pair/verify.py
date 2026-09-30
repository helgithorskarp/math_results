#!/usr/bin/env python3
"""No-import set/degree-sequence/Algorithm-X checker of the full replay.

This is a separate algorithm by the same researcher, not a peer review.
"""
import argparse
import hashlib
import itertools as it
import json
import resource
import time
from collections import Counter
from contextlib import nullcontext
from pathlib import Path

MULT = ((0, 0, 0, 0), (0, 1, 2, 3), (0, 2, 3, 1), (0, 3, 1, 2))
T = frozenset([1, 2, 3])
L = frozenset([0, 1, 2, 3])
PAIR_LIST = list(it.combinations(range(16), 2))
PAIR_INDEX = {e: j for j, e in enumerate(PAIR_LIST)}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decode(mask):
    require(type(mask) is int and 0 <= mask < (1 << 16), 'malformed word mask')
    return frozenset(p for p in range(16) if mask & (1 << p))


def encode(block):
    return sum(1 << p for p in block)


def edge_encode(edges):
    return sum(1 << PAIR_INDEX[e] for e in edges)


def field_plane():
    plane = frozenset([frozenset(4*x+y for y in range(4)) for x in range(4)] +
                      [frozenset(4*x+(MULT[m][x]^b) for x in range(4))
                       for m in range(4) for b in range(4)])
    require(len(plane) == 20 and all(len(b) == 4 for b in plane) and
            all(sum(a in b and c in b for b in plane) == 1 for a, c in PAIR_LIST),
            'invalid field plane')
    return plane


def flag_group(plane):
    functions = [lambda x, y: (x ^ 1, y), lambda x, y: (x ^ 2, y),
                 lambda x, y: (x, y ^ 1), lambda x, y: (x, y ^ 2),
                 lambda x, y: (MULT[2][x], y), lambda x, y: (x, MULT[2][y]),
                 lambda x, y: (y, x), lambda x, y: (x ^ y, y),
                 lambda x, y: (MULT[x][x], MULT[y][y])]
    generators = [tuple(4*f(*divmod(p, 4))[0] + f(*divmod(p, 4))[1]
                        for p in range(16)) for f in functions]
    identity = tuple(range(16))
    found, queue = {identity}, [identity]
    for g in queue:
        for h in generators:
            v = tuple(h[g[p]] for p in range(16))
            if v not in found:
                if len(found) >= 6000:
                    raise RuntimeError('INCOMPLETE group closure')
                require(set(v) == set(range(16)) and
                        frozenset(frozenset(v[p] for p in b) for b in plane) == plane,
                        'invalid plane permutation')
                found.add(v)
                queue.append(v)
    require(len(found) == 5760, 'unexpected permutation closure')
    flag = sorted(g for g in found if g[0] == 0 and frozenset(g[p] for p in L) == L)
    require(len(flag) == 72 and {g[1] for g in flag} == set(T), 'invalid flag action')
    return flag


def degree_graphs(degrees, forbidden):
    """All simple graphs with prescribed degrees, by choosing a vertex's neighbors."""
    answer, nodes = set(), 0

    def visit(d, edges):
        nonlocal nodes
        nodes += 1
        if nodes > 200000:
            raise RuntimeError('INCOMPLETE degree-graph enumeration')
        active = [v for v, r in enumerate(d) if r]
        if not active:
            answer.add(frozenset(edges))
            return
        if sum(d) % 2:
            return
        for v in active:
            if d[v] > sum(w != v and tuple(sorted((v, w))) not in forbidden for w in active):
                return
        v = active[0]
        choices = [w for w in active[1:] if (v, w) not in forbidden]
        for neighbors in it.combinations(choices, d[v]):
            remaining = list(d)
            remaining[v] = 0
            for w in neighbors:
                remaining[w] -= 1
            visit(remaining, edges + tuple((v, w) for w in neighbors))

    visit(list(degrees), ())
    return answer


def orbit_cover(domain, group, action, key):
    todo = set(domain)
    output = []
    while todo:
        first = min(todo, key=key)
        orbit = {action(first, g) for g in group}
        require(orbit <= todo, 'omitted, overlapping, or invalid symmetry orbit')
        todo -= orbit
        output.append((first, len(orbit)))
    require(sum(size for _, size in output) == len(domain), 'incomplete orbit domain')
    return output


def prepare():
    plane = field_plane()
    group = flag_group(plane)
    forbidden = frozenset(it.combinations(range(3), 2))
    templates = [degree_graphs([1, 1, 1, 6, 3, 3, 3], forbidden),
                 degree_graphs([1, 1, 1, 3, 3, 3, 3, 3], forbidden),
                 degree_graphs([4, 1, 1, 3, 3, 3, 3], forbidden)]
    require([len(t) for t in templates] == [1, 605, 28], 'abstract degree graphs mismatch')
    outside = sorted(set(range(16)) - T)
    groups, leaves, support_counts = [], [], []
    for profile in range(3):
        subgroup = [g for g in group if g[1] == 1] if profile == 2 else group
        if profile == 0:
            domain = {(frozenset(s), p) for s in it.combinations(outside, 4) for p in s}
            action = lambda v, g: (frozenset(g[p] for p in v[0]), g[v[1]])
            key = lambda v: (encode(v[0]), v[1])
        else:
            domain = {frozenset(s) for s in it.combinations(outside, 5 if profile == 1 else 4)}
            action = lambda v, g: frozenset(g[p] for p in v)
            key = encode
        supports = orbit_cover(domain, subgroup, action, key)
        support_counts.append(len(supports))
        for support_index, (value, support_size) in enumerate(supports):
            support, doubled = value if profile == 0 else (value, None)
            stabilizer = [g for g in subgroup if frozenset(g[p] for p in support) == support and
                          (doubled is None or g[doubled] == doubled)]
            require(stabilizer, 'empty stabilizer')
            if profile == 0:
                ordering = [doubled] + sorted(support - {doubled})
            else:
                ordering = sorted(support)
            mapping = [1, 2, 3] + ordering
            candidates = {frozenset(tuple(sorted((mapping[a], mapping[b]))) for a, b in graph)
                          for graph in templates[profile]}
            for graph in candidates:
                require(len(graph) == 9 and not (graph & frozenset(it.combinations(T, 2))),
                        'invalid old-pair leave')
            local = orbit_cover(candidates, stabilizer,
                                lambda e, g: frozenset(tuple(sorted((g[a], g[b]))) for a, b in e),
                                edge_encode)
            groups.append([profile, support_index, encode(support), doubled, support_size,
                           len(stabilizer), len(candidates), len(local)])
            for leave, size in local:
                leaves.append([len(leaves), profile, support_index, edge_encode(leave), size])
    require(support_counts == [50, 30, 40] and len(leaves) == 11855, 'coverage count mismatch')
    labelled = sum(r[4]*r[6]*(3 if r[0] == 2 else 1) for r in groups)
    require(labelled == 841555, 'labelled count mismatch')
    return plane, groups, leaves


class AlgorithmX:
    """Sparse set columns, destructive exact-cover selection and undo."""
    def __init__(self, allowed):
        self.allowed = allowed
        self.rows = [tuple(it.combinations(sorted(b), 2)) for b in allowed]

    def run(self, leave, node_cap=200000, time_cap=10.0):
        started = time.monotonic()
        forbidden = set(it.combinations(T, 2)) | set(leave)
        columns = {e: set() for e in PAIR_LIST if e not in forbidden}
        for i, row in enumerate(self.rows):
            if not (set(row) & forbidden):
                for e in row:
                    columns[e].add(i)
        require(len(columns) == 108, 'incorrect exact-cover matrix')
        solutions, nodes = set(), 0

        def select(i):
            removed = []
            for e in self.rows[i]:
                for j in columns[e]:
                    for other in self.rows[j]:
                        if other != e:
                            columns[other].remove(j)
                removed.append(columns.pop(e))
            return removed

        def undo(i, removed):
            for e in reversed(self.rows[i]):
                columns[e] = removed.pop()
                for j in columns[e]:
                    for other in self.rows[j]:
                        if other != e:
                            columns[other].add(j)

        def visit(chosen):
            nonlocal nodes
            nodes += 1
            if nodes > node_cap or (nodes % 256 == 0 and time.monotonic() - started > time_cap):
                raise RuntimeError('INCOMPLETE Algorithm-X node/time guard')
            if not columns:
                require(len(chosen) == 18, 'incorrect solution size')
                solution = tuple(sorted(encode(self.allowed[i]) for i in chosen))
                require(solution not in solutions, 'duplicate Algorithm-X solution')
                solutions.add(solution)
                return
            e = min(columns, key=lambda q: (len(columns[q]), PAIR_INDEX[q]))
            for i in sorted(columns[e]):
                removed = select(i)
                visit(chosen + (i,))
                undo(i, removed)

        visit(())
        return solutions, nodes


def check_case(case, pool, first):
    require(type(case) is list and len(case) == 3, 'malformed case')
    cover, common_masks, colors = case
    require(type(cover) is list and len(cover) == 18 and len(set(cover)) == 18,
            'invalid quadruple list')
    stars = first + [decode(b) | {16} for b in cover]
    require(len(stars) == len(set(stars)) == 38 and
            all(len(a) == 5 for a in stars) and
            all(len(a & b) <= 2 for a, b in it.combinations(stars, 2)), 'invalid star union')
    require([sum(p in s for s in stars) for p in [17, 16]] == [20, 19] and
            sum({16, 17} <= s for s in stars) == 1, 'incorrect degrees')
    common = [b for b in pool if all(len(b & s) <= 2 for s in stars)]
    require([encode(b) for b in common] == common_masks, 'incomplete residual universe')
    require(type(colors) is list and len(colors) == len(common) and
            all(type(c) is int and c >= 0 for c in colors), 'invalid color labels')
    classes = {}
    for b, color in zip(common, colors):
        classes.setdefault(color, []).append(b)
    require(all(len(a & b) >= 3 for blocks in classes.values()
                for a, b in it.combinations(blocks, 2)), 'color class contains compatible words')
    return len(common), 1 + max(colors, default=-1)


def run(args):
    started = time.monotonic()
    plane, groups, leaves = prepare()
    allowed = [frozenset(b) for b in it.combinations(range(16), 4)
               if len(frozenset(b) & T) <= 1 and all(len(frozenset(b) & line) <= 2 for line in plane)]
    first = [b | {17} for b in sorted(plane, key=encode) if b != L] + [T | {16, 17}]
    pool = [frozenset(b) for b in it.combinations(range(16), 5)
            if all(len(frozenset(b) & s) <= 2 for s in first)]
    require(len(allowed) == 714 and len(pool) == 378, 'incorrect universes')
    solver = AlgorithmX(allowed)
    histograms = [Counter() for _ in range(3)]
    stats = [{'leaves': 0, 'realized_leaves': 0, 'star_pairs': 0,
              'max_common_fives': 0, 'max_color_upper': 0} for _ in range(3)]
    digest, nodes = hashlib.sha256(), 0
    with args.replay.open() as replay, (args.native_covers.open() if args.native_covers else nullcontext(None)) as native:
        first_line = replay.readline()
        header = json.loads(first_line)
        require(header == {'groups': groups, 'leaves': leaves, 'plane': sorted(map(encode, plane)),
                           'allowed': list(map(encode, allowed)), 'pool': list(map(encode, pool))},
                'replay does not match regenerated finite domain')
        digest.update(first_line.encode())
        for index, profile, support_index, mask, size in leaves[:args.stop]:
            line = replay.readline()
            require(line, 'truncated replay')
            digest.update(line.encode())
            record = json.loads(line)
            require(set(record) == {'index', 'covers'} and record['index'] == index,
                    'missing, duplicated, or misordered leave')
            leave = {e for j, e in enumerate(PAIR_LIST) if mask & (1 << j)}
            if native is None:
                covers, visited = solver.run(leave)
            else:
                native_line = native.readline()
                require(native_line, 'truncated native cover output')
                native_record = json.loads(native_line)
                require(set(native_record) == {'index', 'covers', 'nodes'} and
                        native_record['index'] == index and type(native_record['nodes']) is int and
                        1 <= native_record['nodes'] <= 200000, 'invalid native record')
                candidates = [tuple(c) for c in native_record['covers']]
                require(len(candidates) == len(set(candidates)), 'duplicate native cover')
                covers, visited = set(candidates), native_record['nodes']
            nodes += visited
            supplied = [tuple(c[0]) for c in record['covers']]
            require(len(supplied) == len(set(supplied)) and set(supplied) == covers,
                    'incomplete or incorrect exact-cover list')
            s = stats[profile]
            s['leaves'] += 1
            s['realized_leaves'] += bool(covers)
            s['star_pairs'] += len(covers)
            for case in record['covers']:
                n, upper = check_case(case, pool, first)
                s['max_common_fives'] = max(s['max_common_fives'], n)
                s['max_color_upper'] = max(s['max_color_upper'], upper)
                histograms[profile][upper] += 1
            if (index + 1) % 100 == 0:
                progress = {'status': 'INCOMPLETE until full replay ends', 'completed_leaves': index + 1,
                            'total_leaves': len(leaves), 'Algorithm_X_nodes': nodes,
                            'seconds': round(time.monotonic() - started, 4)}
                args.progress.write_text(json.dumps(progress, indent=2) + '\n')
                print(json.dumps(progress), flush=True)
        if args.stop < len(leaves):
            print(json.dumps({'status': 'PARTIAL validation only', 'checked_leaves': args.stop,
                              'seconds': round(time.monotonic() - started, 4)}))
            return
        require(not replay.read(), 'unexpected extra replay records')
        require(native is None or not native.read(), 'unexpected extra native cover records')
    expected = json.loads(args.expected.read_text())
    require(expected['status'] == 'COMPLETE' and expected['leaf_orbits'] == len(leaves) and
            expected['replay_sha256'] == digest.hexdigest(), 'summary or replay digest mismatch')
    for actual, source in zip(stats, expected['profiles']):
        require(all(actual[k] == source[k] for k in actual), 'profile summary mismatch')
    require([{str(k): v for k, v in sorted(h.items())} for h in histograms] ==
            expected['color_upper_histograms'], 'color histogram mismatch')
    result = {'agent': 'six-code-3', 'role': 'researcher', 'status': 'COMPLETE independent-algorithm check',
              'peer_review': False, 'leaf_orbits': len(leaves), 'profiles': stats,
              'cover_algorithm': 'C++ linked-column Algorithm X' if args.native_covers else 'Python set Algorithm X',
              'Algorithm_X_nodes': nodes, 'replay_sha256': digest.hexdigest(),
              'max_color_upper': max(s['max_color_upper'] for s in stats),
              'code_size_upper': 38 + max(s['max_color_upper'] for s in stats),
              'seconds': round(time.monotonic() - started, 4),
              'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)


def export_input(path, stop):
    plane, groups, leaves = prepare()
    allowed = [frozenset(b) for b in it.combinations(range(16), 4)
               if len(frozenset(b) & T) <= 1 and all(len(frozenset(b) & line) <= 2 for line in plane)]
    require(len(allowed) == 714, 'incorrect native columns')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as output:
        output.write('120 714 6\n')
        for b in allowed:
            indices = [PAIR_INDEX[e] for e in it.combinations(sorted(b), 2)]
            output.write(' '.join(map(str, [encode(b)] + indices)) + '\n')
        output.write(str(stop) + '\n')
        triple_pairs = {PAIR_INDEX[e] for e in it.combinations(sorted(T), 2)}
        for index, profile, support_index, mask, size in leaves[:stop]:
            blocked = triple_pairs | {j for j in range(120) if mask & (1 << j)}
            require(len(blocked) == 12, 'incorrect native forbidden set')
            output.write(' '.join(map(str, [index, 12] + sorted(blocked))) + '\n')
    print(json.dumps({'status': 'independently regenerated native input', 'leaves': stop}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--replay', type=Path)
    p.add_argument('--expected', type=Path)
    p.add_argument('--progress', type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('--native-covers', type=Path)
    p.add_argument('--export-cover-input', type=Path)
    p.add_argument('--stop', type=int, default=11855)
    a = p.parse_args()
    require(0 <= a.stop <= 11855, 'invalid replay coverage bound')
    if a.export_cover_input:
        export_input(a.export_cover_input, a.stop)
    else:
        require(all([a.replay, a.expected, a.progress, a.output]), 'missing replay verification arguments')
        run(a)
