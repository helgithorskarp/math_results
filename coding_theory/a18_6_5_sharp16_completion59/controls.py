"""Certificate corruption checks and actual finite-guard controls."""
from copy import deepcopy
from itertools import combinations
import json
import resource
import time

from common import Guard, Incomplete, HERE, WORK, digest, encoded, load_input, require
from produce import cliques, pair_covers
from verify import literal_template, packing_census, point_maps, validate_certificate, whole_a_stars


def run():
    started = time.monotonic()
    blocks = load_input()
    # This generated cache is used only for controls after full verification.
    # verify.py itself always rebuilds every model from the literal input.
    models = json.loads((WORK / "literal_models.json").read_text())
    verification = json.loads((WORK / "verification.json").read_text())
    certificate = json.loads((HERE / "certificate.json").read_text())
    witness = json.loads((HERE / "witness.json").read_text())
    require(verification["status"].startswith("COMPLETE") and
            verification["certificate_sha256"] == digest(certificate), "controls need completed verification")
    validate_certificate(certificate, models, witness, blocks)
    rejected = []

    def corruption(label, change, witness_change=False):
        c, w = deepcopy(certificate), deepcopy(witness)
        change(w if witness_change else c)
        try:
            validate_certificate(c, models, w, blocks)
        except (ValueError, KeyError, IndexError, TypeError):
            rejected.append(label)
            return
        raise ValueError("corruption accepted: " + label)

    corruption("wrong_format", lambda c: c.update(format="other"))
    corruption("wrong_upper_bound", lambda c: c.update(upper_family_size=60))
    corruption("wrong_normalized_absence", lambda c: c.update(absent=9))
    corruption("missing_actual_map", lambda c: c["automorphisms"].pop())
    corruption("missing_orbit_point", lambda c: c["absence_orbit"].pop())
    corruption("wrong_pair_count", lambda c: c.update(a_pair_count=89))
    corruption("wrong_pair_hash", lambda c: c.update(a_pairs_sha256="0" * 64))
    corruption("wrong_a_column_count", lambda c: c.update(a_column_count=149))
    corruption("wrong_a_column_hash", lambda c: c.update(a_columns_sha256="0" * 64))
    corruption("missing_a_cover", lambda c: c["a_covers"].pop())
    corruption("duplicate_a_cover", lambda c: c["a_covers"].append(c["a_covers"][0]))
    corruption("missing_fiber", lambda c: c["fibers"].pop())
    corruption("wrong_seed35", lambda c: c["fibers"][0].update(seed35_sha256="0" * 64))
    corruption("wrong_x_count", lambda c: c["fibers"][0].update(x_column_count=0))
    corruption("wrong_x_pool", lambda c: c["fibers"][0].update(x_columns_sha256="0" * 64))
    corruption("missing_sharp_key", lambda c: c["fibers"][0]["sharp_keys"].pop())
    corruption("bad_sharp_key", lambda c: c["fibers"][0]["sharp_keys"][0].pop())
    corruption("missing_residual_case", lambda c: c["fibers"][0]["residuals"].pop())
    corruption("wrong_seed47", lambda c: c["fibers"][0]["residuals"][0].update(seed47_sha256="0" * 64))
    corruption("wrong_residual_count", lambda c: c["fibers"][0]["residuals"][0].update(column_count=0))
    corruption("wrong_residual_pool", lambda c: c["fibers"][0]["residuals"][0].update(columns_sha256="0" * 64))
    corruption("missing_partition_vertex", lambda c: c["fibers"][0]["residuals"][0]["conflict_partition"][0].pop())
    corruption("duplicate_partition_vertex", lambda c: c["fibers"][0]["residuals"][0]["conflict_partition"][0].append(0))

    large_case = next((f, j) for f, fiber in enumerate(models["fibers"])
                      for j, instance in enumerate(fiber["residuals"]) if len(instance["columns"]) >= 13)
    f, j = large_case
    corruption("more_than_twelve_groups", lambda c: c["fibers"][f]["residuals"][j].update(
        conflict_partition=[[i] for i in range(len(models["fibers"][f]["residuals"][j]["columns"]))]))
    # Preserve exact vertex coverage and the <=12 group count while placing
    # genuinely compatible words in one declared conflict group.
    f, j, u, v = next((f, j, u, v) for f, fiber in enumerate(models["fibers"])
                      for j, instance in enumerate(fiber["residuals"]) if len(instance["columns"]) <= 13
                      for u, v in combinations(range(len(instance["columns"])), 2)
                      if len(set(instance["columns"][u]) & set(instance["columns"][v])) <= 2)
    corruption("compatible_words_in_conflict_group", lambda c: c["fibers"][f]["residuals"][j].update(
        conflict_partition=[[u, v]] + [[i] for i in range(len(models["fibers"][f]["residuals"][j]["columns"]))
                                      if i not in (u, v)]))
    corruption("missing_witness_column", lambda c: c["witness"]["extra_columns"].pop())
    corruption("wrong_witness_hash", lambda c: c["witness"].update(words_sha256="0" * 64))
    corruption("wrong_witness_model", lambda w: w.update(case=6), True)
    corruption("duplicate_witness_word", lambda w: w["words"].append(w["words"][0]), True)
    corruption("witness_bad_weight", lambda w: w["words"][0].pop(), True)
    try:
        literal_template(blocks[:-1])
    except ValueError:
        rejected.append("incomplete_template")
    else:
        raise ValueError("incomplete template accepted")
    for label, kwargs in (("escalated_states", {"nodes": 200001}), ("escalated_seconds", {"seconds": 11}),
                          ("negative_states", {"nodes": -1}), ("boolean_states", {"nodes": True})):
        try:
            Guard(**kwargs)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError("invalid guard accepted")

    pool = models["fibers"][0]["x_columns"]
    eligible = tuple(tuple(e) for e in models["a_pairs"])
    incomplete = []
    jobs = [("producer_pair_cover", lambda: pair_covers(eligible, models["a_columns"], nodes=0)),
            ("independent_whole_star", lambda: whole_a_stars(eligible, models["a_columns"], nodes=0)),
            ("producer_clique", lambda: cliques(pool, target=12, nodes=0)),
            ("independent_binary", lambda: packing_census(pool, 12, nodes=0)),
            ("independent_point_map", lambda: point_maps(blocks, seconds=0))]
    for label, job in jobs:
        try:
            job()
        except Incomplete:
            incomplete.append(label)
            if label == "independent_binary":
                (WORK / "unfinished_case.json").replace(WORK / "guard_control_INCOMPLETE.json")
        else:
            raise ValueError("actual guard did not exit INCOMPLETE: " + label)

    # An exhaustively checked tiny instance exercises all positive leaves,
    # target zero, and negative memoization without repeating the full census.
    toy = ((0, 1, 2, 3), (0, 1, 4, 5), (0, 2, 6, 7), (4, 6, 8, 9))
    for target in range(5):
        expected = tuple(s for s in combinations(range(len(toy)), target)
                         if all(len(set(toy[i]) & set(toy[j])) <= 1 for i, j in combinations(s, 2)))
        literal, unused, unused2 = packing_census(toy, target)
        colored, unused, unused2 = cliques(toy, target)
        require(literal == colored == expected, "complete toy census mismatch")
    report = {"agent": "six-code-3", "role": "researcher", "status": "COMPLETE controls",
              "rejected_corruptions": rejected, "genuine_incomplete": incomplete,
              "positive_color_cases": 142, "literal_witness_words": 59,
              "complete_small_censuses": 5, "control_cache_only": True,
              "seconds": time.monotonic() - started,
              "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "controls.json").write_bytes(encoded(report))
    print(json.dumps(report, sort_keys=True))
    return report


if __name__ == "__main__":
    run()
