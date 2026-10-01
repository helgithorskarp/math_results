#!/usr/bin/env python3
"""Independent three-low quotient census and literal finite-certificate checker.

This file imports no producer, solver, graph catalogue, or private data. Its
Petersen adjacency table, low-row-first census, orbit expansion, full-vertex
page oracle, and static/support-deletion verification differ from the producer.
"""
import argparse
from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement, permutations
import hashlib
import json
from functools import lru_cache
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
NEIGHBORS = tuple(map(frozenset, (
    (7, 8, 9), (5, 6, 9), (4, 6, 8), (4, 5, 7), (2, 3, 9),
    (1, 3, 8), (1, 2, 7), (0, 3, 6), (0, 2, 5), (0, 1, 4))))
GROUND = list(combinations(range(5), 2))
POSITION = {edge: i for i, edge in enumerate(GROUND)}
POINTS = frozenset(range(10))
STAR_SETS = [frozenset(i for i, pair in enumerate(GROUND) if t in pair) for t in range(5)]
PAIRS = list(combinations(range(10), 2))
DEFICITS = (2, 1, 1) + (0,) * 8


def require(ok, message):
    if not ok:
        raise ValueError(message)

def pack(value):
    normalized = json.loads(json.dumps(value))  # JSON object keys are strings.
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"))

def digest(value):
    return hashlib.sha256(pack(value).encode()).hexdigest()

def word(points):
    return sum(1 << i for i in points)

def points(mask, n):
    return {i for i in range(n) if mask >> i & 1}

def integer(value, minimum, maximum, name):
    require(type(value) is int and minimum <= value <= maximum, name + " is out of range")

def fields(value, names, name):
    require(type(value) is dict and set(value) == set(names), name + " has malformed fields")

def validate_key(raw):
    require(type(raw) is list and len(raw) == 5, 'malformed incidence key')
    z, w, q, highs, mu = raw
    for value, label in ((z, 'degree-eight row'), (w, 'first degree-nine row'),
                         (q, 'second degree-nine row')):
        integer(value, 0, 1023, label)
    require(w <= q, 'unordered equal-deficit degree-nine rows')
    require(type(highs) is list and len(highs) <= 2, 'malformed full large rows')
    for h in highs:
        integer(h, 0, 1023, 'full large row')
    require(highs == sorted(highs), 'full large rows unsorted')
    require(type(mu) is list and len(mu) == 5, 'malformed four-row multiplicities')
    for m in mu:
        integer(m, 0, 2, 'four-row multiplicity')
    require(sum(mu) + len(highs) == 8, 'incorrect number of full rows')
    return z, w, q, tuple(highs), tuple(mu)


def rows_from_key(key):
    z, w, q, highs, mu = key
    return [z, w, q] + list(highs) + [word(s) for s, count in zip(STAR_SETS, mu) for _ in range(count)]


def low_words(delta):
    result = set()
    for size in range(2, 10 - (4 + delta) + 1):
        for choice in combinations(range(10), size):
            c = set(choice)
            z = POINTS - c
            k = len(z)
            if any(k - delta > 8 - len(NEIGHBORS[i] & c) for i in c):
                continue
            if any(k - 1 - len(NEIGHBORS[i] & z) > 6 for i in z):
                continue
            if any(k + delta + len(NEIGHBORS[i] & c) + len(NEIGHBORS[j] & c) > 12
                   for i, j in PAIRS if j in NEIGHBORS[i] and i in z and j in z):
                continue
            result.add(word(z))
    return result

def quotient(vector):
    def e(i, j):
        return vector[POSITION[tuple(sorted((i, j)))]]
    return (e(0, 3) - e(1, 3) - e(0, 2) + e(1, 2),
            e(0, 4) - e(1, 4) - e(0, 2) + e(1, 2),
            *(e(0, i) + e(0, j) - e(i, j) - e(0, 1) - e(0, 2) + e(1, 2)
              for i, j in ((2, 3), (2, 4), (3, 4))))

