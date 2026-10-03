"""Complete exact cofactor-capacity reduction for nine TAILs/three parents."""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path
from struct import pack

D=tuple(d for d in range(3,316) if 315%d==0)
PREFIX=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
ALLOC=((2,5,2),(3,4,2),(4,3,2),(2,4,3),(3,3,3),(2,3,4))

def require(ok,msg):
    if not ok:raise ValueError(msg)


def build(allocations=ALLOC,raw=None):
    full_physical_phase_populations=[]
    for r in (1,2,3,4,5,6,7):
        xs=[x for x in range(r,2520,8) if all(x%m!=a for m,a in PREFIX)]
        for d in (1,)+D:
            full_physical_phase_populations.append([r,d,[sum(x%d==a for x in xs) for a in range(d)]])
    population_by={(r,d):row for r,d,row in full_physical_phase_populations}
    for d in (1,)+D:
        require(population_by[2,d]==population_by[6,d],'Whole marked-parent phase population mismatch')
        require(all(population_by[1,d]==population_by[r,d] for r in (3,5,7)),'Whole odd-parent phase population mismatch')
    R={r:tuple(x for x in range(r,2520,8) if all(x%m!=a for m,a in PREFIX)) for r in (1,2,4,6)}
    masks={r:{d:tuple(sum(1<<i for i,x in enumerate(R[r]) if x%d==a) for a in range(d))
              for d in (1,)+D} for r in (1,2,4)}
    M={r:{d:max(m.bit_count() for m in ms) for d,ms in masks[r].items()} for r in masks}
    C=M[2]
    # Raw phase unions for the two marked parents.  Three-H group bound
    # uses the public10022 uniform126 theorem, explicitly as a dependency.
    union_rows=[]
    @lru_cache(None)
    def U(labels):
        if not labels:return 0
        if len(labels)==1:return C[labels[0]]
        if len(labels)==2:
            vals=[(a|b).bit_count() for a in masks[2][labels[0]] for b in masks[2][labels[1]]]
            if raw is not None:raw['union:'+json.dumps(labels)]=bytes(vals)
            union_rows.append([list(labels),len(vals),sha256(json.dumps(vals,separators=(',',':')).encode()).hexdigest(),max(vals)])
            return max(vals)
        require(len(labels)==3,'Only at most3 H classes used at a marked parent')
        return min(126,sum(C[d] for d in labels),min(U(tuple(q))+C[d] for d in labels for q in [tuple(e for e in labels if e!=d)]))

    @lru_cache(None)
    def P2(H,nq):
        qcap=0
        if nq>=2:
            for Q in combinations(D,nq):
                for n in range(1,nq):
                    for A in combinations(Q,n):
                        B=tuple(q for q in Q if q not in A)
                        cap=min(sum(C[q] for q in A),sum(C[q] for q in B),sum(C[lcm(a,b)] for a in A for b in B))
                        qcap=max(qcap,cap)
        return min(150,U(H)+qcap)

    local_p6=[]
    @lru_cache(None)
    def P6(H,nq):
        require(nq>0,'Essential placed32 requires at leastone further Q')
        best=-1;witness=None;rows=0;stream=sha256();values_stream=bytearray()
        for Q in combinations(D,nq):
            for hs in product((0,1),repeat=len(H)):
                O=tuple(h for h,s in zip(H,hs) if s==0)
                S=tuple(h for h,s in zip(H,hs) if s==1)
                for qs in product(range(3),repeat=nq):
                    potential=1
                    for orientation in hs:potential|=(10,5)[orientation]
                    for orientation in qs:potential|=(2,8,4)[orientation]
                    if potential!=15:
                        cap=0;row=[list(H),list(Q),list(hs),list(qs),cap]
                        stream.update(bytes((cap,)));values_stream.append(cap);rows+=1
                        if cap>best:best=cap;witness=row
                        continue
                    A=tuple(q for q,s in zip(Q,qs) if s==0)
                    B=tuple(q for q,s in zip(Q,qs) if s==1)
                    Z=tuple(q for q,s in zip(Q,qs) if s==2)
                    pair=min(sum(C[q] for q in A),sum(C[q] for q in B),sum(C[lcm(a,b)] for a in A for b in B))
                    poly=(sum(C[lcm(o,s)] for o in O for s in S)
                         +sum(C[lcm(o,z)] for o in O for z in Z)
                         +sum(C[lcm(s,a,b)] for s in S for a in A for b in B)
                         +sum(C[lcm(z,a,b)] for z in Z for a in A for b in B))
                    cap=min(U(O)+pair,U(S)+sum(C[z] for z in Z),poly,150)
                    row=[list(H),list(Q),list(hs),list(qs),cap]
                    stream.update(bytes((cap,)));values_stream.append(cap);rows+=1
                    if cap>best:best=cap;witness=row
        if raw is not None:raw['p6:'+json.dumps([H,nq])]=bytes(values_stream)
        local_p6.append([list(H),nq,best,rows,stream.hexdigest(),witness])
        return best

    local_third=[]
    @lru_cache(None)
    def PR(r,H,nq):
        N=M[r];h=len(H);best=-1;witness=None;rows=0;stream=sha256();values_stream=bytearray()
        for Q in combinations(D,nq):
            for hs in product((0,1),repeat=h):
                L=tuple(x for x,s in zip(H,hs) if s==0)
                V=tuple(x for x,s in zip(H,hs) if s==1)
                for qs in product(range(4),repeat=nq):
                    potential=0
                    for orientation in hs:potential|=(5,10)[orientation]
                    for orientation in qs:potential|=(1,4,2,8)[orientation]
                    if potential!=15:
                        cap=0;row=[list(H),list(Q),list(hs),list(qs),cap]
                        stream.update(bytes((cap,)));values_stream.append(cap);rows+=1
                        if cap>best:best=cap;witness=row
                        continue
                    arms=[tuple(q for q,s in zip(Q,qs) if s==a) for a in range(4)]
                    A,B,Z,W=arms
                    pl=min(sum(N[x] for x in A),sum(N[x] for x in B),sum(N[lcm(a,b)] for a in A for b in B))
                    pv=min(sum(N[x] for x in Z),sum(N[x] for x in W),sum(N[lcm(z,w)] for z in Z for w in W))
                    poly=(sum(N[lcm(a,b)] for a in L for b in V)
                         +sum(N[lcm(a,z,w)] for a in L for z in Z for w in W)
                         +sum(N[lcm(b,a,c)] for b in V for a in A for c in B)
                         +sum(N[lcm(a,b,z,w)] for a in A for b in B for z in Z for w in W))
                    cap=min(sum(N[x] for x in L)+pl,sum(N[x] for x in V)+pv,poly,len(R[r]))
                    row=[list(H),list(Q),list(hs),list(qs),cap]
                    stream.update(bytes((cap,)));values_stream.append(cap);rows+=1
                    if cap>best:best=cap;witness=row
        if raw is not None:raw['third:'+json.dumps([r,H,nq])]=bytes(values_stream)
        local_third.append([r,list(H),nq,best,rows,stream.hexdigest(),witness])
        return best

    cases=[];survivors=[];global_rows=0
    # Local Q pools separately retain distinct cofactors; collisions BETWEEN
    # parents are relaxed.  Every H label is globally unique across parents.
    for r in (1,4):
        for a,b,c in allocations:
            for h2 in range(a-1,-1,-1):
                q2=a-1-h2
                if a==2 and h2!=1:continue
                for h6 in range(b-1,-1,-1):
                    q6=b-1-h6
                    if q6<1:continue
                    if b==3 and (h6,q6)!=(1,1):continue
                    for hr in range(c,-1,-1):
                        qr=c-hr
                        if c==2 and hr!=2:continue
                        if c==3 and hr==0:continue
                        best=-1;witness=None;rows=0;stream=sha256();values_stream=bytearray();high=0
                        for H2 in combinations(D,h2):
                            rem=tuple(d for d in D if d not in H2)
                            for H6 in combinations(rem,h6):
                                rem2=tuple(d for d in rem if d not in H6)
                                for Hr in combinations(rem2,hr):
                                    caps=(P2(H2,q2),P6(H6,q6),PR(r,Hr,qr))
                                    cap=sum(caps);row=[list(H2),list(H6),list(Hr),list(caps),cap]
                                    stream.update(bytes((cap,)));values_stream.append(cap);rows+=1
                                    if cap>best:best=cap;witness=row
                                    if cap>=177:
                                        high+=1;survivors.append([r,[a,b,c],['H'*h2+'Q'*q2,'H'*h6+'Q'*q6,'H'*hr+'Q'*qr],row])
                        if raw is not None:raw['global:'+json.dumps([r,[a,b,c],h2,h6,hr])]=bytes(values_stream)
                        cases.append([r,[a,b,c],['H'*h2+'Q'*q2,'H'*h6+'Q'*q6,'H'*hr+'Q'*qr],best,rows,high,stream.hexdigest(),witness])
                        global_rows+=rows
    return {'agent':'six-covering-2','role':'researcher','status':'AUTHOR-CHECKED conditional exact-nine three-parent reduction; independent review pending',
            'full_marked_prefix':[[8,0],[9,0],[10,1],[14,0],[12,10],[16,2],[28,4],[32,6]],
            'minimum_exactly':8,'original_moduli_divide':10080,'essential_originals_explicit':[16,32],
            'BASE_lower177_imported_from_public9934':True,'three_H_union126_imported_from_public10022':True,
            'global_H_cofactor_distinctness_enforced':True,'count_allocations':list(map(list,allocations)),
            'capacity_streams_use_one_byte_per_exact_capacity_in_explicit_loop_order':True,'global_Q_cofactor_collisions_relaxed_between_parents':True,
            'cross_H_Q_cofactor_equalities_allowed':True,'initial_hole_parents_counts':{str(r):len(v) for r,v in R.items()},
            'all_physical_odd_phase_population_rows':full_physical_phase_populations,
            'all_capacities':{str(r):[[d,M[r][d]] for d in (1,)+D] for r in M},
            'marked_two_H_union_rows':sorted(union_rows),'all_parent6_local_capacity_rows':sorted(local_p6),
            'all_third_parent_local_capacity_rows':sorted(local_third),'all_nine_three_parent_type_cases':cases,
            'total_global_H_allocation_rows':global_rows,'surviving_relaxed_inventory_rows':survivors,
            'remaining_physical_phase_gluing_open':True,'tenth_tail_bound_claimed':False,'global_bound_changed':False,
            'ordinary_proof_formalized':False,'independent_reviewer':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--allocation',nargs=3,type=int);p.add_argument('--raw-stream',type=Path);args=p.parse_args()
    require(args.allocation is None or tuple(args.allocation) in ALLOC,'Unknown exact-nine count allocation')
    raw={} if args.raw_stream is not None else None
    record=build(raw=raw) if args.allocation is None else build((tuple(args.allocation),),raw=raw);
    if args.raw_stream is not None:
        with args.raw_stream.open('wb') as f:
            for key,data in sorted(raw.items()):
                header=key.encode();f.write(pack('>Q',len(header)));f.write(header);f.write(pack('>Q',len(data)));f.write(data)
    args.out.write_text(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'whole_sha256':sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
       'cases':len(record['all_nine_three_parent_type_cases']),'global_H_rows':record['total_global_H_allocation_rows'],
       'survivors':len(record['surviving_relaxed_inventory_rows']),'source_status':'Complete conditional capacity reduction; no tenth-tail claim'}))
