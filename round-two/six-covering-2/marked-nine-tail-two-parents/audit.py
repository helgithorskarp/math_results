"""Independent author checker: Boolean minimal covers and literal physical sets.
Imports no producer. All arithmetic fields and ordered capacity streams rebuilt.
"""
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

def require(ok,message):
    if not ok:raise ValueError(message)


def populations():
    R={r:tuple(x for x in range(2520) if x%8==r and all(x%m!=a for m,a in PREFIX)) for r in range(8)}
    rows=[];N={}
    for r in range(1,8):
        N[r]={}
        for d in (1,)+D:
            counts=[0]*d
            for x in R[r]:counts[x%d]+=1
            rows.append([r,d,counts]);N[r][d]=max(counts)
    require([len(R[r]) for r in range(8)]==[0,224,150,224,200,224,150,224],'Physical original-parent census changed')
    return R,rows,N


@lru_cache(None)
def minimal_covers(fixed,states,needed=15):
    answer=[]
    for active in range(1<<len(states)):
        union=fixed
        for j,state in enumerate(states):
            if active&(1<<j):union|=state
        if union&needed!=needed:continue
        if any(old&active==old for old in answer):continue
        answer.append(active)
    return tuple(tuple(j for j in range(len(states)) if mask&(1<<j)) for mask in answer)


def polynomial(fixed,states,labels,N,needed=15):
    return sum(N[lcm(*(labels[j] for j in term))] if term else N[1] for term in minimal_covers(fixed,states,needed))


def binary_controls():
    # Every inactive/half/quarter pattern for each relevant local type;
    # actual original congruences realize each active footprint, and another
    # odd residue realizes an inactive footprint at the tested physical x.
    R,_,_=populations();rows=[]
    for r,placed,lengths in ((2,(16,2),range(1,4)),(6,(32,6),range(2,5)),(4,None,range(2,5))):
        x=R[r][0]
        lift_by_binary={y%32:y for y in (x+2520*k for k in range(4))}
        points=[lift_by_binary[b] for b in range(r,32,8)]
        fixed=0 if placed is None else sum(1<<j for j,y in enumerate(points) if y%placed[0]==placed[1])
        for length in lengths:
            for h in range(length,-1,-1):
                types='H'*h+'Q'*(length-h)
                dsH=iter((3,5,7,9));dsQ=iter((3,5,7,9));cofs=[next(dsH) if t=='H' else next(dsQ) for t in types]
                domains=[(0,5,10) if t=='H' else (0,1,2,4,8) for t in types]
                for states in product(*domains):
                    physical=[]
                    for t,d,state in zip(types,cofs,states):
                        two=16 if t=='H' else 32
                        j=next((j for j in range(4) if state&(1<<j)),0)
                        binary=points[j]%two;odd=x%d if state else (x+1)%d
                        phase=next(a for a in range(two*d) if a%two==binary and a%d==odd)
                        actual=sum(1<<j for j,y in enumerate(points) if y%(two*d)==phase)
                        require(actual==state,'Actual10080 four-lift state differs')
                        physical.append(actual)
                    union=fixed
                    for m in physical:union|=m
                    covered=union==15
                    # Boolean minimal covers, evaluated at all active given
                    # states, must be identical to literal four-lift coverage.
                    terms=minimal_covers(fixed,tuple(states))
                    require(covered==bool(terms),'Full Boolean/literal four-lift mismatch')
                    if r==6:
                        moved=tuple(4 if t=='Q' and state==1 else state for t,state in zip(types,states))
                        new=fixed
                        for z in moved:new|=z
                        require(not covered or new==15,'Moving an already filled quarter loses coverage')
                    rows.append([r,types,list(states),fixed,covered])
    return {'complete_rows':len(rows),'ordered_whole_control_sha256':sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest(),
            'literal_10080_binary_controls_checked':True,'all_inactive_states_included':True,'parent6_filled_quarter_move_checked':True}


