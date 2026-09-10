"""Exact color/difference encoding with standard-library sequential counters."""
from itertools import combinations, combinations_with_replacement
import argparse, json
from pathlib import Path

class Formula:
    def __init__(self, start=0): self.nv=start; self.clauses=[]
    def fresh(self): self.nv+=1; return self.nv
    def add(self,*lits): self.clauses.append(list(lits))
    def atmost(self, x, k):
        n=len(x)
        if k>=n:return
        if k==0:
            for v in x:self.add(-v)
            return
        if k==1:
            if n==2:self.add(-x[0],-x[1]);return
            prev=None
            for i,v in enumerate(x):
                nxt=self.fresh() if i<n-1 else None
                if nxt is not None:self.add(-v,nxt)
                if prev is not None:
                    self.add(-v,-prev)
                    if nxt is not None:self.add(-prev,nxt)
                prev=nxt
            return
        prev={}
        for i,v in enumerate(x,1):
            if i==n:
                self.add(-v,-prev[k]);break
            nxt={j:self.fresh() for j in range(1,min(i,k)+1)}
            self.add(-v,nxt[1])
            for j,p in prev.items():self.add(-p,nxt[j])
            for j in range(2,min(i,k)+1):self.add(-v,-prev[j-1],nxt[j])
            if k in prev:self.add(-v,-prev[k])
            prev=nxt
    def write(self,path):
        with Path(path).open('w') as out:
            out.write(f'p cnf {self.nv} {len(self.clauses)}\n')
            for row in self.clauses:out.write(' '.join(map(str,row))+' 0\n')

def build(domain,sizes,kind='difference',symmetry=True):
    domain=sorted(domain);q=len(sizes);n=len(domain)
    if len(set(domain))!=n or any(x<0 for x in domain) or sum(sizes)!=n or any(s<0 for s in sizes):raise ValueError('domain or sizes')
    f=Formula(n*q);idx={x:i for i,x in enumerate(domain)}
    def color(x,c):return idx[x]*q+c+1
    for x in domain:
        row=[color(x,c) for c in range(q)];f.add(*row)
        for a,b in combinations(row,2):f.add(-a,-b)
    for c,k in enumerate(sizes):f.atmost([color(x,c) for x in domain],k)
    if symmetry:
        for c in range(1,q):
            if sizes[c]!=sizes[c-1]:continue
            for i,x in enumerate(domain):f.add(-color(x,c),*[color(y,c-1) for y in domain[:i]])
    if kind=='difference':
        pairs={}
        for a,b in combinations(domain,2):pairs.setdefault(b-a,[]).append((a,b))
        for d,group in sorted(pairs.items()):
            if len(group)<2:continue
            for c in range(q):
                ps=[]
                for a,b in group:
                    v=f.fresh();ps.append(v)
                    f.add(-color(a,c),-color(b,c),v)
                    f.add(-v,color(a,c));f.add(-v,color(b,c))
                f.atmost(ps,1)
    elif kind=='sums':
        pairs={}
        for a,b in combinations_with_replacement(domain,2):pairs.setdefault(a+b,[]).append((a,b))
        edges=sorted({tuple(sorted(set(a+b))) for group in pairs.values() for a,b in combinations(group,2)})
        for edge in edges:
            for c in range(q):f.add(*[-color(x,c) for x in edge])
    else:raise ValueError('kind')
    return f,{'domain':domain,'sizes':sizes,'kind':kind,'symmetry':symmetry,'variables':f.nv,'clauses':len(f.clauses),'point_variables':n*q}

def decode(model,meta):
    yes={x for x in model if x>0};q=len(meta['sizes']);out=[[] for _ in range(q)]
    for i,x in enumerate(meta['domain']):
        cs=[c for c in range(q) if i*q+c+1 in yes]
        if len(cs)!=1:raise ValueError('point color')
        out[cs[0]].append(x)
    for c,row in enumerate(out):
        if len(row)!=meta['sizes'][c]:raise ValueError('class size')
        sums=[a+b for a,b in combinations_with_replacement(row,2)]
        if len(set(sums))!=len(sums):raise ValueError('not Sidon')
    for row in meta.get('forbidden_eleven_sets',[]):
        if any(set(part)==set(row) for part in out):raise ValueError('earlier orbit occurs')
    anchor=meta.get('anchor',[])
    if anchor:
        sums=[x+y for x,y in combinations_with_replacement(anchor,2)]
        if len(set(sums))!=len(sums) or set(anchor)&set(meta['domain']):raise ValueError('bad anchor')
        if sorted(anchor+meta['domain'])!=list(range(meta['n'])):raise ValueError('incomplete anchored domain')
    return out

def build_case(n,sizes,ordered,j,kind='difference'):
    if not 0<=j<len(ordered)//2:raise ValueError('case index')
    anchor=ordered[2*j];big=sizes[0]
    if len(anchor)!=big or not all(len(row)==big for row in ordered):raise ValueError('catalog size')
    domain=[x for x in range(n) if x not in anchor]
    f,m=build(domain,sizes[1:],kind);idx={x:i for i,x in enumerate(domain)};q=len(sizes)-1
    earlier=[row for row in ordered[:2*j] if set(row)<=set(domain)]
    for row in earlier:
        for c,size in enumerate(sizes[1:]):
            if size==big:f.add(*[-(idx[x]*q+c+1) for x in row])
    m.update({'n':n,'anchor':anchor,'case_index':j,'forbidden_eleven_sets':earlier,'clauses':len(f.clauses)})
    return f,m

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--n',type=int,default=84)
    p.add_argument('--sizes',default='11,11,11,11,10,10,10,10')
    p.add_argument('--anchor',type=Path)
    p.add_argument('--case',type=int)
    p.add_argument('--catalog',type=Path)
    p.add_argument('--weights',type=Path)
    p.add_argument('--kind',choices=['difference','sums'],default='difference')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();domain=list(range(a.n));sizes=list(map(int,a.sizes.split(',')));anchor=[]
    if a.case is not None:
        if a.anchor or not a.catalog or not a.weights:p.error('--case needs --catalog and --weights; omit --anchor')
        from orbits import orbit_catalog
        ordered=[list(map(int,l.split())) for l in a.catalog.read_text().splitlines()]
        weights=list(map(int,a.weights.read_text().split()))
        if len(weights)!=a.n or orbit_catalog(ordered,weights)!=ordered:raise ValueError('noncanonical catalog')
        f,m=build_case(a.n,sizes,ordered,a.case,a.kind)
    else:
        if a.anchor:
            anchor=list(map(int,a.anchor.read_text().split()))
            if len(set(anchor))!=len(anchor) or not set(anchor)<=set(domain) or len(anchor)!=sizes[0]:raise ValueError('anchor')
            ps=[x+y for x,y in combinations_with_replacement(anchor,2)]
            if len(set(ps))!=len(ps):raise ValueError('anchor not Sidon')
            domain=[x for x in domain if x not in anchor];sizes=sizes[1:]
        f,m=build(domain,sizes,a.kind);m.update({'n':a.n,'anchor':anchor})
    f.write(a.output);a.output.with_suffix('.json').write_text(json.dumps(m,indent=2)+'\n')
    print(json.dumps({k:m[k] for k in ['n','variables','clauses','point_variables','kind']}))
