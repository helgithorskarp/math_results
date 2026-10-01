#!/usr/bin/env python3
"""Produce a finite Petersen incidence cover and static and shallow support-deletion certificates.

No solver, branching search, host automorphism, or outside degree-floor theorem
is used. Normal mode independently regenerates and compares the frozen output.
"""
import argparse
from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement, permutations, product
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LABELS = list(combinations(range(5), 2))
A = (1 << 10) - 1
P = [sum(1 << j for j, y in enumerate(LABELS) if set(x).isdisjoint(y))
     for x in LABELS]
STARS = [sum(1 << i for i, x in enumerate(LABELS) if t in x) for t in range(5)]
RED = [(i, j) for i, j in combinations(range(10), 2) if P[i] >> j & 1]
BLUE = [(i, j) for i, j in combinations(range(10), 2) if not P[i] >> j & 1]
DELTAS = (2, 1, 1) + (0,) * 8


def require(ok, message):
    if not ok:
        raise ValueError(message)

def canonical_json(value):
    normalized = json.loads(json.dumps(value))  # JSON object keys are strings.
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"))

def digest(value):
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()

def key_rows(key):
    z, w, q, highs, mu = key
    return [z, w, q] + list(highs) + [s for s, m in zip(STARS, mu) for _ in range(m)]

def word_pool(delta):
    result = set()
    for z in range(1024):
        k = z.bit_count()
        if not 4 + delta <= k <= 8:
            continue
        c = A ^ z
        if any(k - delta > 8 - (P[i] & c).bit_count()
               for i in range(10) if c >> i & 1):
            continue
        if any((P[i] & z).bit_count() < k - 7
               for i in range(10) if z >> i & 1):
            continue
        if any(k + delta + (P[i] & c).bit_count() + (P[j] & c).bit_count() > 12
               for i, j in RED if z >> i & 1 and z >> j & 1):
            continue
        result.add(z)
    return result

def census():
    stats = Counter()
    pack = [sum(((z >> i) & 1) << (2 * i) for i in range(10)) for z in range(1024)]
    red_masks = [sum(1 << t for t, (i, j) in enumerate(RED)
                     if z >> i & 1 and z >> j & 1) for z in range(1024)]
    blue_masks = [tuple(t for t, (i, j) in enumerate(BLUE)
                        if z >> i & 1 and z >> j & 1) for z in range(1024)]
    low8 = sorted(word_pool(2))
    low9 = sorted(z for z in word_pool(1) if z.bit_count() <= 7)
    require(Counter(z.bit_count() for z in low8) == {6: 210, 7: 120, 8: 45}, 'low8 size pool')
    require(Counter(z.bit_count() for z in low9) == {5: 252, 6: 210, 7: 120}, 'low9 size pool')
    pairs = defaultdict(list)
    for w, q in combinations_with_replacement(low9, 2):
        if w.bit_count() + q.bit_count() > 12:
            continue
        stats['low9_pairs_within_budget'] += 1
        if red_masks[w] & red_masks[q]:
            continue
        pairs[pack[w] + pack[q]].append((w, q, red_masks[w] | red_masks[q]))
        stats['low9_pairs_red_capped'] += 1
    stats['low9_pair_column_vectors'] = len(pairs)
    full = {k: [z for z in range(1024) if z.bit_count() == k
                and all((P[i] & (A ^ z)).bit_count() <= 1
                        for i in range(10) if not z >> i & 1)] for k in (5, 6)}
    choices = [()] + [(z,) for z in full[5]] + [(z,) for z in full[6]]
    choices += list(combinations_with_replacement(full[5], 2))
    keys = set()
    for highs in choices:
        used = 0
        for h in highs:
            if used & red_masks[h]:
                break
            used |= red_masks[h]
        else:
            stats['high_large_multisets'] += 1
            for mu in product(range(3), repeat=5):
                if sum(mu) + len(highs) != 8:
                    continue
                stats['high_multiplicity_choices'] += 1
                highrows = list(highs) + [s for s, m in zip(STARS, mu) for _ in range(m)]
                residual = [5 - sum(h >> i & 1 for h in highrows) for i in range(10)]
                if any(not 0 <= r <= 3 for r in residual):
                    continue
                high_blue = [sum(bool(h >> i & 1 and h >> j & 1) for h in highrows)
                             for i, j in BLUE]
                if max(high_blue) > 3:
                    continue
                stats['residual_vectors'] += 1
                vector = sum(r << (2 * i) for i, r in enumerate(residual))
                absent = sum(1 << i for i, r in enumerate(residual) if r == 0)
                forced = sum(1 << i for i, r in enumerate(residual) if r == 3)
                for z in low8:
                    if z & absent or z & forced != forced:
                        continue
                    stats['low8_residual_assignments'] += 1
                    if used & red_masks[z]:
                        continue
                    for w, q, pair_mask in pairs.get(vector - pack[z], ()):
                        stats['exact_column_joins'] += 1
                        if pair_mask & (used | red_masks[z]):
                            continue
                        counts = high_blue.copy()
                        for mask in (z, w, q):
                            for t in blue_masks[mask]:
                                counts[t] += 1
                        if max(counts) > 3:
                            continue
                        key = (z, w, q, tuple(sorted(highs)), tuple(mu))
                        require(key not in keys, 'duplicate full-column record')
                        require(len(key_rows(key)) == 11, 'wrong outside count')
                        keys.add(key)
    patterns = Counter((z.bit_count(), *sorted((w.bit_count(), q.bit_count())),
                        tuple(h.bit_count() for h in highs)) for z, w, q, highs, mu in keys)
    report = {'deficits': DELTAS, 'complete': True, 'incidence_records': len(keys),
              'incidence_sha256': digest(sorted(keys)),
              'census': dict(sorted(stats.items())),
              'patterns': [{'sizes': p, 'records': n} for p, n in sorted(patterns.items())],
              'low8_word_sizes': dict(sorted(Counter(z.bit_count() for z in low8).items())),
              'low9_word_sizes': dict(sorted(Counter(z.bit_count() for z in low9).items())),
              'full_large_sizes': {k: len(v) for k, v in full.items()}}
    return keys, report

