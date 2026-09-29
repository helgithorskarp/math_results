#!/usr/bin/env python3
"""Independent exact replay of the two distributed-shortcut price certificates.

Only certificate JSON is imported from the target contribution.  The cube,
geodesic catalog, clauses, Farkas checks, and RUP engine are rebuilt here.
Python 3.11+, standard library, assertions enabled.
"""

from collections import deque
from fractions import Fraction
from functools import reduce
from itertools import combinations
from math import gcd, lcm
from pathlib import Path
import hashlib
import json

SOURCE = Path(__file__).resolve().parents[1] / "planar_two_geodesic_cube_price_boxes"
PRICE = {
    "A": (14,38,7,23,20,17,8,30,11,21,14,29,10,28,36,4,3,7,30,6,2,4,9,5),
    "B": (7,10,4,8,7,11,9,6,16,14,3,23,3,16,15,16,3,10,22,9,12,3,12,7),
}
SC = ((10,14),(10,22),(11,19),(12,14),(12,19),(13,22))
MARKS = (15,16,17,18,20,21,23,24,25)
CORE = tuple(sorted(set(range(14)) | {14,19,22}))
EXPECTED_HASH = {
    "A": "2dda2d05a52f6720832c9e12f58f3ec60c3a1acebf1c9bb51c15c71e3afe72f5",
    "B": "8d8f7f8b6c3476fec541d41b01c2328c687d99f27b474f7e781129bc43321ce9",
    "U": "fb7cc26f4ee1f95f0089d095fcca242202e03a4e93390427704bbc426b87dc1d",
}


def cube():
    adj = [set() for _ in range(26)]
    triangles = []
    radial = []
    def edge(a, b):
        adj[a].add(b)
        adj[b].add(a)
    for v in range(8):
        for axis in range(3):
            f = 8 + 2*axis + ((v >> axis) & 1)
            edge(v, f)
            radial.append((v, f))
    ce = [(a,b) for a,b in combinations(range(8),2) if a ^ b in (1,2,4)]
    for z,(a,b) in enumerate(ce,14):
        axis = (a ^ b).bit_length()-1
        edge(a,z); edge(b,z)
        for other in range(3):
            if other == axis: continue
            f = 8 + 2*other + ((a >> other) & 1)
            edge(z,f)
            triangles.extend(((a,z,f),(b,z,f)))
    edges = {tuple(sorted((a,b))) for a in range(26) for b in adj[a]}
    assert len(edges)==72 and len(triangles)==48 and len(radial)==24
    incid = {e:0 for e in edges}
    for t in triangles:
        for a,b in ((t[0],t[1]),(t[1],t[2]),(t[2],t[0])):
            incid[tuple(sorted((a,b)))] += 1
    assert set(incid.values())=={2} and 26-72+48==2
    for v in range(26):
        links = {u:set() for u in adj[v]}
        for t in triangles:
            if v in t:
                a,b = (u for u in t if u != v)
                links[a].add(b); links[b].add(a)
        assert all(len(ns)==2 for ns in links.values())
        seen={next(iter(links))}; todo=list(seen)
        while todo:
            for u in links[todo.pop()]-seen:
                seen.add(u); todo.append(u)
        assert seen==adj[v]
    assert set(SC)<=edges and all(len(adj[z])==4 for z in MARKS)
    return adj,tuple(sorted(radial))


ADJ,RADIAL=cube()
VARIABLES=RADIAL+SC
INDEX={e:i for i,e in enumerate(VARIABLES)}
assert len(VARIABLES)==30


def incidence(path):
    v=[0]*31
    for a,b in zip(path,path[1:]): v[INDEX[tuple(sorted((a,b)))]]+=1
    return tuple(v)


def radial_profile(price):
    graph=[[] for _ in range(14)]
    for e,w in zip(RADIAL,price):
        a,b=e; graph[a].append((b,w)); graph[b].append((a,w))
    distances=[]; paths={}; cone=set()
    for source in range(14):
        d=[None]*14; d[source]=0; queue=deque([source])
        while queue:
            u=queue.popleft()
            for v,w in graph[u]:
                nd=d[u]+w
                if d[v] is None or nd<d[v]: d[v]=nd; queue.append(v)
        assert all(x is not None for x in d)
        distances.append(d)
        for target in range(14):
            path=[target]
            while path[-1]!=source:
                options=[u for u,w in graph[path[-1]] if d[u]+w==d[path[-1]]]
                assert len(options)==1
                path.append(options[0])
            paths[source,target]=tuple(reversed(path))
        potentials={v:incidence(paths[source,v]) for v in range(14)}
        for i,(a,b) in enumerate(RADIAL):
            for u,v in ((a,b),(b,a)):
                row=[x-y for x,y in zip(potentials[u],potentials[v])]
                row[i]+=1
                if any(row):
                    assert sum(x*y for x,y in zip(row,price))>0
                    cone.add(tuple(row))
                else:
                    assert paths[source,u]+(v,)==paths[source,v]
    return distances,sorted(cone)


