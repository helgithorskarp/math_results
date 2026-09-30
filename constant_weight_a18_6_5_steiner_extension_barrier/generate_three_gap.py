"""Complete three-gap records, exact K4 exclusion, and one-word K5 bound.

Standard-library integer arithmetic only. No full record or graph dump is
written. The separate checker uses fixed-order sets and pair incidences.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import time

from geometry import classical_design, generators, mask, move, points, require
from generate_two_gap import digest, enumerate_masks

CASES = (
    ((362, 661, 1178), 4080),
    ((362, 661, 3457), 8160),
    ((362, 661, 16553), 4080),
    ((362, 661, 19476), 4080),
    ((362, 661, 50241), 2040),
    ((362, 661, 80896), 136),
    ((362, 1178, 1828), 4080),
    ((362, 1178, 2840), 8160),
    ((362, 1178, 6155), 1360),
    ((362, 1178, 9223), 8160),
    ((362, 1178, 9440), 1360),
    ((362, 1178, 12564), 4080),
    ((362, 3457, 12564), 340),
)


def graph(records):
    start = time.monotonic()
    n = len(records)
    require(n <= 40000, 'INCOMPLETE: graph memory guard')
    old_rows = {}
    q_records = {}
    for i, (b, qs) in enumerate(records):
        bit = 1 << i
        for triple in combinations(points(b), 3):
            t = mask(triple)
            old_rows[t] = old_rows.get(t, 0) | bit
        for q in qs:
            q_records[q] = q_records.get(q, 0) | bit
    q_bad = {}
    for q in q_records:
        bad = 0
        for r, vertices in q_records.items():
            if r != q and (q & r).bit_count() > 1:
                bad |= vertices
        q_bad[q] = bad
    universe = (1 << n) - 1
    adjacency = []
    for b, qs in records:
        bad = 0
        for triple in combinations(points(b), 3):
            bad |= old_rows[mask(triple)]
        for q in qs:
            bad |= q_bad[q]
        adjacency.append(universe & ~bad)
    graph_digest = sha256()
    width = (n + 7) // 8
    edges = 0
    triangles = 0
    triangle_witness = None
    for i, row in enumerate(adjacency):
        require(time.monotonic() - start < 45, 'INCOMPLETE: graph time guard')
        require(not row >> i & 1, 'self-loop')
        graph_digest.update(row.to_bytes(width, 'little'))
        later = row & ~((1 << (i + 1)) - 1)
        while later:
            bit = later & -later
            j = bit.bit_length() - 1
            require(adjacency[j] >> i & 1, 'asymmetric graph')
            edges += 1
            common = row & adjacency[j] & ~((1 << (j + 1)) - 1)
            triangles += common.bit_count()
            if common and triangle_witness is None:
                triangle_witness = [i, j, (common & -common).bit_length() - 1]
            later ^= bit
    require(2 * edges == sum(row.bit_count() for row in adjacency), 'incomplete edge census')
    return adjacency, {'vertices': n, 'old_parts': len(q_records), 'edges': edges,
                       'triangles': triangles, 'triangle_witness': triangle_witness,
                       'graph_sha256': graph_digest.hexdigest(),
                       'degree_histogram': dict(sorted(Counter(row.bit_count() for row in adjacency).items())),
                       'seconds': time.monotonic() - start}


def find_clique(adjacency, target):
    start = time.monotonic()
    nodes = 0
    prunes = 0
    root_coloring = None

    def visit(candidates, chosen):
        nonlocal nodes, prunes, root_coloring
        nodes += 1
        if nodes % 512 == 0:
            require(time.monotonic() - start < 45, 'INCOMPLETE: clique time guard')
        needed = target - len(chosen)
        if not needed:
            return chosen
        if candidates.bit_count() < needed:
            return None
        remaining = candidates
        classes = []
        while remaining and len(classes) < needed:
            available = remaining
            color = []
            while available:
                bit = available & -available
                v = bit.bit_length() - 1
                remaining ^= bit
                available ^= bit
                available &= ~adjacency[v]
                color.append(v)
            classes.append(color)
        if not remaining and len(classes) < needed:
            prunes += 1
            if not chosen:
                root_coloring = classes
            return None
        while candidates:
            bit = candidates & -candidates
            v = bit.bit_length() - 1
            candidates ^= bit
            answer = visit(candidates & adjacency[v], chosen + [v])
            if answer is not None:
                return answer
            if candidates.bit_count() < needed:
                break
        return None

    witness = visit((1 << len(adjacency)) - 1, [])
    return witness, {'target': target, 'nodes': nodes, 'color_prunes': prunes,
                     'root_colors': None if root_coloring is None else len(root_coloring),
                     'root_color_sizes': None if root_coloring is None else [len(c) for c in root_coloring],
                     'root_coloring': root_coloring, 'witness_indices': witness,
                     'seconds': time.monotonic() - start, 'complete': True}


def normalize_triples(circles):
    """Cover all gap triples by actual generator orbits, not signatures."""
    start = time.monotonic()
    global_gens, gap_gens = generators()
    gens = global_gens + (gap_gens[-1],)
    universe = set(combinations(circles, 3))
    covered = set()
    for gaps, size in CASES:
        orbit = [gaps]
        seen = {gaps}
        for triple in orbit:
            require(time.monotonic() - start < 45, 'INCOMPLETE: normalization time guard')
            for p in gens:
                image = tuple(sorted(move(c, p) for c in triple))
                if image not in seen:
                    seen.add(image)
                    orbit.append(image)
        require(len(seen) == size and seen <= universe and not seen & covered,
                'invalid, overlapping, or incorrectly sized gap orbit')
        covered.update(seen)
    require(covered == universe and len(universe) == 50116,
            'incomplete three-gap normalization')
    return {'unordered_gap_triples': len(universe), 'orbits': len(CASES)}


def enumerate_fixed(circles, fixed=15):
    """Prune compatibility with the fixed word before and during the CSP."""
    start = time.monotonic()
    circle_set = set(circles)
    require(fixed.bit_count() == 4 and not any(c & fixed == fixed for c in circles),
            'fixed four-set is contained or has wrong weight')
    gaps = {c for c in circles if (c & fixed).bit_count() >= 3}
    require(len(gaps) == 4, 'incorrect fixed-word gap count')
    records = []
    reasons = Counter()
    eligible = Counter()
    histogram = Counter()
    nodes = 0
    for pts in combinations(range(17), 5):
        require(time.monotonic() - start < 45, 'INCOMPLETE: fixed-word time guard')
        b = mask(pts)
        if b in circle_set:
            reasons['design_circle'] += 1
            continue
        if (b & fixed).bit_count() > 2:
            reasons['fixed_word_conflict'] += 1
            continue
        meetings = [(c, (b & c).bit_count()) for c in circles if c not in gaps]
        if any(n >= 4 for c, n in meetings):
            reasons['nongap_four_point_circle'] += 1
            continue
        blockers = [c for c, n in meetings if n == 3]
        options = [[c ^ (1 << p) for p in pts if c >> p & 1
                    and ((c ^ (1 << p)) & fixed).bit_count() <= 1]
                   for c in blockers]
        selected = []
        before = len(records)

        def visit(remaining):
            nonlocal nodes
            nodes += 1
            if nodes % 1024 == 0:
                require(time.monotonic() - start < 45, 'INCOMPLETE: fixed-word time guard')
                require(len(records) <= 40000, 'INCOMPLETE: fixed-word record guard')
            if not remaining:
                records.append((b, tuple(sorted(selected))))
                return
            filtered = [[q for q in qs if all((q & r).bit_count() <= 1 for r in selected)]
                        for qs in remaining]
            i = min(range(len(filtered)), key=lambda j: len(filtered[j]))
            if not filtered[i]:
                return
            tail = filtered[:i] + filtered[i + 1:]
            for q in filtered[i]:
                selected.append(q)
                visit(tail)
                selected.pop()

        visit(options)
        eligible[len(blockers)] += 1
        histogram[(len(blockers), len(records) - before)] += 1
    records.sort()
    require(sum(reasons.values()) + sum(eligible.values()) == 6188,
            'incorrect fixed-word old-set coverage')
    require(len(set(records)) == len(records), 'duplicate fixed-word record')
    return records, {'fixed_old_four_set': fixed, 'gaps': sorted(gaps),
                     'records': len(records), 'records_sha256': digest(records),
                     'rejection_reasons': dict(sorted(reasons.items())),
                     'eligible_outsiders': {str(k): v for k, v in sorted(eligible.items())},
                     'solution_counts': [{'mandatory_circles': k[0], 'assignments': k[1],
                                         'outsiders': v} for k, v in sorted(histogram.items())]}


def compact_graph(summary):
    return {k: summary[k] for k in ('vertices', 'old_parts', 'edges', 'triangles',
                                     'graph_sha256')}


def generate():
    circles, _ = classical_design()
    norm = normalize_triples(circles)
    cases = []
    for case_id, (gaps, size) in enumerate(CASES):
        records, census = enumerate_masks(circles, gaps)
        adjacency, summary = graph(records)
        indices, coverage = find_clique(adjacency, 4)
        require(coverage['complete'] and indices is None, 'four-clique found or search incomplete')
        compact = compact_graph(summary)
        compact['four_cliques'] = 0
        cases.append({'case': case_id, 'gap_circles': list(gaps), 'orbit_size': size,
                      'enumeration': census, 'graph': compact})
    records, census = enumerate_fixed(circles)
    adjacency, summary = graph(records)
    indices, coverage = find_clique(adjacency, 5)
    colors = coverage['root_coloring']
    require(indices is None and coverage['complete'] and colors is not None
            and len(colors) == 4, 'fixed-word graph lacks its four-color bound')
    certificate = {'records_sha256': census['records_sha256'],
                   'graph_sha256': summary['graph_sha256'],
                   'target_clique': 5, 'colors': colors}
    raw = (json.dumps(certificate, separators=(',', ':')) + '\n').encode()
    require(raw == Path(__file__).with_name('single_word_colors.json').read_bytes(),
            'four-color fixture differs from the exact regenerated certificate')
    single = {'enumeration': census, 'graph': compact_graph(summary),
              'colors': len(colors), 'color_sizes': [len(c) for c in colors],
              'certificate_sha256': sha256(raw).hexdigest(), 'certificate_bytes': len(raw)}
    return {'design_blocks': len(circles), 'design_sha256': digest(circles),
            'normalization': norm, 'cases': cases, 'single_word': single}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = generate()
    if args.check is not None:
        expected = json.loads(args.check.read_text())
        require(result == expected['generator'], 'three-gap replay manifest mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
