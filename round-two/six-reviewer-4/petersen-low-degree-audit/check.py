#!/usr/bin/env python3
"""Independent full-column join and synchronous Petersen completion exclusion.

Standard library only. No researcher module, quotient forms, residual low-row
assignment generator, supplied orbit representative, or supplied deletion trace
is used to prove the rooted finite statement.
"""
import argparse
from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement, product
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LABELS = tuple(combinations(range(5), 2))
INDEX = {p: i for i, p in enumerate(LABELS)}
P = tuple(sum(1 << j for j, q in enumerate(LABELS)
              if not (set(p) & set(q))) for p in LABELS)
ALL = 1023
PAIRS = tuple(combinations(range(10), 2))
GROUND_STARS = tuple(sum(1 << i for i, p in enumerate(LABELS) if t in p)
                     for t in range(5))
DEFICITS = (3, 1) + (0,) * 9


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def indices(mask, n):
    return tuple(i for i in range(n) if mask & (1 << i))


def rows_of(key):
    z, w, large, mu = key
    return (z, w) + tuple(large) + tuple(s for s, m in zip(GROUND_STARS, mu)
                                         for _ in range(m))


def low_ok(z, delta):
    k, c = z.bit_count(), ALL ^ z
    return (k >= 4 + delta
            and all(k - delta + (P[i] & c).bit_count() <= 8 for i in indices(c, 10))
            and all(k - 1 - (P[i] & z).bit_count() <= 6 for i in indices(z, 10))
            and all(k + delta + (P[i] & c).bit_count() + (P[j] & c).bit_count() <= 12
                    for i, j in PAIRS if P[i] & (1 << j) and z & (1 << i) and z & (1 << j)))


def complete_census():
    """Join ten-component full-row vectors directly to both fixed-tag low rows.

    Ten base-16 digits encode exact column counts; each is <=11, so sums
    have no carry. No quotient or recovery theorem is needed for this join.
    """
    columns = tuple(sum((1 << (4 * i)) for i in indices(z, 10)) for z in range(1024))
    target = 5 * columns[ALL]
    low = {d: tuple(z for z in range(1024) if z.bit_count() <= 8 and low_ok(z, d))
           for d in (3, 1)}
    high = {k: tuple(z for z in range(1024) if z.bit_count() == k
                    and all((P[i] & (ALL ^ z)).bit_count() <= 1
                            for i in indices(ALL ^ z, 10))) for k in (5, 6)}
    large_choices = [()] + [(z,) for z in high[5] + high[6]]
    large_choices += list(combinations_with_replacement(high[5], 2))
    bank = defaultdict(list)
    bank_count = 0
    for large in large_choices:
        for mu in product(range(3), repeat=5):
            if sum(mu) + len(large) != 9:
                continue
            vector = sum(columns[z] for z in large)
            vector += sum(m * columns[s] for s, m in zip(GROUND_STARS, mu))
            bank[vector].append((tuple(sorted(large)), mu))
            bank_count += 1
    keys = set()
    joined = 0
    for z in low[3]:
        for w in low[1]:
            for large, mu in bank.get(target - columns[z] - columns[w], ()):
                joined += 1
                key = (z, w, large, mu)
                rows = rows_of(key)
                need(len(rows) == 11, "outside row count")
                need(all(sum(bool(q & (1 << i)) for q in rows) == 5 for i in range(10)),
                     "full-column join lost an equation")
                if all(sum(bool(q & (1 << i) and q & (1 << j)) for q in rows)
                       <= (1 if P[i] & (1 << j) else 3) for i, j in PAIRS):
                    need(key not in keys, "duplicate joined incidence")
                    keys.add(key)
    return keys, {"full_vector_bank_records": bank_count,
                  "distinct_full_vectors": len(bank), "full_column_joins": joined,
                  "low_word_counts": {str(d): dict(Counter(z.bit_count() for z in low[d]))
                                      for d in (3, 1)},
                  "large_word_counts": {str(k): len(high[k]) for k in (5, 6)}}