def capacity_audit(allocations=ALLOC,raw=None):
    allR,poprows,Nfull=populations();R={r:allR[r] for r in (1,2,4,6)};N={r:Nfull[r] for r in (1,2,4)};C=N[2]
    footprints={d:tuple(frozenset(x for x in R[2] if x%d==a) for a in range(d)) for d in (1,)+D}
    union_rows=[]
    @lru_cache(None)
    def U(labels):
        if not labels:return 0
        if len(labels)==1:return C[labels[0]]
        if len(labels)==2:
            vals=[len(a.union(b)) for a in footprints[labels[0]] for b in footprints[labels[1]]]
            if raw is not None:raw['union:'+json.dumps(labels)]=bytes(vals)
            union_rows.append([list(labels),len(vals),sha256(json.dumps(vals,separators=(',',':')).encode()).hexdigest(),max(vals)])
            return max(vals)
        require(len(labels)==3,'At most3 marked-parent H footprints')
        return min(126,sum(C[d] for d in labels),min(U(tuple(x for x in labels if x!=d))+C[d] for d in labels))

    @lru_cache(None)
    def P2(H,nq):
        best=0
        for Q in combinations(D,nq):
            for n in range(1,nq):
                for A in combinations(Q,n):
                    B=tuple(q for q in Q if q not in A)
                    states=tuple(2 if q in A else 8 for q in Q)
                    cap=min(sum(C[q] for q in A),sum(C[q] for q in B),polynomial(0,states,Q,C,10))
                    best=max(best,cap)
        return min(150,U(H)+best)

    local_p6=[]
    @lru_cache(None)
    def P6(H,nq):
        require(nq>0,'Explicit essential32 domain')
        best=-1;witness=None;rows=0;stream=sha256();values_stream=bytearray()
        for Q in combinations(D,nq):
            for hs in product((0,1),repeat=len(H)):
                O=tuple(h for h,s in zip(H,hs) if s==0);S=tuple(h for h,s in zip(H,hs) if s==1)
                for qs in product(range(3),repeat=nq):
                    states=tuple(10 if s==0 else 5 for s in hs)+tuple((2,8,4)[s] for s in qs)
                    if not minimal_covers(1,states):
                        cap=0;row=[list(H),list(Q),list(hs),list(qs),cap]
                        stream.update(bytes((cap,)));values_stream.append(cap);rows+=1
                        if cap>best:best=cap;witness=row
                        continue
                    A=tuple(q for q,s in zip(Q,qs) if s==0);B=tuple(q for q,s in zip(Q,qs) if s==1);Z=tuple(q for q,s in zip(Q,qs) if s==2)
                    states=tuple(10 if s==0 else 5 for s in hs)+tuple((2,8,4)[s] for s in qs)
                    qstates=tuple((2,8,4)[s] for s in qs)
                    pair=min(sum(C[q] for q in A),sum(C[q] for q in B),polynomial(0,qstates,Q,C,10))
                    cap=min(U(O)+pair,U(S)+sum(C[q] for q in Z),polynomial(1,states,H+Q,C),150)
                    row=[list(H),list(Q),list(hs),list(qs),cap]
                    stream.update(bytes((cap,)));values_stream.append(cap);rows+=1
                    if cap>best:best=cap;witness=row
        if raw is not None:raw['p6:'+json.dumps([H,nq])]=bytes(values_stream)
        local_p6.append([list(H),nq,best,rows,stream.hexdigest(),witness]);return best

    local_third=[]
    @lru_cache(None)
    def PR(r,H,nq):
        N=Nfull[r];best=-1;witness=None;rows=0;stream=sha256();values_stream=bytearray()
        for Q in combinations(D,nq):
            for hs in product((0,1),repeat=len(H)):
                L=tuple(x for x,s in zip(H,hs) if s==0);V=tuple(x for x,s in zip(H,hs) if s==1)
                for qs in product(range(4),repeat=nq):
                    qstates=tuple((1,4,2,8)[s] for s in qs)
                    states=tuple(5 if s==0 else 10 for s in hs)+qstates
                    if not minimal_covers(0,states):
                        cap=0;row=[list(H),list(Q),list(hs),list(qs),cap]
                        stream.update(bytes((cap,)));values_stream.append(cap);rows+=1
                        if cap>best:best=cap;witness=row
                        continue
                    arms=[tuple(q for q,s in zip(Q,qs) if s==a) for a in range(4)];A,B,Z,W=arms
                    qstates=tuple((1,2,4,8)[s] for s in qs)
                    pl=min(sum(N[x] for x in A),sum(N[x] for x in B),polynomial(0,qstates,Q,N,3))
                    pv=min(sum(N[x] for x in Z),sum(N[x] for x in W),polynomial(0,qstates,Q,N,12))
                    # Third-parent producer halves(5,10) are interleaved in
                    # the four lift positions; map its Q arms into these.
                    qstates=tuple((1,4,2,8)[s] for s in qs)
                    states=tuple(5 if s==0 else 10 for s in hs)+qstates
                    cap=min(sum(N[x] for x in L)+pl,sum(N[x] for x in V)+pv,polynomial(0,states,H+Q,N),len(allR[r]))
                    row=[list(H),list(Q),list(hs),list(qs),cap];stream.update(bytes((cap,)));values_stream.append(cap);rows+=1
                    if cap>best:best=cap;witness=row
        if raw is not None:raw['third:'+json.dumps([r,H,nq])]=bytes(values_stream)
        local_third.append([r,list(H),nq,best,rows,stream.hexdigest(),witness]);return best

    cases=[];survivors=[];global_rows=0
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
                        values={}
                        for labels in combinations(D,h2+h6+hr):
                            for H2 in combinations(labels,h2):
                                rest=tuple(x for x in labels if x not in H2)
                                for H6 in combinations(rest,h6):
                                    Hr=tuple(x for x in rest if x not in H6)
                                    caps=(P2(H2,q2),P6(H6,q6),PR(r,Hr,qr));values[H2,H6,Hr]=caps
                        best=-1;witness=None;rows=0;high=0;stream=sha256();values_stream=bytearray()
                        for (H2,H6,Hr),caps in sorted(values.items()):
                            cap=sum(caps);row=[list(H2),list(H6),list(Hr),list(caps),cap];stream.update(bytes((cap,)));values_stream.append(cap);rows+=1
                            if cap>best:best=cap;witness=row
                            if cap>=177:high+=1;survivors.append([r,[a,b,c],['H'*h2+'Q'*q2,'H'*h6+'Q'*q6,'H'*hr+'Q'*qr],row])
                        if raw is not None:raw['global:'+json.dumps([r,[a,b,c],h2,h6,hr])]=bytes(values_stream)
                        cases.append([r,[a,b,c],['H'*h2+'Q'*q2,'H'*h6+'Q'*q6,'H'*hr+'Q'*qr],best,rows,high,stream.hexdigest(),witness]);global_rows+=rows
    return {'agent':'six-covering-2','role':'researcher','status':'AUTHOR-CHECKED conditional exact-nine three-parent reduction; independent review pending',
            'full_marked_prefix':[[8,0],[9,0],[10,1],[14,0],[12,10],[16,2],[28,4],[32,6]],
            'minimum_exactly':8,'original_moduli_divide':10080,'essential_originals_explicit':[16,32],
            'BASE_lower177_imported_from_public9934':True,'three_H_union126_imported_from_public10022':True,
            'global_H_cofactor_distinctness_enforced':True,'count_allocations':list(map(list,allocations)),
            'capacity_streams_use_one_byte_per_exact_capacity_in_explicit_loop_order':True,
            'global_Q_cofactor_collisions_relaxed_between_parents':True,'cross_H_Q_cofactor_equalities_allowed':True,
            'initial_hole_parents_counts':{str(r):len(v) for r,v in R.items()},'all_physical_odd_phase_population_rows':poprows,
            'all_capacities':{str(r):[[d,N[r][d]] for d in (1,)+D] for r in N},'marked_two_H_union_rows':sorted(union_rows),
            'all_parent6_local_capacity_rows':sorted(local_p6),'all_third_parent_local_capacity_rows':sorted(local_third),
            'all_nine_three_parent_type_cases':cases,'total_global_H_allocation_rows':global_rows,'surviving_relaxed_inventory_rows':survivors,
            'remaining_physical_phase_gluing_open':True,'tenth_tail_bound_claimed':False,'global_bound_changed':False,
            'ordinary_proof_formalized':False,'independent_reviewer':False}


