"""Producer-free point-incidence, whole-point-star and literal certificate audit."""
from collections import Counter
from itertools import combinations, permutations
from math import comb
import argparse
import json
import resource
import time

from common import Guard, Incomplete, HERE, WORK, digest, encoded, load_input, require


def literal_template(blocks):
    require(len(blocks) == 20 and tuple(sorted(set(blocks))) == blocks, "bad literal template order/size")
    require(all(len(q) == 4 and tuple(sorted(set(q))) == q and all(type(p) is int and 0 <= p <= 16 for p in q)
                for q in blocks), "bad literal block")
    require(all(len(set(u) & set(v)) <= 1 for u, v in combinations(blocks, 2)), "template pair repeated")
    incidence = {p: sum(p in q for q in blocks) for p in range(17)}
    require(sorted(incidence.values()) == [4] * 5 + [5] * 12, "wrong literal replication profile")
    highs = {p for p, n in incidence.items() if n == 4}
    uncovered = {e for e in combinations(range(17), 2) if not any(set(e) <= set(q) for q in blocks)}
    core = {e for e in uncovered if set(e) <= highs}
    require(14 in highs and len(core) == 4 and all(14 not in e for e in core), "wrong marked isolated core")
    require(all(sum(p in e for e in core) == (0 if p == 14 else 2) for p in highs), "core is not C4+K1")
    neighbors = tuple(p for p in range(17) if p != 14 and tuple(sorted((14, p))) in uncovered)
    require(len(neighbors) == 4 and not set(neighbors) & highs, "bad absent-point carrier")
    return incidence, neighbors


def point_maps(blocks, nodes=200000, seconds=10):
    rep, unused = literal_template(blocks)
    pairs = {e for q in blocks for e in combinations(q, 2)}
    triples = {e for q in blocks for e in combinations(q, 3)}
    mapping, used = {14: 14}, {14}
    answers = []
    guard = Guard(nodes, seconds)

    def options(p):
        out = []
        for q in range(17):
            if q in used or rep[p] != rep[q]:
                continue
            if any((tuple(sorted((p, z))) in pairs) != (tuple(sorted((q, t))) in pairs)
                   for z, t in mapping.items()):
                continue
            if any((tuple(sorted((p, a, b))) in triples) !=
                   (tuple(sorted((q, mapping[a], mapping[b]))) in triples) for a, b in combinations(mapping, 2)):
                continue
            out.append(q)
        return out

    def visit():
        guard.tick()
        if len(mapping) == 17:
            p = tuple(mapping[z] for z in range(17))
            if {tuple(sorted(p[z] for z in q)) for q in blocks} == set(blocks):
                answers.append(p)
            return
        source = [p for p in range(17) if p not in mapping and rep[p] == 4]
        if not source:
            source = [p for p in range(17) if p not in mapping]
        choices, p = min(((options(p), p) for p in source), key=lambda item: (len(item[0]), item[1]))
        for q in choices:
            mapping[p] = q
            used.add(q)
            visit()
            used.remove(q)
            del mapping[p]

    visit()
    require(len(set(answers)) == len(answers), "duplicate literal point map")
    return tuple(sorted(answers)), guard.nodes


def literal_ordered_orbits(neighbors, maps):
    carrier = set(permutations(neighbors, 2))
    classes = {tuple(sorted({(p[a], p[b]) for p in maps})) for a, b in carrier}
    require(all(set(c) <= carrier for c in classes), "literal orbit escapes carrier")
    require(sum(len(c) for c in classes) == len(carrier) and set().union(*(set(c) for c in classes)) == carrier,
            "literal ordered orbits do not partition")
    return tuple(sorted(classes))


def literal_x_columns(blocks, absent):
    initial = tuple(tuple(sorted((17,) + q)) for q in blocks)
    return tuple(tuple(p for p in word if p != 14) for word in combinations(range(18), 5)
                 if 14 in word and 17 not in word and not set(absent) & set(word)
                 and all(len(set(word) & set(v)) <= 2 for v in initial))


