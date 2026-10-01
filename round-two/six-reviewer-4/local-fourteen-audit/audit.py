"""Independent local-fourteen Book audit: six-reviewer-4, reviewer.

Standard library only; no author program is imported. Fixed-weight graph
words, generic graph-isomorphism backtracking and constraint-first integer
multicover replace the author's normalized group and incidence algorithms.
Every final obstruction is a two- or three-column rank-sum inequality.
"""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
from itertools import combinations, combinations_with_replacement, product
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAIRS = tuple(combinations(range(10), 2))
F_PAIRS = tuple(combinations(range(8), 2))
ALL = (1 << 10) - 1


def need(condition, message):
    if not condition:
        raise ValueError(message)


def stream_hash(values):
    return hashlib.sha256(b''.join(json.dumps(v, separators=(',', ':')).encode()
                                  + b'\n' for v in values)).hexdigest()


def weight_words(n, k):
    """All n-bit words of weight k in increasing order, without pruning."""
    if k == 0:
        yield 0
        return
    if not 0 < k <= n:
        return
    word = (1 << k) - 1
    while word < (1 << n):
        yield word
        low = word & -word
        carry = word + low
        word = carry + (((word ^ carry) // low) >> 2)


def graph(word):
    neighbors = [0] * 10
    for bit, (i, j) in enumerate(F_PAIRS):
        if word & (1 << bit):
            neighbors[i + 2] |= 1 << (j + 2)
            neighbors[j + 2] |= 1 << (i + 2)
    for x, pair in ((0, (2, 3)), (1, (4, 5))):
        for i in pair:
            neighbors[x] |= 1 << i
            neighbors[i] |= 1 << x
    return tuple(neighbors)


def colors(adj):
    result = tuple(x.bit_count() for x in adj)
    while True:
        signatures = [(result[i], tuple(sorted(result[j] for j in range(len(adj))
                                               if adj[i] & (1 << j))))
                      for i in range(len(adj))]
        labels = {v: i for i, v in enumerate(sorted(set(signatures)))}
        new = tuple(labels[v] for v in signatures)
        if len(set(new)) == len(set(result)):
            return new
        result = new


def isomorphism(a, b):
    """Generic color refinement/backtracking; no prescribed alignment group."""
    ca, cb = colors(a), colors(b)
    if Counter(ca) != Counter(cb):
        return None
    mapping = [-1] * len(a)

    def visit(used):
        if used.bit_count() == len(a):
            return tuple(mapping)
        alternatives = []
        for i in range(len(a)):
            if mapping[i] != -1:
                continue
            choices = [j for j in range(len(b)) if not used & (1 << j) and ca[i] == cb[j]
                       and all(bool(a[i] & (1 << k)) == bool(b[j] & (1 << mapping[k]))
                               for k in range(len(a)) if mapping[k] != -1)]
            alternatives.append((len(choices), i, choices))
        _, i, choices = min(alternatives)
        for j in choices:
            mapping[i] = j
            result = visit(used | (1 << j))
            if result is not None:
                return result
            mapping[i] = -1
        return None

    result = visit(0)
    if result is not None:
        need(set(result) == set(range(len(a))) and
             all(bool(a[i] & (1 << j)) == bool(b[result[i]] & (1 << result[j]))
                 for i in range(len(a)) for j in range(len(a))), 'literal isomorphism map')
    return result


def core_census(representatives):
    """A vertex-zero two-star and every weight-eight word on the other 21 pairs."""
    incidence = [sum(1 << bit for bit, pair in enumerate(F_PAIRS) if i in pair)
                 for i in range(8)]
    tail = tuple(weight_words(21, 8))
    need(len(tail) == comb(21, 8), 'complete fixed-weight tail')
    degrees = pairs = nonnegative = disjoint = 0
    eligible = []
    forbidden = (1 << F_PAIRS.index((0, 1))) | (1 << F_PAIRS.index((2, 3)))
    for star in combinations(range(7), 2):
        initial = sum(1 << i for i in star)
        for rest in tail:
            word = initial | (rest << 7)
            if any((word & incidence[i]).bit_count() != (2 if i < 4 else 3)
                   for i in range(1, 8)):
                continue
            degrees += 1
            if word & forbidden:
                continue
            pairs += 1
            adj = graph(word)
            _, _, capacity = bounds(adj, require_nonnegative=False)
            if min(capacity) < 0:
                continue
            nonnegative += 1
            if (adj[2] & adj[3] & ~3) or (adj[4] & adj[5] & ~3):
                continue
            disjoint += 1
            if any(adj[i] & adj[j] for i, j in PAIRS if adj[i] & (1 << j)):
                continue
            eligible.append(word)
    eligible.sort()
    rep_graphs = [graph(w) for w in representatives]
    need(len(set(representatives)) == len(representatives) and
         set(representatives) <= set(eligible), 'representatives belong to census')
    need(all(isomorphism(a, b) is None for a, b in combinations(rep_graphs, 2)),
         'representatives are pairwise nonisomorphic')
    maps, counts = [], Counter()
    for word in eligible:
        a = graph(word)
        match = None
        for index, b in enumerate(rep_graphs):
            phi = isomorphism(a, b)
            if phi is not None:
                match = index
                maps.append([word, representatives[index], list(phi)])
                counts[representatives[index]] += 1
                break
        need(match is not None, 'uncovered triangle-free normalized core')
    return {'fixed_weight_graph_words': comb(7, 2) * comb(21, 8),
            'degree_graphs': degrees, 'forbidden_pair_free_degree_graphs': pairs,
            'nonnegative_joint_capacity_graphs': nonnegative,
            'disjoint_pair_graphs': disjoint, 'triangle_free_graphs': len(eligible),
            'classes': len(representatives), 'aligned_words_sha256': stream_hash(eligible),
            'literal_isomorphism_maps_sha256': stream_hash(maps),
            'class_sizes': [[w, counts[w]] for w in representatives]}


def bounds(adj, require_nonnegative=True):
    h = [x.bit_count() for x in adj]
    need(h == [2, 2] + [3] * 8, 'normalized local degrees')
    columns = [d + 2 for d in h]
    capacity = []
    for i, j in PAIRS:
        if adj[i] & (1 << j):
            baseline = 1 + (adj[i] & adj[j]).bit_count() + 11 - columns[i] - columns[j]
            capacity.append(3 - baseline)
        else:
            blue = (ALL & ~(adj[i] | adj[j] | (1 << i) | (1 << j))).bit_count()
            capacity.append(6 - blue)
    if require_nonnegative:
        need(min(capacity) >= 0, 'nonnegative literal joint-miss bounds')
    return h, columns, capacity


def rows_for(adj, h, capacity):
    rows = []
    allowed = {(1, 0, 0), (0, 1, 1), (0, 1, 0), (0, 0, 1)}
    for z in range(1 << 10):
        k = z.bit_count()
        if not 4 <= k <= 8:
            continue
        if any(tuple((z >> i) & 1 for i in triple) not in allowed
               for triple in ((0, 2, 3), (1, 4, 5))):
            continue
        if any(not cap and z & (1 << i) and z & (1 << j)
               for (i, j), cap in zip(PAIRS, capacity)):
            continue
        valid = True
        for i in range(10):
            if z & (1 << i):
                if (z & ~adj[i] & ~(1 << i)).bit_count() > 6:
                    valid = False
            elif (adj[i] & ~z).bit_count() + max(0, k - h[i] - 2) > 3:
                valid = False
        if valid:
            rows.append(z)
    return rows


def certify(cut, rows, columns, capacity):
    need(type(cut['gamma']) is int and type(cut['rhs']) is int and
         len(cut['alpha']) == 10 and all(type(x) is int for x in cut['alpha']),
         'integer cut data')
    weights = {}
    for i, j, coefficient in cut['beta']:
        need(type(i) is type(j) is type(coefficient) is int and
             (i, j) in PAIRS and coefficient > 0 and (i, j) not in weights,
             'positive, unique integer weighted pair')
        weights[i, j] = coefficient
    scores = []
    for z in rows:
        scores.append(cut['gamma'] + sum(a for i, a in enumerate(cut['alpha']) if z & (1 << i))
                      + sum(a for (i, j), a in weights.items()
                            if z & (1 << i) and z & (1 << j)))
    need(min(scores) >= 0, 'nonnegative score on complete row domain')
    value = 11 * cut['gamma'] + sum(a * t for a, t in zip(cut['alpha'], columns))
    value += sum(weights.get(p, 0) * u for p, u in zip(PAIRS, capacity))
    need(value == cut['rhs'] and value <= 0, 'literal cut bound')
    zero = [z for z, score in zip(rows, scores) if score == 0] if value == 0 else []
    return zero, [index for index, pair in enumerate(PAIRS) if pair in weights]


def size_patterns(surplus, lowest=1):
    if not surplus:
        yield ()
    for extra in range(lowest, surplus + 1):
        for rest in size_patterns(surplus - extra, extra):
            yield (extra + 4,) + rest


def reconstruct(zero, columns, capacity, saturated):
    """Constraint-first integer multicover; neither multiset join nor RREF."""
    groups = {k: [z for z in zero if z.bit_count() == k] for k in range(4, 9)}
    fours = groups[4]
    pair_data = {z: tuple(int(bool(z & (1 << i) and z & (1 << j))) for i, j in PAIRS)
                 for z in zero}
    features = [tuple((z >> i) & 1 for i in range(10)) +
                tuple(pair_data[z][p] for p in saturated) + (1,) for z in fours]
    supports = [tuple(i for i, value in enumerate(f) if value) for f in features]
    width = 10 + len(saturated) + 1
    incident = [sum(1 << r for r, f in enumerate(features) if f[j]) for j in range(width)]

    @lru_cache(maxsize=100000)
    def cover(rhs, active):
        if not any(rhs):
            return ((0,) * len(fours),)
        usable = sum(1 << r for r in range(len(fours)) if active & (1 << r)
                     and all(rhs[j] > 0 for j in supports[r]))
        options = [(int((usable & incident[j]).bit_count()), j)
                   for j, value in enumerate(rhs) if value]
        count, equation = min(options)
        if not count:
            return ()
        selected = [r for r in range(len(fours)) if usable & incident[equation] & (1 << r)]
        next_active = usable & ~incident[equation]
        answer = []
        chosen = [0] * len(fours)

        def allocate(index, residual):
            if index == len(selected):
                if residual[equation]:
                    return
                for child in cover(residual, next_active):
                    answer.append(tuple(a + b for a, b in zip(chosen, child)))
                return
            r = selected[index]
            bound = min(residual[j] for j in supports[r])
            if index == len(selected) - 1:
                choices = (residual[equation],) if residual[equation] <= bound else ()
            else:
                choices = range(bound + 1)
            for value in choices:
                chosen[r] = value
                changed = tuple(x - (value if j in supports[r] else 0)
                                for j, x in enumerate(residual))
                allocate(index + 1, changed)
            chosen[r] = 0

        allocate(0, rhs)
        need(len(answer) == len(set(answer)), 'unique multicover multiplicities')
        return tuple(answer)

    matrices = []
    high_counts = Counter()
    raw = Counter()
    for sizes in size_patterns(4):
        multiplicities = Counter(sizes)
        domains = [combinations_with_replacement(groups[k], multiplicities[k])
                   for k in sorted(multiplicities)]
        for pieces in product(*domains):
            high = tuple(z for piece in pieces for z in piece)
            pattern = tuple(sorted(sizes, reverse=True))
            raw[pattern] += 1
            high_columns = [sum((z >> i) & 1 for z in high) for i in range(10)]
            high_pairs = [sum(pair_data[z][p] for z in high) for p in range(45)]
            residual_columns = tuple(t - c for t, c in zip(columns, high_columns))
            residual_pairs = tuple(u - c for u, c in zip(capacity, high_pairs))
            if min(residual_columns) < 0 or min(residual_pairs) < 0:
                continue
            high_counts[pattern] += 1
            rhs = residual_columns + tuple(residual_pairs[p] for p in saturated) + (11 - len(high),)
            for counts in cover(rhs, (1 << len(fours)) - 1):
                need(all(sum(c * f[j] for c, f in zip(counts, features)) == rhs[j]
                         for j in range(width)), 'complete multicover equality')
                low = [z for z, count in zip(fours, counts) for _ in range(count)]
                if any(sum(pair_data[z][p] for z in low) > residual_pairs[p] for p in range(45)):
                    continue
                matrix = sorted(list(high) + low)
                need(len(matrix) == 11, 'eleven repeated or distinct rows')
                matrices.append(matrix)
    matrices.sort()
    need(len(matrices) == len({tuple(r) for r in matrices}), 'unique full incidence multisets')
    return matrices, {'equations': width, 'four_row_types': len(fours),
                      'all_surplus_four_patterns': sorted([sorted(p, reverse=True) for p in size_patterns(4)]),
                      'raw_high_choices': [[list(k), v] for k, v in sorted(raw.items())],
                      'capped_high_choices': [[list(k), v] for k, v in sorted(high_counts.items())]}


def demands(adj, z):
    k = z.bit_count()
    return [k + n.bit_count() - 3 - (n & z).bit_count() - 3 * int(bool(z & (1 << i)))
            for i, n in enumerate(adj)]


def rank_sum(rows, b, subset, adj):
    k = rows[b].bit_count()
    required = sum(value for i, value in enumerate(demands(adj, rows[b])) if subset & (1 << i))
    available = sum(sorted(((subset & z).bit_count() for c, z in enumerate(rows) if c != b),
                           reverse=True)[:k])
    return required, available


def compressed_cuts(matrices, adj):
    subsets = [sum(1 << i for i in points) for k in (2, 3)
               for points in combinations(range(10), k)]
    certificates = []
    for rows in matrices:
        found = None
        for subset in subsets:
            for b in range(11):
                required, available = rank_sum(rows, b, subset, adj)
                if required > available:
                    found = [b, subset]
                    break
            if found is not None:
                break
        need(found is not None, 'two/three-column cover obstruction for every incidence')
        certificates.append(found)
    return {'schema': 1, 'actual_author': 'six-reviewer-4', 'role': 'independent reviewer',
            'incidences_sha256': stream_hash(matrices), 'cuts': certificates}


def certify_compressed(certificates, matrices, adj):
    need(certificates['schema'] == 1 and certificates['incidences_sha256'] == stream_hash(matrices)
         and len(certificates['cuts']) == len(matrices), 'complete compressed-certificate domain')
    sizes, margins = Counter(), Counter()
    for rows, item in zip(matrices, certificates['cuts']):
        need(isinstance(item, list) and len(item) == 2, 'cover cut format')
        b, subset = item
        need(type(b) is type(subset) is int and 0 <= b < 11 and 0 < subset <= ALL
             and subset.bit_count() in (2, 3), 'cover cut indices')
        required, available = rank_sum(rows, b, subset, adj)
        need(required > available, 'strict rank-sum contradiction')
        sizes[subset.bit_count()] += 1
        margins[required - available] += 1
    return {'certificates': len(matrices), 'subset_sizes': dict(sorted(sizes.items())),
            'integer_margins': dict(sorted(margins.items()))}


def literal_controls():
    """252 ten-regular circulants, actual/fake outside stars: exact demand bridge."""
    spines = stars = 0
    for steps in combinations(range(1, 11), 5):
        red = [sum(1 << ((v + direction * step) % 22) for step in steps for direction in (-1, 1))
               for v in range(22)]
        need(all(x.bit_count() == 10 for x in red), 'control ten-regularity')
        aa = [i for i in range(1, 22) if red[0] & (1 << i)]
        bb = [i for i in range(1, 22) if not red[0] & (1 << i)]
        adj = tuple(sum(1 << j for j, v in enumerate(aa) if red[u] & (1 << v)) for u in aa)
        rows = [sum(1 << i for i, v in enumerate(aa) if not red[u] & (1 << v)) for u in bb]
        need(all(sum((z >> i) & 1 for z in rows) == adj[i].bit_count() + 2 for i in range(10)),
             'literal miss column identity')
        for b, vertex in enumerate(bb):
            k = rows[b].bit_count()
            actual = [c for c, v in enumerate(bb) if red[vertex] & (1 << v)]
            fake = [c for c in range(11) if c != b][:k]
            need(len(actual) == k, 'literal outside degree equals miss size')
            for chosen in (actual, fake):
                full_b = sum(1 << v for i, v in enumerate(aa) if not rows[b] & (1 << i))
                full_b |= sum(1 << bb[c] for c in chosen)
                lower = demands(adj, rows[b])
                for i, v in enumerate(aa):
                    if rows[b] & (1 << i):
                        page_count = (((1 << 22) - 1) & ~red[v] & ~full_b &
                                      ~(1 << v) & ~(1 << vertex)).bit_count()
                        cap = 6
                    else:
                        page_count = (red[v] & full_b).bit_count()
                        cap = 3
                    coverage = sum((rows[c] >> i) & 1 for c in chosen)
                    need(page_count - cap == lower[i] - coverage, 'full literal demand/page identity')
                    spines += 1
                stars += 1
    for n in range(1, 8):
        for k in range(n + 1):
            for values in product(range(3), repeat=n):
                need(max(sum(values[i] for i in subset) for subset in combinations(range(n), k))
                     == sum(sorted(values, reverse=True)[:k]), 'top-k rank-sum control')
    return {'circulant_roots': comb(10, 5), 'actual_and_fake_stars': stars,
            'literal_spine_identities': spines, 'rank_sum_control_max_length': 7}


def build(cut_path, author_source=None, certificate_path=None):
    data = json.loads(cut_path.read_text())
    need(data['schema'] == 1, 'cut schema')
    cuts = data['cuts']
    census = core_census([c['F_mask'] for c in cuts])
    profiles, survivors = [], []
    for cut in cuts:
        adj = graph(cut['F_mask'])
        h, columns, capacity = bounds(adj)
        rows = rows_for(adj, h, capacity)
        zero, saturated = certify(cut, rows, columns, capacity)
        profiles.append({'F_mask': cut['F_mask'], 'row_sizes': dict(sorted(Counter(z.bit_count() for z in rows).items())),
                         'rows_sha256': stream_hash(rows), 'cut_rhs': cut['rhs'],
                         'zero_row_sizes': dict(sorted(Counter(z.bit_count() for z in zero).items()))})
        if zero:
            survivors.append((adj, columns, capacity, zero, saturated, cut['F_mask']))
    need(len(survivors) == 1, 'unique zero face')
    adj, columns, capacity, zero, saturated, mask = survivors[0]
    matrices, multicover = reconstruct(zero, columns, capacity, saturated)
    certificates = (json.loads(certificate_path.read_text()) if certificate_path is not None
                    else compressed_cuts(matrices, adj))
    certificate_summary = certify_compressed(certificates, matrices, adj)
    record = {'status': 'PASS', 'actual_author': 'six-reviewer-4', 'role': 'independent reviewer',
              'core_census': census, 'core_profiles': profiles, 'residual_F_mask': mask,
              'multicover': multicover, 'incidence_matrices': len(matrices),
              'incidences_sha256': stream_hash(matrices),
              'incidence_patterns': [[list(k), v] for k, v in sorted(Counter(tuple(sorted(
                  (z.bit_count() for z in r if z.bit_count() > 4), reverse=True)) for r in matrices).items())],
              'compressed_star_obstructions': certificate_summary, 'literal_controls': literal_controls()}
    comparison = None
    if author_source is not None:
        fixture = json.loads((author_source / 'incidences.json').read_text())
        expected = json.loads((author_source / 'expected.json').read_text())
        need([r['rows'] for r in fixture['records']] == matrices, 'all author incidence matrices entrywise')
        need(json.loads(json.dumps(profiles)) == expected['cores'], 'all author core/row profiles')
        need(expected['incidences_sha256'] == stream_hash(matrices), 'author incidence stream')
        need(expected['high_multisets'] == multicover['capped_high_choices'], 'all author capped high multisets')
        comparison = {'all_incidence_matrices': len(matrices), 'literal_incidence_entries': len(matrices) * 110,
                      'all_core_profiles': len(profiles), 'incidences_sha256': stream_hash(matrices)}
    return record, certificates, comparison


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cuts', type=Path, default=HERE / 'cuts.json')
    parser.add_argument('--expected', type=Path, default=HERE / 'expected.json')
    parser.add_argument('--cover-cuts', type=Path, default=HERE / 'cover-cuts.json')
    parser.add_argument('--author-source', type=Path)
    parser.add_argument('--emit', action='store_true')
    parser.add_argument('--emit-cover-cuts', action='store_true')
    args = parser.parse_args()
    certificate_path = None if args.emit or args.emit_cover_cuts else args.cover_cuts
    record, certificates, comparison = build(args.cuts, args.author_source, certificate_path)
    if args.emit or args.emit_cover_cuts:
        print(json.dumps(certificates if args.emit_cover_cuts else record, sort_keys=True, indent=2))
        return
    need(json.loads(args.expected.read_text()) == json.loads(json.dumps(record)), 'complete expected record')
    print(json.dumps({'status': 'PASS', 'aligned_triangle_free_cores': record['core_census']['triangle_free_graphs'],
                      'incidence_matrices': record['incidence_matrices'],
                      'compressed_star_obstructions': record['compressed_star_obstructions'],
                      'author_comparison': comparison}, sort_keys=True))


if __name__ == '__main__':
    main()