def gluing_audit(raw=None):
    allR,_,_=populations();R=sorted(x for xs in allR.values() for x in xs);blocks=[]
    for r,moduli,placed,threshold in ((2,(80,144,240),(16,2),72),(6,(48,96),(32,6),90),(4,(112,336),None,15)):
        xs=list(allR[r]);points={y for x in xs for y in (x+2520*k for k in range(4))}
        phases=[list(range(r,m,8)) for m in moduli]
        congruences=[{a:frozenset(y for y in points if y%m==a) for a in aa} for m,aa in zip(moduli,phases)]
        fixed=frozenset() if placed is None else frozenset(y for y in points if y%placed[0]==placed[1])
        quartets={x:frozenset(x+2520*k for k in range(4)) for x in xs};values=[];qualifying=[]
        for aa in product(*phases):
            covered=set(fixed)
            for bag,a in zip(congruences,aa):covered.update(bag[a])
            shape=[x for x in xs if quartets[x].issubset(covered)];count=len(shape);values.append(count)
            if count>=threshold:
                require(count==threshold,'Literal parent capacity exceeds surviving inventory bound')
                qualifying.append([list(aa),shape])
        blocks.append({'parent':r,'original_moduli':list(moduli),'phase_lists':phases,'placed':placed,
                       'all_raw_phase_repair_counts':values,'capacity':max(values),'qualifying_original_phases_and_shapes':qualifying})
    combined=[];shapes=set()
    for pp in product(*(b['qualifying_original_phases_and_shapes'] for b in blocks)):
        shape=tuple(sorted(x for p in pp for x in p[1]));aa=[a for p in pp for a in p[0]]
        require(len(shape)==177 and len(set(shape))==177,'Physical177 repair shape must have no overlaps')
        combined.append([aa,list(shape)]);shapes.add(shape)
    originals=[m for m in range(8,2521) if 2520%m==0 and m not in {m for m,a in PREFIX}]
    total_hist={m:[0]*m for m in originals}
    for m in originals:
        for x in R:total_hist[m][x%m]+=1
    gluing=[]
    for xs in sorted(shapes):
        rows=[];tot=0
        for m in originals:
            protected=[0]*m
            for x in xs:protected[x%m]+=1
            values=[[protected[a],total_hist[m][a]-protected[a]] for a in range(m)]
            valid=[a for a in range(m) if protected[a]==0]
            cap=max((values[a][1] for a in valid),default=0)
            data=b''.join(pack('>HH',*v) for v in values)
            if raw is not None:raw.extend(data)
            rows.append([m,m,sha256(data).hexdigest(),valid,cap]);tot+=cap
        gluing.append({'protected_shape':list(xs),'shape_size':len(xs),'outside_holes':len(R)-len(xs),
                       'all_original_phase_blocks':rows,'sum_max_outside':tot})
    return {'agent':'six-covering-2','role':'researcher','status':'AUTHOR-CHECKED complete exceptional phase/BASE gluing; independent review pending',
            'full_marked_prefix':[[8,0],[9,0],[10,1],[14,0],[12,10],[16,2],[28,4],[32,6]],
            'originals_divide10080':True,'minimum_exactly8':True,'essential_originals_explicit':[16,32],
            'productive_inventory':[16,32,48,80,96,112,144,240,336],
            'all_parent_full_physical_phase_blocks':blocks,'all_800_original_phase_completions':combined,
            'all_400_BASE_gluing_shapes':gluing,'all_original_phase_streams_encoding':'ordered a0..m-1; big-endian unsigned16 protected then outside counts',
            'gluing_maximum':max(g['sum_max_outside'] for g in gluing),'gluing_minimum':min(g['sum_max_outside'] for g in gluing),
            'outside_required':1219,'BASE177_public9934_imported':True,'capacity_sharpness_claimed':False,
            'new_tenth_tail_bound_claimed':False,'ordinary_proof_formalized':False,'independent_reviewer':False,'global_bound_changed':False}


