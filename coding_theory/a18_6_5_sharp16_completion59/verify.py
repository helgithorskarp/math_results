"""Producer-free literal census and residual conflict-partition checker."""
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

def packing_census(columns, target=12, nodes=200000, seconds=10):
    pairsets = tuple(frozenset(combinations(q, 2)) for q in columns)
    conflicts = tuple(frozenset(j for j, other in enumerate(pairsets)
                                if j != i and not pairs.isdisjoint(other))
                      for i, pairs in enumerate(pairsets))
    guard = Guard(nodes, seconds)
    failed = set()
    answers = []
    counts = {"cardinality": 0, "partition": 0, "cached": 0}

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

    def visit(available, need, chosen):
        guard.tick()
        if need == 0:
            answers.append(tuple(sorted(chosen)))
            return True
        if len(available) < need:
            counts["cardinality"] += 1
            return False
        key = (available, need)
        if key in failed:
            counts["cached"] += 1
            return False
        if too_few_groups(available, need):
            counts["partition"] += 1
            failed.add(key)
            return False
        v = max(available, key=lambda z: (len(conflicts[z] & available), -z))
        rest = available - {v}
        included = visit(rest - conflicts[v], need - 1, chosen + (v,))
        excluded = visit(rest, need, chosen)
        if not included and not excluded:
            failed.add(key)
        return included or excluded

    try:
        visit(frozenset(range(len(columns))), target, ())
    except Incomplete:
        WORK.mkdir(parents=True, exist_ok=True)
        (WORK / "unfinished_case.json").write_bytes(encoded({"status": "INCOMPLETE", "target": target,
                                                            "columns_sha256": digest(columns), "nodes": guard.nodes,
                                                            "partial_positive_keys": answers, "exclusion": False}))
        raise
    require(len(set(answers)) == len(answers), "duplicate binary packing paths")
    require(all(len(s) == target and all(pairsets[i].isdisjoint(pairsets[j]) for i, j in combinations(s, 2))
                for s in answers), "invalid binary packing leaf")
    return tuple(sorted(answers)), guard.nodes, counts


T = tuple(p for p in range(18) if p not in (2, 14, 17))


def literal_prefix(seed35, pool, key):
    require(len(key) == 12 and tuple(sorted(set(key))) == tuple(key) and
            all(type(i) is int and 0 <= i < len(pool) for i in key), "invalid actual sharp key")
    words = tuple(sorted(seed35 + tuple(tuple(sorted((14,) + pool[i])) for i in key)))
    require(len(words) == len(set(words)) == 47 and
            all(len(set(u) & set(v)) <= 2 for u, v in combinations(words, 2)), "literal sharp prefix collision")
    require(sum(14 in w for w in words) == 16 and sum(17 in w for w in words) ==
            sum(2 in w for w in words) == 20 and not any(14 in w and 2 in w for w in words),
            "literal sharp prefix stars/absence failure")
    return words


def literal_residual(words):
    center_counts = Counter(sum(p in w for p in (2, 14, 17)) for w in words)
    require(center_counts == {1: 38, 2: 9}, "prefix does not decompose into full three stars")
    triplets = [e for w in words for e in combinations(tuple(p for p in w if p in T), 3)]
    forbidden = frozenset(triplets)
    require(len(triplets) == len(forbidden) == 161, "wrong literal residual triple coverage")
    require(len(set(combinations(T, 3)) - forbidden) == 294, "wrong eligible triple count")
    return tuple(w for w in combinations(range(18), 5) if not any(p in w for p in (2, 14, 17))
                 and all(e not in forbidden for e in combinations(w, 3)))


