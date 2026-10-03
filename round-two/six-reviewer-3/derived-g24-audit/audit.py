#!/usr/bin/env python3
"""Independent reflection reconstruction and dual-coordinate Sturm cap audit.
All arithmetic is integer or Fraction. No target module or fixture is read.
"""
import argparse, hashlib, itertools, json, math, sys, time
from fractions import Fraction as F
from pathlib import Path
START=time.monotonic(); GUARD=45

def require(ok,msg):
    if not ok: raise ValueError(msg)
def tick(): require(time.monotonic()-START<GUARD,'incomplete: 45-second guard')
def trim(p):
    p=list(p)
    while p and not p[-1]:p.pop()
    return tuple(p)
def add(a,b):return trim((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b))))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(a,k):return trim(x*k for x in a)
def mul(a,b):
    if not a or not b:return ()
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def power(a,n):
    b=(1,)
    for _ in range(n):b=mul(b,a)
    return b
def primitive(p):
    p=trim(p)
    if not p:return p
    g=math.gcd(*p)
    return tuple(x//g for x in p)
def prem(a,b):
    """Positive multiple of the ordinary rational Euclidean remainder."""
    require(bool(b),'zero polynomial divisor');r=a
    while r and len(r)>=len(b):
        d=len(r)-len(b);k=r[-1];lead=b[-1]
        r=primitive(sub(scale(r,abs(lead)),(0,)*d+scale(b,k*(1 if lead>0 else -1))))
    return r
def gcdp(a,b):
    a,b=primitive(a),primitive(b)
    while b:a,b=b,prem(a,b)
    return neg(a) if a and a[-1]<0 else a
def exactdiv(a,b):
    require(bool(b),'zero exact divisor');r=a;q=[0]*max(0,len(a)-len(b)+1)
    while r and len(r)>=len(b):
        d=len(r)-len(b);k,rem=divmod(r[-1],b[-1]);require(rem==0,'nonintegral exact division')
        q[d]+=k;r=sub(r,(0,)*d+scale(b,k))
    require(not r,'inexact polynomial division');return trim(q)
def evaluate(a,x):
    z=F(0)
    for c in reversed(a):z=z*x+c
    return z
def derivative(a):return trim(i*a[i] for i in range(1,len(a)))
class Rat:
    def __init__(self,n=0,d=(1,)):
        n=(n,) if isinstance(n,int) else trim(n);d=(d,) if isinstance(d,int) else trim(d)
        require(bool(d),'zero rational denominator')
        if not n:self.n,self.d=(),(1,);return
        g=gcdp(n,d);n,d=exactdiv(n,g),exactdiv(d,g)
        content=math.gcd(*(n+d));n,d=tuple(x//content for x in n),tuple(x//content for x in d)
        if d[-1]<0:n,d=neg(n),neg(d)
        self.n,self.d=n,d
    def __add__(self,o):
        o=o if isinstance(o,Rat) else Rat(o);return Rat(add(mul(self.n,o.d),mul(o.n,self.d)),mul(self.d,o.d))
    __radd__=__add__
    def __neg__(self):return Rat(neg(self.n),self.d)
    def __sub__(self,o):return self+-asrat(o)
    def __rsub__(self,o):return asrat(o)+-self
    def __mul__(self,o):
        o=asrat(o);return Rat(mul(self.n,o.n),mul(self.d,o.d))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=asrat(o);require(bool(o.n),'zero rational inverse');return Rat(mul(self.n,o.d),mul(self.d,o.n))
    def __pow__(self,n):return Rat(power(self.n,n),power(self.d,n))
    def val(self,x):return evaluate(self.n,x)/evaluate(self.d,x)
def asrat(x):return x if isinstance(x,Rat) else Rat(x)
def vadd(a,b):return tuple(x+y for x,y in zip(a,b))
def vsub(a,b):return tuple(x-y for x,y in zip(a,b))
def vmul(a,k):return tuple(x*k for x in a)
def dotr(a,b,t):return (1-t)*sum((x*y for x,y in zip(a,b)),Rat())+t*sum(a,Rat())*sum(b,Rat())
T=(0,1);A=(1,1);Q=(1,3,-1,-3,8);L=(1,2,-1)
OMEGA=mul(mul(power(A,5),Q),L)
LO=F(14,25);HI=F(593,1000)
LABELS=(0,1,2,4,5,6,7,8,9,10,11,12,13)
EDGES=((0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),(2,4),(2,8),(2,10),(4,8),(5,7),(5,9),(5,11),(6,11),(7,12),(9,10),(9,11),(10,12),(5,12),(2,13),(9,13),(10,13))
POS_FACTORS=(T,A,(1,-1),(1,2),(-1,3),(1,3),Q,L)

def reconstruct():
    t=Rat(T);r=2*t/(1+t);e=[tuple(Rat(int(i==j)) for j in range(3)) for i in range(3)]
    p={1:e[0],2:e[1],4:e[2]}
    def reflect(i,j,k):return vsub(vmul(vadd(p[i],p[j]),r),p[k])
    p[8]=reflect(2,4,1);p[10]=reflect(1,2,4);p[12]=reflect(1,10,2)
    p[13]=reflect(2,10,1);p[9]=reflect(10,13,2)
    d=dotr(p[9],p[12],t);p[5]=vsub(vmul(vadd(p[9],p[12]),2*t/(1+d)),p[10])
    numerator=vsub(vsub(p[9],vmul(p[5],r*r*(r+1))),vmul(p[12],1-r*r))
    p[7]=tuple(z/(r*(r*r-2)) for z in numerator)
    p[0]=reflect(5,7,12);p[11]=reflect(0,5,7);p[6]=reflect(0,11,5)
    checks=[]
    for i in LABELS:
        require(not (dotr(p[i],p[i],t)-1).n,'unit identity');checks.append(['unit',i])
    for i,j in EDGES:
        require(not (dotr(p[i],p[j],t)-t).n,'literal contact');checks.append(['contact',i,j])
    require(not (1+d-2*Rat(Q)/(1+t)**3).n,'common-neighbor denominator')
    y={i:tuple(exactdiv(mul(z.n,OMEGA),z.d) for z in p[i]) for i in LABELS}
    require(len(EDGES)==24 and len(set(EDGES))==24,'mask completeness')
    tick();return y,checks

def pdot(a,b):return sum_poly(mul(x,y) for x,y in zip(a,b))
def sum_poly(xs):
    p=()
    for q in xs:p=add(p,q)
    return p
def determinant(rows):
    a,b,c=rows
    return sub(add(mul(a[0],sub(mul(b[1],c[2]),mul(b[2],c[1]))),mul(a[2],sub(mul(b[0],c[1]),mul(b[1],c[0])))),mul(a[1],sub(mul(b[0],c[2]),mul(b[2],c[0]))))
def cram(rows,rhs):
    d=determinant(rows);w=[]
    for j in range(3):
        m=[list(row) for row in rows]
        for k in range(3):m[k][j]=rhs[k]
        w.append(determinant(m))
    return d,tuple(w)
def strip(p):
    p=primitive(p)
    for f in POS_FACTORS:
        while p and len(p)>=len(f):
            if prem(p,f):break
            p=exactdiv(p,f)
    return primitive(p)
STURM={}
def sturm(p):
    if p in STURM:return STURM[p]
    require(bool(p),'zero sign polynomial');s=[p]
    d=derivative(p)
    if d:s.append(primitive(d))
    while len(s)>1:
        r=neg(prem(s[-2],s[-1]))
        if not r:break
        s.append(r);tick()
    STURM[p]=s;return s

def variation(s,x):
    signs=[1 if v>0 else -1 for p in s if (v:=evaluate(p,x))]
    return sum(a!=b for a,b in zip(signs,signs[1:]))
def positive(p,lo,hi):
    if not p or evaluate(p,lo)<=0 or evaluate(p,hi)<=0:return False
    s=sturm(p);return variation(s,lo)==variation(s,hi)
def hash_obj(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def row_data(y):return {**{i:y[i] for i in LABELS},99:tuple((k,) for k in (-5,-14,20))},{**{i:mul(T,OMEGA) for i in LABELS},99:(15,)}

def boundedness(y):
    # Positive dependency p0,p4,p9,p11=0; denominators Omega>0 cancel.
    cols=[y[i] for i in (0,4,9)];rows=list(zip(*cols));rhs=tuple(neg(z) for z in y[11]);d,w=cram(rows,rhs)
    require(positive(strip(neg(d)),LO,HI),'boundedness determinant')
    for q in w:require(positive(strip(neg(q)),LO,HI),'positive spanning dependence')
    return {'labels':[0,4,9,11],'sign_polynomial_hashes':[hash_obj(strip(neg(q))) for q in (d,*w)]}

def triple_record(keys,rows,rhs):
    d,w=cram([rows[k] for k in keys],[rhs[k] for k in keys])
    if not d:return {'active':list(keys),'singular':True}
    # Cancel common polynomial factors in the four Cramer components only.
    g=d
    for q in w:g=gcdp(g,q)
    d,w=exactdiv(d,g),tuple(exactdiv(q,g) for q in w)
    for k in keys:require(pdot(rows[k],w)==mul(rhs[k],d),'whole Cramer identity')
    sq=sum_poly(power(q,2) for q in w);sw=power(sum_poly(w),2)
    dual=sub(mul((1,2),sq),mul(T,sw))
    n=strip(sub(scale(mul(mul((1,-1),(1,2)),power(d,2)),49),scale(dual,50)))
    residual={k:strip(sub(pdot(rows[k],w),mul(rhs[k],d))) for k in rows if k not in keys}
    leaves=[]
    def cover(lo,hi,path):
        tick();require(len(path)<=10,'incomplete sign cover')
        if positive(n,lo,hi):leaves.append({'path':path,'type':'norm','polynomial':hash_obj(n)});return
        mid=(lo+hi)/2
        ups=[(k,p) for k,p in residual.items() if evaluate(p,mid)>0]
        downs=[(k,neg(p)) for k,p in residual.items() if evaluate(p,mid)<0]
        up=next(((k,p) for k,p in ups if positive(p,lo,hi)),None)
        down=next(((k,p) for k,p in downs if positive(p,lo,hi)),None)
        if up and down:
            leaves.append({'path':path,'type':'opposite violations','planes':[up[0],down[0]],'polynomials':[hash_obj(up[1]),hash_obj(down[1])]});return
        cover(lo,mid,path+'0');cover(mid,hi,path+'1')
    cover(LO,HI,'')
    require(sum((F(1,2**len(l['path'])) for l in leaves),F())==1,'incomplete leaf mass')
    for a,b in itertools.combinations(leaves,2):require(not a['path'].startswith(b['path']) and not b['path'].startswith(a['path']),'overlapping tree prefixes')
    return {'active':list(keys),'singular':False,'intersection_hash':hash_obj([d,*w]),'leaves':leaves}

def sharpness(y):
    # ALL 78 original pairs, with no native-coordinate or certificate input.
    square=power(OMEGA,2);pairs=[]
    for i,j in itertools.combinations(LABELS,2):
        inner=add(mul((1,-1),pdot(y[i],y[j])),mul(T,mul(sum_poly(y[i]),sum_poly(y[j]))))
        gap=strip(sub(mul(T,square),inner))
        if (i,j) in EDGES:require(not gap,'original-edge equality')
        elif (i,j)==(6,8):
            require(gap==mul((-1,0,3),(-1,1,17,23)),'6-8 exact threshold factor')
            require(positive((-1,1,17,23),LO,HI),'6-8 positive cubic factor')
        else:require(positive(gap,LO,HI),'other core packing gap')
        pairs.append({'pair':[i,j],'reduced_gap':gap})
    require(len(pairs)==78,'full pair coverage')
    rows,rhs=row_data(y);keys=(0,4,6);d,w=cram([rows[k] for k in keys],[rhs[k] for k in keys]);g=d
    for q in w:g=gcdp(g,q)
    d,w=exactdiv(d,g),tuple(exactdiv(q,g) for q in w)
    require(positive(strip(neg(d)),LO,HI),'witness determinant orientation')
    residuals=[]
    for k in LABELS:
        h=strip(sub(pdot(rows[k],w),mul(rhs[k],d)))
        if k in keys:require(not h,'active witness equality')
        else:require(positive(h,LO,HI),'uniform witness strict feasibility')
        residuals.append({'label':k,'positive_residual':h})
    sq=sum_poly(power(q,2) for q in w);sw=power(sum_poly(w),2)
    normgap=strip(sub(sub(mul((1,2),sq),mul(T,sw)),mul(mul((1,-1),(1,2)),power(d,2))))
    positive_factor=mul((-1,1,17,23),(1,3,0,16,79,77))
    require(normgap==mul((-1,0,3),positive_factor),'exact witness norm threshold')
    require(positive(positive_factor,LO,HI),'positive witness norm factor')
    require(3*LO*LO<1<3*HI*HI,'critical threshold lies inside original closed interval')
    t=F(29,50);dv=evaluate(d,t);z=[evaluate(q,t)/dv for q in w]
    q=((1+2*t)*sum(v*v for v in z)-t*sum(z)**2)/((1-t)*(1+2*t))
    require(q>1,'nonvacuous14-point witness')
    for k in LABELS:require(sum(evaluate(a,t)*b for a,b in zip(rows[k],z))<=evaluate(rhs[k],t),'actual witness packing')
    return {'core_pairs':pairs,'threshold':'1/sqrt(3)','witness_active':list(keys),'dual_D':d,'dual_W':w,'strict_residuals':residuals,'norm_gap_factorization':[(-1,0,3),(-1,1,17,23),(1,3,0,16,79,77)],'sample':{'t':str(t),'dual_coordinates':[str(v) for v in z],'squared_norm':str(q)}}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--start',type=int,default=0);ap.add_argument('--stop',type=int,default=364);ap.add_argument('--output',required=True);ap.add_argument('--build-only',action='store_true');ap.add_argument('--expected');args=ap.parse_args()
    y,checks=reconstruct();b=boundedness(y);rows,rhs=row_data(y)
    record={'method':'reflection rational reconstruction; dual metric; exact Sturm root counts','interval':[str(LO),str(HI)],'coordinates':{str(i):y[i] for i in LABELS},'identities':checks,'boundedness':b,'cap':{'normal':[-5,-14,20],'cut':15,'squared_norm_polynomial':[621,-620],'pair_lower':'881/1369'},'triples':[],'sharpness':sharpness(y)}
    triples=list(itertools.combinations(rows,3));require(len(triples)==364,'all active triples')
    if not args.build_only:
        require(0<=args.start<args.stop<=364,'shard range')
        for keys in triples[args.start:args.stop]:record['triples'].append(triple_record(keys,rows,rhs))
    record['range']=[args.start,args.stop] if not args.build_only else None
    if args.expected:require(json.loads(Path(args.expected).read_text())==json.loads(json.dumps(record)),'whole typed expected record mismatch')
    Path(args.output).write_text(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'status':'PASS','range':record['range'],'triples':len(record['triples']),'record_sha256':hash_obj(record),'seconds':time.monotonic()-START,'sturm_polynomials':len(STURM)}))
if __name__=='__main__':main()
