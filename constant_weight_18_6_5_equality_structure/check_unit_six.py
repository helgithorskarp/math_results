"""Exact six-edge all-unit carriers and compact nontrivial rejection proofs."""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import time

from check_unit_eight import rejection_tree

QUAD_PAIRS = {q: frozenset(combinations(q, 2)) for q in combinations(range(17), 4)}
ONE_HIGH = tuple(q for q in QUAD_PAIRS if q[0] < 5 <= q[1])

HERE = Path(__file__).resolve().parent
HIGH = tuple(range(5))
LOW = tuple(range(5, 17))
SPECIAL = tuple(range(5, 13))
MATCHED = tuple(range(13, 17))
ALL_PAIRS = tuple(combinations(range(17), 2))
CORES = {
    'triangle_edge': ((0, 1), (0, 2), (1, 2), (3, 4)),
    'triangle_pendant': ((0, 1), (0, 2), (1, 2), (2, 3)),
    'cycle_four': ((0, 1), (0, 3), (1, 2), (2, 3)),
    'path_five': ((0, 1), (1, 2), (2, 3), (3, 4)),
    'fork_tree': ((0, 1), (0, 2), (0, 3), (3, 4))}
GROUP_ORDERS = {'triangle_edge': 768, 'triangle_pendant': 384,
                'cycle_four': 1024, 'path_five': 128, 'fork_tree': 192}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pairs(q):
    return QUAD_PAIRS[q]