def routes(price,d):
    g={v:set() for v in CORE}
    for a,b in VARIABLES: g[a].add(b); g[b].add(a)
    found={(a,b):[] for a in CORE for b in CORE if a<=b}
    for s in CORE:
        def walk(path,anchor,spent):
            v=path[-1]
            if v>=s: found[s,v].append(tuple(path))
            for u in sorted(g[v]):
                if u in path: continue
                if v<14 and u<14:
                    length=spent+price[INDEX[tuple(sorted((u,v)))]]
                    if length==d[anchor][u]: walk(path+[u],anchor,length)
                elif u<14: walk(path+[u],u,0)
                else: walk(path+[u],None,0)
        walk([s],s if s<14 else None,0)
    assert all(found.values())
    return found


def components(deleted):
    left=set(range(26))-deleted; out=[]
    while left:
        s=left.pop(); part={s}; todo=[s]
        while todo:
            new=ADJ[todo.pop()] & left
            left.difference_update(new); part.update(new); todo.extend(new)
        out.append(part)
    return out


def primitive(values):
    values=list(map(Fraction,values))
    scale=lcm(*(x.denominator for x in values))
    ints=[int(x*scale) for x in values]
    g=reduce(gcd,(abs(x) for x in ints),0)
    return tuple(x//g for x in ints) if g else tuple(ints)


class CNF:
    def __init__(self):
        self.next=1; self.atom_ids={}; self.forms={}; self.clauses=[]
    def new(self):
        answer=self.next; self.next+=1; return answer
    def atom(self,form):
        form=primitive(form)
        if all(x==0 for x in form[:-1]): return form[-1]>=0
        if form not in self.atom_ids:
            n=self.new(); self.atom_ids[form]=n; self.forms[n]=form
        return self.atom_ids[form]
    def ge(self,form,strict=False):
        if strict:
            a=self.atom([-x for x in form]); return not a if type(a) is bool else -a
        return self.atom(form)
    def add(self,lits):
        if any(x is True for x in lits): return
        row=set(x for x in lits if x is not False)
        if any(-x in row for x in row): return
        self.clauses.append(tuple(sorted(row)))


def rup(base,steps,nvars):
    db=list(base)
    for row in steps:
        assert len(set(row))==len(row) and all(type(x) is int and 1<=abs(x)<=nvars for x in row)
        values={};todo=deque(-x for x in row); contradiction=False
        while True:
            while todo:
                lit=todo.popleft(); name=abs(lit); value=lit>0
                if name in values and values[name]!=value:
                    contradiction=True; break
                values[name]=value
            if contradiction: break
            changed=False
            for clause in db:
                if any(abs(x) in values and values[abs(x)]==(x>0) for x in clause): continue
                unknown=[x for x in clause if abs(x) not in values]
                if not unknown: contradiction=True; break
                if len(unknown)==1: todo.append(unknown[0]); changed=True
            if contradiction or not changed: break
        assert contradiction,('bad RUP',row)
        db.append(tuple(row))
    assert steps and steps[-1]==[]
    return len(steps)


def evaluate(name,data):
    price=PRICE[name]; radius=Fraction(data['relative_radius'])
    assert data['metric']==name and radius==Fraction(1,57 if name=='A' else 32)
    distances,cone=radial_profile(price)
    safe=min(Fraction(sum(x*y for x,y in zip(c,price)),sum(abs(x)*y for x,y in zip(c,price))) for c in cone)
    assert safe==radius
    catalog=routes(price,distances)
    catalog_sets={k:set(v) for k,v in catalog.items()}
    enc=CNF()
    parents={(z,p):enc.new() for z in MARKS for p in sorted(ADJ[z])}
    for z in MARKS:
        group=[parents[z,p] for p in sorted(ADJ[z])]
        enc.add(group)
        for a,b in combinations(group,2): enc.add([-a,-b])
    for i in range(30):
        row=[0]*31; row[i]=1; enc.add([enc.ge(row,True)])
    for row in cone: enc.add([enc.ge(row,True)])
    for i,p in enumerate(price):
        lower=[Fraction(0)]*31; lower[i]=1; lower[-1]=-(1-radius)*p
        upper=[Fraction(0)]*31; upper[i]=-1; upper[-1]=(1+radius)*p
        enc.add([enc.ge(lower)]); enc.add([enc.ge(upper)])
    for pair in data['pairs']:
        assert len(pair)==2 and all(len(c & set(MARKS))<=4 for c in components(set(pair[0])|set(pair[1])))
        needed=set(); middle_paths=[]
        for path in pair:
            assert path and len(path)==len(set(path)) and all(0<=v<26 for v in path)
            assert all(v in ADJ[u] for u,v in zip(path,path[1:]))
            assert all(v in CORE for v in path[1:-1])
            if len(path)>1 and path[0] in MARKS: needed.add((path[0],path[1]))
            if len(path)>1 and path[-1] in MARKS: needed.add((path[-1],path[-2]))
            middle=tuple(v for v in path if v in CORE)
            if not middle:
                assert len(path)==1 and path[0] in MARKS
            else:
                if middle[0]>middle[-1]: middle=middle[::-1]
                assert middle in catalog_sets[middle[0],middle[-1]]
                middle_paths.append(middle)
        clause=[-parents[z,p] for z,p in sorted(needed)]
        for path in middle_paths:
            left=incidence(path)
            for other in catalog[path[0],path[-1]]:
                right=incidence(other)
                clause.append(enc.ge([a-b for a,b in zip(left,right)],True))
        enc.add(clause)
    base_clauses=len(enc.clauses)
    assert not data['extra_linear_atoms']
    strict_zeros=0
    for row in data['farkas']:
        total=[Fraction(0)]*31; strict=False
        for lit,txt in row:
            weight=Fraction(txt)
            assert weight>0 and abs(lit) in enc.forms
            sign=1 if lit>0 else -1
            form=enc.forms[abs(lit)]
            total=[a+sign*weight*b for a,b in zip(total,form)]
            strict |= lit<0
        assert all(x==0 for x in total[:-1])
        assert total[-1]<0 or (total[-1]==0 and strict)
        strict_zeros += total[-1]==0
        enc.add([-lit for lit,_ in row])
    steps=rup(enc.clauses,data['rup'],enc.next-1)
    return (len(cone),sum(map(len,catalog.values())),len(data['pairs']),
            base_clauses,len(enc.forms),len(data['farkas']),strict_zeros,steps)


def unit(data):
    assert data['mark']==15 and len(data['templates'])==4
    graph={v:[] for v in CORE}
    for (a,b),w in list(zip(RADIAL,[1]*24))+list(zip(SC,[0]*6)):
        graph[a].append((b,w)); graph[b].append((a,w))
    distances={}
    for s in CORE:
        d={s:0};q=deque([s])
        while q:
            u=q.popleft()
            for v,w in graph[u]:
                if v not in d or d[u]+w<d[v]: d[v]=d[u]+w;q.append(v)
        distances[s]=d
    assert {r['parent'] for r in data['templates']}==ADJ[15]
    for row in data['templates']:
        assert len(row['paths'])==2
        for path in row['paths']:
            assert len(path)==len(set(path)) and all(v in ADJ[u] for u,v in zip(path,path[1:]))
            p=list(path)
            if p[0] in MARKS:
                assert p[0]==15 and p[1]==row['parent'];p.pop(0)
            if p[-1] in MARKS:
                assert p[-1]==15 and p[-2]==row['parent'];p.pop()
            assert all(v<14 for v in p) and len(p)-1==distances[p[0]][p[-1]]
        sizes=sorted(len(c & set(MARKS)) for c in components(set(row['paths'][0])|set(row['paths'][1])))
        assert sizes==row['component_masses']==[4,4]


def main():
    # A genuinely zero non-Q edge is possible under the proved relaxation:
    # choose 25--11 as a zero parent, set all shortcuts to zero, and follow
    # the zero shortcut chain from 11 to 13.  Edge 25--13 is in T but not Q.
    assert 13 in ADJ[25] and (13,25) not in VARIABLES
    assert all(tuple(sorted(e)) in SC for e in
               ((11,19),(19,12),(12,14),(14,10),(10,22),(22,13)))
    results={}
    for name in ('A','B','U'):
        path=SOURCE/f'certificate_{name}.json'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED_HASH[name]
        data=json.loads(path.read_text())
        results[name]=unit(data) if name=='U' else evaluate(name,data)
    assert results['A'][:6]==(205,1176,47,393,599,437)
    assert results['B'][:6]==(199,1226,67,407,659,723)
    assert results['A'][-1]==48 and results['B'][-1]==142
    print(f"A={results['A']} B={results['B']} unit_templates=4 PASS")


if __name__=='__main__': main()
