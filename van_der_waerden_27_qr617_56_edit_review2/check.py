#!/usr/bin/env python3
"""six-reviewer-2's independent Boolean-clause QR617 certificate checker.

No generator or original verifier imports. Quadratic reciprocity computes
colors; integer masks encode clauses and true/false partial assignments.
Every geometric witness and inference is checked before updating state.
"""

import argparse
import hashlib
import json
from pathlib import Path

PRIME, LAST = 617, 3702
CAPS = ((26, 1848), (1848, 26), (27, 28))
BRANCH_CAP = (28, 27)
ENDPOINT_AP = ((1, 617), (3421, 47))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def integer(x):
    return type(x) is int


def jacobi(a, n):
    """Jacobi symbol by the supplement for 2 and quadratic reciprocity."""
    require(integer(a) and integer(n) and n > 0 and n % 2, "Jacobi domain")
    a %= n
    sign = 1
    while a:
        while not a % 2:
            a //= 2
            if n % 8 in (3, 5):
                sign = -sign
        a, n = n, a
        if a % 4 == n % 4 == 3:
            sign = -sign
        a %= n
    return sign if n == 1 else 0


require(all(PRIME % d for d in range(2, 25)), "617 primality")
COLOR = {x: int(jacobi(x, PRIME) == -1)
         for x in range(LAST + 1) if x % PRIME}
CLASS = tuple(sum(1 << x for x, c in COLOR.items() if c == i) for i in (0, 1))
DOMAIN = CLASS[0] | CLASS[1]
require(DOMAIN.bit_count() == 3696 and
        all(m.bit_count() == 1848 for m in CLASS), "QR domain sizes")
require(all(COLOR[x] == COLOR[LAST - x] for x in COLOR), "QR reflection")


def variable(v):
    require(integer(v) and v in COLOR, "Variable outside nonpole domain")
    return 1 << v


def ap_points(pair, endpoint=False):
    require(type(pair) is list and len(pair) == 2 and
            all(integer(t) for t in pair), "AP encoding")
    start, step = pair
    require(start >= 0 and step > 0, "AP must be nonconstant and nonnegative")
    end = start + 6 * step
    require(end == LAST + 1 if endpoint else end <= LAST, "AP interval")
    points = [start + j * step for j in range(6 if endpoint else 7)]
    require(all(x in COLOR for x in points), "AP uses a free pole")
    return points


def prefix_clause(pair):
    points = ap_points(pair)
    masks = tuple(sum(1 << x for x in points if COLOR[x] == i) for i in (0, 1))
    return masks  # Clause i has negative literals masks[i], positive masks[1-i].


def endpoint_clause(pair, endpoint):
    points = ap_points(pair, endpoint=True)
    require(all(COLOR[x] == endpoint for x in points), "Endpoint original color")
    return sum(1 << x for x in points)


def mandatory(pair, endpoint, true):
    require(type(pair) is list and len(pair) == 2 and
            all(integer(t) for t in pair), "Mandatory AP encoding")
    if pair[0] + 6 * pair[1] == LAST + 1:
        positive = endpoint_clause(pair, endpoint)
        require(not positive & true, "Endpoint clause already satisfied")
        return positive
    masks = prefix_clause(pair)
    for negative, positive in (masks, masks[::-1]):
        if not negative & ~true and not positive & true:
            return positive
    raise ValueError("No active mandatory AP clause")


def disjoint(petals, needed):
    require(integer(needed) and needed > 0 and len(petals) == needed,
            "Packing cardinality does not exceed remaining budget")
    used = 0
    for petal in petals:
        require(petal != 0 and not petal & used, "Empty or overlapping packing")
        used |= petal


def cap(data):
    value = data.get("budget")
    require(type(value) is list and len(value) == 2 and
            all(integer(x) and 0 <= x <= 1848 for x in value), "Budget encoding")
    return value


