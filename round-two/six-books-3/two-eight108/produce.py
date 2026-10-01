#!/usr/bin/env python3
"""Produce a finite Petersen incidence cover and static star-pair obstruction certificates.

No solver, branching search, host automorphism, or outside degree-floor theorem
is used. Normal mode independently regenerates and compares the frozen output.
"""
import argparse
from collections import Counter
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
DELTAS = (2, 2) + (0,) * 9


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical_json(value):
    normalized = json.loads(json.dumps(value))  # JSON object keys are strings.
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def key_rows(key):
    z, w, highs, mu = key
    return [z, w] + list(highs) + [s for s, m in zip(STARS, mu) for _ in range(m)]


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
    """Reverse columns: enumerate nine full rows, then assign two residual rows."""
    masks = {z: sum(1 << t for t, (i, j) in enumerate(RED)
                    if z >> i & 1 and z >> j & 1) for z in range(1024)}
    full = {k: [z for z in range(1024) if z.bit_count() == k
                and all((P[i] & (A ^ z)).bit_count() <= 1
                        for i in range(10) if not z >> i & 1)] for k in (5, 6)}
    low = {d: word_pool(d) for d in (2,)}
    choices = [()] + [(z,) for z in full[5]] + [(z,) for z in full[6]]
    choices += list(combinations_with_replacement(full[5], 2))
    stats = Counter()
    keys = set()
    for highs in choices:
        used = 0
        for z in highs:
            if used & masks[z]:
                break
            used |= masks[z]
        else:
            stats["high_large_multisets"] += 1
            for mu in product(range(3), repeat=5):
                if sum(mu) + len(highs) != 9:
                    continue
                stats["high_multiplicity_choices"] += 1
                highrows = list(highs) + [s for s, m in zip(STARS, mu) for _ in range(m)]
                residual = [5 - sum(z >> i & 1 for z in highrows) for i in range(10)]
                if any(not 0 <= value <= 2 for value in residual):
                    continue
                if any(sum(bool(z >> i & 1 and z >> j & 1) for z in highrows) > 3
                       for i, j in BLUE):
                    continue
                stats["residual_vectors"] += 1
                base = sum(1 << i for i, value in enumerate(residual) if value == 2)
                singles = [i for i, value in enumerate(residual) if value == 1]
                for take in (6, 7, 8):
                    amount = take - base.bit_count()
                    if not 0 <= amount <= len(singles):
                        continue
                    for picked in combinations(singles, amount):
                        z = base | sum(1 << i for i in picked)
                        stats["residual_low_assignments"] += 1
                        if z not in low[2]:
                            continue
                        w = sum(1 << i for i, value in enumerate(residual)
                                if value - (z >> i & 1) == 1)
                        if w not in low[2]:
                            continue
                        if z > w:
                            continue
                        if used & masks[z] or used & masks[w] or masks[z] & masks[w]:
                            continue
                        rows = [z, w] + highrows
                        if any(sum(bool(q >> i & 1 and q >> j & 1) for q in rows) > 3
                               for i, j in BLUE):
                            continue
                        stats["pair_capped"] += 1
                        key = (z, w, tuple(sorted(highs)), tuple(mu))
                        require(key not in keys, "duplicate reverse-column record")
                        keys.add(key)
    return keys, {
        "full_large_word_sizes": {str(k): len(words) for k, words in full.items()},
        "low_word_sizes": {str(d): dict(sorted(Counter(z.bit_count() for z in words).items()))
                           for d, words in low.items()},
        "census": dict(sorted(stats.items())),
        "incidence_records": len(keys),
    }


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
    z, w, highs, mu = key
    moved_mu = [0] * 5
    for t in range(5):
        moved_mu[permutation[t]] = mu[t]
    moved_low = sorted((words[z], words[w]))
    return (moved_low[0], moved_low[1], tuple(sorted(words[h] for h in highs)), tuple(moved_mu))


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
    raise ValueError("unexcluded incidence: no complete static certificate produced")


def make_certificate():
    keys, result = census()
    maps = transformations()
    canonical = Counter(min(transformed(k, p, w) for p, w in maps) for k in sorted(keys))
    entries = []
    for key, size in sorted(canonical.items()):
        rows = key_rows(key)
        require(len(rows) == 11, "wrong outside order")
        stars = domains(rows)
        entries.append({"key": key, "orbit_size": size,
                        "domain_sizes": [len(d) for d in stars],
                        "domains_sha256": digest(stars), "exclusion": exclusion(rows, stars)})
    certificate = {"schema": 1, "order": 22, "red_page_cap": 3, "blue_page_cap": 6,
                   "outside_deficits": DELTAS, "local_graph": "KG(5,2)",
                   "incidence_records": len(keys), "entries": entries}
    result.update({"incidence_sha256": digest(sorted(keys)), "orbits": len(entries),
                   "orbit_size_histogram": dict(sorted(Counter(canonical.values()).items())),
                   "exclusion_types": dict(sorted(Counter(e["exclusion"]["type"] for e in entries).items())),
                   "star_pair_covers": sum(len(e["exclusion"].get("covers", [])) for e in entries),
                   "unsupported_stars": sum(len(s["stars"]) for e in entries
                                            for s in e["exclusion"].get("covers", [])),
                   "certificate_sha256": digest(certificate)})
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
