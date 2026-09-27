"""Verify the protected-core/Wasserstein record without importing its producer.

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
    need(data["schema"] == "core-wasserstein-family-input-v1", "input schema")
    need(cert["schema"] == "core-wasserstein-family-certificate-v1", "certificate schema")
    need(cert["status"] == "CERTIFIED_CORE_WASSERSTEIN_ALL_THRESHOLD_FAMILY", "status")
    stages = [[vec(x) for x in rows] for rows in data["core_stages"]]
    need(len(stages) >= 2 and len(stages[0]) >= 2, "chain shape")
    nc,L = len(stages[0]),len(stages)-1
    need(all(len(rows) == nc for rows in stages), "core label continuity")
    background=list(map(vec,data["background_vertices"]))
    need(len(background) > 0,"nonempty background polytope")
    stages=[rows+background for rows in stages]
    n=nc+len(background)
    guards=data["step_guards"]
    need(len(guards) == L,"step guard count")
    R,Re,ell = nat(data["comparison_radius"],1),nat(data["endpoint_radius"],1),nat(data["mass_exponent"])
    S = rat(data["variance_ratio"])
    need(S >= 1 and nc <= (1 << ell), "variance or empty prior domain")
    need(cert["core_labels"] == nc and cert["background_vertices"] == len(background)
         and cert["geometry_labels"] == n and cert["steps"] == L and cert["pairs_per_step"] == n*(n-1)//2,
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
        core_total=nc*sum(inner(x,x)-inner(y,y) for x,y in zip(p[:nc],q[:nc]))
        csx,csy=[tuple(sum(x[k] for x in rows[:nc]) for k in range(3)) for rows in (p,q)]
        core_total+=inner(csy,csy)-inner(csx,csx)
        step_sums.append(core_total)
        row=cert["step_records"][t]
        need(row["kind"] == kind and row["affine_ranks"] == ranks
             and rat(row["all_vertex_loss_sum"]) == total
             and rat(row["core_unordered_loss_sum"]) == core_total
             and row["strict_pairs"] == sum(d > 0 for d in gram_losses), "step loss record")

    def unordered_distance_sum(rows):
        rows=rows[:nc]
        moment=tuple(sum(x[k] for x in rows) for k in range(3))
        return nc*sum(inner(x,x) for x in rows)-inner(moment,moment)
    total=unordered_distance_sum(stages[0])-unordered_distance_sum(stages[-1])
    need(total == sum(step_sums) == rat(cert["accumulated_core_unordered_loss_sum"]), "loss telescope")
    floor=rat(cert["uniform_ordered_loss_floor"])
    need(0 < floor <= 2*total/F(1 << (2*ell)), "positive ordered loss floor")
    a=nat(cert["normalized_loss_exponent"])
    need(dyadic_fits(a,floor/S), "variance-normalized loss")

    centers=list(map(vec,data["endpoint_centers"]))
    need(len(centers) == 2, "endpoint centers")
    p,q = [[diff(x,c) for x in rows] for rows,c in zip((stages[0],stages[-1]),centers)]
    need(all(inner(x,x) <= Re*Re for x in p[:nc]+q), "endpoint radius")
    need(all(inner(x,x) <= R*R for x in p),"initial comparison radius")
    wc,wr=data["width_witness"],cert["width"]
    need(wc["kind"] == "nested-hulls-rational-cap-v1", "width kind")
    bary=[[rat(x) for x in row] for row in wc["target_in_source_hull"]]
    need(len(bary) == n, "hull row count")
    for row,y in zip(bary,q):
        need(len(row) == nc and min(row) >= 0 and sum(row) == 1, "hull simplex")
        need(all(sum(row[i]*(p[i][k]-y[k]) for i in range(nc)) == 0 for k in range(3)), "hull residual")
    axis=vec(wc["cap_axis"])
    c,r=rat(wc["cap_cosine"]),rat(wc["cap_sine_upper"])
    star=nat(wc["source_witness"])
    nat(wc.get("perpendicular_bits",16))
    need(star < nc and inner(axis,axis) == 1 and 0 <= c < 1 and r >= 0 and r*r+c*c >= 1,
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
        need(len(lam) == nc, "anchor dual shape")
        # A dual left-kernel witness for the seven unknown linear coefficients.
        rows=[(F(1),)+p[i]+q[i] for i in range(nc)]
        need(all(sum(lam[i]*rows[i][k] for i in range(nc)) == 0 for k in range(7)), "anchor dual kernel")
        residual=sum(lam[i]*sum((p[i][k]-q[i][k])*(p[i][k]+q[i][k])
                               for k in range(3)) for i in range(nc))
        need(residual != 0, "anchor dual residual")
        obstruction={"squared_norm_residual":str(residual),"endpoint_anchors_exist":False}
    need(cert["endpoint_anchor_obstruction"] == obstruction, "anchor obstruction record")

    z=cert["schedule"]
    A,Q=rat(z["tail_A"]),rat(z["tail_Q"])
    j,k,N,M,brho,B=[nat(z[key]) for key in ("j","k","N","M","target_thickening_exponent","budget_exponent")]
    need(A >= 6*(Re+1)**2+2*S*(ell+1) and Q >= 8*A/w, "signed tail schedule")
    need(j >= Q*Q, "tail-middle overlap")
    need(k >= a+9*R*R+4, "endpoint peak guard")
    nN=40*R*R+9*R+38+3*j+8*(k+1)
    nM=66*R*R+2*R+18+4*j+5*(k+1)
    need(N >= max(nN,nM)+k+2*R*R+2*R+1,"imported mixed-chain margin")
    need(M >= a+N,"total ordered loss factor")
    need(dyadic_fits(brho,min(F(1,2),w/4)), "target thickening reserve")
    need(B >= max(M+1,k,ell+brho+1), "core retention and all-threshold budget")
    conclusion={
        "variance_interval":["1",str(S)],"threshold_interval":"[0,infinity)",
        "reference_prior_region":"core v_i >= 2^-mass_exponent; arbitrary remaining law on the background polytope",
        "error_guard":"W1(mu,mu_actual)+W1(nu,nu_actual) <= 2^-budget_exponent",
        "target_support_guard":"supp(nu_actual) subset K + B(0,2^-target_thickening_exponent)",
        "middle_band":"[C_s*2^-j, actual_source_peak]","middle_gap_exponent":M+1,
        "endpoint_anchor_required":False,"actual_contraction_required":False,
        "actual_source_support_bound_required":False,
        "minimum_background_mass_required":False,"background_atom_count_bound_required":False,
        "diffuse_background_allowed":True,"minimum_step_loss_required":False,
        "independent_review":"PENDING",
    }
    need(cert["conclusion"] == conclusion,"conclusion overreach")
    diameters=[max(inner(diff(x,y),diff(x,y)) for x in rows for y in rows) for rows in (p,q)]
    return encode({"core_labels":nc,"background_vertices":len(background),"geometry_labels":n,"steps":L,"comparison_radius":R,"endpoint_radius":Re,
                   "accumulated_core_unordered_loss_sum":total,"uniform_ordered_loss_floor":floor,
                   "width_lower":w,"target_thickening_exponent":brho,"budget_exponent":B,"variance_interval":[F(1),S],
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
    with tempfile.TemporaryDirectory(prefix="gaussian-core-w1-") as t:
        path=Path(t)/"input.json"
        path.write_text(json.dumps(data))
        return json.loads(subprocess.check_output([sys.executable,"-B",str(HERE/"certificate.py"),str(path)]))


def suite(data,cert):
    family=check(data,cert)
    bad=[]
    for key in ("j","k","N","M","budget_exponent"):
        bad.append(damage(data,cert,"understated_"+key,
            lambda c,key=key:c["schedule"].__setitem__(key,c["schedule"][key]-1)))
    for label,change in [
        ("background_losses_used_for_core_floor",lambda c:c.__setitem__("uniform_ordered_loss_floor","10")),
        ("wrong_core_telescope",lambda c:c.__setitem__("accumulated_core_unordered_loss_sum","271")),
        ("wrong_core_step_loss",lambda c:c["step_records"][0].__setitem__("core_unordered_loss_sum","45")),
        ("wrong_vertex_step_loss",lambda c:c["step_records"][0].__setitem__("all_vertex_loss_sum","1")),
        ("false_width",lambda c:c["width"].__setitem__("lower","1")),
        ("false_transverse_bound",lambda c:c["width"]["perpendicular_upper"].__setitem__(13,"0")),
        ("false_anchor_residual",lambda c:c["endpoint_anchor_obstruction"].__setitem__("squared_norm_residual","7")),
        ("target_envelope_too_thick",lambda c:c["schedule"].__setitem__("target_thickening_exponent",0)),
        ("insufficient_core_retention",lambda c:c["schedule"].__setitem__("target_thickening_exponent",c["schedule"]["budget_exponent"]+1)),
        ("unrestricted_target_support",lambda c:c["conclusion"].__setitem__("target_support_guard","none")),
        ("false_all_variance_scope",lambda c:c["conclusion"].__setitem__("variance_interval",["0","infinity"])),
    ]:
        bad.append(damage(data,cert,label,change))
    for label,change in [
        ("float_input",lambda d:d["core_stages"][0][1].__setitem__(0,1.0)),
        ("empty_core_prior_region",lambda d:d.__setitem__("mass_exponent",3)),
        ("invalid_variance",lambda d:d.__setitem__("variance_ratio","1/2")),
        ("step_anchor_mismatch",lambda d:d["step_guards"][0]["anchors"].__setitem__(1,[0,0,0])),
        ("false_straight_guard",lambda d:d["step_guards"][0].__setitem__("kind","straight")),
        ("six_dimensional_lift",lambda d:d["step_guards"][0].__setitem__("kind","orthogonal_lift")),
        ("expanding_core_pair",lambda d:d["core_stages"][1].__setitem__(0,[3,0,0])),
        ("missing_core_label",lambda d:d["core_stages"][1].pop()),
        ("missing_background",lambda d:d.__setitem__("background_vertices",[])),
        ("expanding_core_background_pair",lambda d:d["background_vertices"].__setitem__(0,[2,0,0])),
        ("endpoint_radius_too_small",lambda d:d.__setitem__("endpoint_radius",2)),
        ("incorrect_hull",lambda d:d["width_witness"]["target_in_source_hull"].__setitem__(3,[0,0,0,1]+[0]*11)),
        ("nonunit_cap",lambda d:d["width_witness"].__setitem__("cap_axis",[2,0,0])),
        ("incorrect_cap_sine",lambda d:d["width_witness"].__setitem__("cap_sine_upper","0")),
        ("false_anchor_dual",lambda d:d["endpoint_anchor_obstruction"].__setitem__(1,0)),
        ("zero_core_chain_loss",lambda d:d.__setitem__("core_stages",[copy.deepcopy(d["core_stages"][0]) for _ in d["core_stages"]])),
    ]:
        bad.append(damage(data,cert,label,change,"input"))

    # Geometry witnesses carry no prior mass: this redundant presentation has
    # 50 vertices/labels, exceeding 2^ell=32, yet describes exactly the same family.
    core=[[vec(x) for x in rows] for rows in data["core_stages"]]
    nc=len(core[0]);V=list(map(vec,data["background_vertices"]))
    refined=copy.deepcopy(data)
    for v in itertools.product((F(-1,3),F(0),F(1,3)),repeat=3):
        refined["background_vertices"].append(encode(v))
        row=[F(0)]*nc
        row[0]=1-sum(map(abs,v))
        for j,t in enumerate(v):
            if t:
                axis=[F(0)]*3;axis[j]=1 if t>0 else -1
                row[core[0].index(tuple(axis))]+=abs(t)
        refined["width_witness"]["target_in_source_hull"].append(encode(row))
    cr=generated(refined);fr=check(refined,cr)
    need(cr["schedule"] == cert["schedule"] and cr["uniform_ordered_loss_floor"] == cert["uniform_ordered_loss_floor"],"background presentation changed budget")
    need(cr["geometry_labels"] > 1 << data["mass_exponent"],"mass-free geometry control vacuous")

    # Check the affine cross-loss extension at vertices and interior points,
    # independently comparing a direct squared-distance loss with interpolation.
    points=[tuple(F(0) for _ in range(3)),tuple(F(1,9) for _ in range(3)),(F(-1,6),F(1,7),F(-1,8))]
    interpolation_controls=0
    for x in points:
        weights=[]
        for v in V:
            z=F(1)
            for k in range(3):
                z *= (1+9*v[k]*x[k])/2
            weights.append(z)
        need(min(weights)>=0 and sum(weights)==1,"cube barycentric weights")
        need(tuple(sum(weights[i]*V[i][k] for i in range(len(V))) for k in range(3))==x,"cube moment")
        for p,q in zip(core,core[1:]):
            for u,v in zip(p,q):
                def loss(y):
                    a,b=diff(u,y),diff(v,y)
                    return inner(a,a)-inner(b,b)
                need(loss(x)==sum(t*loss(y) for t,y in zip(weights,V))>=0,"affine continuum pair guard")
                interpolation_controls+=1

    # Weighted variance telescopes use core, zero/positive background masses,
    # and increasingly small background components. The proof handles all laws.
    priors=[];m=F(1,1 << data["mass_exponent"])
    slack=1-nc*m;extra=V+points
    for divisor in (1,2,17,1024):
        bg=slack/F(divisor)
        v=[m]*nc+[F(0)]*len(extra)
        v[0]+=slack-bg
        for i in range(len(extra)):
            v[nc+i]=bg/F(len(extra))
        priors.append(v)
    v=[m]*nc+[F(0)]*len(extra);v[0]+=slack;priors.append(v)
    variance_controls=[]
    allstages=[rows+extra for rows in core]
    for v in priors:
        need(sum(v)==1 and min(v)>=0,"prior normalization")
        def variance(rows):
            mean=tuple(sum(t*x[k] for t,x in zip(v,rows)) for k in range(3))
            return sum(t*inner(x,x) for t,x in zip(v,rows))-inner(mean,mean)
        direct=2*(variance(allstages[0])-variance(allstages[-1]))
        pair=sum(v[i]*v[j]*(inner(diff(allstages[0][i],allstages[0][j]),diff(allstages[0][i],allstages[0][j]))
                          -inner(diff(allstages[-1][i],allstages[-1][j]),diff(allstages[-1][i],allstages[-1][j])))
                 for i in range(len(v)) for j in range(len(v)))
        need(direct==pair==sum(2*(variance(x)-variance(y)) for x,y in zip(allstages,allstages[1:])),"weighted normalization and telescope")
        need(direct>=rat(cert["uniform_ordered_loss_floor"]),"core-only floor")
        variance_controls.append(str(direct))

    # Exact algebra controls for the newly asymmetric tail enclosure; these do
    # not replace the analytic layer-cake and exponential proof in PROOF.md.
    cubic_controls=0
    for radius in (F(1),F(2),F(4)):
        K=3*radius*radius
        for mult in (4,7,20):
            q=mult*radius;A0=K+5*radius*radius
            for u in (-radius,F(0),radius):
                for e in (-K/q,K/q):
                    need(abs((q+u+e)**3-q**3-3*q*q*u)<=3*A0*q,"cubic signed-tail enclosure")
                    need(q+u-K/q>0,"positive inner radius")
                    cubic_controls+=1
    rho=F(1,1 << cert["schedule"]["target_thickening_exponent"])
    eta=m*rho/2
    need(m-eta/rho==m/2 and rho<=rat(cert["width"]["lower"])/4,"retention boundary")

    # Exercise every finite guard on the continuum, not just the fold calibration.
    mixed={"schema":"core-wasserstein-family-input-v1",
        "core_stages":[[[0,0,0],[2,0,0]],[[0,0,0],["3/2",0,0]],[[0,0,0],[1,0,0]]],
        "background_vertices":[[0,0,0]],
        "step_guards":[{"kind":"straight"},{"kind":"orthogonal_lift"}],
        "comparison_radius":2,"endpoint_radius":2,"endpoint_centers":[[0,0,0],[0,0,0]],
        "mass_exponent":2,"variance_ratio":4,
        "width_witness":{"kind":"nested-hulls-rational-cap-v1","target_in_source_hull":[[1,0],["1/2","1/2"],[1,0]],
            "cap_axis":[1,0,0],"cap_cosine":"4/5","cap_sine_upper":"3/5","source_witness":1}}
    mc=generated(mixed);mf=check(mixed,mc)
    need([r["affine_ranks"] for r in mc["step_records"]]==[None,[1,1]],"mixed guard control")
    # Norm zero-loss insertion must not change the global schedule.
    d=copy.deepcopy(data)
    d["core_stages"].insert(0,copy.deepcopy(d["core_stages"][0]))
    d["step_guards"].insert(0,{"kind":"norm","anchors":[[0,0,0],[0,0,0]]})
    c=generated(d);check(d,c)
    need(c["schedule"]==cert["schedule"],"zero-loss insertion changed budget")

    output=subprocess.check_output([sys.executable,"-B",str(HERE/"certificate.py"),str(HERE/"INPUT.json")])
    need(json.loads(output)==cert and output==(HERE/"CERTIFICATE.json").read_bytes(),"canonical producer output")
    return {"status":"CORE_WASSERSTEIN_FAMILY_EXACT_CONTROLS_PASS","family":family,
        "certificate_sha256":hashlib.sha256(output).hexdigest(),"dependency_pins":dependency_checks(),
        "negative_controls":bad,"background_refinement":{"geometry_labels":fr["geometry_labels"],
            "background_vertices":fr["background_vertices"],"same_core_loss_and_budget":True},
        "affine_continuum_controls":interpolation_controls,"weighted_loss_controls":variance_controls,
        "signed_cubic_controls":cubic_controls,"core_retention_boundary":"PASS",
        "straight_and_lift_guard_control":mf,"zero_loss_insertion":"PASS",
        "integer_inequality_checker_imports_producer":False,"dyadic_budget_denominator_materialized":False,
        "trust_boundary":"Written continuum extension, transport/tail proof and imported analytic margins; author checks, not independent acceptance."}


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path)
    parser.add_argument("--certificate",type=Path)
    args=parser.parse_args()
    need((args.input is None)==(args.certificate is None),"supply both input and certificate")
    ip=args.input if args.input is not None else HERE/"INPUT.json"
    cp=args.certificate if args.certificate is not None else HERE/"CERTIFICATE.json"
    data,cert=json.loads(ip.read_text()),json.loads(cp.read_text())
    result=({"status":"CORE_WASSERSTEIN_FAMILY_CERTIFICATE_VERIFIED","family":check(data,cert),
             "dependency_pins":dependency_checks()} if args.input is not None else suite(data,cert))
    if args.input is None and (HERE/"EXPECTED.json").exists():
        need(result==json.loads((HERE/"EXPECTED.json").read_text()),"expected controls record mismatch")
    print(json.dumps(result,sort_keys=True,indent=2))
