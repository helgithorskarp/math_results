"""Exact bitset pair-cover census and compatibility-clique producer."""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import resource
import time

from common import Guard, Incomplete, HERE, WORK, digest, encoded, load_input, require

def inspect_template(blocks):
    require(len(blocks) == 20 and tuple(sorted(set(blocks))) == blocks, "bad producer template size/order")
    require(all(len(q) == 4 and tuple(sorted(set(q))) == q and all(type(p) is int and 0 <= p < 17 for p in q)
                for q in blocks), "bad producer quadruple")
    rep = Counter(p for q in blocks for p in q)
    counts = Counter(e for q in blocks for e in combinations(q, 2))
    require(sorted(rep.values()) == [4] * 5 + [5] * 12 and set(counts.values()) == {1}, "bad template incidence")
    highs = tuple(p for p in range(17) if rep[p] == 4)
    leave = set(combinations(range(17), 2)) - set(counts)
    core = {e for e in leave if set(e) <= set(highs)}
    require(14 in highs and len(core) == 4 and all(14 not in e for e in core), "bad marked high core")
    require(all(sum(p in e for e in core) == (0 if p == 14 else 2) for p in highs), "bad C4+isolated core")
    cohorts = {h: tuple(p for p in range(17) if p not in highs and tuple(sorted((h, p))) in leave) for h in highs}
    require(sorted(p for cohort in cohorts.values() for p in cohort) == sorted(set(range(17)) - set(highs)),
            "low-point leave cohorts do not partition")
    require(len(cohorts[14]) == 4 and all(len(cohorts[h]) == 2 for h in highs if h != 14), "bad cohort sizes")
    return highs, leave, core, cohorts

def automorphisms(blocks):
    highs, leave, core, cohorts = inspect_template(blocks)
    others = tuple(h for h in highs if h != 14)
    answers = []
    guard = Guard()
    for image in permutations(others):
        upper = dict(zip(others, image)) | {14: 14}
        if {tuple(sorted(upper[p] for p in e)) for e in core} != core:
            continue
        for targets in product(*(tuple(permutations(cohorts[upper[h]])) for h in highs)):
            guard.tick()
            mapping = upper.copy()
            for h, target in zip(highs, targets):
                mapping.update(zip(cohorts[h], target))
            p = tuple(mapping[z] for z in range(17))
            require(set(p) == set(range(17)), "nonbijective leave map")
            require({tuple(sorted(p[z] for z in e)) for e in leave} == leave, "bad leave automorphism")
            if {tuple(sorted(p[z] for z in q)) for q in blocks} == set(blocks):
                answers.append(p)
    require(len(set(answers)) == len(answers), "duplicate automorphism")
    return tuple(sorted(answers)), guard.nodes

def cliques(columns, target=11, nodes=200000, seconds=10):
    n = len(columns)
    masks = tuple(sum(1 << j for j in range(n) if i != j and len(set(columns[i]) & set(columns[j])) <= 1)
                  for i in range(n))
    guard = Guard(nodes, seconds)
    answers = []

    def visit(available, chosen):
        guard.tick()
        if len(chosen) == target:
            answers.append(tuple(sorted(chosen)))
            return
        temporary = available
        order, bounds = [], []
        color = 0
        while temporary:
            color += 1
            independent = temporary
            while independent:
                bit = independent & -independent
                v = bit.bit_length() - 1
                order.append(v)
                bounds.append(color)
                temporary ^= bit
                independent &= ~bit & ~masks[v]
        for at in range(len(order) - 1, -1, -1):
            if len(chosen) + bounds[at] < target:
                return
            v = order[at]
            visit(available & masks[v], chosen + (v,))
            available &= ~(1 << v)

    visit((1 << n) - 1, ())
    require(len(set(answers)) == len(answers), "duplicate clique path")
    return tuple(sorted(answers)), guard.nodes, sum(mask.bit_count() for mask in masks) // 2

def a_model(words, a):
    active = sorted(set(range(18)) - {14, 17, a})
    prefix = tuple(tuple(p for p in w if p != a) for w in words if a in w)
    require(len(prefix) == 5 and all(17 in q and 14 not in q for q in prefix), "bad absent-star prefix")
    used = Counter(e for q in prefix for e in combinations(q, 2))
    require(set(used.values()) == {1}, "prefix pair collision")
    require(sorted(p for q in prefix for p in q if p != 17) == active, "prefix tails do not partition")
    eligible = tuple(e for e in combinations(active, 2) if e not in used)
    raw = tuple(q for q in combinations(active, 4) if not any(e in used for e in combinations(q, 2)))
    columns = tuple(q for q in raw if all(len((set(q) | {a}) & set(w)) <= 2 for w in words))
    require(len(eligible) == 90 and len(raw) == 405, "bad residual pair-cover carrier")
    return eligible, columns

