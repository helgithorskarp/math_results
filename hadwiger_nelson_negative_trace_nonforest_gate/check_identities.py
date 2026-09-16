#!/usr/bin/env python3
"""Exact algebra checks supporting PROOF.md, not a placement census."""
from fractions import Fraction as Q
from pathlib import Path
import json

NAMES = ('A','B','H','r','s','d','db','e','eb','u','c','T','J','dx','dy','vx','vy')
N = len(NAMES)
class L:
    def __init__(self, terms):
        self.t = {tuple(k):Q(v) for k,v in terms.items() if v}
        if any(len(k)!=N for k in self.t): raise ValueError('exponent length')
    @staticmethod
    def constant(v): return L({(0,)*N:Q(v)})
    def __add__(self, other):
        if not isinstance(other,L): other=L.constant(other)
        out=dict(self.t)
        for k,v in other.t.items():out[k]=out.get(k,0)+v
        return L(out)
    __radd__=__add__
    def __neg__(self):return L({k:-v for k,v in self.t.items()})
    def __sub__(self,o):return self+-coerce(o)
    def __rsub__(self,o):return coerce(o)+-self
    def __mul__(self,other):
        other=coerce(other); out={}
        for k,v in self.t.items():
            for j,w in other.t.items():
                h=tuple(a+b for a,b in zip(k,j));out[h]=out.get(h,0)+v*w
        return L(out)
    __rmul__=__mul__
    def __pow__(self,n):
        if n<0:
            if len(self.t)!=1:raise ValueError('Only monomials invertible here')
            (k,v),=self.t.items()
            return L({tuple(n*a for a in k):v**n})
        ans=L.constant(1)
        for _ in range(n):ans=ans*self
        return ans
    def __truediv__(self,o):return self*coerce(o)**-1
    def evaluate(self, values):
        return sum((v*product(Q(values[name])**power for name,power in zip(NAMES,k) if power)
                    for k,v in self.t.items()),Q(0))
def coerce(x):return x if isinstance(x,L) else L.constant(x)
def product(xs):
    p=Q(1)
    for x in xs:p*=x
    return p
def variable(name):
    k=[0]*N;k[NAMES.index(name)]=1;return L({tuple(k):1})
V={n:variable(n) for n in NAMES}
A,B,H,r,s,d,db,e,eb,u,c,T,J,dx,dy,vx,vy=(V[n] for n in NAMES)
checks=[]
def zero(label,expr):
    if expr.t:raise ValueError('identity failed: '+label)
    checks.append(label)
def form(x,y):return A*x*x+B*y*y-2*H*x*y

def run():
    dot=dx*vx+dy*vy
    plus=(dx+vx)**2+(dy+vy)**2
    minus=(dx-vx)**2+(dy-vy)**2
    zero('diagonal norm difference',plus-minus-4*dot)
    zero('diagonal norm sum',plus+minus-2*(dx*dx+dy*dy+vx*vx+vy*vy))
    zero('perpendicularity times u',(db*u*e+d*eb/u)*u-(db*e*u*u+d*eb))
    W=-d*eb/(db*e)
    zero('monic trace-zero quadratic',db*e*(u*u-W)-(db*e*u*u+d*eb))
    rp=2*H*s/A-r
    sp=2*H*rp/B-s
    zero('fixed root exchange',form(rp,s)-form(r,s))
    zero('moving root exchange',form(r,2*H*r/B-s)-form(r,s))
    m00=L.constant(-1);m01=2*H/A;m10=-2*H/B;m11=4*H*H/(A*B)-1
    zero('determinant one',m00*m11-m01*m10-1)
    zero('matrix first coordinate',m00*r+m01*s-rp)
    zero('matrix second coordinate',m10*r+m11*s-sp)
    zero('positive form invariant',form(rp,sp)-form(r,s))
    zero('matrix trace',m00+m11-(4*H*H/(A*B)-2))
    # AB=c*conjugate(c)=J*c^2 and 2H=c*T; all denominators nonzero.
    trace_sub=4*(c*T/2)**2/(J*c*c)-2
    zero('trace equals T squared over J minus two',trace_sub-(T*T/J-2))
    # Rational calibration of the root-exchange matrix; no universal inference.
    def matrix(a,b,h):return ((Q(-1),2*h/a),(-2*h/b,4*h*h/(a*b)-1))
    def mm(x,y):return tuple(tuple(sum(x[i][k]*y[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    ident=((Q(1),Q(0)),(Q(0),Q(1)))
    m=matrix(Q(1),Q(1),Q(1,2))
    if mm(mm(m,m),m)!=ident or m[0][0]+m[1][1]!=-1:raise ValueError('order-three control')
    m0=matrix(Q(1),Q(1),Q(0))
    if mm(m0,m0)!=ident or m0[0][0]+m0[1][1]!=-2:raise ValueError('trace-zero boundary')
    mn=matrix(Q(1),Q(1),Q(1,4))
    if mn[0][0]+mn[1][1]!=Q(-7,4):raise ValueError('negative-trace control')
    def v2(x):
        x=Q(x)
        if not x:raise ValueError('zero requires infinity')
        n=abs(x.numerator);d=x.denominator;a=b=0
        while n%2==0:n//=2;a+=1
        while d%2==0:d//=2;b+=1
        return a-b
    if v2(Q(-7,4))!=-2:raise ValueError('valuation control')
    for k in range(1,13):
        t=Q(1,2**k)
        if v2(t*t-2)!=-2*k:raise ValueError('negative valuation calibration')
    # A nonzero corrupted identity must be detected even under python -O.
    bad=trace_sub-(T*T/J+2)
    if not bad.t or bad.evaluate({'T':Q(1,2),'J':1})!=-4:raise ValueError('corruption control')
    try: _=(A+B)**-1
    except ValueError:pass
    else:raise ValueError('invalid Laurent inversion accepted')
    return {'exact_symbolic_identities':checks,'identity_count':len(checks),
            'rational_controls':['order-three matrix','trace-zero order-two boundary','negative trace -7/4'],
            'negative_rational_valuation_controls':12,'rejection_controls':2,
            'universal_proof':'PROOF.md; not inferred from finite controls',
            'placements_enumerated':0,'new_physical_graph':False,'solver_queries':0}

if __name__=='__main__':
    actual=run();expected_path=Path(__file__).with_name('EXPECTED.json')
    if not expected_path.exists():raise FileNotFoundError('EXPECTED.json')
    if json.loads(expected_path.read_text())!=actual:raise ValueError('unexpected output')
    print(json.dumps(actual,indent=2,sort_keys=True))
