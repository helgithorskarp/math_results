"""Exact outer root coverage and strict/generic replay for one asymmetric box."""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import resource
import time

import verify as v
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("directory", type=Path)
p.add_argument("--endpoint", type=int, choices=[0, 1], required=True)
p.add_argument("--budget", type=int, nargs=2, required=True)
p.add_argument("--output", type=Path, required=True)
a = p.parse_args()
e, B = a.endpoint, a.budget
v.require(B in [[30, 32], [32, 30]], "Unsupported asymmetric box")
DATA = a.directory
v.core.check_domain()
ap = v.core.ENDPOINT_APS[e]
terms = [ap[0] + i * ap[1] for i in range(7)]
v.require(ap[1] > 0 and terms[-1] == 3703 and
          all(x in v.D and v.COLORS[x] == e for x in terms[:-1]),
          "Invalid endpoint monochromatic root cover")
roots = sorted(v.core.endpoint_points(ap, e))
v.require(roots == sorted(terms[:-1]) and len(roots) == 6, "Incomplete derived outer cover")
names = [v.filename(e, root, B) for root in roots]


def suite(bundle):
    return v.verify_box(bundle, e, B)


start = time.monotonic()
manifest, bundle = [], {}
for name in names:
    raw = (DATA / name).read_bytes()
    bundle[name] = json.loads(raw)
    manifest.append({"file": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
results = suite(bundle)
regressions = []
for name in names:
    data = bundle[name]
    trace = data["node"]["trace"]
    parent_only = {**data, "node": {"trace": trace}}
    generic = v.verify_tree(parent_only, complete=False, include_state=True)
    strict = v.core.verify_branch(trace, complete=False, include_state=True)
    terminal_checked = trace["status"] == "EXCLUDED"
    if terminal_checked:
        v.core.verify_branch(trace)
    else:
        v.require(trace["status"] == "STALLED" and "split" in data["node"],
                  "Open parent has no complete checked disjunction")
    leaf = generic["leaves"][0]
    v.require(leaf["allowed_positions"] == strict["allowed_positions"] and
              leaf["forced_positions"] == strict["forced_positions"] and
              leaf["counts"] == strict["step_counts"], "Strict/generic full states disagree")
    regressions.append({"file": name, "allowed": leaf["allowed"], "forced": leaf["forced"],
                        "counts": leaf["counts"], "strict_generic_full_states_equal": True,
                        "strict_terminal_checked": terminal_checked,
                        "parent_status": trace["status"]})
rejections = []


def reject(label, mutate):
    # Only the designated first proof is mutated. The other roots are read
    # without mutation; missing-root controls change only this new mapping.
    altered = dict(bundle)
    altered[names[0]] = copy.deepcopy(bundle[names[0]])
    mutate(altered)
    try:
        suite(altered)
    except ValueError as error:
        rejections.append({"name": label, "reason": str(error)})
    else:
        raise ValueError("Corruption accepted: " + label)


for name in names:
    reject("missing_root_" + name, lambda b, name=name: b.pop(name))
first = names[0]


def terminal_trace(b):
    node = b[first]["node"]
    while "split" in node:
        node = node["split"]["children"][0]["node"]
    return node["trace"]


target_state = v.verify_tree(bundle[first], include_state=True)["leaves"][0]
v.require(all(sum(v.COLORS[x] == c for x in target_state["forced_positions"]) <= B[c]
              for c in (0,1)), "False class-count control needs a terminal with unexhausted counts")
reject("Boolean_endpoint", lambda b: b[first].update(endpoint=bool(e)))
reject("wrong_endpoint", lambda b: b[first].update(endpoint=1-e))
reject("wrong_root", lambda b: b[first].update(root=0))
reject("unsupported_budget", lambda b: b[first].update(budget=[B[0]+1, B[1]]))
reject("swapped_class_budget", lambda b: b[first].update(budget=B[::-1]))
reject("extra_initial_hypothesis", lambda b: b[first].update(initial_forced=[1]))
reject("supplied_initial_state", lambda b: b[first]["node"]["trace"].update(allowed_positions=[1]))
reject("incomplete_terminal", lambda b: terminal_trace(b).update(status="STALLED", contradiction={}))
reject("false_terminal", lambda b: terminal_trace(b).update(contradiction={"reason": "too_many_forced"}))
if "split" in bundle[first]["node"]:
    split = lambda b: b[first]["node"]["split"]
    reject("missing_child", lambda b: split(b)["children"].pop())
    reject("duplicated_child", lambda b: split(b)["children"].__setitem__(1, copy.deepcopy(split(b)["children"][0])))
    reject("child_outside_full_petal", lambda b: split(b)["children"][0].update(assumption=1))
    reject("Boolean_child", lambda b: split(b)["children"][0].update(assumption=True))
    reject("nonmandatory_split", lambda b: split(b).update(ap=[2,1]))
    reject("changed_child_budget", lambda b: split(b)["children"][0]["node"]["trace"].update(budget=[B[0]+1,B[1]]))
    reject("extra_child_hypothesis", lambda b: split(b)["children"][0]["node"]["trace"].update(initial_forced=[1,2]))
    reject("supplied_child_state", lambda b: split(b)["children"][0]["node"]["trace"].update(allowed_positions=[]))
record = {"agent": "six-vdw-2", "role": "researcher", "status": "EXACT_BOX_AND_CHECKER_CONTROLS_PASSED",
    "endpoint": e, "excluded_original_budget": B, "root_AP": ap, "root_AP_terms": terms,
    "roots": roots, "quantified_root_cover_complete": True, "every_required_root_closed": True,
    "independent_lemma": f"No seven-AP-free coloring has endpoint{e}, a<={B[0]}, b<={B[1]} at fixed aligned QR617",
    "earlier_numerical_bounds_used_by_this_box_proof": False,
    "manifest": manifest, "root_results": results, "full_state_regressions": regressions,
    "nodes_checked": sum(r["nodes"] for r in results),
    "splits_checked": sum(r["splits"] for r in results),
    "leaves_checked": sum(len(r["leaves"]) for r in results),
    "corruption_controls": rejections, "controls_rejected": len(rejections),
    "step_totals": {k: sum(r["step_totals"][k] for r in results)
                    for k in ["forbidden", "forced", "packing", "empty", "mixed", "budget"]},
    "proof_corpus_bytes": sum(x["bytes"] for x in manifest), "public_corpus_published": False,
    "total63_or_unrestricted_nonexistence_asserted_by_this_single_box": False}
a.output.write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({"exact_box_excluded": True, "endpoint": e, "budget": B, "roots_checked": len(roots),
                  "full_state_regressions": len(regressions), "controls_rejected": len(rejections),
                  "step_totals": record["step_totals"], "proof_corpus_bytes": record["proof_corpus_bytes"],
                  "checking_seconds": round(time.monotonic()-start, 3),
                  "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}), flush=True)
