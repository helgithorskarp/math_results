"""Literal colored-spine corroboration of the four stated terminal cores."""
from itertools import combinations
import time

ROOT_NEIGHBORHOOD=((1,8,9),(0,),(6,7),(4,5),(3,7,9),(3,6,8),(2,5,9),(2,4,8),(0,5,7),(0,4,6))
X=tuple(range(3,9));END=tuple(range(9,16));VAR=X+END
def build(core,swapped,mapping=None):
    if core not in (0,1) or not isinstance(swapped,bool):
        raise ValueError('exactly two actual r labels and two SY row choices')
    red=[set() for _ in range(16)]
    def edge(i,j):red[i].add(j);red[j].add(i)
    map_old=(2,1,3,4,5,6,7,8,9,10) if mapping is None else tuple(mapping)
    for label,row in enumerate(ROOT_NEIGHBORHOOD):
        edge(0,map_old[label])
        for other in row:
            if label<other:edge(map_old[label],map_old[other])
    expected_cycle=((4,5),(2,3),(1,5),(1,4),(0,3),(0,2))
    if tuple(tuple(sorted(j-3 for j in red[3+i]&set(X))) for i in range(6))!=expected_cycle:
        raise RuntimeError('literal old-label/X-cycle bridge')
    if tuple(tuple(sorted(j-3 for j in red[s]&set(X))) for s in (9,10))!=((3,5),(2,4)):
        raise RuntimeError('literal old-label/SX-own bridge')
    for j in (11,12):edge(1,j)
    for j in (11,12,13,14,15):edge(2,j)
    sx=((14,15),(13,15)) if core==0 else ((13,15),(14,15))
    for s,row in zip((9,10),sx):
        for t in row:edge(s,t)
    for s,row in ((11,(14,15)),(12,(13,14))):
        for t in row:edge(s,t)
    tx=((0,1,3,5),(0,1,2,4),(0,1)) if core==0 else ((0,1,2,4),(0,1,3,5),(0,1))
    for t,row in zip((13,14,15),tx):
        for i in row:edge(t,i+3)
    sy=((0,2,3),(1,4,5))
    if swapped:sy=sy[::-1]
    for s,row in zip((11,12),sy):
        for i in row:edge(s,i+3)
    # Only u,v,a,X,SX global degrees are inputs. Derive outside SY/T degrees
    # from the forced four-regular graph on Bu=SY,T,Q.
    degrees=[10,10,9]+[10]*8
    q=[degrees[i]-len(red[i]) for i in range(11)]
    outside_known=set(range(11,16))
    for i in range(11,16):
        qi=4-len(red[i]&outside_known)
        q.append(qi);degrees.append(len(red[i])+qi)
    degrees=tuple(degrees);q=tuple(q)
    if degrees!=(10,10,9,*([10]*8),9,9,10,10,9):
        raise RuntimeError('derived actual-degree bridge')
    if q!=(0,6,0,3,3,4,4,4,4,4,4,2,2,3,2,3):raise RuntimeError(('literal degrees',core,swapped,q))
    return red,degrees,q

def columns(core,swapped):
    start=time.monotonic();red,degrees,q=build(core,swapped);answer=[]
    tight=[]
    for i,j in combinations(range(16),2):
        cap=3 if j in red[i] else degrees[i]+degrees[j]-14
        limit=cap-len(red[i]&red[j])
        if limit<0:raise RuntimeError('core pair already violates page cap')
        if limit==0:tight.append((i,j,'not_both_red'))
        if limit==q[i]+q[j]-6:tight.append((i,j,'not_both_blue'))
    for bits in range(1<<13):
        if bits%128==0 and time.monotonic()-start>30:
            raise RuntimeError('30s phase guard; incomplete')
        neighbors={1}|{VAR[k] for k in range(13) if bits>>k&1}
        sy=sum(s in neighbors for s in (11,12));ts=sum(t in neighbors for t in (13,14,15))
        h=4-sy-ts
        if ts==0 or h<0:continue
        D=len(neighbors)+h
        if any((i in neighbors and j in neighbors) if rule=='not_both_red' else (i not in neighbors and j not in neighbors) for i,j,rule in tight):continue
        for i in range(16):
            edge=i in neighbors;common=len(red[i]&neighbors)
            outside_lower=max(0,q[i]+h-(6 if edge else 5))
            cap=3 if edge else degrees[i]+D-14
            if common+outside_lower>cap:break
        else:
            answer.append({'bits':bits,'incidence':[int(i in neighbors) for i in VAR],'internal_degree':h,'actual_degree':D})
    return {'core':core,'swapped_SY':swapped,'columns':answer,'count':len(answer),'row_targets':list(q[3:]),'tight_pair_column_rules':tight,'complete':True}
