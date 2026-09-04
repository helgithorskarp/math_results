#!/usr/bin/env python3
"""Solver-free verification of every labeled coupled signature system.

Rebuilds the prior small-core universe with Gray-code neighbor sets and
literal cliques. Transports and checks certificates on every orbit member.
"""

import argparse
from collections import Counter, defaultdict
import csv
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent/'ramsey_r55_exceptional_signature_capacity'
U = {18:85,19:92,20:100,21:107,22:114,23:122,24:132}
STAGES = ('weighted','core5','total_capacity','red_capacity','blue_capacity','pass')
FIELDS = ('counts_18_to_24','M','input_cores','orbits','primal_cores','dual_cores','removed_splits')


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


@lru_cache(None)
def upper(a,b):
    return 1 if min(a,b)==1 else upper(a-1,b)+upper(a,b-1)


def target(d,M):
    return U[d]+U[42-d]-14-comb(42-d,2)+231+M-21*d


def capacities(near,ds,M):
    k,n = len(ds),43-len(ds)
    red,blue = [],[]
    for mask in range(1<<k):
        vertices = [v for v in range(k) if mask>>v&1]
        pairs = list(combinations(vertices,2))
        if all(b in near[a] for a,b in pairs): red.append((mask,len(vertices)))
        if all(b not in near[a] for a,b in pairs): blue.append((mask,len(vertices)))
    if any(size>=5 for _,size in red+blue): return None
    result = {}
    for mask in range(1<<k):
        if sum(ds[v]-21 for v in range(k) if mask>>v&1)>target(21,M): continue
        r = max(size for clique,size in red if clique&mask==clique)
        outside = ((1<<k)-1)^mask
        s = max(size for clique,size in blue if clique&outside==clique)
        if r<4 and s<4: result[mask]=min(n,upper(5-r,5-s)-1)
    return result


def universe(ds,M):
    k,n = len(ds),43-len(ds)
    edges = list(combinations(range(k),2))
    near = [set() for _ in ds]
    previous,hist,answer = 0,Counter(),{}
    for index in range(1<<len(edges)):
        mask=index^(index>>1)
        if index:
            a,b=edges[(mask^previous).bit_length()-1]
            near[a].symmetric_difference_update((b,))
            near[b].symmetric_difference_update((a,))
        previous=mask
        if any(sum(ds[j]-21 for j in near[i])>target(d,M) for i,d in enumerate(ds)): continue
        demands=[d-len(neighbors) for d,neighbors in zip(ds,near)]
        if sum((d-21)*r for d,r in zip(ds,demands))>n*target(21,M): continue
        hist['weighted']+=1
        caps=capacities(near,ds,M)
        if caps is None:
            hist['core5']+=1
            continue
        reason='pass'
        if sum(caps.values())<n: reason='total_capacity'
        else:
            for i,demand in enumerate(demands):
                if sum(c for x,c in caps.items() if x>>i&1)<demand:
                    reason='red_capacity'; break
                if sum(c for x,c in caps.items() if not(x>>i&1))<n-demand:
                    reason='blue_capacity'; break
        hist[reason]+=1
        if reason=='pass': answer[mask]=(caps,[n]+demands,tuple(frozenset(s) for s in near))
    return hist,answer


def read_payload(row,k):
    if row['kind']=='primal':
        pairs=[tuple(map(int,part.split(':'))) for part in row['payload'].split(',')]
        require(all(len(pair)==2 for pair in pairs), 'primal pair format')
        require(pairs==sorted(pairs) and len({p[0] for p in pairs})==len(pairs), 'signature order/uniqueness')
        require(all(0<=sig<1<<k and value>0 for sig,value in pairs), 'primal domain')
        return dict(pairs)
    require(row['kind']=='dual','certificate kind')
    weights=tuple(map(int,row['payload'].split(',')))
    require(len(weights)==k+1,'dual dimension')
    return weights


def check_primal(y,caps,b):
    require(set(y)<=set(caps),'forbidden signature')
    require(all(type(v) is int and 0<=v<=caps[x] for x,v in y.items()),'primal bounds')
    require(sum(y.values())==b[0],'primal total')
    for i,demand in enumerate(b[1:]):
        require(sum(v for x,v in y.items() if x>>i&1)==demand,'primal degree incidence')


def check_dual(weights,caps,b):
    require(len(weights)==len(b) and all(type(w) is int for w in weights),'dual format')
    lhs=sum(w*t for w,t in zip(weights,b))
    rhs=sum(cap*max(0,weights[0]+sum(w for i,w in enumerate(weights[1:]) if x>>i&1))
            for x,cap in caps.items())
    require(lhs>rhs,('dual inequality',lhs,rhs))


