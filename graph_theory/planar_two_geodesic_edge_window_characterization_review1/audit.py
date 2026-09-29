#!/usr/bin/env python3
"""Independent exact finite audit of the edge-window characterization.

No target code is imported.  Compares the window test with direct
two-interval coverage over 4096 small hosts, checks all 4096 deletions
of a strict planar witness, and reruns weighted and fan controls.
"""

from fractions import Fraction
from itertools import product


def graph(path_lengths, ears):
    n=len(path_lengths)+1
    edges=[(i,i+1,w) for i,w in enumerate(path_lengths)]
    ear_edges=[];next_vertex=n
    for target,lengths in ears:
        chain=[0]+list(range(next_vertex,next_vertex+len(lengths)-1))+[target]
        next_vertex+=len(lengths)-1
        ids=[]
        for u,v,w in zip(chain,chain[1:],lengths):
            ids.append(len(edges));edges.append((u,v,w))
        ear_edges.append(ids)
    return n,next_vertex,edges,ear_edges


def metric(vertices,edges,mask):
    inf=10**9
    d=[[0 if i==j else inf for j in range(vertices)] for i in range(vertices)]
    for index,(u,v,w) in enumerate(edges):
        if mask>>index & 1:
            d[u][v]=d[v][u]=min(d[u][v],w)
    for k in range(vertices):
        for i in range(vertices):
            dik=d[i][k]
            for j in range(vertices):
                via=dik+d[k][j]
                if via<d[i][j]:d[i][j]=via
    return d


def focus(n,edges,ear_ids,vertices):
    all_edges=(1<<len(edges))-1
    d=metric(vertices,edges,all_edges)
    times=[0]
    for i in range(n-1):times.append(times[-1]+edges[i][2])
    ports=sorted({0}|{edges[ids[-1]][1] for ids in ear_ids})
    windows=[]
    for i,p in enumerate(ports):
        for q in ports[i+1:]:
            delta=d[p][q]
            if delta<times[q]-times[p]:
                windows.append((p,q,Fraction(times[p]+times[q]-delta,2),
                                Fraction(times[p]+times[q]+delta,2)))
    if windows:assert max(row[2] for row in windows)<=min(row[3] for row in windows)
    return ports,windows,times


def covered(n,edges,mask,distances,times):
    start=0;components=0
    for boundary in range(n):
        if boundary<n-1 and mask>>boundary & 1:continue
        lo,hi=start,boundary
        good=distances[lo][hi]==times[hi]-times[lo]
        for cut in range(lo,hi):
            good |= (distances[lo][cut]==times[cut]-times[lo] and
                     distances[cut+1][hi]==times[hi]-times[cut+1])
        assert good,(mask,lo,hi)
        start=boundary+1
        components+=1
    assert start==n
    return components


def characterize(n,vertices,edges):
    d=metric(vertices,edges,(1<<len(edges))-1)
    t=[0]
    for i in range(n-1):t.append(t[-1]+edges[i][2])
    ports={v for u,w,_ in edges[n-1:] for v in (u,w)
           if v<n and (u>=n or w>=n)}
    windows=[]
    for p in sorted(ports):
        for q in sorted(ports):
            if p>=q:continue
            delta=d[p][q]
            if delta<t[q]-t[p]:
                windows.append((p,q,Fraction(t[p]+t[q]-delta,2),
                                Fraction(t[p]+t[q]+delta,2)))
    valid=[k for k in range(n-1)
           if all(t[k]<=upper and t[k+1]>=lower
                  for _,_,lower,upper in windows)]
    # Directly enumerate all internal geodesic intervals, not just
    # prefix/suffix cuts, to test the necessity reduction separately.
    intervals=[]
    for i in range(n):
        for j in range(i,n):
            if d[i][j]==t[j]-t[i]:
                intervals.append(sum(1<<v for v in range(i,j+1)))
    full=(1<<n)-1
    direct=any(x|y==full for x in intervals for y in intervals)
    assert bool(valid)==direct,(n,edges,windows,valid)
    return windows,valid,d,t


def host_census():
    results=[]
    for nonnegative in (False,True):
        path=[0,2,0,3] if nonnegative else [1,2,1,3]
        count=accepted=strict=0
        for mx,my,xy in product(range(32),range(32),range(2)):
            edges=[(i,i+1,w) for i,w in enumerate(path)]
            for i in range(5):
                if mx>>i&1:edges.append((i,5,(i%3) if nonnegative else 1+i%3))
                if my>>i&1:edges.append((i,6,((2*i)%4) if nonnegative else 1+(2*i)%4))
            if xy:edges.append((5,6,0 if nonnegative else 2))
            windows,valid,_,_=characterize(5,7,edges)
            accepted+=bool(valid)
            if valid and windows and max(x[2] for x in windows)>min(x[3] for x in windows):strict+=1
            count+=1
        assert count==2048 and 0<accepted<count
        results.append((count,accepted,strict))
    return results