def incidence_census():
    """Low-pair quotient table, low8/large join, then exact star recovery."""
    sets = {z: points(z, 10) for z in range(1024)}
    vectors = {z: tuple(int(i in sets[z]) for i in range(10)) for z in range(1024)}
    qs = {z: quotient(vector) for z, vector in vectors.items()}
    red_pairs = [(i,j) for i,j in PAIRS if j in NEIGHBORS[i]]
    blue_pairs = [(i,j) for i,j in PAIRS if j not in NEIGHBORS[i]]
    red_sets = {z: frozenset(t for t,(i,j) in enumerate(red_pairs) if i in sets[z] and j in sets[z]) for z in range(1024)}
    blue_bits = {z: tuple(int(i in sets[z] and j in sets[z]) for i,j in blue_pairs) for z in range(1024)}
    common_star = [next(t for t,star in enumerate(STAR_SETS) if i in star and j in star) for i,j in blue_pairs]
    require(all(qs[word(s)] == (0,) * 5 for s in STAR_SETS), 'nonzero star quotient')
    require(quotient([5] * 10) == (0,) * 5, 'nonzero constant column quotient')
    low8 = sorted(low_words(2))
    low9 = sorted(z for z in low_words(1) if len(sets[z]) <= 7)
    table = defaultdict(list)
    stats = Counter()
    for w in low9:
        for q in low9:
            if w > q or len(sets[w]) + len(sets[q]) > 12:
                continue
            stats['low9_pairs_within_budget'] += 1
            if not red_sets[w].isdisjoint(red_sets[q]):
                continue
            stats['low9_pairs_red_capped'] += 1
            signature = tuple(qs[w][a] + qs[q][a] for a in range(5))
            pair_vector = tuple(vectors[w][i] + vectors[q][i] for i in range(10))
            pair_blue = tuple(blue_bits[w][i] + blue_bits[q][i] for i in range(len(blue_pairs)))
            table[len(sets[w]) + len(sets[q]), signature].append((w, q, red_sets[w] | red_sets[q], pair_vector, pair_blue))
    high = {k: sorted(word(POINTS - set(c)) for c in combinations(range(10), 10 - k)
                     if all(len(NEIGHBORS[i] & set(c)) <= 1 for i in c)) for k in (5, 6)}
    choices = [(0, ())] + [(1, (z,)) for z in high[5]] + [(2, (z,)) for z in high[6]]
    choices += [(2, pair) for pair in combinations_with_replacement(high[5], 2)]
    keys = set()
    high_counts = Counter()
    for surplus, highs in choices:
        if len(highs) == 2 and not red_sets[highs[0]].isdisjoint(red_sets[highs[1]]):
            continue
        high_counts[surplus] += 1
        high_q = tuple(sum(qs[h][a] for h in highs) for a in range(5))
        high_red = frozenset().union(*(red_sets[h] for h in highs))
        high_vector = tuple(sum(vectors[h][i] for h in highs) for i in range(10))
        high_blue = tuple(sum(blue_bits[h][i] for h in highs) for i in range(len(blue_pairs)))
        for z in low8:
            pair_size = 18 - surplus - len(sets[z])
            if pair_size < 10 or pair_size > 12:
                continue
            stats['budget_low8_large_pairs'] += 1
            if not high_red.isdisjoint(red_sets[z]):
                continue
            known_red = high_red | red_sets[z]
            base = tuple(5 - high_vector[i] - vectors[z][i] for i in range(10))
            known_blue = tuple(high_blue[i] + blue_bits[z][i] for i in range(len(blue_pairs)))
            target = tuple(-qs[z][a] - high_q[a] for a in range(5))
            for w, q, pair_red, pair_vector, pair_blue in table.get((pair_size, target), ()):
                stats['quotient_joins'] += 1
                if not known_red.isdisjoint(pair_red):
                    continue
                stats['red_capped_joins'] += 1
                residual = [base[i] - pair_vector[i] for i in range(10)]
                twice0 = residual[POSITION[0, 1]] + residual[POSITION[0, 2]] - residual[POSITION[1, 2]]
                if twice0 % 2:
                    continue
                mu = (twice0 // 2,) + tuple(residual[POSITION[0, j]] - twice0 // 2 for j in range(1, 5))
                if any(not 0 <= m <= 2 for m in mu) or sum(mu) + len(highs) != 8:
                    continue
                if any(mu[i] + mu[j] != residual[t] for t, (i, j) in enumerate(GROUND)):
                    continue
                stats['integral_column_recoveries'] += 1
                key = (z, w, q, tuple(highs), mu)
                if any(known_blue[i] + pair_blue[i] + mu[common_star[i]] > 3
                       for i in range(len(blue_pairs))):
                    continue
                require(key not in keys, 'duplicate quotient recovery')
                keys.add(key)
    patterns = Counter((len(sets[z]), *sorted((len(sets[w]), len(sets[q]))),
                        tuple(len(sets[h]) for h in highs)) for z, w, q, highs, mu in keys)
    return keys, {'high_multiset_counts_by_surplus': [high_counts[i] for i in range(3)],
                  'low8_word_sizes': dict(sorted(Counter(len(sets[z]) for z in low8).items())),
                  'low9_word_sizes': dict(sorted(Counter(len(sets[z]) for z in low9).items())),
                  'full_large_sizes': {k: len(pool) for k, pool in high.items()},
                  'patterns': [{'sizes': p, 'records': n} for p, n in sorted(patterns.items())],
                  'census': dict(sorted(stats.items())), 'incidence_records': len(keys),
                  'incidence_sha256': digest(sorted(keys))}


@lru_cache(maxsize=None)
def orbit(key):
    result = set()
    z, w, q, highs, mu = key
    for perm in permutations(range(5)):
        images = [POSITION[tuple(sorted((perm[a], perm[b])))] for a, b in GROUND]
        require(all((j in NEIGHBORS[i]) == (images[j] in NEIGHBORS[images[i]])
                    for i, j in PAIRS), "non-Petersen relabeling")
        def move(mask):
            return word(images[i] for i in points(mask, 10))
        new_mu = [0] * 5
        for t, count in enumerate(mu):
            new_mu[perm[t]] = count
        moved_low = sorted((move(w), move(q)))
        result.add((move(z), moved_low[0], moved_low[1], tuple(sorted(move(h) for h in highs)), tuple(new_mu)))
    return frozenset(result)

class LiteralFrame:
    """Full physical vertex sets, including root, A, and all B points."""
    def __init__(self, local, rows, deficits):
        self.local = local
        self.rows = rows
        self.deficits = deficits
        self.n = len(rows)
        self.universe = frozenset(range(11 + self.n))
        self.misses = [points(z, 10) for z in rows]
        self.a_red = [frozenset({0} | {j + 1 for j in local[i]}
                               | {11 + b for b, z in enumerate(self.misses) if i not in z})
                      for i in range(10)]
        self.a_blue = [self.universe - red - {i + 1} for i, red in enumerate(self.a_red)]
        self.full = {}

    def neighborhoods(self, b, star):
        key = (b, star)
        if key not in self.full:
            red = frozenset({i + 1 for i in POINTS - self.misses[b]}
                            | {11 + c for c in points(star, self.n)})
            self.full[key] = red, self.universe - red - {11 + b}
        return self.full[key]

    def domains(self):
        result = []
        for b, (z, delta) in enumerate(zip(self.misses, self.deficits)):
            degree = len(z) - delta
            require(0 <= degree < self.n, "literal outside degree out of range")
            accepted = []
            for picked in combinations([c for c in range(self.n) if c != b], degree):
                star = word(picked)
                red, blue = self.neighborhoods(b, star)
                if all(len(blue & self.a_blue[i]) <= 6 if i in z
                       else len(red & self.a_red[i]) <= 3 for i in range(10)):
                    accepted.append(star)
            result.append(sorted(accepted))
        return result

    def compatible(self, b, x, c, y):
        red_b, blue_b = self.neighborhoods(b, x)
        red_c, blue_c = self.neighborhoods(c, y)
        if ((11 + c) in red_b) != ((11 + b) in red_c):
            return False
        return len(red_b & red_c) <= 3 if (11 + c) in red_b else len(blue_b & blue_c) <= 6

@lru_cache(maxsize=None)
def literal_domains(key):
    # Immutable exact domains, keyed by the complete fixed-tag incidence.
    # Repeated integrity controls never need to rebuild the same geometry.
    frame = LiteralFrame(NEIGHBORS, rows_from_key(key), DEFICITS)
    return tuple(tuple(domain) for domain in frame.domains())


def check_exclusion(frame, stars, exclusion):
    require(type(exclusion) is dict, "exclusion is not an object")
    if exclusion.get("type") == "empty_star":
        fields(exclusion, ("type", "point"), "empty-star certificate")
        b = exclusion["point"]
        integer(b, 0, 10, "empty-star point")
        require(not stars[b], "claimed star domain is nonempty")
        return 0, 0, 0, 0
    if exclusion.get('type') == 'arc_deletion':
        fields(exclusion, ('type', 'empty_point', 'steps'), 'support trace')
        integer(exclusion['empty_point'], 0, 10, 'final empty point')
        require(all(stars), 'trace starts with an empty domain')
        require(type(exclusion['steps']) is list and exclusion['steps'], 'empty deletion trace')
        current = [set(domain) for domain in stars]
        removed_count = 0
        for step in exclusion['steps']:
            require(all(current), 'trace continues after emptiness')
            fields(step, ('point', 'against', 'remove'), 'support deletion')
            b, c, removed = step['point'], step['against'], step['remove']
            integer(b, 0, 10, 'deletion point')
            integer(c, 0, 10, 'support point')
            require(b != c, 'self-support deletion')
            require(type(removed) is list and removed, 'empty deletion step')
            for x in removed:
                integer(x, 0, 2047, 'deleted star')
            require(removed == sorted(set(removed)), 'noncanonical deletion stars')
            require(set(removed) <= current[b], 'deleted star not present')
            for x in removed:
                require(not any(frame.compatible(b, x, c, y) for y in current[c]),
                        'deleted star retains support')
            current[b].difference_update(removed)
            removed_count += len(removed)
        require(not current[exclusion['empty_point']], 'claimed final domain is nonempty')
        return 0, 0, len(exclusion['steps']), removed_count
    fields(exclusion, ("type", "point", "covers"), "star-pair certificate")
    require(exclusion["type"] == "star_pair_cover", "unknown exclusion type")
    require(all(stars), "star-pair cover with an initially empty domain")
    b = exclusion["point"]
    integer(b, 0, 10, "target point")
    require(type(exclusion["covers"]) is list and exclusion["covers"], "empty star cover")
    covered = set()
    against_points = []
    for cover in exclusion["covers"]:
        fields(cover, ("against", "stars"), "unsupported-star cover")
        c, unsupported = cover["against"], cover["stars"]
        integer(c, 0, 10, "support point")
        require(b != c, "self-support obstruction")
        against_points.append(c)
        require(type(unsupported) is list and unsupported, "empty unsupported-star list")
        for x in unsupported:
            integer(x, 0, 2047, "unsupported star")
        require(unsupported == sorted(set(unsupported)), "noncanonical unsupported stars")
        require(set(unsupported) <= set(stars[b]), "claimed star not in complete initial domain")
        require(not covered.intersection(unsupported), "overlapping unsupported-star covers")
        for x in unsupported:
            require(not any(frame.compatible(b, x, c, y) for y in stars[c]),
                    "claimed unsupported star has initial support")
        covered.update(unsupported)
    require(against_points == sorted(set(against_points)), "unordered or duplicate support points")
    require(covered == set(stars[b]), "incomplete initial-star obstruction cover")
    return len(exclusion["covers"]), len(covered), 0, 0

def verify_certificate(certificate, keys, census_result):
    fields(certificate, ("schema", "order", "red_page_cap", "blue_page_cap", "outside_deficits",
                         "local_graph", "incidence_records", "entries"), "certificate")
    for name, expected in (("schema", 1), ("order", 22), ("red_page_cap", 3), ("blue_page_cap", 6)):
        require(type(certificate[name]) is int and certificate[name] == expected, "wrong " + name)
    require(certificate["outside_deficits"] == list(DEFICITS)
            and all(type(d) is int for d in certificate["outside_deficits"]), "wrong deficiency tags")
    require(certificate["local_graph"] == "KG(5,2)", "wrong local graph")
    require(type(certificate["entries"]) is list and certificate["entries"], "no certificate entries")
    integer(certificate["incidence_records"], len(keys), len(keys), "incidence record count")
    covered = set()
    hist = Counter()
    exclusions = Counter()
    weighted_exclusions = Counter()
    cover_count = unsupported_count = arc_steps = arc_removed = 0
    ordered_keys = []
    for entry in certificate["entries"]:
        fields(entry, ("key", "orbit_size", "domain_sizes", "domains_sha256", "exclusion"), "entry")
        key = validate_key(entry["key"])
        ordered_keys.append(key)
        images = orbit(key)
        require(key == min(images), "representative is not minimal in its local orbit")
        integer(entry["orbit_size"], len(images), len(images), "orbit size")
        require(not (covered & images), "overlapping orbit entries")
        require(images <= keys, "certificate orbit has inadmissible incidence")
        covered.update(images)
        frame = LiteralFrame(NEIGHBORS, rows_from_key(key), DEFICITS)
        stars = literal_domains(key)
        require(entry["domain_sizes"] == [len(domain) for domain in stars]
                and all(type(s) is int for s in entry["domain_sizes"]), "star domain sizes mismatch")
        require(entry["domains_sha256"] == digest(stars), "literal star domains hash mismatch")
        covers, unsupported, steps, removals = check_exclusion(frame, stars, entry["exclusion"])
        arc_steps += steps
        arc_removed += removals
        cover_count += covers
        unsupported_count += unsupported
        hist[len(images)] += 1
        exclusions[entry["exclusion"]["type"]] += 1
        weighted_exclusions[entry["exclusion"]["type"]] += len(images)
    require(ordered_keys == sorted(set(ordered_keys)), "unordered or duplicate representatives")
    require(covered == keys, "certificate does not cover the complete independent census")
    result = dict(census_result)
    result.update({"orbits": len(ordered_keys), "orbit_size_histogram": dict(sorted(hist.items())),
                   "exclusion_types": dict(sorted(exclusions.items())),
                   "weighted_exclusion_types": dict(sorted(weighted_exclusions.items())),
                   "star_pair_covers": cover_count, "unsupported_stars": unsupported_count,
                   "arc_steps": arc_steps, "arc_removed_stars": arc_removed,
                   "covered_records_sha256": digest(sorted(covered)),
                   "certificate_sha256": digest(certificate)})
    return result

def geometry_controls():
    require(all(len(n) == 3 for n in NEIGHBORS), "Petersen is not cubic")
    require(all((j in NEIGHBORS[i]) == (set(GROUND[i]).isdisjoint(GROUND[j]))
                for i, j in PAIRS), "literal adjacency/ground-label mismatch")
    require(all(len(NEIGHBORS[i] & NEIGHBORS[j]) == (0 if j in NEIGHBORS[i] else 1)
                for i, j in PAIRS), "Petersen common-neighbor table mismatch")
    independent = [frozenset(s) for s in combinations(range(10), 4)
                   if all(j not in NEIGHBORS[i] for i, j in combinations(s, 2))]
    require(set(independent) == set(STAR_SETS), "independent four-set classification mismatch")
    require(all(t * (t - 1) // 2 >= t - 1 for t in range(5)), "four-column packing identity")
    require(all(sum(i in star and j in star for star in STAR_SETS) == (0 if j in NEIGHBORS[i] else 1) for i,j in PAIRS), 'ground-star pair multiplicity')
    patterns = []
    for z in range(6, 11):
        for w in range(5, 11):
            for q in range(w, 11):
                if z + w + q + 8 * 4 <= 50:
                    patterns.append([z, w, q])
    require(patterns == [[6,5,5],[6,5,6],[6,5,7],[6,6,6],[7,5,5],[7,5,6],[8,5,5]],
            'three-low size-budget coverage')
    return {'independent_four_sets': len(independent), 'complete_low_size_patterns': patterns,
            'fixed_tags': [2, 1, 1]}


def primary_control():
    raw = (HERE / "primary21.txt").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == "3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55",
            "primary21 raw fixture hash mismatch")
    matrix = json.loads(raw.decode().split("\n\n")[0])
    require(len(matrix) == 21 and all(len(row) == 21 for row in matrix), "primary21 dimensions")
    red = []
    universe = set(range(21))
    for i in range(21):
        require(matrix[i][i] == 0, "primary21 diagonal")
        require(all(type(matrix[i][j]) is int and matrix[i][j] in (0, 1)
                    and matrix[i][j] == matrix[j][i] for j in range(21)), "primary21 symmetry/entries")
        red.append({j for j in range(21) if j != i and matrix[i][j] == 0})
    blue = [universe - red[i] - {i} for i in range(21)]
    red_pages = [len(red[i] & red[j]) for i, j in combinations(range(21), 2) if j in red[i]]
    blue_pages = [len(blue[i] & blue[j]) for i, j in combinations(range(21), 2) if j in blue[i]]
    require(max(red_pages) == 3 and max(blue_pages) == 6, "primary21 book caps")
    roots = [i for i, n in enumerate(red) if len(n) == 10]
    require(len(roots) == 1, "primary21 unique degree-ten root")
    v = roots[0]
    a, b = sorted(red[v]), sorted(blue[v])
    local = tuple(frozenset(j for j in range(10) if a[j] in red[a[i]]) for i in range(10))
    rows = [word(i for i in range(10) if a[i] not in red[u]) for u in b]
    deficits = [10 - len(red[u]) for u in b]
    actual = [word(j for j in range(10) if b[j] in red[u]) for u in b]
    frame = LiteralFrame(local, rows, deficits)
    domains = frame.domains()
    require(all(actual[i] in domains[i] for i in range(10)), "primary21 actual star rejected")
    require(all(frame.compatible(i, actual[i], j, actual[j]) for i, j in combinations(range(10), 2)),
            "primary21 actual completion rejected")
    damaged = 0
    for i in range(10):
        for j in range(10):
            for h in range(10):
                if len({i, j, h}) != 3 or not actual[i] >> j & 1 or actual[i] >> h & 1:
                    continue
                trial = actual[i] ^ (1 << j) ^ (1 << h)
                require(any(not frame.compatible(i, trial, c, actual[c]) for c in range(10) if c != i),
                        "primary21 asymmetric damaged star accepted")
                damaged += 1
    return {"order": 21, "red_edges": len(red_pages), "blue_edges": len(blue_pages),
            "max_red_pages": max(red_pages), "max_blue_pages": max(blue_pages),
            "actual_stars_accepted": 10, "actual_completion_accepted": 1,
            "asymmetric_degree_preserving_damages_rejected": damaged}

def signed_cut_controls():
    sampler = random.Random(20261001)
    checks = negative_slacks = 0
    for _ in range(32):
        columns = [set(sampler.sample(range(11), 5)) for _ in range(10)]
        rows = [word(i for i in range(10) if b in columns[i]) for b in range(11)]
        b = sampler.randrange(11)
        actual_star = word(c for c in range(11) if c != b and sampler.getrandbits(1))
        frame = LiteralFrame(NEIGHBORS, rows, DEFICITS)
        red, blue = frame.neighborhoods(b, actual_star)
        z = points(rows[b], 10)
        c = POINTS - z
        for i in z:
            pages = len(blue & frame.a_blue[i])
            intersection = len(points(actual_star, 11) & (columns[i] - {b}))
            h = len(NEIGHBORS[i] & c)
            require(intersection == len(z) - 6 + h + (6 - pages), "signed two-column identity")
            checks += 1
            negative_slacks += pages > 6
    require(negative_slacks > 0, "signed controls lack negative blue slack")
    return {"frames": 32, "blue_intersection_identity_checks": checks,
            "negative_blue_slack_cases": negative_slacks}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--expected", type=Path, default=HERE / "expected.json")
    parser.add_argument("--derive", action="store_true", help="omit frozen-summary comparison")
    args = parser.parse_args()
    geometry = geometry_controls()
    keys, census = incidence_census()
    result = verify_certificate(json.loads(args.certificate.read_text()), keys, census)
    result["controls"] = {"geometry": geometry, "primary21": primary_control(),
                          "signed_cut": signed_cut_controls()}
    if not args.derive:
        require(pack(result) == pack(json.loads(args.expected.read_text())["verifier"]),
                "verifier expected-summary mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
