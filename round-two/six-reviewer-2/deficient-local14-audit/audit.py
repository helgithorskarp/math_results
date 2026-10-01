"""Independent Book22 deficient local14 audit; six-reviewer-2, reviewer.

No author code import. Geometric KG(5,2) core, sequential Venn-cell
refinement of eleven outside points, literal full-neighborhood domains,
and binary outside-edge decisions with partial-page lower bounds.
"""
import argparse
import ast
from collections import Counter
import hashlib
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
import tempfile
import time

START = time.monotonic()
MAX_STATES = 2_000_000
MAX_SECONDS = 100


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def guard(states):
    if states > MAX_STATES or time.monotonic() - START > MAX_SECONDS:
        raise RuntimeError('INCOMPLETE: fixed operational guard reached')


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def geometry():
    ground = list(combinations(range(5), 2))
    adj = [{j for j in range(10) if i != j and set(ground[i]).isdisjoint(ground[j])}
           for i in range(10)]
    adj[0].remove(7)
    adj[7].remove(0)
    # A complete checked relabeling of the cited coefficient data, not an
    # assumed symmetry of an unknown Book22 host.
    relabel = [0, 7, 8, 9, 3, 6, 1, 2, 4, 5]
    original_edges = [(0, 2), (0, 3), (1, 4), (1, 5), (2, 7), (2, 9),
                      (3, 6), (3, 8), (4, 8), (4, 9), (5, 6), (5, 7),
                      (6, 9), (7, 8)]
    require({tuple(sorted((relabel[i], relabel[j]))) for i, j in original_edges}
            == {(i, j) for i, j in combinations(range(10), 2) if j in adj[i]},
            'Geometric/core relabeling mismatch')
    return adj, relabel


def checked_cut(path, adj, relabel):
    spec = json.loads(path.read_text())
    require(spec['schema'] == 1 and spec['core_mask'] == 51317328, 'Cut schema/core')
    cut = spec['cut']
    require(cut['F_mask'] == spec['core_mask'], 'Cut label binding')
    require(len(cut['alpha']) == 10 and all(type(x) is int for x in cut['alpha']),
            'Integer column coefficients required')
    require(type(cut['gamma']) is int and type(cut['rhs']) is int, 'Integer constants required')
    seen = set()
    for i, j, q in cut['beta']:
        require(all(type(x) is int for x in [i, j, q]) and 0 <= i < j < 10 and q > 0,
                'Positive integer pair coefficient required')
        require((i, j) not in seen, 'Duplicate pair coefficient')
        seen.add((i, j))
    alpha = [0] * 10
    for i, value in enumerate(cut['alpha']):
        alpha[relabel[i]] = value
    beta = {tuple(sorted((relabel[i], relabel[j]))): q for i, j, q in cut['beta']}
    h = list(map(len, adj))
    caps = {(i, j): h[i] + h[j] - (5 if j in adj[i] else 2) - len(adj[i] & adj[j])
            for i, j in combinations(range(10), 2)}
    upper = 11 * cut['gamma'] + sum(alpha[i] * (h[i] + 2) for i in range(10))
    upper += sum(q * caps[p] for p, q in beta.items())
    require(upper == cut['rhs'] == 0, 'Cut upper bound must be zero')
    return alpha, beta, cut['gamma'], caps


def row_domains(adj, alpha, beta, gamma, caps):
    all_rows, zeros, score_hist = [], [], []
    for deficit in range(3):
        domain, face, hist = [], [], Counter()
        for mask in range(1024):
            z = {i for i in range(10) if mask & (1 << i)}
            k = len(z)
            if k < 4 + deficit:
                continue
            if any(tuple(int(i in z) for i in triple) not in
                   [(1, 0, 0), (0, 1, 1), (0, 1, 0), (0, 0, 1)]
                   for triple in [(0, 8, 9), (7, 3, 6)]):
                continue
            if any(caps[(i, j)] == 0 for i, j in combinations(sorted(z), 2)):
                continue
            t = [len(adj[i] & z) for i in range(10)]
            if any(k > t[i] + 5 + deficit for i in range(10) if i not in z):
                continue
            if any(k - 1 - t[i] > 6 for i in z):
                continue
            score = gamma + sum(alpha[i] for i in z)
            score += sum(q for (i, j), q in beta.items() if i in z and j in z)
            require(score >= 0, 'Negative cut score on a necessary row')
            domain.append(mask)
            hist[score] += 1
            if score == 0:
                face.append(mask)
        all_rows.append(domain)
        zeros.append(face)
        score_hist.append(dict(sorted(hist.items())))
    return all_rows, zeros, score_hist


