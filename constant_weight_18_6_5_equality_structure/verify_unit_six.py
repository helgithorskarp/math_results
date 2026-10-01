"""Rebuild literal six-edge leave carriers and replay compact rejection proofs."""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import sys
import time

HERE = Path(__file__).resolve().parent
HIGH = frozenset(range(5))
LOW = tuple(range(5, 17))
ALL_PAIRS = frozenset(combinations(range(17), 2))
ALL_QUADS = tuple(combinations(range(17), 4))
QUAD_PAIRS = {q: frozenset(combinations(q, 2)) for q in ALL_QUADS}
HIGH_COUNT = {q: len(HIGH & set(q)) for q in ALL_QUADS}
ONE_HIGH = tuple(q for q in ALL_QUADS if HIGH_COUNT[q] == 1)
NAMES = ('triangle_edge', 'triangle_pendant', 'cycle_four', 'fork_tree', 'path_five')
LEAVES = {
    'triangle_edge': frozenset({(0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4),
        (0, 5), (0, 6), (1, 7), (1, 8), (2, 9), (2, 10), (3, 11), (4, 12),
        (13, 14), (15, 16)}),
    'triangle_pendant': frozenset({(0, 3), (0, 4), (1, 3), (1, 4), (2, 4), (3, 4),
        (0, 5), (0, 6), (1, 7), (1, 8), (2, 9), (2, 10), (2, 11), (3, 12),
        (13, 14), (15, 16)}),
    'cycle_four': frozenset({(0, 2), (0, 4), (1, 3), (1, 4), (2, 4), (3, 4),
        (0, 5), (0, 6), (1, 7), (1, 8), (2, 9), (2, 10), (3, 11), (3, 12),
        (13, 14), (15, 16)}),
    'fork_tree': frozenset({(0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4),
        (0, 5), (0, 6), (0, 7), (1, 8), (2, 9), (3, 10), (3, 11), (4, 12),
        (13, 14), (15, 16)}),
    'path_five': frozenset({(0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (2, 4),
        (0, 5), (1, 6), (1, 7), (2, 8), (2, 9), (3, 10), (3, 11), (4, 12),
        (13, 14), (15, 16)})}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return sha256((json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()).hexdigest()


def moved(q, p):
    return tuple(sorted(p[x] for x in q))


def action(prefix, p):
    return tuple(sorted(moved(q, p) for q in prefix))


def direct_group(leave):
    neighbors = {x: h for h, x in leave if h < 5 <= x}
    special = tuple(sorted(neighbors))
    matched = tuple(x for x in LOW if x not in neighbors)
    h_edges = {e for e in leave if e[1] < 5}
    m_edges = {e for e in leave if e[0] >= 5}
    require(len(special) == 8 and len(matched) == 4, 'wrong literal leave pools')
    low_maps = tuple(b for b in permutations(matched)
                     if {tuple(sorted((b[matched.index(x)], b[matched.index(y)])))
                         for x, y in m_edges} == m_edges)
    require(len(low_maps) == 8, 'wrong directly filtered matching group')
    maps = []
    for h in permutations(range(5)):
        if {moved(e, h) for e in h_edges} != h_edges:
            continue
        for a in permutations(special):
            if any(h[neighbors[x]] != neighbors[y] for x, y in zip(special, a)):
                continue
            for b in low_maps:
                p = list(h) + list(LOW)
                for x, y in zip(special, a):
                    p[x] = y
                for x, y in zip(matched, b):
                    p[x] = y
                p = tuple(p)
                require(len(set(p)) == 17 and {moved(e, p) for e in leave} == set(leave),
                        'direct map changes literal leave')
                maps.append(p)
    require(len(maps) == len(set(maps)), 'duplicate direct group map')
    return tuple(sorted(maps))


def direct_multi(leave, branch):
    covered = tuple(e for e in combinations(range(5), 2) if e not in leave)
    doubles = tuple(q for q in ALL_QUADS if HIGH_COUNT[q] == 2 and not QUAD_PAIRS[q] & leave)
    if branch == 'double':
        options = [tuple(q for q in doubles if tuple(x for x in q if x in HIGH) == e)
                   for e in covered]
        raw = set()
        # Literal pair sets, constructed from the full 2380-quad census.
        for a in options[0]:
            for b in options[1]:
                if QUAD_PAIRS[a] & QUAD_PAIRS[b]:
                    continue
                first = QUAD_PAIRS[a] | QUAD_PAIRS[b]
                for c in options[2]:
                    if QUAD_PAIRS[c] & first:
                        continue
                    used = first | QUAD_PAIRS[c]
                    for d in options[3]:
                        if not QUAD_PAIRS[d] & used:
                            raw.add((a, b, c, d))
        return frozenset(raw), [len(o) for o in options]
    triples = tuple(q for q in ALL_QUADS if HIGH_COUNT[q] == 3 and not QUAD_PAIRS[q] & leave)
    raw = set()
    used_doubles = set()
    for a in triples:
        h_pairs = frozenset(e for e in QUAD_PAIRS[a] if e[1] < 5)
        rest = set(covered) - h_pairs
        for b in doubles:
            if {e for e in QUAD_PAIRS[b] if e[1] < 5} != rest:
                continue
            used_doubles.add(b)
            if not QUAD_PAIRS[a] & QUAD_PAIRS[b]:
                raw.add(tuple(sorted((a, b))))
    return frozenset(raw), [len(triples), len(used_doubles)]


def direct_quotient(raw, group):
    remaining, results = set(raw), []
    for root in sorted(raw):
        if root not in remaining:
            continue
        orbit = {action(root, p) for p in group}
        require(orbit <= raw and orbit <= remaining, 'direct orbit escape or overlap')
        stabilizer = tuple(p for p in group if action(root, p) == root)
        require(len(orbit)*len(stabilizer) == len(group), 'direct orbit-stabilizer error')
        remaining -= orbit
        results.append((root, len(orbit), stabilizer))
    require(not remaining and sum(n for _, n, _ in results) == len(raw), 'direct quotient incomplete')
    return results


class Incomplete(Exception):
    pass


def direct_zeros(leave, multi, number, node_limit=200000, seconds=10):
    """Choose sorted zero blocks; derive the last from the remaining incidences."""
    special = {x for h, x in leave if h < 5 <= x}
    counts = tuple(int(x in special)+sum(HIGH_COUNT[q]-1 for q in multi if x in q) for x in LOW)
    require(sum(counts) == 4*number, 'direct incidence total error')
    forbidden = leave | frozenset(e for q in multi for e in QUAD_PAIRS[q])
    frames, nodes, scans = set(), 0, 0
    began = time.monotonic()

    def visit(left, selected, used):
        nonlocal nodes, scans
        nodes += 1
        if nodes > node_limit or (nodes % 128 == 0 and time.monotonic()-began > seconds):
            raise Incomplete('INCOMPLETE direct sorted-zero guard')
        remaining_blocks = number-len(selected)
        if any(n > remaining_blocks for n in left):
            return
        if remaining_blocks == 1:
            last = tuple(x+5 for x, n in enumerate(left) if n)
            if len(last) == 4 and all(n in (0, 1) for n in left) and last > selected[-1] \
                    and not QUAD_PAIRS[last] & (forbidden | used):
                frames.add(selected+(last,))
            return
        forced = frozenset(i for i, n in enumerate(left) if n == remaining_blocks)
        positive = tuple(x+5 for x, n in enumerate(left) if n)
        for q in combinations(positive, 4):
            scans += 1
            if scans % 128 == 0 and time.monotonic()-began > seconds:
                raise Incomplete('INCOMPLETE direct sorted-zero time guard')
            points = tuple(x-5 for x in q)
            if (selected and q <= selected[-1]) or not forced <= set(points) \
                    or QUAD_PAIRS[q] & (forbidden | used):
                continue
            after = list(left)
            for x in points:
                after[x] -= 1
            visit(tuple(after), selected+(q,), used | QUAD_PAIRS[q])

    visit(counts, (), frozenset())
    for frame in frames:
        require(Counter(x for q in frame for x in q) == Counter({x+5:n for x, n in enumerate(counts) if n}),
                'direct zero-frame multiset error')
    return frozenset(frames), nodes


def direct_case(leave, prefix, branch):
    covered = Counter(e for q in prefix for e in QUAD_PAIRS[q])
    require(set(covered.values()) == {1} and not set(covered) & leave, 'direct prefix pair repetition')
    rows = tuple(sorted(ALL_PAIRS - leave - set(covered)))
    left = frozenset(rows)
    columns = tuple(q for q in ONE_HIGH if QUAD_PAIRS[q] <= left)
    require(len(rows) == (90 if branch == 'triple' else 72), 'direct residual size error')
    return rows, columns


def literal_cover(rows, columns, node_limit=200000, seconds=10):
    """A separate set-based search, retaining its literal rejection tree."""
    edges = tuple(QUAD_PAIRS[q] for q in columns)
    at_pair = {r: tuple(i for i, e in enumerate(edges) if r in e) for r in rows}
    nodes, began = 0, time.monotonic()

    def visit(left):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit or (nodes % 128 == 0 and time.monotonic()-began > seconds):
            raise Incomplete('INCOMPLETE literal exact-cover guard')
        if not left:
            return (), None
        compatible = {r: tuple(i for i in at_pair[r] if edges[i] <= left) for r in left}
        pivot = min(left, key=lambda r: (len(compatible[r]), r))
        children = []
        for i in compatible[pivot]:
            witness, subtree = visit(left - edges[i])
            if witness is not None:
                return (columns[i],)+witness, None
            children.append([i, subtree])
        return None, [rows.index(pivot), children]

    witness, tree = visit(frozenset(rows))
    return witness, tree, nodes


BRANCHES = (('triangle_edge', 'triple'), ('triangle_edge', 'double'),
            ('triangle_pendant', 'triple'), ('triangle_pendant', 'double'),
            ('cycle_four', 'double'), ('fork_tree', 'double'), ('path_five', 'double'))


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode('ascii')


def direct_graph_census():
    maps = tuple(permutations(range(5)))
    def canonical(edges):
        edges = tuple(edges)
        return min(tuple(sorted(moved(e, p) for e in edges)) for p in maps)
    named = {canonical(e for e in leave if e[1] < 5): name for name, leave in LEAVES.items()}
    require(len(named) == 5, 'literal high leave classes overlap')
    counts = Counter()
    for leave in combinations(tuple(combinations(range(5), 2)), 6):
        forbidden = any(set(combinations(q, 2)) <= set(leave) for q in combinations(range(5), 4))
        key = canonical(leave)
        require(forbidden or key in named, 'unclassified six-edge high leave')
        require(not forbidden or key not in named, 'named high leave contains K4')
        counts['excluded_K4' if forbidden else named[key]] += 1
    require(sum(counts.values()) == 210, 'literal high leave census incomplete')
    return dict(counts)


def direct_walk(name, branch, summary, compare_primary=False):
    leave = LEAVES[name]
    require(len(leave) == 16 and [sum(x in e for e in leave) for x in range(17)] == [4]*5+[1]*12,
            'wrong literal leave degree sequence')
    group = direct_group(leave)
    raw, options = direct_multi(leave, branch)
    representatives = direct_quotient(raw, group)
    primary = None
    if compare_primary:
        import check_unit_six as primary
        m = primary.model(name)
        require(leave == m['leave'] and group == primary.actual_group(m), 'entry-level model/map mismatch')
        p_raw, p_options = primary.multiblocks(m, branch)
        require(raw == p_raw and options == p_options, 'entry-level raw multi mismatch')
        require(representatives == primary.quotient(p_raw, group), 'entry-level multi quotient mismatch')
    summary.update(model=name, branch=branch, group_order=len(group), group_sha256=digest(group),
                   raw_multi_prefixes=len(raw), raw_multi_sha256=digest(sorted(raw)),
                   multi_options=options, multi_orbits=len(representatives))
    fibers, weight = [], 0
    for multi, n, stabilizer in representatives:
        zero, _ = direct_zeros(leave, multi, 3 if branch == 'triple' else 4)
        zrecords = direct_quotient(zero, stabilizer)
        if primary:
            p_zero, _ = primary.zero_frames(m, multi, 3 if branch == 'triple' else 4)
            require(zero == p_zero, 'entry-level raw zero fiber mismatch')
            require(zrecords == primary.quotient(p_zero, stabilizer), 'entry-level zero quotient mismatch')
        weight += n*len(zero)
        fibers.append([multi, n, len(stabilizer), len(zero), digest(sorted(zero)), len(zrecords)])
        for z, zn, zs in zrecords:
            prefix = multi+z
            rows, columns = direct_case(leave, prefix, branch)
            if primary:
                require((rows, columns) == primary.instance(m, prefix, branch), 'entry-level row/column mismatch')
            yield prefix, n*zn, len(zs), rows, columns
    summary.update(raw_prefixes=weight, zero_fibers_sha256=digest(fibers))


def replay_tree(tree, rows, columns):
    edges = tuple(QUAD_PAIRS[q] for q in columns)
    nodes = 0
    def visit(node, left):
        nonlocal nodes
        nodes += 1
        require(bool(left), 'rejection proof reached a positive cover')
        require(type(node) is list and len(node) == 2, 'malformed rejection node')
        pivot, children = node
        require(type(pivot) is int and 0 <= pivot < len(rows) and rows[pivot] in left,
                'pivot is not an uncovered pair')
        require(type(children) is list and all(type(c) is list and len(c) == 2 and type(c[0]) is int
                                              for c in children), 'malformed rejection branches')
        compatible = [i for i, e in enumerate(edges) if rows[pivot] in e and e <= left]
        require([c[0] for c in children] == compatible, 'missing, extra or reordered compatible branch')
        for i, child in children:
            visit(child, left - edges[i])
    visit(tree, frozenset(rows))
    return nodes


def consume_case(case_index, tree_dictionary, rows, columns):
    key = str(case_index)
    supported = frozenset().union(*(QUAD_PAIRS[q] for q in columns))
    if frozenset(rows) - supported:
        require(key not in tree_dictionary, 'extra tree supplied for an immediate pair hole')
        return 1, True
    require(key in tree_dictionary, 'missing nontrivial proof tree')
    return replay_tree(tree_dictionary[key], rows, columns), False


def verify(certificate, compare_primary=False, checkpoint_dir=None):
    require(certificate.get('schema') == 'all-unit-six-cores-v1', 'wrong certificate schema')
    census = direct_graph_census()
    require(certificate.get('high_graph_census') == census, 'high graph coverage mismatch')
    trees = certificate.get('nontrivial_trees')
    require(type(trees) is dict and all(type(k) is str and k.isdecimal() and str(int(k)) == k for k in trees),
            'malformed sparse proof table')
    stream, summaries, node_counts, case_index, used = sha256(), [], [], 0, set()
    began = time.monotonic()
    for name, branch in BRANCHES:
        summary = {}
        begin, holes, explicit, column_sizes, branch_nodes = case_index, 0, 0, [], []
        for prefix, orbit, stabilizer, rows, columns in direct_walk(name, branch, summary, compare_primary):
            stream.update(encoded([prefix, rows, columns]))
            count, hole = consume_case(case_index, trees, rows, columns)
            holes += int(hole)
            explicit += int(not hole)
            if not hole:
                used.add(str(case_index))
            node_counts.append(count)
            branch_nodes.append(count)
            column_sizes.append(len(columns))
            case_index += 1
        summary.update(cases=case_index-begin, rows=90 if branch == 'triple' else 72,
                       column_range=[min(column_sizes), max(column_sizes)],
                       immediate_pair_holes=holes, explicit_trees=explicit,
                       nodes=sum(branch_nodes), maximum_nodes_per_case=max(branch_nodes))
        summaries.append(summary)
        if checkpoint_dir is not None:
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            progress = {'agent': 'six-code-1', 'role': 'researcher',
                        'status': 'INCOMPLETE_OVERALL', 'completed_branches': summaries,
                        'cases_checked': case_index, 'proof_trees_checked': len(used),
                        'input_prefix_sha256': stream.hexdigest(),
                        'seconds': round(time.monotonic()-began, 4)}
            (checkpoint_dir/'six-partial-replay.json').write_text(
                json.dumps(progress, indent=2, sort_keys=True)+'\n')
            print(json.dumps({'branch_completed': [name, branch],
                              'cases_checked': case_index,
                              'seconds': progress['seconds']}), file=sys.stderr, flush=True)
    require(used == set(trees), 'extra sparse proof tree')
    require(certificate.get('carrier_summary_sha256') == digest(summaries), 'carrier summary hash mismatch')
    require(certificate.get('input_stream_sha256') == stream.hexdigest(), 'input stream hash mismatch')
    return {'agent': 'six-code-1', 'role': 'researcher', 'status': 'COMPLETE_EXACT_NO_COVERS',
            'branches': summaries, 'cases': case_index,
            'raw_prefixes': sum(s['raw_prefixes'] for s in summaries),
            'immediate_pair_holes': sum(s['immediate_pair_holes'] for s in summaries),
            'explicit_trees': len(trees), 'nodes': sum(node_counts),
            'maximum_nodes_per_case': max(node_counts), 'nodes_per_case_sha256': digest(node_counts),
            'input_stream_sha256': stream.hexdigest(), 'carrier_summary_sha256': digest(summaries),
            'certificate_bytes': len(encoded(certificate)),
            'certificate_sha256': sha256(encoded(certificate)).hexdigest(),
            'global_72_word_exclusion': False, 'independent_peer_review': False,
            'ordinary_bridges_formalized': False}


def controls(certificate):
    from copy import deepcopy
    import check_unit_six as primary
    from check_unit_eight import CoverFound, Incomplete as PrimaryIncomplete
    first = next(direct_walk('triangle_edge', 'triple', {}))
    prefix, _, _, rows, columns = first
    original = certificate['nontrivial_trees']['0']
    require(replay_tree(original, rows, columns) > 1, 'control case is not nontrivial')
    mutations = []
    bad = deepcopy(original)
    bad[1].pop()
    mutations.append(bad)
    bad = deepcopy(original)
    bad[0] = len(rows)
    mutations.append(bad)
    bad = deepcopy(original)
    bad[1][0][0] = len(columns)
    mutations.append(bad)
    mutations.append([0, []])
    rejected = 0
    for bad in mutations:
        try:
            replay_tree(bad, rows, columns)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('corrupted local proof accepted')
    try:
        consume_case(0, {}, rows, columns)
    except ValueError:
        rejected += 1
    else:
        raise ValueError('missing sparse proof accepted')
    one = (0, 1, 2, 3)
    for fake in ([0, []], [0, [[0, [0, []]]]]):
        try:
            replay_tree(fake, tuple(sorted(QUAD_PAIRS[one])), (one,))
        except ValueError:
            rejected += 1
        else:
            raise ValueError('positive exact cover accepted as a rejection proof')

    def multiply(a, b):
        result = 0
        for _ in range(2):
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & 4:
                a ^= 7
        return result
    fixed = tuple(tuple(4*x+y for y in range(4)) for x in range(4))
    known = tuple(tuple(sorted(4*x+(multiply(slope, x)^b) for x in range(4)))
                  for slope in range(4) for b in range(4))
    all_edges = Counter(e for q in fixed+known for e in QUAD_PAIRS[q])
    require(len(all_edges) == 120 and set(all_edges.values()) == {1}, 'invalid affine positive fixture')
    positive_rows = tuple(sorted(set(all_edges)-{e for q in fixed for e in QUAD_PAIRS[q]}))
    witness, _, _ = literal_cover(positive_rows, known)
    require(witness is not None and Counter(e for q in witness for e in QUAD_PAIRS[q]) == Counter(positive_rows),
            'separate literal solver rejected affine positive fixture')
    try:
        primary.rejection_tree(positive_rows, known)
    except CoverFound:
        pass
    else:
        raise ValueError('primary solver accepted affine cover as nonexistence')
    for routine, error_type in ((literal_cover, Incomplete), (primary.rejection_tree, PrimaryIncomplete)):
        try:
            routine(positive_rows, known, node_limit=0)
        except error_type:
            pass
        else:
            raise ValueError('zero-node solver guard yielded a mathematical verdict')
    multi = tuple(sorted(prefix[:2]))
    for routine, args in ((direct_zeros, (LEAVES['triangle_edge'], multi, 3)),
                          (primary.zero_frames, (primary.model('triangle_edge'), multi, 3))):
        try:
            routine(*args, node_limit=0)
        except (Incomplete, primary.Incomplete):
            pass
        else:
            raise ValueError('zero-node carrier guard yielded a completeness verdict')

    # A simple affine parallel-class switch gives a genuine all-unit star.
    # Replace one point of each of four parallel lines by the new point16.
    # This is a positive validation fixture, not a claimed new construction.
    switched = tuple(tuple(sorted((set(q)-{4*x}) | {16})) for x, q in enumerate(fixed)) + known
    high = (0, 4, 8, 12, 16)
    low = tuple(x for x in range(17) if x not in high)
    relabel = dict(zip(high+low, range(17)))
    unit = tuple(sorted(tuple(sorted(relabel[x] for x in q)) for q in switched))
    incidence = Counter(e for q in unit for e in QUAD_PAIRS[q])
    require(len(unit) == len(set(unit)) == 20 and len(incidence) == 120
            and set(incidence.values()) == {1}, 'invalid switched all-unit packing')
    require([sum(x in q for q in unit) for x in range(17)] == [4]*5+[5]*12,
            'switched fixture has wrong replication sequence')
    leave = ALL_PAIRS - set(incidence)
    require({e for e in leave if e[1] < 5} == {(0, 4), (1, 4), (2, 4), (3, 4)},
            'switched all-unit fixture has wrong four-edge high core')
    attached = {x for h, x in leave if h < 5 <= x}
    for x in LOW:
        n0 = sum(x in q and HIGH_COUNT[q] == 0 for q in unit)
        extra = sum(HIGH_COUNT[q]-1 for q in unit if x in q and HIGH_COUNT[q] >= 2)
        require(n0-extra == int(x in attached), 'positive unit incidence identity failed')
    unit_fixed = tuple(q for q in unit if HIGH_COUNT[q] != 1)
    unit_rows = tuple(sorted(ALL_PAIRS-leave-{e for q in unit_fixed for e in QUAD_PAIRS[q]}))
    unit_columns = tuple(q for q in ONE_HIGH if QUAD_PAIRS[q] <= frozenset(unit_rows))
    unit_witness = tuple(q for q in unit if HIGH_COUNT[q] == 1)
    require(len(unit_rows) == 96 and len(unit_witness) == 16 and set(unit_witness) <= set(unit_columns)
            and Counter(e for q in unit_witness for e in QUAD_PAIRS[q]) == Counter(unit_rows),
            'positive unit residual factory or explicit cover failed')
    return {'corrupted_or_missing_local_proofs_rejected': rejected,
            'positive_affine_fixture_checked': True, 'zero_node_guards_incomplete': 4,
            'positive_all_unit_star_checked': True, 'positive_all_unit_high_core_edges': 4,
            'positive_all_unit_residual_rows': 96}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare-primary', action='store_true')
    parser.add_argument('--controls-only', action='store_true')
    parser.add_argument('--checkpoint-dir', type=Path)
    args = parser.parse_args()
    blob = (HERE/'unit_six_certificate.json').read_bytes()
    certificate = json.loads(blob)
    require(blob == encoded(certificate), 'certificate is not canonical JSON')
    if args.controls_only:
        print(json.dumps(controls(certificate), indent=2, sort_keys=True))
        return
    report = verify(certificate, args.compare_primary, args.checkpoint_dir)
    require(json.loads((HERE/'unit_six_expected.json').read_text()) == report, 'separate expected report mismatch')
    control_report = controls(certificate)
    print(json.dumps({'verification': report, 'controls': control_report,
                      'entry_level_primary_comparison': args.compare_primary,
                      'separate_implementations_same_author': True}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
