"""Exact phase201 zero rigidity and root1427 necessary edit screen.

Replays the new complete removed-zero tree premise, then checks actual
Euler-colored APs, full-domain petals, integer loads and the complete derived screen.
Imports no solver or numerical proposal generator.
"""
import argparse
import importlib.util
import json
from pathlib import Path

N,P,C = 3704,617,1852
HERE = Path(__file__).parent
ZERO_TREE_SHA = "a1615a81342978109ac85aa9d359a46178f6b42e11fc5abf1df0d7404ba41188"


def need(ok,message):
    if not ok: raise ValueError(message)


def premise(directory=HERE):
    spec=importlib.util.spec_from_file_location("zero_loss_exact",directory/"zero/verify.py")
    zero=importlib.util.module_from_spec(spec);spec.loader.exec_module(zero)
    out=zero.check_all(directory/"zero")
    colors,_,K,_=zero.premise(directory/"zero")
    need(out["conditional_original_class_cap"]==197 and out["fixed_positions_per_class"]==78,
         "Complete phase201 zero-edit premise")
    need(out["tree_certificate_sha256"]==ZERO_TREE_SHA, "Fixed tree identity")
    return colors,K,out


def check_screen(data, colors, K):
    need(type(data) is dict and set(data) == {"format","phase","root","opposite_class_cap","denominator",
         "zero_tree_sha256","AP_weights","cover2_weights"}, "Root schema")
    need(data["format"] == "QR617_PHASE201_ROOT_SCREEN_1", "Root format")
    need(type(data["phase"]) is int and data["phase"] == 201, "Phase201")
    need(type(data["opposite_class_cap"]) is int and data["opposite_class_cap"] == 197, "Opposite original cap197")
    need(data["zero_tree_sha256"] == ZERO_TREE_SHA, "Root zero-rigidity dependency")
    v, D = data["root"], data["denominator"]
    need(type(v) is int and v==1427 and colors[v]==0, "Original-color0 root1427 trial edit")
    need(type(D) is int and D>0, "Positive integer denominator")
    need(all(type(data[k]) is list for k in ("AP_weights","cover2_weights")), "Weight lists")
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
    need(all(loads[x]<=D for x in vertices), "Exact capacity at ALL permitted opposite-class points")
    delta=197*D-W
    need(0<=delta<D and W>196*D, "Nontrivial necessary cap197 defect screen")
    screen={x for x in vertices if D-loads[x]<=delta}
    need(screen, "Nonempty derived screen")
    return {"root":v,"trial_final_color":1,"opposite_original_class":1,"opposite_edit_cap":197,
            "other_original_class_cap_required":False,"denominator":D,"weighted_numerator":W,
            "screen_defect_numerator":delta,"maximum_position_load_numerator":max(loads.values()),
            "necessary_opposite_class_edit_count":197,"full_permitted_positions":len(vertices),
            "necessary_permitted_screen_size":len(screen),"newly_forbidden_opposite_edit_positions":len(vertices-screen),
            "necessary_permitted_screen":sorted(screen),"positive_AP_weights":len(data["AP_weights"]),
            "positive_cover2_weights":len(data["cover2_weights"]),"weighted_activated_APs":activated_rows,
            "checked_actual_APs":checked_APs,"solver_trusted":False,"nonexistence_claim":False}


def check_all(directory=HERE,document=None):
    colors,K,zero=premise(directory)
    if document is None:document=json.loads((directory/"root1427.json").read_text())
    screen=check_screen(document,colors,K)
    return {"agent":"six-vdw-3","role":"researcher","status":"EXACT_PHASE201_ZERO_RIGIDITY_AND_ROOT_SCREEN",
            "phase":201,"key":[201,417,1],"conditional_original_class_cap":197,
            "zero_fixed_positions_per_class":78,"zero_leaf_gap_numerators":[r["colors"][0]["strict_gap_numerator"] for r in zero["leaf_results"]],
            "zero_tree_certificate_sha256":ZERO_TREE_SHA,"root1427_screen":screen,
            "zero_rigidity_other_class_unrestricted":True,
            "original_reference_class_sizes":[1849,1849],"pole_colors_free":True,
            "candidate_symmetry_assumed":False,"solver_trusted":False,"new_W_bound":False,
            "whole_phase201_197_197_box_excluded":False,"feasibility_claim":False}


def main():
    p=argparse.ArgumentParser();p.add_argument("--directory",type=Path,default=HERE)
    p.add_argument("--output",type=Path);p.add_argument("--expected",type=Path)
    a=p.parse_args();result=check_all(a.directory)
    if a.expected:need(result==json.loads(a.expected.read_text()),"Expected exact source result")
    if a.output:a.output.write_text(json.dumps(result,indent=2)+"\n")
    compact={k:v for k,v in result.items() if k!="root1427_screen"}
    compact["root1427_screen"]={k:v for k,v in result["root1427_screen"].items() if k!="necessary_permitted_screen"}
    print(json.dumps(compact))


if __name__=="__main__":main()
