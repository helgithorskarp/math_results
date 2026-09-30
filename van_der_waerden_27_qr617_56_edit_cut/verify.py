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
PREFIX_BUDGETS = [(26, 1848), (1848, 26), (27, 28)]
ENDPOINT_APS = {0: [1, 617], 1: [3421, 47]}


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
    require(all(COLORS[x] == COLORS[LAST - x] for x in D), "Reflection changes colors")


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


def check_prefix_deduction(v, pairs, allowed, budgets):
    require(type(v) is int and v in allowed, "Duplicate or invalid forbidden vertex")
    require(isinstance(pairs, list) and pairs, "Missing AP witnesses")
    petals = []
    for pair in pairs:
        points = progression(pair)
        require(v in points and all(COLORS[x] == 1 - COLORS[v] for x in points - {v}),
                "AP is not critical at the target")
        petals.append((points - {v}) & allowed)
    if any(not petal for petal in petals):
        return "empty"
    check_packing(petals, budgets[1 - COLORS[v]] + 1)
    return "packing"


def verify_prefix(data):
    require(isinstance(data, dict) and data.get("format") == "qr617-color-budget-v1" and
            data.get("status") == "EXCLUDED_NONEMPTY", "Not a completed prefix transcript")
    budgets = budgets_of(data)
    require(data.get("reflect_each_record") is True, "Reflection flag missing")
    records = data.get("records")
    require(isinstance(records, list), "Missing records")
    allowed = set(D)
    counts = {"packing": 0, "empty": 0}
    for row in records:
        require(isinstance(row, list) and len(row) == 2, "Bad prefix record")
        v, pairs = row
        kind = check_prefix_deduction(v, pairs, allowed, budgets)
        w = LAST - v
        reflected = [[LAST - (a + 6 * d), d] for a, d in pairs]
        require(v != w and check_prefix_deduction(w, reflected, allowed, budgets) == kind,
                "Invalid reflected deduction")
        allowed.remove(v)
        allowed.remove(w)
        counts[kind] += 1
    require(not allowed, "Incomplete prefix vertex coverage")
    return {"budget": budgets, "records": len(records), "packing_records": counts["packing"],
            "empty_records": counts["empty"], "eliminated_positions": len(D)}


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


def verify_branch(data):
    require(isinstance(data, dict) and data.get("format") == "qr617-conditional-color-budget-v1" and
            data.get("status") == "EXCLUDED", "Not a completed branch transcript")
    budgets = budgets_of(data)
    endpoint, root = data.get("endpoint"), data.get("root")
    require(type(endpoint) is int and endpoint in (0, 1) and type(root) is int and root in D,
            "Invalid branch hypothesis")
    allowed = set(D)
    forced = {root}
    counts = {"forbidden": 0, "forced": 0, "packing": 0, "empty": 0, "budget": 0}
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
            "budget_steps": counts["budget"], "final_forced": len(forced),
            "final_allowed": len(allowed), "contradiction": reason}


def required_names():
    names = [f"prefix-{a}-{b}.json" for a, b in PREFIX_BUDGETS]
    for endpoint, pair in ENDPOINT_APS.items():
        for root in sorted(endpoint_points(pair, endpoint)):
            names.append(f"branch-{endpoint}-{root}.json")
    return names


def verify_suite(bundle):
    check_domain()
    require(set(bundle) == set(required_names()), "Missing, duplicated, or unexpected case coverage")
    prefix_results = []
    for a, b in PREFIX_BUDGETS:
        data = bundle[f"prefix-{a}-{b}.json"]
        require(data.get("budget") == [a, b], "Wrong prefix budget for coverage")
        prefix_results.append(verify_prefix(data))
    branch_results = []
    for endpoint, pair in ENDPOINT_APS.items():
        # The same AP excludes S=empty and supplies all six covering roots.
        for root in sorted(endpoint_points(pair, endpoint)):
            data = bundle[f"branch-{endpoint}-{root}.json"]
            require(data.get("budget") == [28, 27] and data.get("endpoint") == endpoint and
                    data.get("root") == root, "Wrong branch for coverage")
            branch_results.append(verify_branch(data))
    checked_pairs = 0
    for a in range(56):
        for b in range(56 - a):
            if a + b == 0:
                continue
            prefix_covered = any(a <= x and b <= y for x, y in PREFIX_BUDGETS)
            require(prefix_covered or (a <= 28 and b <= 27), "Uncovered cardinality pair")
            checked_pairs += 1
    return {"verified": True, "required_nonzero_changes": 56, "maximum_nonzero_changes": 3640,
            "required_changes_per_original_color": [27, 27],
            "maximum_changes_per_original_color": [1821, 1821],
            "prefix_rigidity_through_total_changes": 54,
            "checked_nonempty_cardinality_pairs": checked_pairs,
            "exceptional_prefix_positions_free": 7, "new_endpoint_free": True,
            "prefix_certificates": prefix_results, "conditional_branches": branch_results}


def verify_directory(directory, expected=None):
    bundle = {}
    items = []
    for name in required_names():
        raw = (directory / name).read_bytes()
        bundle[name] = json.loads(raw)
        items.append({"file": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    result = verify_suite(bundle)
    if expected is not None:
        require(items == expected.get("certificates"), "Transcript bytes differ from published manifest")
        require(result == expected.get("verification"), "Verified results differ from expected results")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path("build"))
    parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("expected.json"))
    args = parser.parse_args()
    start = time.monotonic()
    result = verify_directory(args.directory, json.loads(args.expected.read_text()))
    result["seconds"] = round(time.monotonic() - start, 3)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
