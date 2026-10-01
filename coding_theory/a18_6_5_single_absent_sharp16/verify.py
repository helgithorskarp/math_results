"""Producer-free literal carriers, whole-point stars and binary packing audit."""
from collections import Counter
from itertools import combinations
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

def whole_a_stars(eligible, columns, nodes=200000, seconds=10):
    active = sorted({p for e in eligible for p in e})
    demand = {p: 4 for p in active}
    pairsets = tuple(frozenset(combinations(q, 2)) for q in columns)
    colsets = tuple(frozenset(q) for q in columns)
    require(len(active) == 15 and len(eligible) == 90, "wrong independent a universe")
    require(all(es <= set(eligible) for es in pairsets), "column leaves independent pair universe")
    answers = []
    guard = Guard(nodes, seconds)

    def visit(remaining, used, chosen):
        guard.tick()
        if not any(remaining.values()):
            require(used == frozenset(eligible) and len(chosen) == 15, "whole-star leaf is not full cover")
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
        tails = {i: colsets[i] - {p} for i in options[p]}

        def star(suffix, selected, consumed):
            guard.tick()
            missing = need - len(selected)
            if not missing:
                updated = remaining.copy()
                for i in selected:
                    for z in columns[i]:
                        updated[z] -= 1
                require(min(updated.values()) >= 0 and updated[p] == 0, "independent quota error")
                visit(updated, used | frozenset(e for i in selected for e in pairsets[i]), chosen + tuple(selected))
                return
            opts = [i for i in suffix if tails[i].isdisjoint(consumed)]
            if len(opts) < missing or len(set().union(*(tails[i] for i in opts))) < 3 * missing:
                return
            for at, i in enumerate(opts):
                star(opts[at + 1:], selected + [i], consumed | tails[i])

        star(options[p], [], frozenset())

    visit(demand, frozenset(), ())
    require(len(set(answers)) == len(answers), "duplicate independent cover path")
    return tuple(sorted(answers)), guard.nodes

def packing_decision(columns, target, nodes=200000, seconds=10):
    pairsets = tuple(frozenset(combinations(q, 2)) for q in columns)
    conflicts = tuple(frozenset(j for j, other in enumerate(pairsets)
                                if j != i and not pairs.isdisjoint(other))
                      for i, pairs in enumerate(pairsets))
    guard = Guard(nodes, seconds)
    failed = set()
    counts = {"cardinality_prunes": 0, "partition_prunes": 0, "cached_prunes": 0}

    def too_few_groups(available, need):
        rest = set(available)
        groups = 0
        while rest:
            groups += 1
            if groups >= need:
                return False
            possible = rest.copy()
            while possible:
                v = min(possible)
                rest.remove(v)
                possible.intersection_update(conflicts[v])
        return True

    def visit(available, need):
        guard.tick()
        if need == 0:
            return ()
        if len(available) < need:
            counts["cardinality_prunes"] += 1
            return None
        key = (available, need)
        if key in failed:
            counts["cached_prunes"] += 1
            return None
        if too_few_groups(available, need):
            counts["partition_prunes"] += 1
            failed.add(key)
            return None
        v = max(available, key=lambda z: (len(conflicts[z] & available), -z))
        rest = available - {v}
        child = visit(rest - conflicts[v], need - 1)
        if child is not None:
            return (v,) + child
        child = visit(rest, need)
        if child is not None:
            return child
        failed.add(key)
        return None

    answer = visit(frozenset(range(len(columns))), target)
    if answer is not None:
        require(len(answer) == target and len(set(answer)) == target and
                all(pairsets[i].isdisjoint(pairsets[j]) for i, j in combinations(answer, 2)),
                "invalid literal packing witness")
    return answer, guard.nodes, counts


