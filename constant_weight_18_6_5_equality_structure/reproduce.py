#!/usr/bin/env python3
"""Exact baseline and abstract local-carrier validation; no global search."""

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
BASELINE_SHA256 = "cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def partitions(n, cap=None):
    if n == 0:
        yield ()
        return
    for first in range(min(n, cap if cap is not None else n), 0, -1):
        for tail in partitions(n - first, first):
            yield (first,) + tail


def mask_edges(k, mask):
    pairs = tuple(combinations(range(k), 2))
    return tuple(e for j, e in enumerate(pairs) if (mask >> j) & 1)


def permute_mask(k, mask, perm):
    pairs = tuple(combinations(range(k), 2))
    moved = {tuple(sorted((perm[a], perm[b]))) for a, b in mask_edges(k, mask)}
    return sum(1 << j for j, e in enumerate(pairs) if e in moved)


def color_permutations(partition):
    return tuple(p for p in permutations(range(len(partition)))
                 if all(partition[i] == partition[p[i]]
                        for i in range(len(partition))))


def admissible(partition, mask):
    k = len(partition)
    core = mask_edges(k, mask)
    isolated_pairs = len(core) - k + 1
    if isolated_pairs < 0 or 2 * isolated_pairs > 17 - k:
        return False
    degrees = [sum(i in e for e in core) for i in range(k)]
    leaves = [1 + 3 * partition[i] - degrees[i] for i in range(k)]
    return min(leaves) >= 0 and sum(leaves) + 2 * isolated_pairs == 17 - k


def representative(partition, mask):
    return min(permute_mask(len(partition), mask, p)
               for p in color_permutations(partition))


def construct_link(entry):
    """Realize the specified core, its attached leaves and isolated edges."""
    partition = tuple(entry["partition"])
    k = len(partition)
    edges = set(mask_edges(k, entry["core_mask"]))
    nxt = k
    for i, count in enumerate(entry["leaf_counts"]):
        for _ in range(count):
            edges.add((i, nxt))
            nxt += 1
    for _ in range(entry["isolated_pairs"]):
        edges.add((nxt, nxt + 1))
        nxt += 2
    require(nxt == 17, "bad reconstructed vertex count")
    require(len(edges) == 16, "bad reconstructed edge count")
    degrees = [sum(i in e for e in edges) for i in range(17)]
    require(degrees == [1 + 3 * t for t in partition] + [1] * (17 - k),
            "bad reconstructed degrees")
    return edges