def incidence_partitions(adj, zeros, beta, caps):
    union = sorted(set().union(*map(set, zeros)))
    order = [0, 8, 9, 7, 3, 6, 1, 4, 2, 5]
    targets = [len(a) + 2 for a in adj]
    pair_list = list(combinations(range(10), 2))
    marks = {z: sum(1 << p for p, (i, j) in enumerate(pair_list)
                    if z & (1 << i) and z & (1 << j)) for z in union}
    # Each cell signature determines exactly which row words can extend it.
    supports = []
    processed = 0
    for depth in range(11):
        classes = {}
        for z in union:
            signature = z & processed
            classes.setdefault(signature, []).append(z)
        table = {}
        for signature, words in classes.items():
            row_any, row_all, pair_any, pair_all = 0, 1023, 0, (1 << 45) - 1
            for z in words:
                row_any |= z
                row_all &= z
                pair_any |= marks[z]
                pair_all &= marks[z]
            table[signature] = (row_any, row_all, pair_any, pair_all)
        supports.append(table)
        if depth < 10:
            processed |= 1 << order[depth]
    stats = Counter()
    matrices = []

    def necessary(cells, depth):
        table = supports[depth]
        minimum = [0] * 10
        maximum = [0] * 10
        pair_min = [0] * 45
        pair_max = [0] * 45
        for mask, multiplicity in cells:
            if mask not in table:
                return False
            row_any, row_all, pair_any, pair_all = table[mask]
            for i in range(10):
                minimum[i] += multiplicity * ((row_all >> i) & 1)
                maximum[i] += multiplicity * ((row_any >> i) & 1)
            for p in range(45):
                pair_min[p] += multiplicity * ((pair_all >> p) & 1)
                pair_max[p] += multiplicity * ((pair_any >> p) & 1)
        if any(not minimum[i] <= targets[i] <= maximum[i] for i in range(10)):
            return False
        for p, ij in enumerate(pair_list):
            if pair_min[p] > caps[ij]:
                return False
            # The zero cut total also forces every positively weighted pair
            # to saturate its cap. This is an exact consequence, not a heuristic.
            if ij in beta and pair_max[p] < caps[ij]:
                return False
        return True

    def visit(cells, depth):
        stats['partition_states'] += 1
        guard(stats['partition_states'])
        if not necessary(cells, depth):
            stats['bounds_rejections'] += 1
            return
        if depth == 10:
            matrices.append(sorted(z for z, multiplicity in cells for _ in range(multiplicity)))
            return
        vertex = order[depth]
        table = supports[depth]
        next_table = supports[depth + 1]
        limits = []
        for mask, size in cells:
            zero = mask in next_table
            one = (mask | (1 << vertex)) in next_table
            require(zero or one, 'Unextendible accepted prefix')
            limits.append((0 if zero else size, size if one else 0))
        suffix_min, suffix_max = [0] * (len(cells) + 1), [0] * (len(cells) + 1)
        for ix in range(len(cells) - 1, -1, -1):
            suffix_min[ix] = suffix_min[ix + 1] + limits[ix][0]
            suffix_max[ix] = suffix_max[ix + 1] + limits[ix][1]
        intersections = [0] * depth
        counts = []

        def distribute(ix, left):
            if not suffix_min[ix] <= left <= suffix_max[ix]:
                return
            if ix == len(cells):
                if any(intersections[p] != caps[tuple(sorted((vertex, old)))]
                       for p, old in enumerate(order[:depth])
                       if tuple(sorted((vertex, old))) in beta):
                    return
                refined = []
                for (mask, size), count in zip(cells, counts):
                    if size > count:
                        refined.append((mask, size - count))
                    if count:
                        refined.append((mask | (1 << vertex), count))
                visit(tuple(sorted(refined)), depth + 1)
                return
            mask, size = cells[ix]
            lower, upper = limits[ix]
            lower = max(lower, left - suffix_max[ix + 1])
            upper = min(upper, left - suffix_min[ix + 1])
            for count in range(lower, upper + 1):
                if any(intersections[p] + count > caps[tuple(sorted((vertex, old)))]
                       for p, old in enumerate(order[:depth]) if mask & (1 << old)):
                    continue
                counts.append(count)
                for p, old in enumerate(order[:depth]):
                    if mask & (1 << old):
                        intersections[p] += count
                distribute(ix + 1, left - count)
                for p, old in enumerate(order[:depth]):
                    if mask & (1 << old):
                        intersections[p] -= count
                counts.pop()
        distribute(0, targets[vertex])

    visit(((0, 11),), 0)
    matrices.sort()
    require(len(matrices) == len({tuple(m) for m in matrices}), 'Duplicate partition output')
    return matrices, dict(stats)


