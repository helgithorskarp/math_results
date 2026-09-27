#!/usr/bin/env python3
"""Exact supporting controls, NOT an adverse-volume or counterexample oracle."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def d2(p, q):
    return sum((x-y)**2 for x,y in zip(p,q))


def bary(points, weights):
    require(len(points)==len(weights), "Weight count")
    require(all(w>=0 for w in weights) and sum(weights)==1, "Not a probability vector")
    return tuple(sum(w*p[j] for w,p in zip(weights,points)) for j in range(3))


def variance(points, weights):
    c=bary(points,weights)
    return sum(w*d2(p,c) for w,p in zip(weights,points))


def rank(rows):
    a=[list(map(Q,row)) for row in rows]
    r=0
    for c in range(len(a[0])):
        k=next((k for k in range(r,len(a)) if a[k][c]),None)
        if k is None:
            continue
        a[r],a[k]=a[k],a[r]
        pivot=a[r][c]
        a[r]=[x/pivot for x in a[r]]
        for k in range(len(a)):
            if k!=r:
                scale=a[k][c]
                a[k]=[x-scale*y for x,y in zip(a[k],a[r])]
        r+=1
    return r


def compositions(m,n):
    if n==1:
        yield (m,)
    else:
        for k in range(m+1):
            for rest in compositions(m-k,n-1):
                yield (k,)+rest


def simplex(m,n):
    return [tuple(Q(k,m) for k in row) for row in compositions(m,n)]


def geometry(a,b,qa,qb):
    require(len(a)==len(qa) and len(b)==len(qb), "Label mismatch")
    for p,q in ((a,qa),(b,qb)):
        for i in range(len(p)):
            for j in range(i):
                require(d2(p[i],p[j])==d2(q[i],q[j]), "Nonrigid component")
    p,q=a+b,qa+qb
    losses=[d2(p[i],p[j])-d2(q[i],q[j]) for i in range(len(p)) for j in range(i)]
    require(all(x>=0 for x in losses), "Not a contraction")
    return losses


def grid_budget(n,m,tau,eta):
    require(isinstance(n,int) and n>=1 and isinstance(m,int) and m>=1, "Invalid grid")
    require(tau>0 and eta>0 and n*tau<=1, "Invalid posterior floor or error")
    error=Q(4*n*n,m*m)/tau
    require(error<=eta, "Grid does not meet the conditional KL budget")
    return error


def gaussian_budget(delta, radius_upper_bounds):
    require(delta>0 and len(radius_upper_bounds)>0, "Missing positive conditional margin")
    require(all(r>=0 for r in radius_upper_bounds), "Negative radius bound")
    n=len(radius_upper_bounds)
    total=sum(radius_upper_bounds)
    epsilon=min(Q(1),delta/(32*total+64*n))
    # Uses epsilon^(3/2)<=epsilon, pi<4 and sqrt(pi/2)<2.
    bound=16*epsilon*total+32*n*epsilon
    require(0<epsilon<=1 and bound<=delta/2, "Conditional tail budget failed")
    return epsilon,bound


def expect_rejected(fn):
    try:
        fn()
    except ValueError:
        return 1
    raise ValueError("Corrupted control was accepted")


def record():
    raw=(HERE/"INPUTS.json").read_bytes()
    data=json.loads(raw)
    a,b,qa,qb=[list(map(lambda row:tuple(map(Q,row)),data[k]))
               for k in ("source_A","source_B","target_A","target_B")]
    losses=geometry(a,b,qa,qb)
    p,q=a+b,qa+qb
    paired=rank([(1,)+x+y for x,y in zip(p,q)])-1
    require(paired==6, "Paired rank-six control changed")
    require(rank([(1,)+x for x in a])==4 and rank([(1,)+x for x in b])==4,
            "Both component affine spans must be three-dimensional")

    la,lb=simplex(3,4),simplex(4,4)
    require(len(la)==comb(6,3) and len(lb)==comb(7,3), "Incomplete simplex enumeration")
    ga=[bary(a,w) for w in la]; gb=[bary(b,w) for w in lb]
    gqa=[bary(qa,w) for w in la]; gqb=[bary(qb,w) for w in lb]
    barycentric_pairs=0
    for i,w in enumerate(la):
        for j,v in enumerate(lb):
            direct=d2(ga[i],gb[j])-d2(gqa[i],gqb[j])
            average=sum(w[k]*v[l]*(d2(a[k],b[l])-d2(qa[k],qb[l]))
                        for k in range(4) for l in range(4))
            require(direct==average and direct>=0, "Barycentric cross identity")
            barycentric_pairs+=1
    enlarged_losses=geometry(ga,gb,gqa,gqb)
    variance_controls=0
    square_controls=0
    for pts,tgt,grid in ((a,qa,la),(b,qb,lb)):
        for w in grid:
            v=variance(pts,w)
            require(v==variance(tgt,w), "Entropy-ball radius variance changed")
            # Second representation independently uses all pair distances.
            pair_v=sum(w[i]*w[j]*d2(pts[i],pts[j])
                       for i in range(4) for j in range(4))/2
            require(v==pair_v, "Pair variance identity")
            variance_controls+=1
            c=bary(pts,w)
            for x in ((Q(0),Q(0),Q(0)),(Q(2,3),Q(-7,5),Q(11,4))):
                require(sum(wi*d2(x,pi) for wi,pi in zip(w,pts))==d2(x,c)+v,
                        "Completed-square envelope identity")
                square_controls+=1

    rounding_controls=0
    for denominator in (11,17):
        # Strict posterior coordinates, including strongly unequal values.
        for counts in compositions(denominator-4,4):
            posterior=tuple(Q(k+1,denominator) for k in counts)
            tau=min(posterior)
            for m in (7,16,64):
                first=[(z*m).numerator//(z*m).denominator for z in posterior[:-1]]
                rounded=tuple(Q(k,m) for k in first+[m-sum(first)])
                l1=sum(abs(x-y) for x,y in zip(rounded,posterior))
                chi=sum((x-y)**2/y for x,y in zip(rounded,posterior))
                require(sum(rounded)==1 and min(rounded)>=0, "Rounding simplex")
                require(l1<=Q(8,m) and chi<=l1*l1/tau<=Q(64,m*m)/tau,
                        "Conditional KL upper-bound control")
                rounding_controls+=1
    cover_examples=[]
    for n,tau,eta,m in ((4,Q(1,64),Q(1,8),256),(1,Q(1),Q(1,4),4),
                        (8,Q(1,1024),Q(1,16),2048)):
        error=grid_budget(n,m,tau,eta)
        cover_examples.append({"n":n,"m":m,"tau":str(tau),"eta":str(eta),
                               "chi_square_bound":str(error),"grid_size":comb(m+n-1,n-1)})

    conditional_budgets=[]
    for delta in (Q(1,1024),Q(1,7),Q(2),Q(10000)):
        for radii in ([Q(0)],[Q(1,2),Q(3,2)],[Q(1),Q(2),Q(3),Q(7,4)]):
            epsilon,bound=gaussian_budget(delta,radii)
            conditional_budgets.append({"assumed_delta":str(delta),"radii_upper":list(map(str,radii)),
                                        "epsilon":str(epsilon),"tail_bound":str(bound)})
    clip_controls=0
    for h in (Q(1,7),Q(1),Q(8,3)):
        for z in (Q(0),Q(1,100),Q(1,2),Q(2),Q(9)):
            require(max(z-h,0)==z-h*min(z/h,1), "Hinge/clipping orientation")
            clip_controls+=1
    changed=list(qb);changed[0]=tuple(x+Q(1,100) for x in changed[0])
    negatives=[lambda:geometry(a,b,qa,changed),
               lambda:bary(a,[Q(1)]*4),
               lambda:bary(a,[Q(2),Q(-1),Q(0),Q(0)]),
               lambda:grid_budget(4,8,Q(1,64),Q(1,8)),
               lambda:grid_budget(4,256,Q(0),Q(1,8)),
               lambda:grid_budget(4,256,Q(1,64),Q(0)),
               lambda:grid_budget(4,256,Q(1),Q(1,8)),
               lambda:gaussian_budget(Q(0),[Q(1)]),
               lambda:gaussian_budget(Q(1),[]),
               lambda:gaussian_budget(Q(1),[Q(-1)])]
    rejected=sum(expect_rejected(fn) for fn in negatives)
    return {"status":"TWO_BODY_CONTACT_TRANSFER_CONTROLS_PASS",
            "adverse_contact_supplied":False,"counterexample_certified":False,
            "input_sha256":hashlib.sha256(raw).hexdigest(),
            "original_pair_count":len(losses),"original_tight_pairs":sum(x==0 for x in losses),
            "original_strict_pairs":sum(x>0 for x in losses),"paired_affine_rank":paired,
            "barycentric_cross_identities":barycentric_pairs,
            "enlarged_pair_controls":len(enlarged_losses),
            "invariant_variance_controls":variance_controls,"completed_square_controls":square_controls,
            "simplex_rounding_controls":rounding_controls,"cover_budget_examples":cover_examples,
            "conditional_tail_budgets":conditional_budgets,
            "hinge_clipping_controls":clip_controls,"invalid_controls_rejected":rejected}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit",action="store_true",help="Emit controls without reading EXPECTED.json")
    args=parser.parse_args()
    result=record()
    if not args.emit:
        require(result==json.loads((HERE/"EXPECTED.json").read_text()), "Expected record mismatch")
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
