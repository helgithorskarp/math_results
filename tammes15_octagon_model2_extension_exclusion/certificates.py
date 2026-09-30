"""Exact necessary affine rows and rational cancellation certificates.

No optimizer or floating arithmetic is used by this verifier.
"""
from fractions import Fraction as Q
from functools import lru_cache
import polynomial as M
from model import forms

def envelope(p):
    a=[Q(0)]*5;error=Q(0);constant=p.get(M.ZERO,Q(0))
    for e,c in p.items():
        degree=sum(e)
        if degree==1:a[e.index(1)]=c
        elif degree>=2:error+=abs(c)
    return tuple(a),error-constant

class Rows:
    def __init__(self,lo,hi):
        self.lo=lo;self.hi=hi;self.forms=forms(2)

    @lru_cache(maxsize=4096)
    def core(self,cell):
        d,i,j=cell;h=Q(8,2**d)
        t=M.variable(0,(self.lo+self.hi)/2,(self.hi-self.lo)/2)
        u=M.variable(1,-4+h*(i+Q(1,2)),h/2)
        v=M.variable(2,-4+h*(j+Q(1,2)),h/2)
        square=M.add(M.mul(u,u),M.mul(v,v));cross=M.mul(u,v)
        def evaluate(p):
            result={}
            for c in reversed(p):result=M.add(M.mul(result,t),M.constant(c))
            return result
        result=[]
        for row in self.forms:
            f,l,m,a,b=(evaluate(p) for p in row)
            p=M.add(f,M.add(M.mul(l,u),M.add(M.mul(m,v),
                    M.add(M.mul(a,square),M.mul(b,cross)))))
            result.append(envelope(p))
        return tuple(result)

    def single(self,cell):
        rows=list(self.core(tuple(cell)))
        for i in range(3):
            for sign in (-1,1):
                a=[Q(0)]*5;a[i]=sign;rows.append((tuple(a),Q(1)))
        return rows

    def pair(self,left,right):
        rows=list(self.core(tuple(left)))
        for a,b in self.core(tuple(right)):
            rows.append(((a[0],0,0,a[1],a[2]),b))
        rows.append(envelope(M.polynomial(left,right,self.lo,self.hi)))
        for i in range(5):
            for sign in (-1,1):
                a=[Q(0)]*5;a[i]=sign;rows.append((tuple(a),Q(1)))
        return rows

def verify_dual(rows,certificate):
    support=certificate['support'];weights=[Q(w) for w in certificate['weights']]
    if not support or len(support)!=len(set(support)) or len(weights)!=len(support):
        raise ValueError('unique nonempty dual support')
    if any(type(k) is not int or not 0<=k<len(rows) for k in support):
        raise ValueError('canonical row indices')
    if any(w<0 for w in weights) or sum(weights)!=1:
        raise ValueError('nonnegative normalized rational weights')
    if any(sum(w*Q(rows[k][0][i]) for k,w in zip(support,weights)) for i in range(5)):
        raise ValueError('uncancelled affine coefficient')
    gap=sum(w*Q(rows[k][1]) for k,w in zip(support,weights))
    if gap>=0 or gap!=Q(certificate['negative_rhs']):
        raise ValueError('strict negative rational RHS')
    return gap