def page_ok(u, nu, v, nv, universe):
    require((v in nu) == (u in nv), 'Nonreciprocal fixed/candidate pair')
    if v in nu:
        return len(nu & nv) <= 3
    return len((universe - {u} - nu) & (universe - {v} - nv)) <= 6


def literal_stars(rows, adj):
    universe = set(range(22))
    fixed = [{*range(1, 11)}]
    for i in range(10):
        fixed.append({0} | {j + 1 for j in adj[i]} |
                     {b + 11 for b, row in enumerate(rows) if not row & (1 << i)})
    require(all(len(n) == 10 for n in fixed), 'Full-root degree reconstruction')
    require(all(page_ok(i, fixed[i], j, fixed[j], universe)
                for i, j in combinations(range(11), 2)), 'Invalid fixed spine')
    domains = []
    for b, row in enumerate(rows):
        local = {i + 1 for i in range(10) if not row & (1 << i)}
        all_choices = []
        for deficit in range(3):
            size = row.bit_count() - deficit
            kept = []
            for star in combinations([c for c in range(11) if c != b], size):
                nb = local | {c + 11 for c in star}
                if all(page_ok(b + 11, nb, i, fixed[i], universe) for i in range(11)):
                    kept.append(sum(1 << c for c in star))
            all_choices.append(kept)
        domains.append(all_choices)
    return domains


def edge_search(initial, fixed_red, fixed_blue, red_cap=3, blue_cap=6):
    n = len(initial)
    full = (1 << n) - 1
    pair_list = list(combinations(range(n), 2))
    stats = Counter()

    def force(red, blue, b, c, color):
        yes, no = (red, blue) if color else (blue, red)
        if (no[b] >> c) & 1 or (no[c] >> b) & 1:
            return False
        yes[b] |= 1 << c
        yes[c] |= 1 << b
        return True

    def visit(domains, red, blue):
        stats['edge_nodes'] += 1
        guard(stats['edge_nodes'])
        while True:
            previous = tuple(red + blue)
            for b in range(n):
                domains[b] = [star for star in domains[b]
                              if star & red[b] == red[b] and not star & blue[b]]
                if not domains[b]:
                    stats['empty_domains'] += 1
                    return None
                common, union = full ^ (1 << b), 0
                for star in domains[b]:
                    common &= star
                    union |= star
                for c in range(n):
                    if c == b:
                        continue
                    if common & (1 << c) and not force(red, blue, b, c, True):
                        stats['reciprocity_rejections'] += 1
                        return None
                    if not union & (1 << c) and not force(red, blue, b, c, False):
                        stats['reciprocity_rejections'] += 1
                        return None
            for b, c in pair_list:
                red_bad = fixed_red[b][c] + (red[b] & red[c]).bit_count() > red_cap
                blue_bad = fixed_blue[b][c] + (blue[b] & blue[c]).bit_count() > blue_cap
                if red_bad and not force(red, blue, b, c, False):
                    stats['page_rejections'] += 1
                    return None
                if blue_bad and not force(red, blue, b, c, True):
                    stats['page_rejections'] += 1
                    return None
            if previous == tuple(red + blue):
                break
        unknown = [(b, c) for b, c in pair_list if not ((red[b] | blue[b]) >> c) & 1]
        if not unknown:
            require(all(red[b] in domains[b] for b in range(n)), 'Leaf not in star domain')
            return red
        b, c = unknown[0]
        for color in [False, True]:
            next_red, next_blue = red.copy(), blue.copy()
            require(force(next_red, next_blue, b, c, color), 'Branch on decided edge')
            answer = visit([list(x) for x in domains], next_red, next_blue)
            if answer is not None:
                return answer
        return None

    answer = visit([list(x) for x in initial], [0] * n, [0] * n)
    return answer, dict(stats)


