#!/usr/bin/env python3
"""Independently check QR-617 flip transcripts and their quantified coverage.

This module does not import the generator, enumerate a search space, or trust
its status, counts, hashing, or claimed UNSAT. It checks every cited AP and
deduction with exact sets. QR colors use Euler's criterion, not square lists.
"""

import argparse
import hashlib
import json
import resource
import time
from pathlib import Path

P = 617
LAST = 3702
D = {x for x in range(LAST + 1) if x % P}
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



def weighted_bound(petals, weights, scale, remaining):
    require(type(scale) is int and scale > 0, "Invalid weighted scale")
    require(petals and len(petals) == len(weights), "Missing weighted petals")
    require(all(type(w) is int and w > 0 for w in weights), "Nonpositive or noninteger weight")
    loads = {}
    for petal, weight in zip(petals, weights):
        for x in petal:
            loads[x] = loads.get(x, 0) + weight
    require(all(load <= scale for load in loads.values()), "Weighted vertex capacity exceeded")
    require(sum(weights) > remaining * scale, "Insufficient weighted packing sum")


def verify_branch(data):
    require(isinstance(data, dict) and data.get("format") == "qr617-weighted-conditional-color-budget-v1" and
            data.get("status") == "EXCLUDED", "Not a completed branch transcript")
    budgets = budgets_of(data)
    endpoint, root = data.get("endpoint"), data.get("root")
    require(type(endpoint) is int and endpoint in (0, 1) and type(root) is int and root in D,
            "Invalid branch hypothesis")
    require(data.get("initial_forced", [root]) == [root],
            "A branch may assume only its single covering root")
    allowed = set(D)
    forced = {root}
    counts = {"forbidden": 0, "forced": 0, "packing": 0, "empty": 0, "budget": 0, "weighted": 0}
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
        elif kind == "w":
            require(len(row) == 4, "Bad weighted forbidden record")
            _, v, scale, triples = row
            require(type(v) is int and v in allowed - forced, "Invalid weighted target")
            require(isinstance(triples, list) and triples, "Missing weighted AP witnesses")
            petals = []
            weights = []
            for triple in triples:
                require(isinstance(triple, list) and len(triple) == 3, "Bad weighted AP encoding")
                a, d, weight = triple
                points = progression([a, d])
                require(v in points, "Weighted AP misses target")
                negative = {x for x in points if COLORS[x] == COLORS[v]}
                positive = points - negative
                require(negative - {v} <= forced and not (positive & forced),
                        "Weighted conditional antecedent unproved or consequent satisfied")
                petals.append(positive & allowed)
                weights.append(weight)
            opposite = 1 - COLORS[v]
            remaining = budgets[opposite] - sum(COLORS[x] == opposite for x in forced)
            weighted_bound(petals, weights, scale, remaining)
            allowed.remove(v)
            counts["forbidden"] += 1
            counts["weighted"] += 1
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
    elif reason == "required_weighted":
        side = contradiction.get("color")
        require(type(side) is int and side in (0, 1), "Invalid weighted contradiction color")
        triples = contradiction.get("aps")
        require(isinstance(triples, list) and triples, "Missing weighted required APs")
        petals = []
        weights = []
        for triple in triples:
            require(isinstance(triple, list) and len(triple) == 3, "Bad weighted required AP")
            a, d, weight = triple
            positive = mandatory_clause([a, d], endpoint, forced)
            require(all(COLORS[x] == side for x in positive), "Wrong weighted clause color")
            petals.append(positive & allowed)
            weights.append(weight)
        remaining = budgets[side] - sum(COLORS[x] == side for x in forced)
        weighted_bound(petals, weights, contradiction.get("scale"), remaining)
    else:
        raise ValueError("Unknown final contradiction")
    return {"budget": budgets, "endpoint": endpoint, "root": root,
            "forbidden_steps": counts["forbidden"], "forcing_steps": counts["forced"],
            "packing_steps": counts["packing"], "empty_steps": counts["empty"],
            "weighted_steps": counts["weighted"], "budget_steps": counts["budget"], "final_forced": len(forced),
            "final_allowed": len(allowed), "contradiction": reason}


BOXES = {0: [(28, 28), (29, 27)], 1: [(28, 28), (27, 29)]}
COROLLARY_DEPENDENCIES = [
    "bafkreifwq573peil5nytqjoomtqu3b7pvt37h2dgoypm5ut5lxe34qyp4u",
    "bafkreidsmjvpmfw3vlmkppu46wxiu3e4gder4zb7iuvcaigcecrvluj3tq",
]


def required_names():
    return [f"branch-{endpoint}-{root}-{a}-{b}.json"
            for endpoint, pair in ENDPOINT_APS.items()
            for a, b in BOXES[endpoint]
            for root in sorted(endpoint_points(pair, endpoint))]


def verify_suite(bundle):
    """Check the new box lemmas and their finite bridge to the cited lemmas.

    This directory does not reprove the two mathematical dependencies.
    They supply total>=56, a,b>=27 and e=0=>a>=28, e=1=>b>=28.
    """
    check_domain()
    require(set(bundle) == set(required_names()), "Missing, duplicated, or unexpected case coverage")
    results = []
    for endpoint, pair in ENDPOINT_APS.items():
        for a, b in BOXES[endpoint]:
            for root in sorted(endpoint_points(pair, endpoint)):
                data = bundle[f"branch-{endpoint}-{root}-{a}-{b}.json"]
                require(data.get("budget") == [a, b] and data.get("endpoint") == endpoint and
                        data.get("root") == root, "Wrong branch for quantified coverage")
                results.append(verify_branch(data))
    residual_triples = []
    for endpoint in (0, 1):
        for a in range(27, 30):
            b = 56 - a
            if b < 27 or (endpoint == 0 and a < 28) or (endpoint == 1 and b < 28):
                continue
            require(any(a <= x and b <= y for x, y in BOXES[endpoint]),
                    "Uncovered total56 triple after the cited prior inequalities")
            residual_triples.append([endpoint, a, b])
    require(len(residual_triples) == 4, "Wrong total56 bridge coverage")
    return {"verified_new_box_exclusions": True, "covering_branches": len(results),
            "excluded_boxes_by_endpoint": {str(e): [list(p) for p in BOXES[e]] for e in (0, 1)},
            "corollary": {"required_total_changes": 57, "maximum_total_changes": 3639,
                          "conditional_on_prior_published_lemmas": COROLLARY_DEPENDENCIES,
                          "checked_residual_total56_triples": residual_triples,
                          "complement_total": len(D)},
            "exceptional_prefix_positions_free": 7, "new_endpoint_free": True,
            "conditional_branches": results}


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
    parser.add_argument("--expected", type=Path, default=Path(__file__).resolve().parent / "expected.json")
    args = parser.parse_args()
    start = time.monotonic()
    expected = json.loads(args.expected.read_text())
    result = verify_directory(args.directory, expected)
    print(json.dumps({"verified_new_box_exclusions": result["verified_new_box_exclusions"],
                      "covering_branches": result["covering_branches"],
                      "corollary": result["corollary"],
                      "seconds": round(time.monotonic() - start, 3),
                      "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == "__main__":
    main()
