"""Data-only late fixture bridge and compact independent replay."""
from independent import *

def canonical_hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def fixture_check(model, path):
    c=unique_json(path);raw=tuple(ints(p,2) for p in c["raw_cells"])
    require(len(set(raw))==len(raw)==64 and set(raw)<=set(model["u"]), "64-cell candidate in U")
    lo=min(x for x,y in raw),min(y for x,y in raw)
    f=c["fixture"];q=tuple(ints(p,2) for p in f["cells"])
    require(tuple(sorted((x-lo[0],y-lo[1]) for x,y in raw))==q,"entire source-origin bridge")
    require([len(x) for x in f["levels"]]==[1,6],"fixture level partition")
    oo=orientations(q);claimed=[]
    for level in f["levels"]:
        for pose in level:
            o,x,y=ints(pose,3);require(0<=o<8,"fixture orientation")
            _,m,b=oo[o];t=x-b[0],y-b[1]
            claimed.append({cell(m,t,p) for p in q})
    expected=[{(cell(m,t,p)[0]-lo[0],cell(m,t,p)[1]-lo[1]) for p in raw}
              for m,t in model["maps"][:7]]
    require(claimed==expected,"ALL seven full footprint equalities")
    footprints,unions=physical(model,set(raw),depth=1)
    root=footprints[0]
    for fp in footprints[1:]:
        require(bool(fp&halo(root)),"every first copy contacts root")
    boundaries=[boundary(set(raw))]+[boundary(p) for p in unions]
    a=assignment(model,set(raw),True)
    first=clean(model["groups"]["packing"]+model["groups"]["halo0"]+
                model["groups"]["nonempty"]+model["groups"]["failure"])
    # Full packing includes second copies and is not a first-only premise.
    first_pack=[]
    for i,j in combinations(range(7),2):
        for p in model["u"]:
            v=model["images"][i][p]
            for q0 in model["u"]:
                if model["images"][j][q0]==v:
                    first_pack.append((-(model["u"].index(p)+1),-(model["u"].index(q0)+1)))
    first=clean(first_pack+model["groups"]["halo0"]+
                model["groups"]["nonempty"]+model["groups"]["failure"])
    require(evaluate(first,a),"literal entire first-only countermodel")
    bad=[{"key":list(k),"count":sum(n*a[x] for x,n in model["coefficients"][k].items())}
         for k in model["order"] if sum(n*a[x] for x,n in model["coefficients"][k].items())!=1]
    require(len(bad)==8 and sum(p["count"] for p in bad)!=8,"eight non-unit period rows")
    return {"area":64,"shift":list(lo),"whole_footprint_equalities":7,
            "prefix_areas":[len(x) for x in unions],"boundary_edges":boundaries,"bad_rows":bad}

def replay(base=BASE):
    model=build(base/"input.json",base/"tiling.json")
    record=build_record(model);proof=read_rup(base/"proof.rup",643)
    checked=verify_rup(model["formula"],proof)
    support=unique_json(base/"geometric-support.json")
    require(isinstance(support,list),"support list")
    support=[tuple(ints(c,len(c))) for c in support]
    require(support==clean(support) and all(all(1<=abs(x)<=123 for x in c) for c in support),
            "complete canonical geometric support")
    physical_base=clean([c for g in ["packing","halo0","halo1"] for c in model["groups"][g]])
    require(set(support)<=set(physical_base),"every weakened constraint is an original physical implication")
    reduced=clean(support+model["groups"]["nonempty"]+model["groups"]["failure"])
    trimmed=read_rup(base/"support.rup",643);verify_rup(reduced,trimmed)
    # Independent record need not trust the supplied reduced support construction.
    result={"agent":"six-reviewer-1","role":"independent mathematical reviewer","source_sites":123,
            "variables":643,"whole_original_clauses":len(model["formula"]),
            "canonical_formula_sha256":record["formula_sha256"],"whole_formula":True,
            "groups":record["group_clauses"],"raw_physical_obligations":record["raw_obligations"],
            "all_prefix_areas":record["prefix_areas"],"all_prefix_boundary_edges":record["prefix_boundaries"],
            "all_quotient_coefficients_sha256":canonical_hash(record["all_quotient_rows"]),
            "all_quotient_terms":sum(len(r) for r in model["coefficients"].values()),
            "all_multiplicities":{str(k):v for k,v in record["multiplicities"].items()},"exact_local_control_rows":record["local_exact_control_rows"],
            "full_rup_additions":len(proof),"full_proof_sha256":hashlib.sha256((base/"proof.rup").read_bytes()).hexdigest(),
            "each_RUP_record_sha256":canonical_hash(checked),
            "strict_weaker_physical_constraints":len(support),"original_unique_physical_constraints":len(physical_base),
            "weaker_full_formula_clauses":len(reduced),"weaker_rup_additions":len(trimmed),
            "geometric_support_sha256":hashlib.sha256((base/"geometric-support.json").read_bytes()).hexdigest(),
            "weaker_proof_sha256":hashlib.sha256((base/"support.rup").read_bytes()).hexdigest(),
            "weaker_condition_proved":True,"support_not_claimed_minimum":True,
            "first_only_counterexample":fixture_check(model,base/"counterexample.json")}
    expected=base/"expected.json"
    if expected.exists():require(result==unique_json(expected),"whole independent record differs")
    return result

if __name__=="__main__":
    print(json.dumps(replay(),sort_keys=True,indent=2))