def relabelings():
    """Four adjacent ground transpositions generate S5; use orbit BFS."""
    result = []
    for t in range(4):
        perm = list(range(5)); perm[t], perm[t + 1] = perm[t + 1], perm[t]
        image = tuple(INDEX[tuple(sorted(perm[a] for a in p))] for p in LABELS)
        need(all(bool(P[i] & (1 << j)) == bool(P[image[i]] & (1 << image[j]))
                 for i, j in PAIRS), "generator does not preserve actual local graph")
        words = tuple(sum(1 << image[i] for i in indices(z, 10)) for z in range(1024))
        need(all(words[words[z]] == z for z in range(1024)), "generator not involutive")
        need(all(words[GROUND_STARS[i]] == GROUND_STARS[perm[i]] for i in range(5)),
             "ground-star transport")
        result.append((tuple(perm), words))
    return tuple(result)


def orbits(keys):
    maps = relabelings()
    remaining = set(keys)
    result = []
    while remaining:
        representative = min(remaining)
        seen = {representative}; todo = [representative]
        while todo:
            z, w, large, mu = todo.pop()
            for perm, words in maps:
                moved = tuple(mu[perm[i]] for i in range(5))  # each generator is involutive
                image = (words[z], words[w], tuple(sorted(words[q] for q in large)), moved)
                need(image in keys, "orbit image missing from complete incidence domain")
                if image not in seen:
                    seen.add(image); todo.append(image)
        need(seen <= remaining, "orbit overlap")
        remaining.difference_update(seen)
        result.append((representative, seen))
    need(set().union(*(o for _, o in result)) == keys, "incomplete orbit cover")
    return result


class Frame:
    """Actual whole-vertex neighborhoods as arbitrary-precision binary integers."""
    def __init__(self, local, rows):
        self.a, self.n = len(local), len(rows)
        self.offset = self.a + 1
        self.universe = (1 << (self.offset + self.n)) - 1
        self.rows = tuple(rows)
        self.a_red = tuple(1 | (local[i] << 1)
                           | sum(1 << (self.offset + b) for b, z in enumerate(rows)
                                 if not z & (1 << i)) for i in range(self.a))
        self.a_blue = tuple(self.universe ^ r ^ (1 << (i + 1))
                            for i, r in enumerate(self.a_red))
        self.base_b_red = tuple((((1 << self.a) - 1) ^ z) << 1 for z in rows)

    def neighborhoods(self, b, star):
        red = self.base_b_red[b] | (star << self.offset)
        return red, self.universe ^ red ^ (1 << (self.offset + b))

    def ab_pages(self, b, star, i):
        red, blue = self.neighborhoods(b, star)
        return ((blue & self.a_blue[i]).bit_count() if self.rows[b] & (1 << i)
                else (red & self.a_red[i]).bit_count())

    def pair_pages(self, b, x, c, y):
        red = bool(x & (1 << c))
        if red != bool(y & (1 << b)):
            return None
        rb, bb = self.neighborhoods(b, x); rc, bc = self.neighborhoods(c, y)
        return red, ((rb & rc) if red else (bb & bc)).bit_count()

    def compatible(self, b, x, c, y):
        result = self.pair_pages(b, x, c, y)
        return result is not None and result[1] <= (3 if result[0] else 6)

    def domains(self, deficits):
        need(len(deficits) == self.n, "deficiency vector length")
        result = []
        for b, (z, delta) in enumerate(zip(self.rows, deficits)):
            degree = z.bit_count() - delta
            need(0 <= degree < self.n, "impossible prescribed outside degree")
            pool = []
            for choice in combinations(tuple(c for c in range(self.n) if c != b), degree):
                star = sum(1 << c for c in choice)
                if all(self.ab_pages(b, star, i) <= (6 if z & (1 << i) else 3)
                       for i in range(self.a)):
                    pool.append(star)
            result.append(tuple(sorted(pool)))
        return tuple(result)


def synchronous_exclusion(frame, domains):
    """Remove all unsupported stars simultaneously; no supplied deletion order."""
    if any(not d for d in domains):
        return {"type": "initial_empty", "empty_point": next(i for i, d in enumerate(domains) if not d),
                "rounds": 0, "removals": 0, "trace": []}
    supports = {}
    for b in range(frame.n):
        for i, x in enumerate(domains[b]):
            supports[b, i] = tuple(sum(1 << j for j, y in enumerate(domains[c])
                                       if frame.compatible(b, x, c, y)) if b != c else 0
                                   for c in range(frame.n))
    current = [(1 << len(d)) - 1 for d in domains]
    trace = []
    while all(current):
        following = current.copy(); round_trace = []
        for b in range(frame.n):
            removed = []
            for i in indices(current[b], len(domains[b])):
                c = next((c for c in range(frame.n) if c != b and not (supports[b, i][c] & current[c])), None)
                if c is not None:
                    following[b] ^= 1 << i; removed.append((domains[b][i], c))
            if removed:
                round_trace.append((b, removed))
        need(following != current, "unexcluded incidence at a genuine fixed point")
        trace.append(round_trace); current = following
    return {"type": "synchronous_empty", "empty_point": next(i for i, d in enumerate(current) if not d),
            "rounds": len(trace), "removals": sum(len(r) for batch in trace for _, r in batch),
            "trace": trace}


