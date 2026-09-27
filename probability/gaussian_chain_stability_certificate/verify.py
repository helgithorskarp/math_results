"""Verify a chain-family record without importing the producer.

Squared-distance production is checked through Gram losses and an
endpoint trace-variance telescope. The written analytic bridge is not formalized.
"""
import argparse
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def need(ok, label):
    if not ok:
        raise ValueError(label)


def rat(x):
    need(type(x) in (int,str), "exact rational encoding")
    return F(x)


def nat(x, minimum=0):
    need(type(x) is int and x >= minimum, "integer domain")
    return x


def vec(x):
    need(type(x) is list and len(x) == 3, "vector shape")
    return tuple(map(rat,x))


def inner(x,y):
    return sum(a*b for a,b in zip(x,y))


def diff(x,y):
    return tuple(a-b for a,b in zip(x,y))


def encode(x):
    if isinstance(x,F):
        return str(x)
    if isinstance(x,(tuple,list)):
        return [encode(t) for t in x]
    if isinstance(x,dict):
        return {k:encode(t) for k,t in x.items()}
    return x


def dyadic_fits(b,x):
    """Test 2^-b <= x without a shift proportional to a huge supplied b."""
    need(x > 0, "positive dyadic comparison")
    t = max(0,x.denominator.bit_length()-x.numerator.bit_length())
    if F(1,1 << t) > x:
        t += 1
    return b >= t


def affine_rank(rows):
    # Scatter Gram matrix: exact PSD rank via principal minors, not row reduction.
    x=[diff(row,rows[0]) for row in rows]
    g=[[sum(row[i]*row[j] for row in x) for j in range(3)] for i in range(3)]
    det=sum((1 if p in ((0,1,2),(1,2,0),(2,0,1)) else -1)
            *g[0][p[0]]*g[1][p[1]]*g[2][p[2]] for p in itertools.permutations(range(3)))
    if det:
        return 3
    if any(g[i][i]*g[j][j]-g[i][j]**2 for i,j in itertools.combinations(range(3),2)):
        return 2
    return 1 if sum(g[i][i] for i in range(3)) else 0