def whole_point_stars(blocks, absent, columns, nodes=200000, seconds=10):
    initial = tuple(tuple(sorted((17,) + q)) for q in blocks)
    common = tuple(tuple(p for p in word if p != 14) for word in initial if 14 in word)
    active = sorted(set(range(18)) - {14, 17, *absent})
    rep = Counter(p for q in common for p in q)
    demand = {p: 4 - rep[p] for p in active}
    require(len(common) == 4 and sum(demand.values()) == 44, "bad independent x demand")
    require(sorted(demand.values()) == [3] * 12 + [4] * 2, "bad independent x quotas")
    pairsets = tuple(frozenset(combinations(q, 2)) for q in columns)
    colsets = tuple(frozenset(q) for q in columns)
    initial_used = frozenset(e for q in common for e in combinations(q, 2))
    answers = []
    guard = Guard(nodes, seconds)

    def visit(remaining, used, chosen):
        guard.tick()
        if not any(remaining.values()):
            answers.append(tuple(sorted(chosen)))
            return
        legal = [i for i, q in enumerate(columns)
                 if pairsets[i].isdisjoint(used) and all(remaining[p] > 0 for p in q)]
        if len(legal) < sum(remaining.values()) // 4:
            return
        options = {}
        for p, need in remaining.items():
            if not need:
                continue
            opts = [i for i in legal if p in colsets[i]]
            if len(opts) < need or len(set().union(*(colsets[i] - {p} for i in opts))) < 3 * need:
                return
            options[p] = opts
        p = min(options, key=lambda z: (comb(len(options[z]), remaining[z]), z))
        need = remaining[p]
        opts = options[p]
        tails = {i: colsets[i] - {p} for i in opts}

        def star(suffix, selected, consumed):
            guard.tick()
            missing = need - len(selected)
            if not missing:
                updated = remaining.copy()
                for i in selected:
                    for z in columns[i]:
                        updated[z] -= 1
                require(min(updated.values()) >= 0 and updated[p] == 0, "whole-star quota error")
                visit(updated, used | frozenset(e for i in selected for e in pairsets[i]), chosen + tuple(selected))
                return
            eligible = [i for i in suffix if tails[i].isdisjoint(consumed)]
            if len(eligible) < missing or len(set().union(*(tails[i] for i in eligible))) < 3 * missing:
                return
            for at, i in enumerate(eligible):
                star(eligible[at + 1:], selected + [i], consumed | tails[i])

        star(opts, [], frozenset())

    visit(demand, initial_used, ())
    require(len(set(answers)) == len(answers), "duplicate whole-star completion")
    return tuple(sorted(answers)), guard.nodes


def literal_joint_seed(blocks, absent, columns, solution):
    require(len(solution) == 11 and tuple(sorted(set(solution))) == solution and
            all(type(i) is int and 0 <= i < len(columns) for i in solution), "invalid x completion key")
    initial = [tuple(sorted((17,) + q)) for q in blocks]
    extra = [tuple(sorted((14,) + columns[i])) for i in solution]
    words = tuple(sorted(initial + extra))
    require(len(words) == len(set(words)) == 31 and all(len(set(w)) == 5 for w in words), "invalid literal seed")
    require(all(len(set(u) & set(v)) <= 2 for u, v in combinations(words, 2)), "literal seed collision")
    require(sum(14 in w for w in words) == 15 and sum(17 in w for w in words) == 20, "literal seed replication")
    require(all(not any(14 in w and a in w for w in words) for a in absent), "absence lost")
    support = set(range(18)) - {14, *absent}
    require(all(sum(14 in w and p in w for w in words) == 4 for p in support), "x pair degree is not four")
    return words


def literal_a_model(words, a):
    prefix = tuple(tuple(p for p in w if p != a) for w in words if a in w)
    active = tuple(p for p in range(18) if p not in (14, 17, a))
    require(len(prefix) == 5 and all(17 in q and 14 not in q for q in prefix), "literal prefix failure")
    require(all(len(set(u) & set(v)) == 1 for u, v in combinations(prefix, 2)), "prefix tails overlap")
    require(set().union(*(set(q) - {17} for q in prefix)) == set(active), "prefix tails incomplete")
    eligible = tuple(e for e in combinations(active, 2) if not any(set(e) <= set(q) for q in prefix))
    universe = tuple(w for w in combinations(range(18), 5) if a in w and 14 not in w and 17 not in w)
    prefix_legal = tuple(w for w in universe if all(len(set(w) & (set(q) | {a})) <= 2 for q in prefix))
    columns = tuple(tuple(p for p in w if p != a) for w in prefix_legal
                    if all(len(set(w) & set(v)) <= 2 for v in words))
    require(len(eligible) == 90 and len(prefix_legal) == 405, "literal carrier cardinality")
    require(all(sum(p in e for e in eligible) == 12 for p in active), "residual pair degree")
    require(all(set(combinations(q, 2)) <= set(eligible) for q in columns), "literal column escapes carrier")
    return eligible, columns


def check_tree(tree, eligible, columns, nodes=200000, seconds=10):
    pairs = tuple(frozenset(combinations(q, 2)) for q in columns)
    require(len(set(eligible)) == len(eligible) and len(set(columns)) == len(columns), "duplicate literal cover input")
    require(all(len(q) == 4 and tuple(sorted(set(q))) == q for q in columns), "invalid literal cover column")
    require(all(len(es) == 6 and es <= set(eligible) for es in pairs), "literal pair-cover column invalid")
    guard = Guard(nodes, seconds)

    def visit(node, free):
        guard.tick()
        require(bool(free), "refutation reaches an exact cover")
        require(type(node) is list and len(node) == 2, "bad certificate node")
        edge, branches = node
        require(type(edge) is int and 0 <= edge < len(eligible) and eligible[edge] in free, "bad branch pair")
        require(type(branches) is list and all(type(b) is list and len(b) == 2 for b in branches), "bad branch list")
        choices = {i for i, es in enumerate(pairs) if eligible[edge] in es and es <= free}
        declared = [b[0] for b in branches]
        require(all(type(i) is int for i in declared) and len(set(declared)) == len(declared) and set(declared) == choices,
                "incomplete or duplicate pair-cover branches")
        for i, child in branches:
            visit(child, free - pairs[i])

    visit(tree, frozenset(eligible))
    return guard.nodes