def geometry_checks():
    need(all(p.bit_count() == 3 for p in P), "local cubic degrees")
    need(all((P[i] & P[j]).bit_count() == (0 if P[i] & (1 << j) else 1)
             for i, j in PAIRS), "local common-neighbor counts")
    independent = tuple(z for z in range(1024) if z.bit_count() == 4
                        and all(not (P[i] & z) for i in indices(z, 10)))
    need(set(independent) == set(GROUND_STARS), "independent four-set classification")
    four = [z for z in range(1024) if z.bit_count() >= 8]
    def cut_score(z, delta):
        c = ALL ^ z
        return max(z.bit_count() + delta + (P[i] & c).bit_count() + (P[j] & c).bit_count()
                   for i, j in PAIRS if P[i] & (1 << j) and z & (1 << i) and z & (1 << j))
    need(all(cut_score(z, 4) > 12 for z in four), "degree-six row survives two-column cut")
    need(all(cut_score(z, 3) > 12 for z in range(1024) if z.bit_count() >= 9),
         "large degree-seven row survives two-column cut")
    need(all(not low_ok(z, 3) for z in range(1024) if z.bit_count() >= 9),
         "large degree-seven row survives")
    eight = [ALL ^ z for z in range(1024) if z.bit_count() == 8 and low_ok(z, 3)]
    need(set(eight) == {((1 << i) | (1 << j)) for i, j in PAIRS if P[i] & (1 << j)},
         "degree-seven size-eight complements")
    return {"degree_six_words_excluded": len(four), "large_degree_seven_words_excluded": 11,
            "degree_seven_size_eight_complements": len(eight), "independent_four_sets": len(independent)}


def small_whole_graph_controls():
    # Exhaust all 1024 six-point graphs with N(0)={1,2,3}, B={4,5}.
    free = tuple(combinations(range(1, 6), 2)); checks = asymmetric = 0
    for bits in range(1 << len(free)):
        adj = [[False] * 6 for _ in range(6)]
        for i in (1, 2, 3): adj[0][i] = adj[i][0] = True
        for t, (i, j) in enumerate(free): adj[i][j] = adj[j][i] = bool(bits & (1 << t))
        local = tuple(sum(1 << j for j in range(3) if adj[i + 1][j + 1]) for i in range(3))
        rows = tuple(sum(1 << i for i in range(3) if not adj[b + 4][i + 1]) for b in range(2))
        actual = tuple(sum(1 << c for c in range(2) if adj[b + 4][c + 4]) for b in range(2))
        frame = Frame(local, rows)
        for b in range(2):
            for i in range(3):
                u, v = b + 4, i + 1; color = adj[u][v]
                pages = sum(adj[u][t] == color and adj[v][t] == color for t in range(6) if t not in (u, v))
                need(frame.ab_pages(b, actual[b], i) == pages, "whole-graph A/B control")
                checks += 1
        color = adj[4][5]
        pages = sum(adj[4][t] == color and adj[5][t] == color for t in range(4))
        need(frame.pair_pages(0, actual[0], 1, actual[1]) == (color, pages), "whole-graph B/B control")
        need(frame.pair_pages(0, actual[0] ^ 2, 1, actual[1]) is None, "asymmetric star accepted")
        checks += 1; asymmetric += 1
    return {"whole_graphs": 1024, "literal_spine_checks": checks, "asymmetric_stars_rejected": asymmetric}


