#!/usr/bin/env python3
"""Build compact physical UNSAT cores for the degree-44 action catalog."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time

from common import (N, PAIR_INDEX, SplitMix64, dpll, edge_partition,
                    maximal_partition_representatives, point_transitive,
                    read_catalog, records_from_supports, sampled_five, support)


REGULAR_INDICES = (1, 2, 3, 4)
MILESTONES = (30_000, 100_000, 300_000)
DPLL_WORK_LIMIT = 250_000


def core_for_action(index, partition):
    variable_count = 1 + max(partition)
    supports = {}
    rng = SplitMix64(0x5235355654343400 ^ index)
    draws = 0
    last_stats = None
    status = None
    for milestone in MILESTONES:
        while draws < milestone:
            five = sampled_five(rng)
            supports.setdefault(support(partition, five), five)
            draws += 1
        records = records_from_supports(supports)
        status, last_stats, _ = dpll(
            variable_count, [(x[0], x[1]) for x in records],
            work_limit=DPLL_WORK_LIMIT)
        if status is False:
            break
    if status is not False:
        for five in combinations(range(N), 5):
            supports.setdefault(support(partition, five), five)
        records = records_from_supports(supports)
        status, last_stats, _ = dpll(
            variable_count, [(x[0], x[1]) for x in records])
        draws = -1
    if status is True:
        raise RuntimeError(f"SAT invariant graph found for action {index}")
    if status is None:
        raise RuntimeError(f"unlimited DPLL was not run for action {index}")

    _, _, used = dpll(variable_count, [(x[0], x[1]) for x in records],
                      collect_reasons=True)
    core = [records[i] for i in sorted(used)]
    for _ in range(3):
        core_status, _, core_used = dpll(
            variable_count, [(x[0], x[1]) for x in core],
            collect_reasons=True)
        if core_status is not False:
            raise AssertionError(f"reason core is not UNSAT for {index}")
        if len(core_used) == len(core):
            break
        core = [core[i] for i in sorted(core_used)]
    check, core_stats, _ = dpll(
        variable_count, [(x[0], x[1]) for x in core])
    if check is not False:
        raise AssertionError(f"final core is not UNSAT for {index}")
    return {
        "index": index,
        "edge_orbits": variable_count,
        "sampling_draws": draws,
        "distinct_sampled_supports": len(supports),
        "clauses": [[color, *five] for _, _, color, five in core],
        "dpll": core_stats,
        "initial_dpll": last_stats,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--certificates", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    actions = read_catalog(args.catalog)
    partitions = []
    for index, _, generators in actions:
        if not point_transitive(generators):
            raise ValueError(f"action {index} is not transitive")
        partitions.append(edge_partition(generators))
    retained, unique = maximal_partition_representatives(partitions)
    if tuple(x for x in retained if x in REGULAR_INDICES) != REGULAR_INDICES:
        raise AssertionError("the four regular catalog actions must be retained")

    certificates = []
    for position, index in enumerate(retained, 1):
        if index in REGULAR_INDICES:
            continue
        item = core_for_action(index, partitions[index - 1])
        certificates.append(item)
        print(f"CERTIFIED {position}/{len(retained)} index={index} "
              f"orbits={item['edge_orbits']} clauses={len(item['clauses'])} "
              f"draws={item['sampling_draws']}", flush=True)

    payload = {
        "format": "r55-vertex-transitive44-physical-cores-v1",
        "catalog_sha256": sha256(args.catalog.read_bytes()).hexdigest(),
        "regular_indices_delegated_to_cayley44": list(REGULAR_INDICES),
        "retained_partition_representatives": list(retained),
        "certificates": certificates,
    }
    args.certificates.write_text(json.dumps(payload, separators=(",", ":")) + "\n")
    clause_counts = [len(item["clauses"]) for item in certificates]
    result = {
        "status": "COMPLETE_VERTEX_TRANSITIVE44_PUNCTURE_EXCLUSION",
        "catalog_actions": len(actions),
        "exact_labeled_edge_partitions": len(unique),
        "retained_maximal_partitions": len(retained),
        "prior_cayley44_partitions": len(REGULAR_INDICES),
        "new_physical_core_partitions": len(certificates),
        "edge_orbit_histogram_retained": dict(sorted(Counter(
            1 + max(partitions[index - 1]) for index in retained).items())),
        "core_clauses_total": sum(clause_counts),
        "core_clauses_max": max(clause_counts),
        "dpll_cached_states_total": sum(
            item["dpll"]["cached_states"] for item in certificates),
        "dpll_cached_states_max": max(
            item["dpll"]["cached_states"] for item in certificates),
        "full_fallback_actions": sum(
            item["sampling_draws"] == -1 for item in certificates),
        "certificate_sha256": sha256(args.certificates.read_bytes()).hexdigest(),
        "elapsed_seconds": time.monotonic() - started,
        "scope": "No good43 graph is constructed and no Ramsey lower bound is improved.",
    }
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
