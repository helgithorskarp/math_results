"""Independent Book22 dirty-root audit, six-reviewer-2, reviewer.

Third graph generator: prescribe degrees, complete each residual neighbor
row, quotient only literal partial twins. No author module or catalogue.
"""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL_HASH = '64eb0a83232e937de90de254cc48a2812dfbaaa900a1f08fe41d969c9e590ee8'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def decode(key, n):
    need(type(key) is int and 0 <= key < (1 << (n*(n-1)//2)), 'graph key range')
    rows = [0]*n
    for bit, (i, j) in enumerate(combinations(range(n), 2)):
        if key & (1 << bit):
            rows[i] |= 1 << j
            rows[j] |= 1 << i
    return tuple(rows)


def encode(rows):
    return sum(1 << bit for bit, (i, j) in enumerate(combinations(range(len(rows)), 2)) if rows[i] & (1 << j))


def degrees(rows):
    return [row.bit_count() for row in rows]


def valid_graph(rows, girth_five=True):
    n = len(rows)
    need(all(type(row) is int and 0 <= row < (1 << n) and not row & (1 << i) for i, row in enumerate(rows)), 'simple rows')
    need(all(bool(rows[i] & (1 << j)) == bool(rows[j] & (1 << i)) for i, j in combinations(range(n), 2)), 'symmetric rows')
    if max(degrees(rows), default=0) > 3:
        return False
    for i, j in combinations(range(n), 2):
        common = (rows[i] & rows[j]).bit_count()
        if rows[i] & (1 << j) and common:
            return False
        if girth_five and common >= 2:
            return False
    return True


def colors(rows, marked=False):
    d = degrees(rows)
    c = [(d[i], int(marked and i == 0)) for i in range(len(rows))]
    # These tuple colors are equivariant across separately labelled graphs.
    for _ in range(2):
        c = [(c[i], tuple(sorted(c[k] for k in range(len(rows)) if rows[i] & (1 << k)))) for i in range(len(rows))]
    return c


def invariant(rows, marked=False):
    return tuple(sorted(colors(rows, marked)))


def isomorphism(A, B, marked=False):
    if len(A) != len(B):
        return None
    n = len(A)
    ca, cb = colors(A, marked), colors(B, marked)
    if sorted(ca) != sorted(cb):
        return None
    mapping = [-1]*n
    used = 0

    def search(used):
        if used.bit_count() == n:
            return tuple(mapping)
        choices = []
        for i in range(n):
            if mapping[i] >= 0:
                continue
            candidates = [j for j in range(n) if not used & (1 << j) and ca[i] == cb[j]
                          and all(mapping[k] < 0 or bool(A[i] & (1 << k)) == bool(B[j] & (1 << mapping[k])) for k in range(n))]
            if not candidates:
                return None
            choices.append((len(candidates), i, candidates))
        _, i, candidates = min(choices)
        for j in candidates:
            mapping[i] = j
            answer = search(used | (1 << j))
            if answer is not None:
                need(not marked or answer[0] == 0, 'mark preserving')
                need(all(bool(A[k] & (1 << l)) == bool(B[answer[k]] & (1 << answer[l])) for k, l in combinations(range(n), 2)), 'literal isomorphism')
                return answer
            mapping[i] = -1
        return None

    return search(used)


def add_class(buckets, rows, marked=False):
    signature = invariant(rows, marked)
    for old in buckets[signature]:
        if isomorphism(rows, old, marked) is not None:
            return False
    buckets[signature].append(rows)
    return True


def generate(n=9, node_limit=2000000):
    """All max-three girth-five graphs via residual-degree completion.

    Future vertices with the same prescribed degree and old adjacency are
    literal twins of the partial graph. Choose a prefix from each twin cell.
    No arbitrary equivalence of final graphs is used as a pruning premise.
    """
    buckets = defaultdict(list)
    nodes = leaves = sequence_count = 0
    for counts in product(range(n+1), repeat=4):
        if sum(counts) != n:
            continue
        target = tuple(d for d in (3, 2, 1, 0) for _ in range(counts[d]))
        if sum(target) % 2:
            continue
        sequence_count += 1
        rows, remaining = [0]*n, list(target)

        def visit(i):
            nonlocal nodes, leaves
            nodes += 1
            need(nodes <= node_limit, 'operational node guard: incomplete enumeration')
            if i == n:
                need(not any(remaining), 'all degrees completed')
                graph = tuple(rows)
                need(degrees(graph) == list(target) and valid_graph(graph), 'literal leaf domain')
                leaves += 1
                add_class(buckets, graph)
                return
            r = remaining[i]
            if r < 0 or r > n-i-1 or any(remaining[k] > n-i-1 for k in range(i, n)):
                return
            cells = defaultdict(list)
            # Distance<=3 forbids a new edge closing a triangle/four-cycle.
            reach = 1 << i
            frontier = 1 << i
            for _ in range(3):
                nxt = 0
                for k in range(n):
                    if frontier & (1 << k):
                        nxt |= rows[k]
                frontier = nxt & ~reach
                reach |= nxt
            for k in range(i+1, n):
                if remaining[k] > 0 and not reach & (1 << k):
                    cells[(target[k], rows[k])].append(k)
            groups = list(cells.values())

            def subsets(group, left, chosen):
                if group == len(groups):
                    if left == 0:
                        yield tuple(chosen)
                    return
                cell = groups[group]
                for count in range(min(left, len(cell))+1):
                    extra = cell[:count]
                    # Pairwise old distance>=3 prevents cycles using two new edges.
                    if any(rows[a] & (1 << b) or rows[a] & rows[b] for a, b in combinations(chosen+extra, 2)):
                        continue
                    yield from subsets(group+1, left-count, chosen+extra)

            for chosen in subsets(0, r, []):
                rows[i] |= sum(1 << k for k in chosen)
                remaining[i] = 0
                for k in chosen:
                    rows[k] |= 1 << i
                    remaining[k] -= 1
                # The exact future degree demand cannot exceed its available slots.
                if all(remaining[k] <= n-i-2 for k in range(i+1, n)):
                    visit(i+1)
                for k in chosen:
                    remaining[k] += 1
                    rows[k] &= ~(1 << i)
                remaining[i] = r
                rows[i] &= ~sum(1 << k for k in chosen)

        visit(0)
    graphs = sorted((g for values in buckets.values() for g in values), key=encode)
    return graphs, {'order': n, 'degree_sequences': sequence_count, 'nodes': nodes, 'leaves_before_final_isomorphism': leaves,
                    'classes': len(graphs), 'edge_distribution': dict(sorted(Counter(sum(degrees(g))//2 for g in graphs).items()))}


def marked_extensions(graphs):
    buckets = defaultdict(list)
    additions = 0
    for F in graphs:
        e = sum(degrees(F))//2
        if e < 10:
            continue
        eligible = [i for i, d in enumerate(degrees(F)) if d < 3]
        for size in range(4):
            if not 13 <= e+size <= 15:
                continue
            for S in combinations(eligible, size):
                if any(F[i] & (1 << j) for i, j in combinations(S, 2)):
                    continue
                J = [sum(1 << (i+1) for i in S)]+[(F[i] << 1)|int(i in S) for i in range(9)]
                need(valid_graph(J, False) and valid_graph(tuple(x >> 1 for x in J[1:])), 'literal marked domain')
                additions += 1
                add_class(buckets, tuple(J), True)
    graphs = sorted((g for values in buckets.values() for g in values), key=encode)
    return graphs, additions


def column_capacities(J):
    d = degrees(J)
    sizes = [d[i]+2+int(i == 0) for i in range(10)]
    bounds = {}
    for i, j in combinations(range(10), 2):
        if J[i] & (1 << j):
            local_pages = 1+sum(bool(J[i] & (1 << k)) and bool(J[j] & (1 << k)) for k in range(10))
            cap = 3-local_pages-(11-sizes[i]-sizes[j])
        else:
            local_pages = sum(k not in (i, j) and not J[i] & (1 << k) and not J[j] & (1 << k) for k in range(10))
            cap = 6-local_pages
        bounds[i, j] = cap
    return sizes, bounds


def packing_bound(total, rows, width):
    """Cheapest marginal costs for bounded rows, independent of author DP."""
    need(0 <= total <= rows*width, 'bounded incidence total')
    return sum(sorted([cost for cost in range(width) for _ in range(rows)])[:total])


def all_cuts(J):
    sizes, bounds = column_capacities(J)
    values = []
    for size in range(2, 11):
        for S in combinations(range(10), size):
            Q = sum(sizes[i] for i in S)
            lower = packing_bound(Q, 11, size)
            upper = sum(bounds[i, j] for i, j in combinations(S, 2))
            values.append({'subset': list(S), 'column_incidences': Q, 'lower': lower, 'upper': upper})
    return values


def table_audit(models, generated):
    need(type(models) is list and len(models) == len(generated), 'complete model count')
    need(all(set(r) == {'key', 'edges', 'local_degrees', 'marked_degree', 'packing_rejection'} for r in models), 'model schema')
    decoded = [decode(r['key'], 10) for r in models]
    need(len({r['key'] for r in models}) == len(models), 'unique stored keys')
    bins = defaultdict(list)
    for index, g in enumerate(decoded):
        need(valid_graph(g, False) and valid_graph(tuple(x >> 1 for x in g[1:])), 'model graph domain')
        r = models[index]
        need((r['edges'], r['local_degrees'], r['marked_degree']) == (sum(degrees(g))//2, degrees(g), degrees(g)[0]), 'model degree metadata')
        bins[invariant(g, True)].append(index)
    matches = {}
    for g in generated:
        targets = [(i, isomorphism(g, decoded[i], True)) for i in bins[invariant(g, True)]]
        good = [(i, m) for i, m in targets if m is not None]
        need(len(good) == 1 and good[0][0] not in matches, 'bijective literal marked-class match')
        matches[good[0][0]] = good[0][1]
    need(len(matches) == len(models), 'every published class covered')
    transcript = sha256()
    survivors, rejected, certificates = [], [], []
    for r, g in sorted(zip(models, decoded), key=lambda pair: pair[0]['key']):
        cuts = all_cuts(g)
        for cut in cuts:
            transcript.update(json.dumps([r['key'], cut], sort_keys=True, separators=(',', ':')).encode()+b'\n')
        failures = [cut for cut in cuts if cut['upper'] < cut['lower']]
        stored = r['packing_rejection']
        need((stored is None) == (not failures), 'exact survivor/rejection status')
        if failures:
            need(stored in failures, 'stored witness literally correct')
            rejected.append(r['key'])
            first = min(failures, key=lambda cut: (len(cut['subset']), cut['subset']))
            certificates.append({'key': r['key'], **first})
        else:
            survivors.append({'key': r['key'], 'edges': r['edges'], 'degrees': sorted(r['local_degrees']), 'marked_degree': r['marked_degree']})
    return {'marked_classes': len(models), 'entrywise_matches': len(matches), 'subsets_per_class': len(all_cuts(decoded[0])),
            'packing_cut_scalars': len(models)*len(all_cuts(decoded[0])), 'cut_transcript_sha256': transcript.hexdigest(),
            'rejected': len(rejected), 'survivors': survivors, 'rejection_certificates': certificates}


def occurrence_audit():
    # z,a,b have degrees8,9,9. Enumerate all low graph edges and all
    # nonsingleton high types; singleton counts are forced by column sums.
    records = []
    for low in range(8):
        L = decode(low, 3)
        R = [d-x for d, x in zip((8, 9, 9), degrees(L))]
        for triple in range(min(R)+1):
            for za, zb, ab in product(range(5), repeat=3):
                pair = [za, zb, ab]
                singles = [R[0]-za-zb-triple, R[1]-za-ab-triple, R[2]-zb-ab-triple]
                if min(singles) < 0 or sum(singles)+sum(pair)+triple != 19:
                    continue
                valid = True
                for k, (i, j) in enumerate(combinations(range(3), 2)):
                    common = pair[k]+triple+(L[i] & L[j]).bit_count()
                    red = bool(L[i] & (1 << j))
                    pages = common if red else 20-(8, 9, 9)[i]-(8, 9, 9)[j]+common
                    if pages > (3 if red else 6):
                        valid = False
                if not valid:
                    continue
                roots = singles[1]+singles[2]
                qz = degrees(L)[0]
                extra = int(bool(L[1] & (1 << 2)))+int(bool(L[0] & 2) and bool(L[0] & 4))+triple
                need(roots >= 7+qz+extra, 'sharper one-nine occurrence')
                records.append({'low_key': low, 'singles_z_a_b': singles, 'pairs_za_zb_ab': pair,
                                'triple': triple, 'one_nine_roots': roots})
    need(records and min(r['one_nine_roots'] for r in records) == 7, 'abstract incidence minimum')
    exceptional = []
    pairs = list(combinations(range(4), 2))
    for x in product(range(5), repeat=6):
        if all(sum(x[k] for k, ij in enumerate(pairs) if i in ij) == 9 for i in range(4)):
            need((x[0], x[1], x[2]) == (x[5], x[4], x[3]), 'opposite pair equalities')
            exceptional.append(x)
    return {'three_low_incidence_models': len(records), 'minimum_one_nine_roots': 7,
            'abstract_seven_root_fixture': next(r for r in records if r['one_nine_roots'] == 7),
            'root_count_distribution': dict(sorted(Counter(r['one_nine_roots'] for r in records).items())),
            'exceptional_labelled_signatures': len(exceptional),
            'exceptional_unordered_signatures': sorted({tuple(sorted(x[:3])) for x in exceptional})}


def run(model=ROOT/'MODEL.json'):
    raw = model.read_bytes()
    need(sha256(raw).hexdigest() == MODEL_HASH, 'source model hash')
    unmarked, census = generate()
    marked, additions = marked_extensions(unmarked)
    table = table_audit(json.loads(raw), marked)
    return {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer',
            'model_sha256': MODEL_HASH, 'generator': census, 'raw_marked_additions': additions,
            'marked_audit': table, 'occurrence_audit': occurrence_audit()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, default=ROOT/'MODEL.json')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--generator-only', action='store_true')
    args = parser.parse_args()
    result = generate()[1] if args.generator_only else run(args.model)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'complete': True, 'summary': result['generator'] if 'generator' in result else result}))
