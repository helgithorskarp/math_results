"""Discover a compact rhombus, orientation and polynomial certificate."""
import argparse
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random
import time

HERE = Path(__file__).resolve().parent
P = 1000000007
USED = (0, 2, 5, 7, 9, 11, 12, 14)
Z = (F(0), F(0))
O = (F(1), F(0))


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
            f = row[p]
            if f != Z:
                row = [self.sub(a, self.mul(f,b)) for a,b in zip(row,old)]
        p = next((i for i,x in enumerate(row) if x != Z), None)
        if p is None: return basis
        f = row[p]
        return sorted(basis+[(p, [self.div(x,f) for x in row])])
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
    data = []
    for name,digest in json.loads((HERE/'inputs.json').read_text()).items():
        raw = (HERE.parent/name).read_bytes()
        if sha256(raw).hexdigest() != digest: raise ValueError('input hash')
        data.append(json.loads(raw))
    edges = [tuple(e) for e in data[0]['edges']]
    raw = data[1]['coordinates']
    coords = [[F(c) for xy in raw[str(v)] for c in xy] for v in range(509)]
    return edges, [tuple(row[j] for j in USED) for row in coords]


def rhombi(edges):
    adj = [set() for _ in range(509)]
    for u,v in edges: adj[u].add(v); adj[v].add(u)
    rows = []
    for a,b in combinations(range(509),2):
        common = sorted(adj[a]&adj[b])
        if len(common)>2: raise ValueError('source K2,3')
        if len(common)==2 and (a,b)<tuple(common): rows.append([a,b,*common])
    return rows,adj


def modular_basis(rows, order):
    basis = {}; chosen = []
    for k in order:
        a,b,c,d = rows[k]; row = {a:1,b:1,c:-1,d:-1}
        while row:
            i = min(row)
            if i not in basis:
                f = pow(row[i],-1,P)
                basis[i] = {j:x*f%P for j,x in row.items()}
                chosen.append(k); break
            f = row[i]
            for j,x in basis[i].items():
                z = (row.get(j,0)-f*x)%P
                if z: row[j]=z
                else: row.pop(j,None)
    return chosen


def obstruction(adj,u,v):
    if v in adj[u]: return {'edge':True}
    graph = [s.copy() for s in adj]
    graph[u] = (graph[u]|graph[v])-{u,v}
    for x in graph[v]: graph[x].discard(v); graph[x].add(u)
    graph[v] = set()
    for a,b in combinations((i for i in range(509) if i!=v),2):
        common = sorted(graph[a]&graph[b])
        if len(common)>=3: return {'k23':[a,b,*common[:3]]}
    raise ValueError(('unresolved exceptional pair',u,v))


def directions(edges,K):
    out = {}
    for u,v in edges:
        d = tuple(y-x for x,y in zip(K[u],K[v]))
        if next(x for x in d if x)<0: d=tuple(-x for x in d)
        if d not in out: out[d]=[u,v]
    V = list(out); index = {v:i for i,v in enumerate(V)}; triads=[]
    for i,j in combinations(range(len(V)),2):
        for sign in (-1,1):
            d = tuple(a+sign*b for a,b in zip(V[i],V[j])); orient=1
            if next((x for x in d if x),0)<0: d=tuple(-x for x in d); orient=-1
            if d in index and j<index[d]: triads.append([i,j,index[d],sign,orient])
    return V,list(out.values()),triads


def frame_certificate(K,V,triads):
    f = Field(-3); leaves=[]
    def visit(basis,signs):
        ker = f.kernel(basis,8); seen={}; pairs=[]
        for i,k in enumerate(K):
            value = tuple(f.sum((c*x,c*y) for c,(x,y) in zip(k,column)) for column in zip(*ker))
            if value in seen:
                pairs.append([seen[value],i])
                if len(pairs)==2:
                    leaves.append({'signs':signs,'pairs':pairs}); return
            else: seen[value]=i
        if len(signs)==len(triads):
            leaves.append({'signs':signs,'survivor':True}); return
        i,j,_,s,_ = triads[len(signs)]
        for sign in (-1,1):
            c = (F(-s,2),F(sign,2))
            row = [f.sub((b,F(0)),(c[0]*a,c[1]*a)) for a,b in zip(V[i],V[j])]
            visit(f.extend(basis,row),signs+[sign])
    visit([],[])
    return leaves


def polynomial_certificate(V):
    f = Field(33)
    def scale(a,s): return (a[0]*s,a[1]*s)
    def equation(v):
        a,b,c,d,e,g,h,j = v
        alpha=(a,c); beta=(e,h/3)
        # N(B),N(D),Re(conj(B)D),coeff_t(conj(B)D),b,y,d,z,1.
        return [(b*b+3*g*g,F(0)),(d*d+j*j/3,F(0)),(2*(b*d+g*j),F(0)),
                (-2*(b*j-3*g*d),F(0)),
                f.add(scale(alpha,2*b),scale(beta,6*g)),
                f.add(scale(alpha,-6*g),scale(beta,6*b)),
                f.add(scale(alpha,2*d),scale(beta,2*j)),
                f.add(scale(alpha,-2*j),scale(beta,6*d)),
                f.sub(f.add(f.mul(alpha,alpha),scale(f.mul(beta,beta),3)),O)]
    rows = [equation(v) for v in V]; basis={}
    for k,row in enumerate(rows):
        row += [O if j==k else Z for j in range(len(rows))]
        for p,old in sorted(basis.items()):
            q=row[p]
            if q!=Z: row=[f.sub(a,f.mul(q,b)) for a,b in zip(row,old)]
        p=next((i for i in range(9) if row[i]!=Z),None)
        if p is not None:
            q=row[p];basis[p]=[f.div(x,q) for x in row]
    for p in sorted(basis,reverse=True):
        for j in sorted(basis):
            if j<p and basis[j][p]!=Z:
                q=basis[j][p];basis[j]=[f.sub(a,f.mul(q,b)) for a,b in zip(basis[j],basis[p])]
    result={}
    for name,p,factor in [('norm_B_minus_5',0,O),('y',5,O),('z',7,O),('d_minus_c_b',4,(F(0),F(-1)))]:
        w=[f.mul(factor,x) for x in basis[p][9:]]
        result[name]=[[i,str(a),str(b)] for i,(a,b) in enumerate(w) if (a,b)!=Z]
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    start=time.monotonic();edges,K=inputs();rows,adj=rhombi(edges)
    orders=[list(range(len(rows))),list(reversed(range(len(rows))))]
    for seed in range(4):
        order=list(range(len(rows)));random.Random(seed).shuffle(order);orders.append(order)
    bases=[modular_basis(rows,order) for order in orders]
    common=set.intersection(*(set(b) for b in bases));exceptions=[]
    for i in sorted(common):
        a,b,c,d=rows[i]
        for u,v in [(a,b),(c,d)]: exceptions.append({'row':i,'pair':[u,v],**obstruction(adj,u,v)})
    V,witnesses,triads=directions(edges,K)
    result={'version':1,'prime':P,'bases':bases,'exceptions':exceptions,
            'direction_edges':witnesses,'triads':triads,'orientation_cover':frame_certificate(K,V,triads),
            'polynomial_combinations':polynomial_certificate(V)}
    args.out.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(result,separators=(',',':'),sort_keys=True)+'\n').encode()
    (args.out/'certificate.json').write_bytes(data)
    print(json.dumps({'certificate_bytes':len(data),'certificate_sha256':sha256(data).hexdigest(),
                      'seconds':time.monotonic()-start},sort_keys=True))

if __name__=='__main__': main()