def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'))


def compare_whole(candidate,reference):
    require(candidate==reference,'Full mathematical record differs from independently rebuilt reference')


def damages(reference):
    candidate=json.loads(canonical(reference));cases=[]
    def damage(name,path,new):
        node=candidate
        for part in path[:-1]:node=node[part]
        key=path[-1];old=node[key];node[key]=new
        try:compare_whole(candidate,reference)
        except ValueError:cases.append(name)
        else:raise ValueError('Damage was accepted: '+name)
        finally:node[key]=old
        compare_whole(candidate,reference)
    damage('minimum-exactly-eight',['capacity','minimum_exactly'],9)
    damage('literal14zero',['capacity','full_marked_prefix',3,1],1)
    damage('literal32six',['capacity','full_marked_prefix',7,1],10)
    damage('explicit-essential32',['capacity','essential_originals_explicit'],[16])
    damage('global-original-H-distinctness',['capacity','global_H_cofactor_distinctness_enforced'],False)
    damage('allowed-cross-H-Q-equality',['capacity','cross_H_Q_cofactor_equalities_allowed'],False)
    damage('stated-Q-collision-relaxation',['capacity','global_Q_cofactor_collisions_relaxed_between_parents'],False)
    damage('whole-physical-population',['capacity','all_physical_odd_phase_population_rows',0,2,0],225)
    damage('missing-count-allocation',['capacity','count_allocations'],reference['capacity']['count_allocations'][:-1])
    damage('local-parent6-full-capacity-stream',['capacity','all_parent6_local_capacity_rows',0,4],'0'*64)
    damage('third-parent-full-capacity-stream',['capacity','all_third_parent_local_capacity_rows',0,4],'0'*64)
    damage('global-H-full-allocation-stream',['capacity','all_nine_three_parent_type_cases',0,6],'0'*64)
    damage('unique-survivor-owner',['capacity','surviving_relaxed_inventory_rows',0,0],1)
    damage('literal-phase-row',['gluing','all_parent_full_physical_phase_blocks',0,'all_raw_phase_repair_counts',0],73)
    damage('missing-literal-completion',['gluing','all_800_original_phase_completions'],reference['gluing']['all_800_original_phase_completions'][:-1])
    damage('whole-BASE-phase-stream',['gluing','all_400_BASE_gluing_shapes',0,'all_original_phase_blocks',0,2],'0'*64)
    damage('protected-shape-point',['gluing','all_400_BASE_gluing_shapes',0,'protected_shape',0],0)
    damage('outside-required1219',['gluing','outside_required'],1168)
    damage('BASE-upper1168',['gluing','gluing_maximum'],1219)
    damage('omission-validity',['gluing','all_400_BASE_gluing_shapes',0,'all_original_phase_blocks',0,3],[0])
    damage('false-tenth-tail-bound',['gluing','new_tenth_tail_bound_claimed'],True)
    damage('false-global-Lmin8-improvement',['gluing','global_bound_changed'],True)
    return {'rejected_semantic_domain_damages':cases,'positive_full_record_accepted_before_and_after_every_damage':True}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=('capacity','gluing','finish'),required=True)
    p.add_argument('--capacity',type=Path,required=True);p.add_argument('--gluing',type=Path)
    p.add_argument('--raw-stream',type=Path);p.add_argument('--producer-raw-stream',type=Path);p.add_argument('--audit-capacity',type=Path);p.add_argument('--audit-gluing',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.stage=='capacity':
        raw={} if a.raw_stream is not None else None
        reference=json.loads(canonical(capacity_audit(raw=raw)));supplied=json.loads(a.capacity.read_text())
        if a.raw_stream is not None:
            with a.raw_stream.open('wb') as f:
                for key,data in sorted(raw.items()):
                    header=key.encode();f.write(pack('>Q',len(header)));f.write(header);f.write(pack('>Q',len(data)));f.write(data)
            require(a.producer_raw_stream is not None and a.raw_stream.read_bytes()==a.producer_raw_stream.read_bytes(),'Complete raw capacity streams differ BYTE FOR BYTE')
        compare_whole(supplied,reference);a.out.write_text(canonical(reference)+'\n')
        print(canonical({'stage':'capacity','full_record_rebuilt_and_equal':True,'whole_sha256':sha256(canonical(reference).encode()).hexdigest()}))
    elif a.stage=='gluing':
        require(a.gluing is not None,'Whole producer gluing record required')
        raw=bytearray() if a.raw_stream is not None else None
        reference=json.loads(canonical(gluing_audit(raw=raw)));supplied=json.loads(a.gluing.read_text())
        if a.raw_stream is not None:
            a.raw_stream.write_bytes(raw)
            require(a.producer_raw_stream is not None and a.raw_stream.read_bytes()==a.producer_raw_stream.read_bytes(),'Every literal BASE phase count must agree BYTE FOR BYTE')
        compare_whole(supplied,reference);a.out.write_text(canonical(reference)+'\n')
        print(canonical({'stage':'gluing','full_record_rebuilt_and_equal':True,'whole_sha256':sha256(canonical(reference).encode()).hexdigest()}))
    else:
        require(a.gluing is not None and a.audit_capacity is not None and a.audit_gluing is not None,'Both separately rebuilt whole audit records required')
        reference={'capacity':json.loads(a.audit_capacity.read_text()),'gluing':json.loads(a.audit_gluing.read_text())}
        supplied={'capacity':json.loads(a.capacity.read_text()),'gluing':json.loads(a.gluing.read_text())}
        compare_whole(supplied,reference);controls=binary_controls();damage=damages(reference)
        result={'agent':'six-covering-2','role':'researcher','all_mathematical_records_rebuilt_and_equal':True,
                'capacity_whole_sha256':sha256(canonical(reference['capacity']).encode()).hexdigest(),
                'gluing_whole_sha256':sha256(canonical(reference['gluing']).encode()).hexdigest(),
                'binary_controls':controls,'damages':damage,'producer_imported':False,'same_author_different_algorithms':True,
                'ordinary_proof_formalized':False,'independent_reviewer':False,'global_bound_changed':False}
        a.out.write_text(canonical(result)+'\n');print(canonical(result))