def transformations():
    position = {x: i for i, x in enumerate(LABELS)}
    output = []
    for permutation in permutations(range(5)):
        mapping = [position[tuple(sorted(permutation[t] for t in x))] for x in LABELS]
        words = [sum(1 << mapping[i] for i in range(10) if z >> i & 1)
                 for z in range(1024)]
        output.append((permutation, words))
    return output

def transformed(key, permutation, words):
    z, w, q, highs, mu = key
    moved_mu = [0] * 5
    for t in range(5):
        moved_mu[permutation[t]] = mu[t]
    pair = sorted((words[w], words[q]))
    return words[z], pair[0], pair[1], tuple(sorted(words[h] for h in highs)), tuple(moved_mu)


def domains(rows):
    """Decomposed A/B page counts; verifier uses literal 22-vertex sets."""
    result = []
    outside = (1 << len(rows)) - 1
    for b, (z, delta) in enumerate(zip(rows, DELTAS)):
        degree = z.bit_count() - delta
        require(0 <= degree < len(rows), "outside degree out of range")
        rest = outside ^ (1 << b)
        columns = [sum(1 << c for c in range(len(rows)) if c != b and rows[c] >> i & 1)
                   for i in range(10)]
        accepted = []
        for picked in combinations([c for c in range(len(rows)) if c != b], degree):
            star = sum(1 << c for c in picked)
            if any((P[i] & (A ^ z)).bit_count() + (star & (rest ^ columns[i])).bit_count() > 3
                   for i in range(10) if not z >> i & 1):
                continue
            if any(z.bit_count() - 1 - (P[i] & z).bit_count()
                   + (columns[i] & (rest ^ star)).bit_count() > 6
                   for i in range(10) if z >> i & 1):
                continue
            accepted.append(star)
        result.append(sorted(accepted))
    return result

def compatible(rows, b, x, c, y):
    if (x >> c & 1) != (y >> b & 1):
        return False
    if x >> c & 1:
        return 10 - (rows[b] | rows[c]).bit_count() + (x & y).bit_count() <= 3
    outside = (1 << len(rows)) - 1
    bx = outside ^ (1 << b) ^ x
    by = outside ^ (1 << c) ^ y
    return 1 + (rows[b] & rows[c]).bit_count() + (bx & by).bit_count() <= 6

def unsupported_groups(rows, target, target_stars, support_domains):
    groups = {}
    for star in target_stars:
        for support in range(11):
            if support != target and not any(compatible(rows, target, star, support, value)
                                              for value in support_domains[support]):
                groups.setdefault(support, []).append(star)
                break
    return groups


