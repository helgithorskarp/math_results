"""Discover a compact H510 rhombus, collision, orientation and polynomial certificate."""
import argparse
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random
import time

HERE = Path(__file__).resolve().parent
P = 1000000007
USED = (0, 2, 5, 7, 9, 11, 12, 14)
Z = (F(0), F(0))
O = (F(1), F(0))
ALIGN = 'hadwiger_nelson_parts509_heule_union_minimum/aligned_510.json'
UNION = 'hadwiger_nelson_parts509_heule_union_minimum/union_510.json'

class Field:
    def __init__(self, square): self.square = square
    def add(self, a, b): return (a[0]+b[0], a[1]+b[1])
    def sub(self, a, b): return (a[0]-b[0], a[1]-b[1])
    def mul(self, a, b):
        return (a[0]*b[0]+self.square*a[1]*b[1], a[0]*b[1]+a[1]*b[0])
    def div(self, a, b):
        d = b[0]*b[0]-self.square*b[1]*b[1]
        return ((a[0]*b[0]-self.square*a[1]*b[1])/d, (a[1]*b[0]-a[0]*b[1])/d)
    def sum(self, xs):
        a = Z
        for x in xs: a = self.add(a, x)
        return a
    def extend(self, basis, row):
        row = row.copy()
        for p, old in basis:
            q = row[p]
            if q != Z: row = [self.sub(a, self.mul(q,b)) for a,b in zip(row,old)]
        p = next((i for i,x in enumerate(row) if x != Z), None)
        if p is None: return basis
        q = row[p]
        return sorted(basis+[(p, [self.div(x,q) for x in row])])
    def kernel(self, basis, n):
        free = [i for i in range(n) if i not in {p for p,_ in basis}]
        out = [[Z for _ in free] for _ in range(n)]
        for j,p in enumerate(free): out[p][j] = O
        for p,row in reversed(basis):
            for j in range(len(free)):
                s = self.sum(self.mul(row[k],out[k][j]) for k in range(p+1,n))
                out[p][j] = (-s[0],-s[1])
        return out

def inputs():
    pin=json.loads((HERE/'inputs.json').read_text()); loaded={}
    for name,digest in pin.items():
        raw=(HERE.parent/name).read_bytes()
        if sha256(raw).hexdigest()!=digest: raise ValueError('input hash '+name)
        loaded[name]=json.loads(raw)
    aligned=loaded[ALIGN]['aligned_H']; union=loaded[UNION]
    if len(aligned)!=510: raise ValueError('H510 coordinate count')
    key=lambda point: tuple(tuple(axis) for axis in point)
    lookup={key(point):i for i,point in enumerate(union['points'])}
    if len(lookup)!=len(union['points']): raise ValueError('union coordinate collision')
    h_to_union=[lookup[key(point)] for point in aligned]
    if len(set(h_to_union))!=510: raise ValueError('H510 coordinate collision')
    back={u:h for h,u in enumerate(h_to_union)}
    edges=sorted((min(back[u],back[v]),max(back[u],back[v])) for u,v in union['edges'] if u in back and v in back)
    if len(edges)!=2504 or len(set(edges))!=2504: raise ValueError('H510 edge census')
    coords=[[F(c) for axis in point for c in axis] for point in aligned]
    if any(any(row[j] for j in range(16) if j not in USED) for row in coords): raise ValueError('coordinate support')
    return edges,[tuple(row[j] for j in USED) for row in coords]

def rhombi(edges):
    adj=[set() for _ in range(510)]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    rows=[]; opposite={}
    for a,b in combinations(range(510),2):
        common=sorted(adj[a]&adj[b])
        if len(common)>2: raise ValueError('source K2,3')
        if len(common)==2 and (a,b)<tuple(common):
            k=len(rows);rows.append([a,b,*common]);opposite[(a,b)]=k;opposite[tuple(common)]=k
    return rows,adj,opposite

