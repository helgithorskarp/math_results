"""Compact readout derived from complete independent results, not search input."""
from collections import Counter, deque
from itertools import combinations
import hashlib
import json
from pathlib import Path
from independent import bits, encoded, require, validate_words


def summary(record, raw_record):
    core, full = record["core"], record["full_core"]
    tails = full["tails"]
    sets = [frozenset(t) for t in tails]
    edges = [[i, j] for i, j in combinations(range(len(tails)), 2) if len(sets[i] ^ sets[j]) == 2]
    adjacent = [set() for _ in tails]
    for i, j in edges:
        adjacent[i].add(j)
        adjacent[j].add(i)
    reached, queue = {0}, deque([0])
    while queue:
        for j in adjacent[queue.popleft()]:
            if j not in reached:
                reached.add(j)
                queue.append(j)
    require(len(reached) == len(tails) == 84, "fixed-core component connectivity")
    require(not set.intersection(*(set(t) for t in tails)), "component common intersection")
    singles, pairs = record["one_deleted"], record["two_deleted"]
    exceptions = [[*r["deleted"], r["optima"][3][1]] for r in pairs if r["optima"][3][0] == 13]
    require(len(exceptions) == 66, "complete exceptional pair count")
    sharp = {"size69_tail": tails[0],
             "exact56_size68": {"omitted": singles[0]["deleted"], "tail": singles[0]["optima"][1][2]},
             "exact55_size68": [{"omitted": r["deleted"], "tail": r["optima"][3][2]}
                                 for r in pairs if r["optima"][3][0] == 13]}
    result = {
        "actual_agent": "six-reviewer-4", "role": "independent mathematical reviewer",
        "whole_record_sha256": hashlib.sha256(raw_record).hexdigest(),
        "whole_record_bytes": len(raw_record),
        "oracle_sha256": record["oracle_sha256"],
        "physical_words": record["universe_words"], "core_words": len(core),
        "blocker_histogram": record["blocker_histogram"],
        "full_core_compatible_words": len(full["words"]), "full_core_maximum_tail_and_count": full["maximum"],
        "full_core_tails_sha256": hashlib.sha256(encoded(tails)).hexdigest(),
        "component_edges": len(edges), "component_connected": True, "common_intersection_is_core": True,
        "pair_cases": len(pairs),
        "pair_candidate_histogram": [[n, count] for n, count in sorted(Counter(len(r["candidate_words"]) for r in pairs).items())],
        "unrestricted_pair_maximum_distribution": [[list(k), v] for k, v in sorted(Counter(tuple(r["optima"][0][:2]) for r in pairs).items())],
        "either_core_word_forbidden_distribution": [[list(k), v] for k, v in sorted(Counter(tuple(o[:2]) for r in pairs for o in r["optima"][1:3]).items())],
        "both_core_words_forbidden_distribution": [[list(k), v] for k, v in sorted(Counter(tuple(r["optima"][3][:2]) for r in pairs).items())],
        "singleton_cases": len(singles),
        "exact56_maximum_tail_and_count_distribution": [[list(k), v] for k, v in sorted(Counter(tuple(r["optima"][1][:2]) for r in singles).items())],
        "exact56_size68_codes": sum(r["optima"][1][1] for r in singles),
        "exact55_exceptional_pairs": len(exceptions), "exact55_other_pairs": len(pairs) - len(exceptions),
        "exact55_size68_codes": sum(r[2] for r in exceptions),
        "exception_inventory_sha256": hashlib.sha256(encoded(exceptions)).hexdigest(),
        "sharp_witnesses_sha256": hashlib.sha256(encoded(sharp)).hexdigest(),
        "pair_left_masks": sum(r["left_masks"] for r in pairs),
        "pair_right_masks": sum(r["right_masks"] for r in pairs),
        "pair_valid_left_masks": sum(r["valid_left_masks"] for r in pairs),
    }
    return result, exceptions, sharp, tails


def provenance(core, tails, identification, raw):
    require(hashlib.sha256(raw).hexdigest() == identification["prior_seed_sha256"], "credited ACL69 bytes")
    lines = raw.decode().splitlines()
    require(len(lines) == 69 and all(len(line) == 18 and set(line) <= {"0", "1"} for line in lines), "ACL row decoding")
    original = [sum(1 << i for i, b in enumerate(line) if b == "1") for line in lines]
    validate_words(original)
    point_map = identification["old_to_new_point_mapping"]
    require(sorted(point_map) == list(range(18)), "actual point identification")
    deleted = identification["prior_removed_seed_rows"]
    require(len(deleted) == len(set(deleted)) == 12 and all(1 <= i <= 69 for i in deleted), "prior row deletion")
    def image(word):
        return sum(1 << point_map[p] for p in bits(word))
    images = [image(w) for w in original]
    require(set(core) == {w for i, w in enumerate(images, 1) if i not in deleted}, "prior literal core identification")
    require(sorted(set(images) - set(core)) in tails, "credited seed belongs to full inventory")
    return {"old_core_identification": True, "mapped_acl69_in_complete84": True,
            "raw_acl69_sha256": hashlib.sha256(raw).hexdigest(), "acl_word_pairs": 2346}


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("record", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    args.output.mkdir(exist_ok=True)
    raw_record = args.record.read_bytes()
    record = json.loads(raw_record)
    result, exceptions, sharp, tails = summary(record, raw_record)
    root = Path(__file__).parent
    result["identification"] = provenance(record["core"], tails, json.loads((root / "IDENTIFICATION.json").read_bytes()), (root / "acl69.txt").read_bytes())
    for name, data in (("expected.json", result), ("EXACT55_EXCEPTIONS.json", exceptions),
                       ("SHARP_TAILS.json", sharp), ("FULL_CORE_TAILS.json", tails)):
        (args.output / name).write_bytes(encoded(data))
    print(json.dumps(result, sort_keys=True))