def strict_planar_case():
    n=9;edges=[(i,i+1,1) for i in range(8)]
    edges += [(0,9,1),(9,5,1),(2,10,1),(10,8,1)]
    windows,valid,_,t=characterize(n,11,edges)
    assert {(p,q):(lo,hi) for p,q,lo,hi in windows} == {
        (0,5):(Fraction(3,2),Fraction(7,2)),
        (0,8):(Fraction(2),Fraction(6)),
        (2,8):(Fraction(4),Fraction(6))}
    assert max(x[2] for x in windows)>min(x[3] for x in windows)
    assert valid==[3]
    components=0
    for mask in range(1<<len(edges)):
        d=metric(11,edges,mask)
        components+=covered(n,edges,mask,d,t)
    assert components==20480
    # Two ears lie in opposite open half-planes of this path drawing.
    drawing={i:(2*i,0) for i in range(9)} | {9:(5,4),10:(10,-4)}
    def orient(a,b,c):
        x,y=drawing[a];u,v=drawing[b];p,q=drawing[c]
        return (u-x)*(q-y)-(v-y)*(p-x)
    for (a,b,_),(c,d,_) in product(edges,repeat=2):
        if len({a,b,c,d})<4:continue
        assert not (orient(a,b,c)*orient(a,b,d)<0 and
                    orient(c,d,a)*orient(c,d,b)<0)
    return components


def distant_case():
    edges=[(i,i+1,1) for i in range(9)]
    edges += [(0,10,1),(10,3,1),(6,11,1),(11,9,1)]
    windows,valid,_,_=characterize(10,12,edges)
    assert windows and not valid


def canonical_mask(n,ear_ids,pathmask,alive):
    mask=pathmask
    for i,ids in enumerate(ear_ids):
        if alive>>i & 1:
            mask|=sum(1<<j for j in ids)
    return mask


def representative_case(path_lengths,ears,expected_states,expected_active):
    n,vertices,edges,ear_ids=graph(path_lengths,ears)
    ports,windows,times=focus(n,edges,ear_ids,vertices)
    assert len(windows)==expected_active
    count=0
    for pathmask,alive in product(range(1<<(n-1)),range(1<<len(ears))):
        mask=canonical_mask(n,ear_ids,pathmask,alive)
        d=metric(vertices,edges,mask)
        covered(n,edges,mask,d,times)
        count+=1
    assert count==expected_states
    return n,len(ports),len(windows),count,windows


def full_deletion_case():
    lengths=[1,2,1,3,2]
    ears=[(3,[1,1]),(5,[2,1,2])]
    n,vertices,edges,ear_ids=graph(lengths,ears)
    ports,windows,times=focus(n,edges,ear_ids,vertices)
    assert ports==[0,3,5] and len(windows)==2
    assert (max(w[2] for w in windows),min(w[3] for w in windows))==(2,3)
    cache={};count=0;broken=0
    for mask in range(1<<len(edges)):
        pathmask=mask & ((1<<(n-1))-1)
        alive=sum((int(all(mask>>j & 1 for j in ids))<<i)
                  for i,ids in enumerate(ear_ids))
        key=(pathmask,alive)
        if key not in cache:
            c_mask=canonical_mask(n,ear_ids,pathmask,alive)
            cache[key]=metric(vertices,edges,c_mask)
        d=metric(vertices,edges,mask)
        assert all(d[i][j]==cache[key][i][j] for i in range(n) for j in range(n))
        covered(n,edges,mask,d,times)
        broken += any(0<sum(mask>>j & 1 for j in ids)<len(ids) for ids in ear_ids)
        count+=1
    assert count==1024 and len(cache)==128 and broken>0
    return count,len(cache),broken


def main():
    census=host_census()
    strict_components=strict_planar_case()
    distant_case()
    full,classes,broken=full_deletion_case()
    two=representative_case([1]*9,[(4,[1]*3),(8,[1]*5)],2048,2)
    assert (max(w[2] for w in two[-1]),min(w[3] for w in two[-1]))==(Fraction(3,2),Fraction(7,2))
    fan=representative_case([1]*7,[(j,[1]*(j-1)) for j in range(3,8)],4096,5)
    assert (max(w[2] for w in fan[-1]),min(w[3] for w in fan[-1]))==(Fraction(1,2),Fraction(5,2))
    print(f"host_census={census} strict_masks=4096 strict_components={strict_components} "
          f"distant_cover=NO weighted_full_masks={full} "
          f"collapsed_profiles={classes} broken_ears={broken} "
          f"unit_three_port_profiles={two[3]} fan8_profiles={fan[3]} "
          f"active_pairs=2,5 PASS")


if __name__=='__main__':main()