def literal_seed(blocks, columns, cover):
    require(len(cover) == 15 and tuple(sorted(set(cover))) == cover and
            all(type(i) is int and 0 <= i < len(columns) for i in cover), "invalid literal a-cover key")
    words = tuple(sorted(tuple(tuple(sorted((17,) + q)) for q in blocks) +
                         tuple(tuple(sorted((2,) + columns[i])) for i in cover)))
    require(len(words) == len(set(words)) == 35 and all(len(w) == len(set(w)) == 5 for w in words),
            "invalid literal seed cardinality")
    require(all(len(set(u) & set(v)) <= 2 for u, v in combinations(words, 2)), "literal seed collision")
    require(sum(2 in w for w in words) == sum(17 in w for w in words) == 20 and
            sum(14 in w for w in words) == 4 and not any(14 in w and 2 in w for w in words),
            "literal seed replication/absence failure")
    a_blocks = tuple(tuple(p for p in w if p != 2) for w in words if 2 in w)
    pairs = [e for q in a_blocks for e in combinations(q, 2)]
    require(len(pairs) == len(set(pairs)) == 120 and
            set(pairs) == set(combinations([p for p in range(18) if p not in (2, 14)], 2)),
            "literal saturated a star does not cover every pair")
    return words


def literal_x_columns(words):
    return tuple(tuple(p for p in w if p != 14) for w in combinations(range(18), 5)
                 if 14 in w and 2 not in w and 17 not in w and
                 all(len(set(w) & set(v)) <= 2 for v in words))


def literal_witness(witness, blocks):
    require(witness["format"] == "literal-three-star-witness-v1" and witness["point_count"] == 18 and
            witness["x"] == 14 and witness["y"] == 17 and witness["a"] == 2, "wrong witness carrier")
    words = tuple(tuple(w) for w in witness["words"])
    require(len(words) == 47 and tuple(sorted(set(words))) == words and
            all(len(w) == 5 and tuple(sorted(set(w))) == w and
                all(type(p) is int and 0 <= p < 18 for p in w) for w in words), "invalid witness words")
    require(all(len(set(u) & set(v)) <= 2 for u, v in combinations(words, 2)), "witness intersection failure")
    require(tuple(tuple(p for p in w if p != 17) for w in words if 17 in w) == blocks, "witness y star failure")
    require(sum(14 in w for w in words) == 16 and sum(17 in w for w in words) == 20 and
            sum(2 in w for w in words) == 20, "witness replication failure")
    require(not any(14 in w and 2 in w for w in words), "witness x-a absence failure")
    return words


def audit_models(blocks):
    rep, neighbors = literal_template(blocks)
    maps, group_nodes = point_maps(blocks)
    orbit = tuple(sorted({p[2] for p in maps}))
    require(len(maps) == 8 and orbit == neighbors == (2, 9, 15, 16), "literal absence quotient incomplete")
    y_words = tuple(tuple(sorted((17,) + q)) for q in blocks)
    eligible, columns = literal_a_model(y_words, 2)
    covers, census_nodes = whole_a_stars(eligible, columns)
    require(len(columns) == 150 and len(covers) == 6, "unexpected literal a census")
    fibers = []
    for cover in covers:
        words = literal_seed(blocks, columns, cover)
        pool = literal_x_columns(words)
        edges = sum(len(set(u) & set(v)) <= 1 for u, v in combinations(pool, 2))
        fibers.append({"a_cover": cover, "seed": words, "x_columns": pool, "x_graph_edges": edges})
    return {"automorphisms": maps, "absence_orbit": orbit, "y_seed": y_words,
            "a_pairs": eligible, "a_columns": columns, "a_covers": covers, "fibers": fibers,
            "group_point_nodes": group_nodes, "whole_star_nodes": census_nodes}


