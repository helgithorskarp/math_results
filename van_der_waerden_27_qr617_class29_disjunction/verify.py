"""Exact mandatory-petal disjunction checker, independent of generation.

The old strict single-root checker is unchanged. A child starts only from
its replayed parent's U/T and its one explicitly covered petal assumption.
No certificate-provided U/T or extra hypothesis is trusted.
"""
import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path

CORE_PATH = Path(__file__).resolve().parent.parent / "van_der_waerden_27_qr617_mixed_edit_region/verify.py"
spec = importlib.util.spec_from_file_location("tree_AP_definitions", CORE_PATH)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
require = core.require
D, COLORS = core.D, core.COLORS
FORMAT = "qr617-mandatory-petal-tree-v1"
TRACE_FORMAT = "qr617-mixed-conditional-color-budget-v1"


def replay(trace, endpoint, root, budgets, start_allowed, start_forced, complete):
    """Replay primitives from a state supplied by the recursive checker only."""
    require(isinstance(trace, dict) and trace.get("format") == TRACE_FORMAT,
            "Invalid primitive format")
    require(trace.get("endpoint") == endpoint and trace.get("root") == root and
            trace.get("budget") == budgets, "Child metadata differs from its parent")
    require(type(trace.get("endpoint")) is int and type(trace.get("root")) is int and
            core.budgets_of(trace) == budgets, "Noninteger primitive metadata")
    require(not ({"initial_forced", "allowed_positions", "forced_positions"} & trace.keys()),
            "Certificate-supplied initial state or hypotheses")
    require(trace.get("status") in ("EXCLUDED", "STALLED", "INCOMPLETE_TIME_LIMIT"),
            "Unknown primitive status")
    if complete:
        require(trace.get("status") == "EXCLUDED", "Incomplete primitive leaf")
    allowed, forced = set(start_allowed), set(start_forced)
    require(forced <= allowed <= D, "Invalid inherited state")
    counts = {"forbidden": 0, "forced": 0, "packing": 0, "empty": 0,
              "budget": 0, "mixed": 0}
    rows = trace.get("records")
    require(isinstance(rows, list), "Missing primitive records")
    for row in rows:
        require(isinstance(row, list) and row, "Invalid primitive record")
        kind = row[0]
        if kind in ("f", "m"):
            require(len(row) == 3, "Invalid forbidden record")
            _, v, pairs = row
            require(type(v) is int and v in allowed - forced, "Invalid forbidden target")
            require(isinstance(pairs, list) and pairs, "Missing AP witnesses")
            petals = []
            for pair in pairs:
                require(isinstance(pair, list) and len(pair) == 2 and
                        all(type(x) is int for x in pair), "Invalid AP encoding")
                a, d = pair
                if kind == "m" and a + 6 * d == core.LAST + 1:
                    positive = core.endpoint_points(pair, endpoint)
                    require(all(COLORS[x] == 1 - COLORS[v] for x in positive) and
                            not (positive & forced), "Wrong or satisfied endpoint petal")
                else:
                    points = core.progression(pair)
                    if kind == "f":
                        require(v in points, "Strict conditional AP omits target")
                    negative = {x for x in points if COLORS[x] == COLORS[v]}
                    positive = points - negative
                    require(negative - {v} <= forced and not (positive & forced),
                            "Unproved antecedent or satisfied consequent")
                petals.append(positive & allowed)
            if any(not petal for petal in petals):
                counts["empty"] += 1
            else:
                side = 1 - COLORS[v]
                remaining = budgets[side] - sum(COLORS[x] == side for x in forced)
                core.check_packing(petals, remaining + 1)
                counts["packing"] += 1
            allowed.remove(v)
            counts["forbidden"] += 1
            counts["mixed"] += int(kind == "m")
        elif kind == "t":
            require(len(row) == 4, "Invalid forcing record")
            _, v, a, d = row
            require(type(v) is int and v in allowed - forced, "Invalid forced target")
            positive = core.mandatory_clause([a, d], endpoint, forced)
            require(positive & allowed == {v}, "Mandatory petal not a singleton")
            forced.add(v)
            counts["forced"] += 1
        elif kind == "budget":
            require(len(row) == 2 and type(row[1]) is int and row[1] in (0, 1),
                    "Invalid exhausted-budget record")
            side = row[1]
            require(sum(COLORS[x] == side for x in forced) == budgets[side],
                    "Class budget not exhausted")
            allowed = {x for x in allowed if COLORS[x] != side or x in forced}
            counts["budget"] += 1
        else:
            raise ValueError("Unknown primitive deduction")
        require(forced <= allowed, "Forced edit was forbidden")
    if complete:
        contradiction = trace.get("contradiction")
        require(isinstance(contradiction, dict), "Missing terminal contradiction")
        reason = contradiction.get("reason")
        if reason == "too_many_forced":
            require(any(sum(COLORS[x] == c for x in forced) > budgets[c] for c in (0, 1)),
                    "No class-count contradiction")
        elif reason == "empty_required":
            positive = core.mandatory_clause(contradiction.get("ap"), endpoint, forced)
            require(not (positive & allowed), "Required petal not empty")
        elif reason == "required_packing":
            side, pairs = contradiction.get("color"), contradiction.get("aps")
            require(type(side) is int and side in (0, 1) and isinstance(pairs, list),
                    "Invalid terminal packing")
            petals = []
            for pair in pairs:
                positive = core.mandatory_clause(pair, endpoint, forced)
                require(all(COLORS[x] == side for x in positive), "Wrong terminal class")
                petals.append(positive & allowed)
            remaining = budgets[side] - sum(COLORS[x] == side for x in forced)
            core.check_packing(petals, remaining + 1)
        else:
            raise ValueError("Unknown terminal contradiction")
    return allowed, forced, counts


