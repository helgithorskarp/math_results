"""Exact cofactor capacities and complete CRT phase-orbit certificate."""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations,product
import json
from math import lcm,prod,perm
from pathlib import Path


PREFIX=((8,0),(9,0),(10,1),(14,0),(12,10),(16,2),(28,4),(32,6))
def document(stage,values):
    return {'agent':'six-covering-2','role':'researcher','schema':1,'stage':stage,
      'status':'exact arithmetic record; ordinary conditional proof in proof.md',
      'domain':{'minimum_exactly':8,'original_moduli_divide':10080,
        'literal_prefix':list(map(list,PREFIX)),'essential_originals_explicit':[16,32],
        'productive_TAILs_exactly':9,'hole_parent_counts':[6,3],
        'BASE_lower_bound_imported':177,'productive_lower_bound_imported':9,
        'productivity':'meets an actual BASE-hole lift x+2520k, k=0,1,2,3',
        'all_other_original_phases_and_omissions_free':True,
        'unproductive_selected_TAILs_allowed':True,'proper_divisor_actual_LCM_allowed':True,
        'original_labels_preserved':True,'prior_private_pilot_as_input':False,
        'three_H_126_numerical_input_used':False,'ordinary_proof_formalized':False,
        'independent_person_reviewed':False,'new_tenth_tail_bound_claimed':False,
        'global_bound_changed':False},**values}

P=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
D=tuple(d for d in range(3,316) if 315%d==0);O=tuple(d for d in D if d!=3)
R2=tuple(x for x in range(2,2520,8) if all(x%m!=a for m,a in P));FULL=(1<<len(R2))-1
MASKS={d:tuple(sum(1<<i for i,x in enumerate(R2) if x%d==a) for a in range(d)) for d in (1,)+D}
C={d:max(v.bit_count() for v in vv) for d,vv in MASKS.items()}

def capacity():
    R6=tuple(x for x in range(6,2520,8) if all(x%m!=a for m,a in P))
    physical6=[]
    for a in range(14,48,16):
        for b in range(22,96,32):
            count=sum(all(any(n%m==phase for m,phase in ((32,6),(48,a),(96,b))) for n in (x+2520*k for k in range(4))) for x in R6)
            physical6.append([a,b,count])
    pair_rows=[];pairs={}
    for a,b in combinations(O,2):
        vals=[(u|v).bit_count() for u in MASKS[a] for v in MASKS[b]]
        pairs[a,b]=max(vals);pair_rows.append([[a,b],vals,max(vals)])
    @lru_cache(None)
    def U(H):
        if not H:return 0
        x=H[0];rest=H[1:]
        return min([150,C[x]+U(rest)]+[pairs[tuple(sorted((x,y)))]+U(tuple(z for z in rest if z!=y)) for y in rest])
    def qb(Q):
        if len(Q)<2:return 0
        best=0
        for n in range(len(Q)-1):
            for rr in combinations(Q[1:],n):
                A=(Q[0],)+rr;B=tuple(d for d in Q if d not in A)
                best=max(best,min(U(A),U(B),sum(C[lcm(a,b)] for a in A for b in B)))
        return best
    qvals={Q:qb(Q) for k in range(6) for Q in combinations(O,k)}
    alltypes=[];candidates=[]
    for h in range(6):
        vals=[];high=[];maximum=-1
        for H in combinations(O,h):
            for Q in combinations(O,5-h):
                cap=min(150,U(H)+qvals[Q]);vals.append(cap);maximum=max(maximum,cap)
                if cap>=87:high.append([list(H),list(Q),cap])
        if h!=4:candidates.extend(high)
        alltypes.append({'h':h,'q':5-h,'all_caps':vals,'maximum_parent2':maximum,'surviving_inventories':high,
                         'single_Q_redundancy_excludes_type':h==4})
    return document('capacity', {
            'prefix':list(map(list,P))+[[16,2],[32,6]],'essential_originals_explicit':[16,32],
            'minimum_exactly':8,'original_moduli_divide':10080,'count_pair':[6,3],
            'BASE177_and_nine_tail_lower_bound_imported':True,'three_H_126_numerical_input_used':False,
            'C_all_physical_phase_populations':[[d,[v.bit_count() for v in MASKS[d]]] for d in (1,)+D],
            'C_maxima':[[d,C[d]] for d in (1,)+D],'remaining_pool':list(O),'all_raw_pair_union_rows':pair_rows,
            'all_parent6_48_96_opposite_half_missing_quarter_phase_counts':physical6,
            'all_union_upper_bounds':[[list(H),U(H)] for k in range(6) for H in combinations(O,k)],
            'all_Q_arm_upper_bounds':[[list(Q),qvals[Q]] for k in range(6) for Q in combinations(O,k)],
            'all_six_parent2_types':alltypes,'phase_candidates':candidates,
            'all_non3_HQ_LCM_capacities':[[g,q,C[lcm(g,q)]] for g in D for q in D],
            'uniform_parent2_capacity':max(t['maximum_parent2'] for t in alltypes),
            'global_original_H_and_Q_distinct':True,'cross_H_Q_equalities_legal':True,'global_bound_changed':False})

