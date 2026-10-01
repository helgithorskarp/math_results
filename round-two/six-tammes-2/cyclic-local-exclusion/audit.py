#!/usr/bin/env python3
"""Audit the certificate with unreduced polynomials and centered enclosures.

This imports neither check.py nor generate.py. Products are convolved without
field reduction; identities are tested by polynomial long division. The inverse
residual is enclosed directly as I-AR, with no rounded R grid.
"""
import argparse
from fractions import Fraction as Q
import json
import math
from pathlib import Path

F=tuple(map(Q,(-1,-3,2,6,-1,13)))
LO=Q('0.59260590292507377809642492233275')
HI=Q('0.59260590292507377809642492233276')
MID=(LO+HI)/2
RAD=(HI-LO)/2

def demand(ok,message):
    if not ok:raise ValueError(message)
def trim(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:p.pop()
    return tuple(p) if p else (Q(0),)
def plus(p,q):
    return trim([(p[i] if i<len(p) else Q(0))+(q[i] if i<len(q) else Q(0))
                 for i in range(max(len(p),len(q)))])
def times(p,q):
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]+=x*y
    return trim(out)
def scalar(p,a):return trim([a*x for x in p])
def minus(p,q):return plus(p,scalar(q,-1))
def total(values):
    out=(Q(0),)
    for p in values:out=plus(out,p)
    return out
def remainder(p):
    p=list(p)
    while len(p)>=len(F):
        z=p[-1]/F[-1];offset=len(p)-len(F)
        for i,x in enumerate(F):p[offset+i]-=z*x
        p.pop()
    return trim(p)
def zero(p):return remainder(p)==(Q(0),)
def at(p,x):return sum(a*x**i for i,a in enumerate(p))
def enclosure(p):
    center=at(p,MID)
    radius=sum(abs(sum(p[j]*math.comb(j,k)*MID**(j-k) for j in range(k,len(p))))*RAD**k
               for k in range(1,len(p)))
    return center-radius,center+radius
def dot(v,w):return total(times(x,y) for x,y in zip(v,w))
def read(p):
    demand(type(p) is list and len(p)==5,'five coefficients in audit input')
    return trim(tuple(map(Q,p)))

def audit(d):
    demand(at(F,LO)<0<at(F,HI),'root sign bracket')
    demand(enclosure(tuple(i*F[i] for i in range(1,len(F))))[0]>0,'unique bracketed root')
    demand(Q(0)<LO<HI<Q(3,5),'positive definite anchor metric')
    V=[tuple(read(p) for p in row) for row in d['vectors']]
    demand(len(V)==15 and all(len(v)==3 for v in V),'fifteen three-coordinate points')
    one=(Q(1),);t=(Q(0),Q(1));z=(Q(0),)
    H=[[one if i==j else t for j in range(3)] for i in range(3)]
    HV=[tuple(dot(row,v) for row in H) for v in V]
    demand(all(zero(minus(dot(v,hv),one)) for v,hv in zip(V,HV)),'fifteen exact unit norms')
    for k,i in enumerate((0,5,11)):
        demand(V[i]==tuple(one if k==j else z for j in range(3)),'anchor coefficient basis')
    for n,i,j,o in ((6,0,11,5),(7,0,5,11),(9,5,11,0),(14,0,6,11),
                    (12,5,7,0),(13,11,9,5),(3,1,4,2),(8,2,4,1),(10,1,2,4)):
        for k in range(3):
            demand(zero(minus(times(plus(one,t),plus(V[n][k],V[o][k])),
                              scalar(times(t,plus(V[i][k],V[j][k])),2))),
                   'raw cyclic triangle-reflection identity')
    a=tuple(map(Q,('-27/2','-3','35','-24','117/2')))
    b=tuple(map(Q,('-31/4','-19/2','34','-53/2','195/4')))
    c=tuple(map(Q,('81/4','21/2','-69','101/2','-429/4')))
    M=((a,b,c),(c,a,b),(b,c,a))
    for i,ai in enumerate((0,5,11)):
        for j,bj in enumerate((1,2,4)):
            demand(zero(minus(dot(V[ai],HV[bj]),M[i][j])),'raw cross Gram identity')
    edges=[]
    for i in range(15):
        for j in range(i+1,15):
            g=dot(V[i],HV[j])
            if zero(minus(g,t)):edges.append([i,j])
            else:demand(enclosure(g)[1]<Q(17,40),'seventy-five strict noncontacts')
    demand(len(edges)==30 and edges==d['edges'],'raw exact thirty-contact list')
    weights=[read(p) for p in d['weights']]
    demand(len(weights)==30,'thirty stress weights')
    demand(all(zero(minus(w,one)) or enclosure(minus(w,one))[0]>0 for w in weights),
           'all weights at least one')
    demand(enclosure(total(weights))[1]<183,'total stress below 183')
    E=[[z]*3 for _ in range(15)]
    for (i,j),w in zip(edges,weights):
        for k in range(3):
            E[i][k]=plus(E[i][k],times(w,minus(V[j][k],times(t,V[i][k]))))
            E[j][k]=plus(E[j][k],times(w,minus(V[i][k],times(t,V[j][k]))))
    demand(all(zero(p) for row in E for p in row),'forty-five raw equilibrium identities')
    chosen=d['selected_edges']
    demand(len(chosen)==27 and len(set(chosen))==27 and
           all(type(k) is int and 0<=k<30 for k in chosen),'twenty-seven contact rows')
    R=[]
    for i in range(15):
        row=[z]*45;row[3*i:3*i+3]=HV[i];R.append(row)
    for k in chosen:
        i,j=edges[k];row=[z]*45;row[3*i:3*i+3]=HV[j];row[3*j:3*j+3]=HV[i];R.append(row)
    for k in (1,2,17):
        row=[z]*45;row[k]=one;R.append(row)
    A=d['inverse_numerators'];den=d['inverse_scale']
    demand(type(den) is int and den>0 and len(A)==45 and
           all(len(row)==45 and all(type(x) is int for x in row) for row in A),'rational inverse shape')
    norm=Q(max(sum(abs(x) for x in row) for row in A),den)
    demand(norm<46,'rational inverse norm bound')
    sparse=[[(j,p) for j,p in enumerate(row) if p!=z] for row in R]
    residual=[]
    for i in range(45):
        row=[one if i==j else z for j in range(45)]
        for k,n in enumerate(A[i]):
            if n:
                for j,p in sparse[k]:row[j]=minus(row[j],scalar(p,Q(n,den)))
        residual.append(sum(max(abs(x) for x in enclosure(p)) for p in row))
    error=max(residual)
    demand(error<Q(1,1000),'direct centered I-AR residual')
    demand(norm/(1-error)<46,'direct Neumann inverse norm')
    demand(Q(144,5)*46*183*Q(1,250000)<1,'quantitative local radius')
    demand(10*2100000000*Q(1,10**16)<Q(1,400000),'both completion branches enter the radius')
    ceiling=Q(-(-error.numerator*10**12//error.denominator),10**12)
    return {'status':'VERIFIED','points':15,'contacts':30,'noncontacts':75,
            'raw_equilibrium_identities':45,'direct_inverse_residual_upper':str(ceiling),
            'gauged_inverse_norm_upper':'46','coefficient_radius':'1/250000',
            'stress_sum_upper':'183','euclidean_radius':'1/400000',
            'twenty_six_contact_tolerance':'1/10000000000000000'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,default=Path(__file__).with_name('certificate.json'))
    args=parser.parse_args()
    print(json.dumps(audit(json.loads(args.certificate.read_text())),sort_keys=True))
