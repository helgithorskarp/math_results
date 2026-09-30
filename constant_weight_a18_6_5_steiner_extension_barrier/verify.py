"""Independent set enumeration, checked symmetry coverage, direct pair proof.

Does not import generate.py or accept its enumerated records or graph. It
shares only the explicit geometry definition and compact expected hashes.
The finite completeness and low-gap reduction are explained in PROOF.md.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import time

from geometry import classical_design, generators, mask, points, require


def digest(records):
    return sha256((json.dumps(records, separators=(',', ':')) + '\n').encode()).hexdigest()


def enumerate_sets(circles, gap):
    start = time.monotonic()
    design = tuple(frozenset(points(c)) for c in circles)
    circle_set = set(design)
    gap_set = frozenset(points(gap))
    records = []
    histogram = Counter()
    eligible = Counter()
    tested = 0
    for pts in combinations(range(17), 5):
        require(time.monotonic() - start < 45, 'INCOMPLETE: checker generation guard')
        b = frozenset(pts)
        if b in circle_set:
            continue
        tested += 1
        blockers = [c for c in design if c != gap_set and len(c & b) >= 3]
        if any(len(c & b) >= 4 for c in blockers):
            continue
        # Enumerate all four-subsets of every mandatory circle directly.
        options = [tuple(frozenset(q) for q in combinations(sorted(c), 4)
                         if len(frozenset(q) & b) <= 2) for c in blockers]
        require(all(len(qs) == 3 for qs in options), 'invalid direct option count')
        # A fixed order and pair ownership give a different enumeration
        # from the generator's dynamically filtered direct intersections.
        paired_options = [[(q, frozenset(combinations(sorted(q), 2))) for q in qs]
                          for qs in options]
        selected = []
        before = len(records)

        def visit(i, owned_pairs):
            if i == len(paired_options):
                records.append((mask(b), tuple(sorted(mask(q) for q in selected))))
                return
            for q, pairs in paired_options[i]:
                if pairs.isdisjoint(owned_pairs):
                    selected.append(q)
                    visit(i + 1, owned_pairs | pairs)
                    selected.pop()

        visit(0, frozenset())
        count = len(records) - before
        eligible[len(blockers)] += 1
        histogram[(len(blockers), count)] += 1
    records.sort()
    require(len(set(records)) == len(records) and tested == 6120,
            'incorrect universe or duplicate records')
    census = {'eligible_outsiders': {str(k): v for k, v in sorted(eligible.items())},
              'solution_counts': [{'blockers': k[0], 'solutions': k[1], 'outsiders': n}
                                  for k, n in sorted(histogram.items())],
              'records': len(records), 'records_sha256': digest(records)}
    return records, census


def check_symmetries(records, circles, gap):
    """Check actual permutations, every record orbit, and circle transitivity."""
    global_gens, gap_gens = generators()
    design = frozenset(frozenset(points(c)) for c in circles)
    gap_set = frozenset(points(gap))

    def image(s, p):
        return frozenset(p[x] for x in s)

    for p in global_gens + gap_gens:
        require(sorted(p) == list(range(17)), 'malformed permutation')
        require(frozenset(image(c, p) for c in design) == design,
                'permutation is not a design automorphism')
    require(all(image(gap_set, p) == gap_set for p in gap_gens),
            'gap generator fails to fix the gap')
    group = [tuple(range(17))]
    group_seen = set(group)
    for p in group:
        for g in gap_gens:
            q = tuple(g[p[x]] for x in range(17))
            if q not in group_seen:
                group_seen.add(q)
                group.append(q)
    circle_orbit = [gap_set]
    circle_seen = {gap_set}
    for c in circle_orbit:
        for p in global_gens:
            d = image(c, p)
            if d not in circle_seen:
                circle_seen.add(d)
                circle_orbit.append(d)
    require(circle_seen == set(design), 'gap-circle transitivity is incomplete')
    set_records = [(frozenset(points(b)), tuple(frozenset(points(q)) for q in qs))
                   for b, qs in records]
    position = {r: i for i, r in enumerate(records)}
    seen = set()
    representatives = []
    orbit_sizes = []
    for i in range(len(records)):
        if i in seen:
            continue
        representatives.append(i)
        orbit = [i]
        orbit_seen = {i}
        for j in orbit:
            b, qs = set_records[j]
            for p in gap_gens:
                r = (mask(image(b, p)), tuple(sorted(mask(image(q, p)) for q in qs)))
                require(r in position, 'enumerated records are not symmetry closed')
                k = position[r]
                if k not in orbit_seen:
                    orbit_seen.add(k)
                    orbit.append(k)
        require(not seen & orbit_seen, 'record orbits overlap')
        seen.update(orbit_seen)
        orbit_sizes.append(len(orbit))
    require(len(seen) == len(records), 'incomplete record orbit coverage')
    # Direct intersections, independent of the incidence-bitset graph.
    counts = Counter()
    for i in representatives:
        b, qs = set_records[i]
        for c, rs in set_records:
            counts['comparisons'] += 1
            if len(b & c) > 2:
                counts['old_incompatibility'] += 1
                continue
            if any(q != r and len(q & r) > 1 for q in qs for r in rs):
                counts['replacement_incompatibility'] += 1
                continue
            raise ValueError('compatible records contradict the no-edge claim')
    return {'verified_gap_stabilizer_order': len(group),
            'gap_circle_orbit': len(circle_seen), 'record_orbits': len(representatives),
            'orbit_size_histogram': {str(k): v for k, v in sorted(Counter(orbit_sizes).items())},
            'direct_pair_counts': dict(sorted(counts.items())), 'compatibility_edges': 0}


def check_witness(circles, path):
    data = json.loads(path.read_text())
    b = data['outsider']
    qs = data['old_parts']
    require(isinstance(b, int) and 0 <= b < (1 << 17) and b.bit_count() == 5,
            'malformed outsider')
    require(b not in circles, 'the outsider is a design circle')
    require(len(qs) == 10 and len(set(qs)) == 10, 'incorrect witness replacement count')
    require(all(isinstance(q, int) and 0 <= q < (1 << 17) and q.bit_count() == 4 for q in qs),
            'malformed old part')
    blocked = {c for c in circles if (c & b).bit_count() >= 3}
    owners = []
    for q in qs:
        cs = [c for c in circles if c & q == q]
        require(len(cs) == 1, 'witness old part is not uniquely contained')
        owners.extend(cs)
    require(len(blocked) == 10 and set(owners) == blocked and len(set(owners)) == 10,
            'witness replacements do not match all blockers')
    words = set(circles) - blocked | {b} | {q | (1 << 17) for q in qs}
    require(len(words) == 69 and all(w.bit_count() == 5 for w in words),
            'incorrect witness size or weight')
    require(all((u & v).bit_count() <= 2 for u, v in combinations(words, 2)),
            'witness is not a packing')
    degree_hist = Counter(sum(w >> p & 1 for w in words) for p in range(18))
    return {'size': len(words), 'old_outsiders': 1, 'contained_new_words': 10,
            'noncontained_new_words': 0,
            'degree_histogram': {str(k): v for k, v in sorted(degree_hist.items())},
            'words_sha256': digest(sorted(words))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--witness', type=Path, default=Path(__file__).with_name('witness69.json'))
    args = parser.parse_args()
    expected = json.loads(args.expected.read_text())
    circles, gap = classical_design()
    records, census = enumerate_sets(circles, gap)
    generator = expected['generator']
    for k, v in census.items():
        require(generator[k] == v, 'independent universe manifest mismatch: ' + k)
    require(generator['design_sha256'] == digest(circles), 'design hash mismatch')
    require(generator['gap_circle'] == gap, 'gap fixture mismatch')
    verification = check_symmetries(records, circles, gap)
    require(verification == expected['verifier'], 'independent no-edge manifest mismatch')
    witness = check_witness(circles, args.witness)
    require(witness == expected['witness'], 'witness manifest mismatch')
    print(json.dumps({'verified_records': len(records), 'record_orbits': verification['record_orbits'],
                      'compatibility_edges': 0, 'at_most_three_outsiders_maximum': 69,
                      'minimum_old_outsiders_for_70': 4, 'witness': witness}, sort_keys=True))


if __name__ == '__main__':
    main()