def build_models(blocks):
    unused, neighbors = literal_template(blocks)
    maps, map_nodes = point_maps(blocks)
    orbit = tuple(sorted({p[2] for p in maps}))
    require(len(maps) == 8 and orbit == neighbors == (2, 9, 15, 16), "literal absence carrier incomplete")
    y_words = tuple(tuple(sorted((17,) + q)) for q in blocks)
    eligible, a_columns = literal_a_model(y_words, 2)
    covers, a_nodes = whole_a_stars(eligible, a_columns)
    require(len(a_columns) == 150 and len(covers) == 6, "literal absent-star cover census incomplete")
    models = {"automorphisms": maps, "absence_orbit": orbit, "a_pairs": eligible,
              "a_columns": a_columns, "a_covers": covers, "fibers": []}
    reports = []
    for case, cover in enumerate(covers):
        words35 = literal_seed(blocks, a_columns, cover)
        pool = literal_x_columns(words35)
        keys, nodes, prunes = packing_census(pool)
        fiber = {"a_cover": cover, "seed35": words35, "x_columns": pool, "sharp_keys": keys, "residuals": []}
        for key in keys:
            words = literal_prefix(words35, pool, key)
            residual = literal_residual(words)
            fiber["residuals"].append({"seed47": words, "columns": residual})
        models["fibers"].append(fiber)
        reports.append({"case": case, "sharp_prefixes": len(keys), "binary_nodes": nodes, "prunes": prunes})
    require(sum(len(f["sharp_keys"]) for f in models["fibers"]) == 142, "literal full sharp census incomplete")
    return json.loads(encoded(models)), {"map_nodes": map_nodes, "a_whole_star_nodes": a_nodes, "fibers": reports}


def check_partition(groups, columns):
    require(type(groups) is list and len(groups) <= 12 and all(type(g) is list and bool(g) for g in groups),
            "partition does not provide upper twelve")
    require(all(type(i) is int and 0 <= i < len(columns) for g in groups for i in g), "invalid partition vertex")
    require(sorted(i for g in groups for i in g) == list(range(len(columns))), "partition loses/duplicates a vertex")
    require(all(all(len(set(columns[i]) & set(columns[j])) >= 3 for i, j in combinations(g, 2)) for g in groups),
            "a declared conflict group contains compatible words")
    return len(groups)


def check_witness(witness, models, blocks):
    require(witness["format"] == "sharp-three-star-cardinality-witness-v1", "wrong witness format")
    case, at = witness["case"], witness["sharp_key_index"]
    require(type(case) is int and 0 <= case < 6 and type(at) is int and
            0 <= at < len(models["fibers"][case]["residuals"]), "invalid witness model key")
    instance = models["fibers"][case]["residuals"][at]
    extra = witness["extra_columns"]
    require(len(extra) == 12 and all(type(i) is int and 0 <= i < len(instance["columns"]) for i in extra)
            and sorted(set(extra)) == extra, "invalid twelve-word witness key")
    restored = sorted(instance["seed47"] + [instance["columns"][i] for i in extra])
    words = witness["words"]
    require(words == restored and len(words) == 59 and tuple(sorted(set(tuple(w) for w in words))) ==
            tuple(tuple(w) for w in words), "literal59 restoration/cardinality mismatch")
    require(all(len(w) == 5 and sorted(set(w)) == w and all(type(p) is int and 0 <= p < 18 for p in w)
                for w in words), "invalid witness word")
    require(all(len(set(u) & set(v)) <= 2 for u, v in combinations(words, 2)), "witness intersection failure")
    require(sum(14 in w for w in words) == 16 and sum(17 in w for w in words) ==
            sum(2 in w for w in words) == 20 and not any(14 in w and 2 in w for w in words),
            "witness stars/absence failure")
    require(tuple(tuple(p for p in w if p != 17) for w in words if 17 in w) == blocks,
            "witness has the wrong exact y star")
    return words


