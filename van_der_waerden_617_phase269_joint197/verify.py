"""Exact four-root exclusion of the phase269 original-class197/197 box.

Checks actual integer APs, Euler colors, activated six-point petals, complete
anchor cover and integer loads. Imports the unchanged earlier low-load
checker only; imports no proposal generator, solver or numerical package.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path

N, P, C = 3704, 617, 1852
HERE = Path(__file__).parent
LOW_SHA = "8fa71e15ec099961f1074beccb4bb7447c363f5a237784208d4c9dc0c3ac4bce"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def premise(directory=HERE):
    need(all(P%d for d in range(2,25)), "Prime617 by complete trial division through its square root")
    raw = (directory / "low/certificate.json").read_bytes()
    need(hashlib.sha256(raw).hexdigest() == LOW_SHA, "Frozen low-load certificate bytes")
    spec = importlib.util.spec_from_file_location("low_load_exact", directory / "low/verify.py")
    low = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(low)
    checked = low.check(json.loads(raw), directory / "low/base/phase-269.json", directory / "low/base/verify.py")
    need(checked["conditional_class_cap"] == 197 and checked["threshold_numerator"] == 65000,
         "Replayed phase269 class197 low-load premise")
    need(checked["forbidden_positions_per_class"] == 107, "Complete107-position premise")
    # Separately reconstruct the original reference colors by Euler's criterion.
    colors = []
    for x in range(N):
        r = (x-C+(269 if x<C else 349)) % P
        colors.append(-1 if r == 0 else int(pow(r,(P-1)//2,P) == P-1)^int(x>=C))
    need(colors.count(-1)==6 and colors.count(0)==colors.count(1)==1849,
         "Six free poles and1849 points in each original reference class")
    K = [set(checked[f"forbidden_low_load_edit_positions_color{c}"]) for c in (0,1)]
    need(all(colors[x] == c for c in (0,1) for x in K[c]), "Premise reference colors agree")
    return colors, K, checked


def check_root(data, colors, K):
    need(type(data) is dict and set(data) == {"format","phase","root","caps","denominator",
         "low_certificate_sha256","AP_weights","cover2_weights","surcharges"}, "Root schema")
    need(data["format"] == "QR617_PHASE269_JOINT197_ROOT_1", "Root format")
    need(type(data["phase"]) is int and data["phase"] == 269, "Phase269")
    need(type(data["caps"]) is list and all(type(x) is int for x in data["caps"]) and data["caps"] == [197,197], "Original caps197/197")
    need(data["low_certificate_sha256"] == LOW_SHA, "Root low-load dependency")
    v, D = data["root"], data["denominator"]
    need(type(v) is int and 0<=v<N and colors[v] == 0 and v not in K[0], "Allowed original-color0 trial edit")
    need(type(D) is int and D>0, "Positive integer denominator")
    need(all(type(data[k]) is list for k in ("AP_weights","cover2_weights","surcharges")), "Weight lists")
    vertices = {x for x in range(N) if colors[x] == 1 and x not in K[1]}
    loads, W, checked_APs, activated_rows = {x:0 for x in vertices}, 0, 0, 0

    def petal(a, d, allow_activated=True):
        nonlocal checked_APs, activated_rows
        need(type(a) is int and type(d) is int and d>0 and 0<=a<a+6*d<N, "Nonconstant actual seven-AP")
        points = {a+j*d for j in range(7)}
        mono = all(colors[x] == 1 for x in points)
        activated = v in points and colors[v] == 0 and all(colors[x] == 1 for x in points-{v})
        need(mono or (allow_activated and activated), "Original-color1 or exactly root-activated AP")
        checked_APs += 1
        activated_rows += int(activated)
        return points & vertices

    seen = set()
    for row in data["AP_weights"]:
        need(type(row) is list and len(row)==3 and all(type(x) is int for x in row), "Integer AP weight row")
        a,d,w = row
        need(w>0 and (a,d) not in seen, "Unique positive AP weight")
        seen.add((a,d))
        for x in petal(a,d): loads[x] += w
        W += w
    seen = set()
    for row in data["cover2_weights"]:
        need(type(row) is list and len(row)==2, "Triple row")
        triple,w = row
        need(type(triple) is list and len(triple)==3 and type(w) is int and w>0, "Positive triple weight")
        need(all(type(ap) is list and len(ap)==2 and all(type(x) is int for x in ap) for ap in triple), "Triple actual AP coordinates")
        key = tuple(sorted(tuple(ap) for ap in triple))
        need(len(set(key)) == 3 and key not in seen, "Unique triple with distinct APs")
        seen.add(key)
        ps = [petal(a,d,allow_activated=False) for a,d in triple]
        need(all(ps) and not set.intersection(*ps), "Triple forces two permitted edits")
        for x in set.union(*ps): loads[x] += w
        W += 2*w
    penalties, surcharge = 0, {}
    for row in data["surcharges"]:
        need(type(row) is list and len(row)==2 and all(type(x) is int for x in row), "Integer surcharge")
        x,num = row
        need(x in vertices and x not in surcharge and num>0, "Unique positive permitted-point surcharge")
        surcharge[x] = num
        penalties += num
    need(all(loads[x] <= D+surcharge.get(x,0) for x in vertices), "Complete exact permitted-point capacity")
    gap = W-penalties-197*D
    need(gap>0, "Strict opposite-class197 contradiction")
    return {"root":v,"opposite_original_class":1,"opposite_edit_cap":197,
            "denominator":D,"weighted_numerator":W,"penalty_numerator":penalties,
            "strict_gap_numerator":gap,"strict_gap":str(Fraction(gap,D)),
            "positive_AP_weights":len(data["AP_weights"]),"positive_cover2_weights":len(data["cover2_weights"]),
            "weighted_activated_APs":activated_rows,"checked_actual_APs":checked_APs,
            "permitted_opposite_edit_positions":len(vertices),"solver_trusted":False}


def check_all(directory=HERE, documents=None):
    colors, K, low = premise(directory)
    anchor = {35+j*323 for j in range(7)}
    need(all(colors[x] == 0 for x in anchor), "Actual original-color0 anchor AP")
    roots = anchor-K[0]
    need(roots == {1004,1327,1650,1973}, "Exact four-root anchor cover")
    if documents is None:
        documents = [json.loads((directory / f"roots/{v}.json").read_text()) for v in sorted(roots)]
    need(type(documents) is list and len(documents)==len(roots), "Complete root documents")
    need(all(type(d) is dict and type(d.get("root")) is int for d in documents), "Root document identities")
    need({d["root"] for d in documents} == roots, "All and only four anchor roots")
    results = [check_root(d,colors,K) for d in sorted(documents,key=lambda d:d["root"])]
    return {"agent":"six-vdw-3","role":"researcher","status":"EXACT_PHASE269_JOINT197_EXCLUSION",
            "phase":269,"key":[269,349,1],"excluded_original_class_caps":[197,197],
            "necessary_max_original_class_edits":198,"anchor_AP":[35,323],
            "complementary_necessary_min_original_class_edits_at_most":1651,
            "original_reference_class_sizes":[1849,1849],
            "anchor_points":sorted(anchor),"anchor_fixed_points":sorted(anchor&K[0]),
            "complete_anchor_roots":sorted(roots),"root_results":results,
            "low_load_premise_threshold":65000,"low_load_fixed_positions_per_class":107,
            "low_load_exact_gap":low["strict_gap"],"low_load_certificate_sha256":LOW_SHA,
            "original_class_lower197_used_in_core_proof":False,
            "other_pole_colors_free":True,"candidate_symmetry_assumed":False,
            "solver_trusted":False,"new_W_bound":False,"attainability_claim":False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--directory",type=Path,default=HERE)
    p.add_argument("--output",type=Path)
    p.add_argument("--expected",type=Path)
    args = p.parse_args()
    result = check_all(args.directory)
    if args.expected: need(result == json.loads(args.expected.read_text()), "Expected exact result")
    if args.output: args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
