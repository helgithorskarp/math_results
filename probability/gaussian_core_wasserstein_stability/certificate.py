"""Exact certificate for a protected source core and arbitrary polytope background.

Adapted from gaussian_chain_stability_certificate. The geometry guards certify
an entire continuum by the affine extension proved in PROOF.md. Only core
masses have lower bounds; the actual source need not have bounded support.
"""
import argparse
from fractions import Fraction as F
import json
from math import isqrt


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rational(x):
    require(type(x) in (int, str), "exact rational encoding required")
    return F(x)


def integer(x, lower=0):
    require(type(x) is int and x >= lower, "integer domain")
    return x


def vector(x):
    require(type(x) is list and len(x) == 3, "three coordinates required")
    return list(map(rational, x))


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def sub(x, y):
    return [a-b for a, b in zip(x, y)]


def ceil_sqrt(x):
    require(x >= 0, "negative square root")
    z = isqrt(x.numerator // x.denominator)
    return z if z*z == x else z+1


def dyadic_below(x):
    require(x > 0, "positive dyadic guard required")
    b = max(0, x.denominator.bit_length()-x.numerator.bit_length())
    if (x.numerator << b) < x.denominator:
        b += 1
    return b


def affine_rank(rows):
    matrix=[sub(row,rows[0]) for row in rows[1:]]
    rank=0
    for col in range(3):
        pivot=next((j for j in range(rank,len(matrix)) if matrix[j][col]),None)
        if pivot is None:
            continue
        matrix[rank],matrix[pivot]=matrix[pivot],matrix[rank]
        div=matrix[rank][col]
        matrix[rank]=[v/div for v in matrix[rank]]
        for j in range(rank+1,len(matrix)):
            q=matrix[j][col]
            matrix[j]=[x-q*y for x,y in zip(matrix[j],matrix[rank])]
        rank+=1
    return rank


def produce(data):
    require(data["schema"] == "core-wasserstein-family-input-v1", "input schema")
    stages = [[vector(x) for x in stage] for stage in data["core_stages"]]
    require(len(stages) >= 2 and len(stages[0]) >= 2, "nonempty chain required")
    nc, L = len(stages[0]), len(stages)-1
    require(all(len(stage) == nc for stage in stages), "fixed core labels required")
    background = list(map(vector, data["background_vertices"]))
    require(len(background) > 0, "nonempty background polytope required")
    stages = [stage+background for stage in stages]
    n = nc+len(background)
    guards=data["step_guards"]
    require(len(guards) == L, "step guards")
    R = integer(data["comparison_radius"], 1)
    Re = integer(data["endpoint_radius"], 1)
    ell = integer(data["mass_exponent"])
    S = rational(data["variance_ratio"])
    m = F(1, 1 << ell)
    require(S >= 1 and nc*m <= 1, "variance or empty prior domain")
    step_records, sums = [], []
    for t in range(L):
        x,y=stages[t:t+2]
        guard=guards[t]
        kind=guard["kind"]
        require(kind in ("norm","straight","orthogonal_lift"), "unsupported step guard")
        ranks=None
        if kind == "norm":
            anchors=list(map(vector,guard["anchors"]))
            require(len(anchors) == 2,"two link anchors")
            x,y=[[sub(z,a) for z in rows] for rows,a in zip((x,y),anchors)]
            require(all(dot(p,p) == dot(q,q) <= R*R for p,q in zip(x,y)), "step anchor/radius")
        if kind == "orthogonal_lift":
            ranks=[affine_rank(x),affine_rank(y)]
            require(sum(ranks) <= 5,"orthogonal lift exceeds dimension five")
        losses, core_losses = [], []
        for i in range(n):
            for j in range(i):
                u, v = sub(x[i],x[j]), sub(y[i],y[j])
                delta = dot(u,u)-dot(v,v)
                require(delta >= 0, "step expands a pair")
                if kind == "straight":
                    require(dot(v,sub(v,u)) <= 0,"straight interpolation expands")
                losses.append(delta)
                if i < nc:
                    core_losses.append(delta)
        sums.append(sum(core_losses))
        step_records.append({"kind":kind,"affine_ranks":ranks,
                             "core_unordered_loss_sum": str(sums[-1]),
                             "all_vertex_loss_sum": str(sum(losses)),
                             "strict_pairs": sum(delta > 0 for delta in losses)})
    d0 = 2*m*m*sum(sums)
    require(d0 > 0, "zero accumulated loss floor")

    centers = list(map(vector, data["endpoint_centers"]))
    require(len(centers) == 2, "two endpoint centers required")
    p, q = [[sub(x,c) for x in stage] for stage,c in
            zip((stages[0], stages[-1]), centers)]
    require(all(dot(x,x) <= Re*Re for x in p[:nc]+q), "endpoint radius")
    require(all(dot(x,x) <= R*R for x in p),"initial comparison radius")
    wc = data["width_witness"]
    require(wc["kind"] == "nested-hulls-rational-cap-v1", "width witness kind")
    bary = [[rational(z) for z in row] for row in wc["target_in_source_hull"]]
    require(len(bary) == n, "containment row count")
    for y,row in zip(q,bary):
        require(len(row) == nc and min(row) >= 0 and sum(row) == 1, "barycentric domain")
        require([sum(row[i]*p[i][k] for i in range(nc)) for k in range(3)] == y, "hull containment")
    axis = vector(wc["cap_axis"])
    c,r = rational(wc["cap_cosine"]), rational(wc["cap_sine_upper"])
    star = integer(wc["source_witness"])
    scale = 1 << integer(wc.get("perpendicular_bits",16))
    require(star < nc and dot(axis,axis) == 1 and 0 <= c < 1 and r >= 0
            and r*r >= 1-c*c, "cap geometry")
    axial, perp = [], []
    for y in q:
        v = sub(p[star],y)
        A = dot(axis,v)
        require(A >= 0, "negative cap axial coefficient")
        axial.append(A)
        perp.append(F(ceil_sqrt((dot(v,v)-A*A)*scale*scale), scale))
    gamma = min(c*A-r*b for A,b in zip(axial,perp))
    w = (1-c)*gamma/2
    require(0 < w <= 2*Re, "nonpositive or inconsistent width")

    obstruction = None
    if "endpoint_anchor_obstruction" in data:
        lam = list(map(rational, data["endpoint_anchor_obstruction"]))
        require(len(lam) == nc and sum(lam) == 0, "anchor obstruction shape")
        require(all(sum(lam[i]*rows[i][k] for i in range(nc)) == 0
                    for rows in (p,q) for k in range(3)), "anchor obstruction moments")
        value = sum(lam[i]*(dot(p[i],p[i])-dot(q[i],q[i])) for i in range(nc))
        require(value != 0, "anchor obstruction has no residual")
        obstruction = {"squared_norm_residual": str(value), "endpoint_anchors_exist": False}

    a = dyadic_below(d0/S)
    A = 6*(Re+1)**2+2*S*(ell+1)
    Q = 8*A/w
    j = -(-(Q*Q).numerator // (Q*Q).denominator)
    k = a+9*R*R+4
    N = max(40*R*R+9*R+38+3*j+8*(k+1),
            66*R*R+2*R+18+4*j+5*(k+1))+k+2*R*R+2*R+1
    M = a+N
    brho = dyadic_below(min(F(1,2),w/4))
    B = max(M+1,k,ell+brho+1)
    return {
        "schema": "core-wasserstein-family-certificate-v1",
        "status": "CERTIFIED_CORE_WASSERSTEIN_ALL_THRESHOLD_FAMILY",
        "core_labels": nc, "background_vertices": len(background),
        "geometry_labels": n, "steps": L, "pairs_per_step": n*(n-1)//2,
        "step_records": step_records,
        "accumulated_core_unordered_loss_sum": str(sum(sums)),
        "uniform_ordered_loss_floor": str(d0), "normalized_loss_exponent": a,
        "width": {"lower": str(w), "cap_gap_lower": str(gamma),
                  "perpendicular_upper": list(map(str,perp))},
        "endpoint_anchor_obstruction": obstruction,
        "schedule": {"tail_A": str(A), "tail_Q": str(Q), "j": j, "k": k,
                     "N": N, "M": M, "target_thickening_exponent": brho, "budget_exponent": B},
        "conclusion": {
            "variance_interval": ["1", str(S)], "threshold_interval": "[0,infinity)",
            "reference_prior_region": "core v_i >= 2^-mass_exponent; arbitrary remaining law on the background polytope",
            "error_guard": "W1(mu,mu_actual)+W1(nu,nu_actual) <= 2^-budget_exponent",
            "target_support_guard": "supp(nu_actual) subset K + B(0,2^-target_thickening_exponent)",
            "middle_band": "[C_s*2^-j, actual_source_peak]",
            "middle_gap_exponent": M+1,
            "endpoint_anchor_required": False, "actual_contraction_required": False,
            "actual_source_support_bound_required": False,
            "minimum_background_mass_required": False,
            "background_atom_count_bound_required": False,
            "diffuse_background_allowed": True, "minimum_step_loss_required": False,
            "independent_review": "PENDING",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    args = parser.parse_args()
    with open(args.input) as f:
        result = produce(json.load(f))
    print(json.dumps(result,sort_keys=True,indent=2))
