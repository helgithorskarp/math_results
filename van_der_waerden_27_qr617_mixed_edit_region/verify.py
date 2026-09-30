#!/usr/bin/env python3
"""Independently check QR-617 flip transcripts and their quantified coverage.

This module does not import the generator, enumerate a search space, or trust
its status, counts, hashing, or claimed UNSAT. It checks every cited AP and
deduction with exact sets. QR colors use Euler's criterion, not square lists.
"""

import argparse
import hashlib
import json
import time
from pathlib import Path

P = 617
LAST = 3702
D = {x for x in range(LAST + 1) if x % P}
ENDPOINT_APS = {0: [1, 617], 1: [3421, 47]}
BOXES = {0: [(27, 1848), (1848, 27), (29, 29)],
         1: [(27, 1848), (1848, 27), (29, 29)]}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def color(x):
    require(type(x) is int and x in D, "Color requested outside prescribed domain")
    value = pow(x % P, (P - 1) // 2, P)
    require(value in (1, P - 1), "Euler criterion failed")
    return int(value == P - 1)


COLORS = {x: color(x) for x in D}


def check_domain():
    require(all(P % t for t in range(2, 25)), "617 is not prime")
    require(len(D) == 3696, "Wrong domain size")
    require(all(sum(COLORS[x] == c for x in D) == 1848 for c in (0, 1)),
            "Wrong original color-class sizes")


def budgets_of(data):
    budgets = data.get("budget")
    require(isinstance(budgets, list) and len(budgets) == 2 and
            all(type(b) is int and 0 <= b <= 1848 for b in budgets), "Invalid budgets")
    return budgets


def progression(pair, end=LAST):
    require(isinstance(pair, list) and len(pair) == 2, "Bad AP encoding")
    a, d = pair
    require(type(a) is int and type(d) is int and a >= 0 and d > 0 and a + 6 * d <= end,
            "AP outside domain or constant")
    points = {a + j * d for j in range(7)}
    require(points <= D, "Prefix AP touches an exceptional position")
    return points


def check_packing(petals, count):
    require(type(count) is int and count >= 1 and len(petals) == count,
            "Wrong opposite-color packing count")
    used = set()
    for petal in petals:
        require(petal and not (petal & used), "Packing empty or intersecting")
        used.update(petal)


def endpoint_points(pair, endpoint):
    require(isinstance(pair, list) and len(pair) == 2, "Bad endpoint AP")
    a, d = pair
    require(type(a) is int and type(d) is int and a >= 0 and d > 0 and
            a + 6 * d == LAST + 1, "AP does not end at the new endpoint")
    old = {a + j * d for j in range(6)}
    require(old <= D and all(COLORS[x] == endpoint for x in old),
            "Endpoint clause is not uniformly colored or touches an exception")
    return old


def mandatory_clause(pair, endpoint, forced):
    require(isinstance(pair, list) and len(pair) == 2, "Bad mandatory AP")
    a, d = pair
    require(type(a) is int and type(d) is int, "Noninteger AP")
    if a + 6 * d == LAST + 1:
        positive = endpoint_points(pair, endpoint)
        require(not (positive & forced), "Endpoint clause already satisfied")
        return positive
    points = progression(pair)
    for side in (0, 1):
        negative = {x for x in points if COLORS[x] == side}
        positive = points - negative
        if negative <= forced and not (positive & forced):
            return positive
    raise ValueError("AP has no mandatory unsatisfied clause at this state")



def verify_branch(data, complete=True, include_state=False):
    require(isinstance(data, dict) and data.get("format") == "qr617-mixed-conditional-color-budget-v1" and
            (data.get("status") == "EXCLUDED" or not complete), "Not a completed branch transcript")
    budgets = budgets_of(data)
    endpoint, root = data.get("endpoint"), data.get("root")
    require(type(endpoint) is int and endpoint in (0, 1) and type(root) is int and root in D,
            "Invalid branch hypothesis")
    hypotheses = data.get("initial_forced", [root])
    require(isinstance(hypotheses, list) and len(hypotheses) == 1 and
            type(hypotheses[0]) is int and hypotheses[0] == root,
            "Additional hypothesis in a covering branch")
    require(data.get("status") in ("EXCLUDED", "STALLED", "INCOMPLETE_TIME_LIMIT"),
            "Unknown proof status")
    allowed = set(D)
    forced = {root}
    counts = {"forbidden": 0, "forced": 0, "packing": 0, "empty": 0, "budget": 0, "mixed": 0}
    records = data.get("records")
    require(isinstance(records, list), "Missing branch records")
    for row in records:
        require(isinstance(row, list) and row, "Bad branch record")
        kind = row[0]
        if kind == "f":
            require(len(row) == 3, "Bad forbidden record")
            _, v, pairs = row
            require(type(v) is int and v in allowed - forced, "Invalid forbidden vertex")
            require(isinstance(pairs, list) and pairs, "Missing conditional APs")
            petals = []
            for pair in pairs:
                points = progression(pair)
                require(v in points, "Conditional AP omits target")
                negative = {x for x in points if COLORS[x] == COLORS[v]}
                positive = points - negative
                require(negative - {v} <= forced and not (positive & forced),
                        "Conditional antecedent unproved or consequent already satisfied")
                petals.append(positive & allowed)
            if any(not petal for petal in petals):
                counts["empty"] += 1
            else:
                opposite = 1 - COLORS[v]
                remaining = budgets[opposite] - sum(COLORS[x] == opposite for x in forced)
                check_packing(petals, remaining + 1)
                counts["packing"] += 1
            allowed.remove(v)
            counts["forbidden"] += 1
        elif kind == "m":
            require(data.get("format") == "qr617-mixed-conditional-color-budget-v1",
                    "Mixed record in an earlier proof format")
            require(len(row) == 3, "Bad mixed forbidden record")
            _, v, pairs = row
            require(type(v) is int and v in allowed - forced, "Invalid mixed target")
            require(isinstance(pairs, list) and pairs, "Missing mixed AP witnesses")
            petals = []
            for pair in pairs:
                require(isinstance(pair, list) and len(pair) == 2, "Bad mixed AP encoding")
                a, d = pair
                require(type(a) is int and type(d) is int, "Noninteger mixed AP")
                if a + 6 * d == LAST + 1:
                    positive = endpoint_points(pair, endpoint)
                    require(all(COLORS[x] == 1 - COLORS[v] for x in positive) and
                            not (positive & forced), "Wrong mixed endpoint clause color or satisfied")
                else:
                    points = progression(pair)
                    negative = {x for x in points if COLORS[x] == COLORS[v]}
                    positive = points - negative
                    require(negative - {v} <= forced and not (positive & forced),
                            "Mixed antecedent unproved or consequent satisfied")
                petals.append(positive & allowed)
            opposite = 1 - COLORS[v]
            remaining = budgets[opposite] - sum(COLORS[x] == opposite for x in forced)
            if any(not petal for petal in petals):
                counts["empty"] += 1
            else:
                check_packing(petals, remaining + 1)
                counts["packing"] += 1
            allowed.remove(v)
            counts["forbidden"] += 1
            counts["mixed"] += 1
        elif kind == "t":
            require(len(row) == 4, "Bad forced record")
            _, v, a, d = row
            require(type(v) is int and v in allowed - forced, "Invalid forced vertex")
            positive = mandatory_clause([a, d], endpoint, forced)
            require(positive & allowed == {v}, "Forced clause is not a singleton")
            forced.add(v)
            counts["forced"] += 1
        elif kind == "budget":
            require(len(row) == 2 and type(row[1]) is int and row[1] in (0, 1),
                    "Invalid exhausted-budget side")
            side = row[1]
            require(sum(COLORS[x] == side for x in forced) == budgets[side], "Budget not exhausted")
            allowed = {x for x in allowed if COLORS[x] != side or x in forced}
            counts["budget"] += 1
        else:
            raise ValueError("Unknown branch deduction")
        require(forced <= allowed, "A mandatory flip was removed")

    if not complete:
        result = {"proof_steps_verified": True, "complete_exclusion": False,
                  "budget": budgets, "endpoint": endpoint, "root": root,
                  "allowed": len(allowed), "forced": len(forced), "step_counts": counts}
        if include_state:
            result["allowed_positions"] = sorted(allowed)
            result["forced_positions"] = sorted(forced)
        return result

    contradiction = data.get("contradiction")
    require(isinstance(contradiction, dict), "Missing final contradiction")
    reason = contradiction.get("reason")
    if reason == "too_many_forced":
        require(any(sum(COLORS[x] == c for x in forced) > budgets[c] for c in (0, 1)),
                "No color cardinality contradiction")
    elif reason == "empty_required":
        positive = mandatory_clause(contradiction.get("ap"), endpoint, forced)
        require(not (positive & allowed), "Required clause not empty")
    elif reason == "required_packing":
        side = contradiction.get("color")
        require(type(side) is int and side in (0, 1), "Invalid contradiction color")
        pairs = contradiction.get("aps")
        require(isinstance(pairs, list), "Missing contradiction APs")
        petals = []
        for pair in pairs:
            positive = mandatory_clause(pair, endpoint, forced)
            require(all(COLORS[x] == side for x in positive), "Packing has wrong original color")
            petals.append(positive & allowed)
        remaining = budgets[side] - sum(COLORS[x] == side for x in forced)
        check_packing(petals, remaining + 1)
    else:
        raise ValueError("Unknown final contradiction")
    return {"budget": budgets, "endpoint": endpoint, "root": root,
            "forbidden_steps": counts["forbidden"], "forcing_steps": counts["forced"],
            "packing_steps": counts["packing"], "empty_steps": counts["empty"],
            "mixed_steps": counts["mixed"], "budget_steps": counts["budget"], "final_forced": len(forced),
            "final_allowed": len(allowed), "contradiction": reason}


def required_names():
    return [f"branch-{e}-{root}-{a}-{b}.json"
            for e, pair in ENDPOINT_APS.items()
            for a, b in BOXES[e] for root in sorted(endpoint_points(pair, e))]


def verify_suite(bundle):
    check_domain()
    require(set(bundle) == set(required_names()), "Missing, duplicated, or unexpected case coverage")
    results = []
    for e, pair in ENDPOINT_APS.items():
        roots = sorted(endpoint_points(pair, e))
        require(len(roots) == 6, "Endpoint root cover has wrong size")
        for a, b in BOXES[e]:
            for root in roots:
                data = bundle[f"branch-{e}-{root}-{a}-{b}.json"]
                require(data.get("budget") == [a, b] and data.get("endpoint") == e
                        and data.get("root") == root, "Wrong quantified branch")
                results.append(verify_branch(data))
    # The two full-width boxes independently establish a,b>=28. The square
    # excludes a,b<=29. These are outputs of the checked cover, not imports
    # from earlier cuts. Complementing c replaces each count by1848-count.
    lower_pairs = []
    for a in range(28, 59):
        for b in range(28, 59):
            if max(a, b) >= 30:
                require(a + b >= 58, "Incorrect lower-distance bridge")
            elif a + b <= 57:
                require(a <= 29 and b <= 29, "Uncovered low-distance pair")
            if a + b <= 57:
                lower_pairs.append([a, b])
    require(2 * 1848 - 58 == 3638 and 1848 - 28 == 1820 and
            1848 - 30 == 1818, "Incorrect complement bridge")
    return {"verified": True, "branches_checked": len(results),
            "original_class_sizes": [1848, 1848],
            "minimum_changes_per_original_class": 28,
            "maximum_changes_per_original_class": 1820,
            "maximum_of_edit_counts_at_least": 30,
            "minimum_of_edit_counts_at_most": 1818,
            "total_edit_bounds": [58, 3638],
            "covered_low_total_pairs_after_class_cuts": lower_pairs,
            "exceptional_prefix_positions_free": 7, "both_endpoint_values_covered": True,
            "external_numerical_cut_assumptions": 0, "branch_results": results}


def verify_directory(directory, expected=None):
    bundle, manifest = {}, []
    for name in required_names():
        raw = (directory / name).read_bytes()
        bundle[name] = json.loads(raw)
        manifest.append({"file": name, "bytes": len(raw),
                         "sha256": hashlib.sha256(raw).hexdigest()})
    result = verify_suite(bundle)
    if expected is not None:
        require(manifest == expected.get("certificates"), "Certificate bytes differ from expected manifest")
        require(result == expected.get("verification"), "Verification differs from expected results")
    return manifest, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--write-expected", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    expected = json.loads(args.expected.read_text()) if args.expected else None
    manifest, result = verify_directory(args.directory, expected)
    if args.write_expected:
        args.write_expected.write_text(json.dumps({"certificates": manifest, "verification": result},
                                                 indent=2) + "\n")
    summary = {k: v for k, v in result.items() if k != "branch_results"}
    summary["seconds"] = round(time.monotonic() - start, 3)
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
