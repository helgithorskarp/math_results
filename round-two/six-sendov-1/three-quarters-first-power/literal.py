"""Standalone CLOSED[29/40,3/4] exact literal kernels.
Own ab3798362ba9a701f68923aad5af2ed7dc608863 method provenance only.
No ancestor numerical exclusions, discovery records or peer/reviewer runtime inputs.
Ordinary/unformalized and independently unreviewed; full argument in PROOF.md.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import comb
from pathlib import Path
import datetime
import json
import resource
import time


Z=(Q(0),Q(0)); ONE=(Q(1),Q(0)); A=Q(29,40); B=1-A*A
EPS=Q(1,10000); M=1/(1+A)
HERE=Path(__file__).resolve().parent


def require(ok,message):
    if not ok:raise ValueError(message)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def scale(a,c):return a[0]*c,a[1]*c
def multiply(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def norm2(a):return a[0]*a[0]+a[1]*a[1]
def inverse(a):return scale((a[0],-a[1]),1/norm2(a))
def poly_multiply(a,b):
    result=[Z]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):result[i+j]=add(result[i+j],multiply(x,y))
    return result
def evaluate(a,x):
    out=Z
    for coefficient in reversed(a):out=add(multiply(out,(x,Q(0))),coefficient)
    return out
def product(items):
    out=ONE
    for x in items:out=multiply(out,x)
    return out
def integral(coeff,weight=0):
    out=Z
    for k,x in enumerate(coeff):out=add(out,scale(x,Q(1,k+weight+1)))
    return out


def channel_coefficients(q,kind,omit=None):
    coefficients=[ONE]
    for k,x in enumerate(q):
        if k==omit:continue
        coefficients=poly_multiply(coefficients,
            [(A,Q(0)),scale(x,B)] if kind=='J' else [ONE,scale(x,-A)])
    return coefficients


def channel(q,kind,omit=None):
    coeff=channel_coefficients(q,kind,omit)
    if omit is None:
        return integral(coeff) if kind=='J' else scale(integral(coeff),9)
    return scale(integral(coeff,1),B if kind=='J' else -9*A)


def primitive_channels(q,damage=''):
    critical=[add((A,Q(0)),scale(inverse(x),-1)) for x in q]
    if damage=='critical-location-sign':critical[-1]=add((A,Q(0)),inverse(q[-1]))
    derivative=[ONE]
    for z in critical:derivative=poly_multiply(derivative,[scale(z,-1),ONE])
    derivative=[scale(x,8 if damage=='monic-leading-factor-eight' else 9) for x in derivative]
    p=[Z]+[scale(x,Q(1,k+1)) for k,x in enumerate(derivative)]
    p[0]=scale(evaluate(p,A),-1)
    require(evaluate(p,A)==Z and p[-1]==ONE and len(p)==10,
            'whole monic ninth-degree primitive with marked zero')
    P=product(q)
    O=scale(multiply(P,evaluate(p,0)),-1/A)
    if damage=='primitive-factor-eight':O=scale(O,Q(8,9))
    J=scale(multiply(P,evaluate(p,1/A)),A**9/(9*B))
    if damage=='primitive-a-power':J=scale(J,1/A)
    native=[]
    for kind,low,slope,factor in (('O',A,-A,scale(P,Q(1,9))),
                                  ('J',A,B/A,scale(P,A**8/9))):
        composed=[]
        for k in range(9):
            coefficient=Z
            for j in range(k,9):
                coefficient=add(coefficient,scale(derivative[j],comb(j,k)*low**(j-k)*slope**k))
            composed.append(multiply(factor,coefficient))
        if damage=='channel-drop-last-coefficient':composed[-1]=Z
        require(composed==channel_coefficients(q,kind),
                'ALL nine affine-derivative versus factor-channel coefficients')
        native.append(dict(channel=kind,all_affine_derivative_coefficients=composed))
    return O,J,p,critical,native


def compute(damage='',endpoint=Q(3,4)):
    global A,B,M
    A=Q(endpoint);B=1-A*A;M=1/(1+A)
    require(A in (Q(29,40),Q(3,4)), 'both closed literal marked endpoints')
    phases=[ONE]*8
    balanced=[(Q(4,5),Q(3,5))]*4+[(Q(4,5),Q(-3,5))]*4
    near=[(Q(21,29),Q(20,29))]*4+[(Q(21,29),Q(-20,29))]*4
    common=[(Q(21,29),Q(20,29))]*8
    spiked=[1/A]+[(8-1/A)/7]*7
    fixtures=[('real', [Q(1)]*8,phases),('balanced',[Q(1)]*8,balanced),
              ('near-energy',[Q(1)]*8,near),('common-imaginary',[Q(1)]*8,common),
              ('removed-slot-square-equality',spiked,phases),('spiked-complex',spiked,balanced),
              ('old-entry-obstruction',[Q(241,80)]+[Q(57,80)]*7,phases)]
    records=[];points=0;gradients=0
    R=8+EPS-7*M;u_minus=Q(113,160)-EPS/8; e_plus=Q(47,10)+2*(R+1)*EPS
    for name,radii,units in fixtures:
        require(sum(radii,Q(0))==8 and all(r>=M for r in radii),'full clipped mass and floor')
        require(all(norm2(z)==1 for z in units),'exact Gaussian unit phases')
        prime=[scale(z,r) for z,r in zip(units,radii)]
        increments=[EPS*(r-M)/(8-(7 if damage=='clip-wrong-denominator' else 8)*M) for r in radii]
        original=[scale(z,r+h) for z,r,h in zip(units,radii,increments)]
        require(sum(increments,Q(0))==EPS,'whole l1 clipping displacement')
        for r,h in zip(radii,increments):
            require(EPS*(r+h-M)/(8+EPS-8*M)==h,'literal original clipping denominator')
        Eprime=sum((norm2(add(x,scale(ONE,-1))) for x in prime),Q(0))
        require(Eprime<Q(47,10),'genuine clipped energy premise')
        Os,Js=channel(prime,'O'),channel(prime,'J')
        if name=='old-entry-obstruction' and A==Q(3,4):
            require(Eprime==Q(3703,800) and Js==(Q(7206091113173168600293617,7205759403792793600000000),Q(0)),
                    'exact old J-only energy entry obstruction')
            require(Os[1]==0 and Os[0]>product(prime)[0],
                    'formal critical tuple violates actual original origin channel')
        Oo,Jo=channel(original,'O'),channel(original,'J')
        require(norm2(add(Oo,scale(Os,-1)))<(Q(5,4)*EPS)**2,
                'literal full origin continuity')
        require(norm2(add(Jo,scale(Js,-1)))<(Q(2,3)*EPS)**2,
                'literal full polar continuity')
        checks=[]
        for v in (Q(0),Q(1,2),Q(1)):
            q=[scale(z,r+v*h) for z,r,h in zip(units,radii,increments)]
            O,J,p,critical,native=primitive_channels(q,damage)
            require(O==channel(q,'O') and J==channel(q,'J'),
                    'full original-primitive and normalized channel values')
            mean=sum((x[0] for x in q),Q(0))/8
            energy=sum((norm2(add(x,scale(ONE,-1))) for x in q),Q(0))
            require(mean>=u_minus and energy<=e_plus,'literal coupled path enclosure')
            grad=[]
            for slot in range(8):
                go,gj=channel(q,'O',slot),channel(q,'J',slot)
                if damage=='gradient-missing-factor-nine':go=scale(go,Q(8,9))
                shifted=list(q);shifted[slot]=add(shifted[slot],ONE)
                require(add(channel(shifted,'O'),scale(O,-1))==go and
                        add(channel(shifted,'J'),scale(J,-1))==gj,
                        'all slot derivatives by exact full multilinear differences')
                require(norm2(go)<Q(5,4)**2 and norm2(gj)<Q(2,3)**2,
                        'all literal slot gradient controls')
                grad.append(dict(slot=slot,O=go,J=gj));gradients+=2
            checks.append(dict(v=v,mean=mean,energy=energy,O=O,J=J,
                              all_ten_primitive_coefficients=p,all_eight_critical_slots=critical,
                              both_full_affine_derivative_representations=native,
                              all_slot_gradients=grad));points+=1
        require(scale(Os,Q(8,9))!=Os and scale(Js,1/A)!=Js,
                'meaningful wrong ninth-factor and polar a-power controls')
        records.append(dict(name=name,all_clipped_radii=radii,all_unit_phases=units,
            all_radial_displacements=increments,Eprime=Eprime,
            Oprime=Os,Jprime=Js,Ooriginal=Oo,Joriginal=Jo,complete_point_controls=checks))
    def clean(x):
        if isinstance(x,Q):return str(x)
        if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)):return [clean(v) for v in x]
        return x
    record=clean(dict(agent='six-sendov-1',role='researcher',all_fixtures=records,
        fixtures_are_not_asserted_disk_rooted_original_polynomials=True,
        finite_point_checks_are_controls_not_a_continuum_proof=True,
        formalized=False,independently_reviewed=False))
    return record

DAMAGES=('critical-location-sign','monic-leading-factor-eight','primitive-factor-eight','primitive-a-power','channel-drop-last-coefficient','gradient-missing-factor-nine','clip-wrong-denominator')