def prefix_step(v, witnesses, false, budgets):
    bit = variable(v)
    require(not bit & false, "Variable already excluded")
    require(type(witnesses) is list and witnesses, "Missing critical witnesses")
    petals = []
    for pair in witnesses:
        masks = prefix_clause(pair)
        require(masks[COLOR[v]] == bit, "Critical clause negative side not singleton")
        petals.append(masks[1 - COLOR[v]] & ~false)
    if 0 in petals:
        return "empty"
    disjoint(petals, budgets[1 - COLOR[v]] + 1)
    return "packing"


def check_prefix(data):
    require(type(data) is dict and data.get("format") == "qr617-color-budget-v1"
            and data.get("status") == "EXCLUDED_NONEMPTY"
            and data.get("reflect_each_record") is True, "Prefix header")
    budgets, rows = cap(data), data.get("records")
    require(type(rows) is list, "Prefix records")
    false, packing, empty = 0, 0, 0
    for row in rows:
        require(type(row) is list and len(row) == 2, "Prefix row")
        v, witnesses = row
        reason = prefix_step(v, witnesses, false, budgets)
        partner = LAST - v
        reflected = [[LAST - (a + 6 * d), d] for a, d in witnesses]
        # Both proofs read the same false mask; no symmetry of S is assumed.
        require(partner != v and
                prefix_step(partner, reflected, false, budgets) == reason,
                "Reflected deduction invalid")
        false |= variable(v) | variable(partner)
        packing += reason == "packing"
        empty += reason == "empty"
    require(false == DOMAIN, "Prefix does not exclude all variables")
    return {"budget": budgets, "records": len(rows), "packing_records": packing,
            "empty_records": empty, "eliminated_positions": false.bit_count()}


def check_branch(data):
    require(type(data) is dict and
            data.get("format") == "qr617-conditional-color-budget-v1" and
            data.get("status") == "EXCLUDED", "Branch header")
    budgets = cap(data)
    endpoint, root = data.get("endpoint"), data.get("root")
    require(integer(endpoint) and endpoint in (0, 1), "Endpoint value")
    true, false = variable(root), 0
    rows = data.get("records")
    require(type(rows) is list, "Branch records")
    counts = {"f": 0, "t": 0, "packing": 0, "empty": 0, "budget": 0}
    for row in rows:
        require(type(row) is list and row, "Branch row")
        tag = row[0]
        if tag == "f":
            require(len(row) == 3, "Forbid row")
            _, v, witnesses = row
            bit = variable(v)
            require(not bit & (true | false), "Forbid assigned variable")
            require(type(witnesses) is list and witnesses, "Conditional witnesses")
            petals = []
            for pair in witnesses:
                masks = prefix_clause(pair)
                negative, positive = masks[COLOR[v]], masks[1 - COLOR[v]]
                require(negative & bit and not (negative ^ bit) & ~true and
                        not positive & true, "Unproved antecedent or satisfied clause")
                petals.append(positive & ~false)
            if 0 in petals:
                counts["empty"] += 1
            else:
                opposite = 1 - COLOR[v]
                remaining = budgets[opposite] - (true & CLASS[opposite]).bit_count()
                disjoint(petals, remaining + 1)
                counts["packing"] += 1
            false |= bit
        elif tag == "t":
            require(len(row) == 4, "Force row")
            _, v, a, d = row
            bit = variable(v)
            require(not bit & (true | false), "Force assigned variable")
            require(mandatory([a, d], endpoint, true) & ~false == bit,
                    "Forcing clause is not a unit")
            true |= bit
        elif tag == "budget":
            require(len(row) == 2 and integer(row[1]) and row[1] in (0, 1),
                    "Budget row")
            side = row[1]
            require((true & CLASS[side]).bit_count() == budgets[side],
                    "Class budget not exhausted")
            false |= CLASS[side] & ~true
        else:
            raise ValueError("Unknown proof rule")
        counts[tag] += 1
        require(not true & false, "Inconsistent partial assignment")
    terminal = data.get("contradiction")
    require(type(terminal) is dict, "Terminal contradiction")
    reason = terminal.get("reason")
    if reason == "too_many_forced":
        require(any((true & CLASS[i]).bit_count() > budgets[i] for i in (0, 1)),
                "No budget violation")
    elif reason == "empty_required":
        require(not mandatory(terminal.get("ap"), endpoint, true) & ~false,
                "Mandatory clause is not empty")
    elif reason == "required_packing":
        side, pairs = terminal.get("color"), terminal.get("aps")
        require(integer(side) and side in (0, 1) and type(pairs) is list,
                "Terminal packing encoding")
        petals = []
        for pair in pairs:
            positive = mandatory(pair, endpoint, true)
            require(not positive & ~CLASS[side], "Terminal packing class")
            petals.append(positive & ~false)
        disjoint(petals, budgets[side] - (true & CLASS[side]).bit_count() + 1)
    else:
        raise ValueError("Unknown terminal contradiction")
    return {"budget": budgets, "endpoint": endpoint, "root": root,
            "forbidden_steps": counts["f"], "forcing_steps": counts["t"],
            "packing_steps": counts["packing"], "empty_steps": counts["empty"],
            "budget_steps": counts["budget"], "final_forced": true.bit_count(),
            "final_allowed": (DOMAIN & ~false).bit_count(), "contradiction": reason}


