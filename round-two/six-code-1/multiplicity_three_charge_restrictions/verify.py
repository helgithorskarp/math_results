"""Exact readout of the published nineteen-star carrier and charge inventories.

Author: six-code-1, researcher. This does not reprove census completeness or
the imported twenty-star lemmas. All mathematical checks remain active under -O.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST_SHA = "83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca"
BASELINE_SHA = "cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d"


def check(ok, message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def mask(points):
    return sum(1 << x for x in points)


def literal_model(lengths):
    holes = set()
    start = 0
    for size in lengths:
        for i in range(size):
            holes.add((start+i, start+i))
            holes.add((start+i, start+(i+1) % size))
        start += size
    cells = sorted(set(product(range(5), repeat=2))-holes)
    anchors = [frozenset([15]+[i for i, rc in enumerate(cells) if rc[0] == r])
               for r in range(5)]
    anchors += [frozenset([16]+[i for i, rc in enumerate(cells) if rc[1] == c])
                for c in range(5)]
    forbidden = {p for w in anchors for p in combinations(sorted(w), 2)}
    candidates = [frozenset(w) for w in combinations(range(15), 4)
                  if not any(p in forbidden for p in combinations(w, 2))]
    return anchors, candidates


def matching_model(lengths):
    # Separate row/column-injection decoder; no four-point subset filtering.
    missing = {}
    offset = 0
    for size in lengths:
        for row in range(offset, offset+size):
            missing[row] = {row, offset+(row-offset+1) % size}
        offset += size
    occupied = [(r, c) for r in range(5) for c in range(5) if c not in missing[r]]
    lookup = {rc: i for i, rc in enumerate(occupied)}
    anchors = []
    for row in range(5):
        anchors.append(mask([15]+[lookup[row, c] for c in range(5)
                                  if (row, c) in lookup]))
    for col in range(5):
        anchors.append(mask([16]+[lookup[r, col] for r in range(5)
                                  if (r, col) in lookup]))
    candidates = set()
    for rows in combinations(range(5), 4):
        for cols in permutations(range(5), 4):
            if all((r, c) in lookup for r, c in zip(rows, cols)):
                candidates.add(tuple(sorted(lookup[r, c] for r, c in zip(rows, cols))))
    return anchors, [mask(w) for w in sorted(candidates)]


def inspect_literal(words):
    check(len(words) == len(set(words)) == 19, "not nineteen distinct blocks")
    check(all(len(w) == 4 and all(type(x) is int and 0 <= x < 17 for x in w)
              for w in words), "invalid block")
    pairs = [p for w in words for p in combinations(sorted(w), 2)]
    check(len(pairs) == len(set(pairs)) == 114, "repeated covered pair")
    rho = [sum(x in w for w in words) for x in range(17)]
    check(max(rho) <= 5, "replication exceeds five")
    deficient = {x for x, r in enumerate(rho) if r < 5}
    leave = set(combinations(range(17), 2))-set(pairs)
    e = sum(set(p) <= deficient for p in leave)
    mu = sum(set(p).isdisjoint(deficient) for p in leave)
    check(e-mu == len(deficient)+5 and len(leave) == 22, "leave identity")
    stats = {"positive_deficits": sorted(5-r for r in rho if r < 5),
             "low_low_pairs": mu, "high_high_pairs": e,
             "homogeneous_pairs": e+mu}
    if stats["positive_deficits"] != [1]*7+[2]:
        return stats, None
    u = rho.index(3)
    W = deficient-{u}
    low = set(range(17))-deficient
    C = {y for w in words if u in w for y in w if y != u}
    check(len(C) == 9 and len(W) == 7, "marked three-star sizes")
    ll = sorted(p for p in leave if set(p) <= low)
    charges = Counter()
    for a, b in leave:
        if a in C & low and b in W:
            charges[b] += 1
        if b in C & low and a in W:
            charges[a] += 1
    return stats, {"marked_point": u, "mu": mu, "C": sorted(C),
                   "W_in_C": sorted(W & C), "low_low_edges": [list(p) for p in ll],
                   "low_low_endpoints_in_C": sum(y in C for p in ll for y in p),
                   "forced_W_charges": [list(p) for p in sorted(charges.items())]}


def inspect_masks(words):
    check(len(set(words)) == len(words) == 19, "invalid mask block count")
    rho = [0]*17
    owner = [[-1]*17 for _ in range(17)]
    for index, word in enumerate(words):
        check(type(word) is int and word >= 0 and word >> 17 == 0
              and word.bit_count() == 4, "invalid mask")
        points = [x for x in range(17) if word >> x & 1]
        for x in points:
            rho[x] += 1
            for y in points:
                if x < y:
                    check(owner[x][y] == -1, "two masks own the same pair")
                    owner[x][y] = index
    check(max(rho) <= 5 and sum(rho) == 76, "mask replication")
    high = [r < 5 for r in rho]
    leave = [(x, y) for x in range(17) for y in range(x+1, 17)
             if owner[x][y] == -1]
    e = sum(high[x] and high[y] for x, y in leave)
    mu = sum(not high[x] and not high[y] for x, y in leave)
    stats = {"positive_deficits": sorted(5-r for r in rho if r < 5),
             "low_low_pairs": mu, "high_high_pairs": e,
             "homogeneous_pairs": e+mu}
    if stats["positive_deficits"] != [1]*7+[2]:
        return stats, None
    u = next(x for x, r in enumerate(rho) if r == 3)
    covered = 0
    for word in words:
        if word >> u & 1:
            covered |= word
    covered &= ~(1 << u)
    C = [x for x in range(17) if covered >> x & 1]
    wc = [x for x in C if high[x]]
    ll = [[x, y] for x, y in leave if not high[x] and not high[y]]
    charges = []
    for w in range(17):
        if not high[w] or w == u:
            continue
        count = sum(owner[min(w, x)][max(w, x)] == -1
                    for x in C if not high[x])
        if count:
            charges.append([w, count])
    return stats, {"marked_point": u, "mu": mu, "C": C, "W_in_C": wc,
                   "low_low_edges": ll,
                   "low_low_endpoints_in_C": sum(x in C for pair in ll for x in pair),
                   "forced_W_charges": charges}


def charge_inventory(rows):
    survivors = []
    tested = 0
    for row in rows:
        q = dict(row["forced_W_charges"])
        for X in (0, 1):
            for c in range(4):
                for z in range(4):
                    # The published incidence inequalities, using b >= c.
                    if 2*X+z+c > 3 or 5*c-z+X > 13:
                        continue
                    for tc in combinations(row["W_in_C"], c):
                        tested += 1
                        R = 3-z+c-2*X
                        forced = sum(max(q.get(y, 0), 2 if y in tc else 0)
                                     for y in set(q) | set(tc))
                        if forced <= R:
                            survivors.append({"model": row["model"], "class": row["class"],
                                              "X": X, "c": c, "z": z,
                                              "T_in_C": list(tc), "R": R,
                                              "forced_W_charge": forced, "mu": row["mu"]})
    check(len(survivors) == 3, "unexpected charge-bound survivors")
    check(all(s["mu"] == 2 and s["X"] == s["c"] == s["z"] == 0
              and s["R"] == s["forced_W_charge"] == 3 for s in survivors),
          "survivor hypotheses changed")
    # Their further exclusion uses the written shared-isolated-hub argument.
    return {"tested_assignments": tested, "survivors_before_written_pair_exclusion": survivors}


def no_low_low_inventory():
    survivors = []
    for p in range(8):
        for cW in range(p+1):
            if 6+cW > p*(p-1)//2 or 5*p+cW > 20+p*(p-1)//2:
                continue
            for X in (0, 1):
                for c in range(min(cW, 3)+1):
                    for z in range(4):
                        if 2*X+z+c > 3 or 5*c-z+X > 13:
                            continue
                        R = 3-z+c-2*X
                        if 9-cW <= R:
                            survivors.append([p, cW, X, c, z])
    check(all(s[2] == 0 and s[3] <= 2 for s in survivors), "X or c restriction failed")
    zero_c = [s for s in survivors if s[3] == 0]
    check(zero_c == [[7, 6, 0, 0, 0]], "zero-overlap boundary changed")
    check(4*26 > 21+3*27, "independent nine-point capacity contradiction")
    final = []
    exclusions = []
    for p, cW, X, c, z in survivors:
        check(X == 0, "internal excess remained")
        R = 3-z+c
        QW = max(9-cW, 2*c)
        h = R-QW
        a = 16-p-z
        minimum_D = 5*a-19+c
        if minimum_D > 27+4*h:
            exclusions.append([p, cW, c, z, "degree", minimum_D, 27+4*h])
        elif h == 0 and 4*minimum_D > (p+z)*(p+z-1)//2+3*27:
            exclusions.append([p, cW, c, z, "capacity", 4*minimum_D,
                               (p+z)*(p+z-1)//2+3*27])
        else:
            final.append([p, cW, c, z])
    check(final == [[7, 5, 2, 0], [7, 5, 2, 1],
                    [7, 6, 1, 0], [7, 6, 1, 1],
                    [7, 6, 2, 0], [7, 6, 2, 1]], f"final inventory changed: {final}")
    return {"surviving_necessary_inventories": survivors,
            "zero_c_boundary": zero_c, "capacity_contradiction": [104, 102],
            "degree_or_capacity_exclusions": exclusions,
            "final_necessary_inventories_p_k_c_z": final}


def controls(words, masks):
    rejected = 0
    malformed = [words[:-1], words[:-1]+[words[0]],
                 words[:-1]+[frozenset([0, 1, 2, 17])],
                 words[:-1]+[frozenset([0, 1, 2])]]
    for bad in malformed:
        try:
            inspect_literal(bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("malformed literal packing accepted")
    for bad in [masks[:-1], masks[:-1]+[masks[0]],
                masks[:-1]+[(1 << 17) | 7], masks[:-1]+[7]]:
        try:
            inspect_masks(bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("malformed mask packing accepted")
    return rejected


def final_charge_patterns(inventories):
    """Every covered-low assignment allowed by the final charge budgets.

    The terminal contradiction is the written isolated-hub lemma, not a
    computational claim that these necessary charge patterns are packings.
    """
    output = []
    for p, k, c, z in inventories:
        check(p == 7, "final W carrier size")
        # Relabel the c distinguished T_C centers as 0,...,c-1. This is
        # only a parameter relabeling, not a symmetry assumption on a code.
        low_count = 9-k
        W_budget = 2+c
        valid = []
        tested = 0
        for partners in product(range(7), repeat=low_count):
            tested += 1
            q = Counter(partners)
            minimum = [max(q.get(y, 0), 2 if y < c else 0) for y in range(7)]
            if sum(minimum) > W_budget:
                continue
            check(sum(minimum) == W_budget, "unexpected free W charge")
            choices = [t for t in range(c) if q[t] >= 2 and q[t] == minimum[t]]
            check(choices, "no fully forced common-T center")
            t = choices[0]
            friends = [i for i, y in enumerate(partners) if y == t]
            check(len(friends) >= 2, "not two distinct covered-low neighbors")
            # For z=1 at most one friend can be Z; for z=0 at most one
            # can be the unique charged A center. Every other friend is
            # a good A center. Exhaust even the cases where none is bad.
            for exception in [None]+list(range(low_count)):
                check(any(i != exception for i in friends), "no good A neighbor")
            valid.append([list(partners), minimum, t])
        expected_count = 19 if c == 1 else 6
        check(len(valid) == expected_count, "charge-pattern coverage changed")
        output.append({"inventory_p_k_c_z": [p, k, c, z], "tested": tested,
                       "valid_patterns": len(valid), "W_charge_budget": W_budget,
                       "pattern_witness_sha256": hashlib.sha256(encode(valid)).hexdigest(),
                       "every_pattern_has_forced_common_T_and_good_A_friend": True})
    check(sum(row["tested"] for row in output) == 6174, "pattern domain count")
    check(sum(row["valid_patterns"] for row in output) == 62, "pattern survivor count")
    return output


def baseline():
    data = (HERE / "acl69.txt").read_bytes()
    check(hashlib.sha256(data).hexdigest() == BASELINE_SHA, "baseline hash")
    lines = data.decode().splitlines()
    check(len(lines) == 69 and all(len(s) == 18 and set(s) <= {"0", "1"} for s in lines),
          "baseline binary format")
    words = [int(s, 2) for s in lines]
    check(len(set(words)) == 69 and all(w.bit_count() == 5 for w in words), "baseline words")
    distances = Counter((a ^ b).bit_count() for a, b in combinations(words, 2))
    check(min(distances) == 6, "baseline distance")
    rho = sorted(Counter(sum(w >> x & 1 for w in words) for x in range(18)).items())
    return {"sha256": BASELINE_SHA, "words": 69, "minimum_distance": 6,
            "replication_counts": [list(p) for p in rho],
            "distance_counts": [list(p) for p in sorted(distances.items())]}


def run():
    data = (HERE / "NINETEEN_STARS.json").read_bytes()
    check(hashlib.sha256(data).hexdigest() == MANIFEST_SHA, "imported manifest hash")
    manifest = json.loads(data)
    check(manifest["format"] == "nineteen-star-census-v1", "manifest format")
    rows, all_count = [], 0
    rejected = 0
    for mi, model in enumerate(manifest["models"]):
        first, columns = literal_model(model["cycle_half_lengths"])
        second, masks = matching_model(model["cycle_half_lengths"])
        check([mask(w) for w in first] == second, "anchor entry mismatch")
        check([mask(w) for w in columns] == masks, "candidate entry mismatch")
        check(len(columns) == model["candidate_count"], "candidate count")
        for ci, entry in enumerate(model["marked_classes"]):
            words = first+[columns[i] for i in entry["clique"]]
            bits = second+[masks[i] for i in entry["clique"]]
            stats, row = inspect_literal(words)
            alternate_stats, alternate_row = inspect_masks(bits)
            check(stats == alternate_stats and row == alternate_row, "readout entry mismatch")
            check(all(stats[k] == entry[k] for k in stats), "published statistics mismatch")
            all_count += 1
            if row is not None:
                row = {"model": mi, "class": ci, "blocks": sorted(mask(w) for w in words), **row}
                check(row["low_low_endpoints_in_C"] == 2*row["mu"],
                      "low-low endpoint property")
                rows.append(row)
        rejected += controls(words, bits)
    check(all_count == 46 and len(rows) == 13, "carrier coverage")
    check(Counter(r["mu"] for r in rows) == {1: 10, 2: 3}, "mu coverage")
    inventory = no_low_low_inventory()
    return {"format": "m3-charge-exclusion-v1", "actual_agent": "six-code-1",
            "role": "researcher", "imported_manifest_sha256": MANIFEST_SHA,
            "marked_classes_decoded": all_count, "relevant_marked_classes": rows,
            "low_low_charge_inventory": charge_inventory(rows),
            "no_low_low_inventory": inventory,
            "final_shared_hub_charge_patterns": final_charge_patterns(
                inventory["final_necessary_inventories_p_k_c_z"]),
            "malformed_controls_rejected": rejected, "historical_baseline": baseline()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.write_expected:
        (HERE / "expected.json").write_bytes(encode(result))
    else:
        check(result == json.loads((HERE / "expected.json").read_text()), "expected record mismatch")
    print(json.dumps({"status": "COMPLETE", "marked_classes_decoded": 46,
                      "relevant_classes": 13, "residual_cases_requiring_written_pair_exclusion": 3,
                      "final_charge_patterns_for_written_hub_exclusion": 62,
                      "manifest_sha256": hashlib.sha256(encode(result)).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