def check(data,cert):
    need(data["schema"] == "chain-cloud-family-input-v1", "input schema")
    need(cert["schema"] == "chain-cloud-family-certificate-v1", "certificate schema")
    need(cert["status"] == "CERTIFIED_UNIFORM_ALL_THRESHOLD_CHAIN_FAMILY", "status")
    stages = [[vec(x) for x in rows] for rows in data["stages"]]
    need(len(stages) >= 2 and len(stages[0]) >= 2, "chain shape")
    n,L = len(stages[0]),len(stages)-1
    need(all(len(rows) == n for rows in stages), "label continuity")
    guards=data["step_guards"]
    need(len(guards) == L,"step guard count")
    R,Re,ell = nat(data["comparison_radius"],1),nat(data["endpoint_radius"],1),nat(data["mass_exponent"])
    S = rat(data["variance_ratio"])
    need(S >= 1 and n <= (1 << ell), "variance or empty prior domain")
    need(cert["labels"] == n and cert["steps"] == L and cert["pairs_per_step"] == n*(n-1)//2,
         "chain dimensions")
    need(len(cert["step_records"]) == L, "step record count")
    step_sums=[]
    for t in range(L):
        p,q=stages[t:t+2]
        kind=guards[t]["kind"]
        need(kind in ("norm","straight","orthogonal_lift"),"unknown step guard")
        ranks=None
        if kind == "norm":
            anchors=list(map(vec,guards[t]["anchors"]))
            need(len(anchors) == 2,"link anchor shape")
            p,q=[[diff(x,a) for x in rows] for rows,a in zip((p,q),anchors)]
            for x,y in zip(p,q):
                need(inner(x,x) == inner(y,y) <= R*R, "step anchor/radius")
        if kind == "orthogonal_lift":
            ranks=[affine_rank(p),affine_rank(q)]
            need(sum(ranks) <= 5,"lift dimension")
        gp=[[inner(x,y) for y in p] for x in p]
        gq=[[inner(x,y) for y in q] for x in q]
        gram_losses=[gp[i][i]+gp[j][j]-2*gp[i][j]-gq[i][i]-gq[j][j]+2*gq[i][j]
                     for i,j in itertools.combinations(range(n),2)]
        need(all(d >= 0 for d in gram_losses), "step pair expands")
        if kind == "straight":
            for i,j in itertools.combinations(range(n),2):
                v=diff(q[i],q[j])
                need(inner(v,v) <= inner(v,diff(p[i],p[j])),"straight endpoint derivative")
        # An independent aggregate identity, valid without anchor cancellation.
        sx,sy = [tuple(sum(x[k] for x in rows) for k in range(3)) for rows in (p,q)]
        total=n*sum(inner(x,x)-inner(y,y) for x,y in zip(p,q))+inner(sy,sy)-inner(sx,sx)
        need(total == sum(gram_losses), "Gram loss normalization")
        step_sums.append(total)
        row=cert["step_records"][t]
        need(row["kind"] == kind and row["affine_ranks"] == ranks
             and rat(row["unordered_loss_sum"]) == total
             and row["strict_pairs"] == sum(d > 0 for d in gram_losses), "step loss record")

    def unordered_distance_sum(rows):
        moment=tuple(sum(x[k] for x in rows) for k in range(3))
        return n*sum(inner(x,x) for x in rows)-inner(moment,moment)
    total=unordered_distance_sum(stages[0])-unordered_distance_sum(stages[-1])
    need(total == sum(step_sums) == rat(cert["accumulated_unordered_loss_sum"]), "loss telescope")
    floor=rat(cert["uniform_ordered_loss_floor"])
    need(0 < floor <= 2*total/F(1 << (2*ell)), "positive ordered loss floor")
    a=nat(cert["normalized_loss_exponent"])
    need(dyadic_fits(a,floor/S), "variance-normalized loss")

    centers=list(map(vec,data["endpoint_centers"]))
    need(len(centers) == 2, "endpoint centers")
    p,q = [[diff(x,c) for x in rows] for rows,c in zip((stages[0],stages[-1]),centers)]
    need(all(inner(x,x) <= Re*Re for x in p+q), "endpoint radius")
    need(all(inner(x,x) <= R*R for x in p),"initial comparison radius")
    wc,wr=data["width_witness"],cert["width"]
    need(wc["kind"] == "nested-hulls-rational-cap-v1", "width kind")
    bary=[[rat(x) for x in row] for row in wc["target_in_source_hull"]]
    need(len(bary) == n, "hull row count")
    for row,y in zip(bary,q):
        need(len(row) == n and min(row) >= 0 and sum(row) == 1, "hull simplex")
        need(all(sum(row[i]*(p[i][k]-y[k]) for i in range(n)) == 0 for k in range(3)), "hull residual")
    axis=vec(wc["cap_axis"])
    c,r=rat(wc["cap_cosine"]),rat(wc["cap_sine_upper"])
    star=nat(wc["source_witness"])
    nat(wc.get("perpendicular_bits",16))
    need(star < n and inner(axis,axis) == 1 and 0 <= c < 1 and r >= 0 and r*r+c*c >= 1,
         "cap domain")
    bounds=list(map(rat,wr["perpendicular_upper"]))
    gamma,w=rat(wr["cap_gap_lower"]),rat(wr["lower"])
    need(len(bounds) == n and min(bounds) >= 0 and gamma > 0
         and 0 < w <= min(F(2*Re),(1-c)*gamma/2), "width lower bound")
    for y,b in zip(q,bounds):
        z=diff(p[star],y)
        axial=inner(axis,z)
        transverse=tuple(z[k]-axial*axis[k] for k in range(3))
        need(axial >= 0 and inner(transverse,transverse) <= b*b, "cap transverse bound")
        need(c*axial-r*b >= gamma, "cap gap")

    obstruction=None
    if "endpoint_anchor_obstruction" in data:
        lam=list(map(rat,data["endpoint_anchor_obstruction"]))
        need(len(lam) == n, "anchor dual shape")
        # A dual left-kernel witness for the seven unknown linear coefficients.
        rows=[(F(1),)+p[i]+q[i] for i in range(n)]
        need(all(sum(lam[i]*rows[i][k] for i in range(n)) == 0 for k in range(7)), "anchor dual kernel")
        residual=sum(lam[i]*sum((p[i][k]-q[i][k])*(p[i][k]+q[i][k])
                               for k in range(3)) for i in range(n))
        need(residual != 0, "anchor dual residual")
        obstruction={"squared_norm_residual":str(residual),"endpoint_anchors_exist":False}
    need(cert["endpoint_anchor_obstruction"] == obstruction, "anchor obstruction record")

    z=cert["schedule"]
    A,Q=rat(z["tail_A"]),rat(z["tail_Q"])
    j,k,N,M,bw,B=[nat(z[key]) for key in ("j","k","N","M","width_exponent","budget_exponent")]
    need(A >= 6*(Re+1)**2+2*S*(ell+1) and Q >= 8*A/w, "signed tail schedule")
    need(j >= Q*Q, "tail-middle overlap")
    need(k >= a+9*R*R+4, "endpoint peak guard")
    nN=40*R*R+9*R+38+3*j+8*(k+1)
    nM=66*R*R+2*R+18+4*j+5*(k+1)
    need(N >= max(nN,nM)+k+2*R*R+2*R+1,"imported mixed-chain margin")
    need(M >= a+N,"total ordered loss factor")
    need(dyadic_fits(bw,w/2), "width reserve")
    need(B >= max(M+1,k,ell+1,1,bw), "all-threshold budget")
    conclusion={
        "variance_interval":["1",str(S)],"threshold_interval":"[0,infinity)",
        "prior_region":"v_i >= 2^-mass_exponent; sum v_i=1",
        "error_guard":"2*cloud_radius + l1(u-v) + l1(z-v) <= 2^-budget_exponent",
        "middle_band":"[C_s*2^-j, actual_source_peak]","middle_gap_exponent":M+1,
        "endpoint_anchor_required":False,"actual_contraction_required":False,
        "diffuse_clouds_allowed":True,"minimum_step_loss_required":False,
        "independent_review":"PENDING",
    }
    need(cert["conclusion"] == conclusion,"conclusion overreach")
    diameters=[max(inner(diff(x,y),diff(x,y)) for x in rows for y in rows) for rows in (p,q)]
    return encode({"labels":n,"steps":L,"comparison_radius":R,"endpoint_radius":Re,
                   "accumulated_unordered_loss_sum":total,"uniform_ordered_loss_floor":floor,
                   "width_lower":w,"budget_exponent":B,"variance_interval":[F(1),S],
                   "endpoint_anchor_obstruction":obstruction,
                   "endpoint_diameters_squared":diameters,
                   "same_reference_strict_homothety_buffer_excluded":diameters[0] == diameters[1] > 0})