def permute_signature(x,p):
    return sum(1<<p[i] for i in range(len(p)) if x>>i&1)


def orbit_with_maps(mask,ds):
    k=len(ds);edges=list(combinations(range(k),2));index={e:i for i,e in enumerate(edges)}
    result={}
    # A different group enumeration from the generator: filter all permutations.
    for p in permutations(range(k)):
        if any(ds[i]!=ds[p[i]] for i in range(k)): continue
        image=sum(1<<index[tuple(sorted((p[i],p[j])))] for bit,(i,j) in enumerate(edges) if mask>>bit&1)
        result.setdefault(image,p)
    return result


def first_clique(adj,color):
    full=(1<<len(adj))-1
    def extend(candidates,chosen):
        if len(chosen)==5: return chosen
        while candidates.bit_count()>=5-len(chosen):
            bit=candidates&-candidates;v=bit.bit_length()-1;candidates^=bit
            neighbors=adj[v] if color else full^adj[v]^(1<<v)
            found=extend(candidates&neighbors,chosen+(v,))
            if found is not None: return found
        return None
    return extend(full,())


def complete_degrees(ds,M,near,y):
    """Construct and check one full degree-relaxation graph, NOT a Ramsey graph."""
    k=len(ds);adj=[set(s) for s in near]+[set() for _ in range(43-k)]
    next_vertex=k
    for sig,count in sorted(y.items()):
        for _ in range(count):
            for i in range(k):
                if sig>>i&1: adj[i].add(next_vertex);adj[next_vertex].add(i)
            next_vertex+=1
    require(next_vertex==43,'central count')
    residual={i:21-len(adj[i]) for i in range(k,43)}
    while any(residual.values()):
        order=sorted((i for i in residual if residual[i]>0),key=lambda i:(-residual[i],i))
        v=order[0];need=residual[v];others=order[1:need+1]
        require(len(others)==need,'degree completion failed')
        residual[v]=0
        for w in others:
            require(w not in adj[v],'duplicate completion edge')
            adj[v].add(w);adj[w].add(v);residual[w]-=1
    degrees=list(ds)+[21]*(43-k)
    require([len(s) for s in adj]==degrees,'completed global degrees')
    require(sum(degrees)//2==231+M,'completed edge count')
    for i,d in enumerate(degrees):
        require(sum(degrees[j]-21 for j in adj[i])<=target(d,M),'completed weighted inequality')
    bits=[sum(1<<j for j in neighbors) for neighbors in adj]
    color=True;bad=first_clique(bits,color)
    if bad is None: color=False;bad=first_clique(bits,color)
    require(bad is not None,'possible target witness needs standalone verification')
    require(len(set(bad))==5 and all((b in adj[a])==color for a,b in combinations(bad,2)),
            'literal non-Ramsey witness')


def load_inputs():
    files=[(PRIOR/'CENSUS.tsv','08a4a09b677031faf9dc7c7dc403e8e06e3245e39d13ca260b251a5c34ed5363'),
           (HERE.parent/'ramsey_r55_exceptional_degree_sieve/PROFILES.tsv',
            'a8bd3a7def8d719947e74601f410255856a309e7f66af0ee16227370b9a4f3fa'),
           (HERE.parent/'ramsey_r55_local_extremal_deficiency/extrema.json',
            '7233dd701f47de79c65ecccb6b06ad8f79b16b92c08cfcf73bcef1ed3b4d5b10')]
    for path,digest in files: require(sha256(path.read_bytes()).hexdigest()==digest,str(path))
    with files[0][0].open() as stream: prior=list(csv.DictReader(stream,delimiter='\t'))
    with files[1][0].open() as stream: globals_=list(csv.DictReader(stream,delimiter='\t'))
    require(len(prior)==32 and sum(int(r['pass']) for r in prior)==4937,'prior universe')
    require(len(globals_)==104 and sum(r['status']=='feasible' for r in globals_)==88,'global input')
    return prior,globals_


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,default=HERE/'CERTIFICATE.tsv')
    parser.add_argument('--emit-summary',action='store_true')
    args=parser.parse_args()
    prior,globals_=load_inputs()
    with args.certificate.open() as stream: certificate=list(csv.DictReader(stream,delimiter='\t'))
    require(len(certificate)==374,'374 orbit certificates')
    grouped=defaultdict(list)
    for row in certificate: grouped[row['counts_18_to_24']].append(row)
    require(set(grouped)=={r['counts_18_to_24'] for r in prior if int(r['pass'])},'profile coverage')
    summary=[];total=Counter();orbit_counts=Counter();removed=0;negative_profiles=0
    primal_test=dual_test=None
    for old in prior:
        counts=tuple(map(int,old['counts_18_to_24'].split(',')))
        ds=tuple(d for d,n in zip(range(18,25),counts) if d!=21 for _ in range(n))
        require(sum(counts)==43 and len(ds)==int(old['k'])<=6,'small profile dimensions')
        require(1<<comb(len(ds),2)==int(old['raw_cores']),'raw core count')
        M=int(old['M']);hist,systems=universe(ds,M)
        require(all(hist[s]==int(old[s]) for s in STAGES),'entry-level prior census replay')
        require((str(min(systems)) if systems else '-')==old['first_mask'],'prior first mask')
        if not systems: continue
        records=grouped[old['counts_18_to_24']];seen=set();tally=Counter()
        for row in records:
            require(int(row['M'])==M,'profile M')
            mask=int(row['red_mask']);require(mask in systems,'noncandidate representative')
            orbit=orbit_with_maps(mask,ds)
            require(min(orbit)==mask and len(orbit)==int(row['orbit_size']),'orbit normalization/count')
            require(set(orbit)<=systems.keys() and not seen&orbit.keys(),'orbit membership/disjointness')
            seen.update(orbit)
            payload=read_payload(row,len(ds))
            for image,p in orbit.items():
                caps,b,near=systems[image]
                if row['kind']=='primal':
                    moved={permute_signature(x,p):v for x,v in payload.items()}
                    check_primal(moved,caps,b)
                else:
                    moved=[payload[0]]+[0]*len(ds)
                    for i in range(len(ds)): moved[p[i]+1]=payload[i+1]
                    check_dual(moved,caps,b)
            caps,b,near=systems[mask]
            if row['kind']=='primal':
                complete_degrees(ds,M,near,payload)
                primal_test=(payload,caps,b)
            else: dual_test=(payload,caps,b)
            tally[row['kind']]+=len(orbit);orbit_counts[row['kind']]+=1
        require(seen==systems.keys(),'exhaustive labeled coverage')
        total.update(tally)
        splits=int(old['split_count']) if not tally['primal'] else 0
        removed+=splits;negative_profiles+=int(not tally['primal'])
        if tally['primal']: require(counts[0]==counts[6]==0,'extreme-degree corollary')
        summary.append([old['counts_18_to_24'],M,len(systems),len(records),tally['primal'],tally['dual'],splits])
    require(total==Counter(primal=4800,dual=137) and negative_profiles==8 and removed==17,'classification totals')
    excluded={r['counts_18_to_24'] for r in prior if not int(r['pass'])}
    excluded.update(row[0] for row in summary if row[4]==0)
    remaining=[r for r in globals_ if r['status']=='feasible' and r['counts_18_to_24'] not in excluded]
    require(len(remaining)==73 and sum(int(r['split_count']) for r in remaining)==290,'cumulative totals')
    gc,sc=Counter(),Counter()
    for r in remaining:
        gc[int(r['M'])]+=1;sc[int(r['M'])]+=int(r['split_count'])
    require([gc[m] for m in range(214,221)]==[1,3,7,11,15,18,18],'global M totals')
    require([sc[m] for m in range(214,221)]==[1,5,17,35,59,80,93],'split M totals')
    # Direct negative tests of the evidence predicates, with no numerical tolerance.
    y,caps,b=primal_test;bad=dict(y);bad[next(iter(bad))]+=1
    tests=[lambda:check_primal(bad,caps,b)]
    weights,dcaps,db=dual_test
    tests.append(lambda:check_dual([0]*len(weights),dcaps,db))
    for test in tests:
        try: test()
        except ValueError: continue
        raise ValueError('invalid evidence accepted')
    text='\t'.join(FIELDS)+'\n'+''.join('\t'.join(map(str,row))+'\n' for row in summary)
    if args.emit_summary:
        print(text,end='');return
    require((HERE/'SUMMARY.tsv').read_text()==text,'summary mismatch')
    print('PASS pinned inputs and full 32-profile, 209443-core marginal census replay')
    print('PASS 374 degree-preserving orbits cover all 4937 labeled input cores, with no overlap')
    print(f'PASS exact certificates: {orbit_counts["primal"]} primal orbits, {orbit_counts["dual"]} dual orbits')
    print('PASS transported certificates: 4800 integer-feasible cores, 137 real-infeasible cores')
    print('PASS eight global and 17 split exclusions; remaining candidates 73 globals, 290 splits')
    print('PASS 17 small profiles retained; all lack degree 18 and degree 24')
    print(f'PASS {orbit_counts["primal"]} explicit degree/weighted completions, each with a verified forbidden five-set')
    print('PASS altered primal and zero-dual evidence rejected')
    print('SCOPE signature counts only; 56 larger profiles unclassified; no Ramsey target witness')
    print('certificate_sha256='+sha256(args.certificate.read_bytes()).hexdigest())


if __name__=='__main__': main()
