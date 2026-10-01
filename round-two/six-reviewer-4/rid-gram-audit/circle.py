"""Exact common-angle decisions, written by independent reviewer six-reviewer-4.

A constraint is (x,y,h), meaning x*cos(theta)+sqrt(metric)*y*sin(theta)>=h.
No angle samples, inverse trig, researcher modules, or floating signs.
"""
from itertools import combinations

def require(ok,message):
    if not ok: raise ValueError(message)

def radical_nonnegative(base, coefficient, square):
    require(square>=0,'nonnegative radical square')
    if coefficient==0 or square==0: return base>=0
    if base>=0 and coefficient>=0: return True
    if base<0 and coefficient<=0: return False
    if base>=0: return base*base>=coefficient*coefficient*square
    return coefficient*coefficient*square>=base*base

def feasible(constraints,metric=1):
    require(metric>0,'positive plane metric')
    active=[]
    for i,(x,y,h) in enumerate(constraints):
        norm=x*x+metric*y*y
        if norm==0:
            if h>0:return {'feasible':False,'empty_constraint':i,'active_constraints':len(active)}
            continue
        if h>0 and h*h>norm:return {'feasible':False,'empty_constraint':i,'active_constraints':len(active)}
        if h<=0 and h*h>=norm:continue
        require(norm-h*h>=0,'active circle boundary')
        active.append((i,x,y,h,norm))
    if not active:return {'feasible':True,'whole_circle':True,'active_constraints':0}
    rejected=[]
    for i,x,y,h,norm in active:
        for side in (-1,1):
            for j,X,Y,H,A in active:
                base=h*(x*X+metric*y*Y)-H*norm
                determinant=x*Y-y*X
                if not radical_nonnegative(base,side*determinant,metric*(norm-h*h)):
                    rejected.append([i,side,j])
                    break
            else:
                return {'feasible':True,'boundary':i,'side':side,'active_constraints':len(active)}
    return {'feasible':False,'active_constraints':len(active),'rejected_boundaries':rejected}

def positive_disk_oracle(constraints):
    """Independent closest-point algorithm for strictly positive thresholds."""
    require(all(h>0 for x,y,h in constraints),'positive halfplanes only')
    if not constraints:return True
    candidates=[]
    for x,y,h in constraints:
        norm=x*x+y*y
        if norm==0:return False
        candidates.append((h*x/norm,h*y/norm))
    for (x,y,h),(X,Y,H) in combinations(constraints,2):
        d=x*Y-y*X
        if d!=0:candidates.append(((h*Y-y*H)/d,(x*H-h*X)/d))
    return any(u*u+v*v<=1 and all(x*u+y*v>=h for x,y,h in constraints) for u,v in candidates)
