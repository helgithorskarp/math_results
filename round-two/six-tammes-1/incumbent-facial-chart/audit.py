"""Direct convex-halfspace audit, independent of rotation sorting/walking.

Common exact arithmetic E is an explicit trust boundary. This is a different
geometric check, not a second arithmetic implementation or reviewer verdict.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inputs'))
from arithmetic import E,T,ZERO,ONE,verify_root

def require(p,m):
    if not p:raise ValueError(m)

def dot(x,y):
    return sum((x[i]*y[j]*(ONE if i==j else T) for i in range(3) for j in range(3)),ZERO)

def determinant(x,y,z):
    return sum((x[i]*y[j]*z[k] for i,j,k in ((0,1,2),(1,2,0),(2,0,1))),ZERO)-sum((x[i]*y[j]*z[k] for i,j,k in ((0,2,1),(1,0,2),(2,1,0))),ZERO)

def verify(data,reference):
    verify_root()
    base=[tuple(E(q) for q in p) for p in reference['incumbent_vectors']]
    alternative=tuple(E(q) for q in reference['alternate_vector'])
    records=[]
    for name,V in (('asymmetric',base),('cyclic_alternative_common_labels',base[:14]+[alternative])):
        require(len(V)==15 and all(dot(v,v)==ONE for v in V),'15 unit vertices')
        edges=set()
        for i,j in combinations(range(15),2):
            sign=(dot(V[i],V[j])-T).sign()
            require(sign<=0,'all packing inequalities')
            if sign==0:edges.add((i,j))
        chart=data[name]
        require(chart['edges']==[list(e) for e in sorted(edges)],'complete actual contact graph')
        require(chart['edge_count']==len(edges)==30,'30 contact edges')
        faces=chart['faces'];darts=Counter();supports=0;outside=0
        convex_records=[]
        for face in faces:
            require(3<=len(face)<=5 and len(set(face))==len(face),'simple3/4/5 cycle')
            require(all(type(i) is int and 0<=i<15 for i in face),'physical labels')
            center=tuple(sum((V[i][k] for i in face),ZERO) for k in range(3))
            require(all(dot(center,V[i]).sign()>0 for i in face),'face vertices in explicit open hemisphere')
            for k,i in enumerate(face):
                j=face[(k+1)%len(face)]
                require(tuple(sorted((i,j))) in edges,'all sides contacts')
                darts[(i,j)]+=1
                for other in face:
                    sign=determinant(V[i],V[j],V[other]).sign();supports+=1
                    require(sign==0 if other in (i,j) else sign>0,'strict convex inward side supports')
            turns=[determinant(V[face[k-1]],V[face[k]],V[face[(k+1)%len(face)]]).sign() for k in range(len(face))]
            convex_records.append({'cycle':face,'turn_signs':turns,'strictly_convex':True})
            for j in set(range(15))-set(face):
                require(any(determinant(V[i],V[face[(k+1)%len(face)]],V[j]).sign()<0 for k,i in enumerate(face)),'no other point in closed face polygon')
                outside+=1
            boundary={tuple(sorted((i,face[(k+1)%len(face)]))) for k,i in enumerate(face)}
            for i,j in combinations(face,2):
                if tuple(sorted((i,j))) not in boundary:
                    require(tuple(sorted((i,j))) not in edges,'no face contact diagonal')
        require(set(darts)=={(i,j) for a,b in edges for i,j in ((a,b),(b,a))} and all(n==1 for n in darts.values()),'each directed contact side exactly once')
        require(chart['face_count']==len(faces)==17 and 15-len(edges)+len(faces)==2,'Euler sphere count')
        require(chart['face_length_counts']=={'3':11,'4':3,'5':3},'declared profile')
        require(Counter(map(len,faces))==Counter({3:11,4:3,5:3}),'actual length profile')
        require(sorted(convex_records,key=lambda r:r['cycle'])==sorted(chart['convexity'],key=lambda r:r['cycle']),'turn/convexity records')
        degrees=Counter(i for e in edges for i in e)
        reached={0}
        while True:
            nxt=reached|{b if a in reached else a for a,b in edges if a in reached or b in reached}
            if nxt==reached:break
            reached=nxt
        require(len(reached)==15,'actual contact graph connected')
        require(Counter(degrees.values())==Counter({3:3,4:9,5:3}),'actual degree profile')
        require(chart['degree_counts']=={'3':3,'4':9,'5':3},'declared degrees')
        # Explicitly check the original motif, without its cached booleans.
        required=((2,10,1),(2,1,4),(2,4,8),(2,8,13),(1,10,12),(0,5,11),(0,11,6),(5,0,7),(11,5,9),(12,10,9,5,7))
        for cycle in required:
            require(any(len(face)==len(cycle) and any(tuple(face[k:]+face[:k])==cycle for k in range(len(face))) for face in faces),'original coherent facial motif')
        records.append({'name':name,'pair_checks':105,'face_side_supports':supports,'outside_vertex_exclusions':outside,'physical_faces':17,'profile':{'T':11,'Q':3,'P':3},'original_motif_faces':10})
    return records

if __name__=='__main__':
    data=json.loads((ROOT/'FACE_CHART.json').read_text())
    reference=json.loads((ROOT/'inputs/fourteen-certificate.json').read_text())
    print(json.dumps(verify(data,reference),sort_keys=True))
