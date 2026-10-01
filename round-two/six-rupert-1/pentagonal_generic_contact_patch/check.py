#!/usr/bin/env python3
"""Exact contact supports and uniform stress; Python 3.11+, stdlib only.

This checker does not search for a hull, choose contacts, or use floating
point decisions. It checks six submitted contacts on all 92 generator
points, then proves positive equilibrium and rank throughout rational
parameter and receiving boxes. The written Cayley bridge is in PROOF.md.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys

HERE=Path(__file__).resolve().parent
PREREQUISITE=HERE.parent/'pentagonal_minimum_diameter/verify.py'
PREREQUISITE_SHA='12c94ea3ab9d7bc42e2086dbb5fbb9154306d6fd7095a8be4b25bb44fefd5339'

def require(ok,message):
    if not ok: raise ValueError(message)

require(hashlib.sha256(PREREQUISITE.read_bytes()).hexdigest()==PREREQUISITE_SHA,
        'named-family prerequisite source hash')
spec=importlib.util.spec_from_file_location('pentagonal_diameter_prerequisite',PREREQUISITE)
V=importlib.util.module_from_spec(spec);sys.modules[spec.name]=V;spec.loader.exec_module(V)
Q,I=V.Q,V.I

def dot(a,b): return sum((x*y for x,y in zip(a,b)),0)
def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def scale(c,a): return tuple(c*x for x in a)
def abs_bound(x):
    x=I.coerce(x);return max(abs(x.lo),abs(x.hi))
def matvec(A,x): return tuple(dot(row,x) for row in A)

def inverse(A):
    n=len(A);require(all(len(row)==n for row in A),'square correction matrix')
    work=[list(row)+[Q(int(i==j)) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        choices=[i for i in range(j,n) if work[i][j]!=V.Z]
        require(bool(choices),'singular reference correction matrix')
        i=choices[0];work[i],work[j]=work[j],work[i]
        pivot=work[j][j];work[j]=[x/pivot for x in work[j]]
        for i in range(n):
            if i==j:continue
            multiplier=work[i][j]
            work[i]=[x-multiplier*y for x,y in zip(work[i],work[j])]
    out=tuple(tuple(row[n:]) for row in work)
    identity=tuple(tuple(Q(int(i==j)) for j in range(n)) for i in range(n))
    require(V.mm(A,out)==identity and V.mm(out,A)==identity,'two-sided exact inverse identity')
    return out

def qpoint(v,parameters): return tuple(dot(coordinate,parameters) for coordinate in v)
def ipoint(v,parameters): return tuple(V.linterval(coordinate,parameters) for coordinate in v)
def row(point,m,E,Fv): return cross(point,m)+(dot(m,E),dot(m,Fv))

@lru_cache(maxsize=1)
def generator_data():
    # Immutable exact generators. Multiple damage controls reuse only
    # these unchanged prerequisites; every submitted contact is rechecked.
    mats=tuple(V.group());return mats,tuple(V.vertices(mats))

def check(certificate,delta=F(1,1000),eta=F(1,10**6)):
    require(certificate.get('schema')=='pentagonal-generic-contact-v1','certificate schema')
    require(certificate.get('base_receiver')==[1,2,3],'base receiving direction')
    basis=certificate.get('translation_basis')
    require(basis==[[0,3,-2],[-13,2,3]],'fixed translation basis')
    E,Fv=(tuple(Q(x) for x in v) for v in basis)
    Eint,Fint=(tuple(I(x,x) for x in v) for v in basis)
    require(delta>0 and eta>0,'positive box widths')
    require(14-3*delta>0,'projected fixed basis spans every receiving plane')
    mats,points=generator_data()
    _,named,_=V.named_parameters()
    p0=tuple((p.lo+p.hi)/2 for p in V.BOX)
    P0=tuple(qpoint(v,p0) for v in points)
    Pi=tuple(ipoint(v,V.BOX) for v in points)
    require(all(sum(x.square().hi for x in p)<4 for p in Pi),'uniform original-point radius < 2')
    r0=tuple(Q(x) for x in (1,2,3))
    ri=(I(1-delta,1+delta),I(2-delta,2+delta),I(3,3))
    contacts=certificate.get('contacts');require(isinstance(contacts,list) and len(contacts)==6,'six contact rows')
    correction=certificate.get('correction_rows')
    require(isinstance(correction,list) and len(correction)==len(set(correction))==5 and all(type(i)==int and 0<=i<6 for i in correction),'five distinct correction rows')
    nums=certificate.get('fixed_weight_numerators');den=certificate.get('fixed_weight_denominator')
    require(type(den)==int and den>0 and isinstance(nums,list) and len(nums)==6,'fixed-weight encoding')
    require(all(nums[i] is None if i in correction else type(nums[i])==int and nums[i]>0 for i in range(6)),
            'one positive fixed weight; only correction weights omitted')
    reference_rows=[];interval_rows=[];interval_heights=[];strict_gaps=[]
    maximum_normal_squared=F(0)
    for contact in contacts:
        require(isinstance(contact,list) and len(contact)==4 and all(type(x)==int for x in contact),'integer contact encoding')
        a,b,v,k=contact
        require(0<=a<92 and 0<=b<92 and a!=b and v in (a,b) and -12<=k<=12,'original contact labels and normal scale')
        gamma=F(2)**k
        m0=scale(gamma,cross(sub(P0[b],P0[a]),r0))
        mi=scale(gamma,cross(sub(Pi[b],Pi[a]),ri))
        h0=dot(m0,P0[v]);hi=dot(mi,Pi[v])
        require(h0.sign()>0 and hi.lo>0,'positive original support height')
        require(dot(m0,sub(P0[b],P0[a]))==V.Z and dot(m0,r0)==V.Z,'exact reference contact and receiving-plane identities')
        # For variable p and r, m=gamma*(P_b-P_a) cross r. Thus
        # m.r=0 and m.(P_b-P_a)=0 identically, including the two endpoints.
        for j in range(92):
            if j in (a,b):continue
            require(dot(m0,sub(P0[v],P0[j])).sign()>0,'strict reference original support')
            gap=dot(mi,sub(Pi[v],Pi[j])).lo
            require(gap>0,f'uniform original support gap at contact {contact}, point {j}')
            strict_gaps.append(gap)
        normal_squared=sum(x.square().hi for x in mi)
        require(normal_squared<4,'uniform selected normal length < 2')
        maximum_normal_squared=max(maximum_normal_squared,normal_squared)
        reference_rows.append(row(P0[v],m0,E,Fv))
        interval_rows.append(row(Pi[v],mi,Eint,Fint))
        interval_heights.append(hi)
    A0=tuple(tuple(reference_rows[j][i] for j in correction) for i in range(5))
    inv=inverse(A0)
    fixed=next(i for i in range(6) if i not in correction)
    weights=[V.Z for _ in range(6)];weights[fixed]=Q(F(nums[fixed],den))
    rhs=scale(-weights[fixed],reference_rows[fixed])
    solution=matvec(inv,rhs)
    for j,w in zip(correction,solution):weights[j]=w
    require(all(w.sign()>0 for w in weights),'positive reference stress')
    require(all(dot(weights,[v[i] for v in reference_rows])==V.Z for i in range(5)),
            'five exact reference equilibrium identities')
    weight_intervals=[V.qi(w) for w in weights]
    L0=max(sum(abs_bound(V.qi(x)) for x in row) for row in inv)
    delta_rows=tuple(tuple(abs_bound(current-V.qi(old)) for current,old in zip(ir,qr)) for ir,qr in zip(interval_rows,reference_rows))
    matrix_error=max(sum(delta_rows[j][i] for j in correction) for i in range(5))
    residual_error=max(sum(abs_bound(w)*delta_rows[j][i] for j,w in enumerate(weight_intervals)) for i in range(5))
    require(L0*matrix_error<F(1,2),'uniform correction inverse Neumann gate')
    L=2*L0;drift=L*residual_error
    current_weights=[I(w.lo-drift,w.hi+drift) if j in correction else w for j,w in enumerate(weight_intervals)]
    require(all(w.lo>0 for w in current_weights),'uniform positive stress after correction')
    # w(p,r) equals the reference weights except that correction weights
    # change by -A(p,r)^(-1) times the five-dimensional reference residual.
    w_lower=min(w.lo for w in current_weights)
    W_upper=sum(w.hi for w in current_weights)
    H_lower=sum(w.lo*h.lo for w,h in zip(current_weights,interval_heights))
    require(H_lower>0,'uniform positive weighted support height')
    # ||R(c)-I-2[c]_x|| <= 3|c|^2 for |c|<=1/2.
    # With |P|<2 and |m|<2 the support remainder is <12|c|^2;
    # use 16. Stress first yields lambda<=2, then all row values
    # are bounded by K|c|^2. Five independent rows control motion.
    remainder=F(16)
    K=2*remainder*max(F(1),W_upper/w_lower)
    require(3*eta*eta<F(1,4),'Cayley remainder radius gate')
    require(6*remainder*W_upper*eta*eta<H_lower,'scale absorption gate')
    require(F(15,2)*L*K*eta<1,'nonlinear Cayley contraction gate')
    # Reader-facing simple rational bounds; all are independently checked
    # against the computed interval quantities rather than rounded floats.
    require(min(strict_gaps)>F(9,1000),'reported support gap lower bound')
    require(maximum_normal_squared<2,'reported normal squared upper bound')
    require(L0<F(21,2) and L<21,'reported inverse upper bounds')
    require(L0*matrix_error<F(1,4),'reported Neumann upper bound')
    require(drift<F(9,125),'reported stress drift upper bound')
    require(w_lower>F(1,60) and W_upper<F(7,5) and H_lower>F(3,5),'reported uniform stress bounds')
    require(K<2700,'reported row coercivity upper bound')
    require(F(15,2)*21*2700*eta<1,'reported simple Cayley contraction gate')
    return {
       'agent':'six-rupert-1','role':'researcher',
       'status':'EXACT_UNIFORM_CONTACT_STRESS_AND_CAYLEY_GATES_PASSED',
       'target':'pentagonal hexecontahedron parameter hull; proper motions near a body symmetry',
       'receiving_raw_direction':'(1+s,2+z,3)',
       'receiving_coordinate_half_width':str(delta),'relative_cayley_infinity_radius':str(eta),
       'parameter_box':[[str(p.lo),str(p.hi)] for p in V.BOX],
       'named_parameters_strictly_inside_box':True,'proper_body_group_order':len(mats),
       'original_points':len(points),'contacts':contacts,'correction_rows':correction,
       'strict_original_support_comparisons':len(strict_gaps),
       'minimum_strict_original_gap_lower':'9/1000',
       'normal_squared_upper':'2',
       'reference_inverse_infinity_upper':'21/2',
       'neumann_product_upper':'1/4','uniform_inverse_infinity_upper':'21',
       'stress_weight_drift_upper':'9/125','stress_weight_lower':'1/60',
       'stress_weight_sum_upper':'7/5','weighted_height_lower':'3/5',
       'first_variation_coercivity_K_upper':'2700',
       'cayley_contraction_product_upper':str(F(15,2)*21*2700*eta),
       'reference_equilibrium_components_exactly_zero':5,
       'two_sided_reference_inverse_verified':True,
       'closed_fit_scope':'lambda>=1, arbitrary actual receiving-plane translation, Q=R(c)G with |c|_infinity<=eta',
       'conclusion':'lambda=1, Q=G, translation=0; full Rupert property remains open',
       'trust_boundary':'Python integers/Fraction/Q(phi), rational intervals and the written unformalized Cayley bridge; author checked, no independent review claimed',
       'prerequisite_sha256':PREREQUISITE_SHA,
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    parser.add_argument('--delta',type=F,default=F(1,1000))
    parser.add_argument('--eta',type=F,default=F(1,10**6))
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=check(json.loads(args.certificate.read_text()),args.delta,args.eta)
    result['certificate_sha256']=hashlib.sha256(args.certificate.read_bytes()).hexdigest()
    if args.output:args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else: print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
