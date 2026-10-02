"""Exact two-adjacent-free-corner closure and three-face port catalog.

Actual author six-tammes-1, researcher. No realization or global profile
coverage is supplied by the finite gluing catalog. See PROOF.md.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse,json,hashlib
from poly import add,sub,mul,bernstein

R=[Q(0),Q(1)];O=[Q(1)];Z=[];D=[Q(2),Q(-1)]
E0=(O,Z,Z);E1=(Z,O,Z);E2=(Z,Z,O)
LO,HI=Q(2,3),Q(3,4)
def require(x,m):
    if not x:raise ValueError(m)
def reflect(center,now,before):
    return tuple(sub(mul(R,add(x,y)),z) for x,y,z in zip(center,now,before))
def fan(previous,current,outside,m):
    a,b=previous,outside
    for _ in range(m-1):a,b=b,reflect(current,b,a)
    return current,b,a
def enc(p):return [str(x) for x in p]
def vertex(v):return str(v[0])+':'+str(v[1])

def closing(word):
    state=E0,E1,E2
    for m in word:state=fan(*state,m)
    v=state[1]
    g=sub(add(mul(D,v[0]),mul(R,add(v[1],v[2]))),R)
    b=bernstein(g,LO,HI)
    require(all(x>0 for x in b) or all(x<0 for x in b),'strict whole-band closing-contact gap')
    return {'word':list(word),'final_boundary_vector':[enc(p) for p in v],
            'contact_polynomial':enc(g),'bernstein':enc(b)}

def ring(sides,ports):
    original=[(i,j) for i,q in enumerate(sides) for j in range(q)]
    parent={v:v for v in original}
    def find(v):
        while parent[v]!=v:v=parent[v]
        return v
    def join(a,b):
        a,b=find(a),find(b)
        if a!=b:parent[max(a,b)]=min(a,b)
    for i,k in enumerate(ports):
        nxt=(i+1)%3
        join((i,k),(nxt,1));join((i,k+1),(nxt,0))
    classes={}
    for v in original:classes.setdefault(find(v),[]).append(v)
    require(all(len(v) in (1,2) for v in classes.values()),'no triple point')
    arcs=[];successor={}
    for i,q in enumerate(sides):
        for j in range(q):
            if j in (0,ports[i]):continue
            a,b=find((i,j)),find((i,(j+1)%q))
            require(a not in successor,'unbranched oriented boundary')
            successor[a]=b;arcs.append((a,b))
    require(set(successor)==set(successor.values())==set(classes),'every quotient vertex is a boundary vertex')
    unseen=set(successor);cycles=[]
    while unseen:
        start=min(unseen);v=start;cycle=[]
        while v in unseen:
            unseen.remove(v);cycle.append(v);v=successor[v]
        require(v==start,'boundary closes')
        cycles.append(cycle)
    mixed=[sum(len(classes[v])==2 for v in cycle) for cycle in cycles]
    require(len(cycles)==2 and mixed==[3,3],'two boundary cycles, three mixed corners each')
    require(len(classes)==sum(sides)-6 and len(arcs)==sum(sides)-6,'whole region vertex/boundary count')
    return {'sides':list(sides),'ports':list(ports),
            'classes':[[vertex(v) for v in vs] for key,vs in sorted(classes.items())],
            'boundary_arcs':[[vertex(a),vertex(b)] for a,b in sorted(arcs)],
            'boundary_cycles':[[vertex(v) for v in cycle] for cycle in cycles],
            'mixed_corners_per_boundary':mixed,'vertices':len(classes)}

def certificate():
    closures=[];rings=[]
    for q in (4,5):
        for word in product((3,4),repeat=q-2):closures.append({'sides':q,**closing(word)})
    for sides in product((4,5),repeat=3):
        for ports in product(*(range(2,q-1) for q in sides)):rings.append(ring(sides,ports))
    require(len(closures)==12 and len(rings)==27,'complete unquotiented domains')
    return {'format':1,'actual_agent':'six-tammes-1','role':'researcher',
            'c_band':['1/2','3/5'],'r_band':['2/3','3/4'],'closure':closures,'rings':rings}

def main():
    p=argparse.ArgumentParser();p.add_argument('--emit',type=Path);args=p.parse_args()
    data=certificate();raw=json.dumps(data,sort_keys=True,separators=(',',':'))+'\n'
    if args.emit:args.emit.write_text(raw)
    else:require(Path(__file__).with_name('CERTIFICATE.json').read_text()==raw,'entire certificate regeneration')
    print(json.dumps({'closing_contact_cases':12,'strict_full_band_exclusions':12,
                      'oriented_ring_cases':27,'ring_boundaries_each_with_three_mixed_corners':54,
                      'certificate_sha256':hashlib.sha256(raw.encode()).hexdigest()},sort_keys=True))
if __name__=='__main__':main()
