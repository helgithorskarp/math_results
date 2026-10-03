"""Separate sparse whole-record check; six-tammes-1/researcher.

Reverse leaf peeling, metric matrix multiplication, Bernstein basis identity
and an independent monotonicity bound. Imports neither check.py nor poly.py.
Sparse reflection arithmetic is credited to the earlier same-author10068
auditor. This is a second algorithm, not independent mathematical review.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from collections import Counter
from math import comb
import argparse,json

ROOT=Path(__file__).resolve().parent
PARENT_SHA='a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187'
PREVIOUS_SHA='b92549e6c9c7047df9c85d7a67fc724a42f3175006050c4fb5984205d2be9b11'
SEED={(1,2,4),(2,4,8),(1,2,10),(1,10,12)}
LO,HI=F(7,10),F(3,4)
def require(ok,why):
    if not ok:raise ValueError(why)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))+'\n'
def digest(x):return sha256(canonical(x).encode()).hexdigest()
def P(*xs):return {i:F(x) for i,x in enumerate(xs) if x}
def tidy(x):return {i:v for i,v in x.items() if v}
def plus(a,b):
    q=dict(a)
    for i,v in b.items():q[i]=q.get(i,F(0))+v
    return tidy(q)
def scale(a,k):return tidy({i:v*k for i,v in a.items()})
def times(a,b):
    q={}
    for i,x in a.items():
        for j,y in b.items():q[i+j]=q.get(i+j,F(0))+x*y
    return tidy(q)
def power(p,n):
    out=P(1)
    for _ in range(n):out=times(out,p)
    return out
def total(ps):
    out={}
    for p in ps:out=plus(out,p)
    return out
def enc(p):return [str(p.get(i,F(0))) for i in range(max(p,default=-1)+1)]
def parse(xs):
    require(type(xs) is list and all(type(x) is str for x in xs),'typed rational polynomial')
    p=P(*(F(x) for x in xs));require(enc(p)==xs,'canonical whole polynomial');return p
def at(p,x):return sum(v*x**i for i,v in p.items())
def derivative(p):return {i-1:i*v for i,v in p.items() if i}
def upper_terms(p,lo=LO,hi=HI):
    require(0<=lo<=hi,'nonnegative closed power interval')
    return sum(v*(hi if v>0 else lo)**i for i,v in p.items())
R,D,K=P(0,1),P(2,-1),P(4,0,-8,-4,2,1)
def gram(v,w):
    h=[total(times(D if i==j else R,v[j]) for j in range(3)) for i in range(3)]
    return total(times(h[i],w[i]) for i in range(3))
def reflection(u,v,w):return tuple(plus(times(R,plus(x,y)),scale(z,-1)) for x,y,z in zip(u,v,w))
def points(triangles):
    left={tuple(t) for t in triangles};peels=[];fixed={1,2,4,8,10,12}
    require(SEED<=left and len(left)==7,'whole seven B triangles with seed')
    while left!=SEED:
        counts=Counter(x for t in left for x in t)
        candidates=[(t,x) for t in left for x in t if t not in SEED and x not in fixed and counts[x]==1]
        require(bool(candidates),'reverse B leaf exists');t,x=max(candidates);peels.append((t,x));left.remove(t)
    ps={1:(P(1),{},{}),2:({},P(1),{}),4:({},{},P(1))}
    ps[8]=reflection(ps[2],ps[4],ps[1]);ps[10]=reflection(ps[1],ps[2],ps[4]);ps[12]=reflection(ps[1],ps[10],ps[2])
    done=set(SEED)
    for t,x in reversed(peels):
        u,v=sorted(set(t)-{x});parents=[q for q in done if u in q and v in q]
        require(len(parents)==1,'whole common-edge reverse predecessor')
        old=next(y for y in parents[0] if y not in (u,v));ps[x]=reflection(ps[u],ps[v],ps[old]);done.add(t)
    require(set(ps)=={1,2,4,8,10,12,20,21,22},'entire nine B labels')
    require(all(gram(v,v)==D for v in ps.values()),'all nine unit identities')
    for t in triangles:
        for u,v in combinations(t,2):require(gram(ps[u],ps[v])==R,'every B contact identity')
    return ps
def verify(record):
    blobs=[(ROOT/'PARENT.json').read_bytes(),(ROOT/'PREVIOUS.json').read_bytes()]
    require([sha256(x).hexdigest() for x in blobs]==[PARENT_SHA,PREVIOUS_SHA],'both complete frozen inputs')
    p,q=map(json.loads,blobs)
    require(q['parent_sha256']==PARENT_SHA and p['B']==[[1,2,4],[2,4,8],[1,2,10],[1,10,12]],'whole seed and cover binding')
    cuts={r['map'] for r in q['rows']};require(len(cuts)==29,'previous whole29 exclusions are an imported theorem')
    require([i for i in p['full_band_maps'] if i not in cuts]==q['remaining_closed_maps'],'whole imported closed cover')
    require([i for i in p['strict_improvement_maps'] if i not in cuts]==q['remaining_strict_maps'],'whole imported strict cover')
    require(len(q['remaining_closed_maps'])==24 and len(q['remaining_strict_maps'])==23,'old24/23 scope')
    # Independent sign argument: K' has a strictly negative termwise upper
    # bound on the closed band, and K at the left endpoint is negative.
    require(upper_terms(derivative(K))==F(-77587,6400),'whole derivative upper bound')
    require(at(K,LO)==F(-64373,100000),'whole endpoint upper bound')
    require(upper_terms(derivative(K))<0 and at(K,LO)<0,'strict closed monotonicity proof')
    bs=[F(x) for x in record['K_Bernstein']];require(len(bs)==6,'entire degree5 Bernstein table')
    t=P(-LO/(HI-LO),1/(HI-LO));one_minus=P(HI/(HI-LO),-1/(HI-LO))
    restored=total(scale(times(power(t,i),power(one_minus,5-i)),bs[i]*comb(5,i)) for i in range(6))
    require(restored==K and max(bs)==F(-64373,100000) and all(x<0 for x in bs),'whole Bernstein polynomial identity and closed sign')
    rows=[];cases=[];keys={}
    # Select every occurrence of the exact impossible gap in the imported
    # full23 list; do not trust the producer's selected list or its count.
    for i in q['remaining_strict_maps']:
        row=p['geometric_maps'][i];ps=points(p['all_shapes'][row['shape']]);counts=Counter(x for x,y in row['cross'])
        anchors=[a for a in (6,7,9) if counts[a]==2];require(len(anchors)==1,'one double-B-contact A leaf in each residual row')
        a=anchors[0];pair=sorted(y for x,y in row['cross'] if x==a);u,v=pair
        g=gram(ps[u],ps[v]);s=plus(times(D,plus(D,g)),scale(times(R,R),-2))
        if s!=times(P(2,-2),K):continue
        key=(row['shape'],tuple(pair))
        if key not in keys:
            index=len(cases);keys[key]=index
            cases.append({'case':index,'shape':row['shape'],'B_triangles':p['all_shapes'][row['shape']],
                          'pair':pair,'B_points':{str(x):[enc(t) for t in ps[x]] for x in sorted(ps)},'pair_N':enc(g),'S':enc(s)})
        rows.append({'map':i,'shape':row['shape'],'anchor':a,'pair':pair,'case':keys[key],'cross':row['cross']})
    ids=[r['map'] for r in rows]
    require(ids==[42,65,69,72,75,76,77,78,79] and len(cases)==6,'whole newly excluded9/six masks')
    strict=[i for i in q['remaining_strict_maps'] if i not in ids];closed=[i for i in q['remaining_closed_maps'] if i not in ids]
    require(len(strict)==14 and len(closed)==15 and set(closed)-set(strict)=={8},'complete residual lists')
    expected={'format':'b7-common-neighbor-obstruction-v1','actual_author':'six-tammes-1','role':'researcher',
              'parent_sha256':PARENT_SHA,'previous_sha256':PREVIOUS_SHA,
              'cosine_closed_band':['7/13','3/5'],'r_closed_band':[str(LO),str(HI)],'B_seed':p['B'],
              'K':enc(K),'K_Bernstein':[str(x) for x in bs],'K_closed_upper':str(max(bs)),
              'cases':cases,'excluded_maps':ids,'rows':rows,'remaining_closed_maps':closed,'remaining_strict_maps':strict,
              'scope':'Six nine-distinct-unit B7/pair masks admit no unit common c-neighbor in R3 on closedJ; nine15-label maps excluded. Physical corollary imports ALL9972/9813/10038/10068; no global bound.'}
    require(record==expected,'whole independently reconstructed geometric certificate')
    return {'status':'complete','cases':6,'excluded_maps':9,'remaining_closed':15,'remaining_strict':14,'certificate_sha256':digest(record)}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--certificate',default=str(ROOT/'CERTIFICATE.json'));args=parser.parse_args()
    print(canonical(verify(json.loads(Path(args.certificate).read_text()))).strip())