def normalize(ds,phases):
    maps={5:{1:1},7:{0:0,4:4},9:{0:0}}
    available={5:[0,2,3,4],7:[1,2,3,5,6]};ba={0:[3,6],1:[1,4,7],2:[2,5,8]}
    result=[]
    for d,a in zip(ds,phases):
        parts=[]
        for p in (9 if d%9==0 else 3,5,7):
            if d%p:continue
            v=a%p
            if p==3:nv=v
            else:
                if v not in maps[p]:maps[p][v]=(ba[v%3] if p==9 else available[p]).pop(0)
                nv=maps[p][v]
            parts.append((p,nv))
        result.append(sum(v*(d//p)*pow(d//p,-1,p) for p,v in parts)%d)
    weight=perm(4,len(maps[5])-1)*perm(5,len(maps[7])-2)
    for branch in range(3):weight*=perm(2 if branch==0 else 3,sum(v%3==branch and v!=0 for v in maps[9]))
    return tuple(result),weight

def normal_tuples(ds):
    def walk(i,ph):
        if i==len(ds):yield ph,normalize(ds,ph)[1];return
        for a in range(ds[i]):
            nxt=ph+(a,)
            if normalize(ds[:i+1],nxt)[0]==nxt:yield from walk(i+1,nxt)
    return walk(0,())

def phases(cap):
    rows=[];shapes=set()
    for H,Q,_ in cap['phase_candidates']:
        H=tuple(H);Q=tuple(Q);ds=H+Q
        orientations=[bb for bb in product((0,1),repeat=len(Q)) if not Q or set(bb)=={0,1}]
        entries=[];hist=[0]*151;ehist=[0]*151;orbit_total=0
        for ph,weight in normal_tuples(ds):
            hs=[MASKS[d][a] for d,a in zip(H,ph[:len(H)])];qs=[MASKS[d][a] for d,a in zip(Q,ph[len(H):])]
            uh=0
            for v in hs:uh|=v
            for bb in orientations:
                arms=[0,0]
                for v,b in zip(qs,bb):arms[b]|=v
                inter=arms[0]&arms[1];S=uh|inter;n=S.bit_count();necessary=n>=87
                if necessary:
                    for i,v in enumerate(hs):
                        other=inter
                        for j,w in enumerate(hs):
                            if i!=j:other|=w
                        if not v&(FULL^other):necessary=False;break
                if necessary:
                    for i,(v,b) in enumerate(zip(qs,bb)):
                        other=uh
                        for j,(w,c) in enumerate(zip(qs,bb)):
                            if i!=j and b==c:other|=w
                        if not v&arms[1-b]&(FULL^other):necessary=False;break
                entries.append([list(ph),list(bb),weight,n,necessary,S if necessary else None])
                hist[n]+=weight;orbit_total+=weight
                if necessary:ehist[n]+=weight;shapes.add(S)
        expected=prod(ds)*len(orientations)
        if orbit_total!=expected:raise ValueError('Normal-form orbit census incomplete')
        rows.append({'H':list(H),'Q':list(Q),'all_canonical_phase_rows':entries,
                     'weighted_raw_histogram':hist,'weighted_essential_ge87_histogram':ehist,
                     'weighted_phase_total':orbit_total,'expected_raw_phase_total':expected,
                     'maximum_parent2':max(n for n,v in enumerate(hist) if v),
                     'essential_ge87_weight':sum(ehist)})
    return document('phases', {
            'all_inventory_phase_blocks':rows,'canonical_repair_masks':sorted(shapes),
            'canonical_shapes':len(shapes),'canonical_phase_rows':sum(len(r['all_canonical_phase_rows']) for r in rows),
            'weighted_raw_phase_rows':sum(r['weighted_phase_total'] for r in rows),
            'fixed_parent6_phases':[[48,14],[96,86]],'parent6_repair_capacity':90,
            'large_H_uniform126_used':False,'global_bound_changed':False})

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('stage',choices=('capacity','phases'));a.add_argument('--out',type=Path,required=True);a.add_argument('--capacity',type=Path)
    z=a.parse_args();r=capacity() if z.stage=='capacity' else phases(json.loads(z.capacity.read_text()))
    z.out.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'stage':z.stage,'whole_sha256':sha256(z.out.read_bytes()).hexdigest(),
                      'candidates':len(r.get('phase_candidates',[])),'uniform_parent2_capacity':r.get('uniform_parent2_capacity'),
                      'canonical_phase_rows':r.get('canonical_phase_rows'),'canonical_shapes':r.get('canonical_shapes'),
                      'weighted_raw_phase_rows':r.get('weighted_raw_phase_rows')}))
