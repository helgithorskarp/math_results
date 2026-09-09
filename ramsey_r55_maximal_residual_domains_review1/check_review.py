"""Reviewer-owned checks for the maximal residual-domain carrier bound."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import struct
import sys
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def stable(value):
    if isinstance(value, dict):
        return {key: stable(item) for key, item in value.items() if key != "seconds"}
    if isinstance(value, list):
        return [stable(item) for item in value]
    return value


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_graph6(word: str, expected_order: int) -> list[int]:
    require(word and ord(word[0]) - 63 == expected_order, "graph6 order")
    bits: list[int] = []
    for character in word[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, "graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    need = expected_order * (expected_order - 1) // 2
    require(len(bits) >= need, "truncated graph6")
    adjacency = [0] * expected_order
    position = 0
    for right in range(1, expected_order):
        for left in range(right):
            if bits[position]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            position += 1
    return adjacency


def direct_profile(adjacency: list[int]) -> tuple[list[int], int]:
    """Definition-level submask enumeration; no zeta or recurrence."""
    n = len(adjacency)
    triangles: list[int] = []
    for a, b, c in combinations(range(n), 3):
        if (adjacency[a] >> b) & 1 and (adjacency[a] >> c) & 1 and (adjacency[b] >> c) & 1:
            triangles.append((1 << a) | (1 << b) | (1 << c))
    valid = [all(mask & triangle != triangle for triangle in triangles) for mask in range(1 << n)]
    profile = [0] * (1 << n)
    incidences = 0
    for container in range(1 << n):
        subset = container
        while True:
            profile[container] += valid[subset]
            incidences += 1
            if subset == 0:
                break
            subset = (subset - 1) & container
    cover = sum((1 if (n - mask.bit_count()) % 2 == 0 else -1) * value**4 for mask, value in enumerate(profile))
    return profile, cover


def local_checks(target: Path, data: Path, replay: Path) -> dict:
    pins = json.loads((target / "INPUTS.json").read_text())
    checked = 0
    entries = 0
    incidences = 0
    selections: dict[str, list[int]] = {}
    for pin in pins:
        n = pin["order"]
        graphs = (data / pin["file"]).read_text().splitlines()
        rows = [line.split() for line in (replay / "census-sequential" / str(n) / "COUNTS.tsv").read_text().splitlines()]
        require(len(graphs) == len(rows) == pin["count"], "catalogue coverage")
        covers = [int(row[3]) for row in rows]
        if n <= 7:
            indices = list(range(len(graphs)))
        else:
            indices = sorted({0, len(graphs) // 2, len(graphs) - 1, covers.index(min(covers)), covers.index(max(covers))})
        selections[str(n)] = f"all 0..{len(graphs) - 1}" if n <= 7 else indices
        words = 1 << n
        with (replay / "census-sequential" / str(n) / "PROFILES.bin").open("rb") as profiles:
            for index in indices:
                require(int(rows[index][0]) == index and rows[index][1] == graphs[index], "count-row identity")
                profile, cover = direct_profile(parse_graph6(graphs[index], n))
                profiles.seek(index * words * 2)
                submitted = list(struct.unpack(f"<{words}H", profiles.read(words * 2)))
                require(profile == submitted, f"profile mismatch order {n} index {index}")
                require(profile[-1] == int(rows[index][2]), "triangle-free total")
                require(cover == int(rows[index][3]), "cover total")
                checked += 1
                entries += words
                incidences += 3**n
    return {
        "status": "REVIEWER_DEFINITION_LEVEL_PROFILES_VERIFIED",
        "cores": checked,
        "profile_entries": entries,
        "direct_submask_incidences": incidences,
        "selections": selections,
    }


def rational(value: dict) -> Fraction:
    return Fraction(value["numerator"], value["denominator"])


def global_checks(target: Path, data: Path, replay: Path) -> dict:
    claim = json.loads((replay / "GLOBAL.json").read_text())
    parent = json.loads((target.parent / "ramsey_r55_three_block_entropy" / "EXPECTED.json").read_text())["global_bound"]
    contacts = [list(map(int, line.split())) for line in (target.parent / "ramsey_r55_q9_core_contact_domains" / "COUNTS.tsv").read_text().splitlines()]
    covers: dict[int, list[int]] = {}
    for pin in json.loads((target / "INPUTS.json").read_text()):
        n = pin["order"]
        rows = [line.split() for line in (replay / "census-sequential" / str(n) / "COUNTS.tsv").read_text().splitlines()]
        covers[n] = [int(row[3]) for row in rows]

    total = Fraction()
    affected: dict[int, int] = {}
    tasks = 0
    for row in claim["classes"]:
        q, r = row["q"], row["r"]
        n = 43 - 4 * q
        blue_blocks = q - r
        red_children = r - 1
        root = comb(1998 + red_children - 1, red_children) * comb(1931 + blue_blocks - 1, blue_blocks)
        pair = 37823 ** (comb(red_children, 2) + comb(blue_blocks, 2)) * 35714 ** (red_children * blue_blocks)
        factor = root * pair
        if q == 9:
            new_terms = []
            old_terms = []
            for index, plain, joint, opposite, _permutation in contacts:
                require(index == len(new_terms), "q9 row order")
                old_blue = contacts[opposite][1]
                new_blue = min(covers[n][index], old_blue)
                new_terms.append(joint**r * new_blue**blue_blocks)
                old_terms.append(joint**r * old_blue**blue_blocks)
        else:
            red_domain = {7: 15**15, 8: 2433780807 * 15**3, 10: 15**3}[q]
            new_terms = [red_domain**r * value**blue_blocks for value in covers[n]]
            old_terms = [red_domain**r * (15**n) ** blue_blocks for _ in covers[n]]
        new_contact = factor * sum(new_terms)
        old_contact = factor * sum(old_terms)
        prior = next(item for item in parent["classes"] if (item["q"], item["r"]) == (q, r))
        beta = rational(prior["probability_upper"])
        before = beta * old_contact
        after = beta * new_contact
        require(old_contact == prior["before"] == row["contact_parent_sum"], "old class factorization")
        require(before == rational(row["before_upper"]), "old weighted class")
        require(new_contact == row["contact_bound_sum"] and after == rational(row["after_upper"]), "new weighted class")
        strict = sum(new < old for new, old in zip(new_terms, old_terms))
        require(strict == row["strictly_improved_tasks"], "class task impact")
        affected[q] = affected.get(q, 0) + strict
        total += after
        tasks += len(covers[n])
    before = rational(claim["before_upper"])
    require(tasks == claim["task_ids"] == 2_189_178, "global task coverage")
    require(total == rational(claim["after_upper"]), "global sum")
    require(total / before == rational(claim["ratio_to_previous_upper"]), "global ratio")
    require(sum(affected.values()) == claim["strictly_improved_task_bounds"], "global task impact")
    require(affected == {7: 1280, 8: 1639068, 9: 1412, 10: 5}, "per-q task impact")
    require(2 * total <= before and claim["gate"] == "PASS", "declared factor-two gate")
    return {
        "status": "REVIEWER_GLOBAL_RESIDUAL_BOUND_VERIFIED",
        "classes": 18,
        "task_ids": tasks,
        "strictly_improved_task_bounds": sum(affected.values()),
        "strictly_improved_by_q": {str(key): value for key, value in sorted(affected.items())},
        "ratio_numerator": (total / before).numerator,
        "ratio_denominator": (total / before).denominator,
    }


def replay_checks(target: Path, data: Path, replay: Path) -> dict:
    sys.path.insert(0, str(target))
    verify_module = load_module("submitted_verify_global", target / "verify_global.py")
    expected = json.loads((target / "EXPECTED.json").read_text())
    census = stable(json.loads((replay / "census-sequential" / "CENSUS.json").read_text()))
    global_bound = json.loads((replay / "GLOBAL.json").read_text())
    independent = verify_module.verify(replay / "census-sequential", data, replay / "GLOBAL.json")
    corruptions = sorted((replay / "normal-corruptions").glob("*.json"))
    require(len(corruptions) == 6, "global corruption corpus")
    for path in corruptions:
        try:
            verify_module.verify(replay / "census-sequential", data, path)
        except (ValueError, KeyError):
            pass
        else:
            raise ValueError(f"corruption accepted: {path.name}")
    actual = {
        "census": census,
        "global_bound": global_bound,
        "global_corruptions": {"status": "GLOBAL_RESIDUAL_CORRUPTIONS_REJECTED", "cases": 6},
        "independent": independent,
        "literal": stable(json.loads((replay / "normal-literal" / "VALIDATION.json").read_text())),
        "physical": json.loads((replay / "normal-physical" / "PHYSICAL.json").read_text()),
        "sanitized": json.loads((replay / "sanitizer" / "SANITIZED.json").read_text()),
    }
    require(actual == expected, "replayed stable result differs from EXPECTED.json")
    require(stable(json.loads((replay / "optimized-literal" / "VALIDATION.json").read_text())) == actual["literal"], "normal/-O literal evidence")
    require(json.loads((replay / "optimized-physical" / "PHYSICAL.json").read_text()) == actual["physical"], "normal/-O physical evidence")
    require((replay / "normal-physical" / "FIXTURES.json").read_bytes() == (target / "FIXTURES.json").read_bytes(), "fixture bytes")
    result_bytes = (json.dumps(actual, sort_keys=True, indent=2) + "\n").encode()
    return {
        "status": "REVIEWER_STABLE_TARGET_REPLAY_VERIFIED",
        "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
        "expected_sha256": sha256(target / "EXPECTED.json"),
        "catalogue_count_hashes": {str(item["order"]): item["count_sha256"] for item in census["catalogues"]},
        "catalogue_profile_hashes": {str(item["order"]): item["profile_sha256"] for item in census["catalogues"]},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("data")
    parser.add_argument("replay")
    parser.add_argument("out")
    args = parser.parse_args()
    target, data, replay = map(lambda value: Path(value).resolve(), (args.target, args.data, args.replay))
    result = {
        "target_replay": replay_checks(target, data, replay),
        "local_definition": local_checks(target, data, replay),
        "global_arithmetic": global_checks(target, data, replay),
    }
    Path(args.out).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
