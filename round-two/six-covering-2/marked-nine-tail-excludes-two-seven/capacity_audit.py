"""Set-union/pair-saving audit of all original inventories; no producer import."""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations,product
import json
from math import gcd
from pathlib import Path


def reconstruct():
    literal=((8,0),(9,0),(10,1),(14,0),(12,10),(16,2),(28,4),(32,6))
    prefix=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
    removed=set()
    for m,a in prefix:removed.update(range(a,2520,m))
    parent=sorted(set(range(6,2520,8))-removed)
    D=tuple(sorted({3**i*5**j*7**k for i in range(3) for j in range(2) for k in range(2)}-{1}))
    HPOOL=tuple(d for d in D if d!=3)
    families={d:tuple({x for x in parent if x%d==a} for a in range(d)) for d in D}
    C={d:max(map(len,v)) for d,v in families.items()}
    pair={};pair_rows=[]
    for a,b in combinations(D,2):
        values=[len(A)+len(B)-len(A&B) for A in families[a] for B in families[b]]
        pair[a,b]=max(values);pair_rows.append([[a,b],values,max(values)])
    @lru_cache(None)
    def saving(group):
        if len(group)<2:return 0
        a=group[0];rest=group[1:]
        return max([saving(rest)]+[C[a]+C[b]-pair[tuple(sorted((a,b)))]+saving(rest[:i]+rest[i+1:]) for i,b in enumerate(rest)])
    @lru_cache(None)
    def U(group):return min(150,sum(C[d] for d in group)-saving(group))
    @lru_cache(None)
    def I(group):
        bounds=[0]
        for flags in product((0,1),repeat=len(group)):
            if not flags or flags[0]!=0 or 1 not in flags:continue
            a=tuple(d for d,b in zip(group,flags) if b==0)
            b=tuple(d for d,c in zip(group,flags) if c==1)
            bounds.append(min(U(a),U(b),sum(C[x*y//gcd(x,y)] for x in a for y in b)))
        return max(bounds)
    @lru_cache(None)
    def hcuts(group):
        cuts=[]
        for bits in product((0,1),repeat=len(group)):
            A=tuple(d for d,b in zip(group,bits) if b==0);B=tuple(d for d,b in zip(group,bits) if b==1)
            cuts.append((A,B,U(A),U(B)))
        return sorted(cuts,key=lambda row:(len(row[0]),row[0]))
    @lru_cache(None)
    def qcuts(group):
        cuts=[]
        for bits in product((0,1),repeat=len(group)):
            same=tuple(d for d,b in zip(group,bits) if b==0)
            other=tuple(d for d,b in zip(group,bits) if b==1)
            if same:cuts.append((same,other,U(same),I(other)))
        return sorted(cuts,key=lambda row:(len(row[0]),row[0]))
    types=[];survivors=[];assignments=0
    for h in range(7):
        q=6-h;caps=[];witness=[];high=[]
        for H in combinations(HPOOL,h):
            for Q in combinations(D,q):
                maximum=0;arg=None
                for A,B,u,v in hcuts(H):
                    for QB,QA,w,i in qcuts(Q):
                        bound=min(150,u+i,v+w);assignments+=1
                        if bound>maximum:maximum=bound;arg=[list(A),list(B),list(QB),list(QA)]
                caps.append(maximum);witness.append(arg)
                if maximum>=87:high.append([list(H),list(Q),maximum,arg])
        survivors.extend(high)
        types.append({'H_count':h,'Q_count':q,'all_caps':caps,'all_maximizing_cuts':witness,
                      'maximum':max(caps),'survivors_ge87':high,'all_H_type_excluded_by_essential32':q==0})
    union_rows=[[list(g),U(g)] for k in range(7) for g in combinations(D,k)]
    inter_rows=[[list(g),I(g)] for k in range(7) for g in combinations(D,k)]
    return {'agent':'six-covering-2','role':'researcher','schema':1,'stage':'two-seven-six-extra-capacity',
        'domain':{'minimum_exactly':8,'original_moduli_divide':10080,'literal_prefix':list(map(list,literal)),
                  'essential_originals':[16,32],'productive_TAILs_exactly':9,'counts_in_actual_hole_parents2_6':[2,7],
                  'BASE_lower_bound_imported':177,'parent2_original_H48_forced_by_separate_small_certificate':True,
                  'productive_parent6_extras_exactly':6,'essential32_forces_nonempty_missing_same_half_Q_arm':True,
                  'H_original48_unavailable_globally':True,'H_pool':list(HPOOL),'Q_pool':list(D),
                  'cross_H_Q_equal_cofactors_legal':True,'same_original_label_reuse_forbidden':True,
                  'all_other_phases_selections_omissions_free':True,'unproductive_selected_tails_allowed':True,
                  'actual_LCM_may_be_proper_divisor':True,'ordinary_proof_formalized':False,
                  'independent_person_reviewed':False,'entire_two_seven_exclusion_claimed':False,'global_bound_changed':False},
        'initial_R6':parent,'all_single_phase_populations':[[d,list(map(len,families[d]))] for d in D],
        'all_raw_pair_union_values':pair_rows,'all_partition_union_upper_bounds':union_rows,
        'all_two_Q_arm_intersection_bounds':inter_rows,'all_types':types,'original_inventory_count':sum(len(t['all_caps']) for t in types),
        'binary_H_missing_Q_arm_cuts_checked':assignments,'uniform_parent6_upper':max(t['maximum'] for t in types),
        'survivors_ge87':survivors,'survivor_count':len(survivors),
        'required_if_parent2_48_26':87,'required_if_parent2_48_42':117,
        'phase42_excluded_by_uniform_capacity':max(t['maximum'] for t in types)<117,
        'new_six_three_126_numeric_input_used':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--reference',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();r=reconstruct();b=(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n').encode()
    if b!=a.reference.read_bytes():raise ValueError('Entire independently reconstructed inventory record differs')
    a.out.write_bytes(b)
    print(json.dumps({'all_record_bytes_agree':True,'inventories':r['original_inventory_count'],
                      'cuts':r['binary_H_missing_Q_arm_cuts_checked'],'maximum':r['uniform_parent6_upper'],
                      'survivors':r['survivor_count'],'sha256':sha256(b).hexdigest()}))
