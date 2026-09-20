#!/usr/bin/env python3
"""Exact supporting audit, not a finite proof of the infinite geometric theorem.

Python 3.11+, standard library only. No solver, floating point, downloaded
data, target-source import, or trigonometric numerical enclosure is used.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import isqrt
from pathlib import Path
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sign_coefficients(c):
    require(len(c) >= 3 and all(x in (-1, 1) for x in c), "invalid code")
    return (-(c[0] + c[-1]),) + tuple(c[i-1]-c[i] for i in range(1,len(c)))


def edge_velocities(v):
    return tuple(v[i+1]-v[i] for i in range(len(v)-1)) + (-v[0]-v[-1],)


def check_motion(a, v):
    require(any(v), "zero motion")
    require(sum(x*y for x,y in zip(a,v)) == 0, "closure changes")
    require(any(edge_velocities(v)), "every edge is stationary")


def code_audit():
    counts = dict(codes=0, zero_coefficient_motions=0, two_vertex_motions=0,
                  endpoint_motions=0, adjacent_pair_motions=0)
    digest = hashlib.sha256()
    for n in range(3, 11):
        for c in product((-1,1), repeat=n):
            a=sign_coefficients(c)
            # Direct expansion of sum c_j(z_(j+1)-z_j), not the formula for a.
            expanded=[0]*n
            for j,cj in enumerate(c):
                expanded[j]-=cj
                if j+1<n:
                    expanded[j+1]+=cj
                else:
                    expanded[0]-=cj
            require(tuple(expanded)==a, "summation-by-parts convention")
            require(any(a), "zero closure row")
            counts['codes']+=1
            for r in range(n):
                if a[r]==0:
                    v=[0]*n; v[r]=1
                    check_motion(a,v)
                    counts['zero_coefficient_motions']+=1
                    counts['endpoint_motions']+=(r==0)
                    digest.update(bytes([n,*[x+2 for x in a],r]))
            for r,s in combinations(range(n),2):
                if a[r] and a[s]:
                    v=[0]*n; v[r]=a[s]; v[s]=-a[r]
                    check_motion(a,v)
                    counts['two_vertex_motions']+=1
                    counts['endpoint_motions']+=(r==0)
                    counts['adjacent_pair_motions']+=(s==r+1 or (r==0 and s==n-1))
                    digest.update(bytes([n,*[x+2 for x in a],r,s]))
    counts['case_digest']=digest.hexdigest()
    return counts


def constants_audit():
    # The proof imports only the classical analytic bounds 3 < pi < 22/7.
    lo,hi=Q(3),Q(22,7)
    margins={
        'strict_edge_gap':lo**2/6-Q(1,100),
        'normal_width_squared':lo**2/16-Q(3,50),
        'misalignment_squared':Q(1,256)-Q(1,300),
        'gradient_ratio':3-5*hi/6,
        'first_variation_angle':Q(5,16)-3*hi/32,
        'separation_contradiction':Q(11,16)-Q(5,16),
        'bingane_all_n_ge_32':Q(32**3)-100*hi**7/18,
    }
    for name,margin in margins.items():
        require(margin>0, 'failed margin: '+name)
    return {name:str(margin) for name,margin in margins.items()}


def add(u,v): return tuple(x+y for x,y in zip(u,v))
def sub(u,v): return tuple(x-y for x,y in zip(u,v))
def mul(a,u): return tuple(a*x for x in u)
def dot(u,v): return sum(x*y for x,y in zip(u,v))
def cross(u,v): return u[0]*v[1]-u[1]*v[0]
def rot90(u): return (-u[1],u[0])


def sqrt_rational(q):
    a,b=isqrt(q.numerator),isqrt(q.denominator)
    require(a*a==q.numerator and b*b==q.denominator,'not a rational square')
    return Q(a,b)


def half_edges(z):
    return [sub(z[i+1],z[i]) for i in range(len(z)-1)]+[sub(mul(-1,z[0]),z[-1])]


def validate_geometry(z,c):
    full=z+[mul(-1,p) for p in z]
    edges=[sub(full[(i+1)%len(full)],p) for i,p in enumerate(full)]
    require(all(dot(p,p)<=1 for p in full),'outside disk')
    # Strict supporting-edge inequalities independently establish convexity.
    for i,e in enumerate(edges):
        for j,p in enumerate(full):
            if j not in (i,(i+1)%len(full)):
                require(cross(e,sub(p,full[i]))>0,'not strictly convex')
    require(tuple(sum(cj*ej[k] for cj,ej in zip(c,half_edges(z)))
                  for k in range(2))==(0,0),'geometric closure')


def rational_fixtures():
    # Two interior half-vertices. This 3-4-5 triangle is not a local maximum.
    z=[(Q(3,5),Q(-4,5)),(Q(3,5),Q(0)),(Q(0),Q(4,5))]
    c=(-1,1,-1)
    validate_geometry(z,c)
    a=sign_coefficients(c)
    zz=list(z)
    zz[1]=add(z[1],(Q(1,50),Q(0)))
    zz[2]=add(z[2],(Q(1,50),Q(0)))
    validate_geometry(zz,c)
    e=half_edges(zz)
    require(dot(e[0],e[0])>Q(4,5)**2,'first length did not increase')
    require(dot(e[1],e[1])==1,'middle length changed')
    require(dot(e[2],e[2])==Q(31,50)**2,'last length')
    require(Q(4,5)+1+Q(31,50)>Q(12,5),'no perimeter improvement')

    # One interior half-vertex at the antipodal endpoint; all edge lengths
    # are rational, so the first variation is evaluated without radicals.
    z=[(Q(10,13),Q(0)),(Q(5,13),Q(12,13)),(Q(-5,13),Q(12,13))]
    c=(1,-1,1)
    validate_geometry(z,c)
    a=sign_coefficients(c)
    edges=half_edges(z)
    units=[mul(1/sqrt_rational(dot(e,e)),e) for e in edges]
    g0=mul(-1,add(units[-1],units[0]))
    g1=sub(units[0],units[1])
    derivative=dot(sub(g1,mul(Q(a[1],a[0]),g0)),rot90(z[1]))
    require(derivative==Q(-156,169),'incorrect first variation')
    # Check exact two-sided feasibility with rational circle rotation.
    for h in (Q(1,1000),Q(-1,1000)):
        co=(1-h*h)/(1+h*h); si=2*h/(1+h*h)
        moved=add(mul(co,z[1]),mul(si,rot90(z[1])))
        zz=list(z); zz[1]=moved
        zz[0]=sub(z[0],mul(Q(a[1],a[0]),sub(moved,z[1])))
        validate_geometry(zz,c)
        require(dot(zz[0],zz[0])<1,'interior endpoint left disk')
    return {'two_interior_new_perimeter_lower_bound':'121/50',
            'two_interior_original_perimeter':'12/5',
            'one_interior_angular_derivative':str(derivative),
            'rational_circle_curve_sides_checked':2}


def negative_controls():
    failures=0
    for f in (lambda:sign_coefficients((1,0,1)),
              lambda:sign_coefficients((1,-1)),
              lambda:check_motion((2,-2,2),(0,0,0)),
              lambda:check_motion((2,-2,2),(1,0,0)),
              lambda:sqrt_rational(Q(2)),
              lambda:validate_geometry([(Q(2),Q(0)),(Q(0),Q(1)),
                                        (Q(-1),Q(1))],(1,-1,1))):
        try: f()
        except ValueError: failures+=1
        else: raise ValueError('negative control accepted')
    return failures


def main():
    result={'scope':'exact supporting checks; universal theorem is proved in PROOF.md',
            'constants':constants_audit(),'codes':code_audit(),
            'geometric_fixtures':rational_fixtures(),
            'negative_controls_rejected':negative_controls()}
    output=json.dumps(result,sort_keys=True,indent=2)+'\n'
    expected=Path(__file__).with_name('expected.json')
    if expected.exists():
        require(output==expected.read_text(),'expected record mismatch')
    print(output,end='')


if __name__=='__main__':
    main()
