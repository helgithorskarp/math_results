"""Exact labelled facial chart of two credited Tammes-15 incumbents.

six-tammes-1, researcher. Uses the pinned published E arithmetic (peer,
source58d66bf) only as an exact arithmetic layer; no solver or floats.
The written noncrossing/rotation-to-physical-face bridge is separate.
"""
from pathlib import Path
from functools import cmp_to_key
from itertools import combinations
from collections import Counter
import sys, json, hashlib

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inputs'))
from arithmetic import E,T,ZERO,ONE,verify_root

def require(p,m):
    if not p: raise ValueError(m)

def dot(x,y):
    return (1-T)*sum((a*b for a,b in zip(x,y)),ZERO)+T*sum(x,ZERO)*sum(y,ZERO)

def det(x,y,z):
    return x[0]*(y[1]*z[2]-y[2]*z[1])-x[1]*(y[0]*z[2]-y[2]*z[0])+x[2]*(y[0]*z[1]-y[1]*z[0])

def canonical(cycle):
    return min(tuple(cycle[k:]+cycle[:k]) for k in range(len(cycle)))

def unoriented(cycle):
    return min(canonical(list(cycle)),canonical(list(reversed(cycle))))

def construction():
    a=E(['-27/2','-3','35','-24','117/2'])
    b=E(['-31/4','-19/2','34','-53/2','195/4'])
    c=E(['81/4','21/2','-69','101/2','-429/4'])
    M=((a,b,c),(c,a,b),(b,c,a))
    V={i:tuple(ONE if j==k else ZERO for j in range(3)) for k,i in enumerate((0,5,11))}
    for j,i in enumerate((1,2,4)):
        V[i]=tuple(M[k][j]/(1-T)-T*sum((M[n][j] for n in range(3)),ZERO)/((1-T)*(1+2*T)) for k in range(3))
    r=2*T/(1+T)
    steps=((6,0,11,5),(7,0,5,11),(9,5,11,0),(8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4),(3,1,4,2),(14,0,6,11))
    for n,i,j,o in steps:
        V[n]=tuple(r*(x+y)-z for x,y,z in zip(V[i],V[j],V[o]))
    require(set(V)==set(range(15)),'full labelled construction')
    published=json.loads((ROOT/'inputs/fourteen-certificate.json').read_text())
    ref=[tuple(E(q) for q in p) for p in published['incumbent_vectors']]
    require(all(V[i]==ref[i] for i in range(15)),'reconstructed exact published coordinates')
    alt=tuple(E(q) for q in published['alternate_vector'])
    return [V[i] for i in range(15)],alt

TRIANGLES=((2,10,1),(2,1,4),(2,4,8),(2,8,13),(1,10,12),(0,5,11),(0,11,6),(5,0,7),(11,5,9))
PENTAGON=(12,10,9,5,7)

def chart(V):
    require(all(dot(p,p)==ONE for p in V),'all15 exact unit points')
    pair_signs={}
    edges=[]
    for i,j in combinations(range(15),2):
        s=(dot(V[i],V[j])-T).sign()
        require(s<=0,'packing inequality')
        pair_signs[(i,j)]=s
        if s==0: edges.append((i,j))
    rotation={};orientation_records=[]
    for i in range(15):
        neighbors=sorted(j for a,b in edges for j in ([b] if a==i else [a] if b==i else []))
        require(len(neighbors)>=2,'no low-degree vertex')
        reference=neighbors[0]
        def half(j):
            s=det(V[i],V[reference],V[j]).sign()
            if s: return 0 if s>0 else 1
            d=(dot(V[reference],V[j])-T*T).sign()
            require(d!=0,'nonzero reference tangent direction')
            return 0 if d>0 else 1
        def compare(a,b):
            if a==b:return 0
            ha,hb=half(a),half(b)
            if ha!=hb:return -1 if ha<hb else 1
            s=det(V[i],V[a],V[b]).sign()
            require(s!=0,'distinct tangent rays within a half circle')
            return -s
        order=sorted(neighbors,key=cmp_to_key(compare))
        require(order[0]==reference,'reference first')
        rotation[i]=order
        for j,k in combinations(neighbors,2):
            orientation_records.append([i,j,k,det(V[i],V[j],V[k]).sign(),(dot(V[j],V[k])-T*T).sign()])
    darts={(i,j) for a,b in edges for i,j in ((a,b),(b,a))}
    visited=set();faces=[]
    for start in sorted(darts):
        if start in visited:continue
        now=start;walk=[]
        while now not in visited:
            visited.add(now);i,j=now;walk.append(i)
            order=rotation[j]; k=order[(order.index(i)-1)%len(order)]
            now=(j,k)
        require(now==start,'face permutation closed orbit')
        require(len(walk)==len(set(walk)),'all physical boundary walks simple')
        faces.append(canonical(walk))
    require(visited==darts,'all directed contact arcs used once')
    require(15-len(edges)+len(faces)==2,'spherical Euler identity')
    face_set=set(faces)
    forward=all(canonical(list(t)) in face_set for t in TRIANGLES+(PENTAGON,))
    backward=all(canonical(list(reversed(t))) in face_set for t in TRIANGLES+(PENTAGON,))
    convex=[]
    for face in faces:
        turns=[det(V[face[k-1]],V[face[k]],V[face[(k+1)%len(face)]]).sign() for k in range(len(face))]
        # A left face has angle below pi precisely for a strictly positive turn.
        convex.append({'cycle':list(face),'turn_signs':turns,'strictly_convex':all(s>0 for s in turns)})
    return {'edges':[list(e) for e in edges],'edge_count':len(edges),
            'rotation':{str(i):rotation[i] for i in range(15)},
            'faces':[list(f) for f in sorted(faces)],'face_count':len(faces),
            'face_length_counts':dict(sorted(Counter(map(len,faces)).items())),
            'degree_counts':dict(sorted(Counter(map(len,rotation.values())).items())),
            'motif_all_faces_forward':forward,'motif_all_faces_backward':backward,
            'motif_unoriented_faces':all(unoriented(t) in {unoriented(f) for f in faces} for t in TRIANGLES+(PENTAGON,)),
            'convexity':convex,'orientation_sign_records':orientation_records,
            'noncontact_pairs':[list(p) for p,s in pair_signs.items() if s<0]}

def main():
    root_derivative=verify_root();V,alt=construction()
    left=chart(V);W=V[:14]+[alt];right=chart(W)
    data={'actual_agent':'six-tammes-1','role':'researcher','status':'exact labelled face computation, geometric bridge recorded separately',
          'root_derivative_lower':root_derivative,'construction_reconstructed_and_compared':True,
          'pinned_inputs':json.loads((ROOT/'inputs/PINS.json').read_text()),
          'asymmetric':left,'cyclic_alternative_common_labels':right}
    out=json.dumps(data,sort_keys=True,indent=2)+'\n'
    require((ROOT/'FACE_CHART.json').read_text()==out,'exact regeneration of the included face chart')
    print(json.dumps({'sha256':hashlib.sha256(out.encode()).hexdigest(),
           'asymmetric':{k:v for k,v in left.items() if k not in ('orientation_sign_records','noncontact_pairs','rotation','convexity')},
           'cyclic_alternative':{k:v for k,v in right.items() if k not in ('orientation_sign_records','noncontact_pairs','rotation','convexity')}},sort_keys=True))

if __name__=='__main__':main()