def cases():
    result = [(f"prefix-{a}-{b}.json", (a, b), None, None) for a, b in CAPS]
    for endpoint, pair in enumerate(ENDPOINT_AP):
        mask = endpoint_clause(list(pair), endpoint)
        for root in range(LAST + 1):
            if mask & (1 << root):
                result.append((f"branch-{endpoint}-{root}.json", BRANCH_CAP, endpoint, root))
    return result


def check_suite(bundle):
    required = cases()
    require(set(bundle) == {c[0] for c in required}, "Incomplete or extra case cover")
    prefixes, branches = [], []
    for filename, budgets, endpoint, root in required:
        data = bundle[filename]
        require(type(data) is dict and data.get("budget") == list(budgets),
                "Case budget mismatch")
        if endpoint is None:
            prefixes.append(check_prefix(data))
        else:
            require(data.get("endpoint") == endpoint and data.get("root") == root,
                    "Endpoint/root case substitution")
            branches.append(check_branch(data))
    nonempty_pairs = [(a, total - a) for total in range(1, 56)
                      for a in range(total + 1)]
    gap = [pair for pair in nonempty_pairs
           if not any(pair[0] <= x and pair[1] <= y for x, y in CAPS)]
    require(len(nonempty_pairs) == 1595 and gap == [(28, 27)], "Budget case reduction")
    # The endpoint clauses also exclude S=empty. No pole values enter the clauses.
    return {"verified": True, "required_nonzero_changes": 56,
            "maximum_nonzero_changes": DOMAIN.bit_count() - 56,
            "required_changes_per_original_color": [27, 27],
            "maximum_changes_per_original_color": [m.bit_count() - 27 for m in CLASS],
            "prefix_rigidity_through_total_changes": 54,
            "checked_nonempty_cardinality_pairs": len(nonempty_pairs),
            "exceptional_prefix_positions_free": LAST + 1 - DOMAIN.bit_count(),
            "new_endpoint_free": True,
            "prefix_certificates": prefixes, "conditional_branches": branches}


def read_bundle(directory):
    names = [c[0] for c in cases()]
    require({p.name for p in directory.glob("*.json")} - {"manifest.json"} == set(names),
            "Directory case coverage")
    bundle, hashes = {}, []
    for name in names:
        raw = (directory / name).read_bytes()
        bundle[name] = json.loads(raw)
        hashes.append({"file": name, "bytes": len(raw),
                       "sha256": hashlib.sha256(raw).hexdigest()})
    return bundle, hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--target-expected", type=Path,
                        help="Optional comparison after independent proof checking")
    args = parser.parse_args()
    bundle, hashes = read_bundle(args.directory)
    result = {"certificates": hashes, "verification": check_suite(bundle)}
    if args.target_expected:
        expected = json.loads(args.target_expected.read_text())
        require(result == expected, "Checked result/bytes differ from target manifest")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