def outside_cases(matrices, adj):
    records, cases, total = [], [], Counter()
    for index, rows in enumerate(matrices):
        guard(index)
        domains = literal_stars(rows, adj)
        counts = [[len(x) for x in per_b] for per_b in domains]
        assignments = []
        # Weak compositions of total deficiency two, including repeated point.
        for p, q in combinations_with_replacement(range(11), 2):
            deficits = [0] * 11
            deficits[p] += 1
            deficits[q] += 1
            if not all(domains[b][d] for b, d in enumerate(deficits)):
                continue
            assignments.append(deficits)
            red = [[0] * 11 for _ in range(11)]
            blue = [[0] * 11 for _ in range(11)]
            for b, c in combinations(range(11), 2):
                red[b][c] = red[c][b] = 10 - (rows[b] | rows[c]).bit_count()
                blue[b][c] = blue[c][b] = 1 + (rows[b] & rows[c]).bit_count()
            stars = [domains[b][d] for b, d in enumerate(deficits)]
            answer, stats = edge_search(stars, red, blue)
            total.update(stats)
            require(answer is None, 'A valid local14 completion was found: ' +
                    json.dumps({'rows': rows, 'deficits': deficits, 'stars': answer}))
            cases.append({'incidence_index': index, 'deficits': deficits,
                          'domain_sizes': [len(x) for x in stars], 'edge_search': stats})
        records.append({'rows': rows, 'star_counts': counts,
                        'deficit_assignments': sorted(assignments)})
    return records, sorted(cases, key=lambda c: (c['incidence_index'], c['deficits'])), dict(total)


def small_edge_controls():
    n = 4
    pairs = list(combinations(range(n), 2))
    graphs = []
    for encoding in range(1 << len(pairs)):
        stars = [0] * n
        for bit, (i, j) in enumerate(pairs):
            if encoding & (1 << bit):
                stars[i] |= 1 << j
                stars[j] |= 1 << i
        graphs.append(stars)
    profiles = sorted({tuple(x.bit_count() for x in g) for g in graphs})
    controls = 0
    for degrees in profiles:
        initial = [[sum(1 << q for q in choice)
                    for choice in combinations([q for q in range(n) if q != b], d)]
                   for b, d in enumerate(degrees)]
        for cap in [0, 1, 2]:
            expected = any(tuple(x.bit_count() for x in g) == degrees and
                           all(((g[i] & g[j]).bit_count() <= cap if g[i] & (1 << j)
                                else (((15 ^ (1 << i)) ^ g[i]) &
                                      ((15 ^ (1 << j)) ^ g[j])).bit_count() <= cap)
                               for i, j in pairs) for g in graphs)
            answer, _ = edge_search(initial, [[0] * n for _ in range(n)],
                                    [[0] * n for _ in range(n)], cap, cap)
            require((answer is not None) == expected, 'Literal small graph control fails')
            controls += 1
    # An explicit positive cycle and a nonreciprocal singleton domain.
    cycle = [10, 5, 10, 5]
    answer, _ = edge_search([[x] for x in cycle], [[0] * n for _ in range(n)],
                            [[0] * n for _ in range(n)], 0, 0)
    require(answer == cycle, 'Positive four-cycle control')
    broken = [[x] for x in cycle]
    broken[0] = [8]
    answer, _ = edge_search(broken, [[0] * n for _ in range(n)], [[0] * n for _ in range(n)])
    require(answer is None, 'Asymmetric star control accepted')
    return controls + 2