def validate_certificate(certificate, models, witness, blocks):
    require(certificate["format"] == "sharp16-total59-color-v1" and certificate["absent"] == 2 and
            certificate["upper_family_size"] == 59, "wrong certificate scope")
    require(certificate["automorphisms"] == models["automorphisms"] and
            certificate["absence_orbit"] == models["absence_orbit"], "actual template group/orbit mismatch")
    require(certificate["a_pairs_sha256"] == digest(models["a_pairs"]) and
            certificate["a_columns_sha256"] == digest(models["a_columns"]) and
            certificate["a_pair_count"] == 90 and certificate["a_column_count"] == 150,
            "actual a carrier mismatch")
    require(certificate["a_covers"] == models["a_covers"] and len(certificate["fibers"]) == 6,
            "incomplete saturated-star cover fiber")
    profiles, color_counts, column_counts = Counter(), [], []
    for declared, actual in zip(certificate["fibers"], models["fibers"]):
        require(declared["a_cover"] == actual["a_cover"] and declared["seed35_sha256"] == digest(actual["seed35"])
                and declared["x_column_count"] == len(actual["x_columns"]) and
                declared["x_columns_sha256"] == digest(actual["x_columns"]) and
                declared["sharp_keys"] == actual["sharp_keys"], "actual twelve-word solution fiber mismatch")
        require(len(declared["residuals"]) == len(actual["residuals"]), "missing residual coloring case")
        for proof, instance in zip(declared["residuals"], actual["residuals"]):
            require(proof["seed47_sha256"] == digest(instance["seed47"]) and
                    proof["column_count"] == len(instance["columns"]) and
                    proof["columns_sha256"] == digest(instance["columns"]), "actual residual carrier mismatch")
            count = check_partition(proof["conflict_partition"], instance["columns"])
            color_counts.append(count)
            column_counts.append(len(instance["columns"]))
            degrees = [sum(14 in w and p in w for w in instance["seed47"]) for p in range(18) if p != 14]
            k = degrees.count(3)
            require(0 <= k <= 4 and sorted(degrees) == [0] + [3] * k + [4] * (16 - 2 * k) + [5] * k,
                    "literal hub profile differs from five claimed patterns")
            profiles[k] += 1
    words = check_witness(witness, models, blocks)
    key = certificate["witness"]
    require(key["case"] == witness["case"] and key["sharp_key_index"] == witness["sharp_key_index"] and
            key["extra_columns"] == witness["extra_columns"] and key["words_sha256"] == digest(words),
            "witness certificate provenance mismatch")
    require(sum(profiles.values()) == len(color_counts) == 142, "incomplete residual certificate carrier")
    return {"profiles": dict(sorted(profiles.items())), "color_counts": color_counts,
            "column_counts": column_counts, "witness_words_sha256": digest(words)}


def run(certificate_path, compare_producer=False):
    started = time.monotonic()
    blocks = load_input()
    models, counts = build_models(blocks)
    if compare_producer:
        require(models == json.loads((WORK / "full_census.json").read_text()), "entrywise actual producer mismatch")
    certificate = json.loads(certificate_path.read_text())
    witness = json.loads((HERE / "witness.json").read_text())
    checked = validate_certificate(certificate, models, witness, blocks)
    report = {"agent": "six-code-3", "role": "researcher", "status": "COMPLETE producer-free certificate audit",
              "input_blocks_sha256": digest(blocks), "certificate_sha256": digest(certificate),
              "sharp_prefixes": 142, "group_point_states": counts["map_nodes"],
              "a_whole_star_states": counts["a_whole_star_nodes"], "fibers": counts["fibers"],
              "hub_pair_profile_k_counts": checked["profiles"],
              "residual_candidate_min": min(checked["column_counts"]),
              "residual_candidate_max": max(checked["column_counts"]),
              "verified_color_cases": len(checked["color_counts"]),
              "conflict_group_counts": dict(sorted(Counter(checked["color_counts"]).items())),
              "upper_family_size": 59, "witness_words": 59,
              "witness_words_sha256": checked["witness_words_sha256"],
              "entrywise_producer_comparison": compare_producer, "seconds": time.monotonic() - started,
              "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "literal_models.json").write_bytes(encoded(models))
    (WORK / "verification.json").write_bytes(encoded(report))
    print(json.dumps({k: v for k, v in report.items() if k != "fibers"}, sort_keys=True))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=lambda p: HERE / p, default=HERE / "certificate.json")
    parser.add_argument("--compare-producer", action="store_true")
    args = parser.parse_args()
    try:
        run(args.certificate, args.compare_producer)
    except Incomplete as exc:
        print(str(exc))
        raise SystemExit(2)
