"""Single-thread fractional proposal for the root1427 necessary edit screen.

The original monochromatic APs force edits. Editing a trial original-color0
point also activates every pole-free AP with that point as its sole color0
term: its six original-color1 terms must contain a class1 edit. No solver
status is accepted as a proof. The fixed zero-load positions are a separately
replayed independently for each original edit class. Only the opposite
class197 cap is used in the root1427 screen lemma.
"""
import argparse
import json
import math
import os
from pathlib import Path
import resource
import time
import hashlib
import verify

HERE = Path(__file__).parent

for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[key] = "1"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=int, choices=(1427,), default=1427)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--summary", type=Path)
    p.add_argument("--plans", type=Path, default=HERE / "plans.json")
    p.add_argument("--state", type=Path)
    args = p.parse_args()
    start = time.monotonic()
    _, _, fixed = verify.premise()
    K = [set(fixed[f"fixed_color{c}_positions"]) for c in (0,1)]
    sq = {r*r%617 for r in range(1,617)}
    colors = []
    for x in range(3704):
        r = (x-1852+(201 if x<1852 else 417))%617
        colors.append(-1 if not r else int(r not in sq)^int(x>=1852))
    if colors[args.root]!=0 or args.root in K[0]:
        raise ValueError("Trial must be an allowed original-color0 edit")
    vertices = [x for x in range(3704) if colors[x]==1 and x not in K[1]]
    index = {x:i for i,x in enumerate(vertices)}
    aps = [(a,d) for d in range(1,618) for a in range(max(0,1852-6*d),min(1852,3704-6*d))
           if all(colors[a+j*d]==1 for j in range(7))]
    activated = []
    for d in range(1,618):
        for j in range(7):
            a = args.root-j*d
            if 0<=a<a+6*d<3704 and all(colors[a+k*d]==1 for k in range(7) if k!=j):
                activated.append((a,d))
    rows = [{index[x] for x in (a+j*d for j in range(7)) if x in index}
            for a,d in aps+activated]
    if any(not row for row in rows):
        out = {"direct_empty_petal":True,"root":args.root,"AP":list((aps+activated)[next(i for i,r in enumerate(rows) if not r)])}
        args.output.write_text(json.dumps(out,indent=2)+"\n")
        print(json.dumps(out));return
    triples = []
    # Reconstruct the existing robust plans in the full permitted edit domain;
    # only bundles still satisfying multiplicity two are valid here.
    plans = json.loads(args.plans.read_text())
    lookup = {(a,d):i for i,(a,d) in enumerate(aps)}
    for t in plans["cover2_triples"]:
        reflected = [(3703-a-6*d,d) for a,d in t]
        if any(ap not in lookup for ap in reflected):
            raise ValueError("Reflected original AP missing")
        ps = [rows[lookup[ap]] for ap in reflected]
        if all(ps) and not set.intersection(*ps):
            triples.append(reflected)
            rows.append(set.union(*ps))
    existing = {tuple(sorted(tuple(ap) for ap in t)) for t in triples}
    for triple in plans.get("opposite_cover2_triples", []):
        key = tuple(sorted(tuple(ap) for ap in triple))
        if key in existing: continue
        if len(key)!=3 or len(set(key))!=3 or any(ap not in lookup for ap in key):
            raise ValueError("Fresh triple must comprise three original opposite-color APs")
        ps = [rows[lookup[ap]] for ap in key]
        if not all(ps) or set.intersection(*ps):
            raise ValueError("Fresh triple not valid in full permitted opposite domain")
        triples.append([list(ap) for ap in key])
        rows.append(set.union(*ps))
        existing.add(key)
    cols = [[] for _ in vertices]
    for i,row in enumerate(rows):
        for j in row:cols[j].append(i)
    starts,indices = [0],[]
    for col in cols:
        indices.extend(col);starts.append(len(indices))
    import highspy as hs
    import numpy as np
    h = hs.Highs()
    options = {"threads":1,"parallel":"off","output_flag":False,"solver":"ipm",
               "run_crossover":"on","time_limit":15.0,"random_seed":0,
               "primal_feasibility_tolerance":1e-9,"dual_feasibility_tolerance":1e-9,"ipm_optimality_tolerance":1e-9}
    for key,value in options.items():
        if h.setOptionValue(key,value)!=hs.HighsStatus.kOk:raise RuntimeError("Solver option")
    lp = hs.HighsLp()
    lp.num_col_,lp.num_row_ = len(vertices),len(rows)
    lp.col_cost_,lp.col_lower_,lp.col_upper_ = np.ones(len(vertices)),np.zeros(len(vertices)),np.ones(len(vertices))
    lp.row_lower_ = np.array([1.0]*(len(aps)+len(activated))+[2.0]*len(triples))
    lp.row_upper_ = np.full(len(rows),hs.kHighsInf)
    lp.a_matrix_.format_ = hs.MatrixFormat.kColwise
    lp.a_matrix_.start_,lp.a_matrix_.index_ = np.array(starts,dtype=np.int32),np.array(indices,dtype=np.int32)
    lp.a_matrix_.value_ = np.ones(len(indices))
    if h.passModel(lp)!=hs.HighsStatus.kOk:raise RuntimeError("Solver model")
    h.run(); sol=h.getSolution()
    if not sol.value_valid or not sol.dual_valid or not all(math.isfinite(w) for w in sol.row_dual):
        raise RuntimeError("Incomplete guide, no exclusion")
    if args.state:
        args.state.write_text(json.dumps({"APs":aps,"petals":[sorted(row) for row in rows[:len(aps)]],
                                         "point_values":list(sol.col_value),"existing_triples":triples},
                                        separators=(",",":"))+"\n")
    D=1_000_000; nums=[max(0,math.floor(w*D)) for w in sol.row_dual]
    load=[0]*len(vertices)
    for row,w in zip(rows,nums):
        for x in row:load[x]+=w
    W=sum(nums[:len(aps)+len(activated)])+2*sum(nums[len(aps)+len(activated):])
    nu=sum(max(0,w-D) for w in load)
    out={"agent":"six-vdw-3","role":"researcher","root":args.root,
         "opposite_original_class_cap":197,"other_original_class_cap_required":False,
         "fixed_zero_points":fixed['fixed_positions_per_class'],
         "opposite_class_vertices":len(vertices),"original_mono_APs":len(aps),"activated_six_term_petals":len(activated),
         "valid_actual_triples":len(triples),"floating_objective":h.getObjectiveValue(),
         "candidate_weight_numerator":W,"candidate_vertex_penalty_numerator":nu,
         "denominator":D,"candidate_gap_to_exclusion_numerator":W-nu-197*D,
         "solver_status":h.modelStatusToString(h.getModelStatus()),"options":options,
         "seconds":time.monotonic()-start,"peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         "guide_only_requires_independent_exact_replay":True,"nonpositive_gap_is_not_a_valid_branch":True,
         "AP_weights":[[a,d,w] for (a,d),w in zip(aps+activated,nums) if w],
         "triple_weights":[[t,w] for t,w in zip(triples,nums[len(aps)+len(activated):]) if w],
         "surcharges":[[x,w-D] for x,w in zip(vertices,load) if w>D]}
    cert = {"format":"QR617_PHASE201_ROOT_SCREEN_1","phase":201,"root":args.root,
            "opposite_class_cap":197,"denominator":D,"zero_tree_sha256":verify.ZERO_TREE_SHA,
            "AP_weights":out.pop("AP_weights"),"cover2_weights":out.pop("triple_weights"),
            }
    if out.pop("surcharges"):raise RuntimeError("Screen certificate needs exact capacities without surcharges")
    encoded = (json.dumps(cert,sort_keys=True,separators=(",",":"))+"\n").encode()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes(encoded)
    out["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    if args.summary: args.summary.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out),flush=True)


if __name__=="__main__":
    main()
