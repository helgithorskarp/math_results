#!/usr/bin/env python3
"""Independent finite checks for the universal split-path theorem.

The reference oracle follows every legal cycle move recursively and never
uses transfer messages.  The tested theorem implementation instead evaluates
signed path messages.  Finite agreement corroborates the proof; it is not an
extrapolation to untested orders or masses.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
from math import comb
from pathlib import Path
import platform
import random

from cycle_split_transfer import (
    cycle_split_witness,
    path_root_scores,
    spanning_path_stackable,
    verify_witness,
)


ROOT = Path(__file__).resolve().parent


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def raw_cycle_oracle(order: int):
    """Return a direct move-DAG stackability oracle for one cycle order."""

    @lru_cache(None)
    def stackable(configuration: tuple[int, ...]) -> bool:
        if sum(value > 0 for value in configuration) == 1:
            return True
        for source, value in enumerate(configuration):
            if value < 2:
                continue
            for target in ((source - 1) % order, (source + 1) % order):
                child = list(configuration)
                child[source] -= 2
                child[target] += 1
                if stackable(tuple(child)):
                    return True
        return False

    return stackable


def raw_path_oracle(order: int):
    """Return reachable stacked targets under direct legal path moves."""

    @lru_cache(None)
    def targets(configuration: tuple[int, ...]) -> int:
        support = [vertex for vertex, value in enumerate(configuration) if value]
        mask = 1 << support[0] if len(support) == 1 else 0
        for source, value in enumerate(configuration):
            if value < 2:
                continue
            for target in (source - 1, source + 1):
                if not 0 <= target < order:
                    continue
                child = list(configuration)
                child[source] -= 2
                child[target] += 1
                mask |= targets(tuple(child))
        return mask

    return targets


def path_transfer_check(digest) -> dict[str, int]:
    """Check the path-message implementation against a targetwise raw oracle."""

    configurations = 0
    target_decisions = 0
    oracle_states = 0
    for order in range(1, 8):
        oracle = raw_path_oracle(order)
        for mass in range(0, 11):
            for configuration in compositions(mass, order):
                truth = oracle(configuration)
                scores = path_root_scores(configuration)
                decision = sum(
                    1 << target
                    for target, score in enumerate(scores)
                    if score >= 1
                )
                if decision != truth:
                    raise AssertionError(
                        ("path transfer mismatch", configuration, truth, scores)
                    )
                digest.update(
                    json.dumps(
                        ["path", order, configuration, truth, scores],
                        separators=(",", ":"),
                    ).encode()
                )
                configurations += 1
                target_decisions += order
        oracle_states += oracle.cache_info().currsize
    return {
        "orders": 7,
        "maximum_mass": 10,
        "configurations": configurations,
        "target_decisions": target_decisions,
        "oracle_states": oracle_states,
    }


def exhaustive_check(order: int, maximum_mass: int, digest) -> dict[str, int]:
    oracle = raw_cycle_oracle(order)
    configurations = 0
    stackable = 0
    nonstackable = 0
    for mass in range(1, maximum_mass + 1):
        level_count = 0
        for configuration in compositions(mass, order):
            truth = oracle(configuration)
            witness = cycle_split_witness(configuration)
            decision = witness is not None
            if decision != truth:
                raise AssertionError((order, mass, configuration, truth, witness))
            if witness is not None and not verify_witness(configuration, witness):
                raise AssertionError(("invalid witness", configuration, witness))
            digest.update(
                json.dumps(
                    [order, configuration, truth, witness],
                    separators=(",", ":"),
                    sort_keys=True,
                ).encode()
            )
            level_count += 1
            stackable += truth
        expected_level = comb(mass + order - 1, order - 1)
        if level_count != expected_level:
            raise AssertionError((order, mass, level_count, expected_level))
        configurations += level_count
    nonstackable = configurations - stackable
    return {
        "order": order,
        "maximum_mass": maximum_mass,
        "configurations": configurations,
        "oracle_states": oracle.cache_info().currsize,
        "stackable": stackable,
        "nonstackable": nonstackable,
    }


def reverse_move_instances(digest) -> dict[str, int]:
    """Test larger cycles on configurations with explicit stacking ancestry."""

    rng = random.Random(20260920)
    instances = 0
    for order in range(8, 16):
        for _ in range(2000):
            configuration = [0] * order
            configuration[rng.randrange(order)] = rng.randrange(1, 5)
            reverse_steps = rng.randrange(1, 61)
            for _ in range(reverse_steps):
                target = rng.choice(
                    [vertex for vertex, value in enumerate(configuration) if value]
                )
                source = (target + rng.choice((-1, 1))) % order
                configuration[target] -= 1
                configuration[source] += 2
            configuration = tuple(configuration)
            witness = cycle_split_witness(configuration)
            if witness is None or not verify_witness(configuration, witness):
                raise AssertionError(("reverse instance failed", configuration))
            digest.update(
                json.dumps(
                    [order, configuration, witness],
                    separators=(",", ":"),
                    sort_keys=True,
                ).encode()
            )
            instances += 1
    return {"orders": 8, "instances": instances, "seed": 20260920}


def strict_gain_examples() -> list[dict[str, object]]:
    examples = [
        (0, 1, 1, 0, 6),
        (0, 0, 1, 1, 0, 0, 15),
    ]
    result = []
    for configuration in examples:
        witness = cycle_split_witness(configuration)
        if witness is None or not verify_witness(configuration, witness):
            raise AssertionError(("missing strict-gain witness", configuration))
        if spanning_path_stackable(configuration):
            raise AssertionError(("ordinary path unexpectedly suffices", configuration))
        oracle = raw_cycle_oracle(len(configuration))
        if not oracle(configuration):
            raise AssertionError(("example is not cycle-stackable", configuration))
        result.append(
            {
                "configuration": list(configuration),
                "witness": witness,
                "every_spanning_path_fails": True,
            }
        )
    return result


def rejection_checks() -> int:
    configuration = (0, 1, 1, 0, 6)
    witness = cycle_split_witness(configuration)
    assert witness is not None
    malformed = [
        None,
        [],
        {"cut": 4},
        {**witness, "extra": 0},
        {**witness, "cut": -1},
        {**witness, "left_pile": configuration[witness["cut"]] + 1},
        {**witness, "target": len(configuration) + 1},
        {**witness, "root_score": witness["root_score"] + 1},
        {**witness, "left_pile": 1.0},
    ]
    for candidate in malformed:
        if verify_witness(configuration, candidate):
            raise AssertionError(("accepted malformed witness", candidate))
    return len(malformed)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check-expected",
        action="store_true",
        help="compare the complete result with EXPECTED.json",
    )
    args = parser.parse_args()
    digest = hashlib.sha256()
    domains = [
        exhaustive_check(order, maximum_mass, digest)
        for order, maximum_mass in ((3, 8), (4, 10), (5, 12), (6, 12), (7, 17))
    ]
    result = {
        "status": "PASS",
        "python": platform.python_version(),
        "exact_integer_arithmetic": True,
        "exhaustive_domains": domains,
        "exhaustive_configurations": sum(x["configurations"] for x in domains),
        "path_transfer_checks": path_transfer_check(digest),
        "reverse_move_checks": reverse_move_instances(digest),
        "strict_gain_examples": strict_gain_examples(),
        "malformed_witnesses_rejected": rejection_checks(),
        "canonical_check_sha256": digest.hexdigest(),
    }
    if args.check_expected:
        expected = json.loads((ROOT / "EXPECTED.json").read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError(
                "result differs from EXPECTED.json\n"
                + json.dumps(result, indent=2, sort_keys=True)
            )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