def dependency_checks():
    pins=json.loads((HERE/"DEPENDENCIES.json").read_text())
    for pin in pins:
        need(hashlib.sha256((HERE/pin["path"]).read_bytes()).hexdigest() == pin["sha256"],
             "dependency changed: "+pin["path"])
    return len(pins)


def damage(data,cert,label,change,which="record"):
    d,c=copy.deepcopy(data),copy.deepcopy(cert)
    change(c if which == "record" else d)
    try:
        check(d,c)
    except (ValueError,KeyError,TypeError,ZeroDivisionError,IndexError):
        return label
    raise ValueError("damaged certificate accepted: "+label)


def generated(data):
    with tempfile.TemporaryDirectory(prefix="gaussian-chain-") as t:
        path=Path(t)/"input.json"
        path.write_text(json.dumps(data))
        return json.loads(subprocess.check_output([sys.executable,"-B",str(HERE/"certificate.py"),str(path)]))


def refined_two_label_chain(L):
    radii=[F(2)-F(j,L) for j in range(L+1)]
    guards=[]
    for j,(r,s) in enumerate(zip(radii,radii[1:])):
        guards.append({"kind":"norm","anchors":[[(r+s)/2,0,0],[(r+s)/2,0,0]]}
                      if j % 3 == 0 else {"kind":"straight" if j % 3 == 1 else "orthogonal_lift"})
    return encode({
        "schema":"chain-cloud-family-input-v1",
        "stages":[[[0,0,0],[r,0,0]] for r in radii],
        "step_guards":guards,
        "comparison_radius":2,"endpoint_radius":2,"endpoint_centers":[[0,0,0],[0,0,0]],
        "mass_exponent":2,"variance_ratio":4,
        "width_witness":{"kind":"nested-hulls-rational-cap-v1",
            "target_in_source_hull":[[1,0],[F(1,2),F(1,2)]],
            "cap_axis":[1,0,0],"cap_cosine":"4/5","cap_sine_upper":"3/5","source_witness":1},
    })


