"""Separate full-entry finite audit by the same author, not peer review.
Binary H masks and ordered labeled U tuples validate the prefix/set cover.
"""
from collections import Counter
from itertools import combinations,product
import hashlib,json
import check

def raw(r):
    out=set();n4=15-2*r
    for f in product(range(r+1),repeat=5):
        if sum(f)!=r:continue
        d=sum(j*f[j] for j in range(5))
        for a in range(n4+1):
            for b in range(n4-a+1):
                if a+2*b+d==6:out.add((a,b)+f)
    return tuple(sorted(out))

def direct_h(row):
    a,b,f0,f1,f2,_,_=row
    role=[(2,False)]*a+[(3,False)]*b+[(2,True)]*f1+[(3,True)]*f2
    n=len(role);pairs=tuple(combinations(range(n),2));out=[]
    for mask in range(2**len(pairs)):
        edge={pairs[k] for k in range(len(pairs)) if mask>>k&1}
        degrees=[sum(v in e for e in edge) for v in range(n)]
        if any(degrees[v]>role[v][0] or (role[v][1] and degrees[v]!=role[v][0]) for v in range(n)):continue
        if any(all(e in edge for e in combinations(t,2)) for t in combinations(range(n),3)):continue
        out.append(mask)
    return tuple(out)

def direct_u(row,r):
    a,b,f0,f1,f2,_,_=row;capacities=[2]*a+[4]*b+[1]*f1+[2]*f2
    triples=tuple(combinations(range(len(capacities)),3));out=set()
    for ordered in product(triples,repeat=r):
        if len(set(ordered))<r:continue
        if any(sum(v>=a+b for v in t)>1 for t in ordered):continue
        if any(sum(v in t for t in ordered)>capacities[v] for v in range(len(capacities))):continue
        if any(sum(i in t and j in t for t in ordered)>2 for i,j in combinations(range(len(capacities)),2)):continue
        out.add(tuple(sorted(ordered)))
    return tuple(sorted(out))

def main():
    entries=[]
    for r in range(1,8):
        check.need(raw(r)==check.raw_profiles(r),'every raw profile compared with independent box cover')
    for r in range(1,4):
        for row in raw(r):
            if row[-1] or row[-2]:continue
            if 3*r+row[3]+2*row[4]>12:continue
            h=direct_h(row);check.need(h==check.h_masks(row),'all H graph entries compared')
            u=direct_u(row,r);check.need(u==check.u_families(row,r),'all U family entries compared')
            entries.append({'r':r,'row':row,'H_count':len(h),'H_sha256':check.digest(h),
                            'U_count':len(u),'U_sha256':check.digest(u)})
    # Three fixed H vertices, with degree caps>=2, have seven triangle-free graphs.
    check.need(direct_h((0,3,1,0,0,0,0))==(0,1,2,3,4,5,6),'three-vertex control all masks except triangle')
    print(json.dumps({'agent':'six-tammes-1','role':'researcher','algorithm':'binary H edge subsets; ordered U tuples; independent raw profile box loops',
                      'all_entries_equal':True,'raw_profiles_compared_for_r':list(range(1,8)),
                      'H_and_U_domains_compared':len(entries),'entries':entries,
                      'is_independent_mathematical_review':False},indent=2,sort_keys=True))

if __name__=='__main__':main()
