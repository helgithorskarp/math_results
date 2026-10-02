"""Literal matrix/Bernstein audit and pair-quotient/undirected ring audit.

Imports neither producer nor dense polynomial helper. Same-author
different algorithms; not independent researcher review.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json,hashlib

def require(x,m):
    if not x:raise ValueError(m)
def read(p):
    require(isinstance(p,list) and all(type(s) is str for s in p),'rational-string polynomial')
    values=[F(s) for s in p];require(not values or values[-1]!=0,'trimmed polynomial')
    return {i:v for i,v in enumerate(values) if v}
def plus(*ps):
    out={}
    for p in ps:
        for i,v in p.items():out[i]=out.get(i,F(0))+v
    return {i:v for i,v in out.items() if v}
def scale(p,c):return {i:v*c for i,v in p.items() if v*c}
def neg(p):return scale(p,-1)
def times(a,b):
    out={}
    for i,x in a.items():
        for j,y in b.items():out[i+j]=out.get(i+j,F(0))+x*y
    return {i:v for i,v in out.items() if v}
def power(p,n):
    out={0:F(1)}
    for _ in range(n):out=times(out,p)
    return out
Z={};O={0:F(1)};R={1:F(1)}
LO,HI=F(2,3),F(3,4)
I=[[O if i==j else Z for j in range(3)] for i in range(3)]
T3=[[Z,O,Z],[neg(R),plus(R,power(R,2)),plus(power(R,2),neg(O))],[neg(O),R,R]]
T4=[[Z,O,Z],[plus(O,neg(power(R,2))),plus(power(R,2),power(R,3)),plus(power(R,3),scale(R,-2))],
    [neg(R),plus(R,power(R,2)),plus(power(R,2),neg(O))]]
def matmul(a,b):
    return [[plus(*(times(a[i][k],b[k][j]) for k in range(3))) for j in range(3)] for i in range(3)]
def transfer(word):
    m=I
    for n in word:m=matmul(T3 if n==3 else T4,m)
    return m
def bernstein_identity(g,strings):
    require(bool(g),'nonzero contact obstruction')
    b=list(map(F,strings));n=max(g)
    require(len(b)==n+1 and (all(v>0 for v in b) or all(v<0 for v in b)),'strict Bernstein signs including endpoints')
    u={0:-LO/(HI-LO),1:1/(HI-LO)};v={0:HI/(HI-LO),1:-1/(HI-LO)}
    expanded=plus(*(scale(times(power(u,k),power(v,n-k)),comb(n,k)*b[k]) for k in range(n+1)))
    require(expanded==g,'literal Bernstein basis expansion')
def token(v):return str(v[0])+':'+str(v[1])
def canonical_cycle(cycle):
    require(len(cycle)==len(set(cycle)) and len(cycle)>=3,'simple boundary cycle')
    options=[]
    for direction in (cycle,list(reversed(cycle))):
        k=direction.index(min(direction));options.append(tuple(direction[k:]+direction[:k]))
    return min(options)

def audit_ring(row):
    sides=tuple(row['sides']);ports=tuple(row['ports'])
    require(len(sides)==len(ports)==3 and all(q in (4,5) for q in sides),'three Q/P disks')
    require(all(2<=k<=q-2 for q,k in zip(sides,ports)),'disjoint incoming/outgoing edge ends')
    original={(i,j) for i,q in enumerate(sides) for j in range(q)};partner={}
    # Literal disjoint pair identifications; no union-find or producer walk.
    for i,k in enumerate(ports):
        pairs=[((i,k),((i+1)%3,1)),((i,k+1),((i+1)%3,0))]
        for a,b in pairs:
            require(a in original and b in original and a not in partner and b not in partner,'six disjoint identification pairs')
            partner[a]=b;partner[b]=a
    rep={v:min(v,partner.get(v,v)) for v in original}
    classes={}
    for v in sorted(original):classes.setdefault(rep[v],[]).append(token(v))
    expected_classes=[v for k,v in sorted(classes.items())]
    require(row['classes']==expected_classes,'every labeled quotient class')
    arcs=[];neighbors={v:set() for v in classes}
    for i,q in enumerate(sides):
        for j in range(q):
            if j in (0,ports[i]):continue
            a,b=rep[(i,j)],rep[(i,(j+1)%q)]
            require(a!=b and b not in neighbors[a],'simple noncollapsed boundary edge')
            neighbors[a].add(b);neighbors[b].add(a);arcs.append([token(a),token(b)])
    require(row['boundary_arcs']==sorted(arcs),'every oriented boundary arc')
    require(all(len(ns)==2 for ns in neighbors.values()),'undirected boundary degree two')
    unseen=set(neighbors);cycles=[];mixed=[]
    while unseen:
        start=min(unseen);previous=None;current=start;cycle=[]
        while current not in cycle:
            require(current in unseen,'disjoint boundary components');unseen.remove(current);cycle.append(current)
            candidates=neighbors[current]-({previous} if previous is not None else set())
            nxt=min(candidates);previous,current=current,nxt
        require(current==start,'undirected walk returns to its own start')
        cycles.append([token(v) for v in cycle]);mixed.append(sum(len(classes[v])==2 for v in cycle))
    actual_cycles=sorted(canonical_cycle(c) for c in cycles)
    supplied_cycles=sorted(canonical_cycle(c) for c in row['boundary_cycles'])
    require(supplied_cycles==actual_cycles,'entire boundary cycles, up to direction/start')
    require(len(cycles)==2 and mixed==[3,3] and row['mixed_corners_per_boundary']==[3,3],'three mixed corners on each of exactly two boundaries')
    require(row['vertices']==len(classes)==sum(sides)-6 and len(arcs)==len(classes),'every vertex lies on the boundary')
    return {'pentagons':sum(q==5 for q in sides),'lengths':tuple(sorted(map(len,cycles)))}

def verify(data):
    require(data['format']==1 and data['c_band']==['1/2','3/5'] and data['r_band']==['2/3','3/4'],'exact closed mathematical domain')
    expected={(q,tuple(3+(mask>>j&1) for j in range(q-2))) for q in (4,5) for mask in range(2**(q-2))}
    seen=set();positions=0
    for row in data['closure']:
        key=row['sides'],tuple(row['word']);require(key in expected and key not in seen,'complete unique closing word domain');seen.add(key)
        vector=transfer(row['word'])[1]
        require([read(p) for p in row['final_boundary_vector']]==vector,'every final boundary coordinate')
        # Alternative Gram weighting: (2-r)*(1-c)=2-2r, (2-r)*c=r.
        g=plus(times(plus(scale(O,2),scale(R,-2)),vector[0]),times(R,plus(*vector)),neg(R))
        require(read(row['contact_polynomial'])==g,'literal closing contact polynomial')
        bernstein_identity(g,row['bernstein'])
        positions+=sum(max(p,default=-1)+1 for p in vector)
    require(seen==expected,'all12 closing words')
    # Enumerate the independent literal ring domain using integer decoding.
    ring_domain=set()
    for types in range(8):
        q=tuple(4+(types>>i&1) for i in range(3))
        for k0 in range(2,q[0]-1):
            for k1 in range(2,q[1]-1):
                for k2 in range(2,q[2]-1):ring_domain.add((q,(k0,k1,k2)))
    rings_seen=set();counts={}
    for row in data['rings']:
        key=tuple(row['sides']),tuple(row['ports']);require(key in ring_domain and key not in rings_seen,'complete unique ring domain');rings_seen.add(key)
        result=audit_ring(row);tag=result['pentagons'],result['lengths'];counts[tag]=counts.get(tag,0)+1
    require(rings_seen==ring_domain and len(rings_seen)==27,'entire27-port domain')
    return {'closing_contact_cases':12,'full_band_exclusions':12,'closure_coordinate_coefficient_positions':positions,
            'oriented_ring_cases':27,'boundary_cycles':54,'each_boundary_has_three_mixed_corners':True,
            'ring_counts':[{'pentagons':tag[0],'lengths':list(tag[1]),'cases':n} for tag,n in sorted(counts.items())]}

if __name__=='__main__':
    raw=Path(__file__).with_name('CERTIFICATE.json').read_bytes();out=verify(json.loads(raw));out['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    print(json.dumps(out,sort_keys=True))
