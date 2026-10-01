"""Bitset clique census and exact-pair-cover refutation-tree producer."""
from collections import Counter
from itertools import combinations, permutations, product
import argparse
import json
import resource
import time

from common import Guard, Incomplete, HERE, WORK, digest, encoded, load_input, require


class PositiveWitness(Exception):
    def __init__(self, columns):
        self.columns = tuple(columns)


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


def ordered_orbits(points, maps):
    unseen = set(permutations(points, 2))
    orbits = []
    while unseen:
        key = min(unseen)
        orbit = tuple(sorted({(p[key[0]], p[key[1]]) for p in maps}))
        require(set(orbit) <= unseen, "ordered-orbit overlap or escape")
        unseen.difference_update(orbit)
        orbits.append(orbit)
    return tuple(orbits)


def x_columns(blocks, absent):
    active = sorted(set(range(18)) - {14, 17, *absent})
    seed = tuple(frozenset((17,) + q) for q in blocks)
    return tuple(q for q in combinations(active, 4)
                 if all(len((set(q) | {14}) & word) <= 2 for word in seed))


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


def joint_seed(blocks, columns, solution):
    words = tuple(sorted([tuple(sorted((17,) + q)) for q in blocks]
                         + [tuple(sorted((14,) + columns[i])) for i in solution]))
    require(len(words) == len(set(words)) == 31 and all(len(w) == 5 for w in words), "wrong joint seed")
    require(all(len(set(u) & set(v)) <= 2 for u, v in combinations(words, 2)), "joint seed collision")
    require(sum(14 in w for w in words) == 15 and sum(17 in w for w in words) == 20, "bad seed replications")
    return words


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


def refute(eligible, columns, nodes=200000, seconds=10):
    index = {e: i for i, e in enumerate(eligible)}
    require(len(index) == len(eligible), "duplicated eligible pair")
    masks = []
    for q in columns:
        require(len(q) == 4 and tuple(sorted(set(q))) == q, "bad refutation column")
        edges = tuple(combinations(q, 2))
        require(all(e in index for e in edges), "column escapes residual pair universe")
        masks.append(sum(1 << index[e] for e in edges))
    guard = Guard(nodes, seconds)

    def visit(free, chosen):
        guard.tick()
        if not free:
            raise PositiveWitness(chosen)
        legal = [i for i, mask in enumerate(masks) if mask & free == mask]
        domains = [(tuple(i for i in legal if masks[i] & (1 << e)), e)
                   for e in range(len(eligible)) if free >> e & 1]
        choices, edge = min(domains, key=lambda item: (len(item[0]), item[1]))
        branches = [[i, visit(free ^ masks[i], chosen + (i,))] for i in choices]
        return [edge, branches]

    tree = visit((1 << len(eligible)) - 1, ())
    return tree, guard.nodes


def run(output):
    started = time.monotonic()
    blocks = load_input()
    group, group_nodes = automorphisms(blocks)
    highs, leave, core, cohorts = inspect_template(blocks)
    orbits = ordered_orbits(cohorts[14], group)
    require(len(group) == 8 and tuple(len(o) for o in orbits) == (4, 4, 4), "unexpected ordered carrier")
    certificate = {"format": "ordered-two-absence-v1", "automorphisms": group,
                   "ordered_absence_orbits": orbits, "fibers": []}
    full_census = {"models": []}
    reports = []
    for orbit in orbits:
        absent = orbit[0]
        columns = x_columns(blocks, absent)
        solutions, count, edges = cliques(columns)
        fiber = {"absent": absent, "x_column_count": len(columns), "x_columns_sha256": digest(columns),
                 "solutions": solutions, "refutations": []}
        full_model = {"absent": absent, "columns": columns, "solutions": solutions, "a_instances": []}
        a_nodes = []
        a_counts = []
        for solution in solutions:
            words = joint_seed(blocks, columns, solution)
            eligible, a_columns = a_model(words, absent[0])
            tree, tree_nodes = refute(eligible, a_columns)
            full_model["a_instances"].append({"solution": solution, "seed": words,
                                              "eligible": eligible, "columns": a_columns})
            fiber["refutations"].append({"seed_sha256": digest(words), "columns_sha256": digest(a_columns),
                                         "column_count": len(a_columns), "tree": tree, "nodes": tree_nodes})
            a_nodes.append(tree_nodes)
            a_counts.append(len(a_columns))
        certificate["fibers"].append(fiber)
        full_census["models"].append(full_model)
        reports.append({"absent": absent, "x_candidates": len(columns), "x_graph_edges": edges,
                        "x_completions": len(solutions), "x_nodes": count,
                        "a_candidate_counts": a_counts, "a_nodes": a_nodes})
    output.write_bytes(encoded(certificate))
    report = {"agent": "six-code-3", "role": "researcher", "status": "COMPLETE",
              "input_blocks_sha256": digest(blocks), "certificate_sha256": digest(certificate),
              "group_order": len(group), "group_leave_maps": group_nodes, "fibers": reports,
              "x_completions": sum(r["x_completions"] for r in reports),
              "a_refutation_nodes": sum(sum(r["a_nodes"]) for r in reports),
              "seconds": time.monotonic() - started,
              "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "full_census.json").write_bytes(encoded(full_census))
    (WORK / "producer.json").write_bytes(encoded(report))
    print(json.dumps({k: v for k, v in report.items() if k != "fibers"}, sort_keys=True))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=lambda p: HERE / p, default=HERE / "certificate.json")
    args = parser.parse_args()
    try:
        run(args.output)
    except Incomplete as exc:
        print(str(exc))
        raise SystemExit(2)
    except PositiveWitness as exc:
        print("SATISFIABLE: pair-cover witness; no exclusion", list(exc.columns))
        raise SystemExit(3)
