#!/usr/bin/env python3
"""Definition-level QR617 proof checking, without importing any generator.

Same-author reuse of the earlier independent Euler/set checker. Each AP,
forced antecedent, packing and final contradiction is checked directly.
No enumeration exhaustion, solver status or file hash proves a claim here.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

P=617
LAST=3702
D={x for x in range(LAST+1) if x%P}
ENDPOINT_APS={0:[1,617],1:[3421,47]}
CAPS={0:[27,1848],1:[1848,27]}

def require(condition, message):
    if not condition:
        raise ValueError(message)


def color(x):
    require(type(x) is int and x in D, "Color requested outside prescribed domain")
    value = pow(x % P, (P - 1) // 2, P)
    require(value in (1, P - 1), "Euler criterion failed")
    return int(value == P - 1)

COLORS={x:color(x) for x in D}

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
    return [f'branch-{endpoint}-{root}.json' for endpoint,pair in ENDPOINT_APS.items()
            for root in sorted(endpoint_points(pair,endpoint))]


def verify_suite(bundle):
    check_domain()
    require(set(bundle)==set(required_names()),'Missing or unexpected branch coverage')
    results=[]
    for endpoint,pair in ENDPOINT_APS.items():
        for root in sorted(endpoint_points(pair,endpoint)):
            data=bundle[f'branch-{endpoint}-{root}.json']
            require(data.get('budget')==CAPS[endpoint] and data.get('endpoint')==endpoint and
                    data.get('root')==root,'Wrong case or unrestricted opposite budget')
            results.append(verify_branch(data))
    return {'verified':True,'minimum_changes_in_original_endpoint_color_class':28,
            'maximum_changes_in_original_opposite_color_class':1820,
            'unrestricted_other_class_size':1848,'prescribed_nonzero_positions':3696,
            'exceptional_prefix_positions_free':7,'new_endpoint_free':True,
            'conditional_branches':results}


def verify_directory(directory,expected=None):
    bundle={};items=[]
    for name in required_names():
        raw=(directory/name).read_bytes();bundle[name]=json.loads(raw)
        items.append({'file':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    result=verify_suite(bundle)
    if expected is not None:
        require(items==expected.get('certificates'),'Transcript bytes differ from manifest')
        require(result==expected.get('verification'),'Results differ from published expectations')
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',nargs='?',type=Path,default=Path('build'))
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    args=parser.parse_args();start=time.monotonic()
    result=verify_directory(args.directory,json.loads(args.expected.read_text()))
    result['seconds']=round(time.monotonic()-start,3)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
