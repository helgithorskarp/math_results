"""Positive, corrupted-coverage and genuine INCOMPLETE controls."""
from collections import Counter
from copy import deepcopy
from itertools import combinations
import json
import resource
import time

import produce
import verify
from common import Guard, Incomplete, HERE, WORK, encoded, load_input, require


def gf4_product(a, b):
    value = 0
    for unused in range(2):
        if b & 1:
            value ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return value


def affine_positive():
    lines = {tuple(4 * a + b for b in range(4)) for a in range(4)}
    lines.update(tuple(sorted(4 * a + (gf4_product(m, a) ^ c) for a in range(4)))
                 for m in range(4) for c in range(4))
    require(len(lines) == 20 and all(len(set(q)) == 4 for q in lines), "bad explicit positive packing")
    pair = Counter(e for q in lines for e in combinations(q, 2))
    require(set(pair) == set(combinations(range(16), 2)) and set(pair.values()) == {1}, "positive pair cover invalid")
    prefix = [q for q in lines if 0 in q]
    eligible = tuple(e for e in combinations(range(1, 16), 2) if not any(set(e) <= set(q) for q in prefix))
    columns = tuple(sorted(q for q in lines if 0 not in q))
    require(len(prefix) == 5 and len(eligible) == 90 and len(columns) == 15, "positive residual shape")
    try:
        produce.refute(eligible, columns)
    except produce.PositiveWitness as witness:
        selected = [columns[i] for i in witness.columns]
        cover = Counter(e for q in selected for e in combinations(q, 2))
        require(len(selected) == 15 and set(cover) == set(eligible) and set(cover.values()) == {1},
                "positive witness invalid")
        return {"lines": 20, "prefix": 5, "residual_columns": 15, "covered_pairs": 90}
    raise ValueError("producer incorrectly excluded the positive residual cover")