def modular_basis(rows,order):
    basis={};chosen=[]
    for k in order:
        a,b,c,d=rows[k];row={a:1,b:1,c:P-1,d:P-1}
        while row:
            i=min(row)
            if i not in basis:
                q=pow(row[i],P-2,P);basis[i]={j:x*q%P for j,x in row.items()};chosen.append(k);break
            q=row[i]
            for j,x in basis[i].items():
                z=(row.get(j,0)-q*x)%P
                if z:row[j]=z
                else:row.pop(j,None)
    return chosen

def quotient_k23(adj, collision_pairs):
    parent=list(range(510))
    def find(x):
        while parent[x]!=x: parent[x]=parent[parent[x]];x=parent[x]
        return x
    def unite(a,b):
        a,b=find(a),find(b)
        if a!=b:parent[b]=a
    for a,b in collision_pairs:unite(a,b)
    if any(find(a)==find(b) for a in range(510) for b in adj[a] if a<b): raise ValueError('edge collapsed')
    reps=sorted({find(v) for v in range(510)}); index={r:i for i,r in enumerate(reps)}
    qadj=[set() for _ in reps]
    for u in range(510):
        for v in adj[u]:
            a,b=index[find(u)],index[find(v)]
            if a!=b:qadj[a].add(b)
    for a,b in combinations(range(len(reps)),2):
        common=sorted(qadj[a]&qadj[b])
        if len(common)>=3:return [reps[a],reps[b],reps[common[0]],reps[common[1]],reps[common[2]]]
    raise ValueError('exceptional collision has no K2,3')

def rank_certificate(rows,adj,opposite):
    orders=[list(range(len(rows))),list(reversed(range(len(rows))))]
    for seed in range(18):
        order=list(range(len(rows)));random.Random(seed).shuffle(order);orders.append(order)
    bases=[modular_basis(rows,order) for order in orders]
    if any(len(b)!=501 for b in bases):raise ValueError('rhombus rank')
    sets=list(map(set,bases));allmask=(1<<len(bases))-1
    masks=[sum(1<<i for i,b in enumerate(sets) if r in b) for r in range(len(rows))]
    hits=[]
    for r,s in combinations(range(len(rows)),2):
        if masks[r]|masks[s]==allmask:hits.append((r,s))
    exceptions=[]
    for r,s in hits:
        cases=[]
        for p in (rows[r][:2],rows[r][2:]):
            for q in (rows[s][:2],rows[s][2:]):
                cases.append({'pairs':[p,q],'k23':quotient_k23(adj,[p,q])})
        exceptions.append({'rows':[r,s],'cases':cases})
    # A triple collision can invalidate three identities, one for each pair.
    # Record the complete opposition-triangle census and those hitting all bases.
    graph=[set() for _ in range(510)]
    for u,v in opposite:graph[u].add(v);graph[v].add(u)
    triangle_hits=[];triangle_count=0
    for u in range(510):
        for v in sorted(x for x in graph[u] if x>u):
            for w in sorted(x for x in graph[u]&graph[v] if x>v):
                triangle_count+=1
                ids=sorted({opposite[(u,v)],opposite[(u,w)],opposite[(v,w)]})
                if len(ids)!=3:raise ValueError('repeated triangle identity')
                if masks[ids[0]]|masks[ids[1]]|masks[ids[2]]==allmask:
                    triangle_hits.append({'vertices':[u,v,w],'rows':ids})
    if len(hits)!=2 or len(triangle_hits)!=2:raise ValueError(('unexpected rank exceptions',hits,triangle_hits))
    return bases,exceptions,triangle_count,triangle_hits

def directions(edges,K):
    out={}
    for u,v in edges:
        d=tuple(y-x for x,y in zip(K[u],K[v]))
        if next(x for x in d if x)<0:d=tuple(-x for x in d)
        if d not in out:out[d]=[u,v]
    V=list(out);index={v:i for i,v in enumerate(V)};triads=[]
    for i,j in combinations(range(len(V)),2):
        for sign in (-1,1):
            d=tuple(a+sign*b for a,b in zip(V[i],V[j]));orient=1
            if next((x for x in d if x),0)<0:d=tuple(-x for x in d);orient=-1
            if d in index and j<index[d]:triads.append([i,j,index[d],sign,orient])
    return V,list(out.values()),triads

