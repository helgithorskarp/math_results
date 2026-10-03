"""Independent sparse checker: reverse B peeling and integer determinant interpolation.

No import from check.py or poly.py. Actual author six-tammes-1; this is a
second same-author algorithm, not an independent mathematical review.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import comb,gcd,factorial
import argparse,json

ROOT=Path(__file__).resolve().parent
PARENT_SHA='a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187'
A=((0,5,11),(0,6,11),(0,5,7),(5,9,11));B=((1,2,4),(2,4,8),(1,2,10),(1,10,12));LEAF=(6,7,9)
LO,HI=F(7,10),F(3,4)

def require(ok,why):
    if not ok:raise ValueError(why)

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'))+'\n'
def digest(x):return sha256(canon(x).encode()).hexdigest()
def P(*a):return {i:F(x) for i,x in enumerate(a) if x}
def tidy(p):return {k:v for k,v in p.items() if v}
def plus(a,b):
    p=dict(a)
    for k,v in b.items():p[k]=p.get(k,F(0))+v
    return tidy(p)
def scale(a,k):return tidy({i:x*k for i,x in a.items()})
def times(a,b):
    p={}
    for i,x in a.items():
        for j,y in b.items():p[i+j]=p.get(i+j,F(0))+x*y
    return tidy(p)
def degree(p):return max(p,default=-1)
def coeffs(p):return [p.get(i,F(0)) for i in range(degree(p)+1)]
def encode(p):return [str(v) for v in coeffs(p)]
def parsep(x):
    require(type(x) is list and all(type(v) is str for v in x),'typed rational polynomial')
    p=P(*(F(v) for v in x));require(encode(p)==x,'whole canonical polynomial representation');return p

def divrem(a,b):
    require(bool(b),'nonzero polynomial divisor');p=dict(a);q={};n=degree(b)
    while p and degree(p)>=n:
        power=degree(p)-n;v=p[degree(p)]/b[n];q[power]=q.get(power,F(0))+v
        p=plus(p,scale({i+power:x for i,x in b.items()},-v))
    return tidy(q),p

def primitive(p):
    if not p:return {}
    den=1
    for v in p.values():den=den*v.denominator//gcd(den,v.denominator)
    ints={i:int(v*den) for i,v in p.items()};content=0
    for v in ints.values():content=gcd(content,abs(v))
    return {i:F(v//content) for i,v in ints.items() if v}

def common(a,b):
    while b:_,rem=divrem(a,b);a,b=b,rem
    require(bool(a),'some nonzero necessary equation')
    return scale(a,1/a[degree(a)])

R,D,Q=P(0,1),P(2,-1),P(0,-3,2,2)
FACTORS=(R,D,P(1,-1),P(1,1),P(2,1),P(-1,2),P(1,2))

def centered_sign(p,lo=LO,hi=HI,depth=0):
    if not p:return 0
    mid=(lo+hi)/2;rad=(hi-lo)/2;shift={}
    for i,x in p.items():
        for k in range(i+1):shift[k]=shift.get(k,F(0))+x*comb(i,k)*mid**(i-k)
    center=shift.get(0,F(0));error=sum(abs(v)*rad**k for k,v in shift.items() if k)
    if center-error>0:return 1
    if center+error<0:return -1
    if depth>=12:return 0
    a=centered_sign(p,lo,mid,depth+1)
    if not a:return 0
    b=centered_sign(p,mid,hi,depth+1)
    return a if a==b else 0

def reduced(p,L):
    for f in FACTORS:
        while p and degree(p)>=degree(f):
            q,re=divrem(p,f)
            if re:break
            p=q
    p=primitive(p)
    while p and degree(p)>=degree(L):
        q,re=divrem(p,L)
        if re:break
        p=q
    return primitive(p)

def sum_poly(ps):
    ans={}
    for p in ps:ans=plus(ans,p)
    return ans

def gram(v,w):
    total=sum_poly(v)
    h=[plus(times(P(2,-2),x),times(R,total)) for x in v]
    return sum_poly(times(x,y) for x,y in zip(h,w))

def reflect(u,v,w):return tuple(plus(times(R,plus(x,y)),scale(z,-1)) for x,y,z in zip(u,v,w))

def Bpoints(triangles):
    seed=set(tuple(sorted(t)) for t in B);left=set(tuple(t) for t in triangles);peels=[];fixed={1,2,4,8,10,12}
    while left!=seed:
        count={}
        for t in left:
            for x in t:count[x]=count.get(x,0)+1
        picks=[(t,x) for t in left for x in t if t not in seed and x not in fixed and count[x]==1]
        require(bool(picks),'reverse B leaf exists');t,x=max(picks);peels.append((t,x));left.remove(t)
    ps={1:(P(1),{},{}),2:({},P(1),{}),4:({},{},P(1))}
    ps[8]=reflect(ps[2],ps[4],ps[1]);ps[10]=reflect(ps[1],ps[2],ps[4]);ps[12]=reflect(ps[1],ps[10],ps[2]);done=set(seed)
    for t,x in reversed(peels):
        u,v=sorted(set(t)-{x});parents=[tt for tt in done if u in tt and v in tt];require(len(parents)==1,'single reverse-parent edge')
        old=next(y for y in parents[0] if y not in (u,v));ps[x]=reflect(ps[u],ps[v],ps[old]);done.add(t)
    require(len(ps)==9 and all(gram(v,v)==D for v in ps.values()),'all nine independently restored unit B points')
    for t in triangles:
        for u,v in combinations(t,2):require(gram(ps[u],ps[v])==R,'every prescribed B contact')
    return ps

def Acoeff():
    m=[[R,P(-1),R],[R,R,P(-1)],[P(-1),R,R]];md=times(P(-1,2),times(P(1,1),P(1,1)))
    c={v:[md if i==j else {} for i in range(3)] for j,v in enumerate(LEAF)}
    for i,x in enumerate((0,5,11)):
        c[x]=[]
        for j in range(3):
            mi=[[m[a][b] for b in range(3) if b!=i] for a in range(3) if a!=j]
            c[x].append(scale(plus(times(mi[0][0],mi[1][1]),scale(times(mi[0][1],mi[1][0]),-1)),(-1)**(i+j)))
    for i in range(3):
        for j in range(3):require(sum_poly(times(m[i][k],c[(0,5,11)[k]][j]) for k in range(3))==(md if i==j else {}),'whole independent inverse coefficients')
    require(centered_sign(md)==1,'invertible A root-to-leaf map')
    return c,md

def integer_det(matrix):
    a=[list(row) for row in matrix];n=len(a);old=1;sgn=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if a[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];sgn=-sgn
        piv=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                q,re=divmod(piv*a[i][j]-a[i][k]*a[k][j],old);require(re==0,'exact integer determinant division');a[i][j]=q
        for i in range(k+1,n):a[i][k]=0
        old=piv
    return sgn*a[-1][-1]

def at(p,x):return sum(v*x**i for i,v in p.items())

def interpolate_det(matrix):
    # A determinant has degree <= the sum of maximum row degrees, whether
    # generic full rank, identically singular, or singular at a sample.
    if any(all(not p for p in row) for row in matrix):return {}
    bound=sum(max(degree(p) for p in row) for row in matrix);scaled=[];total_scale=1
    for row in matrix:
        d=1
        for p in row:
            for v in p.values():d=d*v.denominator//gcd(d,v.denominator)
        scaled.append([{i:int(v*d) for i,v in p.items()} for p in row]);total_scale*=d
    values=[integer_det([[at(p,j) for p in row] for row in scaled]) for j in range(bound+1)]
    out={};basis=P(1);differences=list(values)
    for k in range(bound+1):
        out=plus(out,scale(basis,F(differences[0],factorial(k)*total_scale)))
        differences=[b-a for a,b in zip(differences,differences[1:])]
        basis=times(basis,P(-k,1))
    # Additional exact samples independently exercise interpolation, beyond
    # the degree-bound argument used for the whole polynomial identity.
    for j in (bound+1,bound+2):require(at(out,j)*total_scale==integer_det([[at(p,j) for p in row] for row in scaled]),'extra integer interpolation control')
    return out

def audit(record):
    blob=(ROOT/'PARENT.json').read_bytes();require(sha256(blob).hexdigest()==PARENT_SHA,'whole parent input')
    p=json.loads(blob);c,md=Acoeff();require(all(centered_sign(f)==1 for f in FACTORS),'every removed fixed factor strictly positive')
    aset=set(c);selected=[]
    for i in p['strict_improvement_maps']:
        row=p['geometric_maps'][i];fs=[f for f in row['faces'] if len(f)==4 and len(aset.intersection(f))==1]
        if fs:require(len(fs)==1,'one selected quad');selected.append((i,row,fs[0]))
    require(len(selected)==29 and [r['map'] for r in record['rows']]==[i for i,_,_ in selected],'whole case list, not matching counts alone')
    rebuilt=[]
    for stored,(i,row,face) in zip(record['rows'],selected):
        ts=p['all_shapes'][row['shape']];bp=Bpoints(ts);a=next(v for v in face if v in aset);pos=face.index(a);u,z,v=(face[(pos+h)%4] for h in (1,2,3))
        n=[parsep(x) for x in stored['anchor_n']];L=parsep(stored['anchor_L']);rawL=plus(D,gram(bp[u],bp[v]))
        rawN=[plus(times(scale(R,2),plus(x,y)),scale(times(rawL,zz),-1)) for x,y,zz in zip(bp[u],bp[v],bp[z])]
        require(centered_sign(rawL)==1 and centered_sign(L)==1,'both closed anchor denominators positive')
        require(all(times(nn,rawL)==times(rr,L) for nn,rr in zip(n,rawN)),'entire anchor ratio, no chosen numeric location')
        require(gram(n,n)==times(D,times(L,L)),'whole independent anchor unit identity')
        unk=sorted(set(LEAF)-{a});ai=LEAF.index(a);basis=[tuple(P(1) if j==k else {} for j in range(3)) for k in range(3)];rawmat=[];rawrhs=[]
        h=[gram(e,n) for e in basis]
        for leaf in unk:
            rawmat.append([h[j] if unk[k]==leaf else {} for k in range(2) for j in range(3)]);rawrhs.append(times(Q,L))
        for ax,b in row['cross']:
            if ax==a:require(gram(n,bp[b])==times(R,L),'all fixed-anchor cross contacts');continue
            h=[gram(e,bp[b]) for e in basis];cf=c[ax]
            rawmat.append([times(times(L,cf[LEAF.index(unk[k])]),h[j]) for k in range(2) for j in range(3)])
            rawrhs.append(plus(times(times(R,md),L),scale(times(cf[ai],gram(n,bp[b])),-1)))
        require(len(rawmat)==6 and len(stored['row_divisors'])==6,'whole six-row constraint system')
        matrix=[];rhs=[]
        for ar,b,gdata in zip(rawmat,rawrhs,stored['row_divisors']):
            g=parsep(gdata);require(centered_sign(g) in (-1,1),'row divisor nonzero throughout closed band')
            reduced_row=[]
            for x in ar+[b]:q,re=divrem(x,g);require(not re,'entire sparse row exact division');reduced_row.append(q)
            matrix.append(reduced_row[:-1]);rhs.append(reduced_row[-1])
        delta=interpolate_det(matrix);nums=[]
        for j in range(6):nums.append(interpolate_det([[rhs[k] if j==h else x for h,x in enumerate(ar)] for k,ar in enumerate(matrix)]))
        for ar,b in zip(matrix,rhs):require(sum_poly(times(x,y) for x,y in zip(ar,nums))==times(delta,b),'all six independent Cramer identities')
        v,w=nums[:3],nums[3:];d2=times(delta,delta)
        raw=[plus(gram(v,v),scale(times(D,d2),-1)),plus(gram(w,w),scale(times(D,d2),-1)),plus(gram(v,w),scale(times(Q,d2),-1))]
        eq=[reduced(x,L) for x in raw];h=eq[0]
        for e in eq[1:]:h=common(h,e)
        h=primitive(h);sg=centered_sign(h);require(sg in (-1,1),'closed common-zero exclusion by derivative-free centered bounds')
        rr={'map':i,'shape':row['shape'],'B_triangles':ts,'cross':row['cross'],'quad':face,'anchor':a,
            'anchor_n':[encode(x) for x in n],'anchor_L':encode(L),'row_divisors':stored['row_divisors'],
            'linear_system_digest':digest([[encode(x) for x in ar] for ar in matrix]+[[encode(x) for x in rhs]]),
            'Cramer_digest':digest([encode(delta),[encode(x) for x in nums]]),'determinant_degree':degree(delta),
            'norm_equations_digest':digest([encode(x) for x in raw]),'reduced_equations_digest':digest([encode(x) for x in eq]),
            'reduced_degrees':[degree(x) for x in eq],'common_gcd':encode(h),'closed_gcd_sign':sg}
        require(canon(rr)==canon(stored),'whole row matches independent polynomial reconstruction');rebuilt.append(rr)
    kept=[i for i in p['full_band_maps'] if i not in {r['map'] for r in rebuilt}];strict=[i for i in kept if i in p['strict_improvement_maps']]
    for i in strict:require(all(len(aset.intersection(f))==2 for f in p['geometric_maps'][i]['faces'] if len(f)==4),'every remaining Q has two A and two B corners')
    expected={'format':'b7-sole-corner-exclusions-v1','actual_author':'six-tammes-1','role':'researcher','parent_sha256':PARENT_SHA,
              'cosine_closed_band':['7/13','3/5'],'r_closed_band':[str(LO),str(HI)],'A_triangles':A,'rows':rebuilt,
              'remaining_closed_maps':kept,'remaining_strict_maps':strict,
              'scope':'29 literal15-distinct-unit contact masks impossible on closedJ; full physical corollary imports ALL9972/9813 and10038; no global bound'}
    require(canon(expected)==canon(record),'whole typed final certificate matches')
    b=canon(expected).encode()
    return {'status':'complete','excluded_literal_masks':len(rebuilt),'remaining_closed_maps':len(kept),'remaining_strict_maps':len(strict),
            'singular_parameters_retained':True,'certificate_bytes':len(b),'certificate_sha256':sha256(b).hexdigest()}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--verify',default=str(ROOT/'CERTIFICATE.json'));args=parser.parse_args()
    print(canon(audit(json.loads(Path(args.verify).read_text()))).strip())
