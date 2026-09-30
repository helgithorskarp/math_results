"""Removed-zero-edit replay of the complete frozen phase201 binary tree.

Imports no leaf checker, proposal generator, solver or numerical library.
The unchanged base checker is replayed; all new APs, residual petals, loads
and all 78 removed-edit losses are reconstructed here in BOTH actual colors.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path

N, P, C = 3704, 617, 1852
HERE = Path(__file__).parent
BASE_SHA = "2dcfe134ee32ae48daaff08548ae19965a53c6f62fee0b093c8788cf45cd144a"
TREE_SHA = "a1615a81342978109ac85aa9d359a46178f6b42e11fc5abf1df0d7404ba41188"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def premise(directory=HERE):
    need(all(P%d for d in range(2,25)), "Prime617 by complete trial division")
    raw = (directory / "base/phase-201.json").read_bytes()
    need(hashlib.sha256(raw).hexdigest() == BASE_SHA, "Frozen base certificate")
    base = json.loads(raw)
    spec = importlib.util.spec_from_file_location("unchanged_base_checker", directory / "base/verify.py")
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    out = checker.check_case(base)
    need(out["key"] == [201,417,1], "Phase201 base geometry")
    colors = []
    for x in range(N):
        r = (x-C+(201 if x<C else 417))%P
        colors.append(-1 if not r else int(pow(r,308,P)==P-1)^int(x>=C))
    need(colors.count(-1)==6 and colors.count(0)==colors.count(1)==1849, "Partial reference sizes")
    loads = [0]*N
    S = 0
    for a,d,w in base["color0_APs"]:
        for aa in (a,N-1-a-6*d):
            for j in range(7): loads[aa+j*d] += w
        S += w
    D = base["denominator"]
    delta = 196*D-S
    need(delta>=0 and all(0<=v<=D for v in loads), "Nonnegative complete base defects")
    V = [{x for x in range(N) if colors[x]==c and D-loads[x]<=delta} for c in (0,1)]
    K = [{x for x in range(N) if colors[x]==c and loads[x]==0} for c in (0,1)]
    need(all(len(v)==1086 for v in V) and all(len(k)==78 for k in K), "Complete phase201 screen and zero mask")
    need(all(not(V[c]&K[c]) for c in (0,1)), "Removed zeros are outside the residual screen")
    need(V[1]=={N-1-x for x in V[0]} and K[1]=={N-1-x for x in K[0]}, "Reflected domains, no candidate symmetry")
    return colors,V,K,{"base_denominator":D,"base_weight_numerator":S,"screen_defect_numerator":delta,
                       "base_certificate_sha256":BASE_SHA,"checked_base_APs":out["checked_APs"]}


def check_leaf(data, colors, V, K, c, T, X):
    need(type(data) is dict and set(data)=={"format","phase","class_cap","base_certificate_sha256",
         "denominator","color0_APs","color0_cover2","color0_surcharges"}, "Residual leaf schema")
    need(data["format"]=="QR617_UNIFORM_SCREENED_COVER2_1", "Residual leaf format")
    need(type(data["phase"]) is int and data["phase"]==201, "Residual leaf phase")
    need(type(data["class_cap"]) is int and data["class_cap"]==196, "Residual cap196")
    need(data["base_certificate_sha256"]==BASE_SHA, "Residual base dependency")
    D = data["denominator"]
    need(type(D) is int and D>0, "Positive integer denominator")
    need(T<=V and X<=V and not(T&X), "Inherited disjoint states within screen")
    need(all(type(data[k]) is list for k in ("color0_APs","color0_cover2","color0_surcharges")), "Weight lists")
    F = V-T-X
    loads = {x:0 for x in F}
    losses = {z:0 for z in K}
    W,checked = 0,0

    def actual(a,d):
        nonlocal checked
        need(type(a) is int and type(d) is int and d>0 and 0<=a<a+6*d<N, "Actual nonconstant seven-AP")
        aa = a if c==0 else N-1-a-6*d
        A = {aa+j*d for j in range(7)}
        need(all(colors[x]==c for x in A), "Actual original-color AP, no pole")
        checked += 1
        return A

    seen = set()
    for row in data["color0_APs"]:
        need(type(row) is list and len(row)==3 and all(type(x) is int for x in row), "Integer AP row")
        a,d,w = row
        need(w>0 and (a,d) not in seen, "Unique positive AP weight")
        seen.add((a,d))
        A = actual(a,d)
        b = int(not(A&V&T))
        W += b*w
        for x in A&F: loads[x] += w
        for z in A&K: losses[z] += b*w
    seen = set()
    for row in data["color0_cover2"]:
        need(type(row) is list and len(row)==2, "Triple row schema")
        triple,w = row
        need(type(triple) is list and len(triple)==3 and type(w) is int and w>0, "Positive triple")
        need(all(type(ap) is list and len(ap)==2 and all(type(x) is int for x in ap) for ap in triple), "Actual triple coordinates")
        key = tuple(sorted(tuple(ap) for ap in triple))
        need(len(set(key))==3 and key not in seen, "Distinct APs and unique triple")
        seen.add(key)
        As = [actual(a,d) for a,d in triple]
        ps = [A&V for A in As]
        need(all(ps) and not set.intersection(*ps), "Screened triple requires two edits")
        U = set.union(*ps)
        b = max(0,2-len(U&T))
        W += b*w
        for x in U&F: loads[x] += w
        for z in K:
            count = sum(z in A for A in As)
            ell = 2 if count==3 else int(count>0)
            losses[z] += min(b,ell)*w
    sur,nu = {},0
    for row in data["color0_surcharges"]:
        need(type(row) is list and len(row)==2 and all(type(x) is int for x in row), "Integer surcharge row")
        x,w = row
        x = x if c==0 else N-1-x
        need(x in F and x not in sur and w>0, "Unique positive free-point surcharge")
        sur[x]=w; nu+=w
    need(all(loads[x]<=D+sur.get(x,0) for x in F), "Exact capacity at EVERY free screen point")
    worst = max(losses.values())
    old_gap = W-nu-(196-len(T))*D
    gap = old_gap-worst
    need(gap>0, "Strict contradiction for EVERY removed zero edit")
    return {"original_class":c,"forced":sorted(T),"forbidden":sorted(X),"free_screen_size":len(F),
            "denominator":D,"weighted_numerator":W,"penalty_numerator":nu,"old_gap_numerator":old_gap,
            "worst_removed_loss_numerator":worst,"worst_removed_loss_positions":sorted(z for z in K if losses[z]==worst),
            "strict_gap_numerator":gap,"strict_gap":str(Fraction(gap,D)),"removed_positions_checked":len(K),
            "positive_AP_weights":len(data["color0_APs"]),"positive_triple_weights":len(data["color0_cover2"]),
            "checked_actual_APs":checked,"loss_profile":[[z,losses[z]] for z in sorted(K)]}


def check_tree(data, colors, V, K):
    need(type(data) is dict and set(data)=={"format","phase","class_cap","base_certificate_sha256","tree"}, "Complete tree schema")
    need(data["format"]=="QR617_CLASS196_BINARY_COVER_1", "Complete tree format")
    need(type(data["phase"]) is int and data["phase"]==201, "Tree phase")
    need(type(data["class_cap"]) is int and data["class_cap"]==196, "Tree residual cap")
    need(data["base_certificate_sha256"]==BASE_SHA, "Tree base dependency")
    results = []
    def walk(node,T,X,path):
        need(type(node) is dict, "Tree node")
        if set(node)=={"leaf"}:
            pair = []
            for c in (0,1):
                tc = T if c==0 else {N-1-x for x in T}
                xc = X if c==0 else {N-1-x for x in X}
                pair.append(check_leaf(node["leaf"],colors,V[c],K[c],c,tc,xc))
            results.append({"path":path,"colors":pair})
            return
        need(set(node)=={"split","unchanged","edited"}, "Both binary children mandatory, no hidden assumption")
        x=node["split"]
        need(type(x) is int and x in V[0]-T-X, "Fresh split point in full screen")
        need(len(T)+len(X)<127, "Bounded complete tree")
        walk(node["unchanged"],T,X|{x},path+["unchanged"])
        walk(node["edited"],T|{x},X,path+["edited"])
    walk(data["tree"],set(),set(),[])
    return results


def check_all(directory=HERE):
    colors,V,K,base = premise(directory)
    raw = (directory/"tree.json").read_bytes()
    need(hashlib.sha256(raw).hexdigest()==TREE_SHA, "Frozen complete phase201 tree bytes")
    results = check_tree(json.loads(raw),colors,V,K)
    need(len(results)==2, "Both leaves of the phase201 cover")
    return {"agent":"six-vdw-3","role":"researcher","status":"EXACT_PHASE201_ZERO_EDIT_RIGIDITY",
            "phase":201,"key":[201,417,1],"conditional_original_class_cap":197,
            "other_original_class_unrestricted":True,"fixed_positions_per_class":78,
            "fixed_color0_positions":sorted(K[0]),"fixed_color1_positions":sorted(K[1]),
            "screen_size_per_class":1086,"leaf_results":results,**base,
            "tree_certificate_sha256":TREE_SHA,"candidate_symmetry_assumed":False,
            "pole_colors_free":True,"solver_trusted":False,"new_W_bound":False}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--directory",type=Path,default=HERE)
    p.add_argument("--output",type=Path)
    p.add_argument("--expected",type=Path)
    a=p.parse_args();result=check_all(a.directory)
    if a.expected: need(result==json.loads(a.expected.read_text()), "Expected exact zero-load result")
    if a.output: a.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("leaf_results","fixed_color0_positions","fixed_color1_positions")}))


if __name__=="__main__": main()