def forced_groups(K,ker):
    field=Field(-3);groups=defaultdict(list)
    for i,k in enumerate(K):
        value=tuple(field.sum((c*x,c*y) for c,(x,y) in zip(k,column)) for column in zip(*ker))
        groups[value].append(i)
    return sorted((g for g in groups.values() if len(g)>1),key=lambda g:(-len(g),g))

def frame_certificate(K,V,triads):
    f=Field(-3);leaves=[]
    def visit(basis,signs):
        groups=forced_groups(K,f.kernel(basis,8));loss=sum(len(g)-1 for g in groups)
        if loss>=3:
            pairs=[]
            for g in groups:
                for x in g[1:]:
                    pairs.append([g[0],x])
                    if len(pairs)==3:break
                if len(pairs)==3:break
            leaves.append({'signs':signs,'pairs':pairs});return
        if len(signs)==len(triads):
            leaves.append({'signs':signs,'survivor':True});return
        i,j,_,s,_=triads[len(signs)]
        for sign in (-1,1):
            c=(F(-s,2),F(sign,2));row=[f.sub((b,F(0)),(c[0]*a,c[1]*a)) for a,b in zip(V[i],V[j])]
            visit(f.extend(basis,row),signs+[sign])
    visit([],[])
    return leaves

def polynomial_certificate(V):
    f=Field(33)
    def scale(a,s):return(a[0]*s,a[1]*s)
    def equation(v):
        a,b,c,d,e,g,h,j=v;alpha=(a,c);beta=(e,h/3)
        return [(b*b+3*g*g,F(0)),(d*d+j*j/3,F(0)),(2*(b*d+g*j),F(0)),
                (-2*(b*j-3*g*d),F(0)),f.add(scale(alpha,2*b),scale(beta,6*g)),
                f.add(scale(alpha,-6*g),scale(beta,6*b)),f.add(scale(alpha,2*d),scale(beta,2*j)),
                f.add(scale(alpha,-2*j),scale(beta,6*d)),f.sub(f.add(f.mul(alpha,alpha),scale(f.mul(beta,beta),3)),O)]
    rows=[equation(v) for v in V];basis={}
    for k,row in enumerate(rows):
        row += [O if j==k else Z for j in range(len(rows))]
        for p,old in sorted(basis.items()):
            q=row[p]
            if q!=Z:row=[f.sub(a,f.mul(q,b)) for a,b in zip(row,old)]
        p=next((i for i in range(9) if row[i]!=Z),None)
        if p is not None:
            q=row[p];basis[p]=[f.div(x,q) for x in row]
    for p in sorted(basis,reverse=True):
        for j in sorted(basis):
            if j<p and basis[j][p]!=Z:
                q=basis[j][p];basis[j]=[f.sub(a,f.mul(q,b)) for a,b in zip(basis[j],basis[p])]
    result={}
    for name,p,factor in [('norm_B_minus_5',0,O),('y',5,O),('z',7,O),('d_minus_c_b',4,(F(0),F(-1)))]:
        weights=[f.mul(factor,x) for x in basis[p][9:]]
        result[name]=[[i,str(a),str(b)] for i,(a,b) in enumerate(weights) if (a,b)!=Z]
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    start=time.monotonic();edges,K=inputs();rows,adj,opposite=rhombi(edges)
    bases,exceptions,triangle_count,triangle_hits=rank_certificate(rows,adj,opposite)
    V,witnesses,triads=directions(edges,K)
    result={'version':1,'prime':P,'bases':bases,'rank_exceptions':exceptions,
            'opposition_triangle_count':triangle_count,'opposition_triangle_hits':triangle_hits,
            'direction_edges':witnesses,'triads':triads,'orientation_cover':frame_certificate(K,V,triads),
            'polynomial_combinations':polynomial_certificate(V)}
    args.out.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(result,separators=(',',':'),sort_keys=True)+'\n').encode()
    (args.out/'certificate.json').write_bytes(data)
    print(json.dumps({'certificate_bytes':len(data),'certificate_sha256':sha256(data).hexdigest(),'seconds':time.monotonic()-start},sort_keys=True))
if __name__=='__main__':main()
