"""Capacity-24 equality support and its 64 maximal axis extensions at a=109.

The capacity implication uses the separately DRAT-verified impossibility of
the paired five-colour prefix through110. This file checks its finite geometry.
"""
import argparse
import itertools
import json
from pathlib import Path


def path_capacity(length):
    size,previous,count,previous_count=0,0,1,1
    for _ in range(length):
        take=previous+1;skip=size
        best=max(take,skip)
        ways=(previous_count if take==best else 0)+(count if skip==best else 0)
        previous,size,previous_count,count=size,best,count,ways
    return size,count


def axis_supports():
    for square in ({36,49},{37,48}):
        for bits in itertools.product((0,1),repeat=5):
            support={12}|square
            for bit,ends,middle in zip(bits,[(38,47),(39,46),(40,45),(41,44),(42,43)],range(50,55)):
                support.update(ends if bit==0 else [middle])
            yield tuple(sorted(support))


def check():
    a=109;I=set(range(37,73));capacities=[]
    for d in range(1,23):
        value=0;count=1
        for start in range(d):
            length=len(range(start,36,d));size,ways=path_capacity(length)
            value+=size;count*=ways
        capacities.append(dict(difference=d,capacity=value,maximum_supports=count))
    assert max(row['capacity'] for row in capacities)==24
    assert [(r['difference'],r['maximum_supports']) for r in capacities if r['capacity']==24]==[(12,1)]
    C=set(range(37,49))|set(range(61,73))
    assert len(C)==24 and C<=I
    differences={(x-y)%a for x in C for y in C}
    assert differences=={0}|{u%a for d in list(range(1,12))+list(range(13,36)) for u in (d,-d)}
    assert [d for d in range(1,23) if d not in differences]==[12]
    assert all((x+y)%a not in C and (-1-x-y)%a not in C for x in C for y in C)
    J=set(range(1,a))-differences
    representatives={min(x,a-x) for x in J}
    assert representatives=={12}|set(range(36,55))
    edges=set()
    for x in J:
        for y in J:
            z=(x+y)%a
            if z in J:edges.add(frozenset({min(w,a-w) for w in (x,y,z)}-{12}))
    expected={frozenset(e) for e in [(36,37),*[(q,q+12) for q in range(36,43)],*[(q,97-q) for q in range(43,49)]]}
    assert edges==expected and all(len(edge)==2 for edge in edges)
    index={q:i for i,q in enumerate(range(36,55))}
    forbidden=[sum(1<<index[q] for q in edge) for edge in edges]
    valid=0;maximal=[]
    for mask in range(1<<19):
        if any(mask&edge==edge for edge in forbidden):continue
        valid+=1
        if all(any(((mask|1<<v)&edge)==edge for edge in forbidden) for v in range(19) if not mask>>v&1):
            maximal.append(tuple([12]+[q for q in range(36,55) if mask>>index[q]&1]))
    supports=list(axis_supports())
    assert valid==21875 and set(maximal)==set(supports) and len(supports)==64
    sizes={}
    for support in supports:
        E=set(support)|{a-q for q in support}
        assert E<=J and 12 in E and all((x+y)%a not in E for x in E for y in E)
        points={5*q for q in E}
        for q in C:
            for b in (1,2):points.update((5*q+b,545-5*q-b))
        assert all((x+y)%545 not in points for x in points for y in points)
        sizes[len(E)]=sizes.get(len(E),0)+1
    return dict(status='FINITE_BOUNDARY_AND_AXIS_COVER_VERIFIED',axis_factor=a,prefix_exclusion_endpoint=110,
                capacities=capacities,capacity_bound=24,equality_support=sorted(C),forced_axis=[12,97],
                remaining_axis_representatives=sorted(representatives),forbidden_edges=[sorted(e) for e in sorted(edges,key=lambda e:tuple(sorted(e)))],
                tested_axis_subsets=1<<19,valid_with_axis12=valid,maximal_axis_supports=[list(s) for s in supports],
                maximal_axis_support_count=64,axis_size_histogram={str(k):v for k,v in sorted(sizes.items())},
                full_schur_colouring_supplied=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    r=check();Path(args.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('maximal_axis_supports','capacities')},indent=2))
