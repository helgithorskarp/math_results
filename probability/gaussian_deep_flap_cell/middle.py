#!/usr/bin/env python3
"""Exact reference-grid middle and source-peak computation. See PROOF.md."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from math import factorial
from pathlib import Path
import sys,json,time
from radial import X,Y,EPS,HERE,need
from direct_hinge import exp_neg,gaussian_constant,quadrature_error,density_histograms

def window_max(source, target, left, right):
    """Maximum of the upper adverse polygon on the WHOLE closed window."""
    need(0 <= left < right, 'invalid threshold window')
    need(sum(source.values()) == sum(target.values()), 'unequal site totals')
    need(all(isinstance(v, int) and v >= 0 and isinstance(n, int) and n > 0
             for hist in (source, target) for v, n in hist.items()),
         'invalid histogram')
    value = sum(n * max(v-left, 0) for v, n in source.items())
    value -= sum(n * max(v-left, 0) for v, n in target.items())
    best, arg = value, left
    slope = -sum(n for v, n in source.items() if v > left)
    slope += sum(n for v, n in target.items() if v > left)
    previous = left
    knots = sorted({v for v in source.keys() | target.keys()
                    if left < v <= right} | {right})
    for knot in knots:
        value += slope * (knot-previous)
        if value > best:
            best, arg = value, knot
        slope += source.get(knot, 0)-target.get(knot, 0)
        previous = knot
    return best, arg, len(knots)



def orbits(M):
    for i,j,k in combinations_with_replacement(range(M+1),3):
        div=1
        for n in Counter((i,j,k)).values():div*=factorial(n)
        base=(1<<sum(v>0 for v in (i,j,k)))*6//div
        if i==0:yield (i,j,k),base
        else:
            need(base%2==0,'tetrahedral orbit size')
            yield (i,j,k),base//2
            yield (-i,j,k),base//2

def histograms(h,M,bits):
    Q=1<<bits;den=16*Q*Q
    tables={a:[exp_neg((h*j-a)**2/2,bits) for j in range(-M,M+1)] for p in X+Y for a in p}
    atoms=[[tuple(tables[a] for a in p) for p in P] for P in [X,Y]]
    source=Counter();target=Counter();stream=sha256();num=0
    for point,mult in orbits(M):
        i,j,k=(a+M for a in point)
        top=sum(tx[i][1]*ty[j][1]*tz[k][1] for tx,ty,tz in atoms[0])
        bottom=sum(tx[i][0]*ty[j][0]*tz[k][0] for tx,ty,tz in atoms[1])
        fu=(top+den-1)//den;gl=bottom//den
        source[fu]+=mult;target[gl]+=mult;num+=1
        stream.update(f'{point},{mult},{fu},{gl}\n'.encode())
    need(sum(source.values())==sum(target.values())==(2*M+1)**3,'orbit completeness')
    return source,target,num,stream.hexdigest()

def controls():
    total=0
    for M,h in [(1,F(1,2)),(2,F(1,3)),(3,F(1,4))]:
        s,t,_,_=histograms(h,M,32)
        _,ss,*_=density_histograms(Counter(X),16,h,M,32)
        tt,*_=density_histograms(Counter(Y),16,h,M,32)
        need(s==ss and t==tt,'full entry-level orbit disagreement')
        total+=(2*M+1)**3
    return {'unquotiented_sites':total}

def calculate():
    start=time.monotonic();cc=controls();h=F(1,16);M=120;bits=48;Q=1<<bits
    s,t,n,digest=histograms(h,M,bits)
    mx,arg,knots=window_max(s,t,Q//512,9*Q//32)
    cl,cu=gaussian_constant(bits)
    poly=F(mx,Q)*h**3*(cl if mx<0 else cu)
    quad,tail=quadrature_error(h,F(6),bits)
    upper=poly+quad+tail+EPS
    need(upper<-F(1,128),'middle margin')
    peak=F(max(s),Q)+F(61,100)*(F(7,128)+EPS)
    need(peak<F(9,32),'source peak')
    need(F(exp_neg(F(18),bits)[1],Q)<F(max(s),Q),
         'outside-grid source peak bound')
    result={'status':'DEEP_FLAP_MIDDLE_AND_PEAK_PASS','controls':cc,'h':str(h),'M':M,'bits':bits,
        'orbits':n,'sites':(2*M+1)**3,'histogram_sha256':digest,'window':['1/512','9/32'],
        'knots':knots,'maximizing_threshold':str(F(arg,Q)),'reference_polygon_upper':str(poly),
        'quadrature_error':str(quad),'tail_error':str(tail),'cell_adverse_upper':str(upper),
        'source_peak_upper':str(peak)}
    return result