def generate_catalog():
    catalog, summary = [], []
    for part in partitions(5):
        k = len(part)
        masks = tuple(mask for mask in range(1 << (k * (k - 1) // 2))
                      if admissible(part, mask))
        reps = sorted({representative(part, mask) for mask in masks})
        group = color_permutations(part)
        # Burnside averages fixed labeled cores instead of canonicalizing orbits.
        fixed_sum = sum(sum(permute_mask(k, mask, p) == mask for mask in masks)
                        for p in group)
        require(fixed_sum == len(group) * len(reps), "Burnside mismatch")
        for mask in reps:
            core = mask_edges(k, mask)
            degree = [sum(i in e for e in core) for i in range(k)]
            entry = {
                "partition": list(part),
                "core_mask": mask,
                "leaf_counts": [1 + 3 * part[i] - degree[i] for i in range(k)],
                "isolated_pairs": len(core) - k + 1,
            }
            construct_link(entry)
            catalog.append(entry)
        # Expanding catalog representatives must cover every admissible mask.
        expanded = {permute_mask(k, mask, p) for mask in reps for p in group}
        require(expanded == set(masks), "incomplete orbit coverage")
        summary.append({"partition": list(part), "types": len(reps),
                        "labeled_core_masks": len(masks)})
    return catalog, summary


def validate_words(words):
    require(len(words) == len(set(words)), "duplicate codeword")
    for word in words:
        require(len(word) == 18 and set(word) <= {"0", "1"}, "malformed word")
        require(word.count("1") == 5, "wrong weight")
    blocks = [frozenset(i for i, c in enumerate(word) if c == "1") for word in words]
    for a, b in combinations(blocks, 2):
        require(len(a & b) <= 2, "minimum-distance failure")
    # Direct distance/intersection checking and triple multiplicity checking.
    triple_counts = Counter(t for b in blocks for t in combinations(sorted(b), 3))
    require(all(count == 1 for count in triple_counts.values()), "repeated triple")
    return blocks, triple_counts


def controls():
    a = "111110000000000000"
    good = [a, "000000000000011111"]
    validate_words(good)
    invalid = [[a, a], [a[:-1]], ["x" + a[1:]], ["0" * 18],
               [a, "111101000000000000"]]
    for words in invalid:
        try:
            validate_words(words)
        except ValueError:
            continue
        raise ValueError("invalid fixture was accepted")
    return len(invalid)


def histogram(values):
    return {str(k): v for k, v in sorted(Counter(values).items())}


def audit_baseline(catalog):
    raw = (HERE / "baseline69.txt").read_bytes()
    require(sha256(raw).hexdigest() == BASELINE_SHA256, "baseline hash mismatch")
    words = raw.decode("ascii").splitlines()
    require(len(words) == 69, "baseline cardinality mismatch")
    blocks, covered = validate_words(words)
    all_pairs = tuple(combinations(range(18), 2))
    pairs = Counter(p for b in blocks for p in combinations(sorted(b), 2))
    replication = [sum(x in b for b in blocks) for x in range(18)]
    leave = set(combinations(range(18), 3)) - set(covered)
    known = {(tuple(e["partition"]), e["core_mask"]) for e in catalog}
    local_types = Counter()
    for x, r in enumerate(replication):
        if r != 20:
            continue
        deficit = {y: 5 - pairs[tuple(sorted((x, y)))]
                   for y in range(18) if y != x}
        require(min(deficit.values()) >= 0 and sum(deficit.values()) == 5,
                "bad saturated-point deficits")
        link = {tuple(y for y in triple if y != x) for triple in leave if x in triple}
        require(len(link) == 16, "bad saturated link edge count")
        for y, t in deficit.items():
            require(sum(y in e for e in link) == 1 + 3 * t,
                    "link degree disagrees with direct leave")
        high = sorted((y for y, t in deficit.items() if t),
                      key=lambda y: (-deficit[y], y))
        part = tuple(deficit[y] for y in high)
        core_pairs = tuple(combinations(range(len(high)), 2))
        mask = sum(1 << j for j, (a, b) in enumerate(core_pairs)
                   if tuple(sorted((high[a], high[b]))) in link)
        key = (part, representative(part, mask))
        require(key in known, "baseline link absent from complete carrier")
        p = sum(deficit[a] == 0 and deficit[b] == 0 for a, b in link)
        require(mask.bit_count() - p == len(high) - 1, "core/matching identity")
        local_types["+".join(map(str, part))] += 1
    return {
        "words": len(words),
        "word_sha256": sha256(raw).hexdigest(),
        "minimum_distance": min(10 - 2 * len(a & b) for a, b in combinations(blocks, 2)),
        "covered_triples": len(covered),
        "leave_triples": len(leave),
        "replication_histogram": histogram(replication),
        "pair_multiplicity_histogram": histogram(pairs[p] for p in all_pairs),
        "saturated_points": sum(r == 20 for r in replication),
        "saturated_partition_histogram": dict(sorted(local_types.items())),
    }


def encoded_json(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-fixtures", action="store_true",
                        help="regenerate the compact catalog and expected report")
    args = parser.parse_args()
    catalog, summary = generate_catalog()
    catalog_bytes = encoded_json(catalog)
    report = {
        "baseline": audit_baseline(catalog),
        "local_carrier": {
            "types": len(catalog),
            "labeled_core_masks": sum(row["labeled_core_masks"] for row in summary),
            "partitions": summary,
            "catalog_sha256": sha256(catalog_bytes).hexdigest(),
        },
        "invalid_code_controls_rejected": controls(),
        "global_72_word_exclusion": False,
    }
    require(report["local_carrier"]["types"] == 48, "unexpected carrier size")
    if args.write_fixtures:
        (HERE / "local_types.json").write_bytes(catalog_bytes)
        (HERE / "expected.json").write_bytes(encoded_json(report))
    else:
        require((HERE / "local_types.json").read_bytes() == catalog_bytes,
                "catalog differs entry by entry")
        expected = json.loads((HERE / "expected.json").read_text())
        require(report == expected, "expected validation report differs")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