def reused_mixed_input():
    """Consume R8's published two-link input; invent no additional geometry."""
    base=json.loads((HERE/"../gaussian_motion_chain_strictness/INPUT.json").read_text())
    p=list(map(vec,base["source"]))
    stages=[base["source"]]+[row["target"] for row in base["stages"]]
    guards=[]
    for row in base["stages"]:
        guards.append({"kind":row["kind"],"anchors":[row["source_anchor"],row["target_anchor"]]}
                      if row["kind"] == "norm" else {"kind":row["kind"]})
    bary=[]
    for q in map(vec,stages[-1]):
        row=[]
        for x in p:
            value=F(1)
            if any(abs(t) != 1 for t in x):
                value=F(0)
            else:
                for k in range(3):
                    value *= (1+x[k]*q[k])/2
            row.append(value)
        bary.append(row)
    return encode({"schema":"chain-cloud-family-input-v1","stages":stages,"step_guards":guards,
        "comparison_radius":2,"endpoint_radius":2,"endpoint_centers":[[0,0,0],[0,0,0]],
        "mass_exponent":5,"variance_ratio":4,
        "width_witness":{"kind":"nested-hulls-rational-cap-v1","target_in_source_hull":bary,
            "cap_axis":[0,0,1],"cap_cosine":"4/5","cap_sine_upper":"3/5",
            "source_witness":p.index((F(0),F(0),F(1))),"perpendicular_bits":4}})