def compare_manifest(manifest, models, witness, blocks):
    require(manifest["format"] == "single-absence-replay-manifest-v1" and
            type(manifest["absent"]) is int and manifest["absent"] == 2, "wrong manifest format/absence")
    require(tuple(tuple(p) for p in manifest["automorphisms"]) == models["automorphisms"] and
            tuple(manifest["absence_orbit"]) == models["absence_orbit"], "manifest actual group/orbit mismatch")
    require(manifest["a_pair_count"] == len(models["a_pairs"]) and
            manifest["a_pairs_sha256"] == digest(models["a_pairs"]) and
            manifest["a_column_count"] == len(models["a_columns"]) and
            manifest["a_columns_sha256"] == digest(models["a_columns"]), "manifest actual a carrier mismatch")
    require(tuple(tuple(s) for s in manifest["a_covers"]) == models["a_covers"], "incomplete actual a cover fiber")
    require(len(manifest["fibers"]) == len(models["fibers"]), "missing extra-hub instance")
    for declared, actual in zip(manifest["fibers"], models["fibers"]):
        require(tuple(declared["a_cover"]) == actual["a_cover"] and
                declared["seed_sha256"] == digest(actual["seed"]) and
                declared["x_column_count"] == len(actual["x_columns"]) and
                declared["x_columns_sha256"] == digest(actual["x_columns"]) and
                declared["x_graph_edges"] == actual["x_graph_edges"] and
                type(declared["excluded_extra_count"]) is int and declared["excluded_extra_count"] == 13,
                "manifest actual extra-hub carrier mismatch")
    words = literal_witness(witness, blocks)
    key = manifest["witness"]
    require(type(key["case"]) is int and key["case"] == 0 and len(key["x_columns"]) == 12 and
            all(type(i) is int for i in key["x_columns"]) and
            tuple(sorted(set(key["x_columns"]))) == tuple(key["x_columns"]), "bad sharpness witness key")
    model = models["fibers"][0]
    require(all(0 <= i < len(model["x_columns"]) for i in key["x_columns"]), "witness key out of bounds")
    restored = tuple(sorted(model["seed"] + tuple(tuple(sorted((14,) + model["x_columns"][i]))
                                                  for i in key["x_columns"])))
    require(words == restored and digest(words) == key["words_sha256"], "literal witness manifest mismatch")
    return words


def run(manifest_path, write_report=True, compare_producer=False):
    started = time.monotonic()
    blocks = load_input()
    manifest = json.loads(manifest_path.read_text())
    witness = json.loads((HERE / "witness.json").read_text())
    models = audit_models(blocks)
    words = compare_manifest(manifest, models, witness, blocks)
    if compare_producer:
        producer = json.loads((WORK / "full_census.json").read_text())
        comparable = {k: v for k, v in models.items() if k not in ("group_point_nodes", "whole_star_nodes")}
        comparable["fibers"] = [{k: v for k, v in f.items() if k != "x_graph_edges"}
                                for f in comparable["fibers"]]
        require(json.loads(encoded(comparable)) == producer, "entrywise producer actual carrier mismatch")
    reports = []
    for case, fiber in enumerate(models["fibers"]):
        answer, nodes, counts = packing_decision(fiber["x_columns"], 13)
        require(answer is None, "POSITIVE replication17 packing; local exclusion fails")
        reports.append({"case": case, "x_column_count": len(fiber["x_columns"]),
                        "x_graph_edges": fiber["x_graph_edges"], "target": 13, "negative": True,
                        "binary_nodes": nodes, "prunes": counts})
    report = {"agent": "six-code-3", "role": "researcher", "status": "COMPLETE producer-free audit",
              "input_blocks_sha256": digest(blocks), "manifest_sha256": digest(manifest),
              "group_order": len(models["automorphisms"]), "group_point_nodes": models["group_point_nodes"],
              "a_pair_count": len(models["a_pairs"]), "a_column_count": len(models["a_columns"]),
              "a_covers": len(models["a_covers"]), "whole_star_nodes": models["whole_star_nodes"],
              "excluded_extra_count": 13, "sharp_hub_replication": 16,
              "witness_word_count": len(words), "witness_words_sha256": digest(words),
              "fibers": reports, "entrywise_producer_comparison": compare_producer,
              "seconds": time.monotonic() - started,
              "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if write_report:
        WORK.mkdir(parents=True, exist_ok=True)
        (WORK / "verification.json").write_bytes(encoded(report))
        print(json.dumps({k: v for k, v in report.items() if k != "fibers"}, sort_keys=True))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=lambda p: HERE / p, default=HERE / "manifest.json")
    parser.add_argument("--compare-producer", action="store_true")
    args = parser.parse_args()
    try:
        run(args.manifest, compare_producer=args.compare_producer)
    except Incomplete as exc:
        print(str(exc))
        raise SystemExit(2)
