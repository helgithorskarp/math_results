"""Complete six-extra original H/Q inventory upper bounds in parent6."""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from math import lcm
from pathlib import Path

PREFIX=((8,0),(9,0),(10,1),(14,0),(12,10),(16,2),(28,4),(32,6))
P=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
D=tuple(d for d in range(3,316) if 315%d==0)
HPOOL=tuple(d for d in D if d!=3)
R6=tuple(x for x in range(6,2520,8) if all(x%m!=a for m,a in P))
M={d:tuple(sum(1<<i for i,x in enumerate(R6) if x%d==a) for a in range(d)) for d in D}
C={d:max(v.bit_count() for v in mm) for d,mm in M.items()}


def generate():
    pair={};pair_rows=[]
    for a,b in combinations(D,2):
        vals=[(u|v).bit_count() for u in M[a] for v in M[b]]
        pair[a,b]=max(vals);pair_rows.append([[a,b],vals,max(vals)])
    @lru_cache(None)
    def U(group):
        if not group:return 0
        a=group[0];rest=group[1:]
        return min([150,C[a]+U(rest)]+[pair[tuple(sorted((a,b)))]+U(tuple(v for v in rest if v!=b)) for b in rest])
    def subsets(group):
        for k in range(len(group)+1):
            yield from combinations(group,k)
    @lru_cache(None)
    def intersect(Q):
        best=0
        if len(Q)<2:return best
        for A in subsets(Q[1:]):
            A=(Q[0],)+A;B=tuple(v for v in Q if v not in A)
            if B:best=max(best,min(U(A),U(B),sum(C[lcm(a,b)] for a in A for b in B)))
        return best
    @lru_cache(None)
    def cuts_H(H):return tuple((A,tuple(v for v in H if v not in A),U(A),U(tuple(v for v in H if v not in A))) for A in subsets(H))
    @lru_cache(None)
    def cuts_Q(Q):return tuple((B,tuple(v for v in Q if v not in B),U(B),intersect(tuple(v for v in Q if v not in B))) for B in subsets(Q) if B)
    types=[];survivors=[];assignments=0
    for h in range(7):
        q=6-h;caps=[];high=[];witness=[]
        for H in combinations(HPOOL,h):
            for Q in combinations(D,q):
                best=0;arg=None
                for A,B,ua,ub in cuts_H(H):
                    for QB,QA,uB,iA in cuts_Q(Q):
                        cap=min(150,ua+iA,ub+uB)
                        assignments+=1
                        if cap>best:best=cap;arg=[list(A),list(B),list(QB),list(QA)]
                caps.append(best);witness.append(arg)
                if best>=87:high.append([list(H),list(Q),best,arg])
        survivors.extend(high)
        types.append({'H_count':h,'Q_count':q,'all_caps':caps,'all_maximizing_cuts':witness,
                      'maximum':max(caps),'survivors_ge87':high,'all_H_type_excluded_by_essential32':q==0})
    urows=[[list(g),U(g)] for k in range(7) for g in combinations(D,k)]
    irows=[[list(g),intersect(g)] for k in range(7) for g in combinations(D,k)]
    return {'agent':'six-covering-2','role':'researcher','schema':1,'stage':'two-seven-six-extra-capacity',
        'domain':{'minimum_exactly':8,'original_moduli_divide':10080,'literal_prefix':list(map(list,PREFIX)),
                  'essential_originals':[16,32],'productive_TAILs_exactly':9,'counts_in_actual_hole_parents2_6':[2,7],
                  'BASE_lower_bound_imported':177,'parent2_original_H48_forced_by_separate_small_certificate':True,
                  'productive_parent6_extras_exactly':6,'essential32_forces_nonempty_missing_same_half_Q_arm':True,
                  'H_original48_unavailable_globally':True,'H_pool':list(HPOOL),'Q_pool':list(D),
                  'cross_H_Q_equal_cofactors_legal':True,'same_original_label_reuse_forbidden':True,
                  'all_other_phases_selections_omissions_free':True,'unproductive_selected_tails_allowed':True,
                  'actual_LCM_may_be_proper_divisor':True,'ordinary_proof_formalized':False,
                  'independent_person_reviewed':False,'entire_two_seven_exclusion_claimed':False,'global_bound_changed':False},
        'initial_R6':list(R6),'all_single_phase_populations':[[d,[v.bit_count() for v in M[d]]] for d in D],
        'all_raw_pair_union_values':pair_rows,'all_partition_union_upper_bounds':urows,
        'all_two_Q_arm_intersection_bounds':irows,'all_types':types,'original_inventory_count':sum(len(t['all_caps']) for t in types),
        'binary_H_missing_Q_arm_cuts_checked':assignments,'uniform_parent6_upper':max(t['maximum'] for t in types),
        'survivors_ge87':survivors,'survivor_count':len(survivors),
        'required_if_parent2_48_26':87,'required_if_parent2_48_42':117,
        'phase42_excluded_by_uniform_capacity':max(t['maximum'] for t in types)<117,
        'new_six_three_126_numeric_input_used':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    d=generate();a.out.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'inventories':d['original_inventory_count'],'cuts':d['binary_H_missing_Q_arm_cuts_checked'],
                      'maximum':d['uniform_parent6_upper'],'survivors':d['survivor_count'],
                      'types':[[t['H_count'],t['Q_count'],len(t['all_caps']),t['maximum'],len(t['survivors_ge87'])] for t in d['all_types']],
                      'phase42_excluded':d['phase42_excluded_by_uniform_capacity'],'sha256':sha256(a.out.read_bytes()).hexdigest()}))