def shallow_trace(rows, initial):
    # Restrict two domains by initial unsupported stars. Then try a complete
    # obstruction at a third point using these sound restricted supports.
    for first, second in combinations(range(11), 2):
        current = [list(stars) for stars in initial]
        steps = []
        for target in (first, second):
            groups = unsupported_groups(rows, target, initial[target], initial)
            removed = {star for values in groups.values() for star in values}
            current[target] = [star for star in initial[target] if star not in removed]
            for support, values in sorted(groups.items()):
                steps.append({'point': target, 'against': support, 'remove': sorted(values)})
        require(all(current), 'static failure did not retain a supported star')
        for target in range(11):
            if target in (first, second):
                continue
            groups = unsupported_groups(rows, target, initial[target], current)
            if {star for values in groups.values() for star in values} != set(initial[target]):
                continue
            for support, values in sorted(groups.items()):
                steps.append({'point': target, 'against': support, 'remove': sorted(values)})
            return {'type': 'arc_deletion', 'empty_point': target, 'steps': steps}
    raise ValueError('unexcluded incidence: no complete shallow certificate produced')


def exclusion(rows, stars):
    for b, domain in enumerate(stars):
        if not domain:
            return {"type": "empty_star", "point": b}
    # Use the complete initial domains only. Every star of one point must
    # lack pairwise support somewhere; no propagation or domain update.
    for b, domain in enumerate(stars):
        groups = {}
        for x in domain:
            for c in range(11):
                if c != b and not any(compatible(rows, b, x, c, y) for y in stars[c]):
                    groups.setdefault(c, []).append(x)
                    break
            else:
                break
        else:
            return {"type": "star_pair_cover", "point": b,
                    "covers": [{"against": c, "stars": sorted(xs)}
                               for c, xs in sorted(groups.items())]}
    return shallow_trace(rows, stars)

def make_certificate():
    keys, result = census()
    maps = transformations()
    covered = set()
    entries = []
    histogram = Counter()
    for key in sorted(keys):
        if key in covered:
            continue
        orbit = {transformed(key, p, words) for p, words in maps}
        require(key == min(orbit), 'nonminimum orbit representative')
        require(orbit <= keys and not covered.intersection(orbit), 'invalid or overlapping orbit')
        covered.update(orbit)
        rows = key_rows(key)
        require(len(rows) == 11, 'wrong outside order')
        stars = domains(rows)
        entries.append({'key': key, 'orbit_size': len(orbit),
                        'domain_sizes': [len(domain) for domain in stars],
                        'domains_sha256': digest(stars), 'exclusion': exclusion(rows, stars)})
        histogram[len(orbit)] += 1
    require(covered == keys, 'incomplete raw orbit cover')
    certificate = {'schema': 1, 'order': 22, 'red_page_cap': 3, 'blue_page_cap': 6,
                   'outside_deficits': DELTAS, 'local_graph': 'KG(5,2)',
                   'incidence_records': len(keys), 'entries': entries}
    result.update({'orbits': len(entries), 'orbit_size_histogram': dict(sorted(histogram.items())),
                   'exclusion_types': dict(sorted(Counter(e['exclusion']['type'] for e in entries).items())),
                   'star_pair_covers': sum(len(e['exclusion'].get('covers', [])) for e in entries),
                   'unsupported_stars': sum(len(c['stars']) for e in entries for c in e['exclusion'].get('covers', [])),
                   'arc_steps': sum(len(e['exclusion'].get('steps', [])) for e in entries),
                   'arc_removed_stars': sum(len(s['remove']) for e in entries for s in e['exclusion'].get('steps', [])),
                   'certificate_sha256': digest(certificate)})
    return certificate, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--derive", action="store_true", help="report without frozen-summary comparison")
    parser.add_argument("--output", type=Path, help="explicit destination for regenerated certificate")
    args = parser.parse_args()
    certificate, result = make_certificate()
    if not args.derive:
        require(canonical_json(certificate) == canonical_json(json.loads((HERE / "certificate.json").read_text())),
                "regenerated certificate mismatch")
        require(canonical_json(result) == canonical_json(json.loads((HERE / "expected.json").read_text())["producer"]),
                "producer expected-summary mismatch")
    if args.output is not None:
        args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
