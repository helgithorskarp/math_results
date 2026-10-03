"""Exact six-linear-constraint producer; actual author six-tammes-1.

Cramer necessary norm equations hold even at a zero determinant. This
program never divides by a six-by-six determinant or removes its roots.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, permutations
from hashlib import sha256
from math import gcd
from collections import Counter
import argparse,json
from poly import add,neg,mul,divide,bezout,bernstein

R,D,Q=[F(0),F(1)],[F(2),F(-1)],[F(0),F(-3),F(2),F(2)]
LO,HI=F(7,10),F(3,4)
A=((0,5,11),(0,6,11),(0,5,7),(5,9,11))
B=((1,2,4),(2,4,8),(1,2,10),(1,10,12))
LEAVES=(6,7,9)
FACTORS=(R,D,[F(1),F(-1)],[F(1),F(1)],[F(2),F(1)],[F(-1),F(2)],[F(1),F(2)])
PARENT_SHA='a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187'
M=[[R,[F(-1)],R],[R,R,[F(-1)]],[[F(-1)],R,R]]
G=[F(x) for x in (-2,2,2,-2,0,1)]

def need(ok,why):
    if not ok:raise ValueError(why)

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))+'\n'
def digest(x):return sha256(canonical(x).encode()).hexdigest()
def enc(p):return [str(x) for x in p]
def vecscale(p,v):return [mul(p,x) for x in v]
def vecadd(a,b):return [add(x,y) for x,y in zip(a,b)]

def primitive(p):
    if not p:return []
    scale=1
    for a in p:scale=scale*a.denominator//gcd(scale,a.denominator)
    ns=[int(a*scale) for a in p];content=0
    for n in ns:content=gcd(content,abs(n))
    return [F(n//content) for n in ns]

def strip(p):
    for f in FACTORS:
        while p and len(p)>=len(f):
            q,r=divide(p,f)
            if r:break
            p=q
    return primitive(p)

def direct_sign(p):
    bs=bernstein(p,LO,HI)
    return 1 if all(a>0 for a in bs) else -1 if all(a<0 for a in bs) else 0

def sign(p):return direct_sign(strip(p))

def inner(v,w):
    diag=[];sv=[];sw=[]
    for x,y in zip(v,w):diag=add(diag,mul(x,y));sv=add(sv,x);sw=add(sw,y)
    return add(mul([F(2),F(-2)],diag),mul(R,mul(sv,sw)))

def flip(u,v,w):return vecadd(vecscale(R,vecadd(u,v)),vecscale([F(-1)],w))

def reconstruct(ts):
    p={1:[[F(1)],[],[]],2:[[],[F(1)],[]],4:[[],[],[F(1)]]}
    p[8]=flip(p[2],p[4],p[1]);p[10]=flip(p[1],p[2],p[4]);p[12]=flip(p[1],p[10],p[2])
    done={tuple(sorted(t)) for t in B};todo=set(map(tuple,ts))-done
    while todo:
        t=next((t for t in sorted(todo) if len(set(t)&set(p))==2),None);need(t is not None,'fresh B triangle exists')
        e=sorted(set(t)&set(p));parents=[u for u in done if set(e)<=set(u)];need(len(parents)==1,'single B parent')
        old=next(x for x in parents[0] if x not in e);fresh=next(x for x in t if x not in e)
        p[fresh]=flip(p[e[0]],p[e[1]],p[old]);done.add(t);todo.remove(t)
    need(len(p)==9 and all(inner(v,v)==D for v in p.values()),'every unit B identity')
    for t in ts:
        for i,j in combinations(t,2):need(inner(p[i],p[j])==R,'every B contact identity')
    return p

def bareiss(matrix):
    a=[[list(x) for x in row] for row in matrix];n=len(a);old=[F(1)];sgn=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if a[i][k]),None)
        if pivot is None:return []
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];sgn=-sgn
        piv=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                raw=add(mul(piv,a[i][j]),neg(mul(a[i][k],a[k][j])))
                q,re=divide(raw,old);need(not re,'exact entire Bareiss division');a[i][j]=q
        for i in range(k+1,n):a[i][k]=[]
        old=piv
    return mul([F(sgn)],a[-1][-1])

def coeffs():
    md=bareiss(M);need(md==mul([F(-1),F(2)],mul([F(1),F(1)],[F(1),F(1)])),'whole A leaf determinant')
    c={v:[md if i==j else [] for i in range(3)] for j,v in enumerate(LEAVES)}
    for i,label in enumerate((0,5,11)):
        c[label]=[]
        for j in range(3):
            mm=[[([F(1)] if k==j else []) if h==i else x for h,x in enumerate(row)] for k,row in enumerate(M)]
            c[label].append(bareiss(mm))
    for i in range(3):
        for j in range(3):
            s=[]
            for k in range(3):s=add(s,mul(M[i][k],c[(0,5,11)[k]][j]))
            need(s==(md if i==j else []),'coefficientwise A inverse identity')
    return c,md

def parent():
    blob=Path(__file__).with_name('PARENT.json').read_bytes();need(sha256(blob).hexdigest()==PARENT_SHA,'entire immutable9972 certificate')
    p=json.loads(blob);need(p['A']==[list(t) for t in A] and p['B']==[list(t) for t in B],'whole prescribed A4/B4 seeds')
    need(len(p['full_band_maps'])==53 and len(p['strict_improvement_maps'])==52,'parent finite lists')
    need(all(direct_sign(f)==1 for f in FACTORS),'all fixed removed factors positive on closed band')
    return p

def predictions(row):
    ans=[]
    for f in row['faces']:
        if len(f)==4 and sum(x in (0,5,6,7,9,11) for x in f)==1:
            i=next(i for i,x in enumerate(f) if x in (0,5,6,7,9,11))
            ans.append((f[i],[f[(i+h)%4] for h in (1,2,3)],f))
    return ans

def anchor(points,pred):
    a,(u,z,v),face=pred
    rawL=add(D,inner(points[u],points[v]));rawn=vecadd(vecscale(mul([F(2)],R),vecadd(points[u],points[v])),vecscale(neg(rawL),points[z]))
    need(sign(rawL)==1,'positive unscaled common-neighbor denominator')
    g=rawL
    for x in rawn:g=bezout(g,x)[0]
    n=[]
    for x in rawn:
        q,re=divide(x,g);need(not re,'entire exact anchor cancellation');n.append(q)
    L,re=divide(rawL,g);need(not re,'exact anchor denominator cancellation')
    sg=sign(L);need(sg in (-1,1),'anchor denominator nonzero over whole band')
    if sg==-1:n=vecscale([F(-1)],n);L=neg(L)
    need(inner(n,n)==mul(D,mul(L,L)),'whole anchor unit identity')
    for x in (u,v):need(inner(n,points[x])==mul(R,L),'both anchor cross-contact identities')
    return a,n,L

def row_reduce(row,rhs):
    g=rhs
    for x in row:g=bezout(g,x)[0]
    if not g or not sign(g):return row,rhs,[F(1)]
    xs=[]
    for x in row+[rhs]:
        q,re=divide(x,g);need(not re,'entire exact nonzero row cancellation');xs.append(q)
    return xs[:-1],xs[-1],g

def reduce_equation(p,L):
    p=strip(p)
    while p and len(p)>=len(L):
        q,re=divide(p,L)
        if re:break
        p=q
    return primitive(p)

def linear_case(index,row,ts,pred,c,md):
    bp=reconstruct(ts);a,n,L=anchor(bp,pred);unknown=[v for v in LEAVES if v!=a];ai=LEAVES.index(a);matrix=[];rhs=[];factors=[]
    need(len(unknown)==2 and sign(L)==1,'two other A leaves and positive anchor denominator')
    basis=[[[F(1)] if i==j else [] for i in range(3)] for j in range(3)]
    for leaf in unknown:
        h=[inner(n,e) for e in basis];rr=mul(Q,L)
        ar=[h[j] if unknown[k]==leaf else [] for k in range(2) for j in range(3)]
        ar,rr,g=row_reduce(ar,rr);matrix.append(ar);rhs.append(rr);factors.append(enc(g))
    for ax,b in row['cross']:
        if ax==a:
            need(inner(n,bp[b])==mul(R,L),'all fixed-anchor cross contacts');continue
        cf=c[ax];h=[inner(bp[b],e) for e in basis]
        ar=[mul(mul(cf[LEAVES.index(unknown[k])],L),h[j]) for k in range(2) for j in range(3)]
        rr=add(mul(mul(R,md),L),neg(mul(cf[ai],inner(n,bp[b]))))
        ar,rr,g=row_reduce(ar,rr);matrix.append(ar);rhs.append(rr);factors.append(enc(g))
    need(len(matrix)==6,'complete six linear necessary equations')
    delta=bareiss(matrix);nums=[]
    for j in range(6):nums.append(bareiss([[rhs[i] if j==k else x for k,x in enumerate(ar)] for i,ar in enumerate(matrix)]))
    for ar,b in zip(matrix,rhs):
        s=[]
        for x,y in zip(ar,nums):s=add(s,mul(x,y))
        need(s==mul(delta,b),'all Cramer row identities, no determinant inversion')
    v,w=nums[:3],nums[3:];d2=mul(delta,delta)
    raw=[add(inner(v,v),neg(mul(D,d2))),add(inner(w,w),neg(mul(D,d2))),add(inner(v,w),neg(mul(Q,d2)))]
    equations=[reduce_equation(e,L) for e in raw];h=equations[0]
    for e in equations[1:]:h=bezout(h,e)[0]
    h=primitive(h)
    return {'map':index,'shape':row['shape'],'B_triangles':ts,'cross':row['cross'],'quad':pred[2],
            'anchor':a,'anchor_n':[enc(x) for x in n],'anchor_L':enc(L),'row_divisors':factors,
            'linear_system_digest':digest([[enc(x) for x in ar] for ar in matrix]+[[enc(x) for x in rhs]]),
            'Cramer_digest':digest([enc(delta),[enc(x) for x in nums]]),'determinant_degree':len(delta)-1,
            'norm_equations_digest':digest([enc(e) for e in raw]),'reduced_equations_digest':digest([enc(e) for e in equations]),
            'reduced_degrees':[len(e)-1 for e in equations],'common_gcd':enc(h),'closed_gcd_sign':direct_sign(h)},equations

def build():
    p=parent();c,md=coeffs();rows=[]
    for index in p['strict_improvement_maps']:
        row=p['geometric_maps'][index];ps=predictions(row)
        if not ps:continue
        need(len(ps)==1,'one sole A-corner quadrilateral per strict map')
        result,_=linear_case(index,row,p['all_shapes'][row['shape']],ps[0],c,md)
        need(result['closed_gcd_sign'] in (-1,1),'closed whole-band common-zero exclusion')
        rows.append(result)
    need(len(rows)==29 and Counter(r['anchor'] for r in rows)==Counter({7:8,9:15,6:6}),'entire sole-corner cover')
    surviving=[i for i in p['full_band_maps'] if i not in {r['map'] for r in rows}]
    strict=[i for i in surviving if i in p['strict_improvement_maps']]
    need(len(surviving)==24 and len(strict)==23 and set(surviving)-set(strict)=={8},'whole residual lists')
    for i in strict:
        need(all(sum(v in c for v in f)==2 for f in p['geometric_maps'][i]['faces'] if len(f)==4),'every remaining strict Q has two A/two B corners')
    return {'format':'b7-sole-corner-exclusions-v1','actual_author':'six-tammes-1','role':'researcher',
            'parent_sha256':PARENT_SHA,'cosine_closed_band':['7/13','3/5'],'r_closed_band':[str(LO),str(HI)],
            'A_triangles':A,'rows':rows,'remaining_closed_maps':surviving,'remaining_strict_maps':strict,
            'scope':'29 literal15-distinct-unit contact masks impossible on closedJ; full physical corollary imports ALL9972/9813 and10038; no global bound'}

def verify(record,expected=None):
    if expected is None:expected=build()
    need(canonical(record)==canonical(expected),'whole freshly computed typed certificate equality')

def summary(record):
    blob=canonical(record).encode()
    return {'status':'complete','excluded_literal_masks':len(record['rows']),'remaining_closed_maps':len(record['remaining_closed_maps']),
            'remaining_strict_maps':len(record['remaining_strict_maps']),'singular_parameters_retained':True,
            'certificate_bytes':len(blob),'certificate_sha256':sha256(blob).hexdigest()}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--emit');parser.add_argument('--verify',default=str(Path(__file__).with_name('CERTIFICATE.json')));args=parser.parse_args()
    r=build()
    if args.emit:Path(args.emit).write_text(canonical(r))
    else:verify(json.loads(Path(args.verify).read_text()),r)
    print(canonical(summary(r)).strip())
