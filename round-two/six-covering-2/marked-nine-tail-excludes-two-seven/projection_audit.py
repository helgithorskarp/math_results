"""CRT-product and reachable-count dynamic program audit; no producer import."""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from math import gcd
from pathlib import Path


def reconstruct(cap):
    literal=((8,0),(9,0),(10,1),(14,0),(12,10),(16,2),(28,4),(32,6))
    if cap['domain']['literal_prefix']!=list(map(list,literal)) or cap['uniform_parent6_upper']>=117:
        raise ValueError('Literal predecessor domain mismatch')
    prefix=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
    grid_rows=[];physical=set()
    for branch,axis in ((0,(3,6)),(2,(2,5,8))):
        triples=[]
        for z,f,s in product(axis,range(5),range(1,7)):
            residues=(6,z,f,s);moduli=(8,9,5,7)
            x=sum(a*(2520//m)*pow(2520//m,-1,m) for a,m in zip(residues,moduli))%2520
            if x%8!=6 or x%3!=branch or any(x%m==a for m,a in prefix):
                raise ValueError('CRT point fails original literal constraints')
            physical.add(x);triples.append([x%9,x%5,x%7])
        grid_rows.append([branch,sorted(triples)])
    covered=set()
    for m,a in prefix:covered.update(range(a,2520,m))
    if physical!=set(range(6,2520,8))-covered:
        raise ValueError('Product-grid construction is not the whole original parent')
    C={d:max(values) for d,values in cap['all_single_phase_populations']}
    U={tuple(g):v for g,v in cap['all_partition_union_upper_bounds']}
    def lcm(a,b):return a*b//gcd(a,b)
    @lru_cache(None)
    def projection_union(group,branch):
        sizes=(2 if branch==0 else 3,5,6);N=sizes[0]*sizes[1]*sizes[2]
        reachable={(0,0,0)}
        for d in group:
            options=[]
            if d%9==0:options.append(0)
            if d%5==0:options.append(1)
            if d%7==0:options.append(2)
            if d==3:return N
            if not options:raise ValueError('Invalid projected original cofactor')
            next_counts=set()
            for vector in reachable:
                for axis in options:
                    value=list(vector);value[axis]+=1;next_counts.add(tuple(value))
            reachable=next_counts
        best=N
        for x,y,z in reachable:
            uncovered=max(0,sizes[0]-x)*max(0,sizes[1]-y)*max(0,sizes[2]-z)
            best=min(best,N-uncovered)
        return best
    inventories=[];roles=0;coupled=0;maximum=0;high=[];groups=set()
    for index,(H,Q,_,_) in enumerate(cap['survivors_ge87']):
        H=tuple(H);Q=tuple(Q);all_labels=H+Q
        positions=[i for i,d in enumerate(all_labels) if d%3==0]
        rows=[]
        for hroles in product((0,1),repeat=len(H)):
            h0=tuple(d for d,r in zip(H,hroles) if r==0)
            h1=tuple(d for d,r in zip(H,hroles) if r==1)
            for qroles in product((0,1,2),repeat=len(Q)):
                roles+=1
                q0=tuple(d for d,r in zip(Q,qroles) if r==0)
                q1=tuple(d for d,r in zip(Q,qroles) if r==1)
                q2=tuple(d for d,r in zip(Q,qroles) if r==2)
                if not q2:
                    coarse=0
                else:
                    shared=min(U[q0],U[q1],sum(C[lcm(a,b)] for a in q0 for b in q1))
                    coarse=min(150,U[h0]+shared,U[h1]+U[q2])
                entries=[]
                if coarse>=87:
                    for residues in product((0,2),repeat=len(positions)):
                        phase_branch=dict(zip(positions,residues));bounds=[]
                        for branch in (0,2):
                            active_h=[[],[]];active_q=[[],[],[]]
                            for i,d in enumerate(all_labels):
                                if d%3==0 and phase_branch[i]!=branch:continue
                                if i<len(H):active_h[hroles[i]].append(d)
                                else:active_q[qroles[i-len(H)]].append(d)
                            intersections=[lcm(a,b) for a in active_q[0] for b in active_q[1]]
                            opposite=tuple(sorted(active_h[0]+intersections))
                            same=tuple(sorted(active_h[1]+active_q[2]))
                            a=projection_union(opposite,branch);b=projection_union(same,branch)
                            groups.add((opposite,branch));groups.add((same,branch))
                            bounds.append([branch,list(opposite),list(same),a,b,min(a,b)])
                        bound=min(coarse,bounds[0][-1]+bounds[1][-1])
                        entries.append([list(residues),bounds,bound]);coupled+=1
                        maximum=max(maximum,bound)
                        if bound>=87:high.append([index,list(hroles),list(qroles),list(residues),bound])
                else:maximum=max(maximum,coarse)
                rows.append([list(hroles),list(qroles),coarse,entries])
        inventories.append({'H':list(H),'Q':list(Q),'branch_positions':positions,'all_role_rows':rows})
    return {'agent':'six-covering-2','role':'researcher','schema':1,'stage':'two-seven-projection',
        'domain':{'minimum_exactly':8,'original_moduli_divide':10080,'literal_prefix':list(map(list,literal)),
                  'essential_originals':[16,32],'productive_TAILs_exactly':9,'counts_in_actual_hole_parents2_6':[2,7],
                  'BASE_lower_bound_imported':177,'parent2_original48_phase26_forced_by_checked_predecessors':True,
                  'productive_parent6_extras_exactly':6,'essential32_requires_missing_same_half_Q_arm':True,
                  'Q_in_placed_quarter_redundant_at_exact_minimum_count':True,
                  'cofactor_divisible_by3_productive_branch_choices':[0,2],
                  'all_original_odd_phases_and_omissions_free':True,'cross_H_Q_equal_cofactors_legal':True,
                  'unproductive_selected_tails_allowed':True,'actual_LCM_may_be_proper_divisor':True,
                  'ordinary_proof_formalized':False,'independent_person_reviewed':False,'global_bound_changed':False},
        'literal_product_grids':grid_rows,'original_six_extra_inventories':inventories,
        'all_projection_union_values':[[list(g),e,projection_union(g,e)] for g,e in sorted(groups)],
        'H_orientation_order':[14,6],'Q_quarter_order':[14,30,22],
        'inventory_count':len(inventories),'all_role_assignments':roles,'all_unpruned_mod3_phase_cases':coupled,
        'uniform_role_branch_upper':maximum,'survivors_ge87':high,'survivor_count':len(high),
        'entire_two_seven_excluded_by_projection':len(high)==0,'new_six_three_or126_numeric_input_used':False}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('capacity','reference','out'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();r=reconstruct(json.loads(a.capacity.read_text()));b=(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n').encode()
    if b!=a.reference.read_bytes():raise ValueError('Entire independently reconstructed projection record differs')
    a.out.write_bytes(b)
    print(json.dumps({'whole_record_bytes_agree':True,'inventories':r['inventory_count'],
                      'roles':r['all_role_assignments'],'coupled_cases':r['all_unpruned_mod3_phase_cases'],
                      'upper':r['uniform_role_branch_upper'],'survivors':r['survivor_count'],
                      'sha256':sha256(b).hexdigest()}))
