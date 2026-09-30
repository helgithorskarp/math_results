"""Independent free-face-first enumeration and direct representative transport."""
from itertools import combinations, product
from collections import Counter
import json

E=(1,5,6,11)
O=(12,13,14)
F=(0,7)
BASE=((0,1,2),(0,2,3),(0,3,4),(0,4,5),(7,6,8),(7,8,9),(7,9,10),(7,10,11))
REF_FREE={(1,12,14),(6,13,14)}
def need(ok,text):
    if not ok:raise ValueError(text)
def cycle(f):
    f=tuple(f); rev=f[::-1]
    return min(v[i:]+v[:i] for v in (f,rev) for i in range(len(v)))
def paired_rotation_cover():
    rows=[];surviving_faces=[]
    for i,j in product((1,2,3),repeat=2):
        la=[None]*5;lb=[None]*5
        la[i-1:i+2]=[2,1,3];lb[j-1:j+2]=[3,0,2]
        aa=iter((4,5));bb=iter((6,7))
        la=[next(aa) if x is None else x for x in la]
        lb=[next(bb) if x is None else x for x in lb]
        fs={tuple(sorted((f,a,b))) for f,link in [(0,la),(1,lb)] for a,b in zip(link,link[1:])}
        counts=[sum(v in tri for tri in fs) for v in (2,3)]
        rows.append({'positions':[i,j],'common_neighbor_T_counts':counts})
        if max(counts)<=2:surviving_faces.append((i,j,fs))
    need([(i,j) for i,j,_ in surviving_faces]==[(1,1),(3,3)],'nine original rotations')
    m={i:i for i in range(8)}
    for a,b in [(2,3),(4,5),(6,7)]:m[a],m[b]=b,a
    need({tuple(sorted(m[v] for v in tri)) for tri in surviving_faces[1][2]}==surviving_faces[0][2],
         'surviving paired rotations full face map')
    return rows
def run():
    roles=[]
    for ears in product((0,1),repeat=4):
        for outside in product((0,1,2),repeat=3):
            if sum(ears)+sum(outside)==6:roles.append(ears+outside)
    pairs=[]
    for faces in combinations(tuple(combinations(E+O,3)),2):
        counts=Counter(v for face in faces for v in face)
        if any(counts[v]>1 for v in E):continue
        role=tuple(counts[v] for v in E+O)
        need(role in roles,'role coverage')
        pairs.append((faces,counts))
    reject=[0,0,0]; survivors=[];raw=0
    for faces,counts in pairs:
        for qa,qb in product((6,11)+O,(1,5)+O):
            raw+=1
            tt=lambda v:counts[v]+int(v in E)
            if tt(qa)==2 or tt(qb)==2:reject[0]+=1;continue
            qfaces=[(0,1,qa,5),(7,6,qb,11)]
            allfaces=list(BASE)+list(faces)+qfaces
            neighbors=[set() for _ in range(15)]
            for face in allfaces:
                for v,w in zip(face,face[1:]+face[:1]):
                    neighbors[v].add(w);neighbors[w].add(v)
            if any(len(ns)>(5 if v in F else 4) for v,ns in enumerate(neighbors)):
                reject[1]+=1;continue
            if 5 in neighbors[1] or 11 in neighbors[6]:reject[2]+=1;continue
            promoted=[v for v in E if counts[v]]
            need(len(promoted)==2 and sum(v in (1,5) for v in promoted)==1,'one promoted per fan')
            need(qa!=qb and qa in O and qb in O,'distinct outside opposites')
            r=next(v for v in O if v not in (qa,qb))
            need(counts[qa]==counts[qb]==1 and counts[r]==2,'outside roles')
            m=list(range(15))
            if 5 in promoted:
                for a,b in [(1,5),(2,4)]:m[a],m[b]=m[b],m[a]
            if 11 in promoted:
                for a,b in [(6,11),(8,10)]:m[a],m[b]=m[b],m[a]
            m[qa],m[qb],m[r]=12,13,14
            need(set(m)==set(range(15)),'actual original label bijection')
            need({tuple(sorted(m[v] for v in face)) for face in BASE}=={tuple(sorted(f)) for f in BASE},'all fan faces')
            need({tuple(sorted(m[v] for v in face)) for face in faces}==REF_FREE,'full free-face transport')
            need({cycle(tuple(m[v] for v in face)) for face in qfaces}=={cycle((0,1,12,5)),cycle((7,6,13,11))},'cyclic Q transport')
            survivors.append({'free_Ts':[list(f) for f in faces],'QA':qa,'QB':qb,'map_to_representative':m})
    need(len(roles)==83 and len(pairs)==235 and raw==5875,'independent raw cover counts')
    need(reject==[4051,1770,30] and len(survivors)==24,'independent filtered counts')
    return {'agent':'six-reviewer-4','role':'independent mathematical reviewer','method':'enumerate free triangle pairs first; infer roles; direct fan reversal/outside transport',
            'role_assignments':len(roles),'free_T_pairs':len(pairs),'raw_cases':raw,'rejections':reject,
            'surviving_labelings':len(survivors),'survivors':survivors,
            'prerequisite_paired_rotation_cover':paired_rotation_cover()}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
