"""All field-valued horizontal-shear contact events of the frozen 530 points."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from collections import Counter
import heapq,json
from field import Field,add,sub,neg,scale

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
Z=(F(0),)*8;ONE=(F(1),)+Z[1:]
RAD=(1,3,5,15,11,33,55,165)

def require(ok,why):
    if not ok:raise ValueError(why)

def points():
    pins=json.loads((HERE/'inputs.json').read_text())
    for path,h in pins.items():require(sha256((REPO/path).read_bytes()).hexdigest()==h,('input digest',path))
    all_points=[]
    for line in (REPO/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text().splitlines():
        if not line or line.startswith('#'):continue
        a=tuple(3*int(x)for x in line.split());require(len(a)==16,'point width')
        all_points.append((a[:8],a[8:]))
    require(len(all_points)==509,'base points')
    cs=json.loads((REPO/'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())['points']
    for c in cs:
        a=tuple(288*F(v)for axis in ('x','y')for v in c[axis])
        require(len(a)==16 and all(x.denominator==1 for x in a),'completion coordinates')
        a=tuple(map(int,a));all_points.append((a[:8],a[8:]))
    c=json.loads((REPO/'hadwiger_nelson_point606_criticality_gate/certificate.json').read_text())
    deleted=c['deleted_labels'];require(deleted==sorted(set(deleted)),'deletion domain')
    labels=[v for v in list(range(585))+[606] if v not in deleted]
    P=[all_points[v]for v in labels]
    require(len(P)==530 and len(set(P))==530,'distinct core')
    return P,labels

def flat_mul(a,b):
    """Separate mask multiplication for direct coordinate/distance auditing."""
    out=[0]*8
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:out[i^j]+=RAD[i&j]*x*y
    return tuple(out)

def inventory(P):
    K=Field();diffs={}
    for i,j in combinations(range(len(P)),2):
        x=sub(P[j][0],P[i][0]);y=sub(P[j][1],P[i][1])
        if next(v for v in x+y if v)<0:x,y=neg(x),neg(y)
        diffs.setdefault((x,y),[]).append((i,j))
    fixed=[];roots={};ys={};eligible=0
    for (xi,yi),edges in sorted(diffs.items()):
        x=scale(xi,F(1,288));y=scale(yi,F(1,288))
        if y==Z:
            if K.mul(x,x)==ONE:fixed+=edges
            continue
        if y not in ys:ys[y]=K.sqrt(sub(ONE,K.mul(y,y)))
        r=ys[y]
        if r is None:continue
        eligible+=1
        require(K.mul(r,r)==sub(ONE,K.mul(y,y)),'square root')
        for a in set([r,neg(r)]):
            t=K.div(sub(a,x),y);u=add(x,K.mul(t,y))
            require(add(K.mul(u,u),K.mul(y,y))==ONE,'contact equation')
            roots.setdefault(t,[]).extend(edges)
    roots={t:sorted(set(es+fixed))for t,es in roots.items()}
    return sorted(fixed),dict(sorted(roots.items())),dict(pair_count=len(P)*(len(P)-1)//2,
        signed_difference_classes=len(diffs),nonzero_y_values=len(ys),
        root_eligible_difference_classes=eligible,field_events=len(roots),fixed_edges=len(fixed)),ys

def peel(n,edges):
    adj=[set()for _ in range(n)]
    for a,b in edges:require(0<=a<b<n,'edge domain');adj[a].add(b);adj[b].add(a)
    degree=list(map(len,adj));heap=[(d,i)for i,d in enumerate(degree)];heapq.heapify(heap)
    removed=set();order=[];degeneracy=0
    while heap:
        d,v=heapq.heappop(heap)
        if v in removed:continue
        require(d==degree[v],'stale degree')
        removed.add(v);order.append(v);degeneracy=max(degeneracy,d)
        for u in adj[v]-removed:degree[u]-=1;heapq.heappush(heap,(degree[u],u))
    require(len(order)==n,'incomplete peeling')
    colours={}
    for v in reversed(order):
        banned={colours[u]for u in adj[v]if u in colours}
        colours[v]=next(c for c in range(degeneracy+1)if c not in banned)
    word=''.join(str(colours[v])for v in range(n))
    require(all(word[a]!=word[b]for a,b in edges),'greedy word')
    return degeneracy,word

def phase_bytes(roots):
    return ''.join(','.join(str(F(x))for x in t)+'\n'for t in roots).encode()