def pair_covers(eligible, columns, nodes=200000, seconds=10):
    index = {e: i for i, e in enumerate(eligible)}
    masks = tuple(sum(1 << index[e] for e in combinations(q, 2)) for q in columns)
    incidence = tuple(sum(1 << i for i, mask in enumerate(masks) if mask >> e & 1)
                      for e in range(len(eligible)))
    compatible = tuple(sum(1 << j for j, other in enumerate(masks)
                           if not mask & other) for mask in masks)
    guard = Guard(nodes, seconds)
    answers = []

    def visit(free, available, chosen):
        guard.tick()
        if not free:
            answers.append(tuple(sorted(chosen)))
            return
        if available.bit_count() * 6 < free.bit_count():
            return
        pivot = min((e for e in range(len(eligible)) if free >> e & 1),
                    key=lambda e: ((incidence[e] & available).bit_count(), e))
        choices = incidence[pivot] & available
        while choices:
            bit = choices & -choices
            i = bit.bit_length() - 1
            require(masks[i] & free == masks[i], "candidate mask escapes free pairs")
            visit(free ^ masks[i], available & compatible[i], chosen + (i,))
            choices ^= bit

    visit((1 << len(eligible)) - 1, (1 << len(columns)) - 1, ())
    require(len(answers) == len(set(answers)), "duplicate exact-cover path")
    return tuple(sorted(answers)), guard.nodes


def a_seed(blocks, columns, solution):
    words = tuple(sorted(tuple(tuple(sorted((17,) + q)) for q in blocks) +
                         tuple(tuple(sorted((2,) + columns[i])) for i in solution)))
    require(len(solution) == 15 and len(words) == len(set(words)) == 35, "wrong a seed size")
    require(all(len(set(u) & set(v)) <= 2 for u, v in combinations(words, 2)), "a seed collision")
    require(sum(2 in w for w in words) == sum(17 in w for w in words) == 20 and
            sum(14 in w for w in words) == 4, "wrong a seed replication")
    return words


def x_columns(words):
    active = tuple(p for p in range(18) if p not in (2, 14, 17))
    return tuple(q for q in combinations(active, 4)
                 if all(len((set(q) | {14}) & set(w)) <= 2 for w in words))


def run(output):
    started = time.monotonic()
    blocks = load_input()
    group, group_nodes = automorphisms(blocks)
    orbit = tuple(sorted({p[2] for p in group}))
    require(len(group) == 8 and orbit == (2, 9, 15, 16), "incomplete single-absence normalization")
    y_words = tuple(tuple(sorted((17,) + q)) for q in blocks)
    eligible, columns = a_model(y_words, 2)
    covers, cover_nodes = pair_covers(eligible, columns)
    require(len(columns) == 150 and len(covers) == 6, "unexpected complete a census")
    manifest = {"format": "single-absence-replay-manifest-v1", "absent": 2,
                "automorphisms": group, "absence_orbit": orbit,
                "a_pair_count": len(eligible), "a_pairs_sha256": digest(eligible),
                "a_column_count": len(columns), "a_columns_sha256": digest(columns),
                "a_covers": covers, "fibers": []}
    full = {"automorphisms": group, "absence_orbit": orbit, "y_seed": y_words,
            "a_pairs": eligible, "a_columns": columns, "a_covers": covers, "fibers": []}
    reports = []
    witness_words = None
    for case, cover in enumerate(covers):
        words = a_seed(blocks, columns, cover)
        pool = x_columns(words)
        negatives, nodes, edges = cliques(pool, target=13)
        require(not negatives, "POSITIVE replication17 witness; sharp16 exclusion fails")
        fiber = {"a_cover": cover, "seed_sha256": digest(words), "x_column_count": len(pool),
                 "x_columns_sha256": digest(pool), "x_graph_edges": edges, "excluded_extra_count": 13}
        manifest["fibers"].append(fiber)
        full["fibers"].append({"a_cover": cover, "seed": words, "x_columns": pool})
        reports.append({"case": case, "x_column_count": len(pool), "x_graph_edges": edges,
                        "target": 13, "clique_count": 0, "nodes": nodes})
        if case == 0:
            positives, positive_nodes, unused = cliques(pool, target=12)
            require(bool(positives), "no sharpness witness at replication16")
            key = positives[0]
            witness_words = tuple(sorted(words + tuple(tuple(sorted((14,) + pool[i])) for i in key)))
            require(len(witness_words) == len(set(witness_words)) == 47 and
                    all(len(set(u) & set(v)) <= 2 for u, v in combinations(witness_words, 2)),
                    "sharpness witness collision")
            manifest["witness"] = {"case": 0, "x_columns": key, "words_sha256": digest(witness_words)}
    witness = {"format": "literal-three-star-witness-v1", "point_count": 18,
               "x": 14, "y": 17, "a": 2, "words": witness_words}
    require(json.loads((HERE / "witness.json").read_text()) == json.loads(encoded(witness)),
            "supplied witness differs from exact regenerated witness")
    output.write_bytes(encoded(manifest))
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "full_census.json").write_bytes(encoded(full))
    report = {"agent": "six-code-3", "role": "researcher", "status": "COMPLETE author computation",
              "input_blocks_sha256": digest(blocks), "manifest_sha256": digest(manifest),
              "group_order": len(group), "group_leave_maps": group_nodes,
              "a_pair_count": len(eligible), "a_column_count": len(columns), "a_covers": len(covers),
              "a_pair_cover_nodes": cover_nodes, "fibers": reports,
              "excluded_extra_count": 13, "sharp_hub_replication": 16,
              "witness_word_count": len(witness_words), "witness_words_sha256": digest(witness_words),
              "witness_census_nodes": positive_nodes,
              "seconds": time.monotonic() - started,
              "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (WORK / "producer.json").write_bytes(encoded(report))
    print(json.dumps({k: v for k, v in report.items() if k != "fibers"}, sort_keys=True))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=lambda p: HERE / p, default=HERE / "manifest.json")
    args = parser.parse_args()
    try:
        run(args.output)
    except Incomplete as exc:
        print(str(exc))
        raise SystemExit(2)
