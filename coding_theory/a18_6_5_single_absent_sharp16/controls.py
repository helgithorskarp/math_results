"""Carrier/witness corruption checks, positive controls and actual guard exits."""
from copy import deepcopy
from itertools import combinations
import json
import resource
import time

from common import Guard, Incomplete, HERE, WORK, encoded, load_input, require
from produce import cliques, pair_covers
from verify import audit_models, compare_manifest, literal_template, packing_decision, point_maps, whole_a_stars


def run():
    started = time.monotonic()
    blocks = load_input()
    models = audit_models(blocks)
    manifest = json.loads((HERE / "manifest.json").read_text())
    witness = json.loads((HERE / "witness.json").read_text())
    compare_manifest(manifest, models, witness, blocks)
    rejected = []

    def corruption(label, change, witness_change=False):
        m, w = deepcopy(manifest), deepcopy(witness)
        change(w if witness_change else m)
        try:
            compare_manifest(m, models, w, blocks)
        except (ValueError, KeyError, IndexError, TypeError):
            rejected.append(label)
            return
        raise ValueError("corruption accepted: " + label)

    corruption("missing_actual_map", lambda m: m["automorphisms"].pop())
    corruption("missing_absence_orbit_point", lambda m: m["absence_orbit"].pop())
    corruption("wrong_normalized_absence", lambda m: m.update(absent=9))
    corruption("wrong_pair_count", lambda m: m.update(a_pair_count=89))
    corruption("wrong_pair_universe_hash", lambda m: m.update(a_pairs_sha256="0" * 64))
    corruption("wrong_a_pool_hash", lambda m: m.update(a_columns_sha256="0" * 64))
    corruption("missing_actual_cover", lambda m: m["a_covers"].pop())
    corruption("duplicate_cover", lambda m: m["a_covers"].append(m["a_covers"][0]))
    corruption("missing_hub_instance", lambda m: m["fibers"].pop())
    corruption("wrong_seed", lambda m: m["fibers"][0].update(seed_sha256="0" * 64))
    corruption("wrong_hub_pool", lambda m: m["fibers"][0].update(x_columns_sha256="0" * 64))
    corruption("wrong_graph_edge_count", lambda m: m["fibers"][0].update(x_graph_edges=0))
    corruption("weaker_exclusion_target", lambda m: m["fibers"][0].update(excluded_extra_count=14))
    corruption("missing_witness_column", lambda m: m["witness"]["x_columns"].pop())
    corruption("wrong_witness_hash", lambda m: m["witness"].update(words_sha256="0" * 64))
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
    incomplete = []
    jobs = [("producer_pair_cover", lambda: pair_covers(models["a_pairs"], models["a_columns"], nodes=0)),
            ("independent_whole_star", lambda: whole_a_stars(models["a_pairs"], models["a_columns"], nodes=0)),
            ("producer_clique", lambda: cliques(pool, target=13, nodes=0)),
            ("independent_binary", lambda: packing_decision(pool, 13, nodes=0)),
            ("independent_point_map", lambda: point_maps(blocks, seconds=0))]
    for label, job in jobs:
        try:
            job()
        except Incomplete:
            incomplete.append(label)
        else:
            raise ValueError("actual guard did not exit INCOMPLETE: " + label)

    positive, positive_nodes, unused = packing_decision(pool, 12)
    require(positive is not None, "independent algorithm failed actual twelve-column positive control")
    positive_words = tuple(sorted(models["fibers"][0]["seed"] +
                                 tuple(tuple(sorted((14,) + pool[i])) for i in positive)))
    require(len(positive_words) == 47 and len(set(positive_words)) == 47 and
            all(len(set(u) & set(v)) <= 2 for u, v in combinations(positive_words, 2)),
            "independent positive restored collision")
    # Distinct quadruples sharing a pair admit one block and exclude two.
    toy = ((0, 1, 2, 3), (0, 1, 4, 5), (0, 1, 6, 7))
    toy_positive, unused, unused2 = packing_decision(toy, 1)
    toy_negative, unused, unused2 = packing_decision(toy, 2)
    require(toy_positive is not None and toy_negative is None, "toy exact decision control failed")
    report = {"agent": "six-code-3", "role": "researcher", "status": "COMPLETE controls",
              "rejected_corruptions": rejected, "genuine_incomplete": incomplete,
              "positive_a_covers": len(models["a_covers"]), "positive_hub_replication": 16,
              "positive_binary_nodes": positive_nodes, "literal_witness_words": 47,
              "small_positive_and_negative_decisions": True,
              "seconds": time.monotonic() - started,
              "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "controls.json").write_bytes(encoded(report))
    print(json.dumps(report, sort_keys=True))
    return report


if __name__ == "__main__":
    run()