def run():
    started = time.monotonic()
    rejected, incomplete = [], []

    def rejection(name, function, message):
        try:
            function()
        except ValueError as exc:
            require(message in str(exc), "unexpected rejection for " + name + ": " + str(exc))
            rejected.append(name)
            return
        raise ValueError("corrupted control was accepted: " + name)

    def guarded(name, function):
        try:
            function()
        except Incomplete:
            incomplete.append(name)
            return
        raise ValueError("guarded control returned a purported complete result: " + name)

    blocks = load_input()
    certificate = json.loads((HERE / "certificate.json").read_text())
    root = WORK / "controls"
    root.mkdir(parents=True, exist_ok=True)

    def altered(name, mutate, message):
        data = deepcopy(certificate)
        mutate(data)
        path = root / (name + ".json")
        path.write_bytes(encoded(data))
        rejection(name, lambda: verify.run(path, write_report=False), message)

    altered("missing_automorphism", lambda c: c["automorphisms"].pop(), "full automorphism mismatch")
    altered("unordered_instead_of_marked", lambda c: c["ordered_absence_orbits"].pop(), "incomplete ordered absence carrier")
    altered("missing_marked_orientation", lambda c: c["fibers"].pop(), "missing ordered fiber")
    altered("missing_x_completion", lambda c: c["fibers"][0]["solutions"].pop(), "incomplete actual x-solution fiber")
    altered("missing_third_star_case", lambda c: c["fibers"][0]["refutations"].pop(), "missing refutation case")
    altered("changed_candidate_universe", lambda c: c["fibers"][0].update(x_columns_sha256="0" * 64),
            "actual x-column universe mismatch")
    altered("changed_joint_seed", lambda c: c["fibers"][0]["refutations"][0].update(seed_sha256="0" * 64),
            "actual joint-seed mismatch")
    altered("changed_a_candidate_universe", lambda c: c["fibers"][0]["refutations"][0].update(columns_sha256="0" * 64),
            "actual a-column universe mismatch")

    fiber = certificate["fibers"][0]
    columns = verify.literal_x_columns(blocks, tuple(fiber["absent"]))
    at = next(i for i, r in enumerate(fiber["refutations"]) if r["tree"][1])
    words = verify.literal_joint_seed(blocks, tuple(fiber["absent"]), columns, tuple(fiber["solutions"][at]))
    eligible, a_columns = verify.literal_a_model(words, fiber["absent"][0])
    tree = fiber["refutations"][at]["tree"]
    missing = deepcopy(tree)
    missing[1].pop()
    rejection("missing_pair_cover_branch", lambda: verify.check_tree(missing, eligible, a_columns),
              "incomplete or duplicate pair-cover branches")
    duplicate = deepcopy(tree)
    duplicate[1].append(deepcopy(duplicate[1][0]))
    rejection("duplicate_pair_cover_branch", lambda: verify.check_tree(duplicate, eligible, a_columns),
              "incomplete or duplicate pair-cover branches")
    bad_pair = deepcopy(tree)
    bad_pair[0] = len(eligible)
    rejection("invalid_branch_pair", lambda: verify.check_tree(bad_pair, eligible, a_columns), "bad branch pair")
    rejection("false_empty_domain", lambda: verify.check_tree([tree[0], []], eligible, a_columns),
              "incomplete or duplicate pair-cover branches")
    toy_pairs = tuple(combinations(range(4), 2))
    toy_columns = ((0, 1, 2, 3),)
    rejection("hidden_positive_column", lambda: verify.check_tree([0, []], toy_pairs, toy_columns),
              "incomplete or duplicate pair-cover branches")
    rejection("positive_cover_as_negative_leaf", lambda: verify.check_tree([0, [[0, [0, []]]]], toy_pairs, toy_columns),
              "refutation reaches an exact cover")

    guarded("clique_node_guard", lambda: produce.cliques(columns, nodes=0))
    guarded("whole_star_node_guard", lambda: verify.whole_point_stars(blocks, tuple(fiber["absent"]), columns, nodes=0))
    guarded("producer_cover_node_guard", lambda: produce.refute(eligible, a_columns, nodes=0))
    guarded("checker_cover_node_guard", lambda: verify.check_tree(tree, eligible, a_columns, nodes=0))
    guarded("point_map_time_guard", lambda: verify.point_maps(blocks, seconds=0))
    rejection("escalated_node_guard", lambda: Guard(nodes=200001), "invalid or escalated node guard")
    rejection("escalated_time_guard", lambda: Guard(seconds=10.01), "invalid or escalated time guard")

    positive = affine_positive()
    joint = tuple(tuple(w) for w in json.loads((HERE / "positive_seed.json").read_text()))
    require(len(joint) == len(set(joint)) == 35 and all(len(w) == len(set(w)) == 5 for w in joint),
            "bad35-word positive fixture")
    require(all(len(set(u) & set(v)) <= 2 for u, v in combinations(joint, 2)), "positive fixture collision")
    require(tuple(sorted(tuple(p for p in w if p != 17) for w in joint if 17 in w)) == blocks,
            "positive fixture does not contain the specified y star")
    require(sum(2 in w for w in joint) == 20 and sum(14 in w for w in joint) == 4,
            "positive fixture replication mismatch")
    require(all(not any(14 in w and a in w for w in joint) for a in (2, 9, 15, 16)),
            "positive fixture absence mismatch")
    toy_pool = ((0, 1, 2, 3), (0, 4, 5, 6), (1, 4, 7, 8), (0, 1, 5, 8))
    actual, unused, edges = produce.cliques(toy_pool, target=2)
    expected = tuple(c for c in combinations(range(len(toy_pool)), 2)
                     if len(set(toy_pool[c[0]]) & set(toy_pool[c[1]])) <= 1)
    require(actual == expected and edges == len(expected), "toy positive clique census mismatch")
    empty, unused, edges = produce.cliques((), target=1)
    require(empty == () and edges == 0, "empty clique boundary mismatch")
    report = {"agent": "six-code-3", "role": "researcher", "status": "ALL CONTROLS PASSED",
              "rejected_corruptions": rejected, "genuine_incomplete": incomplete,
              "positive_pair_cover": positive, "toy_cliques": len(expected),
              "positive_joint_words": 35, "positive_joint_hub_replication": 4,
              "seconds": time.monotonic() - started,
              "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (WORK / "controls.json").write_bytes(encoded(report))
    print(json.dumps(report, sort_keys=True))
    return report


if __name__ == "__main__":
    run()
