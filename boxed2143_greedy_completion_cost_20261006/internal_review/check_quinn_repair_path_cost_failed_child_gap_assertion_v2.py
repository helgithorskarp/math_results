#!/usr/bin/env python3
"""Independent whole648 controls; no author/teammate executable imports.

Dyck shape generation, pointer-stack Cartesian trees, direct greater-position
gap tests, strict-rectangle prefix counts and exact tagged population sums.
Uniform proofs and scope are documented separately. All outputs are immutable.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
import json
from math import factorial
from pathlib import Path
import platform
import resource
from time import perf_counter


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def fp(p):
    b = p.read_bytes()
    return {"bytes": len(b), "sha256": sha256(b).hexdigest()}


def canonical(item):
    return (json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n").encode()


def shape_word(t):
    return "." if t is None else "(" + shape_word(t[0]) + shape_word(t[1]) + ")"


def dyck_shapes(n):
    # Standard Catalan code: '(' code(left) ')' code(right).
    pending, words = [("", 0, 0)], []
    while pending:
        word, opened, closed = pending.pop()
        if opened == closed == n:
            words.append(word)
            continue
        if closed < opened:
            pending.append((word + ")", opened, closed + 1))
        if opened < n:
            pending.append((word + "(", opened + 1, closed))
    shapes = []
    for word in words:
        cursor = 0

        def parse():
            nonlocal cursor
            if cursor == len(word) or word[cursor] == ")":
                return None
            cursor += 1
            left = parse()
            require(word[cursor] == ")", "bad Dyck close")
            cursor += 1
            return left, parse()

        shapes.append(parse())
        require(cursor == len(word), "unread Dyck suffix")
    return sorted(shapes, key=shape_word)


def representative(t):
    left, right = [], []

    def index(node):
        if node is None:
            return None
        l = index(node[0])
        root = len(left)
        left.append(l)
        right.append(None)
        right[root] = index(node[1])
        return root

    root = index(t)
    p, value, pending = [0] * len(left), len(left), [root]
    while pending:
        node = pending.pop()
        if node is None:
            continue
        p[node], value = value, value - 1
        pending.append(right[node])
        pending.append(left[node])
    return tuple(p)


def cartesian(p):
    left, right, stack = [None] * len(p), [None] * len(p), []
    for node, value in enumerate(p):
        last = None
        while stack and p[stack[-1]] < value:
            last = stack.pop()
        if stack:
            right[stack[-1]] = node
        left[node] = last
        stack.append(node)
    root = stack[0] if stack else None
    paths, pending = [], [(root, "")]
    while pending:
        node, word = pending.pop()
        if node is None:
            paths.append(word)
        else:
            pending.append((right[node], word + "R"))
            pending.append((left[node], word + "L"))

    def tree(node):
        return None if node is None else (tree(left[node]), tree(right[node]))

    return tree(root), paths


def boxes(p):
    n = len(p)
    require(sorted(p) == list(range(1, n + 1)), "nonpermutation input")
    # prefix[t][v] counts positions <t with value <=v.
    prefix = [[0] * (n + 1)]
    for value in p:
        prefix.append([count + int(value <= v) for v, count in enumerate(prefix[-1])])
    answer = []
    for a, b, c, d in combinations(range(n), 4):
        low, high = p[b], p[c]
        if low < p[a] < p[d] < high:
            inside = (prefix[d][high - 1] - prefix[a + 1][high - 1]
                      - prefix[d][low] + prefix[a + 1][low])
            if inside == 0:
                answer.append([a, b, c, d])
    return answer


def intervals(p):
    answer = []
    for j, value in enumerate(p):
        l = next((i for i in range(j - 1, -1, -1) if p[i] > value), None)
        r = next((i for i in range(j + 1, len(p)) if p[i] > value), None)
        if l is not None and r is not None and p[l] < p[r]:
            answer.append((l, j, r))
    return answer


def legal_gaps(p):
    bad = set()
    for _, j, r in intervals(p):
        bad.update(range(j + 1, r + 1))
    return tuple(g for g in range(len(p) + 1) if g not in bad)


def offending_positions(w):
    first_l = w.find("L")
    return [] if first_l == -1 else [j for j in range(first_l + 1, len(w) - 1)
                                    if w[j:j + 2] == "RR"]


def raw_rr(w):
    return sum(w[j:j + 2] == "RR" for j in range(len(w) - 1))


def inserted(p, g):
    return p[:g] + (len(p) + 1,) + p[g:]


def repair(p, g):
    p, steps, rewrites = tuple(p), [], []
    initial = len(offending_positions(cartesian(p)[1][g]))
    while g not in legal_gaps(p):
        legal = legal_gaps(p)
        k = max(x for x in legal if x < g)
        word = cartesian(p)[1][g]
        first = offending_positions(word)[0]
        q, v = word[:first], word[first + 2:]
        child = inserted(p, k)
        child_boxes = boxes(child)
        require(not child_boxes, "illegal actual auxiliary child")
        after = cartesian(child)[1][g + 1]
        require(after == "R" + "L" * q.count("L") + "R" + v, "first-pair rewrite mismatch")
        require(len(offending_positions(after)) == len(offending_positions(word)) - 1,
                "cost does not decrease by exactly one")
        steps.append({"desired_gap": g, "chosen_gap": k, "legal_gaps": list(legal),
                      "parent": list(p), "child": list(child)})
        rewrites.append({"before": word, "first_pair_index": first, "q": q,
                         "v": v, "after": after, "complete_auxiliary_boxes": child_boxes})
        p, g = child, g + 1
        require(len(steps) <= initial, "repair exceeded initial D")
    require(len(steps) == initial, "exact initial cost mismatch")
    return len(steps), {"final_desired_gap": g, "final_word": list(p), "steps": steps}, rewrites


def original_gaps(tags):
    return [i for i, tag in enumerate(tags) if tag is not None] + [len(tags)]


def potential(p, tags):
    paths = cartesian(p)[1]
    return sum(raw_rr(paths[g]) for g in original_gaps(tags))


def advance(p, tags, g, rank):
    cost, evidence, rewrites = repair(p, g)
    tags = list(tags)
    for step in evidence["steps"]:
        tags.insert(step["chosen_gap"], None)
    child = inserted(tuple(evidence["final_word"]), evidence["final_desired_gap"])
    tags.insert(evidence["final_desired_gap"], rank)
    child_boxes = boxes(child)
    require(not child_boxes, "illegal actual original child")
    return {"initial_current_gap": g, "cost": cost, "word": list(child),
            "tags": tags, "phi": potential(child, tags)}, {
                "repair_trace": evidence, "rewrites": rewrites,
                "complete_original_child_boxes": child_boxes}


def completion(source):
    p, tags, costs, stages = (), [], [], []
    for rank in range(1, len(source) + 1):
        later = source[source.index(rank) + 1:]
        neighbor = next((value for value in later if value < rank), None)
        gap = tags.index(neighbor) if neighbor is not None else len(p)
        result, certificate = advance(p, tags, gap, rank)
        p, tags = tuple(result["word"]), result["tags"]
        costs.append(result["cost"])
        stages.append({"rank": rank, "result": result, "certificate": certificate})
    require(tuple(tag for tag in tags if tag is not None) == source, "source ID decode")
    originals = [v for v, tag in zip(p, tags) if tag is not None]
    ranks = {v: i + 1 for i, v in enumerate(sorted(originals))}
    require(tuple(ranks[v] for v in originals) == source, "source value decode")
    return p, tags, costs, stages


def source_hashes(packet, names):
    return {name: fp(packet / name)["sha256"] for name in names}


def check_report(packet, name, expected):
    actual = json.loads((packet / name).read_text())
    documentary = {k: actual[k] for k in ("seconds", "peak_rss_kib_linux")}
    require({k: v for k, v in actual.items() if k not in documentary} == expected,
            "entire deterministic author report mismatch: " + name)
    require(documentary["seconds"] > 0 and documentary["peak_rss_kib_linux"] > 0,
            "bad documentary resource fields")
    return documentary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    args = parser.parse_args()
    packet, out = args.packet, args.output_directory
    require(not out.exists(), "preserve prior output directory")
    began = perf_counter()
    manifest = json.loads((packet / "MANIFEST.json").read_text())
    require(fp(packet / "MANIFEST.json")["sha256"] ==
            "62a38b24f083b16351a83c0b7111a9758ccf7aabc44ea101a36cd848d5862941",
            "pinned packet manifest changed")
    before = {e["path"]: fp(packet / e["path"]) for e in manifest["files"]}
    require(before == {e["path"]: {k: e[k] for k in ("bytes", "sha256")}
                       for e in manifest["files"]}, "author packet bytes changed")
    old_stream, literal_stream = sha256(), sha256()
    records, rows, old_rows = [], [], []
    gaps = auxiliaries = hypothetical_total = 0
    for n in range(8):
        shapes = dyck_shapes(n)
        size_gaps = size_aux = 0
        for t in shapes:
            p = representative(t)
            reconstructed, paths = cartesian(p)
            require(reconstructed == t and not boxes(p), "shape representative mismatch")
            for g, path in enumerate(paths):
                predicted = len(offending_positions(path))
                cost, trace, rewrites = repair(p, g)
                coverage = sum(j < g <= r for _, j, r in intervals(p))
                full = boxes(inserted(p, g))
                require(predicted == cost == coverage == len(full), "path/coverage/literal mismatch")
                record = {"n": n, "shape": shape_word(t), "gap": g, "path": path,
                          "D": predicted, "cost": cost, "blocker_coverage": coverage,
                          "hypothetical_full_occurrence_set": full, "repair_trace": trace}
                literal_stream.update(canonical(record))
                old_stream.update(f"{shape_word(t)}|{g}|{path}|{predicted}|{cost}\n".encode())
                records.append({"author_stream_record": record, "independent_path_rewrites": rewrites})
                gaps += 1
                size_gaps += 1
                auxiliaries += cost
                size_aux += cost
                hypothetical_total += len(full)
        rows.append({"n": n, "complete_shapes": len(shapes), "complete_gaps": size_gaps,
                     "actual_auxiliary_children": size_aux})
        old_rows.append({"n": n, "fully_examined_shapes": len(shapes)})
    expected_path = {
        "actor": "literature-researcher-3", "full_target_solved": False,
        "status": "finite formula controls only; all-size statement unproved",
        "formula": "RR adjacency count after an earlier L", "first_mismatch": None,
        "gaps_checked": gaps, "complete_rows": old_rows, "stream_sha256": old_stream.hexdigest(),
        "python": "3.11.2", "processes": 1, "native_threads": 1}
    expected_literal = {
        "actor": "literature-researcher-3", "full_target_solved": False,
        "status": "PASS same-author complete literal controls; whole review pending",
        "domain": "ALL shapes n0..7 and EVERY external gap", "rows": rows, "gaps_checked": gaps,
        "actual_auxiliary_children_literal_checked": auxiliaries,
        "hypothetical_maximum_children_literal_checked": gaps,
        "hypothetical_occurrences_total": hypothetical_total,
        "stream_sha256": literal_stream.hexdigest(), "preserved_v1_stream_sha256": old_stream.hexdigest(),
        "source_sha256": source_hashes(packet, ["repair_path_cost_literal_controls_v2.py",
            "repair_path_cost_probe_v1.py", "kernel.py", "tree_dynamics.py", "verify_kernel.py"]),
        "python": "3.11.2", "processes": 1, "native_threads": 1}
    documentary = {}
    documentary["path"] = check_report(packet, "repair_path_cost_probe_v1.json", expected_path)
    documentary["literal"] = check_report(packet, "repair_path_cost_literal_controls_v2.json", expected_literal)

    raw_stream, raw_records, raw_rows, failure = sha256(), [], [], None
    for n in range(7):
        largest, checked = None, 0
        for source in permutations(range(1, n + 1)):
            p, tags, _, _ = completion(source)
            phi = potential(p, tags)
            children = [advance(p, tags, g, n + 1)[0] for g in original_gaps(tags)]
            numerator = sum(c["cost"] + c["phi"] for c in children) - (n + 1) * phi
            record = {"source": list(source), "n": n, "word": list(p), "tags": tags,
                      "phi": phi, "children": children, "drift_numerator": numerator,
                      "drift_denominator": n + 1}
            raw_records.append(record)
            raw_stream.update(canonical(record))
            checked += 1
            largest = numerator if largest is None else max(largest, numerator)
            if numerator > n + 1:
                failure = record
                break
        raw_rows.append({"n": n, "source_states_checked": checked,
                         "largest_drift_numerator": largest, "denominator": n + 1})
        if failure:
            break
    expected_raw = {
        "actor": "literature-researcher-3", "full_target_solved": False,
        "status": "author drift-candidate rejection",
        "potential": "sum over original gaps of all RR adjacencies in their paths",
        "tested_drift_constant": 1, "first_failure": failure, "states_checked": len(raw_records),
        "rows": raw_rows, "stream_sha256": raw_stream.hexdigest(),
        "python": "3.11.2", "processes": 1, "native_threads": 1}
    documentary["raw_probe"] = check_report(packet, "repair_rr_potential_probe_v1.json", expected_raw)

    family_stream, family_rows, family_cert = sha256(), [], []
    shape_children = literal_children = arrivals = 0
    for n, q in [(2, 1), (4, 1), (8, 2), (27, 3), (64, 4)]:
        b = n - q - 1
        p = tuple(range(1, b + 1)) + tuple(range(n, n - q - 1, -1))
        t, paths = cartesian(p)
        literal = n + 1 <= 28
        require(legal_gaps(p) == tuple(range(n + 1)), "family parent has illegal gap")
        require(all(not offending_positions(w) for w in paths), "family path illegal")
        phi = sum(raw_rr(w) for w in paths)
        require(phi == q * (q + 1) // 2, "family parent formula")
        parent_boxes = boxes(p) if literal else None
        require(not parent_boxes, "family parent boxes")
        previous, prefix_records = (), []
        for rank in range(1, n + 1):
            restricted = tuple(value for value in p if value <= rank)
            g = restricted.index(rank)
            require(g in legal_gaps(previous) and inserted(previous, g) == restricted,
                    "family rank arrival requires repair")
            _, prefix_paths = cartesian(restricted)
            require(all(not offending_positions(w) for w in prefix_paths), "family prefix language")
            full = boxes(restricted) if literal else None
            require(not full, "family prefix boxes")
            prefix_records.append({"rank": rank, "gap": g, "word": list(restricted),
                                   "paths": prefix_paths, "complete_boxes": full})
            arrivals += 1
            previous = restricted
        children, child_cert = [], []
        for g in range(n + 1):
            child = inserted(p, g)
            child_t, child_paths = cartesian(child)
            child_phi = sum(raw_rr(w) for w in child_paths)
            if g <= b:
                predicted = phi + q + 1
            else:
                index = g - b
                remaining = q + 1 - index
                predicted = (index * (index - 1) + remaining * (remaining + 1)) // 2
            require(child_phi == predicted, "family child formula")
            require(all(not offending_positions(w) for w in child_paths), "family child path language")
            full = boxes(child) if literal else None
            require(not full, "family child boxes")
            literal_children += literal
            shape_children += 1
            children.append({"gap": g, "cost": 0, "child_phi": child_phi, "full_literal_scan": literal})
            child_cert.append({"gap": g, "word": list(child), "shape": shape_word(child_t),
                               "paths": child_paths, "complete_boxes": full})
        drift = Fraction(sum(c["child_phi"] for c in children), n + 1) - phi
        require(drift == Fraction((q + 1) * (6 * n - q * (q + 5)), 6 * (n + 1)),
                "family rational drift formula")
        if n == q ** 3 and q >= 2:
            require(drift >= Fraction(q + 1, 3), "family subsequence lower bound")
        row = {"n": n, "q": q, "b": b, "parent": list(p), "parent_phi": phi, "children": children,
               "conditional_drift_numerator": drift.numerator, "conditional_drift_denominator": drift.denominator,
               "parent_prefix_literal_scans": n + 1 if literal else 0}
        family_rows.append(row)
        family_stream.update(canonical(row))
        family_cert.append({"author_stream_record": row, "parent_shape": shape_word(t),
                            "parent_paths": paths, "complete_parent_boxes": parent_boxes,
                            "all_rank_arrivals": prefix_records, "all_children": child_cert})
    expected_family = {
        "actor": "literature-researcher-3", "full_target_solved": False,
        "status": "PASS directed controls; uniform raw-RR drift obstruction AUTHOR pending whole check",
        "potential": "sum of all RR adjacencies over ORIGINAL gap paths", "rows": family_rows,
        "shape_children_checked": shape_children, "children_full_literal_checked": literal_children,
        "rank_arrival_steps_checked": arrivals, "stream_sha256": family_stream.hexdigest(),
        "source_sha256": source_hashes(packet, ["repair_rr_drift_family_v1.py", "repair_path_cost_probe_v1.py",
                                                "kernel.py", "tree_dynamics.py", "verify_kernel.py"]),
        "python": "3.11.2", "processes": 1, "native_threads": 1,
        "excluded": "unconditional mean bounds, other potentials, full target410"}
    documentary["raw_family"] = check_report(packet, "repair_rr_drift_family_v1.json", expected_family)

    population_records, population_rows, mean_aux, mean_mass = [], [], [], []
    identity_rhs = Fraction(0)
    for n in range(7):
        cost_sum = mass_sum = 0
        for source in permutations(range(1, n + 1)):
            p, tags, costs, stages = completion(source)
            paths, o = cartesian(p)[1], original_gaps(tags)
            path_mass = sum(len(offending_positions(paths[g])) for g in o)
            blocker_mass = sum(sum(j < g <= r for g in o) for _, j, r in intervals(p))
            require(path_mass == blocker_mass, "original-weight blocker mass mismatch")
            cost = sum(costs)
            require(cost == len(p) - n, "completion cost accounting")
            cost_sum += cost
            mass_sum += blocker_mass
            population_records.append({"source": list(source), "word": list(p), "tags": tags,
                                       "original_gaps": o, "stage_costs": costs, "all_stages": stages,
                                       "original_gap_blocker_mass": blocker_mass})
        mean_aux.append(Fraction(cost_sum, factorial(n)))
        mean_mass.append(Fraction(mass_sum, factorial(n)))
        require(mean_aux[n] == identity_rhs, "finite weighted expectation identity mismatch")
        population_rows.append({"n": n, "source_histories": factorial(n), "auxiliary_sum": cost_sum,
                                "original_gap_blocker_mass_sum": mass_sum,
                                "mean_aux": [mean_aux[n].numerator, mean_aux[n].denominator],
                                "identity_rhs": [identity_rhs.numerator, identity_rhs.denominator]})
        identity_rhs += mean_mass[n] / (n + 1)

    for stem in ["repair_path_cost_probe_v1", "repair_path_cost_literal_controls_v2",
                 "repair_rr_potential_probe_v1", "repair_rr_drift_family_v1"]:
        require((packet / (stem + ".stderr")).read_bytes() == b"", "author stderr changed")
        author = json.loads((packet / (stem + ".json")).read_text())
        printed = json.loads((packet / (stem + ".stdout")).read_text())
        expected_stdout = {k: v for k, v in author.items() if k != "rows"} if stem == "repair_rr_drift_family_v1" else author
        require(printed == expected_stdout, "author stdout/report discrepancy: " + stem)
    after = {e["path"]: fp(packet / e["path"]) for e in manifest["files"]}
    require(before == after, "author packet changed during new check")
    out.mkdir(parents=True)
    certificate = {"all4707_path_records_and_every1380_rewrite": records,
                   "all12_raw_probe_records": raw_records, "all5_family_records": family_cert,
                   "all874_weighted_population_histories": population_records}
    cert_path = out / "quinn_repair_path_cost_full_certificate_v2.json"
    cert_path.write_text(json.dumps(certificate, separators=(",", ":")) + "\n")
    result = {
        "author": "literature-researcher-3", "checker": "literature-researcher-4", "source_message_id": 648,
        "decision_message_id": 410, "full_target_solved": False, "status": "entire deterministic648 controls agree",
        "scope": "exact path cost/bijection/weighted identity and one raw-RR drift obstruction; no cost estimate/full410/655/novelty",
        "source": fp(Path(__file__)), "author_manifest": fp(packet / "MANIFEST.json"),
        "author_files_before_after_identical": after, "author_executable_imports": 0,
        "new_independent_executions": 1, "deterministic_reconstructions": {
            "path": expected_path, "literal": expected_literal, "raw_probe": expected_raw, "raw_family": expected_family},
        "documentary_author_resources": documentary, "new_population_identity_complete_rows": population_rows,
        "new_population_history_count": len(population_records), "full_certificate": fp(cert_path),
        "certificate_relative_path": cert_path.name, "python": platform.python_version(), "processes": 1, "native_threads": 1,
        "seconds_including_certificate_before_report_serialization": perf_counter() - began,
        "rss_sample_kib_before_report_serialization": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    report = out / "quinn_repair_path_cost_reproduction_v2.json"
    temporary = report.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2) + "\n")
    temporary.replace(report)
    print(json.dumps({"status": result["status"], "shapes": sum(row["complete_shapes"] for row in rows),
                      "gaps": gaps, "auxiliary_children": auxiliaries, "raw_states": len(raw_records),
                      "family_shape_children": shape_children, "family_literal_children": literal_children,
                      "family_rank_arrivals": arrivals, "population_histories": len(population_records),
                      "streams": [old_stream.hexdigest(), literal_stream.hexdigest(), raw_stream.hexdigest(), family_stream.hexdigest()],
                      "seconds": result["seconds_including_certificate_before_report_serialization"],
                      "rss_sample_kib": result["rss_sample_kib_before_report_serialization"]}))


if __name__ == "__main__":
    main()