def digest(value):
    return sha256((json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()).hexdigest()


def moved(q, p):
    return tuple(sorted(p[x] for x in q))


def action(prefix, p):
    return tuple(sorted(moved(q, p) for q in prefix))


def model(name):
    covered = CORES[name]
    attached, next_point = {}, 5
    for h in HIGH:
        d = sum(h in e for e in covered)
        attached[h] = tuple(range(next_point, next_point + d))
        next_point += d
    require(next_point == 13, 'eight attached low points')
    leave = frozenset((set(combinations(HIGH, 2)) - set(covered)) |
                      {(h, x) for h in HIGH for x in attached[h]} |
                      {(13, 14), (15, 16)})
    require(len(leave) == 16 and [sum(x in e for e in leave) for x in range(17)] == [4]*5+[1]*12,
            'wrong leave degrees')
    return {'name': name, 'covered': covered, 'attached': attached, 'leave': leave}


def legal(m, prefix):
    multiplicities = Counter(e for q in prefix for e in pairs(q))
    return not set(multiplicities) & m['leave'] and set(multiplicities.values()) == {1}


def actual_group(m):
    maps = []
    for h in permutations(HIGH):
        if {moved(e, h) for e in m['covered']} != set(m['covered']):
            continue
        for attached_maps in product(*(tuple(permutations(m['attached'][h[i]])) for i in HIGH)):
            for order in permutations(range(2)):
                for flips in product(range(2), repeat=2):
                    p = list(h) + list(LOW)
                    for i in HIGH:
                        for x, y in zip(m['attached'][i], attached_maps[i]):
                            p[x] = y
                    for i in range(2):
                        for j in range(2):
                            p[13 + 2*i + j] = 13 + 2*order[i] + (j ^ flips[i])
                    p = tuple(p)
                    require(len(set(p)) == 17 and {moved(e, p) for e in m['leave']} == set(m['leave']),
                            'map is not an actual leave permutation')
                    maps.append(p)
    require(len(maps) == len(set(maps)) == GROUP_ORDERS[m['name']], 'wrong group size')
    return tuple(sorted(maps))


def quotient(raw, group):
    unseen, result = set(raw), []
    for root in sorted(raw):
        if root not in unseen:
            continue
        orbit = {action(root, p) for p in group}
        require(orbit <= raw and orbit <= unseen, 'orbit escaped or overlapped')
        stabilizer = tuple(p for p in group if action(root, p) == root)
        require(len(orbit)*len(stabilizer) == len(group), 'orbit-stabilizer failure')
        unseen -= orbit
        result.append((root, len(orbit), stabilizer))
    require(sum(n for _, n, _ in result) == len(raw), 'incomplete quotient')
    return result


def multiblocks(m, branch):
    if branch == 'double':
        options = [tuple(e+t for t in combinations(LOW, 2) if legal(m, (e+t,)))
                   for e in m['covered']]
        raw = set()
        def extend(selected, used):
            if len(selected) == len(options):
                raw.add(selected)
                return
            for q in options[len(selected)]:
                if not pairs(q) & used:
                    extend(selected+(q,), used | pairs(q))
        extend((), frozenset())
        return frozenset(raw), [len(x) for x in options]
    triangle = (0, 1, 2)
    require(set(combinations(triangle, 2)) <= set(m['covered']), 'no triple-high branch')
    edge, = set(m['covered']) - set(combinations(triangle, 2))
    options = [tuple(triangle+(x,) for x in LOW if legal(m, (triangle+(x,),))),
               tuple(edge+t for t in combinations(LOW, 2) if legal(m, (edge+t,)))]
    raw = frozenset(tuple(sorted(prefix)) for prefix in product(*options) if legal(m, prefix))
    return raw, [len(x) for x in options]


class Incomplete(Exception):
    pass


def zero_frames(m, multi, number, node_limit=200000, seconds=10):
    counts = Counter(SPECIAL)
    for q in multi:
        j = sum(x in HIGH for x in q)
        for x in q:
            if x in LOW:
                counts[x] += j-1
    require(sum(counts.values()) == 4*number, 'wrong zero incidence total')
    forbidden = m['leave'] | frozenset().union(*(pairs(q) for q in multi))
    candidates = tuple(q for q in combinations(sorted(counts), 4) if not pairs(q) & forbidden)
    edges = tuple(pairs(q) for q in candidates)
    at_point = {x: tuple(i for i, q in enumerate(candidates) if x in q) for x in counts}
    found, nodes, start = set(), 0, time.monotonic()

    def visit(left, used, selected):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit or (nodes % 128 == 0 and time.monotonic()-start > seconds):
            raise Incomplete('INCOMPLETE zero-frame guard reached')
        if len(selected) == number-1:
            if len(left) != 4 or set(left.values()) != {1}:
                return
            last = tuple(sorted(left))
            if not pairs(last) & (forbidden | used):
                found.add(tuple(sorted(tuple(candidates[i] for i in selected) + (last,))))
            return
        require(bool(left), 'empty incidence multiset too early')
        _, pivot = min((sum(not edges[i] & used and all(left.get(x, 0) for x in candidates[i])
                           for i in at_point[v]), v) for v in left)
        for i in at_point[pivot]:
            if edges[i] & used or any(not left.get(x, 0) for x in candidates[i]):
                continue
            remaining = Counter(left)
            for x in candidates[i]:
                remaining[x] -= 1
                if not remaining[x]:
                    del remaining[x]
            visit(remaining, used | edges[i], selected+(i,))

    visit(counts, frozenset(), ())
    for z in found:
        require(legal(m, multi+z) and Counter(x for q in z for x in q) == counts,
                'invalid zero-frame carrier')
    return frozenset(found), nodes


def instance(m, prefix, branch):
    require(legal(m, prefix), 'invalid prefix')
    used = frozenset().union(*(pairs(q) for q in prefix))
    rows = tuple(e for e in ALL_PAIRS if e not in m['leave'] | used)
    remaining = set(rows)
    columns = tuple(q for q in ONE_HIGH if pairs(q) <= remaining)
    require(len(rows) == (90 if branch == 'triple' else 72), 'wrong residual pair count')
    return rows, columns


def check_positive(m, prefix, added):
    quads = tuple(sorted(prefix+tuple(added)))
    covered = Counter(e for q in quads for e in pairs(q))
    require(len(quads) == len(set(quads)) == 20 and set(covered) == set(ALL_PAIRS)-m['leave']
            and set(covered.values()) == {1}, 'invalid positive twenty-block packing')
    require([sum(x in q for q in quads) for x in range(17)] == [4]*5+[5]*12, 'invalid replication pattern')
    return quads


BRANCHES = (('triangle_edge', 'triple'), ('triangle_edge', 'double'),
            ('triangle_pendant', 'triple'), ('triangle_pendant', 'double'),
            ('cycle_four', 'double'), ('fork_tree', 'double'), ('path_five', 'double'))


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode('ascii')


def high_graph_census():
    maps = tuple(permutations(HIGH))
    def canonical(edges):
        edges = tuple(edges)
        return min(tuple(sorted(moved(e, p) for e in edges)) for p in maps)
    named = {canonical(edges): name for name, edges in CORES.items()}
    require(len(named) == 5, 'named covered high graphs overlap')
    counts = Counter()
    for edges in combinations(tuple(combinations(HIGH, 2)), 4):
        leave = set(combinations(HIGH, 2)) - set(edges)
        forbidden = any(set(combinations(q, 2)) <= leave for q in combinations(HIGH, 4))
        key = canonical(edges)
        require(forbidden or key in named, 'unclassified four-edge high graph')
        require(not forbidden or key not in named, 'named high leave contains K4')
        counts['excluded_K4' if forbidden else named[key]] += 1
    require(counts == Counter(triangle_edge=10, triangle_pendant=60, cycle_four=15,
                              fork_tree=60, path_five=60, excluded_K4=5),
            'wrong complete labeled high graph census')
    return dict(counts)


def walk(name, branch, summary):
    """Stream residual instances; hold only one tail fiber in memory."""
    m, group = model(name), actual_group(model(name))
    raw, options = multiblocks(m, branch)
    representatives = quotient(raw, group)
    summary.update(model=name, branch=branch, group_order=len(group), group_sha256=digest(group),
                   raw_multi_prefixes=len(raw), raw_multi_sha256=digest(sorted(raw)),
                   multi_options=options, multi_orbits=len(representatives))
    fibers, weight = [], 0
    for multi, n, stabilizer in representatives:
        zero, _ = zero_frames(m, multi, 3 if branch == 'triple' else 4)
        zrecords = quotient(zero, stabilizer)
        weight += n*len(zero)
        fibers.append([multi, n, len(stabilizer), len(zero), digest(sorted(zero)), len(zrecords)])
        for z, zn, zs in zrecords:
            prefix = multi+z
            rows, columns = instance(m, prefix, branch)
            yield prefix, n*zn, len(zs), rows, columns
    summary.update(raw_prefixes=weight, zero_fibers_sha256=digest(fibers))


def build(checkpoint_dir=None):
    census = high_graph_census()
    stream = sha256()
    trees, summaries, node_counts = {}, [], []
    case_index = 0
    for name, branch in BRANCHES:
        summary = {}
        begin, holes, explicit, column_sizes, branch_nodes = case_index, 0, 0, [], []
        for prefix, orbit, stabilizer, rows, columns in walk(name, branch, summary):
            stream.update(encoded([prefix, rows, columns]))
            supported = frozenset().union(*(QUAD_PAIRS[q] for q in columns))
            if set(rows) - supported:
                # A missing row is itself an exact rejection proof; no corpus entry is needed.
                count = 1
                holes += 1
            else:
                tree, count = rejection_tree(rows, columns)
                require(count > 1, 'nontrivial residual unexpectedly has a one-node proof')
                trees[str(case_index)] = tree
                explicit += 1
            branch_nodes.append(count)
            node_counts.append(count)
            column_sizes.append(len(columns))
            case_index += 1
        summary.update(cases=case_index-begin, rows=90 if branch == 'triple' else 72,
                       column_range=[min(column_sizes), max(column_sizes)],
                       immediate_pair_holes=holes, explicit_trees=explicit,
                       nodes=sum(branch_nodes), maximum_nodes_per_case=max(branch_nodes))
        summaries.append(summary)
        if checkpoint_dir is not None:
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            partial = {'schema': 'all-unit-six-partial-v1', 'status': 'INCOMPLETE_OVERALL',
                       'completed_branches': summaries, 'completed_cases': case_index,
                       'input_stream_of_completed_branches_sha256': stream.hexdigest(),
                       'completed_nodes_per_case_sha256': digest(node_counts),
                       'nontrivial_trees_for_completed_branches': trees}
            (checkpoint_dir/'six-partial-proof.json').write_bytes(encoded(partial))
    certificate = {'schema': 'all-unit-six-cores-v1', 'high_graph_census': census,
                   'carrier_summary_sha256': digest(summaries),
                   'input_stream_sha256': stream.hexdigest(), 'nontrivial_trees': trees}
    report = {'agent': 'six-code-1', 'role': 'researcher', 'status': 'COMPLETE_EXACT_NO_COVERS',
              'branches': summaries, 'cases': case_index,
              'raw_prefixes': sum(s['raw_prefixes'] for s in summaries),
              'immediate_pair_holes': sum(s['immediate_pair_holes'] for s in summaries),
              'explicit_trees': len(trees), 'nodes': sum(node_counts),
              'maximum_nodes_per_case': max(node_counts), 'nodes_per_case_sha256': digest(node_counts),
              'input_stream_sha256': stream.hexdigest(),
              'carrier_summary_sha256': digest(summaries),
              'certificate_bytes': len(encoded(certificate)),
              'certificate_sha256': sha256(encoded(certificate)).hexdigest(),
              'global_72_word_exclusion': False, 'independent_peer_review': False,
              'ordinary_bridges_formalized': False}
    return certificate, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-certificate', action='store_true')
    parser.add_argument('--checkpoint-dir', type=Path)
    args = parser.parse_args()
    certificate, report = build(args.checkpoint_dir)
    if args.write_certificate:
        (HERE/'unit_six_certificate.json').write_bytes(encoded(certificate))
        (HERE/'unit_six_expected.json').write_bytes(encoded(report))
    else:
        require((HERE/'unit_six_certificate.json').read_bytes() == encoded(certificate),
                'certificate differs entry by entry')
        require(json.loads((HERE/'unit_six_expected.json').read_text()) == report, 'expected report differs')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