def local_normalization_controls():
    # A first-layer pairing of P6 must have all path distances >=3.
    pairings = []
    def match(left, chosen):
        if not left:
            pairings.append(chosen)
            return
        a = left[0]
        for b in left[1:]:
            match([i for i in left if i not in [a, b]], chosen + [(a, b)])
    match(list(range(6)), [])
    path = [p for p in pairings if all(abs(i - j) >= 3 for i, j in p)]
    cycle = [p for p in pairings if all(min(abs(i - j), 6 - abs(i - j)) >= 3
                                      for i, j in p)]
    require(path == [[(0, 3), (1, 4), (2, 5)]] and cycle == path,
            'P6/C6 Moore pairings')
    profiles = []
    # Every subcubic ten-vertex graph with >=13 edges has deficit<=4.
    for isolated in range(2):
        for low in range(5):
            total_deficit = 3 * isolated + low
            if total_deficit <= 4 and total_deficit % 2 == 0:
                profiles.append({'isolated': isolated, 'degree_two': low,
                                 'edges': (30 - total_deficit) // 2})
    require([(p['isolated'], p['degree_two']) for p in profiles] ==
            [(0, 0), (0, 2), (0, 4), (1, 1)], 'Subcubic profile coverage')
    return {'perfect_matchings': len(pairings), 'path_survivors': len(path),
            'cycle_survivors': len(cycle), 'profiles': profiles}


def compare_external_records(actual, external):
    require(isinstance(external, list) and len(external) == len(actual),
            'Incomplete external incidence coverage')
    projected = []
    for record in external:
        rows = record['rows']
        require(len(rows) == 11 and all(type(z) is int and 0 <= z < 1024 for z in rows),
                'Malformed external row encoding')
        require(rows == sorted(rows), 'External rows are not canonical')
        counts = record['star_counts']
        require(len(counts) == 11 and all(len(x) == 3 and
                all(type(q) is int and q >= 0 for q in x) for x in counts),
                'Malformed external domain cardinalities')
        assignments = record['deficit_assignments']
        require(all(len(ds) == 11 and all(type(d) is int and 0 <= d <= 2 for d in ds)
                    and sum(ds) == 2 for ds in assignments), 'Incorrect external deficiency')
        projected.append({'rows': rows, 'star_counts': counts,
                          'deficit_assignments': sorted(assignments)})
    projected.sort(key=lambda record: record['rows'])
    require(len({tuple(r['rows']) for r in projected}) == len(projected),
            'Repeated external incidence')
    require(actual == projected, 'External incidence/domain/deficit mismatch')


def corruption_controls(certificate_path, adj, relabel, records, output_dir):
    spec = json.loads(certificate_path.read_text())
    rejected = []
    with tempfile.TemporaryDirectory(prefix='book22-cut-controls-', dir=output_dir) as temporary:
        path = Path(temporary) / 'cut.json'
        for name in ['wrong_bound', 'noninteger_beta', 'wrong_core_binding', 'duplicate_beta']:
            broken = json.loads(json.dumps(spec))
            if name == 'wrong_bound':
                broken['cut']['rhs'] = 1
            elif name == 'noninteger_beta':
                broken['cut']['beta'][0][2] = 0.5
            elif name == 'wrong_core_binding':
                broken['cut']['F_mask'] ^= 1
            else:
                broken['cut']['beta'].append(broken['cut']['beta'][0])
            path.write_text(json.dumps(broken))
            try:
                checked_cut(path, adj, relabel)
            except RuntimeError:
                rejected.append(name)
            else:
                raise RuntimeError('Damaged cut accepted: ' + name)
    compare_external_records(records, records)
    for name in ['missing_matrix', 'duplicate_matrix', 'wrong_domain_size', 'wrong_deficiency']:
        broken = json.loads(json.dumps(records))
        if name == 'missing_matrix':
            broken.pop()
        elif name == 'duplicate_matrix':
            broken[-1] = broken[0]
        elif name == 'wrong_domain_size':
            broken[0]['star_counts'][0][0] += 1
        else:
            chosen = next(r for r in broken if r['deficit_assignments'])
            chosen['deficit_assignments'][0] = [0] * 11
        try:
            compare_external_records(records, broken)
        except RuntimeError:
            rejected.append(name)
        else:
            raise RuntimeError('Damaged record accepted: ' + name)
    return rejected


def primary_control(path):
    # The original primary file is a literal binary matrix followed by
    # search metadata. Parse only the literal; never evaluate its metadata.
    text = path.read_text()
    require(']]' in text, 'Primary matrix terminator')
    matrices = ast.literal_eval(text.split(']]', 1)[0] + ']]')
    require(isinstance(matrices, list) and len(matrices) == 21 and
            all(isinstance(row, list) and len(row) == 21 and
                all(type(x) is int and x in [0, 1] for x in row) for row in matrices),
            'Primary matrix encoding')
    require(all(matrices[i][j] == matrices[j][i] for i, j in combinations(range(21), 2)),
            'Primary matrix symmetry')
    red = [{j for j in range(21) if j != i and matrices[i][j] == 0} for i in range(21)]
    universe = set(range(21))
    require(all(i not in red[i] and all(i in red[j] for j in red[i]) for i in range(21)),
            'Primary matrix symmetry')
    blue = [universe - {i} - red[i] for i in range(21)]
    max_red = max(len(red[i] & red[j]) for i, j in combinations(range(21), 2) if j in red[i])
    max_blue = max(len(blue[i] & blue[j]) for i, j in combinations(range(21), 2) if j in blue[i])
    red_edges = sum(map(len, red)) // 2
    require((red_edges, max_red, max_blue) == (93, 3, 6), 'Primary known construction')
    return {'red_edges': red_edges, 'blue_edges': 210 - red_edges,
            'max_red_pages': max_red, 'max_blue_pages': max_blue,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--primary', type=Path, required=True)
    parser.add_argument('--compare-author', type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    adj, relabel = geometry()
    alpha, beta, gamma, caps = checked_cut(args.certificate, adj, relabel)
    admissible, zeros, score_hist = row_domains(adj, alpha, beta, gamma, caps)
    native, partition_stats = incidence_partitions(adj, zeros, beta, caps)
    canonical = sorted(sorted(sum(1 << i for i, geo in enumerate(relabel)
                                  if row & (1 << geo)) for row in matrix)
                       for matrix in native)
    source_adj = [{j for j in range(10) if relabel[j] in adj[relabel[i]]}
                  for i in range(10)]
    records, cases, edge_stats = outside_cases(canonical, source_adj)
    result = {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer',
              'complete': True, 'core_construction': 'KG(5,2) minus edge 0--7',
              'source_to_geometry': relabel,
              'admissible_rows_by_deficit': [len(x) for x in admissible],
              'zero_rows_by_deficit': [len(x) for x in zeros],
              'score_histograms': score_hist,
              'union_zero_rows': len(set().union(*map(set, zeros))),
              'saturated_pair_count': len(beta), 'partition_stats': partition_stats,
              'matrices': len(canonical), 'matrix_sha256': digest(canonical),
              'candidate_matrices': sum(bool(r['deficit_assignments']) for r in records),
              'deficit_cases': len(cases),
              'assignment_types': dict(sorted(Counter(','.join(map(str, sorted(d for d in c['deficits'] if d)))
                                                        for c in cases).items())),
              'case_domain_sha256': digest([{k: c[k] for k in ['incidence_index', 'deficits', 'domain_sizes']}
                                           for c in cases]),
              'edge_stats': edge_stats, 'solutions': 0,
              'literal_small_controls': small_edge_controls(),
              'normalization_controls': local_normalization_controls(),
              'primary21': primary_control(args.primary),
              'damaged_control_rejections': corruption_controls(args.certificate, adj, relabel, records,
                                                                 args.output_dir)}
    if args.compare_author:
        compare_external_records(records, json.loads(args.compare_author.read_text()))
    result = json.loads(json.dumps(result))
    if args.expected:
        require(result == json.loads(args.expected.read_text()), 'Exact expected record mismatch')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, value in [('RESULT.json', result), ('RECORDS.json', records), ('CASES.json', cases)]:
        (args.output_dir / name).write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