def verify_tree(data, complete=True, include_state=False):
    core.check_domain()
    require(isinstance(data, dict) and data.get("format") == FORMAT, "Invalid tree format")
    budgets = core.budgets_of(data)
    endpoint, root = data.get("endpoint"), data.get("root")
    require(type(endpoint) is int and endpoint in (0, 1) and type(root) is int and
            root in core.endpoint_points(core.ENDPOINT_APS[endpoint], endpoint),
            "Tree root outside the prescribed endpoint cover")
    require(not ({"initial_forced", "allowed_positions", "forced_positions"} & data.keys()),
            "Tree supplied additional initial hypotheses")
    nodes = splits = 0
    totals = {"forbidden": 0, "forced": 0, "packing": 0, "empty": 0,
              "budget": 0, "mixed": 0}
    leaves = []

    def check_node(node, allowed, forced, path):
        nonlocal nodes, splits
        require(isinstance(node, dict) and set(node) <= {"trace", "split"} and
                "trace" in node, "Invalid tree node fields")
        nodes += 1
        trace = node["trace"]
        has_split = "split" in node
        leaf_closed = isinstance(trace, dict) and trace.get("status") == "EXCLUDED"
        require(not (has_split and leaf_closed), "Already closed trace has a split")
        U, T, counts = replay(trace, endpoint, root, budgets, allowed, forced,
                              complete=leaf_closed)
        for key, value in counts.items():
            totals[key] += value
        if not has_split:
            item = {"path": path, "closed": leaf_closed, "allowed": len(U),
                    "forced": len(T), "counts": counts}
            if include_state:
                item.update(allowed_positions=sorted(U), forced_positions=sorted(T))
            leaves.append(item)
            return leaf_closed
        split = node["split"]
        require(isinstance(split, dict) and set(split) == {"ap", "children"},
                "Invalid split fields")
        positive = core.mandatory_clause(split["ap"], endpoint, T)
        petal = positive & U
        require(petal, "Empty mandatory petal should be a terminal contradiction")
        children = split["children"]
        require(isinstance(children, list) and len(children) == len(petal),
                "Incomplete or duplicated disjunctive coverage")
        hypotheses = []
        for child in children:
            require(isinstance(child, dict) and set(child) == {"assumption", "node"},
                    "Invalid child fields")
            value = child["assumption"]
            require(type(value) is int and value in petal and value not in T,
                    "Child assumption outside the required petal")
            hypotheses.append(value)
        require(len(set(hypotheses)) == len(hypotheses) and set(hypotheses) == petal,
                "Missing or repeated petal child")
        splits += 1
        # Evaluate every child; short circuiting would hide unchecked coverage.
        outcomes = [check_node(child["node"], U, T | {child["assumption"]},
                               path + [child["assumption"]]) for child in children]
        return all(outcomes)

    closed = check_node(data.get("node"), set(D), {root}, [])
    require(not complete or closed, "Open leaf prevents parent exclusion")
    return {"agent": "six-vdw-2", "role": "researcher", "endpoint": endpoint,
            "root": root, "budget": budgets, "closed": closed, "nodes": nodes,
            "splits": splits, "leaves": leaves, "step_totals": totals}


def required_names():
    return [f"tree-0-{root}-28-1848.json" for root in
            sorted(core.endpoint_points(core.ENDPOINT_APS[0], 0))]


def verify_suite(bundle):
    """Establish the new e=0 cut only; PROOF.md states the dependent corollary."""
    core.check_domain()
    require(isinstance(bundle, dict) and set(bundle) == set(required_names()),
            "Missing or unexpected endpoint-root tree coverage")
    results = []
    for root, name in zip(sorted(core.endpoint_points(core.ENDPOINT_APS[0], 0)),
                          required_names()):
        data = bundle[name]
        require(data.get("endpoint") == 0 and data.get("root") == root and
                data.get("budget") == [28, 1848], "Wrong full-width quantified case")
        results.append(verify_tree(data))
    require(len(results) == 6 and all(x["closed"] for x in results),
            "Incomplete root cover")
    totals = {key: sum(x["step_totals"][key] for x in results)
              for key in results[0]["step_totals"]}
    return {"verified": True, "endpoint": 0, "excluded_budget": [28, 1848],
            "original_class_sizes": [1848, 1848],
            "endpoint0_original_class0_edits_at_least": 29,
            "other_original_class_edits_unrestricted": True,
            "exceptional_prefix_positions_free": 7,
            "trees_checked": len(results),
            "nodes_checked": sum(x["nodes"] for x in results),
            "splits_checked": sum(x["splits"] for x in results),
            "leaves_checked": sum(len(x["leaves"]) for x in results),
            "step_totals": totals, "tree_results": results}


def verify_directory(directory, expected=None):
    bundle, manifest = {}, []
    for name in required_names():
        raw = (directory / name).read_bytes()
        bundle[name] = json.loads(raw)
        manifest.append({"file": name, "bytes": len(raw),
                         "sha256": hashlib.sha256(raw).hexdigest()})
    result = verify_suite(bundle)
    if expected is not None:
        require(manifest == expected.get("certificates"), "Bytes differ from reference manifest")
        require(result == expected.get("verification"), "Checking differs from reference results")
    return {"certificates": manifest, "verification": result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--write-expected", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    expected = json.loads(args.expected.read_text()) if args.expected else None
    result = verify_directory(args.directory, expected)
    if args.write_expected:
        args.write_expected.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result["verification"].items()
                      if k != "tree_results"}, sort_keys=True))
    print(json.dumps({"checking_seconds": round(time.monotonic() - start, 3)}, sort_keys=True))


if __name__ == "__main__":
    main()