def suite(data,cert):
    family=check(data,cert)
    bad=[]
    for key in ("j","k","N","M","budget_exponent"):
        bad.append(damage(data,cert,"understated_"+key,
            lambda c,key=key:c["schedule"].__setitem__(key,c["schedule"][key]-1)))
    for label,change in [
        ("false_loss_floor",lambda c:c.__setitem__("uniform_ordered_loss_floor","100")),
        ("wrong_loss_telescope",lambda c:c.__setitem__("accumulated_unordered_loss_sum","271")),
        ("wrong_step_loss",lambda c:c["step_records"][0].__setitem__("unordered_loss_sum","45")),
        ("false_width",lambda c:c["width"].__setitem__("lower","1")),
        ("false_transverse_bound",lambda c:c["width"]["perpendicular_upper"].__setitem__(13,"0")),
        ("false_cap_gap",lambda c:c["width"].__setitem__("cap_gap_lower","1")),
        ("false_anchor_residual",lambda c:c["endpoint_anchor_obstruction"].__setitem__("squared_norm_residual","7")),
        ("false_variance_scope",lambda c:c["conclusion"].__setitem__("variance_interval",["0","infinity"])),
    ]:
        bad.append(damage(data,cert,label,change))
    for label,change in [
        ("float_input",lambda d:d["stages"][0][1].__setitem__(0,1.0)),
        ("empty_prior_region",lambda d:d.__setitem__("mass_exponent",3)),
        ("invalid_variance",lambda d:d.__setitem__("variance_ratio","1/2")),
        ("step_anchor_mismatch",lambda d:d["step_guards"][0]["anchors"].__setitem__(1,[0,0,0])),
        ("false_straight_guard",lambda d:d["step_guards"][0].__setitem__("kind","straight")),
        ("six_dimensional_lift",lambda d:d["step_guards"][0].__setitem__("kind","orthogonal_lift")),
        ("expanding_equal_norm_step",lambda d:d["stages"][1].__setitem__(0,[3,0,0])),
        ("missing_label",lambda d:d["stages"][1].pop()),
        ("endpoint_radius_too_small",lambda d:d.__setitem__("endpoint_radius",2)),
        ("incorrect_hull",lambda d:d["width_witness"]["target_in_source_hull"].__setitem__(3,[0,0,0,1]+[0]*11)),
        ("nonunit_cap",lambda d:d["width_witness"].__setitem__("cap_axis",[2,0,0])),
        ("incorrect_cap_sine",lambda d:d["width_witness"].__setitem__("cap_sine_upper","0")),
        ("false_anchor_dual",lambda d:d["endpoint_anchor_obstruction"].__setitem__(1,0)),
        ("zero_chain_loss",lambda d:d.__setitem__("stages",[copy.deepcopy(d["stages"][0]) for _ in d["stages"]])),
    ]:
        bad.append(damage(data,cert,label,change,"input"))

    stages=[[vec(x) for x in rows] for rows in data["stages"]]
    n,m=len(stages[0]),F(1,1 << data["mass_exponent"])
    priors=[[m+(1-n*m if i == j else 0) for i in range(n)] for j in range(n)]+[[F(1,n)]*n]
    cov=[]
    for v in priors:
        def variance(rows):
            mean=tuple(sum(v[i]*rows[i][k] for i in range(n)) for k in range(3))
            return sum(v[i]*inner(rows[i],rows[i]) for i in range(n))-inner(mean,mean)
        step=[2*(variance(x)-variance(y)) for x,y in zip(stages,stages[1:])]
        direct=2*(variance(stages[0])-variance(stages[-1]))
        need(sum(step) == direct >= rat(cert["uniform_ordered_loss_floor"]),"weighted loss telescope")
        cov.append(str(direct))

    refined=[]
    schedules=[]
    for L in [1,2,7,31,257]:
        d=refined_two_label_chain(L);c=generated(d);checked=check(d,c)
        schedules.append(c["schedule"])
        refined.append({"steps":L,"minimum_step_unordered_loss":
                        str(min(rat(r["unordered_loss_sum"]) for r in c["step_records"])),
                        "uniform_ordered_loss_floor":checked["uniform_ordered_loss_floor"],
                        "budget_exponent":checked["budget_exponent"]})
    need(all(z == schedules[0] for z in schedules),"refinement changed global schedule")
    d=copy.deepcopy(data)
    d["stages"].insert(0,copy.deepcopy(d["stages"][0]))
    d["step_guards"].insert(0,{"kind":"norm","anchors":[[0,0,0],[0,0,0]]})
    c=generated(d);check(d,c)
    need(c["schedule"] == cert["schedule"],"zero-loss insertion changed budget")

    # Independent translation at every stage, with both adjacent anchor pairs updated.
    shifts=[(F(j+1,3),F(-j,7),F(2*j+1,11)) for j in range(len(stages))]
    translated=copy.deepcopy(data)
    translated["stages"]=encode([[tuple(x[k]+shifts[j][k] for k in range(3))
                                  for x in rows] for j,rows in enumerate(stages)])
    for j,guard in enumerate(data["step_guards"]):
        if guard["kind"] == "norm":
            translated["step_guards"][j]["anchors"]=encode([
                tuple(rat(guard["anchors"][e][k])+shifts[j+e][k] for k in range(3)) for e in (0,1)])
    translated["endpoint_centers"]=encode([tuple(rat(data["endpoint_centers"][e][k])+shifts[j][k]
                                                  for k in range(3)) for e,j in ((0,0),(1,len(stages)-1))])
    need(check(translated,cert) == family,"independent stage translations")

    d=reused_mixed_input();c=generated(d)
    mixed=check(d,c)
    mixed["step_records"]=c["step_records"]
    need([r["kind"] for r in c["step_records"]] == ["norm","orthogonal_lift"],"reused R8 chain changed")

    output=subprocess.check_output([sys.executable,"-B",str(HERE/"certificate.py"),str(HERE/"INPUT.json")])
    need(json.loads(output) == cert and output == (HERE/"CERTIFICATE.json").read_bytes(),"canonical producer record")
    return {"status":"CHAIN_FAMILY_EXACT_CONTROLS_PASS","family":family,
            "certificate_sha256":hashlib.sha256(output).hexdigest(),"dependency_pins":dependency_checks(),
            "negative_controls":bad,"covariance_prior_controls":cov,"refinement_controls":refined,
            "zero_loss_step_insertion":"PASS","independent_stage_translations":"PASS",
            "reused_R8_mixed_family":mixed,
            "integer_inequality_checker_imports_producer":False,
            "dyadic_budget_denominator_materialized":False,
            "trust_boundary":"Imported mixed-chain margin and written all-threshold join; author checks, not independent review."}


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path)
    parser.add_argument("--certificate",type=Path)
    args=parser.parse_args()
    need((args.input is None) == (args.certificate is None),"supply both input and certificate")
    ip=args.input if args.input is not None else HERE/"INPUT.json"
    cp=args.certificate if args.certificate is not None else HERE/"CERTIFICATE.json"
    data,cert=json.loads(ip.read_text()),json.loads(cp.read_text())
    result=({"status":"UNIFORM_CHAIN_FAMILY_CERTIFICATE_VERIFIED","family":check(data,cert),
             "dependency_pins":dependency_checks()} if args.input is not None else suite(data,cert))
    print(json.dumps(result,sort_keys=True,indent=2))