def run(certificate_path, write_report=True, compare_producer=False):
    started = time.monotonic()
    blocks = load_input()
    certificate = json.loads(certificate_path.read_text())
    primary = json.loads((WORK / "full_census.json").read_text()) if compare_producer else None
    require(certificate["format"] == "ordered-two-absence-v1", "wrong certificate format")
    rep, neighbors = literal_template(blocks)
    group, group_nodes = point_maps(blocks)
    require(tuple(tuple(p) for p in certificate["automorphisms"]) == group, "full automorphism mismatch")
    orbits = literal_ordered_orbits(neighbors, group)
    require(tuple(tuple(tuple(v) for v in o) for o in certificate["ordered_absence_orbits"]) == orbits,
            "incomplete ordered absence carrier")
    require(len(group) == 8 and tuple(len(o) for o in orbits) == (4, 4, 4), "unexpected literal orbit mass")
    require([f["absent"] for f in certificate["fibers"]] == [list(o[0]) for o in orbits], "missing ordered fiber")
    reports = []
    for model_index, fiber in enumerate(certificate["fibers"]):
        absent = tuple(fiber["absent"])
        columns = literal_x_columns(blocks, absent)
        require(len(columns) == fiber["x_column_count"] and digest(columns) == fiber["x_columns_sha256"],
                "actual x-column universe mismatch")
        solutions, census_nodes = whole_point_stars(blocks, absent, columns)
        require(solutions == tuple(tuple(s) for s in fiber["solutions"]), "incomplete actual x-solution fiber")
        require(len(fiber["refutations"]) == len(solutions), "missing refutation case")
        if primary:
            first = primary["models"][model_index]
            require(tuple(first["absent"]) == absent and tuple(tuple(q) for q in first["columns"]) == columns and
                    tuple(tuple(s) for s in first["solutions"]) == solutions,
                    "entrywise producer x-carrier or solution mismatch")
            require(len(first["a_instances"]) == len(solutions), "entrywise producer a-carrier coverage mismatch")
        a_nodes, a_counts = [], []
        for case_index, (solution, refutation) in enumerate(zip(solutions, fiber["refutations"])):
            words = literal_joint_seed(blocks, absent, columns, solution)
            eligible, a_columns = literal_a_model(words, absent[0])
            if primary:
                old = first["a_instances"][case_index]
                require(tuple(old["solution"]) == solution and tuple(tuple(w) for w in old["seed"]) == words and
                        tuple(tuple(e) for e in old["eligible"]) == eligible and
                        tuple(tuple(q) for q in old["columns"]) == a_columns,
                        "entrywise producer seed/pair/column mismatch")
            require(digest(words) == refutation["seed_sha256"], "actual joint-seed mismatch")
            require(len(a_columns) == refutation["column_count"] and digest(a_columns) == refutation["columns_sha256"],
                    "actual a-column universe mismatch")
            count = check_tree(refutation["tree"], eligible, a_columns)
            require(count == refutation["nodes"], "certificate-node count mismatch")
            a_nodes.append(count)
            a_counts.append(len(a_columns))
        reports.append({"absent": absent, "x_candidates": len(columns), "x_completions": len(solutions),
                        "whole_star_nodes": census_nodes, "a_candidate_counts": a_counts, "a_nodes": a_nodes})
    report = {"agent": "six-code-3", "role": "researcher", "status": "COMPLETE producer-free audit",
              "input_blocks_sha256": digest(blocks), "certificate_sha256": digest(certificate),
              "group_order": len(group), "group_point_nodes": group_nodes, "fibers": reports,
              "x_completions": sum(r["x_completions"] for r in reports),
              "a_refutation_nodes": sum(sum(r["a_nodes"]) for r in reports),
              "seconds": time.monotonic() - started,
              "entrywise_producer_comparison": compare_producer,
              "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if write_report:
        WORK.mkdir(parents=True, exist_ok=True)
        (WORK / "verification.json").write_bytes(encoded(report))
        print(json.dumps({k: v for k, v in report.items() if k != "fibers"}, sort_keys=True))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=lambda p: HERE / p, default=HERE / "certificate.json")
    parser.add_argument("--compare-producer", action="store_true")
    args = parser.parse_args()
    try:
        run(args.certificate, compare_producer=args.compare_producer)
    except Incomplete as exc:
        print(str(exc))
        raise SystemExit(2)