def primary_control():
    fixture = json.loads((HERE / 'primary21.json').read_text())
    need(fixture['order'] == 21, 'primary fixture order')
    edges = fixture['red_edges']
    need(len(edges) == len({tuple(e) for e in edges}) == 93, 'primary edge list')
    adj = [0] * 21
    for u, v in edges:
        need(type(u) is int and type(v) is int and 0 <= u < v < 21, 'primary edge')
        adj[u] |= 1 << v; adj[v] |= 1 << u
    blue = tuple(((1 << 21) - 1) ^ a ^ (1 << i) for i, a in enumerate(adj))
    red_pages = [(adj[u] & adj[v]).bit_count() for u, v in combinations(range(21), 2) if adj[u] & (1 << v)]
    blue_pages = [(blue[u] & blue[v]).bit_count() for u, v in combinations(range(21), 2) if not adj[u] & (1 << v)]
    need(max(red_pages) == 3 and max(blue_pages) == 6, 'primary ordinary book caps')
    roots = [i for i, a in enumerate(adj) if a.bit_count() == 10]
    need(len(roots) == 1, 'primary degree-ten root')
    root = roots[0]; a = indices(adj[root], 21); b = indices(blue[root], 21)
    local = tuple(sum(1 << j for j, v in enumerate(a) if adj[u] & (1 << v)) for u in a)
    rows = tuple(sum(1 << i for i, v in enumerate(a) if not adj[u] & (1 << v)) for u in b)
    stars = tuple(sum(1 << j for j, v in enumerate(b) if adj[u] & (1 << v)) for u in b)
    deficits = tuple(10 - adj[u].bit_count() for u in b)
    frame = Frame(local, rows); domains = frame.domains(deficits)
    need(all(stars[i] in domains[i] for i in range(10)), 'primary actual star')
    need(all(frame.compatible(i, stars[i], j, stars[j]) for i, j in combinations(range(10), 2)),
         'primary actual reciprocal completion')
    damaged = 0
    for i in range(10):
        for remove in indices(stars[i], 10):
            for add in range(10):
                if add == i or stars[i] & (1 << add): continue
                changed = stars[i] ^ (1 << remove) ^ (1 << add)
                need(any(not frame.compatible(i, changed, j, stars[j]) for j in range(10) if j != i),
                     'primary degree-preserving asymmetric star')
                damaged += 1
    return {'red_edges': 93, 'blue_edges': 117, 'max_red_pages': 3, 'max_blue_pages': 6,
            'actual_stars_accepted': 10, 'actual_completion_accepted': 1,
            'degree_preserving_asymmetric_damages_rejected': damaged}


def compute():
    geometry = geometry_checks(); small = small_whole_graph_controls(); primary = primary_control()
    keys, census = complete_census(); classes = orbits(keys)
    records = []; initial_weight = propagated_weight = 0
    for key, orbit in classes:
        frame = Frame(P, rows_of(key)); domains = frame.domains(DEFICITS)
        exclusion = synchronous_exclusion(frame, domains)
        if exclusion['type'] == 'initial_empty': initial_weight += len(orbit)
        else: propagated_weight += len(orbit)
        records.append({'key': key, 'orbit_size': len(orbit), 'domain_sizes': tuple(map(len, domains)),
                        'domains_sha256': digest(domains), 'exclusion': exclusion})
    patterns = Counter((z.bit_count(), w.bit_count(), tuple(h.bit_count() for h in large))
                       for z, w, large, _ in keys)
    round_counts = Counter(); round_coverage = Counter()
    for record in records:
        r = record['exclusion']['rounds']; round_counts[str(r)] += 1
        round_coverage[str(r)] += record['orbit_size']
    return {'actual_reviewer': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'scope': 'Rooted finite lemma of 8941 only; unrooted corollary remains conditional on credited 8828.',
            'geometry': geometry, 'whole_graph_controls': small, 'primary_control': primary, 'census': census,
            'incidence_count': len(keys), 'incidence_sha256': digest(sorted(keys)),
            'orbits': len(classes), 'orbit_histogram': dict(Counter(str(len(o)) for _, o in classes)),
            'initial_empty_coverage': initial_weight, 'synchronous_empty_coverage': propagated_weight,
            'round_representatives': dict(round_counts), 'round_weighted_coverage': dict(round_coverage),
            'size_patterns': [[z, w, large, count] for (z, w, large), count in sorted(patterns.items())],
            'records': records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args(); result = compute()
    if args.emit:
        print(json.dumps(result, sort_keys=True, separators=(',', ':')))
    else:
        need(json.loads(json.dumps(result)) == json.loads((HERE / 'expected.json').read_text()),
             'complete independent frozen record mismatch')
        print('PASS')


if __name__ == '__main__':
    main()
